---
name: sales-kadence
description: "Kadence Blocks platform help — Gutenberg page-builder block plugin for WordPress by StellarWP (600k+ installs): 20+ free blocks (Row Layout/Section containers, Advanced Form, Tabs, Posts, Testimonials) plus Pro Advanced Query Loop, Advanced Slider, Modal, Dynamic Content (ACF/MetaBox/WooCommerce binding), Design Library and Kadence AI. No hosted REST API — extend via WordPress hooks/filters (kadence_blocks_posts_query_args, kadence_blocks_pro_query_loop_query_vars) and Advanced Form webhooks (Pro). Use when the Kadence editor goes blank or won't load, dynamic CSS regeneration is slowing TTFB on a high-traffic or WooCommerce site, child-theme or custom CSS won't show in the editor, a caching/optimization plugin breaks Kadence styles, you're deciding which plan unlocks Dynamic Content/Query Loop/AI, or wiring an Advanced Form submission to a webhook/Zapier/CRM. Do NOT use for cross-tool builder selection or funnel/CRO strategy (use /sales-funnel) or checkout/cart across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in Kadence Blocks]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
github: "https://github.com/stellarwp"
---

# Kadence Blocks Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken state — editor blank/won't load, blocks or CSS not rendering on inner pages, custom/child-theme CSS not showing in the editor, a caching/optimization plugin broke styles, slow TTFB / high server load
   - B) Build with blocks — Row Layout/Section flexbox containers, Advanced Form, Gallery, Tabs/Accordion, Posts, Testimonials, Design Library patterns, Starter Templates
   - C) Use Pro/dynamic features — Advanced Query Loop, Dynamic Content (ACF/MetaBox/WooCommerce), Advanced Slider, Modal, Animate on Scroll, Custom Fonts, Kadence AI
   - D) Customize/automate — public hooks/filters (`kadence_blocks_posts_query_args`, `kadence_blocks_pro_query_loop_query_vars`, `kadence_element_display`), Advanced Form webhooks → Zapier/Make/CRM, WordPress REST API on block content
   - E) Pick or compare a plan (Free / Essentials / Pro / Elite, or standalone Kadence Blocks Pro) or weigh Kadence Blocks vs other block builders

2. **Free or Pro?** Free (WordPress.org, 20+ blocks). Pro adds Advanced Query Loop, Dynamic Content, Advanced Slider/Modal, the Design Library/Creative Kit, Kadence AI, and form webhooks. Pro is sold standalone or inside the unified Kadence bundles (Essentials/Pro/Elite).

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, builder selection across tools (Spectra/GenerateBlocks/Elementor/SeedProd…) | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| A/B testing methodology (Kadence Blocks has no native split testing) | `/sales-vwo` — Run: `/sales-vwo {user's original question}` |
| Email sequences/automation after a Kadence Advanced Form opt-in | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| WooCommerce store/checkout beyond Kadence's blocks + Shop Kit | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |
| On-page/technical SEO beyond Kadence's schema/FAQ blocks | `/sales-seo` — Run: `/sales-seo {user's original question}` |

If the question is Kadence-specific, continue to Step 3.

## Step 3 — Kadence Blocks platform reference

**Read `references/platform-guide.md`** for the full platform reference — blocks/modules, pricing/plan gates, data model, integration recipes, and code examples. For the public hooks/filters list, the Advanced Form webhook flow, and the WordPress REST API surface on block content, read `references/kadence-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **Dynamic CSS regeneration is the #1 performance complaint.** On high-traffic or WooCommerce sites, Kadence can regenerate block CSS per request and inflate TTFB. Fix: Kadence → **Settings → General → CSS/JS** set CSS output to **External File** (not inline), enable the built-in **Performance** tools, and let a page cache serve the generated assets. Confirm `class-kadence-blocks-css.php` isn't running uncached.
- **"Editor goes blank / won't load"** is usually a JS conflict or a stale build. Update Kadence Blocks (+ Pro) first, hard-refresh, disable other editor-heavy plugins to isolate, and check the browser console. Do **not** enable `SCRIPT_DEBUG` on production to debug it.
- **"Custom/child-theme CSS won't show in the editor"** — the block editor iframe doesn't auto-load your stylesheet. Enqueue it with `add_editor_style()` (or `enqueue_block_assets`) so it loads inside the editor, and regenerate Kadence's cached CSS after changes.
- **Plan gating drives most surprises.** Free is 20+ blocks; **Advanced Query Loop, Dynamic Content, Advanced Slider, Modal, Custom Fonts, the Design Library/Creative Kit, Kadence AI, and form webhooks are Pro.** Confirm the tier before promising a feature; Pro features degrade when the license lapses.
- **No native A/B testing, heatmaps, or analytics.** Pair with a separate tool (VWO, Microsoft Clarity) — Kadence only builds the page.
- **The real automation surface is WordPress hooks/filters + the WP REST API**, not a hosted API. Form leads exit through the **Advanced Form webhook** (Pro) or the connected ESP integration — there is no outbound platform webhook beyond that.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially items about plan-gated features and integration details that may be outdated.*

