# AGENTS.md

## Project

`kotkoa-botanical-theme` is the Shopify theme for **kotkoa.com** (shop.kotkoa.com), a Printify-fulfilled microstock-themed store (pillow covers, wrapping paper, wall art, table linens, bags, digital collections — botanical/nature imagery from the owner's own microstock photography).

- Products are print-on-demand via Printify: variants are usually sizes of the same artwork, and product media often contains near-duplicate Printify mockups per size that need SEO cleanup. Read `docs/image-seo-update-plan.md` before touching product media, filenames, or alt text.
- Store domain: `shop.kotkoa.com` / Admin: `byn3vh-ew.myshopify.com`, theme id `201942892878`.
- No other project-specific conventions beyond the general Shopify theme practices below.

## Tooling

- 🚨 MANDATORY: call `learn_shopify_api` once when starting any session that touches Liquid, then use the [Shopify AI Toolkit](https://shopify.dev/docs/apps/build/ai-toolkit) for all Shopify API/platform work.
- `.pi/skills/shopify-image-seo-cycle` implements the gated, safe workflow for cleaning up **product** image filenames/alt text and deduplicating Printify variant mockups (`/image-1-audit`, `/image-2-approve`, `/image-3-apply`). Never `fileDelete` — dedup only detaches file references. A live write requires plan status exactly `approved-not-applied` and `scripts/validate_plan.py` passing.
- Admin API access is already provisioned via a Dev Dashboard app (`Kotkoa Image SEO`, client-credentials grant, scopes `read_products write_products read_files write_files`). Credentials live in `.env` (never commit, never paste into chat). Full token-exchange and read-only query recipes: `docs/image-seo-app-access.md`.

## Theme sync: two change streams

Content edited in Shopify's Theme Editor and code edited locally both live in the same theme files, and `shopify theme pull`/`push` overwrite whichever side is stale. Treat them as two streams that must not be handled out of order:

| Change type | Lives in | Rule |
|---|---|---|
| **Content** (images, block text, section settings via Theme Editor) | `templates/*.json`, `sections/*-group.json`, `config/settings_data.json` | Always `theme pull` before starting a code session. If the Editor was touched since the last sync, pull first or local edits will be pushed over it. |
| **Code** (Liquid logic, CSS, JS, section `{% schema %}`) | `sections/*.liquid`, `snippets/*.liquid`, `blocks/*.liquid`, `assets/*`, `locales/*` | Edit locally → commit → `theme push`. Do not touch the Theme Editor between starting and pushing, or the next pull will fight the code change. |

Practical flow for a code session:

```bash
# 1. pull content-only, never clobber local code
shopify theme pull --store byn3vh-ew.myshopify.com --theme 201942892878 \
  --only 'templates/*.json' --only 'sections/*.json' --only 'config/settings_data.json'
git diff --stat   # confirm only expected content changed, commit it separately
# 2. make code changes, commit
# 3. push everything (local now = remote content + local code)
shopify theme push --store byn3vh-ew.myshopify.com --theme 201942892878 --allow-live
```

Say "сначала pull" / "pull first" if the Theme Editor was used since the last sync — this must happen before any code edit, not after.

## Theme architecture

**Focus on generating snippets, blocks, and sections; users create templates/content via the theme editor.**

```
assets/     static CSS/JS/images/fonts, referenced via asset_url — keep only critical.css and
            files needed on every page; otherwise use {% stylesheet %}/{% javascript %}
blocks/     small reusable, nestable components; need {% schema %}; need {% doc %} if
            statically rendered via content_for 'block'
config/     settings_schema.json (schema) + settings_data.json (values)
layout/     theme.liquid wraps every page; must include content_for_header and content_for_layout
locales/    per-language translation files, keyed by {{ 'key' | t }}
sections/   full-width, theme-editor-customizable modules; need {% schema %}
snippets/   reusable fragments rendered via {% render %}; always need a {% doc %} header
templates/  JSON files defining which sections/blocks appear per page type
```

- `{% stylesheet %}` / `{% javascript %}` are only valid in `snippets/`, `blocks/`, `sections/`.
- Snippets and statically-rendered blocks require a `{% doc %}` header documenting params — see `docs/component-templates.md` for the exact shape and full starter templates for a snippet, a block, and a section.

## Liquid essentials

- No parentheses, no ternaries — always nested `{% if %}` for compound conditions.
- `{{ }}` outputs, `{% %}` is logic-only; `-` on either side (`{{-`, `-%}`, …) trims surrounding whitespace.
- `{% schema %}` settings: a setting that maps to **one** CSS property → output as a CSS custom property; a setting that changes **multiple** properties → output as a CSS class/modifier. Full worked examples (including the mobile-columns `select` pattern): `docs/liquid-syntax-reference.md`.
- Full filter/tag/object catalog (arrays, color, money, media, all page-scoped objects, every tag's syntax): `docs/liquid-syntax-reference.md`. Read it before guessing an unfamiliar filter signature — do not invent Liquid syntax.

## Translations

- Every user-facing string goes through `{{ 'key' | t }}`; only add English keys to `locales/en.default.json` — translators handle the rest.
- Sentence case everywhere (`Featured collection`, not `Featured Collection`).
- Escape interpolated variables unless they intentionally output HTML: `{{ variable | escape }}`.
- Hierarchical, snake_case keys, max 3 levels deep.
- File structure, schema-locale (`*.schema.json`) conventions, and full examples: `docs/translation-localization.md`.

## Reference index

- `docs/liquid-syntax-reference.md` — full Liquid syntax/filters/tags/objects + `{% schema %}` patterns.
- `docs/component-templates.md` — starter templates for snippet/block/section.
- `docs/translation-localization.md` — translation and locale-file conventions in full.
- `docs/image-seo-app-access.md` — Admin API token exchange and read-only query recipes.
- `docs/image-seo-update-plan.md` — active product image/alt-text/filename audit workflow.
- `docs/KOTKOA_THEME_ROADMAP.md` — store build/launch roadmap and status.
