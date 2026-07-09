---
name: sales-beaver-builder
description: "Beaver Builder platform help — stable, developer-friendly WordPress drag-and-drop page builder (by FastLine Media): front-end editor with Modules/Rows/Columns, reusable Templates, the Beaver Builder Theme, and Beaver Themer for dynamic theme templates via Field Connections (ACF/WooCommerce data); flat per-plan licensing (1/3/50/unlimited sites), white labeling, and a real PHP developer API (custom modules extending FLBuilderModule + a large fl_builder_* hooks/filters surface). Use when pages load slowly or the editor lags on big layouts, layouts break or the builder deactivates after a migration or update, building a custom module with FLBuilder::register_module(), wiring dynamic ACF/WooCommerce data through Beaver Themer Field Connections, which plan unlocks multisite/white labeling, or reading fl_builder layout data via the WordPress REST API. Do NOT use for cross-tool builder selection or funnel/CRO strategy (use /sales-funnel) or checkout/cart across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in Beaver Builder]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
github: "https://github.com/beaverbuilder"
---

# Beaver Builder Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken state — pages/editor loading slowly, the editor lags or freezes on big layouts, the builder got **deactivated on all pages except the home page after a migration**, layouts broke / "Beaver Builder not working" after a WordPress or plugin **update**, styling missing, license won't activate
   - B) Build with the editor — Rows/Columns layout, Modules (Heading, Photo, Button, Gallery, Slider, Subscribe Form, HTML, etc.), reusable **Templates** and **Saved Rows/Modules**, responsive editing, global rows
   - C) Use **Beaver Themer** — dynamic **headers/footers/archives/singular/404/search** templates, **Field Connections** to pull WordPress/custom-field/**ACF**/EDD/The Events Calendar/**WooCommerce** data, the **Loop Builder** for post listings, location/conditional rules
   - D) Develop / automate — write a **custom module** (extend `FLBuilderModule`, `FLBuilder::register_module()`), use the **`fl_builder_*` hooks/filters**, the Beaver Builder **Theme** + theme hooks, or read/write `fl_builder` layout data via the **WordPress REST API** / WP-CLI
   - E) Pick or compare a plan (Starter / Plus / Professional / Unlimited, or free **Lite**) or weigh Beaver Builder vs Elementor/Divi/Bricks/SeedProd/Gutenberg block plugins

2. **Free or paid?** The free **Beaver Builder Lite** (WordPress.org) ships a limited set of modules and no Themer/templates. The paid plugin adds the full module set, the Template/Saved-row system, and (on current plans) **Beaver Themer + Loop Builder + WooCommerce support on every tier**; **multisite is Professional+** and **white labeling is Unlimited-only**.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, builder selection across tools (Elementor/Divi/Bricks/SeedProd/Gutenberg blocks…) | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| A/B testing methodology (Beaver Builder has no native split testing) | `/sales-vwo` — Run: `/sales-vwo {user's original question}` |
| Email sequences/automation after a Subscribe Form opt-in | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| WooCommerce store/checkout strategy across platforms | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |
| WordPress/WooCommerce funnel + upsells around the pages | `/sales-cartflows` — Run: `/sales-cartflows {user's original question}` |
| On-page/technical SEO beyond clean markup | `/sales-seo` — Run: `/sales-seo {user's original question}` |

If the question is Beaver Builder-specific, continue to Step 3.

## Step 3 — Beaver Builder platform reference

**Read `references/platform-guide.md`** for the full platform reference — modules/capabilities, pricing/plan gates, data model, integration recipes, and best practices. For the **developer API** (custom modules via `FLBuilderModule`, `FLBuilder::register_module()` settings, the `fl_builder_*` hooks/filters, the Hooks Reference, and the WordPress REST surface for `fl_builder` layout data), read `references/beaver-builder-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **Beaver Builder is a standalone drag-and-drop builder, not a Gutenberg block plugin.** It edits pages in its own live front-end UI (**Rows → Columns → Modules**) over any theme — so it does *not* produce `wp-block-*` markup like Kadence/Spectra/GenerateBlocks. Its reputation is **stability + clean, semantic HTML** and a gentle learning curve, not raw feature count.
- **Low lock-in is a genuine selling point.** When you deactivate Beaver Builder, the *formatting* disappears but your **text content survives cleanly in the default WordPress editor** (it isn't left as broken/"invalid" blocks). That makes BB safer to leave than block plugins — call this out when a user worries about migration/lock-in.
- **Performance isn't automatic.** BB outputs clean markup, but heavy pages (many modules, large images, sliders, third-party row backgrounds) still load slowly and lag the editor. Before blaming BB, check the **theme, image sizes, third-party scripts, and a caching/optimization plugin**; split very long pages; cache assets. (See Troubleshooting.)
- **Beaver Themer is where the power is.** Themer turns BB into a full **theme builder** — dynamic headers/footers/archives/singular/404 templates plus **Field Connections** that bind any row/column/module setting to WordPress data, custom fields, **ACF**, EDD, The Events Calendar, or **WooCommerce**. The **Loop Builder** (Themer) renders dynamic post listings. On current plans Themer + Loop Builder ship on **every** paid tier.
- **The real automation surface is WordPress + the PHP API**, not a hosted Beaver Builder API. There is **no hosted REST API and no outbound webhook**. Extend via **custom modules** (`FLBuilderModule` + `FLBuilder::register_module()`), the large **`fl_builder_*` hooks/filters** surface (see the Hooks Reference), the Beaver Builder **Theme** hooks, and the **WordPress core REST API / WP-CLI** (a page's layout lives in `post_content` plus the **`_fl_builder_data`** post meta — best-effort serialized data, not a documented public schema).
- **Lead capture** is the built-in **Subscribe Form** module (native ESP integrations — Mailchimp, etc., extendable via `fl_builder_subscribe_form_services`) or a third-party form plugin + Zapier. Pair with `/sales-email-marketing` for the sequence.
- **Plan gating drives surprises.** Themer/Loop Builder/WooCommerce are on all paid tiers now, but **multisite is Professional+** and **white labeling is Unlimited-only**; the free **Lite** has a reduced module set and no Themer/templates. Confirm the tier before promising a feature.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

1. **Builder deactivated on all pages except the home page after a migration.** A common post-migration symptom (URL/serialized-data mismatch). Run a proper **search-replace** on the database (e.g. WP-CLI `search-replace` or a migration plugin that handles serialized data), clear caches, and re-save affected pages.
2. **"Beaver Builder not working after upgrading."** After a WordPress, theme, or BB update the editor may fail to load or styles vanish — usually a **cache or stale-CSS** issue or a plugin/theme conflict. Clear page/object/CDN cache, re-save the page (regenerates CSS), bump PHP memory, and isolate conflicts (default theme + only BB active).
3. **Slow loading / sluggish editor on big pages.** Clean markup ≠ automatic speed — many modules, large images, sliders, and third-party scripts still cost. Optimize images, add caching/minification, split long pages, and audit the theme before assuming BB is the cause.
4. **Low lock-in, but not zero.** Deactivating BB leaves text cleanly in the default editor (a plus) — but **shortcode-based modules** and Themer dynamic layouts won't render without BB. Don't promise a perfectly styled site after deactivation.
5. **No hosted REST API, no outbound webhook, no native A/B testing.** It's a WordPress plugin — automate via the WordPress REST API + the PHP module/hooks API + WP-CLI; measure/split-test with a separate tool (VWO, Microsoft Clarity).
6. **Plan gates.** Multisite = Professional+; white labeling = Unlimited-only; free Lite drops Themer/templates and many modules. Pricing/feature splits change — verify on wpbeaverbuilder.com/pricing.
7. **Custom-module naming.** Use a **prefixed, lowercase, dash-separated** module slug (e.g. `acme-button`) to avoid collisions with core modules; gate registration behind `class_exists( 'FLBuilder' )`.

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, and builder selection across tools (Elementor, Divi, Bricks, SeedProd, Kadence/Spectra/GenerateBlocks, ClickFunnels, Leadpages)
- `/sales-seedprod` — A WordPress landing-page + Theme Builder plugin — compare the standalone-builder + theme-builder approach and templates vs Beaver Builder/Themer
- `/sales-cartflows` — WordPress/WooCommerce funnel + checkout/upsells around the pages (CartFlows officially supports Beaver Builder for step design)
- `/sales-spectra` — A Gutenberg-native block plugin — the block-editor contrast to Beaver Builder's standalone drag-and-drop UI (markup, lock-in, performance)
- `/sales-kadence` — A Gutenberg block plugin with a design library and Kadence AI — compare blocks, dynamic content, and plan gates vs Beaver Builder + Themer
- `/sales-vwo` — A/B testing and heatmap methodology Beaver Builder lacks natively
- `/sales-audience-growth` — Growing an email list (lead magnets, opt-in strategy) behind a Subscribe Form
- `/sales-email-marketing` — Email sequences to run after a Subscribe Form captures the lead
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Build a custom module and register it
**User**: "How do I add my own module to Beaver Builder and register it so it shows up in the editor?"
**Approach**: Beaver Builder's developer API is a **PHP module class + a registration call**. Create a class that **extends `FLBuilderModule`** and sets its config in the constructor (`name`, `description`, `group`/`category`, `dir`, `url`, `icon`, `editor_export`, `enabled`, `partial_refresh`, `include_wrapper`); include the file from your plugin behind a **`class_exists( 'FLBuilder' )`** guard; then call **`FLBuilder::register_module( 'YourModuleClass', $tabs )`** where `$tabs` defines tabs → sections → fields (e.g. a `text`/`photo`/`color` field). Use a **prefixed, dash-separated slug** (`acme-button`) to avoid clashing with core modules, and render output in the module's `frontend.php`. Pull the exact class skeleton, the `register_module()` settings array, and the field types from `references/beaver-builder-api-reference.md`.

### Example 2: Pull dynamic ACF/WooCommerce data into a template
**User**: "I want one blog-post template that fills in each post's title, featured image, and an ACF field automatically — and a product template for WooCommerce. How?"
**Approach**: This is **Beaver Themer**. Create a **Themer Layout** of type *Singular* (for posts) or a WooCommerce product layout, set its **Location** (e.g. "All Posts" / "All Products"), then in any module use **Field Connections** — click the **plus icon** on a setting and bind it to **Post Title**, **Featured Image**, an **ACF** field, or a **WooCommerce** field. The template then renders the correct data per post/product. For dynamic *listings* (a grid of posts), use the **Loop Builder**. Themer + Loop Builder ship on all paid tiers. See the Beaver Themer + Field Connections section in `references/platform-guide.md`.

### Example 3: Which plan do I need, and what survives if I leave Beaver Builder?
**User**: "Do I need the top plan for a client multisite and white labeling — and if I cancel, do my pages break?"
**Approach**: On current plans, **multisite is Professional+ (50 sites)** and **white labeling is Unlimited-only**; Starter (1 site) and Plus (3 sites) include the full builder + Themer but not those two. On lock-in: when you deactivate Beaver Builder the **text content survives cleanly in the default WordPress editor** — only the *formatting/layout* and any shortcode/Themer-dynamic modules stop rendering. So a client site degrades gracefully rather than filling with broken blocks, but it won't stay visually styled. Flag pricing as best-effort and verify on wpbeaverbuilder.com/pricing; confirm current tiers in `references/platform-guide.md`.

## Troubleshooting

### Builder is deactivated on every page except the home page after a migration
**Symptom**: After moving the site (new host/domain/staging→live), Beaver Builder layouts render only on the home page; inner pages show raw/unstyled content or a "this layout was built with Beaver Builder" prompt.
**Cause**: The migration left **stale URLs/paths inside Beaver Builder's serialized layout data** (`_fl_builder_data`) — a plain find-replace that doesn't handle serialized PHP corrupts or misses it.
**Solution**: Run a **serialized-data-safe search-replace** (WP-CLI `wp search-replace 'oldurl' 'newurl' --all-tables`, or a migration plugin that handles serialized data), then clear page/object/CDN cache and re-save affected pages. Confirm the WordPress Address/Site Address (Settings → General) match the new URL.

### "Beaver Builder not working after upgrading"
**Symptom**: After a WordPress core, theme, or Beaver Builder update the editor won't open, hangs, or pages lose their styling.
**Cause**: Stale cached CSS/JS, an outdated BB/Themer/theme version, low PHP memory, or a plugin/theme conflict introduced by the update.
**Solution**: Update **Beaver Builder, Beaver Themer, and the BB Theme together**; clear all caches (page/object/CDN/browser) and re-save a page to regenerate CSS; raise PHP memory (`WP_MEMORY_LIMIT`); then isolate conflicts by switching to a default theme with only Beaver Builder active and re-enabling plugins one by one.

### Pages and the editor are excruciatingly slow
**Symptom**: Front-end pages load slowly and the editor lags or freezes, especially on long/complex layouts.
**Cause**: Too many modules, oversized images, slider/background scripts, an unoptimized theme, or no caching — not BB's markup itself.
**Solution**: Compress/serve images at the right size (WebP), add a **caching + minification** plugin, reduce module/slider count, **split very long pages** into sections or Themer parts, and audit the theme and third-party scripts. Confirm front-end speed with PageSpeed Insights after each change rather than judging from the editor.
