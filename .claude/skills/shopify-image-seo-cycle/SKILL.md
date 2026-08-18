---
name: shopify-image-seo-cycle
description: |
  KOTKOA Shopify product-image SEO cycle: dedup Printify variant mockups, rename files,
  write alt text. Three gated commands — /image-1-audit <handle> [observations],
  /image-2-approve <handle> [approval or edits], /image-3-apply <handle>.
  Triggers on: image-1-audit, image-2-approve, image-3-apply, image SEO, alt text,
  дедупликация картинок, переименовать картинки товара, аудит изображений.
---

# Shopify image SEO cycle

One product handle per cycle. Artifacts in `audits/image-seo/`:
`<slug>.md`, `<slug>-dry-run.json`, `backups/<slug>-admin-readonly-<date>.json`,
`backups/<slug>-apply-<date>/{before,after,files-after,summary}.json` + mutation responses.

## Hard rules

- Never `fileDelete` / `productDeleteMedia`. Dedup = `fileUpdate.referencesToRemove` only.
- Never change pixels, dimensions, EXIF/ICC, price, copy, variants.
- Shared variant-media ≠ proof of visual duplicate. Prove duplicates by SHA-256 + visual check.
- Keep different size/aspect/finish/scene images unless user explicitly approves removal.
- Phase 1 and 2 do zero writes. Phase 3 requires status `approved-not-applied` + validator pass.
- Stop on any GraphQL top-level error, `userErrors`, state mismatch, or ambiguous mapping.
- Never print `.env` values, tokens, or secrets.

## Auth (phases 1 and 3)

```bash
set -a; source .env; set +a
TOKEN=$(curl -s -X POST "https://${SHOPIFY_STORE}/admin/oauth/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=${SHOPIFY_CLIENT_ID}&client_secret=${SHOPIFY_CLIENT_SECRET}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])")
```
Write `$TOKEN` to a scratchpad file (chmod 600), never echo it. Delete it at the end.

GraphQL call shape (reuse for every query/mutation):
```bash
curl -s -X POST "https://${SHOPIFY_STORE}/admin/api/${SHOPIFY_API_VERSION}/graphql.json" \
  -H "X-Shopify-Access-Token: ${TOKEN}" -H "Content-Type: application/json" \
  -d "$(python3 -c "import json,sys; print(json.dumps({'query':sys.argv[1],'variables':json.loads(sys.argv[2])}))" "$Q" "$V")" \
  -o "$OUT"
```

Product query (used by phases 1 and 3 — save wrapped as `{"data":{...}}`):
```graphql
query { productByIdentifier(identifier:{handle:"HANDLE"}) {
  id handle title
  media(first:20){nodes{__typename id alt ... on MediaImage{status mimeType image{id url width height}}}}
  variants(first:20){nodes{id title sku media(first:5){nodes{id}}}} } }
```

## /image-1-audit `<handle>` [observations]

1. Auth, run the product query, save to `backups/<slug>-admin-readonly-<date>.json` **wrapped in `{"data": ...}`** (validator requires it).
2. Download every `image.url` with curl into the scratchpad; `shasum -a 256` all of them.
3. Build a contact sheet and **look at it** (PIL thumbnails side by side, or `montage`). Identical SHA = duplicate; different SHA ≠ unique scene — still compare visually.
4. Check the live storefront (chrome-devtools `navigate_page` + `take_snapshot`) for the default variant; note that per-variant galleries make storefront count differ from Admin count.
5. Reconcile with the user's observations. If evidence contradicts them, say so explicitly with the hashes.
6. Write `<slug>-dry-run.json`:
```json
{"status":"draft-not-applied","productId":"gid://...","handle":"...","plannedMediaCount":N,
 "sharedVariantMediaId":"<one of keepMediaIds>","keepMediaIds":[],"detachFromProductMediaIds":[],
 "variantMediaChanges":[{"variantId":"","detachMediaId":"","appendMediaId":""}],
 "metadataUpdates":[{"id":"","filename":"","alt":""}],
 "filesDeleted":false,"pixelsChanged":false}
```
   Validator constraints: keep ∪ detach must equal the backup media set exactly, no overlap;
   `plannedMediaCount == len(keep)`; one `metadataUpdates` entry per kept media; filename lowercase,
   no spaces/slashes, **original extension preserved**.
7. Write `<slug>.md`: Admin/storefront counts, variant table, hash-evidence table, keep table
   (filename + alt), detach table (media ID + evidence), op counts, rollback note, unchecked checklist.
8. Validate, then stop and report:
```bash
python3 .claude/skills/shopify-image-seo-cycle/scripts/validate_plan.py \
  audits/image-seo/<slug>-dry-run.json \
  audits/image-seo/backups/<slug>-admin-readonly-<date>.json --expected-handle <handle>
```

Filename/alt style: lowercase hyphenated, descriptive, no keyword stuffing; alt describes the visible
scene naturally, never starts with "Image of", distinct per retained scene.

## /image-2-approve `<handle>` [approval or edits]

No Shopify calls. Apply the user's text corrections to both `.md` and `metadataUpdates`.
Tick only what was explicitly approved. If keep/detach/variant changes/filenames/alt are all approved:
set `"status":"approved-not-applied"`, mark the Markdown approved, rerun the validator with
`--require-approved`, report, stop.

## /image-3-apply `<handle>`

1. Rerun validator with `--require-approved`. Abort on failure.
2. Auth, fetch a fresh snapshot → `backups/<slug>-apply-<date>/before.json`.
3. Assert against the plan before writing: handle, productId, current media set == keep ∪ detach,
   every `detachMediaId` currently attached to its variant, every `appendMediaId` in keep.
4. Mutate in this order, saving each response and checking `errors` + `userErrors` are empty after each:

```graphql
mutation($productId:ID!,$variantMedia:[ProductVariantDetachMediaInput!]!){
  productVariantDetachMedia(productId:$productId,variantMedia:$variantMedia){
    productVariants{id media(first:5){nodes{id}}} userErrors{field message}}}

mutation($productId:ID!,$variantMedia:[ProductVariantAppendMediaInput!]!){
  productVariantAppendMedia(productId:$productId,variantMedia:$variantMedia){
    productVariants{id media(first:5){nodes{id}}} userErrors{field message}}}

mutation($files:[FileUpdateInput!]!){
  fileUpdate(files:$files){files{id alt ... on MediaImage{image{url}}} userErrors{field message}}}
```
   `variantMedia` items are `{"variantId":..,"mediaIds":[..]}`. The `fileUpdate` batch carries
   `{id,filename,alt}` for each kept media **plus** `{id,referencesToRemove:[productId]}` for each
   detached media — one call.
5. Re-query → `after.json`. Assert: gallery set == `keepMediaIds`, count == `plannedMediaCount`,
   every kept media's URL filename + alt match the plan, status `READY`, variants hold the approved media.
6. Query the detached IDs via `nodes(ids:[...])` → `files-after.json`; both must still be `READY` (not deleted).
7. Storefront check with chrome-devtools on **each** changed variant URL: correct gallery, new filenames
   in image URLs, correct alt, no duplicate scene.
8. Only if everything passes: write `summary.json`, set plan `"applied-success"`, add a Result section
   to the Markdown. Delete the scratch token.
9. On any failure: stop, keep all evidence, report the exact mismatch, do not touch another product.
   Roll back only from this run's `before.json`, after explaining the plan.
