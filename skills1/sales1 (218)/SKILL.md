---
name: sales-gutenkit
description: "GutenKit platform help — feature-rich Gutenberg block plugin + page builder for WordPress by Wpmet (slug gutenkit-blocks-addon; 70k+ installs, 65+ blocks, 20+ modules, 900+ templates, flexbox Container, Mega Menu, Query Loop Builder, dynamic content, display conditions, FSE-compatible, Block API v3, zero jQuery). Use when the GutenKit/Gutenberg editor won't load or a block shows 'this block has encountered an error and cannot be previewed' after a customization change, the GutenKit Template Library errors out (often a conflict with ElementsKit or another Wpmet plugin), block styles look right in the editor but not on the published page, blocks vanish or break after a plugin update, deciding which plan unlocks the mega menu / query loop builder / dynamic content / display conditions, or reading/writing gutenkit/-namespaced block markup via the WordPress REST API. Do NOT use for cross-tool builder selection or funnel/CRO strategy (use /sales-funnel) or checkout/cart across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in GutenKit]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
---

# GutenKit Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken state — the editor won't load or a block shows "this block has encountered an error and cannot be previewed" after a customization change, the **GutenKit Template Library** throws an error, styles apply in the editor but not on the frontend, or blocks vanished/broke after an update
   - B) Build with blocks — layout/section structure with the flexbox **Container**, content/interactive blocks (Advanced Accordion/Tab, Post Grid, Pricing Table, Countdown, Image Comparison), the **Mega Menu** and **Nav Menu**, **Offcanvas**, the 900+ template library, global colors/fonts
   - C) Show dynamic content — the **Query Loop Builder** (filter by post type/taxonomy/meta/author/date), **Dynamic Content** (bind block text to post meta/ACF/user/site fields), and **Display Conditions** (show/hide blocks by rule)
   - D) Capture leads — the built-in **Mailchimp** block (opt-in into a Mailchimp audience); note GutenKit has no full form builder
   - E) Pick or confirm a plan (Free / Personal / Professional / Agency, yearly or lifetime) or weigh which feature is Pro
   - F) Customize/automate — WordPress hooks/filters and reading/writing `gutenkit/`-namespaced block markup via the WordPress core REST API

2. **Free or Pro?** Free (WordPress.org) ships the core block set + the template library + flexbox Container + responsive editing. **Mega Menu, Query Loop Builder, Dynamic Content, Display Conditions, One Page Scroll, Sticky Content, Glass Morphism, Advanced Tooltip, Google Map, and the advanced Parallax are Pro.** Confirm the tier before promising a feature.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, builder selection across tools (Spectra/Kadence/GenerateBlocks/Stackable/Gutenverse/Elementor…) | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| A/B testing methodology (GutenKit has no native split testing) | `/sales-vwo` — Run: `/sales-vwo {user's original question}` |
| Email sequences/automation after a Mailchimp opt-in | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| WooCommerce store/checkout around the pages | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |
| WordPress/WooCommerce funnel + upsells around the pages | `/sales-cartflows` — Run: `/sales-cartflows {user's original question}` |
| On-page/technical SEO and Core Web Vitals beyond clean markup | `/sales-seo` — Run: `/sales-seo {user's original question}` |

If the question is GutenKit-specific, continue to Step 3.

## Step 3 — GutenKit platform reference

