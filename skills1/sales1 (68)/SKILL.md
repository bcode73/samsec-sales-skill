---
name: sales-breakdance
description: "Breakdance platform help — standalone visual website/page builder for WordPress (by Soflyy, the Oxygen makers): a front-end editor that replaces the theme, with a WooCommerce Builder, Form Builder + Popup Builder, Dynamic Data, Element Studio (custom-element IDE), Breakdance AI, and a real PHP developer API (Form Actions API, Dynamic Data Field API, Conditions API, hooks/filters). Use when a Breakdance form notification still emails you after a spam plugin blocked the entry, building a custom Form Action or Dynamic Data field, routing Breakdance AI to OpenRouter/Claude via the AI endpoint filters, migrating an Oxygen site, registering a custom element or display condition, building WooCommerce product templates, pages are slow despite the lean builder, or choosing Breakdance Free vs Pro (no lifetime plan). Do NOT use for cross-tool builder selection or funnel/CRO strategy (use /sales-funnel), A/B testing/heatmaps (use /sales-vwo), or checkout/cart across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in Breakdance]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
github: "https://github.com/soflyy/breakdance-developer-docs"
---

# Breakdance Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken state — form notifications still emailing after a spam plugin blocked the entry, form submissions not stored/not arriving, builder deactivated/blank after a migration, slow pages despite the lean builder, AI settings UI not reflecting a filter change
   - B) Build with the UI — Elements, Templates/Design Library, the **WooCommerce Builder** (product/shop/cart/checkout templates), the **Form Builder** (multi-step, conditional fields), the **Popup Builder**, **Dynamic Data** (loops/repeaters/conditional display), global blocks, headers/footers
   - C) Extend with code — a custom **Form Action**, a custom **Dynamic Data field**, an **Element Display Condition**, a custom element in **Element Studio**, reusable dependencies, or one of the `breakdance_*` hooks/filters
   - D) Connect data or AI — POST a form to Zapier/Make via the **Webhook action**, route **Breakdance AI** to a different model/provider (OpenRouter, Claude) with the AI endpoint filters, or read/write page markup via the WordPress REST API
   - E) Pick or compare a plan (Free vs Pro / +AI bundle), weigh Breakdance vs Bricks/Elementor/Oxygen, or plan an **Oxygen→Breakdance** migration

2. **Free or paid?** **Breakdance Free** (WordPress.org) ships ~80 elements + the core builder. **Pro (~$199.99/yr, unlimited sites + unlimited domain activations)** unlocks all ~145 elements, the full Design Library, the WooCommerce Builder, the Form Builder/Popup Builder, Global Blocks, and Client Mode. There is **no lifetime plan** (annual subscription with a price-lock guarantee). *(Pricing best-effort — verify.)*

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, builder selection across tools (Bricks/Elementor/Oxygen/Beaver Builder/Gutenberg…) | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| A/B testing methodology (Breakdance has no native split testing) | `/sales-vwo` — Run: `/sales-vwo {user's original question}` |
| Email sequences/automation after a form opt-in | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| WooCommerce store/checkout strategy across platforms | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |
| WordPress/WooCommerce funnel + upsells around the pages | `/sales-cartflows` — Run: `/sales-cartflows {user's original question}` |
| On-page/technical SEO beyond clean markup | `/sales-seo` — Run: `/sales-seo {user's original question}` |

If the question is Breakdance-specific, continue to Step 3.

## Step 3 — Breakdance platform reference

