---
name: sales-gutenverse
description: "Gutenverse platform help — free Gutenberg-native FSE block plugin + ecosystem for WordPress by Jegstudio (57 blocks, 600+ starter templates, popup builder, mega menu, global colors/fonts, Unibiz companion theme, plus a separate free Gutenverse Form plugin with WordPress-stored entries). Use when the Gutenverse editor won't load or breaks after a customization change, color or style changes work in the editor but don't apply on the frontend, blocks vanish or break after a plugin update, you're isolating a plugin conflict, deciding which plan unlocks the form builder / dynamic data / display conditions / custom fonts, form submissions need email notifications or spam protection, or reading/writing gutenverse/-namespaced block markup via the WordPress REST API. Do NOT use for cross-tool builder selection or funnel/CRO strategy (use /sales-funnel) or checkout/cart across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in Gutenverse]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
github: "https://github.com/Jegstudio"
---

# Gutenverse Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken state — the editor page won't load or breaks after a customization change, colors/styles apply in the editor but not on the frontend, blocks vanished or broke after an update, or a plugin conflict
   - B) Build with blocks — layout/section structure, content/interactive blocks (Tabs, Accordion, Testimonials, Countdown, Chart), the popup builder, mega menu, Post/Query blocks, the 600+ starter template library, global colors/fonts
   - C) Capture leads — the **separate Gutenverse Form plugin** (form blocks, entries stored in WordPress, CSV export, reCAPTCHA, admin/user email notifications); Pro form features (conditional logic, multi-step, calculation/payment fields)
   - D) Use Pro/dynamic features — dynamic data, display/visibility conditions, custom fonts, premium templates/blocks, sticky/cursor effects, Lottie animations
   - E) Customize/automate — the `gutenverse-core` framework hooks (`gutenverse_after_init_framework`, `gutenverse_include_block`, `gutenverse_block_config`), reading/writing `gutenverse/`-namespaced block markup via the WordPress REST API
   - F) Pick or compare a plan (Free / Pro Professional / Agency) or weigh Gutenverse vs other block builders

2. **Free or Pro?** Free (WordPress.org) ships all 57 blocks + the template library + popup builder + global colors/fonts + responsive editing. **Form builder advanced features, dynamic data, display conditions, custom fonts, premium templates/blocks, and the mega menu are Pro.** The **Gutenverse Form** plugin is a separate free install.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, builder selection across tools (Spectra/Kadence/GenerateBlocks/Stackable/SeedProd/Elementor…) | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| A/B testing methodology (Gutenverse has no native split testing) | `/sales-vwo` — Run: `/sales-vwo {user's original question}` |
| Email sequences/automation after a form opt-in | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| WooCommerce store/checkout (Gutenverse builds pages, WooCommerce blocks are "coming soon") | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |
| WordPress/WooCommerce funnel + upsells around the pages | `/sales-cartflows` — Run: `/sales-cartflows {user's original question}` |
| On-page/technical SEO and Core Web Vitals beyond clean markup | `/sales-seo` — Run: `/sales-seo {user's original question}` |

If the question is Gutenverse-specific, continue to Step 3.

## Step 3 — Gutenverse platform reference

