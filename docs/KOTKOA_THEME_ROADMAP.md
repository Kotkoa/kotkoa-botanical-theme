---
title: Kotkoa Botanical Theme — development and store roadmap
status: active
created: 2026-08-11
reference: design/c1f00361-ea18-48a3-bdb6-29c110fb3bda.png
---

# Kotkoa Botanical Theme — development and store roadmap

## Purpose

Build and launch a production-ready Shopify storefront based on Dawn and the visual reference in `design/`. The work includes theme development, Shopify Admin configuration, responsive design, accessibility, performance, SEO, testing, and owner education.

## How progress is tracked

- `[ ]` — not started or not verified.
- `[x]` — completed and verified.
- An implementation task is complete only after all acceptance criteria (AC) for that task pass.
- Changes are developed against the Shopify development theme first. The live theme is updated only after verification.

## Current status

- [x] Shopify CLI 4.6.1 is installed.
- [x] Dawn 16.0.0 replaced the local skeleton.
- [x] The remote theme is named **Kotkoa Botanical Theme**.
- [x] The theme is available in Shopify and through `shopify theme dev`.
- [x] The local development preview responds at `http://127.0.0.1:9292`.
- [x] The obsolete skeleton backup was deleted by owner request.
- [x] `pi-chrome-dev-tools` 0.1.0 was installed globally for pi.
- [x] Reload pi and verify that the `chrome_*` browser tools are available.
- [x] Design decision: keep block 7 as a Trust strip and place a compact legal/navigation footer below it.

## Reference analysis

The desktop reference is a 1196 × 1315 px concept with:

1. Announcement bar with shipping, country, and currency information.
2. Header with search, navigation, centered logo, account, wishlist, and cart.
3. Large editorial hero.
4. Four brand feature items.
5. Four-card collection grid.
6. Split editorial area for the brand story and design library.
7. Four-item Trust strip.
8. A compact footer to be added below the reference composition.

Indicative palette extracted from the reference:

- warm background: `#EFEAE4`;
- muted olive: `#6E6652`;
- warm gray: `#B0A597`;
- light sand: `#D2C6B5`;
- lavender accent: `#CAB8C3`;
- dark brown text: `#342B22`.

These values are starting points and must be visually verified against original brand assets.

## Scope principles

- Reuse Dawn commerce behavior where possible.
- Create custom sections only when Dawn cannot reproduce the required design cleanly.
- Keep merchant content editable in Shopify Theme Editor.
- Put reusable presentation logic in snippets and editable components in sections/blocks.
- Translate all storefront UI text through Shopify locale files.
- Avoid direct changes to the live theme until a milestone passes QA.
- Treat the desktop screenshot as a visual direction, not as production-ready image assets.

---

# Stage 0 — content and design inventory

## Goal

Collect production assets and distinguish design content from Shopify store data before component development begins.

## Tasks

- [ ] Inventory every file in `design/` and record its intended use.
- [ ] Obtain the Kotkoa logo in SVG or transparent high-resolution PNG.
- [ ] Obtain separate desktop and mobile hero images.
- [ ] Obtain images for Lavender, Lemon, Tropical, and Grape & Olive collections.
- [ ] Obtain the image for “The Kotkoa world”.
- [ ] Obtain or approve a consistent SVG icon set.
- [ ] Confirm brand copy, collection names, calls to action, and links.
- [ ] Confirm shipping, return, payment, and support statements.
- [ ] Confirm social channels and contact details.
- [ ] Confirm font files and licensing, or choose Shopify-hosted alternatives.
- [ ] Record missing assets and owners in this document or a linked content checklist.

## Learning track

- [ ] Understand the difference between a design reference, production asset, theme setting, and Shopify resource.
- [ ] Understand why an image embedded in a screenshot is not suitable as a production image.
- [ ] Understand which content is managed in Theme Editor and which is managed in Shopify Admin.

## Acceptance criteria

### AC-0.1 — Asset inventory

- [ ] **Given** the current design reference and brand materials, **when** the inventory is reviewed, **then** every visible image, icon, logo, and text area has a source file or is explicitly marked missing.

### AC-0.2 — Content ownership

