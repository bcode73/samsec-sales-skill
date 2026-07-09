---
name: sales-greenshift
description: "Greenshift platform help — performance-focused Gutenberg page-builder + animation block plugin for WordPress (by Wpsoul): 50+ blocks, GSAP scroll/hover animations, Interaction Layers, 3D/Lottie/Rive, dynamic data + Query addon, and an API Connector that binds external REST or LLM APIs (incl. OpenAI chat/streaming) into blocks; plus AI Helpers (bring-your-own key), Figma/HTML/webpage→blocks converters, and a VS Code extension. Use when Greenshift styles won't load on the frontend, animations show on the front end but blank in the editor, patterns crash the editor or trigger 'too many requests' host errors, fonts/icons break after an HTTP→HTTPS move, building a Query loop or dynamic listing, wiring the API Connector to an external or AI API, choosing between Design/Woo/GreenLight PRO/All-in-One plans, or a Pro block drops to fallback after a license lapse. Do NOT use for cross-tool builder selection or funnel/CRO strategy (use /sales-funnel) or checkout/cart across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in Greenshift]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
github: "https://github.com/wpsoul/greenshift-ai-lab"
---

# Greenshift Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken state — styles missing on the frontend, animations show on the front end but blank in the editor, patterns crash the editor / "too many requests" host errors, fonts/icons break after an HTTP→HTTPS move, duplicate styles after copying a synced pattern
   - B) Build with blocks — layout/Container, animated headlines, counters, sliders, Interaction Layers, GSAP scroll/hover effects, 3D/Lottie/Rive, shape dividers
   - C) Use dynamic/Pro features — **Query addon** (post types, users, taxonomies, comments, ACF/ACPT repeaters, options, external repeaters), dynamic fields/placeholders, WooCommerce blocks, SEO/schema blocks
   - D) Connect data or AI — the **API Connector** (server-side or client-side) to bind an external REST API, a Google Sheet/CSV, or an **LLM API (OpenAI chat/streaming)** into blocks; **AI Helpers** (bring-your-own key) to generate blocks; Figma/HTML/webpage→blocks converters; the `GSPB_API_RESPONSE` JS event; reading/writing block markup via the WordPress REST API
   - E) Pick or compare a plan (Design Pack / Woo Pack / GreenLight PRO / All-in-One) or weigh Greenshift vs other block builders

2. **Free or paid?** The free WordPress.org plugin ships 50+ blocks and basic animations. **GSAP advanced animations, dynamic fields, the Query addon, the API Connector, AI Helpers/agents, the Figma converter, WooCommerce blocks, SEO/schema blocks, and the VS Code extension are paid** (split across Design / Woo / GreenLight PRO / All-in-One packs).

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, builder selection across tools (Kadence/Spectra/GenerateBlocks/SeedProd/Elementor…) | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| A/B testing methodology (Greenshift has no native split testing) | `/sales-vwo` — Run: `/sales-vwo {user's original question}` |
| Email sequences/automation after a form opt-in | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| WooCommerce store/checkout strategy across platforms | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |
| WordPress/WooCommerce funnel + upsells around the pages | `/sales-cartflows` — Run: `/sales-cartflows {user's original question}` |
| On-page/technical SEO beyond clean markup + schema blocks | `/sales-seo` — Run: `/sales-seo {user's original question}` |

If the question is Greenshift-specific, continue to Step 3.

## Step 3 — Greenshift platform reference

