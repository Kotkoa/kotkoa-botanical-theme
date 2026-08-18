---
description: Phase 3 — apply one approved Shopify image plan with fail-closed checks
argument-hint: "<product-handle>"
---
Load and follow `/skill:shopify-image-seo-cycle`.

Run **Phase 3 only** for product handle `$1`.

Hard constraints:
- Abort unless plan status is exactly `approved-not-applied` and `validate_plan.py --require-approved` passes.
- Save a fresh complete `before.json` immediately before writes and compare it to the approved plan.
- Mutate this product only; never batch or continue to another product.
- Never delete files; only remove approved product references.
- Stop on any GraphQL error, `userErrors`, mismatch, or ambiguity.
- Verify Admin media, all original Files, filenames, alt text, every variant combination, and storefront gallery.
- Record mutation responses and result artifacts before marking `applied-success`.
