---
name: sales-generateblocks
description: "GenerateBlocks platform help — minimalist, high-performance Gutenberg block plugin for WordPress by EDGE22 (GeneratePress makers): a few versatile blocks (Container, Grid, Headline, Button, Image, Query Loop) instead of dozens, plus Pro Global Styles, Dynamic Data, 150+ patterns, asset library; developer hooks/filters (generateblocks_dynamic_tag_output, generateblocks_dynamic_content_output) and a custom dynamic-tag registration API (GenerateBlocks_Register_Dynamic_Tag). Use when GenerateBlocks blocks or CSS won't render after an update or migration, the editor is slow on long pages, deciding which plan unlocks Dynamic Data/Global Styles/Pro blocks, Pro blocks drop to fallback after a license lapse, building a Query Loop or binding post meta/ACF via Dynamic Data, registering a custom dynamic tag in code, or tuning Core Web Vitals on a block-built site. Do NOT use for cross-tool builder selection or funnel/CRO strategy (use /sales-funnel) or checkout/cart across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in GenerateBlocks]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
---

# GenerateBlocks Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken state — blocks/CSS not rendering after an update or migration, editor slow on long pages, layout broke, styles missing on inner pages
   - B) Build with blocks — Container/Grid flexbox layout, Headline/Button/Image, patterns/templates, Global Styles
   - C) Use Pro/dynamic features — **Dynamic Data** (post meta/ACF/author/featured image), **Query Loop**, device visibility, shape dividers, scroll effects, asset library
   - D) Customize/automate — public hooks/filters (`generateblocks_dynamic_tag_output`, `generateblocks_dynamic_content_output`), registering a **custom dynamic tag** (`GenerateBlocks_Register_Dynamic_Tag`), reading/writing block markup via the WordPress REST API
   - E) Pick or compare a plan (Free / Pro Personal / Pro Professional / GeneratePress One) or weigh GenerateBlocks vs other block builders

2. **Free or Pro?** Free (WordPress.org) ships the core blocks incl. Query Loop. **Global Styles, Dynamic Data, device visibility, shape dividers, gradients, scroll effects, the asset/template library, and custom attributes are Pro.**

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, builder selection across tools (Kadence/Spectra/SeedProd/Elementor…) | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| A/B testing methodology (GenerateBlocks has no native split testing) | `/sales-vwo` — Run: `/sales-vwo {user's original question}` |
| Email sequences/automation after a form opt-in | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| WooCommerce store/checkout (GenerateBlocks builds pages, not carts) | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |
| WordPress/WooCommerce funnel + upsells around the pages | `/sales-cartflows` — Run: `/sales-cartflows {user's original question}` |
| On-page/technical SEO beyond clean markup | `/sales-seo` — Run: `/sales-seo {user's original question}` |

If the question is GenerateBlocks-specific, continue to Step 3.

## Step 3 — GenerateBlocks platform reference