- [ ] **Given** all required storefront copy, **when** each content item is classified, **then** it has an identified source of truth: theme locale, Theme Editor setting, Shopify resource, metafield, menu, or policy page.

### AC-0.3 — Claims are verified

- [ ] **Given** shipping, payment, return, and support claims in the reference, **when** they are approved for publication, **then** each claim matches an actual Shopify configuration or published policy.

### AC-0.4 — Missing asset fallback

- [ ] **Given** a required asset is unavailable, **when** development reaches its component, **then** an explicit placeholder is used without extracting a low-quality image from the screenshot.

---

# Stage 1 — development foundation

## Goal

Establish Dawn, Shopify CLI, local preview, validation, browser inspection, and a safe release workflow.

## Tasks

- [x] Install Node.js and Shopify CLI.
- [x] Replace the local skeleton with Dawn 16.0.0.
- [x] Upload Dawn as a separate theme.
- [x] Rename it to **Kotkoa Botanical Theme**.
- [x] Start and verify `shopify theme dev`.
- [x] Run Shopify Theme Check.
- [x] Install `pi-chrome-dev-tools`.
- [x] Reload pi and run a browser smoke test against the local preview.
- [ ] Define Git milestone/commit conventions.
- [ ] Define the unpublished-preview-to-live release procedure.

## Learning track

- [ ] Understand what Dawn provides and why it is safer than rebuilding commerce behavior.
- [ ] Understand development, unpublished, and live theme roles.
- [ ] Understand the difference between local files, a development theme, and the live storefront.
- [ ] Understand what Theme Check validates and what it does not validate.

## Acceptance criteria

### AC-1.1 — Local preview

- [x] **Given** the local Dawn files and authenticated Shopify CLI, **when** `shopify theme dev` is running, **then** the local preview returns HTTP 200 and renders store data.

### AC-1.2 — Theme identity

- [x] **Given** the uploaded theme, **when** the Shopify theme library is opened, **then** it is listed as **Kotkoa Botanical Theme** with Dawn 16.0.0 metadata.

### AC-1.3 — Static validation

- [x] **Given** the current Dawn source, **when** Theme Check runs, **then** it completes without errors; baseline upstream warnings are documented rather than silently treated as new regressions.

### AC-1.4 — Browser tooling

- [x] **Given** pi has been reloaded after package installation, **when** the browser tools are listed and a navigation test runs, **then** `chrome_navigate`, `chrome_snapshot`, and `chrome_screenshot` can inspect `http://127.0.0.1:9292`.

### AC-1.5 — Safe release

- [ ] **Given** unfinished local changes, **when** a developer previews them, **then** they are visible in a development or unpublished theme and do not alter the live storefront until an explicit release action.

---

# Stage 2 — Kotkoa design system

## Goal

Create global visual rules before styling individual homepage sections.

## Tasks

- [ ] Define approved color schemes for warm neutral, olive accent, lavender accent, and dark contrast areas.
- [ ] Choose the heading and body font families.
- [ ] Configure typography scale and line heights.
- [ ] Configure content width and section spacing.
- [ ] Configure button, input, card, badge, and media styles.
- [ ] Upload/configure the logo and favicon.
- [ ] Define focus, hover, active, disabled, and error states.
- [ ] Record design tokens and usage rules in this document or a linked design-system file.

## Learning track

- [ ] Understand `config/settings_schema.json` versus `config/settings_data.json`.
- [ ] Understand Shopify color schemes and global theme settings.
- [ ] Understand why shared tokens reduce inconsistent one-off CSS.
- [ ] Understand the difference between a hosted Shopify font and a custom font asset.

## Acceptance criteria

### AC-2.1 — Global palette

- [ ] **Given** the approved palette, **when** global theme settings are applied, **then** background, text, buttons, cards, and form controls use named Kotkoa color schemes without section-specific duplicate color values unless justified.

### AC-2.2 — Typography

- [ ] **Given** the approved fonts, **when** representative headings and body content render, **then** typography matches the brand direction, remains legible at mobile and desktop sizes, and falls back safely if a font fails.

### AC-2.3 — Interactive states

- [ ] **Given** any interactive control, **when** it is hovered, focused by keyboard, pressed, or disabled, **then** its state is visually distinguishable and meets contrast requirements.