**Read `references/platform-guide.md`** for the full platform reference — blocks/modules, pricing/plan gates, data model, integration recipes, and code examples. For the **API Connector** (server-side + client-side, AI chat/streaming), the dynamic data / Query addon, the `GSPB_API_RESPONSE` event, and the WordPress REST surface, read `references/greenshift-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **The API Connector is the standout developer feature.** Unlike lean block plugins, Greenshift can fetch and bind an **external REST API, a Google Sheet/CSV, or an LLM API** into blocks with no glue code — server-side (data stored in the block, WordPress Application-Password auth) or client-side (browser `fetch`). Client-side supports **AI chat (message history) and streaming**. **Warning: client-side keys are public** — never put a secret API key in a client-side connector; proxy through the server-side connector or your own endpoint.
- **Performance is the pitch, but it's not automatic.** Greenshift loads ~2 KB base styles, conditional assets, no jQuery — leanest among feature-rich block plugins. But heavy GSAP/3D/Lottie blocks, the editor's API calls, and per-page CSS still cost. If Core Web Vitals are poor, check the *theme*, images, third-party scripts, and how many animation/3D blocks are on the page first.
- **"No styles on the frontend" is usually the inline-CSS save limit.** On huge pages, hosting/DB field limits can truncate saved styles. The fix is Greenshift Settings → CSS management → save styles **inline within blocks**, then re-save the page. (Confirm before promising — see Troubleshooting.)
- **Animations blank in the editor but fine on the front end is expected** for some scroll/GSAP effects — they render on the front end. Preview the published page rather than judging from the editor canvas.
- **Plan gating drives most surprises.** Free = 50+ blocks + basic animations. **GSAP advanced animations + dynamic fields + Figma converter + API Connector + AI Helpers + VS Code extension** live in **GreenLight PRO**; **WooCommerce blocks** in **Woo Pack**; **SEO/schema + charts + AI agents** in **All-in-One**. Confirm the pack before promising a feature.
- **Pro blocks/features degrade if the license lapses** — like other block plugins, paid-only styling/features can stop applying when the license expires. Don't ship a critical page solely on paid-only features without testing the fallback on staging.
- **The real automation surface is WordPress + the API Connector**, not a hosted Greenshift API: read/write block markup through the **WordPress REST API** (blocks are `greenshift-blocks/`-namespaced in `post_content`), pull dynamic data via the **Query addon**, bind external/AI APIs via the **API Connector**, and hook client-side responses with the `GSPB_API_RESPONSE` JS event. No outbound webhook from Greenshift itself.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

1. **"No styles on frontend" = inline-CSS save limit on big pages.** Hosting/DB field limits truncate saved styles; switch CSS management to save inline within blocks and re-save the page.
2. **Animations can show blank in the Gutenberg editor but work on the published page** — judge scroll/GSAP effects from the front end, not the editor canvas.
3. **Backend "too many requests" / editor freeze.** Heavy pages, the Button block, or many editor-side API calls can make a host throw request-rate errors or hang the editor. Split long pages; isolate the offending block; check host limits.
4. **HTTP→HTTPS leaves fonts/icons broken** because old `http://` static files don't load. Re-upload static files (remove old first) and confirm Settings → General shows the HTTPS URL.
5. **Duplicate synced patterns share style IDs.** After ungrouping a synced pattern, duplicate the *ungrouped* copy and delete the original so Greenshift regenerates unique IDs — otherwise styles collide/duplicate.
6. **Client-side API Connector keys are public.** Anyone can read a key placed in a client-side connector — use the server-side connector (or your own proxy) for anything secret, especially LLM API keys.
7. **Plan gates + license lapse.** GSAP advanced animations, dynamic fields, API Connector, AI Helpers, Figma converter, WooCommerce/SEO blocks, and the VS Code extension are paid; paid features can fall back if the license expires. Test on staging.
8. **Stay updated.** A historical security advisory (CVE-2023-6636) affected older versions — keep Greenshift current and avoid pirated/"nulled" builds.
9. **No hosted REST API, no outbound webhook, no native A/B testing/heatmaps.** It's a WordPress plugin: automate via the WordPress REST API + the API Connector; measure with a separate tool (VWO, Microsoft Clarity).

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, and builder selection across tools (Kadence Blocks, Spectra, GenerateBlocks, Stackable, Nexter, SeedProd, Elementor, ClickFunnels, Leadpages)
- `/sales-generateblocks` — A minimalist, performance-first Gutenberg block plugin — the lean-primitives contrast to Greenshift's feature breadth; compare DOM/CSS output and dynamic data
- `/sales-kadence` — A Gutenberg block plugin with 40+ ready-made blocks, a design system, and Kadence AI — compare blocks, dynamic content, and plan gates vs Greenshift
- `/sales-spectra` — Another Gutenberg-native block plugin (by Brainstorm Force) — compare animations, dynamic content, and hooks
- `/sales-stackable` — A design-focused Gutenberg-native block plugin (by Gambit Technologies) — breadth/design contrast
- `/sales-nexter` — An all-in-one Gutenberg ecosystem with a native MCP server — compare AI/forms/popups vs Greenshift's API Connector + AI Helpers
- `/sales-cartflows` — WordPress/WooCommerce funnel + checkout/upsells around the pages Greenshift builds
- `/sales-vwo` — A/B testing and heatmap methodology Greenshift lacks natively
- `/sales-audience-growth` — Growing an email list (lead magnets, opt-in strategy) behind a form
- `/sales-email-marketing` — Email sequences to run after a form captures the lead
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Bind an external (or AI) API into a block with the API Connector
**User**: "I want to pull live data from a REST API into a Greenshift block — and later call OpenAI from the page. How does the API Connector work and what's safe?"
**Approach**: Greenshift has no hosted API; its integration surface is the **API Connector**. Choose **server-side** (processes on the WP server, response stored in the block, supports Application-Password Basic auth and placeholders like `{{FORM:field}}`, `{{INCREMENT:1}}`, `{{USER_META:field}}`) for anything with a secret key or for WordPress endpoints; choose **client-side** (browser `fetch`, placeholders like `{{VALUE:.selector}}`, `{{COOKIE:name}}`) for public data and for **AI chat/streaming** (append messages to a `messages` array, extract `choices[0][message]`). **Never put a secret key in a client-side connector — they're public.** Map results via the template-block + result-container pattern, and hook the response with the `GSPB_API_RESPONSE` JS event. Pull the exact placeholder list, auth steps, and chat/streaming config from `references/greenshift-api-reference.md`.

