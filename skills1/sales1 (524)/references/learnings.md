# Shopify Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-27**: Research baseline — platform docs, API surface (GraphQL Admin API base `https://{shop}.myshopify.com/admin/api/{version}/graphql.json`, version `2026-04`; REST legacy as of 2024-10-01; new public apps GraphQL-only since 2025-04-01), GraphQL calculated-query-cost rate limiting (100/200/1000/2000 pts/sec by plan, 1000-pt max query, `extensions.cost.throttleStatus`), REST leaky bucket (40 burst / 2 per sec), webhooks (HMAC-SHA256 on raw body via `X-Shopify-Hmac-Sha256`, mandatory GDPR topics, no guaranteed ordering/delivery, Pub/Sub + EventBridge delivery), bulk operations for large reads, and pricing/plan gates (Basic/Grow/Advanced/Plus; third-party gateway fees; Checkout Extensibility Plus-tier) captured from live sources on this date. Pricing returned in EUR (geo-detected) — re-verify local currency and current fees before relying on them.
