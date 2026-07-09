# Chargebee Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, API surface (v2, HTTP Basic key-as-username, form-encoded, offset pagination, idempotency header), webhook model (NO HMAC — basic-auth/secret-URL/IP-allowlist + dedupe on event id + order by resource_version), pricing (free Starter cumulative $250K cap → 0.75% overage; Performance ~$7,188/yr caps at $100K/mo; RevRec/Retention as separately-priced add-ons), Product Catalog 1.0 vs 2.0 split, and AgentKit MCP server (`@chargebee/mcp`) captured from live sources on this date. Re-verify specifics (especially pricing, IP ranges, and PC1↔PC2 endpoint differences) against current docs before relying on them.