### AC-2.4 — Theme Editor control

- [ ] **Given** a merchant using Theme Editor, **when** supported global settings are changed, **then** the storefront updates without editing Liquid files.

---

# Stage 3 — announcement bar and header

## Goal

Reproduce the reference header while preserving Dawn search, account, localization, navigation, and cart behavior.

## Tasks

- [ ] Configure the free-shipping announcement.
- [ ] Configure main navigation menus in Shopify Admin.
- [ ] Place and size the Kotkoa logo.
- [ ] Match desktop navigation and icon layout.
- [ ] Configure country and currency selectors.
- [ ] Configure sticky-header behavior.
- [ ] Design and verify the mobile menu.
- [ ] Decide whether wishlist is omitted, app-based, or custom-built.
- [ ] Add accessible labels and focus states to icon controls.

## Learning track

- [ ] Understand section groups and `sections/header-group.json`.
- [ ] Understand Shopify menus and localization forms.
- [ ] Understand why wishlist is not a standard Dawn feature.
- [ ] Understand the accessibility requirements for icon-only controls.

## Acceptance criteria

### AC-3.1 — Desktop header

- [ ] **Given** a desktop viewport at 1200 px or wider, **when** the homepage loads, **then** the logo, menu, search, account, localization, and cart controls match the approved composition without overlap.

### AC-3.2 — Mobile navigation

- [ ] **Given** a 320–430 px viewport, **when** the menu is opened and navigated by touch or keyboard, **then** all navigation items are reachable, focus remains visible, and the menu can be closed without losing context.

### AC-3.3 — Localization fallback

- [ ] **Given** the store has only one country, language, or currency option, **when** the header renders, **then** redundant selectors are hidden or rendered without empty controls.

### AC-3.4 — Wishlist decision

- [ ] **Given** Dawn does not include persistent wishlist behavior, **when** the header scope is approved, **then** the wishlist icon is either backed by a tested feature or intentionally absent; no non-functional icon is shown.

---

# Stage 4 — Kotkoa hero

## Goal

Create an editable, responsive hero matching the editorial image/text composition in the reference.

## Tasks

- [ ] Decide whether to extend Dawn `image-banner` or create `sections/kotkoa-hero.liquid`.
- [ ] Add desktop and mobile image settings.
- [ ] Add heading, description, CTA label, and CTA link settings.
- [ ] Add content position, alignment, overlay, and height settings.
- [ ] Configure focal-point-safe image cropping.
- [ ] Optimize responsive image output and loading priority.
- [ ] Add locale keys for section UI text where required.

## Learning track

- [ ] Understand section schema and Theme Editor settings.
- [ ] Understand `image_picker`, responsive image widths, focal points, and `image_tag`.
- [ ] Understand the roles of Liquid, HTML, CSS, and JavaScript.
- [ ] Understand why the above-the-fold image affects LCP.

## Acceptance criteria

### AC-4.1 — Editable content

- [ ] **Given** the merchant is in Theme Editor, **when** hero image, heading, body, button label, or link is changed, **then** the preview updates without code changes.

### AC-4.2 — Responsive composition

- [ ] **Given** approved desktop and mobile images, **when** the hero is viewed from 320 px through 1440 px, **then** text remains readable, the subject is not unintentionally cropped, and no horizontal overflow occurs.

### AC-4.3 — Missing content

- [ ] **Given** an optional description or CTA is empty, **when** the hero renders, **then** no blank wrapper, broken link, or unintended spacing remains.

### AC-4.4 — Hero performance

- [ ] **Given** the homepage is loaded from a clean session, **when** browser performance is inspected, **then** the hero image has explicit dimensions, responsive sources, and appropriate high loading priority without loading an unnecessarily oversized asset.

---

# Stage 5 — brand features

## Goal

Create the four-item “Inspired by nature” feature section with editable, reorderable blocks.

## Tasks

- [ ] Create the Kotkoa features section.
- [ ] Add icon, heading, description, and optional link settings per block.
- [ ] Add 4-block default preset based on the reference.
- [ ] Create desktop, tablet, and mobile layouts.
- [ ] Ensure decorative icons are hidden from assistive technology.
- [ ] Add translation keys for storefront/editor text as needed.

