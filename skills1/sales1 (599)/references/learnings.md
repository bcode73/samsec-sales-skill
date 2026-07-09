# TexAu Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-28**: Research baseline — platform docs, API surface, pricing, and webhooks captured from live sources on this date (official n8n nodes repo `texauhq/texau-n8n-apis-nodes`, MCP catalog in `texauhq/texau-gtm-skills`, texau.com product/pricing pages). Re-verify specifics against current docs before relying on them.

**2026-06-28**: TexAu has repositioned from a purely PhantomBuster-style "automations + automation hours" tool toward a Clay-style V3 GTM data platform (table interface, waterfall enrichment, AI Column) — but both products coexist, with different billing (automation hours that don't roll over vs pay-on-match credits that roll over up to 2×).

**2026-06-28**: The same team publishes a sister-brand API/MCP under `richapi.ai` (`api.richapi.ai/api/v1`, `mcp.richapi.ai/mcp`) alongside the TexAu-branded `v3-api.texau.com` / `mcp.texau.com/mcp`. The endpoint surface and credit catalog look identical. Treat them as the same API on different hosts; use whichever host issued the user's key.

**2026-06-28**: Homepage (`texau.com`) and `docs.texau.com`/Postman documenter are JS-rendered or bot-block WebFetch — the authoritative, machine-readable endpoint surface is the official n8n community-nodes repo (`credentials/`, `nodes/TexAu/shared/operations.ts`). Prefer that for verbatim endpoint/field detail.

**2026-06-28**: #1 user complaint is LinkedIn account restriction/ban after running automations — inherent to LinkedIn automation, not removable by safety settings. Second is the onboarding/learning curve of chaining recipe steps.
