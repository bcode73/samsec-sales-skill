# Framer Platform Reference

## Overview

Framer is a design-first, AI-assisted website builder — a Figma-like canvas that publishes real sites. It owns the startup-landing-page / portfolio / marketing-site niche: fastest design-to-live workflow, strong Core Web Vitals on published sites, AI design agents, and a growing dev surface (Server API in beta, explicitly aimed at Claude Code/Cursor-driven workflows). The structural trade: **no code export** — everything lives in Framer — and content/SEO depth (CMS caps, no JSON-LD/hreflang) trails Webflow.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Canvas/design + AI agents (Wireframer, Workshop) | Figma-like visual building; AI generates/refines on-canvas | **UI-only** (AI-assisted); Server API can update canvas |
| CMS (Collections) | Typed content collections bound to layouts | **Server API** (beta) + **Plugin API** (Managed Collections for programmatic sync); WordPress REST import |
| Publishing | Instant publish, staging, versions | **Server API** (programmatic publish) |
| Forms | Native forms (Pro-leaning) | UI + integrations |
| A/B testing & analytics | Built-in experiments, CWV monitoring | **UI-only** |
| Localization | Multi-language, per-language priced | **UI-only** config |
| SEO | Meta, sitemaps, redirects; **no JSON-LD authoring, no hreflang; robots.txt Pro-gated** | UI-only |
| Fetch | External API data in components at view time | **Code/components** |
| Plugins & Marketplace | In-editor extensions; templates/components economy | **Plugin API** |
| Commerce | None native — embed Foxy/Snipcart/Lemon Squeezy/Stripe links | Third-party |

No first-party MCP server found; the Server API (WebSocket + `framer-api` npm) is the agent-integration path Framer promotes.

## Pricing, limits & plan gates

*Best-effort (2026-07) — plans changed multiple times recently (Mini/Launch discontinued; May 2026 seat reprice); verify at framer.com/pricing.*

- **Free** — non-commercial, Framer branding.
- **Basic ~$10/mo** (annual) — solo sites; **CMS capped ~100 items**; limited SEO controls.
- **Pro ~$30/mo** — CMS **~1,000 items per collection**, forms, robots.txt editing, A/B testing.
- **Scale from ~$100/mo** — high traffic, bigger limits. **Enterprise** custom.
- **Per-seat and per-language costs stack**: editor seats ~$20/seat/mo (May 2026 reprice; $10 content-editor seats), localization ~$20–40 per language per month — a "small" site with 3 editors and 2 languages can cost more in add-ons than in plan fee.

## Integrations

Marketing stack via embeds and integrations (analytics, chat, forms → ESPs); commerce via third-party checkout embeds (Lemon Squeezy, Foxy, Snipcart, Stripe Payment Links); WordPress import (REST). Partner ecosystem runs on Dub (affiliate links). Data flows: CMS IN via Server/Plugin API sync (Notion, Airtable, custom); site OUT — **only via publishing; no code export**.

## Data model

Site → Pages (canvas) + CMS Collections (typed fields) → items bound to canvas layouts. Programmatic access via Server API (same surface as Plugin API): collections, items, publish, project settings.

```json
// CMS collection item (representative shape via Plugin/Server API)
{ "id": "abc123", "slug": "my-post",
  "fieldData": { "title": "Launch Week", "date": "2026-07-01", "body": "…" } }
```
<!-- Constructed from docs descriptions — the framer-api package types are authoritative -->

## Quick-start recipes

### Recipe 1 — Sync a Notion/Airtable-backed blog into Framer CMS (Server API)

```bash
npm install framer-api
# Create an API key: Framer → Site Settings → API
```

```javascript
import { connect } from "framer-api";

const framer = await connect({ apiKey: process.env.FRAMER_API_KEY });
// 1. find/create the Managed Collection for posts
// 2. upsert items from your source (Notion/Airtable/DB rows → fieldData)
// 3. publish the site when the batch completes
```

Gotchas: the Server API is **open beta** — pin the package version and expect changes; use Managed Collections (plugin/API-owned) so human edits don't fight the sync; the exact call signatures live in the `framer-api` README/GitHub examples.

### Recipe 2 — Drive Framer from Claude Code (agent workflow)

Framer explicitly supports agent-driven workflows (Claude Code, Cursor, Codex):

1. Create a site API key (Site Settings → API), export as `FRAMER_API_KEY`.
2. In your repo, add a small script wrapping `framer-api` (list collections, upsert items, publish).
3. Let the agent call the script — e.g. "add this changelog entry and publish" becomes an upsert + publish call.

Gotchas: keep the API key in env/secrets (it grants site control); batch CMS writes then publish once — publishing per-item is slow and churns versions.

### Recipe 3 — Add checkout to a Framer site (no native commerce)

Framer has no native cart. Options, cheapest-to-richest:
- **Stripe Payment Links / Lemon Squeezy checkout links** on buttons — zero backend, MoR option via Lemon Squeezy.
- **Snipcart or Foxy embeds** — real cart + webhooks; Snipcart needs crawlable product data (mind Framer's rendering), Foxy uses HMAC-signed links that work anywhere.

Gotchas: for Snipcart on Framer confirm product pages render server-side for the crawler; for subscriptions/tax handled for you, prefer a Merchant-of-Record checkout (see `/sales-merchant-of-record`).

## Integration patterns

- **Content-ops pipeline**: source-of-truth in Notion/Airtable/DB → Server API sync into Managed Collections → programmatic publish — content teams never open Framer.
- **SEO ceiling awareness**: no JSON-LD authoring and no hreflang means schema-dependent SERP features and multilingual SEO are structurally limited — if those drive the business, weigh Webflow/WordPress before investing (compare via `/sales-funnel`).
- **Exit strategy (no export)**: keep the CMS mirrored externally (the same sync that feeds Framer can feed a rebuild), keep design tokens/assets in Figma, and treat Framer as the render layer — leaving means rebuilding the front-end, not recovering it.
- **Cost modeling**: plan fee + seats + languages; audit add-on lines before comparing against Webflow (whose CMS/SEO depth may need fewer workarounds).