## Learning track

- [ ] Understand the difference between a section and a block.
- [ ] Understand block ordering and `block.shopify_attributes`.
- [ ] Understand why editable content must not be hardcoded into Liquid markup.

## Acceptance criteria

### AC-5.1 — Block management

- [ ] **Given** the feature section in Theme Editor, **when** blocks are added, removed, or reordered, **then** the storefront immediately reflects the configured order and content.

### AC-5.2 — Responsive layout

- [ ] **Given** 1–4 feature blocks, **when** the section renders across supported viewport widths, **then** items remain balanced and readable without clipped text or uneven inaccessible ordering.

### AC-5.3 — Icon accessibility

- [ ] **Given** a decorative feature icon, **when** a screen reader traverses the section, **then** it announces the meaningful heading and description once and does not announce redundant SVG content.

---

# Stage 6 — Shop by collection

## Goal

Connect the four visual cards to real Shopify collections while matching the image-overlay card design.

## Tasks

- [ ] Create/confirm the required collections in Shopify Admin.
- [ ] Assign collection titles, descriptions, images, products, and SEO fields.
- [ ] Decide whether Dawn `collection-list` is sufficient or create `sections/kotkoa-collection-grid.liquid`.
- [ ] Use collection resource settings rather than manually typed handles.
- [ ] Add image, title, CTA, and fallback behavior.
- [ ] Implement the approved desktop and mobile grid/slider behavior.

## Learning track

- [ ] Understand products, collections, collection resources, and resource settings.
- [ ] Understand how `collection.title`, `collection.image`, and `collection.url` reach Liquid.
- [ ] Understand why resource references are more robust than hardcoded URLs.

## Acceptance criteria

### AC-6.1 — Real collection links

- [ ] **Given** a configured collection card, **when** its image, title, or CTA is activated, **then** the customer reaches the corresponding existing collection page.

### AC-6.2 — Resource updates

- [ ] **Given** a collection is renamed or its image is replaced in Shopify Admin, **when** the homepage reloads, **then** the card reflects the resource update without editing the section code.

### AC-6.3 — Missing collection/image

- [ ] **Given** a block has no selected collection or its collection has no image, **when** the section renders, **then** Theme Editor shows a useful placeholder or fallback and the customer does not receive a broken image or dead link.

### AC-6.4 — Mobile browsing

- [ ] **Given** a touch viewport, **when** customers browse all configured collection cards, **then** every card is reachable without relying on hover and all tap targets remain usable.

---

# Stage 7 — editorial split content

## Goal

Build the three-part “The Kotkoa world” and “For designers & creators” editorial section.

## Tasks

- [ ] Create a reusable split-content section.
- [ ] Add image, two headings, two text fields, two links, and optional decorative icon settings.
- [ ] Implement the desktop three-column composition.
- [ ] Define a deliberate mobile content order.
- [ ] Verify semantic heading hierarchy and link labels.

## Learning track

- [ ] Understand semantic content structure and heading hierarchy.
- [ ] Understand responsive CSS Grid.
- [ ] Understand why mobile source/visual order affects accessibility.

## Acceptance criteria

### AC-7.1 — Desktop composition

- [ ] **Given** approved section content at desktop width, **when** the section renders, **then** the image and two text areas follow the approved proportions and alignment without fixed-height clipping.

### AC-7.2 — Mobile reading order

- [ ] **Given** a narrow viewport or screen reader, **when** the section is traversed, **then** image and text content follow a logical reading order independent of desktop visual positioning.

### AC-7.3 — Optional links

- [ ] **Given** either editorial link is not configured, **when** the section renders, **then** its link control is omitted and surrounding spacing remains consistent.

---

# Stage 8 — Trust strip and compact footer

## Goal

Keep reference block 7 as a Trust strip and add only the compact legal/navigation footer needed below it.

## Confirmed design decision

- [x] Block 7 remains visually unchanged in purpose: Secure payments, Free shipping, Easy returns, Customer support.
- [x] No large multi-column footer is required unless future content creates a clear need.
- [x] Add a compact footer below the Trust strip.

## Tasks — Trust strip

