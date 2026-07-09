---
name: sales-nexter
description: "Nexter platform help — all-in-one WordPress Gutenberg ecosystem by POSIMYTH Innovations (Nexter Blocks 90+ blocks, Nexter Extension 50+ site tools + Theme Builder; slug the-plus-addons-for-block-editor): built-in popup builder, mega menu, form builder, header/theme builder, Dynamic Content (ACF/Toolset/Pods), AI via ChatGPT/Gemini, plus Nexter Abilities — a native MCP server exposing 115 AI tools to Claude/Cursor/VS Code from a prompt. Use when Nexter blocks won't show in the editor after install or the v4 ApiVersion-3 update, styles missing on the frontend, configuring the Nexter Abilities MCP server in Claude or Cursor, choosing which plan unlocks Theme Builder/White Label/Dynamic Content, taming asset bloat / Core Web Vitals, or reading/writing tpgb/-namespaced block markup via the WordPress REST API. Do NOT use for builder selection or funnel/CRO strategy (use /sales-funnel), A/B-testing/heatmap methodology (use /sales-vwo), or checkout/cart across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in Nexter]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
github: "https://github.com/posimyth/the-plus-addons-for-block-editor"
---

# Nexter Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken state — blocks not showing in the editor after install/update, styles missing on the frontend, layout broke after the v4 ApiVersion-3 conversion, an update introduced bugs
   - B) Build with blocks — containers/layout, headings/buttons, pricing tables, testimonials, post grids/carousels, the **Form Builder**, the **Popup Builder**, the **Mega Menu**, the **Header/Theme Builder**, 1000+ templates
   - C) Use Pro/dynamic features — **Dynamic Content** (ACF/Toolset/Pods/native fields), WooCommerce blocks, Lottie/Spline 3D/scroll animations, White Label, the expanded template library
   - D) Automate with AI / MCP — set up **Nexter Abilities** (the built-in MCP server, 115 tools) in Claude/Cursor/VS Code, or use the in-editor AI (ChatGPT/Gemini)
   - E) Customize/automate via code — performance flags (`tpgb_defer_css_js`, `tpgb_delay_css_js`), reading/writing `tpgb/`-namespaced block markup via the WordPress REST API
   - F) Pick or compare a plan (Starter / Professional / Studio / Agency Bundle) or weigh Nexter vs other block builders

2. **Free or Pro?** Free (WordPress.org) ships ~45+ blocks plus the built-in Form Builder and AI. **Theme Builder, White Label, Dynamic Content, WooCommerce blocks, the Popup Builder's advanced types, Lottie/Spline/scroll animations, and the Pro half of the MCP abilities are paid** (Professional+ for Theme Builder/White Label).

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, builder selection across tools (Spectra/Kadence/GenerateBlocks/Stackable/SeedProd/Elementor…) | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| A/B testing methodology (Nexter has no native split testing) | `/sales-vwo` — Run: `/sales-vwo {user's original question}` |
| Email sequences/automation after a form opt-in | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| WooCommerce store/checkout (Nexter has WooCommerce blocks but no cart/upsell engine) | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |
| WordPress/WooCommerce funnel + upsells around the pages | `/sales-cartflows` — Run: `/sales-cartflows {user's original question}` |
| On-page/technical SEO beyond clean markup | `/sales-seo` — Run: `/sales-seo {user's original question}` |

If the question is Nexter-specific, continue to Step 3.

## Step 3 — Nexter platform reference

