---
name: sales-sleekplan
description: "Sleekplan (sleekplan.com) platform help — AI customer-feedback suite (Canny/Frill/Featurebase alternative): feedback boards with voting/comments + AI auto-categorization and duplicate merging, roadmap, changelog, NPS/CSAT surveys, plus an MCP server for Claude/Cursor. Developer surface: REST API (Bearer key from Settings → Developer) for posts/comments/votes/users/changelog/surveys/tags/topics, dashboard-configured webhooks (secret GET-param verification, NOT HMAC-signed), JWT SSO (HS256), and the $sleek widget SDK. Use when reading or syncing feedback posts and votes via the API, wiring the Sleekplan MCP server into Claude Code, verifying an incoming webhook, embedding the widget or identifying users with SSO, mapping statuses to a public roadmap, or choosing a plan (free Indie vs Starter vs Business). Do NOT use for voice-of-customer / NPS survey program strategy across tools (use /sales-customer-feedback) or aggregating unsolicited feedback across reviews/social (use /sales-noisely)."
argument-hint: "[describe what you need help with in Sleekplan]"
license: MIT
version: 1.0.0
tags: [sales, customer-feedback, product, platform]
github: "https://github.com/Sleekplan"
---

# Sleekplan Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Read/sync feedback posts, votes, comments via the REST API (Bearer key)
   - B) Verify an incoming webhook (secret GET-param — NOT HMAC) and react to item/vote/comment events
   - C) Wire the Sleekplan **MCP server** into Claude Code / Cursor (OAuth 2.1)
   - D) Embed the widget / identify logged-in users (JWT SSO) via the `$sleek` SDK
   - E) Map statuses to a public roadmap, publish a changelog, or run NPS/CSAT surveys
   - F) Decide Sleekplan vs Canny/Frill/Featurebase, or pick a plan (Indie/Starter/Business)

2. **API or no-code?** Code → REST API + webhooks + MCP. Front-end → `$sleek` widget SDK + JWT SSO. AI-client → MCP server.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Voice-of-customer / NPS/CSAT survey **program** strategy across tools | `/sales-customer-feedback {question}` |
| Aggregating **unsolicited** feedback across reviews/social/support | `/sales-noisely {question}` |
| Public review **generation** strategy (Trustpilot/G2) | `/sales-customer-reviews {question}` |
| Connecting Sleekplan to a CRM/PM tool generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-customer-feedback build a closed-loop feedback program`".

## Step 3 — Sleekplan platform reference

**Read `references/platform-guide.md`** for the full reference — the Boards/Roadmap/Changelog/Surveys module map (what's API vs widget vs MCP vs UI), the AI layer (Sleek Intelligence / Sleekmate, AI credits), plan tiers, the data model, and quick-start recipes (pull posts via the API; verify a webhook; configure the MCP server; embed + SSO-identify a user).

**Read `references/sleekplan-api-reference.md`** for the integration surface — **Bearer** API-key auth (key from `app.sleekplan.com/settings/developer`), the resources (posts/comments/votes/metadata/users/changelog/surveys/tags/topics), the **four auth mechanisms** (JWT SSO for users, API keys for REST, OAuth 2.1 for MCP, secret tokens for webhooks/Canvas), the **webhook** event list + `{product_id, action, data, timestamp}` payload, the **MCP server** (`https://mcp.sleekplan.com/mcp`), and the **JWT SSO** (HS256) payload fields.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Bearer auth.** `Authorization: Bearer <key>` with the key from **Settings → Developer** (`app.sleekplan.com/settings/developer`). Keep it server-side. The full endpoint reference (exact paths, bodies, params) lives **in-app** at that same screen — Sleekplan doesn't publish a separate public spec, so confirm request bodies there.
- **Webhooks are NOT HMAC-signed.** Unlike Frill, Sleekplan verifies delivery via a **secret GET parameter** you append to the endpoint URL (`?key=MY_SECRET_KEY`). Check that param server-side; the payload is `{product_id, action, data, timestamp}` and `data` matches the REST response shape. Dedupe on the entity id + `timestamp`.
- **The MCP server is a first-class interface.** `https://mcp.sleekplan.com/mcp` over **OAuth 2.1 (PKCE, dynamic client registration)** — add it with `claude mcp add sleekplan --transport streamable-http https://mcp.sleekplan.com/mcp`, then `/mcp` to authorize. Exposes feedback/comments/changelog/surveys/votes/users/topics/tags tools.
- **Identify users with JWT SSO.** Sign an **HS256** token (SSO secret from Settings → Developer, **server-side only**) with payload `mail` (required) + optional `id`/`name`/`img`/`weight`/`meta`, pass it via `$sleek.sso`/`setUser` or `?sso=` — otherwise widget feedback is anonymous.
- **It's a feedback-board tool, not a VoC survey suite.** Sleekplan collects *solicited* board feedback + roadmap + changelog (with built-in NPS/CSAT). For survey *program* strategy use `/sales-customer-feedback`; for mining *unsolicited* feedback across reviews/social use `/sales-noisely`.
- **API/SSO/integrations are plan-gated.** The free **Indie** tier has no API access, team seats, surveys, or integrations; those start on **Starter** ($13/mo) and **Business** ($38/mo). Size the plan to seats + AI credits.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — webhooks/SSO/MCP/SDK verbatim from sleekplan.com/docs; pricing from sleekplan.com/pricing. Confirm in-account; the full REST endpoint reference is in-app at Settings → Developer.*

