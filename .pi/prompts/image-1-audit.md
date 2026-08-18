---
description: Phase 1 — read-only Shopify product image audit
argument-hint: "<product-handle> [user observations about unique images and duplicates]"
---
Load and follow `/skill:shopify-image-seo-cycle`.

Run **Phase 1 only** for product handle `$1`.

User observations: `${@:2}`

Hard constraints:
- Read-only: do not call any Shopify mutation.
- Inspect both Admin media and storefront behavior for every variant combination.
- Produce the Markdown audit, machine-readable dry-run plan, backup, and validator result.
- Propose filenames and alt text for human review.
- Stop after reporting the proposed texts and exact keep/detach media positions.