**Read `references/platform-guide.md`** for the full platform reference — blocks/modules, pricing/plan gates, data model, integration recipes, and code examples. For the Dynamic Data filters, the custom dynamic-tag registration API, and the WordPress REST surface, read `references/generateblocks-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **Performance is the whole point.** GenerateBlocks emits lean, semantic markup with minimal CSS — the leanest of the major block plugins. If a site's Core Web Vitals are still poor, look at the *theme*, images, third-party scripts, and other plugins before blaming GenerateBlocks. Pair with GeneratePress for the lightest stack.
- **The "few blocks" model is the learning curve.** There are only ~9 blocks because **Container + Grid compose everything** — there's no dedicated "pricing table" or "testimonial" block; you build them. Users coming from Kadence/Stackable (40+ blocks) expect ready-made widgets and get confused. Frame it as primitives, not widgets; lean on patterns/templates (Pro) for a head start.
- **Plan gating drives most surprises.** Free covers Container/Grid/Headline/Button/Image/Query Loop. **Dynamic Data, Global Styles, device visibility, shape dividers, scroll effects, custom attributes, and the asset/template library are Pro.** Confirm the tier before promising a feature.
- **Pro blocks/features degrade if the license lapses** — like other block plugins, Pro-only styling/features can stop applying when Pro is deactivated/expired. Don't build a critical page solely on Pro-only features without testing the fallback on staging.
- **Dynamic Data is the killer Pro feature.** It binds Headline/Button/Image/Container content to **post title, excerpt, date, post meta (incl. ACF/deeply-nested arrays), terms, author/user fields, comments count, and featured/meta/avatar images** — and powers the Query Loop for blog/portfolio/CPT listings. This is what replaces a "blog grid" widget.
- **The real automation surface is WordPress + PHP hooks**, not a hosted API: read/write block markup through the **WordPress REST API** (blocks are `generateblocks/`-namespaced in `post_content`), filter output with `generateblocks_dynamic_tag_output` / `generateblocks_dynamic_content_output` / `generateblocks_do_content` / `generateblocks_image_url`, and **register your own dynamic tag** with `GenerateBlocks_Register_Dynamic_Tag` (2.0+). No outbound webhook.
- **GenerateBlocks 2.0 was a rewrite.** Dynamic tags, the unified Query Loop, and the new Styles engine arrived in 2.0 — older tutorials (1.x "Dynamic Data" UI, separate Grid/Query) may not match the current editor.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

1. **Only a handful of blocks by design.** Container + Grid are layout primitives you compose into everything; there are no one-off widget blocks (pricing table, testimonial). This is intentional, but it's the #1 source of "where's the X block?" confusion.
2. **Dynamic Data, Global Styles, device visibility, shape dividers, scroll effects, custom attributes, and the pattern/asset library are Pro.** The free plugin is core blocks + Query Loop only.
3. **Pro features can degrade when the license lapses/deactivates** — Pro-only styling/features may stop applying. Test fallbacks on staging before relying on them on a live page.
4. **GenerateBlocks 2.0 is a major rewrite** (dynamic tags, unified Query Loop, new Styles engine). Pre-2.0 tutorials and the old Dynamic Data UI can mislead — confirm the version.
5. **No hosted REST API, no outbound webhook, no Zapier app.** It's a WordPress plugin: automate via the WordPress core REST API (block markup in `post_content`) and PHP hooks/filters. Form leads exit through whatever form plugin you pair with it.
6. **No native A/B testing, heatmaps, or analytics.** GenerateBlocks builds pages; measurement needs a separate tool (VWO, Microsoft Clarity).
7. **Migrating/bulk-importing pages can leave stale CSS.** Block CSS is generated per page; after a migration or mass update, regenerate assets and clear page/object/CDN cache or inner pages render unstyled.

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, and builder selection across tools (Kadence Blocks, Spectra, SeedProd, Elementor, ClickFunnels, Leadpages)
- `/sales-kadence` — A Gutenberg block plugin with 40+ ready-made blocks and a design system — compare blocks, performance, plan gates, and developer hooks vs GenerateBlocks' minimalist model
- `/sales-spectra` — Another Gutenberg-native block plugin (by Brainstorm Force) — the closest design-flexibility rival; compare DOM output, Dynamic Content, and hooks
- `/sales-stackable` — A design-focused Gutenberg-native block plugin (by Gambit Technologies) with 42 ready-made blocks and a Global Design System — the breadth/design contrast to GenerateBlocks' few primitives
- `/sales-seedprod` — A WordPress page/landing-page builder plugin (non-Gutenberg alternative with Theme Builder + coming-soon pages)
- `/sales-cartflows` — WordPress/WooCommerce funnel + checkout/upsells around the pages GenerateBlocks builds
- `/sales-vwo` — A/B testing and heatmap methodology GenerateBlocks lacks natively
- `/sales-audience-growth` — Growing an email list (lead magnets, opt-in strategy) behind a form
- `/sales-email-marketing` — Email sequences to run after a form captures the lead
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Register a custom dynamic tag and filter its output
**User**: "How do I extend GenerateBlocks in code — add my own dynamic tag and tweak what a dynamic tag outputs?"
**Approach**: GenerateBlocks has no hosted REST API; it's extended through WordPress-style PHP. Register a custom tag (2.0+) by instantiating `GenerateBlocks_Register_Dynamic_Tag` inside an `init` action with a config array (`title`, `tag`, `type`, `supports`, `return` callback); the callback returns through `GenerateBlocks_Dynamic_Tag_Callbacks::output()`. To modify existing output, filter `generateblocks_dynamic_tag_output` (or `generateblocks_dynamic_content_output` for legacy 1.x). Pull the exact array shape, callback signature, and a code snippet from `references/generateblocks-api-reference.md`.

### Example 2: Build a blog/portfolio listing that pulls custom fields
**User**: "I want a grid of my custom post type that shows a custom-field price and the featured image — what do I need?"
**Approach**: Use the **Query Loop** block to pull the CPT, and **Dynamic Data** (Pro) to bind a Headline to the post title, another to the post-meta/ACF field, and the Image block to the featured image. Dynamic Data lives on the Headline/Button/Image/Container blocks and can read deeply-nested post meta. Query Loop is free; **Dynamic Data binding is Pro** — confirm the tier. See `references/platform-guide.md` (Dynamic Data + Query Loop recipe).

### Example 3: Which plan unlocks Dynamic Data, and how many sites?
**User**: "Which GenerateBlocks plan do I need for Dynamic Data and Global Styles, and how many sites does each cover?"
**Approach**: **Dynamic Data, Global Styles, device visibility, shape dividers, scroll effects, and the asset/template library are Pro** — not in the free plugin. Pro Personal (~$59/yr) covers **1 site**; Pro Professional (~$99/yr) covers up to **500 sites**; **GeneratePress One** (~$149/yr) bundles GP Premium + GenerateBlocks Pro + GenerateCloud. Warn that pricing is best-effort/annual/intro-rated and Pro-only features degrade if the license lapses. Verify current tiers in `references/platform-guide.md`.

## Troubleshooting

### Blocks or styles render broken after an update or migration
**Symptom**: Pages look unstyled or layouts collapse after updating GenerateBlocks, GeneratePress, or migrating the site.
**Cause**: GenerateBlocks generates block CSS per page; after a bulk change the cached CSS can be stale, or a 2.0 rewrite changed the markup/Styles engine.
**Solution**: Update GenerateBlocks **and** GenerateBlocks Pro together to the latest version; clear page/object cache and CDN; re-save a affected page to regenerate its CSS. On 1.x→2.0 jumps, test on staging first — the Styles engine and dynamic tags changed.

### The editor is slow or sluggish on long pages
**Symptom**: The block editor lags when editing long pages with many GenerateBlocks blocks.
**Cause**: Editor-side rendering overhead on very long documents (compounded by other heavy editor plugins).
**Solution**: Split very long pages; deactivate unrelated heavy editor plugins to isolate the conflict; keep GenerateBlocks/Pro updated. The front-end output stays lean even when the editor is heavy — they're separate concerns.

### A Pro block/feature stopped working ("fallback" styling)
**Symptom**: A page built with Dynamic Data, Global Styles, or other Pro features lost its styling/behavior.
**Cause**: GenerateBlocks Pro is deactivated, expired, or the license isn't active on that site.
**Solution**: Reactivate/renew GenerateBlocks Pro and confirm the license is applied to this site (Pro Personal = 1 site only). Avoid building a critical live page solely on Pro-only features without a tested fallback.
