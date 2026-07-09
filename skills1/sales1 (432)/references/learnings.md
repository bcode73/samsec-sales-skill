# Printful Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, API surface (v2 beta + v1), pricing, and webhooks captured from live sources on this date. Re-verify specifics against current docs before relying on them. Key facts: base `https://api.printful.com/v2/`; OAuth 2.0 / Bearer token auth; leaky-bucket rate limit 120 req/60s with `retry-after` on 429; 19 webhook event types; v2 webhooks are HTTPS-only + signed + expiring; order cost is async (`calculating`) and orders can't be confirmed until it completes; always order by `catalog_variant_id`, not product id. Pricing: Free $0, Growth $24.99/mo (free above $12K/yr sales), Enterprise custom; add-ons (labels/premium image/embroidery digitization) cost per item. GitHub org `github.com/printful` (PHP SDK); community MCP server `Purple-Horizons/printful-mcp` (17 tools).
