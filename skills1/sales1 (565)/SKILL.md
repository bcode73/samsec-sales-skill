---
name: sales-stackable
description: "Stackable platform help — design-focused, Gutenberg-native WordPress block plugin by Gambit Technologies (gambitph; GPLv3, 200k+ installs, lean CSS): 42 blocks (Columns, Hero, Card, Carousel, Pricing, Testimonial, Blog Posts, Timeline), a Global Design System (Global Colors/Typography, block defaults), a 375+ Design Library, theme.json/block-theme support, plus Pro Dynamic Content (ACF/Metabox/JetEngine), Motion Effects, Conditional Display, Role Manager & per-block Custom CSS. Use when Stackable blocks won't show in the editor after install or update, handling the v2-to-v3 block migration (load v2 blocks vs v3-only), styles missing on the frontend (stackable_force_css_load), choosing which plan unlocks Dynamic Content/Motion/Role Manager, an update introduced bugs you need to roll back, or reading/writing stackable/-namespaced block markup via the WordPress REST API. Do NOT use for cross-tool builder selection or funnel/CRO strategy (use /sales-funnel) or checkout/cart across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in Stackable]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
github: "https://github.com/gambitph/Stackable"
---

# Stackable Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken state — blocks not showing in the editor, styles missing on the frontend, layout broke or an update introduced bugs, v2 blocks vs v3 blocks confusion
   - B) Build with blocks — Columns/section layout, Hero/Card/Feature/CTA, Carousel/Tabs/Accordion, Blog Posts, the Design Library, Global Design System (Global Colors/Typography, block defaults)
   - C) Use Pro/dynamic features — **Dynamic Content** (post meta/ACF/Metabox/JetEngine), **Motion Effects**, **Conditional Display**, **Role Manager**, per-block **Custom CSS**, advanced copy-paste styling
   - D) Customize/automate — the `stackable_force_css_load` filter, `render_block`, reading/writing `stackable/`-namespaced block markup via the WordPress REST API
   - E) Pick or compare a plan (Free / Premium / All Access Pass) or weigh Stackable vs other block builders

2. **Free or Pro?** Free (WordPress.org) ships all 42 blocks + the Global Design System + part of the Design Library. **Dynamic Content, Motion Effects/transforms, Conditional Display, Role Manager, per-block Custom CSS, advanced copy-paste, and the expanded Design Library/presets are Pro.**

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, builder selection across tools (Spectra/Kadence/GenerateBlocks/SeedProd/Elementor…) | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| A/B testing methodology (Stackable has no native split testing) | `/sales-vwo` — Run: `/sales-vwo {user's original question}` |
| Email sequences/automation after a form opt-in (Stackable has **no form block**) | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| WooCommerce store/checkout (Stackable builds pages, not carts, and has no WooCommerce blocks) | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |
| WordPress/WooCommerce funnel + upsells around the pages | `/sales-cartflows` — Run: `/sales-cartflows {user's original question}` |
| On-page/technical SEO beyond clean markup | `/sales-seo` — Run: `/sales-seo {user's original question}` |

If the question is Stackable-specific, continue to Step 3.

## Step 3 — Stackable platform reference