**Read `references/platform-guide.md`** for the full platform reference — blocks/modules, the Form plugin, pricing/plan gates, data model, integration recipes, and code examples. For the `gutenverse-core` framework hooks, the `gutenverseCore.*` packages, and the WordPress REST API approach to `gutenverse/`-namespaced markup, read `references/gutenverse-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **"The editor page won't load / breaks after a change" is the #1 reported issue.** It typically appears right after a customization change and clears when Gutenverse is deactivated — a JS conflict or a corrupted block. Update Gutenverse, hard-refresh and clear browser + page cache, then bisect by disabling other plugins (and switching to a default theme) until the conflict surfaces. Keep a staging copy before editing a live site.
- **"Colors/styles work in the editor but not on the frontend"** is a styling-cache/asset-loading mismatch. Regenerate/clear Gutenverse's style cache, clear page/object/CDN cache, and allowlist Gutenverse's CSS/JS in any minify/optimization plugin. v3.4.0+ added an improved styling cache mechanism — make sure you're current.
- **Forms are a separate plugin with a deliberately small surface.** Gutenverse Form stores entries **in WordPress** (CSV export), sends **admin + user email notifications**, and offers a **reCAPTCHA** block — but the free plugin has **no webhooks, no Zapier/Mailchimp/CRM integrations, no conditional logic, no multi-step, and no payment fields** (those are Pro). For anything beyond simple capture + email, pair a dedicated form plugin and route the sequence via `/sales-email-marketing`.
- **Plan gating drives most surprises.** All 57 blocks, the template library, the popup builder, and global colors/fonts are **free**. **Dynamic data, display conditions, custom fonts, premium templates/blocks, the mega menu, and advanced form features are Pro** (and degrade if the license lapses). Confirm the tier before promising a feature — and treat pricing as best-effort/annual.
- **Know what's "coming soon."** WooCommerce blocks, custom fields, and Query Loop for custom post types were marketed as upcoming, not shipped. Don't assume them; verify against the current changelog.
- **The automation surface is WordPress, not a hosted API.** No Gutenverse REST API, no outbound webhook, no Zapier app. Read/write block markup through the **WordPress core REST API** (blocks are `gutenverse/`-namespaced in `post_content`, Application-Password auth); extend the editor via the **`gutenverse-core`** hooks (`gutenverse_after_init_framework`, `gutenverse_include_block`, `gutenverse_block_config`) and the `gutenverseCore.*` ES6/window packages. It's open source under `github.com/Jegstudio` — deeper extension means building against the core framework.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

1. **Editor page failing to load after a customization change is the top reported problem.** The frontend still renders; deactivating Gutenverse restores the editor. Treat it as a JS conflict/corrupted block — update, clear cache, bisect plugins on staging before touching a live site.
2. **Color/style changes applying in the editor but not on the frontend** is a styling-cache/asset issue. Regenerate Gutenverse's style cache, clear page/CDN cache, and exclude its assets from minify/optimize plugins. Stay on v3.4.0+ for the improved cache mechanism.
3. **The form builder is a separate free plugin (`gutenverse-form`)** — and the free tier has **no webhooks, no Zapier/Mailchimp/CRM, no conditional logic, no multi-step, no payment fields**. Entries are stored in WordPress with CSV export; anti-spam is reCAPTCHA only (a third-party Cloudflare Turnstile add-on exists).
4. **Dynamic data, display conditions, custom fonts, premium templates/blocks, the mega menu, and advanced form features are Pro** and stop applying if the license lapses — test on staging.
5. **WooCommerce blocks, custom fields, and CPT Query Loop were "coming soon," not guaranteed shipped.** Verify against the current changelog before promising them.
6. **No hosted REST API, no outbound webhook, no Zapier app.** Automate via the WordPress core REST API (`gutenverse/` block markup in `post_content`) and the `gutenverse-core` framework hooks. Form leads exit through email or whatever form plugin you pair with it.
7. **No native A/B testing, heatmaps, or analytics.** Gutenverse builds pages; measurement needs a separate tool (VWO, Microsoft Clarity).

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, and builder selection across tools (Spectra, Kadence Blocks, GenerateBlocks, Stackable, SeedProd, Elementor, ClickFunnels, Leadpages)
- `/sales-stackable` — Another design-focused, Gutenberg-native block plugin — compare blocks, footprint, Pro gates, and note Stackable has no form/popup builder where Gutenberg-verse ships both
- `/sales-spectra` — A Gutenberg-native block plugin (by Brainstorm Force) that also ships a Popup Builder + Starter Templates — compare blocks, DOM output, and Pro Dynamic Content
- `/sales-kadence` — A Gutenberg block plugin (by StellarWP) with an Advanced Form block + webhooks and Kadence AI — compare form/automation depth vs Gutenverse Form
- `/sales-generateblocks` — The minimalist, performance-first Gutenberg block plugin — compare its few-primitives, lean-DOM model against Gutenverse's 57 ready-made blocks
- `/sales-seedprod` — A WordPress page/landing-page builder plugin (non-Gutenberg alternative with Theme Builder + coming-soon pages)
- `/sales-cartflows` — WordPress/WooCommerce funnel + checkout/upsells around the pages Gutenverse builds
- `/sales-vwo` — A/B testing and heatmap methodology Gutenverse lacks natively
- `/sales-audience-growth` — Growing an email list (lead magnets, opt-in strategy) behind a form
- `/sales-email-marketing` — Email sequences to run after a Gutenverse Form captures the lead
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Read and bulk-edit Gutenverse block markup programmatically
**User**: "I want to update the CTA text inside a Gutenverse Button across 30 landing pages from a script. Is there an API?"
**Approach**: There's **no Gutenverse REST API** — use the **WordPress core REST API**. Gutenverse blocks are `gutenverse/`-namespaced block markup in each post's `content` field (with attributes like a unique element id), so authenticate with an **Application Password**, `GET` the post `content`, transform the `<!-- wp:gutenverse/button … -->` markup, and `POST` it back. To change rendered output instead of stored content, hook WordPress core `render_block`; to extend the editor, use the `gutenverse-core` framework hooks. Pull the snippets from `references/gutenverse-api-reference.md`.

### Example 2: My Gutenverse editor stopped loading after I changed a section
**User**: "After editing a section, the Gutenverse editor screen just won't load anymore — but the live site is fine."
**Approach**: This is the top reported Gutenverse issue. The frontend rendering while the editor breaks points to a JS conflict or a corrupted block introduced by that edit. Update Gutenverse to the latest version, hard-refresh and clear browser + page cache, then on a **staging copy** disable other plugins (and switch to a default theme) one at a time to isolate the conflict; if a single block is corrupt, remove/re-add it. See Troubleshooting.

### Example 3: Which plan do I need for a form with conditional logic and dynamic content?
**User**: "I want a multi-step contact form with conditional fields, and I want to bind block content to custom fields. What tier?"
**Approach**: Both are **Pro**. Gutenverse Form's free tier covers basic fields, WordPress-stored entries, CSV export, email notifications, and reCAPTCHA — but **conditional logic, multi-step, calculation/payment fields are Pro**, and **dynamic data / display conditions** in the page blocks are Pro too. Pro is annual (~$79–99/yr for the Professional/10-site tier; an Agency/100-site tier exists). Treat pricing as best-effort and confirm current tiers and site counts in `references/platform-guide.md`; warn that Pro features degrade if the license lapses.

## Troubleshooting

### The Gutenverse editor page won't load (frontend still works)
**Symptom**: After making a customization change, the block editor screen fails to load; deactivating Gutenverse lets the editor load again. The published frontend is unaffected.
**Cause**: A JavaScript conflict with another plugin/theme, a corrupted block from the last edit, or a stale editor build/cache.
**Solution**: Update Gutenverse to the latest version; hard-refresh and clear browser + page/object cache; on a staging copy, deactivate all other plugins and switch to a default theme, then re-enable one at a time to find the conflict. If one block is the culprit, delete and re-insert it. Keep a backup before editing live.

### Color or style changes don't show on the frontend
**Symptom**: A color, spacing, or typography change looks right in the editor but the published page doesn't reflect it.
**Cause**: Gutenverse's per-page styling cache is stale, a caching/CDN layer is serving old CSS, or a minify/optimization plugin stripped or reordered Gutenverse's assets.
**Solution**: Regenerate/clear Gutenverse's style cache and clear page/object/CDN cache; allowlist Gutenverse's CSS/JS in any minify/combine plugin; confirm you're on v3.4.0+ (improved styling cache). Re-check in an incognito window to rule out the browser cache.

### Form submissions aren't reaching me / are full of spam
**Symptom**: Gutenverse Form entries don't arrive by email, or the inbox fills with spam.
**Cause**: Missing/failing site email (no SMTP), notification not configured, or anti-spam limited to reCAPTCHA on the free plugin (no webhooks/CRM routing, no honeypot beyond reCAPTCHA).
**Solution**: Confirm admin + user email notifications are enabled on the form and that WordPress can send mail (add an SMTP plugin if deliverability is poor); entries are also stored in WordPress with CSV export as a fallback. Enable the reCAPTCHA block; for stronger protection add a Cloudflare Turnstile add-on, and for routing leads into a CRM/sequence pair a dedicated form plugin and use `/sales-email-marketing`.