### Example 2: Styles disappear on the frontend of a long page
**User**: "My Greenshift page looks fine in the editor but has no styling on the live site. It's a very long page."
**Approach**: This is the classic **inline-CSS save limit** — on huge pages, hosting/DB field length limits truncate the saved styles so they never reach the database. Fix: Greenshift Settings → CSS management → set styles to **save inline within blocks**, then re-open and re-save the affected page. Clear page/object/CDN cache afterward. If it persists, check for an HTTP→HTTPS mismatch (Settings → General URL) and re-uploaded static files. See Troubleshooting and `references/learnings.md`.

### Example 3: Which pack unlocks the API Connector / dynamic fields / WooCommerce?
**User**: "Which Greenshift plan do I need for the API Connector and dynamic fields, and is WooCommerce separate?"
**Approach**: The **API Connector, dynamic fields, GSAP advanced animations, AI Helpers, the Figma converter, and the VS Code extension are in GreenLight PRO**; **WooCommerce blocks are the Woo Pack**; **SEO/schema blocks, charts, and AI agents are All-in-One** (which bundles GreenLight PRO). The free WordPress.org plugin is 50+ blocks + basic animations only. Site counts scale by tier (single → 5 → unlimited) with annual and lifetime options (lifetime can be paid in crypto). Flag pricing as best-effort and verify on greenshiftwp.com/pricing; warn that paid features degrade if the license lapses. Confirm current packs in `references/platform-guide.md`.

## Troubleshooting

### No styles on the frontend (page looks unstyled live but fine in the editor)
**Symptom**: A published Greenshift page renders with no/partial styling, often on long pages.
**Cause**: Hosting or database field-length limits truncate the styles that Greenshift tries to save, so they're not stored.
**Solution**: Greenshift Settings → CSS management → save styles **inline within blocks**; re-save the affected page; clear page/object/CDN cache. Verify the site URL is HTTPS (Settings → General) and that static files were re-uploaded if you migrated HTTP→HTTPS.

### Animations don't show in the editor (blank space where the block should animate)
**Symptom**: Scroll/GSAP animations render blank inside the Gutenberg editor.
**Cause**: Some scroll/GSAP effects render on the **front end**, not in the editor canvas — this is expected for those effects.
**Solution**: Preview/publish the page and check the live front end. If it's also blank on the front end, look for a JS conflict (deactivate other editor/animation plugins to isolate) and confirm the animation addon's pack is active.

### Editor freezes or the host throws "too many requests"
**Symptom**: The backend hangs when editing/updating, or the host returns rate/request errors while building.
**Cause**: Very long pages, a specific block (e.g. the Button block has been reported to freeze on update), or many editor-side API/asset calls hitting host request limits.
**Solution**: Split very long pages into sections/templates; isolate the offending block by removing it; reduce editor-side API Connector "loop" frequency (4–5s+ intervals); raise or check the host's request limits; keep Greenshift updated.

### A paid block/feature stopped working (fallback styling)
**Symptom**: A page built with GSAP animations, dynamic fields, the API Connector, or WooCommerce blocks lost its styling/behavior.
**Cause**: The relevant Greenshift pack/license is deactivated, expired, or not applied to this site.
**Solution**: Reactivate/renew the correct pack (e.g. GreenLight PRO for the API Connector and dynamic fields; Woo Pack for WooCommerce blocks) and confirm the license covers this site (single-site tiers cover one). Avoid shipping a critical live page solely on paid-only features without a tested staging fallback.
