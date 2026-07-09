---
name: sales-seedprod
description: "SeedProd platform help — WordPress drag-and-drop website + landing-page builder plugin (by Awesome Motive): Theme Builder (headers/footers/templates/WooCommerce), 300+ templates, coming-soon & maintenance-mode pages, opt-in/sales/squeeze/thank-you/404/login pages, subscriber capture to 13+ ESPs, Dynamic Text, an AI site builder, and a WordPress Abilities API (6.20+) exposing 8 named actions to AI tools and automation. Use when a SeedProd coming-soon or maintenance page stays stuck on the whole site after deactivating or uninstalling, pages built in SeedProd won't display with the theme set as default, deciding which plan unlocks WooCommerce/Zapier/Dynamic Text, capturing opt-in leads into an ESP, automating SeedProd via the Abilities API or permission/shortcode hooks, or judging intro-vs-renewal pricing and code-bloat/performance. Do NOT use for cross-tool builder selection or funnel/CRO strategy (use /sales-funnel) or checkout/cart across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in SeedProd]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
---

# SeedProd Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken state — site stuck in coming-soon/maintenance mode, pages not displaying, theme not applying
   - B) Build a page or theme — landing/opt-in/sales page, Theme Builder header/footer, Smart Sections, templates
   - C) Capture leads — opt-in form → ESP (Mailchimp, ConvertKit, ActiveCampaign…), subscriber management, spam/reCAPTCHA
   - D) Automate — Abilities API (toggle coming-soon, save page, import theme), permission filters, shortcodes, Zapier
   - E) Pick or compare a plan (Basic / Plus / Pro / Elite) or weigh SeedProd vs other builders

2. **Which plan/version?** Free (WordPress.org), Basic ($79), Plus ($199), Pro ($399), Elite ($599). Several features are plan-gated, and the Abilities API needs SeedProd 6.20.0+ on WordPress 6.9+.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, builder selection across tools | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| A/B testing methodology (SeedProd has no native split testing) | `/sales-vwo` — Run: `/sales-vwo {user's original question}` |
| Email sequences/automation after opt-in | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| WooCommerce store/checkout beyond SeedProd's product blocks | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |
| Generic iPaaS wiring (Zapier/Make) to a CRM/ESP | `/sales-integration` — Run: `/sales-integration {user's original question}` |
| On-page/technical SEO beyond SeedProd's basics | `/sales-seo` — Run: `/sales-seo {user's original question}` |

If the question is SeedProd-specific, continue to Step 3.

## Step 3 — SeedProd platform reference

**Read `references/platform-guide.md`** for the full platform reference — modules, pricing/plan gates, data model, integration recipes, code examples. For the Abilities API actions, permission filters, and shortcode list, read `references/seedprod-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **Coming-soon/maintenance lockout is the #1 support issue.** If the whole site shows the coming-soon page (even after deactivating), the mode is still toggled on or cached. Turn it off in SeedProd → Pages, clear caches/CDN, and only then deactivate. If already locked out, deactivate via FTP/file manager (rename the plugin folder) or set the coming-soon page to "Inactive" in the database.
- **Plan gating drives most surprises.** **Theme Builder needs Plus+**; **WooCommerce support and Domain Mapping are Elite-only**; **Zapier (3000+) and Dynamic Text need Pro+**. Confirm the tier before promising a feature.
- **No native A/B testing or analytics.** Pair with a separate tool (VWO, Google Optimize successor, or Clarity for heatmaps) — SeedProd only builds the page.
- **Abilities API is the real automation surface** (WP 6.9 + SeedProd 6.20.0+): 8 named actions an AI tool/script can discover and trigger. No legacy outbound webhooks — lead data flows out through the connected ESP or Zapier.
- **Intro pricing renews at full price** and is annual; the most-cited value complaint. Set that expectation.
- **Performance: SeedProd outputs nested div markup.** For Core Web Vitals-sensitive pages, enable caching/minification and test against a Gutenberg-native option.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

