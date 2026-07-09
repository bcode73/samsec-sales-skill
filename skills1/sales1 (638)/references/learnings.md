# Userback Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, REST API (`rest.userback.io/1.0`, Bearer), webhooks, MCP server (`mcp.userback.io/v1/mcp/`), JS/React/Vue/Next/mobile SDKs, and pricing captured from live sources (docs.userback.io, support.userback.io, userback.io/pricing) on this date. Re-verify specifics against current docs before relying on them.
**2026-06-29**: The REST API and webhooks are gated to **Business Plus** (top tier); Zapier is Team+, session replay + JS SDK methods are Business+. Any API-based integration plan must budget for Business Plus from the start — a Free/Team/Business prototype that depends on the API will not work.
**2026-06-29**: Webhooks have **no documented HMAC signature**. Identify them via `User-Agent: Userback-Webhook`, keep the endpoint URL secret, and re-fetch the entity via `GET /feedback/{id}` rather than trusting the (thin) payload body.
**2026-06-29**: List endpoints cap `limit` at **50 records/page**; exact rate limits are unpublished — handle `429` with exponential backoff. Free-plan feedback is purged after **7 days**.