- [ ] Create a Trust strip section with reorderable blocks.
- [ ] Add icon, heading, short description, and optional link per block.
- [ ] Connect each promise to actual store policy/configuration.
- [ ] Implement responsive wrapping without turning the strip into an oversized footer.

## Tasks — compact footer

- [ ] Adapt Dawn footer or create a minimal footer configuration.
- [ ] Add copyright text.
- [ ] Add links to Privacy, Terms, Shipping, Returns, and Contact where applicable.
- [ ] Add Instagram/Pinterest only if active profiles exist.
- [ ] Retain country/language selectors only if they add value and do not duplicate the header unnecessarily.
- [ ] Retain payment icons only if approved and visually appropriate.
- [ ] Create/configure the footer menu in Shopify Admin.

## Learning track

- [ ] Understand the difference between a Trust strip and a footer.
- [ ] Understand policy pages and why trust claims must match operational settings.
- [ ] Understand footer section groups and Shopify menus.
- [ ] Understand why a large footer is optional but legal/contact access is important.

## Acceptance criteria

### AC-8.1 — Trust claims

- [ ] **Given** each Trust strip message, **when** it is compared with shipping, return, payment, and support configuration, **then** the statement is accurate and links to supporting information where useful.

### AC-8.2 — Compact footer content

- [ ] **Given** the bottom of any storefront page, **when** the footer is reached, **then** copyright and approved Privacy, Terms, Shipping, Returns, and Contact links are available without a large multi-column layout.

### AC-8.3 — Missing policy

- [ ] **Given** a policy page has not been created or published, **when** the footer renders, **then** it does not show a broken or misleading policy link and the missing policy remains recorded as an incomplete task.

### AC-8.4 — Responsive finish

- [ ] **Given** desktop and mobile viewports, **when** the Trust strip and footer render, **then** all items remain readable and keyboard/touch accessible without horizontal overflow.

---

# Stage 9 — product, collection, cart, and content templates

## Goal

Apply the Kotkoa system beyond the homepage while preserving Dawn commerce behavior.

## Tasks

- [ ] Style collection banner, filters, sorting, grid, pagination, and empty states.
- [ ] Style product gallery, title, price, variants, quantity, product form, and recommendations.
- [ ] Define product information metafields for materials, care, dimensions, shipping, or origin as needed.
- [ ] Style cart drawer/page, discounts, quantity changes, removal, totals, and checkout CTA.
- [ ] Style search and predictive search.
- [ ] Style About, Contact, FAQ, and policy pages.
- [ ] Verify sold-out, sale, unavailable variant, and empty-cart states.

## Learning track

- [ ] Understand templates, sections, snippets, Shopify resources, and metafields.
- [ ] Understand product variants and the product form.
- [ ] Understand what the theme controls versus what Shopify checkout controls.

## Acceptance criteria

### AC-9.1 — Product purchase flow

- [ ] **Given** an available product with variants, **when** a customer selects an available variant and adds it to cart, **then** the correct variant, price, and quantity appear in the cart.

### AC-9.2 — Unavailable product state

- [ ] **Given** a sold-out product or unavailable variant, **when** it is selected, **then** purchase controls clearly communicate unavailability and do not submit an invalid cart request.

### AC-9.3 — Collection discovery

- [ ] **Given** a populated collection, **when** customers sort, filter, paginate, and open products, **then** state and results remain accurate and usable by keyboard and touch.

### AC-9.4 — Empty/error states

- [ ] **Given** an empty cart, empty collection, or no search results, **when** the corresponding page renders, **then** it presents a clear next action rather than broken or empty UI.

---

# Stage 10 — mobile and responsive design

## Goal

Create an intentional mobile experience rather than merely shrinking the desktop screenshot.

## Tasks

- [ ] Review at 320, 375, 390, 768, 1024, 1200, and 1440 px widths.
- [ ] Approve mobile hero crop and content placement.
- [ ] Approve card column counts or sliders.
- [ ] Verify header, drawer, modals, selectors, and cart on touch devices.
- [ ] Verify text zoom and long translated content.
- [ ] Verify safe-area spacing and horizontal overflow.

## Learning track

- [ ] Understand mobile-first responsive design.
- [ ] Understand CSS breakpoints, fluid sizing, and touch-target requirements.
- [ ] Understand why mobile composition requires design decisions absent from the desktop reference.

