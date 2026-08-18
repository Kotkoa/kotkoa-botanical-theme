# Controlled Shopify image workflow

## Phase 1 — read-only audit

1. Require one exact product handle and record the user's visual observations.
2. Exchange client credentials for a temporary Admin API token without printing it.
3. Query the current product through Admin GraphQL with:
   - product ID, handle, title;
   - every media ID in gallery order, alt, image URL, dimensions, file size and status;
   - every variant ID, title, SKU and attached media IDs.
4. Save the complete response under `audits/image-seo/backups/`.
5. Inspect the live storefront with browser tools. Record how many images appear for the default variant and after every option combination. Storefront count can differ from Admin media count.
6. Compare every image visually. Use exact SHA-256 and perceptual hashes only as supporting evidence:
   - identical hash proves a duplicate;
   - different hash does not prove a unique scene;
   - variant-media association never proves duplication.
7. Reconcile the user's confirmed unique/duplicate count with hidden Admin variant-media. Explain any discrepancy explicitly.
8. Write the Markdown audit without applying changes. Include:
   - current Admin and storefront counts;
   - variants and current media;
   - keep table with proposed filename and alt;
   - detach table with exact media ID and evidence;
   - dry-run operation counts;
   - safety and rollback rules;
   - unchecked approval checklist.
9. Write `<slug>-dry-run.json` with at least:
   - `status: draft-not-applied`;
   - `productId`, `handle`, `plannedMediaCount`, `sharedVariantMediaId`;
   - `keepMediaIds`, `detachFromProductMediaIds`;
   - `variantMediaChanges` containing `variantId`, `detachMediaId`, `appendMediaId`;
   - `metadataUpdates` containing `id`, `filename`, `alt`;
   - `filesDeleted: false`, `pixelsChanged: false`.
10. Validate the plan without `--require-approved`. Report the proposed texts and stop.

### Filename and alt rules

- Preserve the original extension.
- Use lowercase descriptive hyphenated filenames; do not keyword-stuff.
- Alt describes visible content and scene naturally. Do not start with “Image of”.
- Keep alt concise, specific, and distinct between retained scenes.
- Do not optimize metadata for detached files.

## Phase 2 — human approval only

1. Read the exact audit and plan for the requested handle.
2. Apply the user's text corrections to both Markdown and `metadataUpdates` in JSON.
3. Mark only explicitly approved checklist items as `[x]`.
4. If all keep IDs, detach IDs, variant changes, filenames and alt texts are explicitly approved:
   - set plan status to `approved-not-applied`;
   - mark the Markdown dry-run `approved — not applied`.
5. Run the validator with `--require-approved`.
6. Do not call a Shopify mutation. Report that approval is recorded and stop.

## Phase 3 — single-product apply

1. Read the skill, approved Markdown, plan JSON and read-only backup.
2. Run `validate_plan.py --require-approved`. Abort on failure.
3. Query a fresh full product snapshot and save `before.json` immediately before writes.
4. Compare fresh state with the approved plan:
   - exact handle and product ID;
   - current media set contains exactly keep plus detach IDs;
   - every planned detach media is currently attached to its listed variant;
   - every append media is retained and belongs to this product.
5. Use Admin GraphQL in this order:
   1. `productVariantDetachMedia` for old variant attachments;
   2. verify zero top-level errors and zero `userErrors`;
   3. `productVariantAppendMedia` for shared retained media;
   4. verify again;
   5. one `fileUpdate` batch for approved retained metadata and `referencesToRemove` on approved duplicates.
6. Never use `fileDelete`, `productDeleteMedia`, upload APIs, or destructive file deletion.
7. Poll Admin API until state converges. Verify:
   - gallery media IDs equal `keepMediaIds` in approved order;
   - gallery count equals `plannedMediaCount`;
   - all variants have the approved media assignment;
   - every retained alt and URL filename matches the approved metadata;
   - every original file node still exists and has `READY` status.
8. Save all mutation responses, `after.json`, `files-after.json`, and `summary.json`.
9. Test storefront with browser tools:
   - exact gallery count;
   - all approved alt and filename URLs;
   - every variant/option combination uses the same cleaned gallery;
   - no duplicate scene remains.
10. Only after all checks pass:
    - set plan status `applied-success`;
    - add a result section to Markdown;
    - update the numbered queue item to completed/protected.
11. If any check fails, stop, preserve evidence, report the exact mismatch, and do not continue to another product. Restore only from the immediate `before.json` after explaining the rollback plan.

## Queue discipline

- Item 1 (Provence Lavender Pillow Cover) is completed and protected.
- A completed item stays untouched unless the user explicitly requests rollback.
- Never batch products.
- Start the next audit only after the previous product is verified or the user explicitly changes the order.