**Read `references/platform-guide.md`** for the full platform reference — blocks/modules, the Mega Menu / Query Loop / Dynamic Content / Display Conditions features, pricing/plan gates, data model, integration recipes, and code examples. For WordPress hooks/filters and the WordPress REST API approach to `gutenkit/`-namespaced markup, read `references/gutenkit-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **"The editor won't load / a block shows 'encountered an error and cannot be previewed'" is the #1 reported issue.** It typically appears right after a customization change or an update, and clears when GutenKit is deactivated — a JS conflict, a corrupted block, or a stale editor build. Update GutenKit, hard-refresh and clear browser + page cache, then bisect by disabling other plugins (and switching to a default theme) on a staging copy until the conflict surfaces. Back up before editing a live site.
- **The GutenKit Template Library erroring inside ElementsKit Lite is a known Wpmet-internal conflict.** GutenKit and ElementsKit (both Wpmet) share a template-library handler; running mismatched versions throws a `gutenkit-template-library` error. Update *both* plugins to their latest versions and clear cache; if it persists, deactivate one to confirm the culprit, then re-enable on the matched version.
- **"Styles apply in the editor but not on the frontend"** is a per-page asset/cache mismatch. GutenKit loads CSS/JS selectively per page — regenerate/clear any page/object/CDN cache and allowlist GutenKit's assets in any minify/combine plugin so the frontend matches the editor.
- **Plan gating drives most surprises.** The core blocks, template library, flexbox Container, and responsive editing are **free**. **Mega Menu, Query Loop Builder, Dynamic Content, Display Conditions, One Page Scroll, Sticky Content, Glass Morphism, Advanced Tooltip, Google Map, and advanced Parallax are Pro** — and degrade if the license lapses. Treat pricing as best-effort/annual and confirm the tier.
- **Lead capture is thin.** GutenKit ships a **Mailchimp** opt-in block but no full form builder — no webhooks, no conditional logic, no multi-step, no payment fields. For anything beyond a Mailchimp opt-in, pair a dedicated form plugin and route the sequence via `/sales-email-marketing`.
- **The automation surface is WordPress, not a hosted API.** No GutenKit REST API, no outbound webhook, no Zapier app. Read/write block markup through the **WordPress core REST API** (blocks are `gutenkit/`-namespaced in `post_content`, Application-Password auth); deeper extension means WordPress hooks/filters against the rendered output.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

1. **A block showing "this block has encountered an error and cannot be previewed," or the editor failing to load, is the top reported problem.** The frontend often still renders; deactivating GutenKit restores the editor. Treat it as a JS conflict / corrupted block / stale build — update, clear cache, bisect plugins on staging before touching a live site.
2. **The GutenKit Template Library can error inside ElementsKit Lite** (both are Wpmet plugins sharing a template-library handler). Keep *both* plugins on matched, current versions and clear cache; deactivate one to isolate if it persists.
3. **Mega Menu, Query Loop Builder, Dynamic Content, Display Conditions, One Page Scroll, Sticky Content, Glass Morphism, Advanced Tooltip, Google Map, and advanced Parallax are Pro** and stop applying if the license lapses — test on staging.
4. **Style changes applying in the editor but not on the frontend** is a per-page asset/cache issue. Clear page/object/CDN cache and exclude GutenKit's CSS/JS from minify/combine plugins.
5. **No full form builder.** GutenKit has a Mailchimp opt-in block only — no native form storage, webhooks, conditional logic, multi-step, or payment fields.
6. **No hosted REST API, no outbound webhook, no Zapier app.** Automate via the WordPress core REST API (`gutenkit/` block markup in `post_content`) and WordPress hooks/filters.
7. **No native A/B testing, heatmaps, or analytics.** GutenKit builds pages; measurement needs a separate tool (VWO, Microsoft Clarity).
8. **Free-vs-Pro block/module/template counts vary across sources** — confirm the live feature matrix before promising a specific count on the free tier.

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, and builder selection across tools (Spectra, Kadence Blocks, GenerateBlocks, Stackable, Gutenverse, SeedProd, Elementor, ClickFunnels, Leadpages)
- `/sales-gutenverse` — Another free-tier-strong, Gutenberg-native FSE block plugin — compare blocks, template library, Pro gates, and note Gutenverse ships a separate Form plugin where GutenKit has only a Mailchimp opt-in block
- `/sales-spectra` — A Gutenberg-native block plugin (by Brainstorm Force) that also ships a Popup Builder + Starter Templates — compare blocks, DOM output, and Pro Dynamic Content
- `/sales-kadence` — A Gutenberg block plugin (by StellarWP) with an Advanced Form block + webhooks and Kadence AI — compare form/automation depth vs GutenKit's Mailchimp-only capture
- `/sales-generateblocks` — The minimalist, performance-first Gutenberg block plugin — compare its few-primitives, lean-DOM model against GutenKit's 65+ ready-made blocks
- `/sales-stackable` — A design-focused Gutenberg-native block plugin — compare blocks, footprint, and Pro gates
- `/sales-nexter` — An all-in-one Gutenberg ecosystem (by POSIMYTH) with a Form Builder, Mega Menu, and an MCP server — compare breadth vs GutenKit
- `/sales-cartflows` — WordPress/WooCommerce funnel + checkout/upsells around the pages GutenKit builds
- `/sales-vwo` — A/B testing and heatmap methodology GutenKit lacks natively
- `/sales-audience-growth` — Growing an email list (lead magnets, opt-in strategy) behind a capture block
- `/sales-email-marketing` — Email sequences to run after a Mailchimp opt-in captures the lead
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Read and bulk-edit GutenKit block markup programmatically
**User**: "I want to update the CTA text inside a GutenKit Button across 30 landing pages from a script. Is there an API?"
**Approach**: There's **no GutenKit REST API** — use the **WordPress core REST API**. GutenKit blocks are `gutenkit/`-namespaced block markup in each post's `content` field, so authenticate with an **Application Password**, `GET` the post `content` with `context=edit`, transform the `<!-- wp:gutenkit/... -->` markup string (not the rendered HTML), and `POST` it back. Pull the cURL/Python snippets from `references/gutenkit-api-reference.md` and test on staging first.

### Example 2: My GutenKit editor stopped loading after I added a block
**User**: "After I added a GutenKit section, the editor shows 'this block has encountered an error and cannot be previewed' and won't load — but the live site is fine."
**Approach**: This is the top reported GutenKit issue. The frontend rendering while the editor breaks points to a JS conflict, a corrupted block from that edit, or a stale editor build. Update GutenKit to the latest version, hard-refresh and clear browser + page cache, then on a **staging copy** disable other plugins (and switch to a default theme) one at a time to isolate the conflict; if a single block is corrupt, remove/re-add it. If you also run ElementsKit, make sure both Wpmet plugins are on matched current versions. See Troubleshooting.

### Example 3: Which plan do I need for a mega menu and dynamic post listings?
**User**: "I want a multi-column mega menu in my header and a blog grid that filters by category and pulls the post's ACF subtitle. What tier?"
**Approach**: All three are **Pro**. The **Mega Menu**, the **Query Loop Builder** (filter by category/taxonomy), and **Dynamic Content** (binding to an ACF field) are Pro-gated — the free tier covers the core blocks and template library but not these. Pricing is best-effort/annual (Personal/1-site ~$39, Professional/5-site ~$79, Agency/unlimited ~$149, with lifetime options); confirm current tiers and site counts in `references/platform-guide.md`, and warn that Pro features degrade if the license lapses.

## Troubleshooting

### A GutenKit block shows "encountered an error and cannot be previewed" / the editor won't load
**Symptom**: After a customization change or an update, a block can't be previewed or the block editor screen fails to load; deactivating GutenKit lets the editor load again. The published frontend is unaffected.
**Cause**: A JavaScript conflict with another plugin/theme, a corrupted block from the last edit, a stale editor build/cache, or (if ElementsKit is installed) a version mismatch between the two Wpmet plugins.
**Solution**: Update GutenKit (and ElementsKit, if present) to the latest version; hard-refresh and clear browser + page/object cache; on a staging copy, deactivate all other plugins and switch to a default theme, then re-enable one at a time to find the conflict. If one block is the culprit, delete and re-insert it. Keep a backup before editing live.

### The GutenKit Template Library throws an error (often inside ElementsKit)
**Symptom**: Opening the GutenKit template/pattern library shows an error (e.g. a `gutenkit-template-library` error), sometimes surfaced while using ElementsKit Lite.
**Cause**: GutenKit and ElementsKit (both Wpmet) share a template-library handler; mismatched plugin versions, a failed library asset load, or a server/firewall blocking the library request break it.
**Solution**: Update *both* GutenKit and ElementsKit to their latest versions and clear cache; confirm the server can reach the Wpmet template endpoint (no aggressive firewall/security-plugin block). If it persists, deactivate one of the two plugins to confirm the culprit, then re-enable on the matched version; report a reproducible case to Wpmet support.

### Block styles look right in the editor but not on the published page
**Symptom**: A color, spacing, or layout change looks correct in the editor but the live page doesn't reflect it.
**Cause**: GutenKit loads CSS/JS selectively per page; a caching/CDN layer is serving old assets, or a minify/optimization plugin stripped or reordered GutenKit's assets.
**Solution**: Clear page/object/CDN cache; allowlist GutenKit's CSS/JS in any minify/combine plugin; re-check in an incognito window to rule out the browser cache. If only some blocks are affected, edit and re-save the page to regenerate its assets.