**Read `references/platform-guide.md`** for the full platform reference — modules, pricing/plan gates, data model, integration recipes, and the Oxygen relationship. For the **developer APIs** (Form Actions API, Dynamic Data Field API, Conditions API, the `breakdance_*` hooks/filters, AI endpoint filters, Menu/Animations JS APIs, and the WordPress REST surface), read `references/breakdance-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **Breakdance is a standalone visual builder, not a Gutenberg block plugin.** It builds pages in its own front-end editor and is **themeless by default** (it can replace the theme entirely) — closer to Elementor/Beaver Builder/Oxygen than to Spectra/Kadence/GenerateBlocks. Pages are **Sections/Elements**, not native blocks, so they live in Breakdance's own data, not as portable Gutenberg block markup.
- **The form "spam still emails me" trap is real and the #1 gotcha.** Breakdance runs form **Actions After Submit** in order, but it **does not let plugins intercept the Email action** — so a spam-filter plugin can block storage yet the Email notification still fires. Fix: order the spam-check action **above** Store Submission and Email, and for hard cases **remove the Email action entirely** and send notifications downstream (Make/Zapier) off the Webhook action. Enable the built-in **honeypot** (off by default) and **reCAPTCHA v3** (the only version supported).
- **Breakdance AI is model/provider-swappable via filters.** `breakdance_ai_api_endpoint` + `breakdance_ai_model` let you point it at OpenRouter (and an Anthropic Claude model) or any OpenAI-compatible endpoint; `breakdance_ai_enabled` toggles it. **The WP-Admin AI Assistant settings UI won't reflect these filter changes** — verify by watching the developer console and the provider's usage charts. The API key still goes in the "OpenAI API Key" field regardless of provider.
- **Register custom Form Actions / Dynamic Data fields / Conditions on `init`** and guard with `function_exists()` / `class_exists()` so the plugin fails gracefully when Breakdance is inactive — the docs explicitly call out file-loading race conditions otherwise. Custom elements are built in **Element Studio**, which also has a code escape hatch (PHP/HTML/CSS) and reusable dependencies (`%%BREAKDANCE_REUSABLE_*%%`, incl. predefined GSAP/ScrollTrigger).
- **Performance is the pitch, but it's not automatic.** Breakdance markets a 45 KB blank page (vs Elementor's ~576 KB), conditional asset loading, and jQuery-independence. But slow real-world pages almost always come from **misuse** — bad layout structure, heavy Dynamic Data loops, unoptimized images, no caching — not the builder. Audit those (and the theme/host) before blaming Breakdance.
- **The real automation surface is WordPress + the form Webhook action**, not a hosted Breakdance API. There is **no hosted REST API and no platform-level outbound webhook**; the Form Builder's **Webhook action** POSTs submissions to Zapier/Make, and you read/write page content via the **WordPress core REST API** (Breakdance page data is in post meta, not portable block markup — see the reference). Migrating from **Oxygen**: Oxygen 6 runs on the Breakdance engine and Oxygen lifetime licenses now include it; for Oxygen *Classic* content, conversion is done with a third-party JSON converter (e.g. TransferForge), not a native importer.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features, pricing, and integration details that may be outdated.*

1. **Spam plugins can't stop Breakdance's Email action.** Even when a spam filter blocks a submission, the **Email** notification action can still send, because Breakdance doesn't expose an interception point for it. Order the spam-check action above Store/Email, or remove the Email action and notify via the Webhook action + Make/Zapier.
2. **Honeypot is off by default; reCAPTCHA is v3-only.** Enable the honeypot field explicitly; Breakdance forms support **reCAPTCHA v3 only** (not v2 checkbox).
3. **No lifetime plan.** Breakdance is annual-subscription only (~$199.99/yr unlimited sites) with a **price-lock guarantee** at renewal — unlike Bricks/Divi which sell lifetime. Don't promise a one-time license. *(Pricing best-effort — verify.)*
4. **The AI settings UI doesn't reflect endpoint/model filters.** After applying `breakdance_ai_api_endpoint`/`breakdance_ai_model`, the Breakdance → Settings → AI Assistant screen is unchanged; verify via the browser console and the provider's usage dashboard. The key always goes in the "OpenAI API Key" field.
5. **Register extensions on `init` with guards.** Form Actions, Dynamic Data fields, and Conditions must be registered inside a WordPress action (e.g. `init`) and wrapped in `function_exists()`/`class_exists()` checks to avoid file-loading race conditions when Breakdance isn't active.
6. **Oxygen migration is engine-shared but not one-click for Classic.** Oxygen 6 is rebuilt on the Breakdance engine (and is included in the Oxygen lifetime license), but converting **Oxygen Classic** layouts uses a third-party JSON converter, not a built-in importer — test on staging and expect manual cleanup.
7. **Themeless by default = your theme's templates may not apply.** Breakdance can replace the theme; if headers/footers/archives look wrong, confirm whether Breakdance Templates (not the theme) are controlling that area.
8. **No native A/B testing, heatmaps, analytics, or hosted REST API.** It's a WordPress builder — measure with a separate tool (VWO, Microsoft Clarity) and automate via the WordPress REST API + the form Webhook action.

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, and builder selection across tools (Bricks, Elementor, Oxygen, Beaver Builder, SeedProd, ClickFunnels, Leadpages)
- `/sales-beaver-builder` — Another standalone WordPress page builder (Rows/Columns/Modules + a PHP module API) — the closest "not-a-block-plugin" comparison to Breakdance
- `/sales-seedprod` — A WordPress page + Theme Builder plugin — compare theme-replacement, templates, and developer surface vs Breakdance
- `/sales-spectra` — A Gutenberg-native block plugin — the block-editor contrast to Breakdance's standalone editor and proprietary page data
- `/sales-greenshift` — A Gutenberg block plugin whose API Connector binds external/LLM APIs — compare data/AI integration vs Breakdance's AI endpoint filters + form Webhook action
- `/sales-cartflows` — WordPress/WooCommerce funnel + checkout/upsells around the pages Breakdance builds (CartFlows supports Breakdance for step design)
- `/sales-vwo` — A/B testing and heatmap methodology Breakdance lacks natively
- `/sales-audience-growth` — Growing an email list (lead magnets, opt-in strategy) behind a form
- `/sales-email-marketing` — Email sequences to run after a form captures the lead
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: A spam-filter plugin blocks the entry but I still get the email
**User**: "I added OOPSpam to my Breakdance form. Spam entries stop being stored, but I still get the email notifications. How do I stop the spam emails?"
**Approach**: This is Breakdance's best-known form gotcha — it runs **Actions After Submit** in order but **doesn't let a plugin intercept the Email action**, so the notification fires even when the spam plugin blocks storage. Fix: open the form → **Actions After Submit** → drag the spam-check action **above** "Store Submission" and "Email" so bad entries are stopped first; for hard cases **remove the Email action entirely** and send notifications downstream via the **Webhook action → Make/Zapier**, filtering spam there. Also enable the built-in **honeypot** (off by default) and **reCAPTCHA v3** (the only version supported). Pull the exact action ordering and webhook setup from `references/platform-guide.md`.

### Example 2: Build a custom Form Action (log/forward submissions in PHP)
**User**: "I want to run my own code on every Breakdance form submission — send it to my CRM. How do I write a custom Form Action?"
**Approach**: Breakdance has a public **Form Actions API**. Create a class extending `Breakdance\Forms\Actions\Action` and implement `name()`, `slug()` (unique, prefixed), and `run($form, $settings, $extra)` — `$extra` carries `fields` (`id ⇒ value`), `formId`, `postId`, `ip`, `referer`, `userAgent`, `userId`, and uploaded `files`. Return `['type' => 'success'|'error', 'message' => '...']`. **Register it on `init`**, guarded with `function_exists('\Breakdance\Forms\Actions\registerAction')` / `class_exists('\Breakdance\Forms\Actions\Action')`, then `registerAction(new MyAction())`. POST `$extra['fields']` to your CRM inside `run()`. The full class skeleton and argument shapes are in `references/breakdance-api-reference.md`.

### Example 3: Route Breakdance AI to Claude via OpenRouter
**User**: "Can I make Breakdance AI use Claude instead of OpenAI?"
**Approach**: Yes — Breakdance AI exposes filters. Use `breakdance_ai_api_endpoint` to return `https://openrouter.ai/api`, and `breakdance_ai_model` to return an Anthropic model string (e.g. `anthropic/claude-3.5-sonnet`); paste your **OpenRouter** key into Breakdance → Settings → AI Assistant's **"OpenAI API Key"** field (the field name doesn't change). Note the settings UI won't visibly change — **verify via the browser console and OpenRouter's usage charts**. `breakdance_ai_enabled` (`__return_false`) disables AI entirely. Exact filter signatures and code are in `references/breakdance-api-reference.md`; flag that model availability/credits depend on the provider.

