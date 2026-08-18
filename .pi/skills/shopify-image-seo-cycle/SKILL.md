---
name: shopify-image-seo-cycle
description: Runs the controlled Shopify product-image workflow audit → human text/removal approval → single-product apply with backups and strict verification. Use for KOTKOA image deduplication, alt text, filenames, variant-media reassignment, rollback, and the /image-1-audit, /image-2-approve, /image-3-apply commands.
compatibility: Requires Shopify Admin credentials in the project .env, curl, jq, Python 3, and browser tools.
---

# Shopify image SEO cycle

Follow [the complete workflow](references/workflow.md). Never skip a gate.

## Non-negotiable safety rules

- Work on exactly one product handle per cycle.
- Invoke `learn_shopify_api` once when available; also load the Shopify Admin/API instructions available in the agent host.
- Never print `.env`, access tokens, client secrets, or full authenticated curl traces.
- Never delete Shopify Files. Deduplication uses `fileUpdate.referencesToRemove` only.
- Never change pixels, dimensions, proportions, compression, EXIF, ICC, prices, product copy, or variants.
- A variant-media association is not evidence of a visual duplicate.
- Preserve different size, aspect-ratio, finish, or scene images unless the user explicitly approves removing them.
- A live write is forbidden during audit and approval phases.
- A live write is forbidden unless the plan status is exactly `approved-not-applied` and the validator passes.
- Stop immediately on any GraphQL top-level error, `userErrors`, state mismatch, or ambiguous media mapping.

## Commands

1. `/image-1-audit <handle> [user observations]` — read-only audit and proposed text.
2. `/image-2-approve <handle> [approval or edits]` — record human approval only; no Shopify writes.
3. `/image-3-apply <handle>` — apply the approved plan to that product only, then verify Admin API and storefront.

## Required artifacts

Use `audits/image-seo/`:

- `<slug>.md` — human-readable audit and approval checklist.
- `<slug>-dry-run.json` — machine-readable plan and status.
- `backups/<slug>-admin-readonly-<date>.json` — audit snapshot.
- `backups/<slug>-apply-<date>/before.json` — immediate pre-write snapshot.
- mutation responses, `after.json`, `files-after.json`, and `summary.json` in the apply directory.

Before phase 3 run:

```bash
python3 .pi/skills/shopify-image-seo-cycle/scripts/validate_plan.py \
  audits/image-seo/<slug>-dry-run.json \
  audits/image-seo/backups/<slug>-admin-readonly-<date>.json \
  --expected-handle <handle> \
  --require-approved
```

A successful validator is necessary but not sufficient: still obtain a fresh snapshot and compare it with the approved plan before every mutation.