## Acceptance criteria

### AC-10.1 — Supported widths

- [ ] **Given** each target viewport width, **when** primary templates are inspected, **then** no unintended horizontal scrolling, overlap, clipped text, or unreachable control is present.

### AC-10.2 — Touch interaction

- [ ] **Given** a touch device, **when** customers use menus, cards, product controls, cart, selectors, and footer links, **then** controls do not depend on hover and have usable target sizes.

### AC-10.3 — Content resilience

- [ ] **Given** long headings, translated labels, or 200% text zoom, **when** content renders, **then** critical content and actions remain visible and operable.

---

# Stage 11 — accessibility, performance, and SEO

## Goal

Make the theme perceivable, operable, fast, indexable, and stable.

## Tasks

- [ ] Verify one meaningful H1 per primary page and logical heading order.
- [ ] Verify alt text and decorative image/icon handling.
- [ ] Verify keyboard navigation and visible focus.
- [ ] Verify color contrast.
- [ ] Honor `prefers-reduced-motion`.
- [ ] Verify responsive image dimensions, lazy loading, and hero priority.
- [ ] Measure LCP, CLS, and INP on representative pages.
- [ ] Verify title, description, canonical, Open Graph, structured data, sitemap, and robots behavior.
- [ ] Test with browser accessibility tree and automated tooling.

## Learning track

- [ ] Understand WCAG fundamentals.
- [ ] Understand Core Web Vitals: LCP, CLS, and INP.
- [ ] Understand technical SEO versus product/content SEO.
- [ ] Understand why automated checks do not replace manual keyboard and screen-reader-oriented review.

## Acceptance criteria

### AC-11.1 — Keyboard access

- [ ] **Given** a customer using only a keyboard, **when** they navigate header, homepage, product page, cart, and footer, **then** every interactive control is reachable, visibly focused, usable, and logically ordered.

### AC-11.2 — Images and layout stability

- [ ] **Given** a cold page load, **when** images load, **then** image dimensions reserve layout space, below-fold images lazy-load, and no avoidable image-driven layout shift occurs.

### AC-11.3 — Reduced motion

- [ ] **Given** the operating system requests reduced motion, **when** the storefront loads and interactions occur, **then** nonessential reveal and movement animations are removed or reduced.

### AC-11.4 — SEO output

- [ ] **Given** an indexable product, collection, or content page, **when** its document head and structured data are inspected, **then** title, description, canonical URL, social metadata, and applicable schema are valid and resource-specific.

### AC-11.5 — Performance baseline

- [ ] **Given** agreed test conditions and representative pages, **when** Lighthouse/Core Web Vitals checks run, **then** results meet the agreed launch thresholds and regressions are documented before release.

---

# Stage 12 — Shopify Admin and store operations

## Goal

Configure the commercial and informational data required for the theme to represent a real store accurately.

## Tasks

- [ ] Create and populate products, variants, prices, SKUs, inventory, and media.
- [ ] Create collections and assign products.
- [ ] Configure navigation menus.
- [ ] Create About, Contact, FAQ, Shipping, Returns, Privacy, and Terms pages.
- [ ] Configure Markets, countries, languages, and currencies.
- [ ] Configure shipping rates and free-shipping thresholds.
- [ ] Configure payments and test mode as appropriate.
- [ ] Configure taxes with qualified advice where required.
- [ ] Configure domain and sender email.
- [ ] Add product and collection SEO content.

## Learning track

- [ ] Understand which store data is independent of the theme.
- [ ] Understand Markets, shipping profiles, payments, policies, and domains.
- [ ] Understand why changing a theme does not configure checkout, payments, tax, or fulfillment.

## Acceptance criteria

### AC-12.1 — Navigation resources

- [ ] **Given** approved menus and pages, **when** a customer follows header and footer navigation, **then** every link resolves to published, relevant content without placeholder pages.

### AC-12.2 — Shipping consistency

- [ ] **Given** a free-shipping threshold displayed by the theme, **when** eligible and ineligible carts are evaluated at checkout, **then** Shopify shipping configuration produces behavior consistent with the displayed claim.