## Troubleshooting

### Form notifications still email me after a spam plugin blocks the entry
**Symptom**: A spam-protection plugin stops spam submissions from being stored, but email notifications keep arriving.
**Cause**: Breakdance runs Actions After Submit in sequence but **does not allow plugins to intercept the Email action**, so it can still send.
**Solution**: In the form's **Actions After Submit**, drag the spam-check action **above** "Store Submission" and "Email". For stubborn cases, **remove the Email action** and send notifications downstream via the **Webhook action → Make/Zapier**, filtering spam there. Enable the honeypot (off by default) and reCAPTCHA v3.

### Form submissions aren't stored or aren't arriving
**Symptom**: A submitted form shows no entry under Breakdance → Form Submissions, or no notification arrives.
**Cause**: The **Store Submission** action isn't enabled, the Email action is misconfigured/blocked by the host's mail setup, or an earlier action errored and halted the chain.
**Solution**: Add/enable the **Store Submission** action; check each action's "details" under Breakdance → Form Submissions for per-action status; use an SMTP plugin for reliable email; confirm action ordering so a failing action doesn't block the rest.

### Pages are slow even though Breakdance is "lean"
**Symptom**: Poor PageSpeed/Core Web Vitals on a Breakdance site despite the builder's lightweight reputation.
**Cause**: Almost always **misuse** — over-nested layout structure, heavy Dynamic Data loops, unoptimized images, no caching — or the theme/host, not the builder.
**Solution**: Simplify section/layout nesting, limit Dynamic Data query size, compress/serve modern images, add a caching layer/CDN, and audit the theme + third-party scripts. Confirm conditional asset loading is doing its job before attributing slowness to Breakdance.

### Breakdance AI ignores my endpoint/model filter
**Symptom**: After adding `breakdance_ai_api_endpoint`/`breakdance_ai_model`, the AI Assistant settings screen looks unchanged and you're unsure it's working.
**Cause**: Expected — the WP-Admin AI Assistant UI **does not reflect** these filters.
**Solution**: Verify by watching the **browser developer console** during an AI action and checking the **provider's usage dashboard** (e.g. OpenRouter). Ensure the API key for the *active* endpoint is in the "OpenAI API Key" field and that the model string matches the provider's exact identifier.