1. **Webhooks are NOT HMAC-signed** — verification is a **secret GET param** (`?key=...`), not a signature header. Don't write HMAC verification code; check the secret param and treat the endpoint URL itself as the secret (keep it private, prefer IP allowlisting too).
2. **No published REST spec.** The orientation docs list the resources, but exact paths/bodies/params live **in-app** (Settings → Developer). Confirm request bodies there before building; don't invent endpoints.
3. **Four different auth schemes.** JWT SSO (users) ≠ API key (REST) ≠ OAuth 2.1 (MCP) ≠ secret token (webhooks/Canvas). Use the right one for the surface — e.g. don't try to hit the REST API with an SSO token.
4. **API access is plan-gated.** The free Indie tier has no API/SSO/integrations/surveys; those require Starter+ — an integration built against a free workspace will 401/403.
5. **AI runs on monthly credits.** Starter ~1,000 / Business ~5,000 AI credits/mo power auto-categorization, duplicate merging, and Sleekmate; heavy AI use can exhaust them.
6. **Multi-product/workspace caps.** One workspace per low tier — managing several products historically needed Enterprise (a recurring user complaint). Verify current limits before consolidating.

## Related skills

- `/sales-customer-feedback` — Voice-of-customer / survey program strategy across tools (Sleekplan is a feedback-board option) — program design, tool selection. Install: `npx skills add sales-skills/sales --skill sales-customer-feedback -a claude-code`
- `/sales-frill` — Frill platform help — the closest like-for-like affordable feedback-board competitor; differs on webhooks (Frill is **HMAC-SHA256 signed** + cursor pagination vs Sleekplan's secret-GET-param + Bearer). Install: `npx skills add sales-skills/sales --skill sales-frill -a claude-code`
- `/sales-featureos` — FeatureOS (formerly Hellonext) feedback boards + roadmap + changelog + knowledge base; REST API v3 (`API-KEY` header), OAuth 2.0 apps, auto-disabling webhooks. Install: `npx skills add sales-skills/sales --skill sales-featureos -a claude-code`
- `/sales-userjot` — UserJot platform help — the closest AI-first feedback board that *also* ships an **MCP server** (Canny/Productboard alternative, no per-seat pricing); compare on webhooks (UserJot's signing scheme is unpublished — capture live), the `/requests` post resource + `Idempotency-Key`, and free-tier integration gating. Install: `npx skills add sales-skills/sales --skill sales-userjot -a claude-code`
- `/sales-noisely` — AI aggregation of **unsolicited** feedback across reviews/social/support (complement: Sleekplan = solicited boards, Noisely = unsolicited mining). Install: `npx skills add sales-skills/sales --skill sales-noisely -a claude-code`
- `/sales-integration` — Connecting Sleekplan to a CRM/PM tool via API/webhooks. Install: `npx skills add sales-skills/sales --skill sales-integration -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Pull feedback posts + votes into my system via the API (developer/automation)
**User says**: "How do I sync all the feedback posts and their vote counts out of Sleekplan?"
**Skill does**: Shows authenticating with **`Authorization: Bearer <key>`** (key from Settings → Developer), listing **posts** (the feedback resource — "Returns a list of feedback posts. Sorted by trend by default"), and reading each post's status/votes (with the comments + votes resources for detail). Notes that the exact endpoint paths/params live in the in-app reference, that the key stays server-side, and that **webhooks** (item/vote events) beat polling for ongoing sync.
**Result**: A complete export of posts + engagement, with the right auth and the in-app-spec caveat.

### Example 2: Wire the Sleekplan MCP server into Claude Code (developer/automation)
**User says**: "Can I use Sleekplan from Claude so it can read and triage our feedback?"
**Skill does**: Gives the exact command — `claude mcp add sleekplan --transport streamable-http https://mcp.sleekplan.com/mcp` — then `/mcp` to authorize via **OAuth 2.1 (PKCE, dynamic client registration)**, which opens a browser to sign in and pick a workspace. Lists the tools it exposes (feedback list/create/merge/find-similar/stats, comments, changelog, surveys, votes, users, topics, tags) and notes only access tokens reach the client.
**Result**: A connected MCP server Claude can use to list, tag, and merge feedback.

### Example 3: Sleekplan vs Frill vs Canny — which feedback tool?
**User says**: "We're a small SaaS — Sleekplan, Frill, or Canny for a feedback board + roadmap?"
**Skill does**: Frames the tradeoff — **Sleekplan** is the AI-forward affordable pick (free Indie tier, $13 Starter / $38 Business, AI auto-categorization + duplicate merging, **MCP server**), **Frill** is similarly cheap with **HMAC-signed** webhooks + cursor pagination, and **Canny** is pricier/enterprise. Flags the webhook-verification difference (secret GET param vs HMAC) for integration builders, and routes broader selection: "run: `/sales-customer-feedback choose a product-feedback board tool`."
**Result**: A price- and integration-grounded board-tool choice.

## Troubleshooting

### My webhook receiver can't verify the request is really from Sleekplan
**Symptom**: You're looking for a signature header to validate and there isn't one.
**Cause**: Sleekplan **does not HMAC-sign** webhook payloads (unlike Frill/Four/Four).
**Solution**: Append a **secret GET parameter** to the endpoint you register (`https://you.app/webhooks?key=MY_SECRET_KEY`) and check that `key` server-side, rejecting anything without it. Keep the URL private and ideally IP-allowlist Sleekplan. Payload is `{product_id, action, data, timestamp}`; dedupe on the entity id + `timestamp`.

### I can't find the exact API endpoint/path I need in the public docs
**Symptom**: The docs describe resources (posts, comments, votes…) but not full paths/request bodies.
**Cause**: Sleekplan doesn't publish a separate public API spec — the authoritative reference is **in-app**.
**Solution**: Open **Settings → Developer** (`app.sleekplan.com/settings/developer`) for the interactive endpoint reference (parameters, request bodies, examples) and your API key. Don't reconstruct endpoints from memory; confirm bodies there.

### My API calls return 401/403 on the free plan
**Symptom**: Auth fails even with a key, or you can't generate a key at all.
**Cause**: **API access (and SSO/integrations/surveys) is plan-gated** — the free **Indie** tier doesn't include them.
**Solution**: Upgrade to **Starter** ($13/mo) or **Business** ($38/mo) to unlock the API/SSO/integrations, then re-issue the key from Settings → Developer. For survey-program strategy beyond boards, use `/sales-customer-feedback`.
