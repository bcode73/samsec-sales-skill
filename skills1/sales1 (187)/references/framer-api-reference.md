<!-- Source: https://www.framer.com/updates/server-api + https://www.framer.com/developers/ (reference, cms, fetch-introduction pages), fetched 2026-07-04. Docs are app-rendered; Server API details captured from the official update post — verify at framer.com/developers before building. -->

# Framer API Reference

Framer's developer surface has three parts: the **Server API** (programmatic, from your backend or an AI agent), the **Plugin API** (runs inside the editor), and **Fetch** (dynamic data on published sites). There is no traditional public REST CMS endpoint — the Server API is the programmatic path.

## Server API (open beta)

Verbatim from the official announcement:

> The Server API shares the same capabilities as our Plugin API — sync CMS collections with external sources such as Notion or Airtable, publish changes, update the canvas, and change project settings — triggered by AI agents, webhooks, or scheduled jobs.
> The API leverages a stateful WebSocket channel, making it ideal for batch processing and LLM integrations that need very fast streaming responses, but also interoperable with REST services and Webhooks.

- **Auth**: create an **API key in the site settings**.
- **Client**: `npm install framer-api` — official package; examples on GitHub.
- **Status**: open beta, free during beta; feedback to server-api-feedback@framer.com.
- Explicitly positioned for **Claude Code / Cursor / Codex / terminal workflows** — Framer markets direct AI-agent control of sites.

```javascript
// Shape of a Server API integration (see framer-api docs for exact calls)
import { connect } from "framer-api";

const framer = await connect({ apiKey: process.env.FRAMER_API_KEY });
// Same capability surface as the Plugin API:
// - list/create/update CMS collections + items (Managed Collections)
// - publish the site
// - read/update canvas nodes and project settings
```
<!-- Illustrative shape — the framer-api package README/GitHub examples are the authoritative call signatures -->

## Plugin API (in-editor)

Plugins run inside the Framer editor and "can read and write to the Framer CMS, allowing you to create anything from a Notion Sync plugin, to a custom database integration, or an exporter."

- **Managed vs Unmanaged Collections** (verbatim): "Unmanaged Collections are primarily created and updated by people, whereas Managed Collections are primarily controlled by Plugins." Build sync integrations on Managed Collections so plugin writes own the data.
- Navigation API: "programmatically navigate the UI to a canvas node, a CMS collection item, or a code file… optionally select targets, zoom to canvas layers, or focus a specific field in the item editor."
- Distribution: the Framer Marketplace (plugins/templates/components — 12,000+ community resources).

## Fetch (dynamic data on the published site)

> Fetch is optimized for data that is naturally very dynamic or personalized to the person using the site, rather than information that can be typed onto your site manually or into your CMS.

Use Fetch to pull external API data into components at view time (pricing, availability, personalization) — not as a CMS substitute.

## CMS model

Collections → items with typed fields, connected directly to canvas layouts. Plan caps (best-effort 2026-07): **100 CMS items on Basic; 1,000 items per collection on Pro**; localization is per-language priced. WordPress import via its REST API is supported for migration in.

## What does NOT exist (verify before promising)

- **No code export** — sites can't be downloaded/self-hosted; the design, CMS, interactions all live in Framer.
- **No structured data/JSON-LD authoring** and **no hreflang** support (per 2026 community analysis); robots.txt customization is Pro-gated.
- No published REST CMS endpoint outside the Server API beta; no outbound webhook catalog documented (the Server API *consumes* webhooks/triggers rather than emitting a documented event feed).
- No first-party MCP server found (the Server API's agent orientation fills that role).

## Gaps

- Server API docs are app-rendered; exact method signatures weren't capturable verbatim — the `framer-api` npm README and GitHub examples are the source of truth.
- Rate limits for the Server API: not published (open beta).
- Plan caps and localization pricing shift frequently — re-verify at framer.com/pricing.