**Read `references/platform-guide.md`** for the full platform reference — blocks/modules, pricing/plan gates, data model, integration recipes, and code examples. For the `stackable_force_css_load` filter, the `render_block` surface, and the WordPress REST API approach to `stackable/`-namespaced markup, read `references/stackable-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **The v2→v3 migration is the #1 source of confusion.** Stackable v3 was a near-total rewrite; v2 blocks are kept as separate "version 2" blocks. In **Settings → Other Settings → Migration**, you choose whether to load v2 blocks (for existing posts), allow both, or go v3-only. Old tutorials show v2 UI that no longer matches. Don't bulk-update a live site without testing the migration on staging — existing v2 pages keep working only while v2 block loading is enabled.
- **"Stackable blocks not showing in the editor"** is usually a JS conflict, a stale build/cache, or v2 blocks being disabled in Migration settings. Update Stackable, clear browser + page cache, re-check the editor with other editor plugins disabled, and confirm the relevant blocks are enabled (Settings → Blocks).
- **"Styles missing on the frontend"** — Stackable only loads its CSS on pages that contain Stackable blocks (an optimization). If you inject Stackable markup dynamically (shortcode, page builder, REST), the CSS may not enqueue; return `true` from the **`stackable_force_css_load`** filter to force it. After migrations/bulk edits, also clear page/object/CDN cache.
- **Plan gating drives most surprises.** All 42 blocks are **free**. **Dynamic Content, Motion Effects, Conditional Display, Role Manager, per-block Custom CSS, advanced copy-paste, and the expanded Design Library are Pro.** Confirm the tier before promising a feature, and warn that Pro-only styling/features can stop applying if the license lapses — test on staging.
- **Know what Stackable doesn't do.** No header/footer builder, **no popup builder, no form block,** and **no WooCommerce-specific blocks.** For lead capture pair a form plugin (and route the sequence via `/sales-email-marketing`); for commerce use WooCommerce/a funnel plugin. This is the defining contrast with Spectra/Kadence/aBlocks.
- **The automation surface is WordPress, not a hosted API.** No Stackable REST API, no outbound webhook, no Zapier app. Read/write block markup through the **WordPress core REST API** (blocks are `stackable/`-namespaced in `post_content`, Application-Password auth); modify output with the WordPress `render_block` filter; force asset loading with `stackable_force_css_load`. It's GPLv3 and open source (`github.com/gambitph/Stackable`) — deeper extension means forking/building.
- **Performance is a selling point, not a free pass.** Stackable is among the lightest block plugins (~10–75KB added), but page weight still depends on your theme, images, and other plugins. Benchmark before/after if Core Web Vitals matter; for deeper remediation use `/sales-seo`.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

1. **v2→v3 migration is a known footgun.** v3 was a rewrite; v2 blocks live on as separate blocks controlled by the Migration setting. Existing v2 pages keep rendering only while v2 block loading is enabled. Test the migration on staging before flipping a live site to v3-only.
2. **Stackable loads its CSS only on pages that contain Stackable blocks.** Dynamically-injected markup (shortcodes, REST, another builder) can render unstyled — force it with the `stackable_force_css_load` filter (return `true`).
3. **Dynamic Content, Motion Effects, Conditional Display, Role Manager, per-block Custom CSS, advanced copy-paste, and the expanded Design Library/presets are Pro.** The free plugin is all 42 blocks + Global Design System + part of the library.
4. **No header/footer builder, no popup builder, no form block, and no WooCommerce blocks.** Sites needing those add companion plugins — factor the extra plugin count in.
5. **Major-version updates have introduced bugs in past releases.** Keep a backup/staging copy and a rollback plan before updating on a live site (WordPress.org reviews cite update-stability issues).
6. **No hosted REST API, no outbound webhook, no Zapier app.** Automate via the WordPress core REST API (`stackable/` block markup in `post_content`) and the `render_block` / `stackable_force_css_load` filters. Form leads exit through whatever form plugin you pair with it.
7. **No native A/B testing, heatmaps, or analytics.** Stackable builds pages; measurement needs a separate tool (VWO, Microsoft Clarity).

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, and builder selection across tools (Spectra, Kadence Blocks, GenerateBlocks, SeedProd, Elementor, ClickFunnels, Leadpages)
- `/sales-spectra` — Another Gutenberg-native block plugin (by Brainstorm Force) — compare blocks, DOM output, Dynamic Content, and the fact Spectra ships a Popup Builder and form blocks Stackable lacks
- `/sales-kadence` — A Gutenberg block plugin (by StellarWP) with an Advanced Form block + webhooks and Kadence AI — compare design controls, plan gates, and developer hooks vs Stackable
- `/sales-generateblocks` — The minimalist, performance-first Gutenberg block plugin (by EDGE22/GeneratePress) — compare its few-primitives model and lean DOM against Stackable's 42 ready-made blocks
- `/sales-seedprod` — A WordPress page/landing-page builder plugin (non-Gutenberg alternative with Theme Builder + coming-soon pages)
- `/sales-cartflows` — WordPress/WooCommerce funnel + checkout/upsells around the pages Stackable builds
- `/sales-vwo` — A/B testing and heatmap methodology Stackable lacks natively
- `/sales-audience-growth` — Growing an email list (lead magnets, opt-in strategy) behind a form
- `/sales-email-marketing` — Email sequences to run after a form captures the lead (Stackable has no form block — pair a form plugin)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Force Stackable's CSS to load and edit block markup programmatically
**User**: "I'm injecting Stackable block markup through a shortcode and the page renders unstyled — and I want to bulk-update those blocks from a script. How?"
**Approach**: Stackable only enqueues its CSS on pages it detects Stackable blocks on, so dynamically-injected markup loads without styles. Force it by returning `true` from the **`stackable_force_css_load`** filter. For programmatic edits, there's no Stackable REST API — use the **WordPress core REST API**: Stackable blocks are `stackable/`-namespaced in the page's `content` field, so read/write the post with an Application Password and template the block markup. Modify rendered output with the WordPress `render_block` filter. Pull the snippets from `references/stackable-api-reference.md`.

### Example 2: Existing pages broke (or blocks vanished) after updating to v3
**User**: "After updating Stackable my older pages look wrong and some blocks disappeared from the editor."
**Approach**: This is the v2→v3 migration. v3 is a rewrite; v2 blocks are kept as separate blocks gated by **Settings → Other Settings → Migration**. Re-enable loading v2 blocks so existing posts render, decide whether to allow both v2+v3 or migrate to v3-only, and clear cache. Test the migration on staging before applying to a live site. See Troubleshooting.

### Example 3: Which plan do I need for Dynamic Content and Conditional Display?
**User**: "I want to bind block content to ACF fields and show/hide sections by user role — what tier, and how many sites?"
**Approach**: **Dynamic Content (ACF/Metabox/JetEngine) and Conditional Display are Pro** — the free plugin can't do them. Premium (~$49/yr) and the All Access Pass (~$89/yr) start at **1 site**, with 10-site/Unlimited and lifetime toggles; 30-day money-back. Warn that pricing is best-effort/annual and Pro-only features degrade if the license lapses. Confirm current tiers in `references/platform-guide.md`.

## Troubleshooting

### Stackable blocks don't appear in the editor
**Symptom**: After installing or updating, Stackable blocks are missing from the block inserter, or older v2 blocks vanished.
**Cause**: A JS conflict or stale editor build/cache, the blocks being disabled in Settings → Blocks, or v2 block loading being turned off after the v3 migration.
**Solution**: Update Stackable to the latest version; hard-refresh and clear browser + page cache; disable other editor plugins to isolate a JS conflict; confirm the blocks are enabled (Settings → Blocks); and in Settings → Other Settings → Migration, enable loading v2 blocks if you still have v2 content.

### Stackable blocks render unstyled on the frontend
**Symptom**: A page using Stackable blocks shows raw/unstyled output, often when the content is injected dynamically (shortcode, REST, another builder).
**Cause**: Stackable only enqueues its CSS on pages where it detects its blocks; dynamically-added markup isn't detected, so the stylesheet never loads. Or a cache/optimization plugin stripped the CSS.
**Solution**: Return `true` from the **`stackable_force_css_load`** filter to always load Stackable's frontend CSS. Clear page/object/CDN cache after migrations or bulk edits, and allowlist Stackable's assets in any minify/optimization plugin.

### A Pro feature stopped working or an update broke pages
**Symptom**: Dynamic Content/Motion/Conditional Display stopped applying, or pages broke right after a major-version update.
**Cause**: Stackable Premium is deactivated/expired (Pro-only features degrade), or a major release introduced a regression.
**Solution**: Reactivate/renew Premium and confirm the license is active on this site; for an update regression, roll back from your backup/staging copy, then re-test the update on staging. Avoid building critical live pages solely on Pro-only features without a tested fallback.