1. **Coming-soon/maintenance can lock you (and visitors) out of the whole site.** Turn the mode off and clear caches *before* deactivating; if stuck, rename the plugin folder via FTP or flip the page to Inactive in the DB.
2. **WooCommerce support and Domain Mapping are Elite ($599) only.** Don't promise the WooCommerce Theme Builder / shop templates on Basic/Plus/Pro.
3. **Zapier and Dynamic Text are Pro ($399)+; Theme Builder is Plus ($199)+.** The Basic plan is page-building only — single site, 50 templates.
4. **No built-in A/B testing, heatmaps, or analytics.** SeedProd builds pages; measurement needs a separate tool.
5. **Pricing is annual, intro-priced, and renews at full rate.** The headline price isn't the renewal price; functionality is "basic" relative to full page builders per reviewers.
6. **Nested div output can hurt Core Web Vitals.** Heavily styled pages need caching/minification; compare against Gutenberg-native builders if speed is critical.
7. **Abilities API requires WordPress 6.9 and SeedProd 6.20.0+.** On older cores it isn't registered — the AI-tool/automation path silently won't exist.

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, and builder selection across tools (Elementor, ClickFunnels, Leadpages, Instapage, WordPress builders)
- `/sales-spectra` — Gutenberg-native WordPress block builder plugin — an alternative that extends the block editor instead of replacing the theme
- `/sales-kadence` — Kadence Blocks: a Gutenberg page-builder block plugin (by StellarWP) — another self-hosted WordPress alternative that extends the block editor
- `/sales-generateblocks` — GenerateBlocks: a minimalist, performance-first Gutenberg block plugin (by EDGE22/GeneratePress) — another self-hosted WordPress alternative that extends the block editor
- `/sales-stackable` — Stackable: a design-focused Gutenberg-native block plugin (by Gambit Technologies) — another self-hosted WordPress alternative that extends the block editor
- `/sales-instapage` — Instapage platform help — a hosted post-click/landing-page alternative with a REST API and A/B testing
- `/sales-leadpages` — Leadpages platform help — a hosted budget landing-page alternative
- `/sales-vwo` — A/B testing and heatmap methodology SeedProd lacks natively
- `/sales-audience-growth` — Growing an email list (lead magnets, opt-in strategy, referrals)
- `/sales-email-marketing` — Email sequences to run after a SeedProd opt-in captures the lead
- `/sales-integration` — Connect SeedProd to a CRM or ESP via Zapier or the Abilities API
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Automate coming-soon mode for a launch via the Abilities API
**User**: "Can I flip my SeedProd coming-soon page on and off from a script or AI tool?"
**Approach**: Yes — SeedProd registers the WordPress **Abilities API** (WP 6.9 + SeedProd 6.20.0+) with named actions `toggle-coming-soon` and `toggle-maintenance`, plus `get-status` to read the current state, `list-pages`, and `save-page`. A connected AI tool (WPVibe/Claude) or any REST client that speaks the Abilities API can discover and invoke them — no per-integration glue. Pull the action list, requirements, and the standard WP REST authentication note (application passwords) from `references/seedprod-api-reference.md`.

### Example 2: My whole site shows the coming-soon page and I can't get in
**User**: "I uninstalled SeedProd but my site is still stuck on the coming soon page."
**Approach**: The coming-soon/maintenance mode is still enabled (or cached). If you still have admin: SeedProd → Pages → set Coming Soon Mode to Inactive, then purge page/CDN cache. If locked out: rename the `seedprod`/`coming-soon-page-by-seedprod` plugin folder via FTP or hosting file manager to force-deactivate, then clear cache. As a last resort, flip the active flag in the `wp_posts`/SeedProd settings via phpMyAdmin. See Troubleshooting.

### Example 3: Which plan do I need to connect WooCommerce and Zapier?
**User**: "I want to use SeedProd's Theme Builder with WooCommerce and push leads through Zapier — what tier?"
**Approach**: **Theme Builder** unlocks at **Plus ($199)**, **Zapier (3000+) and Dynamic Text** at **Pro ($399)**, but **WooCommerce support and Domain Mapping are Elite ($599) only**. So WooCommerce + Zapier together requires **Elite**. Note pricing is annual/intro and renews at full; confirm in `references/platform-guide.md`.

## Troubleshooting

### Site stuck on the coming-soon / maintenance page
**Symptom**: The whole site shows the coming-soon or maintenance page — sometimes even after deactivating or uninstalling the plugin.
**Cause**: Coming Soon / Maintenance Mode is still toggled on, or a page/object cache or CDN is serving the cached coming-soon page.
**Solution**: In SeedProd → Pages, set Coming Soon Mode (and Maintenance Mode) to **Inactive**, then clear all caches (page cache plugin, host cache, CDN). If you're locked out of wp-admin, force-deactivate by renaming the plugin folder over FTP/file manager, then clear cache. Last resort: disable the active flag in the database.

### Pages built in SeedProd won't display
**Symptom**: You built pages with SeedProd and set the SeedProd theme as default, but the pages don't appear on the live site.
**Cause**: The Theme Builder template conditions/priority aren't matching the URL, the SeedProd theme isn't actually enabled, or a caching/permalink issue.
**Solution**: Confirm the SeedProd Theme Builder is toggled **on** and the template's display conditions include the page; flush permalinks (Settings → Permalinks → Save) and clear cache. For single landing pages (not full themes), publish the page directly rather than relying on the theme.

### Expected feature is missing or pricing surprised me
**Symptom**: WooCommerce blocks, Zapier, Dynamic Text, or the Theme Builder aren't available — or the renewal charge is higher than expected.
**Cause**: Plan gating (Theme Builder = Plus+, Zapier/Dynamic Text = Pro+, WooCommerce + Domain Mapping = Elite) and intro pricing that renews at full price.
**Solution**: Check the current license tier in SeedProd → Settings. Upgrade to the tier that unlocks the feature (Elite for WooCommerce), and budget for the full renewal rate rather than the introductory price.