### AC-12.3 — Market presentation

- [ ] **Given** each enabled market, **when** a customer selects an available country/currency/language, **then** supported storefront content and pricing update correctly without offering unavailable choices.

### AC-12.4 — Operational dependency failure

- [ ] **Given** a payment, shipping, domain, or email configuration remains incomplete, **when** launch readiness is reviewed, **then** launch is blocked and the unresolved dependency is visible in the checklist.

---

# Stage 13 — QA, release, and rollback

## Goal

Validate the complete storefront, release deliberately, and retain a recoverable previous version.

## Tasks

- [ ] Run Theme Check and distinguish baseline warnings from new warnings.
- [ ] Run automated browser smoke tests.
- [ ] Run manual desktop, mobile, keyboard, and content checks.
- [ ] Test search, collection browsing, product variants, add to cart, cart updates, and checkout handoff.
- [ ] Test localization and customer account links where enabled.
- [ ] Push a named unpublished release candidate.
- [ ] Review the release candidate in Shopify Theme Editor and share preview.
- [ ] Record the release commit/tag and theme ID.
- [ ] Publish only after all blocking AC pass.
- [ ] Keep the previously live theme available for rollback.
- [ ] Run post-publish smoke tests on the public domain.

## Learning track

- [ ] Understand smoke, regression, accessibility, visual, and acceptance testing.
- [ ] Understand release candidates, Git tags, theme IDs, and rollback.
- [ ] Understand why a successful upload is not the same as a successful release.

## Acceptance criteria

### AC-13.1 — Release candidate

- [ ] **Given** a milestone intended for release, **when** it is uploaded, **then** it exists as a named unpublished theme tied to a known Git commit and can be reviewed without altering live traffic.

### AC-13.2 — Blocking checks

- [ ] **Given** the release checklist, **when** any blocking acceptance criterion fails, **then** the theme is not published and the failure has a documented owner or next action.

### AC-13.3 — Publish and smoke test

- [ ] **Given** all blocking criteria pass, **when** the release candidate is published, **then** the public domain serves the intended theme and critical browsing/cart paths pass post-publish smoke tests.

### AC-13.4 — Rollback

- [ ] **Given** a critical post-release regression, **when** rollback is initiated, **then** the previously live theme can be republished and the storefront returns to its prior working state.

---

# Suggested implementation order

1. [ ] Complete Stage 0 content/design inventory.
2. [ ] Complete Stage 1 browser-tool verification and release workflow.
3. [ ] Build Stage 2 design system.
4. [ ] Build Stage 3 announcement bar/header.
5. [ ] Build Stage 4 hero.
6. [ ] Build Stage 5 brand features.
7. [ ] Build Stage 6 collection grid.
8. [ ] Build Stage 7 editorial split content.
9. [ ] Build Stage 8 Trust strip and compact footer.
10. [ ] Complete Stage 9 commerce/content templates.
11. [ ] Complete Stage 10 responsive review.
12. [ ] Complete Stages 11–12 accessibility, performance, SEO, and Admin setup.
13. [ ] Complete Stage 13 QA and release.

# Open decisions

- [ ] Is wishlist required for the first launch?
- [ ] Which exact heading and body fonts are approved and licensed?
- [ ] Will the store launch in more than one market, currency, or language?
- [ ] Is the “Design library” a Shopify page, collection, gated resource, or external destination?
- [ ] Are newsletter signup and social links required in the compact footer?
- [ ] What measurable Lighthouse/Core Web Vitals thresholds will block launch?

# Definition of done for every code stage

- [ ] Shopify documentation was checked for any Liquid/API behavior used.
- [ ] New storefront text is translated through locale keys.
- [ ] Theme schema and Liquid validate.
- [ ] Theme Check introduces no unexplained new errors or warnings.
- [ ] Theme Editor can configure the intended merchant content.
- [ ] Empty, missing, long, and unexpected content states were tested.
- [ ] Desktop and mobile layouts were inspected.
- [ ] Keyboard and visible-focus behavior were inspected.
- [ ] Images have responsive sizing and correct loading behavior.
- [ ] Changes were reviewed in the development theme before any live update.
- [ ] Relevant checklist and AC items in this roadmap were updated.
