---
description: Phase 2 — record human approval for one Shopify image audit
argument-hint: "<product-handle> <approved items or corrected texts>"
---
Load and follow `/skill:shopify-image-seo-cycle`.

Run **Phase 2 only** for product handle `$1`.

Human approval/corrections: `${@:2}`

Hard constraints:
- Update only that product's audit Markdown and dry-run JSON.
- Keep Markdown metadata and JSON `metadataUpdates` identical.
- Mark only explicitly approved items.
- Set `approved-not-applied` only when every required item is approved and validation passes.
- Do not call any Shopify mutation.
- Stop after reporting approval status and validator output.
