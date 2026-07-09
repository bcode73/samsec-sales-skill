---
name: sales-superb-addons
description: "Superb Addons platform help — Gutenberg-native WordPress block-addon plugin by SuperbThemes (slug superb-blocks, 80k+ installs): 20 blocks, 200+ patterns, 50+ pre-built pages, a form builder (multi-step, calculated fields, Mailchimp/Brevo/Google Sheets/Slack + webhook integrations, honeypot/hCaptcha/reCAPTCHA/Turnstile), a Popup block with smart triggers, 70+ animations, a Theme Designer, and responsive visibility controls. Use when the Theme Designer won't load or respond when clicked, you're unsure whether forms/popups/animations are free or Premium-gated, you want to send Superb form submissions to a CRM via webhook or Mailchimp, saved form submissions aren't showing in wp-admin, Superb blocks render unstyled on inner pages, a conflict with another block plugin (e.g. Gutenverse) breaks the editor, or choosing Free vs Premium. Do NOT use for cross-tool block-builder selection or funnel/CRO strategy (use /sales-funnel) or checkout across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in Superb Addons]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
---

# Superb Addons Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken state — Theme Designer won't load/respond, blocks or CSS unstyled on inner pages, editor breaks after an update or a conflict with another block plugin (e.g. Gutenverse), saved form submissions not showing in wp-admin
   - B) Build with blocks — patterns/pre-built pages, Popup block, Carousel/Slider, Countdown, animations, responsive visibility, Theme Designer layouts
   - C) Forms & lead capture — multi-step forms, calculated fields, conditional logic, anti-spam, where submissions are stored
   - D) Connect/automate — send form submissions to a webhook, Mailchimp, Brevo, Google Sheets, or Slack; read content via the WordPress REST API; hooks/filters
   - E) Pick or compare a plan (Free vs Premium yearly vs lifetime) or weigh Superb Addons vs other block plugins

2. **Free or Premium?** The plugin is freemium. The WordPress.org readme markets a "free form builder," but the marketing pricing page lists Forms, Popups, 70+ animations, sliders, and the Theme Designer as Premium. Plan gating is genuinely ambiguous — confirm what's unlocked on the actual install before promising a feature (see Gotchas).

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, builder selection across tools (Spectra/Kadence/GenerateBlocks/Stackable/Elementor…) | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| A/B testing methodology (Superb Addons has no native split testing) | `/sales-vwo` — Run: `/sales-vwo {user's original question}` |
| Email sequences/automation after a Superb form opt-in | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy behind the form/popup | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| WooCommerce checkout/cart beyond the Add to Cart block | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |
| On-page/technical SEO and Core Web Vitals beyond Superb's blocks | `/sales-seo` — Run: `/sales-seo {user's original question}` |

If the question is Superb-Addons-specific, continue to Step 3.

## Step 3 — Superb Addons platform reference

**Read `references/platform-guide.md`** for the full reference — blocks/modules, pricing/plan gates, the form data model, and integration recipes. For the form webhook/integration surface, anti-spam config, and WordPress REST/hooks notes, read `references/superb-addons-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **Theme Designer not loading/responding is the most-reported issue.** First update Superb Addons to the latest version, then run the built-in **Troubleshooter** (wp-admin → Superb Addons → Get Help → Start Troubleshoot Process), which isolates plugin/theme conflicts. A known conflict: **Theme Designer previews break when Gutenverse is active** — deactivate the other block plugin to confirm, then clear caches.
- **Plan-gating ambiguity drives surprises.** Don't assume forms/popups/animations are free just because the readme says so — verify the capability is active on the install. Multi-step forms, integrations, smart popup triggers, the full animation set, and Theme Designer layouts behave as Premium features.
- **"Blocks unstyled on inner pages"** is the generic block-plugin CSS/asset issue — clear any caching/optimization plugin and CDN, and re-save/regenerate the affected page; allowlist the plugin's assets in minify/security plugins.
- **The real automation surface is the form builder, not a hosted API.** Superb has **no public REST API**. To get a lead out: add a **webhook** to the form (POSTs the submission to your URL) or use the native **Mailchimp / Brevo / Google Sheets / Slack** integrations. Block content is readable via the **WordPress core REST API** (`/wp-json/wp/v2/...`) as namespaced block markup in `post_content`.
- **Submissions storage:** the form can store submissions in wp-admin, email admin/user notifications, and auto-delete for GDPR — but a permalink-config bug has hidden saved submissions in the dashboard; update first if they're missing.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