1. **Dynamic block CSS can regenerate per request** and slow TTFB on high-traffic/WooCommerce sites. Switch CSS output to an external file, enable the Performance tools, and serve generated assets from page cache.
2. **The editor occasionally loads blank / won't let you edit.** Usually a JS conflict or stale asset build — update Kadence, clear caches, and isolate other editor plugins; check the console.
3. **Child-theme / custom CSS doesn't appear inside the block editor.** The editor runs in an iframe; enqueue styles with `add_editor_style()` / `enqueue_block_assets` and regenerate Kadence's cached CSS.
4. **Caching/optimization plugins can break Kadence styles or scripts** (aggressive minify/combine/defer). Exclude Kadence's generated CSS/JS handles, then re-test.
5. **Some blocks still depend on jQuery** (e.g. the Tabs block has broken when jQuery was manually dequeued). Don't blanket-dequeue jQuery on pages using those blocks.
6. **Advanced Query Loop, Dynamic Content, Advanced Slider, Modal, Custom Fonts, Design Library, Kadence AI, and form webhooks are Pro.** The free plugin is block-building only; Pro features degrade when the license expires.
7. **No native A/B testing, heatmaps, or analytics.** Kadence builds pages; measurement needs a separate tool.
8. **Homepage and docs now live under StellarWP / Liquid Web** (kadencewp.com 301-redirects to liquidweb.com). Old `kadencewp.com/help-center/...` doc links redirect — follow them.

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, and builder selection across tools (Spectra, GenerateBlocks, Elementor, SeedProd, ClickFunnels, Leadpages)
- `/sales-spectra` — The closest rival: another Gutenberg-native block plugin (by Brainstorm Force / Astra) — compare blocks, performance, and plan gates
- `/sales-generateblocks` — The minimalist, performance-first Gutenberg block plugin (by EDGE22/GeneratePress) — compare its few-primitives model and lean DOM against Kadence's 20+ blocks and design system
- `/sales-stackable` — A design-focused Gutenberg-native block plugin (by Gambit Technologies) — 42 blocks + Global Design System but no form block/webhooks (Kadence has both); compare design controls and plan gates
- `/sales-seedprod` — A non-Gutenberg WordPress page/landing-page builder plugin (Theme Builder + coming-soon pages) alternative
- `/sales-vwo` — A/B testing and heatmap methodology Kadence lacks natively
- `/sales-audience-growth` — Growing an email list (lead magnets, opt-in strategy) behind a Kadence Advanced Form
- `/sales-email-marketing` — Email sequences to run after a Kadence form captures the lead
- `/sales-checkout` — Checkout/cart strategy beyond Kadence's blocks and Shop Kit
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Send an Advanced Form submission to a CRM via webhook
**User**: "How do I push Kadence form submissions into my CRM automatically?"
**Approach**: The Advanced Form **webhook** is the right surface (it requires **Kadence Blocks Pro**). On a Kadence Form, open **Actions After Submit** and check **WebHook**; on a Kadence Form (Adv), open **Submit Actions** and add **WebHook**. A **Webhook Settings** panel appears — paste your endpoint as the **Webhook URL** and use **Map Fields** to bind each form field to the payload key your CRM (or a Zapier/Make "Catch Hook") expects. Test with a temporary URL (e.g. webhook-test.com) before going live. For the exact menu path and field-id format (`kadence-form-{id}`), see `references/kadence-api-reference.md`.

### Example 2: My site got slow after adding Kadence Blocks
**User**: "TTFB jumped on my WooCommerce store after I started using Kadence Blocks — what's going on?"
**Approach**: This is almost always **dynamic CSS being regenerated per request** (`class-kadence-blocks-css.php`). In **Kadence → Settings → General → CSS/JS**, set CSS output to **External File** instead of inline so the stylesheet is generated once and cached, enable the built-in **Performance** tools, and make sure a page cache is serving the assets. Re-test TTFB. See Troubleshooting and `references/platform-guide.md` for the full performance checklist.

### Example 3: Which plan do I need for Dynamic Content and the Query Loop?
**User**: "I want to build a dynamic listing pulling ACF fields into blocks — what tier?"
**Approach**: **Advanced Query Loop and Dynamic Content are Pro** — the free plugin can't do them. Kadence Blocks Pro (standalone, or inside the Essentials/Pro/Elite bundles) unlocks them, plus the Design Library and Kadence AI. Warn that Pro-gated features degrade if the license lapses, so test on staging. Confirm current tiers/prices in `references/platform-guide.md` (pricing is best-effort and annual).

## Troubleshooting

### Editor loads blank or won't let me edit
**Symptom**: Opening a page/post shows a blank editor or nothing loads, intermittently.
**Cause**: A JavaScript conflict with another plugin, or a stale/partial asset build.
**Solution**: Update Kadence Blocks and Kadence Blocks Pro to the latest version; hard-refresh and clear browser + page cache; deactivate other editor-heavy plugins one at a time to isolate the conflict; check the browser console for the failing script. Avoid enabling `SCRIPT_DEBUG` on production — it can expose dev assets and cause its own issues.

### Site is slow / high TTFB after adding Kadence Blocks
**Symptom**: Slower TTFB or higher server load, especially on high-traffic or WooCommerce pages.
**Cause**: Kadence regenerating dynamic block CSS on every request without caching.
**Solution**: Set CSS output to **External File** (Kadence → Settings → General → CSS/JS), enable the built-in Performance tools, and ensure a page-cache plugin serves the generated assets. Confirm the CSS class isn't running uncached on every load.

### Kadence styles broke after enabling a caching/optimization plugin (or custom CSS won't show in the editor)
**Symptom**: Blocks render unstyled/distorted after turning on minify/combine/defer, or your child-theme CSS doesn't appear inside the block editor.
**Cause**: The optimization plugin is stripping/deferring Kadence's generated CSS/JS, or the editor iframe never loads your stylesheet.
**Solution**: In the caching/optimization plugin, **exclude Kadence's generated CSS/JS handles** from minify/combine/defer, then regenerate Kadence's cached CSS and clear caches. For editor styling, enqueue your stylesheet with `add_editor_style()` (or hook `enqueue_block_assets`) so it loads inside the editor.
