# Sleekplan Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-28**: Research baseline — platform docs, API surface, webhooks, JWT SSO, MCP server, `$sleek` SDK, and pricing captured from live sources (sleekplan.com/docs/* and /pricing) on this date. Re-verify specifics against current docs before relying on them.

**2026-06-28**: Sleekplan publishes **no separate public REST API spec** — the docs/api page is an orientation guide that lists resources (posts/comments/votes/metadata/users/changelog/surveys/tags/topics) but says the full endpoint reference (paths, params, request bodies, examples) lives **in-app at Settings → Developer** (`app.sleekplan.com/settings/developer`). The `https://api.sleekplan.com/v1/...` paths in the reference files are illustrative — confirm in-app before building.

**2026-06-28**: Webhooks are **NOT HMAC-signed** (unlike Frill/Four/Four). Verification = a **secret GET parameter** appended to the registered endpoint URL (`?key=...`). Payload is `{product_id, action, data, timestamp}`; `data` mirrors the REST response shape; no documented retry behavior.

**2026-06-28**: **Four** distinct auth schemes — JWT SSO (HS256) for widget users, API key (Bearer) for REST, OAuth 2.1 (PKCE + dynamic client registration) for the MCP server, secret GET-param tokens for webhooks + Canvas. Easy to mix up.

**2026-06-28**: **API access, SSO, integrations, and surveys are plan-gated** — the free **Indie** tier has none of them. Paid tiers: Starter $13/mo (3 seats, 1,000 AI credits, CSAT/NPS), Business $38/mo (10 seats, 5,000 AI credits, surveys), Enterprise custom (SAML SSO). AI credits (not seats) are the binding constraint on the AI features.

**2026-06-28**: MCP server `https://mcp.sleekplan.com/mcp` is a genuine differentiator vs Canny/Frill — `claude mcp add sleekplan --transport streamable-http https://mcp.sleekplan.com/mcp`, then `/mcp` to OAuth-authorize. Tools cover feedback (incl. find-similar + merge + tag), comments, changelog, surveys, votes, users, topics, tags, workspace.

**2026-06-28**: Recurring user complaint (AppSumo/Capterra) — multi-product/multi-workspace caps on lower tiers (managing several products needed Enterprise); limited survey depth; some missing UI languages. Founder team noted as responsive. Verify current limits in-account.
