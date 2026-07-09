---
name: sales-framer
description: "Framer platform help — design-first AI website builder for marketing sites, landing pages, and portfolios (Figma-like canvas, AI design agents, CMS Collections, A/B testing, localization) with a developer surface: the Server API (framer-api npm package, API key from site settings, stateful WebSocket + REST/webhook interop — sync CMS from Notion/Airtable, publish programmatically, drive from Claude Code/Cursor), a Plugin API, and Fetch for dynamic data. Use when automating Framer CMS updates or publishing from a server or AI agent, hitting CMS item caps (100 on Basic, 1,000 per collection on Pro), structured data/JSON-LD or hreflang isn't supported and rankings suffer, weighing the no-code-export lock-in before committing, per-language localization and per-seat editor costs balloon the bill, or adding checkout to a Framer site via embeds. Do NOT use for landing-page strategy or builder selection (use /sales-funnel) or checkout platform choice (use /sales-checkout)."
argument-hint: "[describe what you need help with in Framer]"
license: MIT
version: 1.0.0
tags: [sales, funnels, website-builder, platform]
github: "https://github.com/framer"
---

# Framer Platform Help

Framer is a design-first, AI-assisted website builder — a Figma-like canvas that publishes production marketing sites, with AI design agents and a beta **Server API** built for agent-driven workflows (Claude Code/Cursor). Its structural trades: **no code export** (full platform lock-in) and content/SEO depth behind Webflow (CMS caps, no JSON-LD/hreflang).

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer from the user's prompt:

1. **What are you trying to do?**
   - A) Build/ship a site (landing page, portfolio, marketing site)
   - B) Automate the CMS or publishing (Server API, Notion/Airtable sync, AI-agent workflows)
   - C) Fix SEO/content limits (structured data, hreflang, CMS caps)
   - D) Understand pricing (plans + seat + per-language add-ons) or the lock-in trade
   - E) Add commerce/checkout to a Framer site

2. **Which plan?** CMS caps, robots.txt editing, and A/B testing are plan-gated — most limit questions are plan questions.

Skip-ahead rule: if the user's prompt already has enough context, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| Which site/landing-page builder to pick (Framer vs Webflow/WordPress builders/Unbounce) | `/sales-funnel {question}` |
| Landing-page conversion strategy across tools | `/sales-funnel {question}` |
| Which checkout to embed (Snipcart vs Foxy vs Lemon Squeezy vs Stripe links) | `/sales-checkout {question}` |
| Tax-handled checkout (Merchant of Record) | `/sales-merchant-of-record {question}` |
| SEO strategy beyond Framer's controls | `/sales-seo {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-funnel {original question}`"

Otherwise, answer Framer-specific questions directly using Step 3.

## Step 3 — Framer platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface, pricing/plan gates, data model, and quick-start recipes (Server API CMS sync, Claude Code agent workflow, adding checkout).

For the Server API / Plugin API / Fetch details and the documented platform limits, read `references/framer-api-reference.md`.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **For automation, reach for the Server API** (`framer-api` npm, API key from Site Settings, WebSocket-based, same surface as the Plugin API) — sync CMS from Notion/Airtable/DB, publish programmatically, drive from Claude Code/Cursor. Flag that it's **open beta**: pin versions, expect changes, and treat the package README as the authoritative signatures.
- **Use Managed Collections for programmatic sync** so plugin/API writes own the data and human edits don't fight the pipeline; batch writes, then publish once.
- **State the SEO ceiling plainly when relevant**: no structured-data/JSON-LD authoring, no hreflang, robots.txt Pro-gated — schema-dependent SERP features and multilingual SEO are structurally limited; route platform reconsideration to `/sales-funnel`.
- **Surface the lock-in before the user commits**: there is **no code export** — leaving Framer means rebuilding, not migrating. Advise mirroring CMS content externally (the same sync that feeds Framer can feed a rebuild) and keeping design sources in Figma.
- **Model the full cost, not the plan fee**: seats (~$20/editor/mo) and localization (~$20–40 per language/mo) stack on top of plans (Basic ~$10 / Pro ~$30 / Scale ~$100+); present all pricing as best-effort and point to framer.com/pricing — plans changed repeatedly in 2026.
- **For commerce, recommend embeds by need**: Stripe/Lemon Squeezy payment links for simple sales (MoR via Lemon Squeezy), Snipcart/Foxy for a real cart — compare via `/sales-checkout`.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — review these, especially plan pricing/caps (changed multiple times in 2026) and the Server API's beta status.*

