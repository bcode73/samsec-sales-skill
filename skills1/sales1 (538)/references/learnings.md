# Snipcart Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-04**: Research baseline — docs.snipcart.com v3 is JS-rendered; auth + webhook-security sections captured verbatim via rendered fetch, endpoint table assembled from the docs nav (verify shapes before building). Official hosted MCP server (snipcart-mcp.azurewebsites.net, X-Snipcart-Api-Key header, ~38 tools) documented under /v3/mcp-server. Pricing (2% or ~$20/mo minimum) best-effort. product-crawling-failed threads on support.snipcart.com are the richest problem source.
