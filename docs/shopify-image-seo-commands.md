# Shopify image SEO: three-command workflow

Project-local Pi skill: `.pi/skills/shopify-image-seo-cycle/SKILL.md`

After adding or changing these resources, run `/reload` in Pi.

## Command 1 — audit only

```text
/image-1-audit <product-handle> <your count/notes about unique images and duplicates>
```

Example:

```text
/image-1-audit lemon-blossom-gift-wrap-paper-citrus-floral-wrapping-roll 3 unique storefront images and 3 visible duplicates
```

This command is read-only. It creates the Admin backup, Markdown audit and JSON dry-run, proposes filenames and alt text, validates the media partition, and stops for review.

## Command 2 — approve or correct text

```text
/image-2-approve <product-handle> <approval or corrected filenames/alt text>
```

Example:

```text
/image-2-approve lemon-blossom-gift-wrap-paper-citrus-floral-wrapping-roll approve all texts and removals
```

This command updates local audit artifacts and runs the approval guard. It never writes to Shopify.

## Command 3 — apply one approved plan

```text
/image-3-apply <product-handle>
```

Example:

```text
/image-3-apply lemon-blossom-gift-wrap-paper-citrus-floral-wrapping-roll
```

This command fails closed unless the exact plan is approved and validated. It backs up current state, applies only that product, keeps all source files in Shopify Files, and verifies Admin API plus every storefront variant.

## Model recommendation

- Cost-efficient default for commands 1 and 2: `openai-codex/gpt-5.4-mini`, reasoning `medium`.
- Safer cost-conscious choice for command 3: `openai-codex/gpt-5.4`, reasoning `medium`.
- One-model option for all three: `openai-codex/gpt-5.4-mini`, reasoning `medium`, relying on the fail-closed validator and explicit approval gate.
- Do not use `gpt-5.3-codex-spark` for audits because its current Pi model entry has no image input.

Select through `/model`, then run `/reload` so the new skill and prompt commands are visible.