- **No code export, period.** The site — design, CMS, interactions — exists only inside Framer. Performance tuning beyond Framer's defaults and self-hosting are impossible; the exit is a rebuild.
- **CMS caps bite content sites**: ~100 items on Basic, ~1,000 per collection on Pro — a growing blog or programmatic-SEO play hits the wall; check caps before migrating content in.
- **SEO gaps are structural**: no JSON-LD/structured-data authoring, no hreflang for multilingual, robots.txt editing Pro-gated. Great CWV doesn't compensate for missing schema when rich results matter.
- **Add-ons dominate real cost**: per-seat editors and per-language localization often exceed the plan fee; the discontinued cheap tiers (Mini/Launch) no longer anchor pricing.
- **Server API is beta**: free during beta, subject to change — don't build unversioned production dependencies on it.
- **No native commerce** — checkout is always a third-party embed; subscriptions/tax need the embedded provider, not Framer.

## Related skills

- `/sales-funnel` — Landing-page/site-builder selection and conversion strategy (Framer vs Webflow vs WordPress builders)
- `/sales-checkout` — Adding checkout to a Framer site (Snipcart vs Foxy vs payment links)
- `/sales-snipcart` — Snipcart platform help (JS cart embed; mind crawler validation on Framer rendering)
- `/sales-foxy` — Foxy platform help (HMAC-signed links work on any Framer page)
- `/sales-merchant-of-record` — Tax-handled checkout options for Framer sites
- `/sales-seo` — SEO strategy when Framer's built-in controls run out
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Agent-driven content pipeline (developer/automation)
**User says**: "I want Claude Code to add changelog entries to our Framer site and publish automatically."
**Skill does**: Sets up the Server API — API key from Site Settings, `npm install framer-api`, a small script exposing upsert-item + publish that the agent calls — using a Managed Collection so the sync owns the data, batching writes before a single publish, and flagging the beta status (pin the package, watch for signature changes).
**Result**: "Add this changelog entry and publish" becomes one agent command.

### Example 2: Rankings stuck despite a fast site
**User says**: "Our Framer site scores great on Core Web Vitals but we can't get rich results and our German pages compete with the English ones."
**Skill does**: Explains the structural gaps — no JSON-LD authoring (so no schema-driven rich results) and no hreflang (so multilingual pages can't declare language targeting) — offers the available mitigations (meta hygiene, Pro robots.txt), and frames the honest decision: if schema/multilingual SEO drive revenue, evaluate Webflow/WordPress via `/sales-funnel`.
**Result**: User stops debugging CWV and makes an informed platform-level call.

### Example 3: The lock-in question before committing
**User says**: "We're moving our startup site to Framer — anything we should set up now to avoid regret later?"
**Skill does**: Surfaces the no-export lock-in and prescribes the exit-ready setup: keep CMS content mirrored in an external source (Notion/Airtable/DB) synced via the Server API, keep design sources in Figma, document embeds — and models true monthly cost (plan + seats + languages) as best-effort against framer.com/pricing.
**Result**: The team adopts Framer with an exit strategy and a real cost picture instead of discovering both later.

## Troubleshooting

### CMS import stops partway / items missing
**Symptom**: Content migration halts or new items won't save.
**Cause**: Plan CMS caps — ~100 items on Basic, ~1,000 per collection on Pro.
**Solution**: Check current caps against your content count before migrating; upgrade, split collections, or reconsider the platform for large content sites. Keep the source-of-truth external either way.

### Server API script broke after working fine
**Symptom**: A previously working `framer-api` integration errors after an update.
**Cause**: The Server API is open beta — signatures and behavior change.
**Solution**: Pin the `framer-api` package version, read the GitHub examples/changelog before upgrading, and wrap calls so failures alert rather than silently skip publishes.

### Costs way above the advertised plan price
**Symptom**: The bill is a multiple of the $10–30 plan fee.
**Cause**: Per-seat editor charges (~$20/seat/mo) and per-language localization (~$20–40/language/mo) stack on the plan; 2026 plan restructures removed cheaper tiers.
**Solution**: Audit seats (downgrade content-only users to $10 content-editor seats), trim unused languages, and re-verify current pricing at framer.com/pricing before renewing annually.
