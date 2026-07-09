<!-- Source: https://quickhunt.app (homepage, /pricing, /integrations) — no public API/developer docs page exists; /docs returns 404. Captured 2026-06-29. -->

# Quickhunt API & Integration Reference

> **Bottom line:** Quickhunt's **REST API is gated to the top Premium plan ($99/mo) and is not documented publicly** — there is no developer portal (the `/docs` path 404s), no OpenAPI spec, and no MCP server. Below Premium the only programmatic surface is **no-code (Zapier / viaSocket / native connectors)** plus **webhooks**. Do not reconstruct or assume endpoint paths, auth schemes, or payloads — confirm them in-account (Premium) or by capturing a live webhook delivery.

## What IS known

### REST API — Premium only, undocumented

- **Availability:** listed as a feature only on the **Premium ($99/mo / $79 annual)** plan, alongside a "dedicated account manager." Not available on Free, Starter, or Growth.
- **Documentation:** none found publicly. No `quickhunt.app/docs`, `/api`, `/developers`, or `developers.quickhunt.app` page rendered at research time.
- **How to get it:** if you're on Premium, request the API reference (base URL, auth method, endpoints, pagination, rate limits) from your dedicated account manager and **verify everything in-account** before building.

### Webhooks

- **Mentioned** as a feature on the integrations page, but **no payload schema and no signing/HMAC scheme are documented**.
- **How to use safely:**
  1. Register your endpoint in-account.
  2. **Capture the first delivery** (log the raw body) to learn the real event names and field shapes.
  3. Secure the endpoint by **secret URL / IP allowlist / payload validation** — do **not** assume HMAC signatures exist.
  4. **Dedupe** on the feedback id and return **200** quickly; retry/backoff behavior is undocumented.

### Integrations (no-code) — Growth tier ($49/mo) and up

Free and Starter have **no integrations**. From Growth:

| Integration | Direction | What it does |
|---|---|---|
| **Slack** | Quickhunt → Slack | Feedback delivered to channels with insights |
| **Zapier** | bidirectional | Bridge to 5,000+ apps — the primary no-code stand-in for the missing low-tier API |
| **viaSocket** | bidirectional | Second iPaaS bridge to "thousands of apps" |
| **ClickUp** | Quickhunt → ClickUp | Feedback → tasks |
| **GitHub** | Quickhunt → GitHub | Feedback → actionable issues |
| **HubSpot** | bidirectional | Connect feedback with HubSpot contacts/insights |
| **Jira** | Quickhunt → Jira | Feedback → issues |
| **Intercom** | *coming soon* | Intercom messages → Quickhunt feedback (not yet live) |

**Zapier/viaSocket note:** exact trigger and action names are not published — confirm them in the live Zap/viaSocket editor. Treat these as the practical automation path for any account below Premium.

### Embeddable widget

- Surfaces the **feedback board, changelog ("what's new"), and knowledge base** in-app.
- Formats: **embed, modal, sidebar, popover, banner**.
- The embed widget is **limited on Free**; a custom-domain hosted portal is **Starter+**.
- Copy the exact embed snippet and any user-identify settings from **Quickhunt → Widget settings** — the snippet and identify mechanism are not publicly documented.

## Auth quick-start

Not possible to document — the API is Premium-gated and unpublished. The closest "auth" you control below Premium is your **webhook receiver** (secure by secret URL) and your **Zapier/viaSocket account** credentials. On Premium, obtain the auth scheme from your account manager.

## Representative shapes

> <!-- Constructed from product UI terminology — NOT from an API spec. Verify against the live API (Premium) or a captured webhook payload. -->

```jsonc
// Likely "new feedback" webhook delivery (shape unconfirmed — capture a live one)
{
  "event": "feedback.created",
  "data": {
    "id": "fb_123",
    "board_id": "board_abc",
    "title": "Add a Kanban view",
    "status": "planned",
    "upvotes": 0,
    "type": "feature_request",
    "author": { "name": "Jane D.", "email": "jane@acme.com" },
    "created_at": "2026-06-29T10:00:00Z"
  }
}
```

## Gaps

The following could **not** be determined from public sources and must be confirmed in-account (Premium) or via a captured webhook:

- REST API base URL, versioning, and full endpoint list (boards, feedback, votes, comments, roadmap, changelog, in-app messages, docs).
- API authentication scheme (API key? Bearer token? OAuth?) and where to generate credentials.
- Pagination model (page/offset vs cursor) and rate limits / 429 behavior.
- Webhook event catalog, exact payload schemas, signing/HMAC scheme, and retry/auto-disable behavior.
- Whether the widget supports an `identify` call to attach feedback to known users (and SSO, if any).
- Exact Zapier / viaSocket trigger and action names.

**If a documented, lower-cost API is a hard requirement,** evaluate alternatives that publish one: **Frill** (`api.frill.co/v1`, signed webhooks, ~$25/mo), **UserJot** (`api.userjot.com/v1`, MCP server, free tier), **Sleekplan** (REST + MCP server), or **FeatureOS** (REST API v3 + OAuth apps).