**Read `references/platform-guide.md`** for the full platform reference — blocks/modules, the Nexter Extension + Theme Builder, pricing/plan gates, data model, integration recipes, and code examples. For **Nexter Abilities (the MCP server)** setup, the `tpgb/` block markup, the WordPress REST API approach, and the performance flags, read `references/nexter-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **Nexter is an all-in-one Gutenberg ecosystem, not a single block library.** It's three parts: **Nexter Blocks** (90+ blocks + in-editor AI), **Nexter Extension** (50+ site tools + the Theme Builder, security/performance/code-snippets, White Label), and the **Nexter Theme**. This breadth is its defining contrast with lean block plugins like Stackable/GenerateBlocks — it *does* ship a form builder, popup builder, mega menu, and header/theme builder.
- **The standout for makers is Nexter Abilities — a native MCP server.** It exposes **115 server-side tools** (68 free / 47 Pro, plus 8 workflow skills, button-preset CRUD, and a page-inspection ability) so an MCP client (Claude Desktop, Cursor, VS Code, Windsurf, Cline, Zed, Continue) can compose real, editable `tpgb/` Gutenberg blocks from a prompt, screenshot, or URL. Auth is a **token you generate in WP admin, scoped to post types + abilities**, and every call respects WordPress capability checks. See `references/nexter-api-reference.md`.
- **"Blocks not showing in the editor"** is usually that you're not in the Gutenberg Block Editor (Classic Editor or another page builder is active), a plugin/JS conflict, or a stale build/cache after an update. Confirm Gutenberg is active, update Nexter, hard-refresh + clear caches, and test with other editor plugins disabled.
- **The v4 ApiVersion-3 conversion is a known update boundary.** v4.7.0 converted all blocks to WordPress "ApiVersion 3." Older tutorials/screenshots may not match, and a major update can introduce regressions — keep a backup/staging copy and a rollback plan before updating a live site.
- **Performance: the "1 CSS + 1 JS file per page, disabled blocks load nothing" claim is real but not a free pass.** Third-party tests still measure ~0.2–0.35s and ~6–9 MiB added per request. For Core Web Vitals, enable Nexter's asset controls (`tpgb_defer_css_js` / `tpgb_delay_css_js`), only enable the blocks you use, add caching, and benchmark before/after. For deeper remediation use `/sales-seo`.
- **Plan gating drives most surprises.** **Theme Builder and White Label are Professional+ (5 sites+); Dynamic Content, WooCommerce blocks, advanced popups, and Lottie/Spline/scroll animations are Pro.** Confirm the tier before promising a feature, and warn that Pro-only blocks/styling can fall back or stop applying if the license lapses — test on staging.
- **The automation surface is WordPress + MCP, not a hosted SaaS API.** No Nexter REST API, no outbound webhook, no first-party Zapier app. Programmatic surface = the **Nexter Abilities MCP server**, the **WordPress core REST API** (blocks are `tpgb/`-namespaced in `post_content`, Application-Password auth), the in-editor AI, and PHP option/filter flags. It's GPLv3 (`github.com/posimyth/the-plus-addons-for-block-editor`) — deeper extension means building from source.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features, the MCP ability counts, and integration details that may be outdated.*

1. **All-in-one breadth, but tiered.** Form Builder + in-editor AI are free; **Theme Builder & White Label are Professional+**, and **Dynamic Content, WooCommerce blocks, advanced popups, and Lottie/Spline/scroll animations are Pro.** Confirm the tier before promising a feature.
2. **Nexter Abilities (MCP) is split free/Pro too.** 68 of the 115 abilities are free; the other 47 (CTA banners, timeline, repeater, popup builder, Mailchimp, Lottie/Spline/scroll) require Pro. The MCP endpoint is token-authenticated and scoped — every call still respects WordPress capabilities, and you can disable the endpoint anytime (existing pages stay intact).
3. **The v4.7.0 ApiVersion-3 conversion is a migration boundary.** Major updates have introduced regressions; back up + test on staging before updating a live site. Old tutorials may show pre-v4 UI.
4. **Performance claims vs reality.** "1 CSS + 1 JS per page, disabled blocks load nothing" is accurate, but third-party tests still show measurable overhead (~0.2–0.35s, ~6–9 MiB). Use `tpgb_defer_css_js`/`tpgb_delay_css_js`, enable only needed blocks, and cache.
5. **No hosted REST API, no outbound webhook, no first-party Zapier app.** Automate via the Nexter Abilities MCP server and the WordPress core REST API (`tpgb/` block markup in `post_content`). Form leads exit through the form's configured ESP/integration (e.g. Mailchimp).
6. **`tpgb/` block namespace is best-effort.** It's consistent with Nexter's `tpgb_*` option flags but not confirmed verbatim in public docs — copy real block markup from a live install rather than hand-authoring attribute keys.
7. **No native A/B testing, heatmaps, or analytics.** Nexter builds pages; measurement needs a separate tool (VWO, Microsoft Clarity).

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, and builder selection across tools (Spectra, Kadence Blocks, GenerateBlocks, Stackable, SeedProd, Elementor, ClickFunnels, Leadpages)
- `/sales-spectra` — Another Gutenberg-native block plugin (by Brainstorm Force) that also ships a Popup Builder and form blocks — compare blocks, DOM output, Dynamic Content, and plan gates vs Nexter's broader ecosystem
- `/sales-kadence` — A Gutenberg block plugin (by StellarWP) with an Advanced Form block + webhooks and Kadence AI — compare form/automation surface and plan gates vs Nexter
- `/sales-generateblocks` — The minimalist, performance-first Gutenberg block plugin (by EDGE22/GeneratePress) — the lean opposite of Nexter's all-in-one breadth
- `/sales-stackable` — A design-focused Gutenberg block plugin (GPLv3) that, unlike Nexter, has no form/popup/header builder — compare breadth vs lean footprint
- `/sales-seedprod` — A WordPress page/landing-page + Theme Builder plugin (non-block-editor alternative with coming-soon pages and the WordPress Abilities API)
- `/sales-cartflows` — WordPress/WooCommerce funnel + checkout/upsells around the pages Nexter builds
- `/sales-vwo` — A/B testing and heatmap methodology Nexter lacks natively
- `/sales-audience-growth` — Growing an email list (lead magnets, opt-in strategy) behind a Nexter form
- `/sales-email-marketing` — Email sequences to run after a Nexter form captures the lead
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Set up the Nexter Abilities MCP server in Claude to build pages from a prompt
**User**: "I want Claude to build Nexter landing pages on my WordPress site from a description. How do I wire up the MCP server, and what can it actually do?"
**Approach**: That's **Nexter Abilities**, Nexter's built-in MCP server. Install Nexter Blocks (it includes the MCP endpoint + all 115 abilities), connect your Nexter account, enable MCP permissions and scope which post types/abilities the AI may touch, generate a token, and paste the generated MCP config into Claude Desktop. The AI then calls block-add abilities to compose real, editable `tpgb/` Gutenberg blocks (containers, headings, pricing tables, testimonials, forms…) — **68 abilities are free, 47 are Pro**. It can also recreate a layout from a screenshot or inspect a competitor URL for fonts/colors/media. Every build runs inside a page-type performance budget. Pull exact steps from `references/nexter-api-reference.md`. **Confirm the MCP config snippet against your install** — it's generated per-site and wasn't captured verbatim in research.

### Example 2: Blocks/styles broke after updating to v4
**User**: "After updating Nexter, some blocks vanished from the editor and a couple of pages look wrong."
**Approach**: v4.7.0 converted all blocks to WordPress **ApiVersion 3** — a major-update boundary that can introduce regressions. First confirm you're in the **Gutenberg Block Editor** (not Classic/another builder) and that Nexter is updated; hard-refresh and clear browser + page + object/CDN cache; disable other editor plugins to isolate a JS conflict. If pages are still wrong, **roll back from your backup/staging copy** and re-test the update on staging. See Troubleshooting.

### Example 3: Which plan unlocks Theme Builder and Dynamic Content — and is it lean enough?
**User**: "I want the Theme Builder, ACF-bound dynamic content, and white-label for client sites. What tier, and will it slow the sites down?"
**Approach**: **Theme Builder and White Label are Professional+ (5 sites)**; **Studio (~$129/yr) is unlimited sites**. **Dynamic Content (ACF/Toolset/Pods) is Pro.** Pricing is best-effort/annual with Lifetime options — verify on nexterwp.com/pricing and note Pro features degrade if the license lapses. On performance: Nexter loads **1 CSS + 1 JS file per page and disabled blocks load nothing**, but benchmark — third-party tests still show ~0.2–0.35s overhead; enable `tpgb_defer_css_js`/`tpgb_delay_css_js`, turn off unused blocks, and cache. Confirm current tiers in `references/platform-guide.md`.

## Troubleshooting

### Nexter blocks don't appear in the editor
**Symptom**: After installing or updating, Nexter blocks are missing from the block inserter (or some vanished after an update).
**Cause**: You're not in the Gutenberg Block Editor (Classic Editor or another page builder is active), a plugin/JS conflict, or a stale editor build/cache — often after the v4 ApiVersion-3 conversion.
**Solution**: Confirm the Gutenberg Block Editor is the active editor; update Nexter to the latest version; hard-refresh and clear browser + page cache; disable other editor plugins to isolate a JS conflict; and confirm the relevant blocks are enabled in Nexter's block manager.

### Nexter pages render unstyled or bloat Core Web Vitals
**Symptom**: A page shows raw/unstyled output, or PageSpeed flags render-blocking CSS/JS and excess weight.
**Cause**: Cache/optimization plugin stripped or reordered Nexter's assets, or too many blocks/animations are loading without the performance controls enabled.
**Solution**: Clear page/object/CDN cache and allowlist Nexter's handles in any minify/optimization plugin. Enable Nexter's asset controls (`tpgb_defer_css_js` / `tpgb_delay_css_js`), disable blocks you don't use, add caching, and benchmark before/after. For deeper remediation use `/sales-seo`.

### A Pro feature stopped working or an update broke pages
**Symptom**: Theme Builder / Dynamic Content / Pro blocks stopped applying, or pages broke right after a major update.
**Cause**: The Nexter license is deactivated/expired (Pro-only blocks/styling fall back), or a major release (e.g. the v4.7.0 ApiVersion-3 conversion) introduced a regression.
**Solution**: Reactivate/renew the license and confirm it's active on this site; for an update regression, roll back from your backup/staging copy, then re-test the update on staging. Avoid building critical live pages solely on Pro-only blocks without a tested fallback.