1. **What's free vs Premium is genuinely ambiguous.** The WordPress.org readme markets a free form builder ("no license or account needed"), while the SuperbThemes pricing page lists Forms, multi-step forms, Popups with smart triggers, 70+ animations, sliders, Theme Designer, visibility conditions, and advanced custom CSS as Premium. Verify each capability on the live install before relying on it.
2. **Theme Designer won't load / doesn't respond when clicked** is the top support pattern. Update the plugin, then use the built-in Troubleshooter to bisect conflicts; clear object/page/CDN cache.
3. **Conflict with other block plugins** — e.g. v4.0.5 fixed Theme Designer previews not rendering when **Gutenverse** is active. When the editor or previews misbehave, deactivate other block plugins to isolate.
4. **Saved form submissions may not display in the wp-admin dashboard** under some permalink configurations (a fixed bug) — update to the latest version and re-check Settings → Permalinks (re-save).
5. **No public hosted REST API and no inbound API.** Outbound automation is the form's webhook + Mailchimp/Brevo/Sheets/Slack integrations; read access is the WordPress core REST API over block markup.
6. **No native A/B testing, heatmaps, or analytics** — Superb builds pages and captures form leads; measurement needs a separate tool.
7. **Block-plugin deactivation risk** — like other Gutenberg block addons, pages built with Superb blocks can show invalid-block/raw-HTML warnings if the plugin is deactivated. Test on staging before removing it from a live site.

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, and block-builder selection across tools (Spectra, Kadence Blocks, GenerateBlocks, Stackable, Gutenverse, Elementor, SeedProd)
- `/sales-spectra` — The closest rival: another Gutenberg-native block plugin that also ships a form builder + Popup Builder; compare blocks, plan gates, and developer hooks
- `/sales-stackable` — Design-focused Gutenberg block plugin with no form/popup builder — Superb ships both; compare blocks and plan gates
- `/sales-gutenverse` — Free FSE block plugin (named in Superb's compatibility fixes) — useful when isolating an editor conflict
- `/sales-vwo` — A/B testing and heatmap methodology Superb lacks natively
- `/sales-audience-growth` — Growing an email list (lead magnets, opt-in strategy) behind a Superb form or popup
- `/sales-email-marketing` — Email sequences to run after a Superb form captures the lead (Mailchimp/Brevo and beyond)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Send Superb form submissions to my CRM
**User**: "When someone submits my Superb contact form I want the lead pushed into my CRM automatically — how do I do that without a plugin marketplace connector?"
**Approach**: Superb has no hosted API, so use the form's **Webhook** integration: on the Superb Form block, add a Webhook that POSTs the submission to an endpoint you control (or a Zapier/Make Catch Hook), then map fields into your CRM. If your CRM is Mailchimp/Brevo, use the native integration instead (no middleware). The exact payload schema isn't published — capture one live delivery to map field keys. See the recipe and field-mapping notes in `references/superb-addons-api-reference.md`.

### Example 2: Theme Designer won't open
**User**: "I click Theme Designer in Superb Addons and nothing happens / it never loads."
**Approach**: This is the top reported issue. Update Superb Addons to the latest version first (recent releases fixed Theme Designer rendering, including a conflict when **Gutenverse** is active). Then run the built-in **Troubleshooter** (Superb Addons → Get Help → Start Troubleshoot Process) to bisect plugin/theme conflicts, and clear object/page/CDN cache. See Troubleshooting.

### Example 3: Is the form builder actually free?
**User**: "The listing says Superb has a free form builder, but the pricing page lists Forms under Premium. Which is it?"
**Approach**: Plan gating is genuinely ambiguous between the WordPress.org readme and the marketing pricing page. Treat multi-step forms, calculated fields, integrations (Mailchimp/Brevo/Sheets/Slack/webhook), smart popup triggers, the full animation set, and Theme Designer layouts as **Premium**, and verify what's unlocked on the actual install before committing. Confirm current tiers/prices (Free; Premium ~$29–$49/yr or ~$59–$99 lifetime by site count) in `references/platform-guide.md` — pricing is best-effort.

## Troubleshooting

### Theme Designer won't load or respond
**Symptom**: Clicking Theme Designer does nothing, or it never finishes loading.
**Cause**: An outdated plugin version or a conflict with another block plugin/theme (a known one: previews failing when Gutenverse is active).
**Solution**: Update Superb Addons to the latest version. Run the built-in **Troubleshooter** (Superb Addons → Get Help → Start Troubleshoot Process) to isolate the conflict; deactivate other block plugins one at a time to confirm. Clear object cache, page cache, and CDN, then retry.

### Saved form submissions don't appear in the dashboard
**Symptom**: Form submissions are configured to be stored, but the admin list is empty.
**Cause**: A permalink-configuration bug that prevented saved submissions from displaying in wp-admin for some setups (addressed in a recent release).
**Solution**: Update to the latest version. Go to Settings → Permalinks and re-save (flushes rewrite rules). Submit a test entry and confirm it appears; also verify the form's "store submissions" option is enabled and email notifications are configured as a backup.

### Superb blocks render unstyled or broken on inner pages
**Symptom**: A pattern/page looks correct in the editor or on the homepage but unstyled on other pages.
**Cause**: The plugin's per-page CSS/assets aren't loading sitewide, or a caching/optimization/minify plugin is stripping or deferring them.
**Solution**: Clear page cache + CDN and re-save the affected page. In any minify/optimization/security plugin, **allowlist Superb's assets** (don't combine/defer them) and exclude its scripts from JS deferral. Confirm the page isn't pulling a stale cached version.
