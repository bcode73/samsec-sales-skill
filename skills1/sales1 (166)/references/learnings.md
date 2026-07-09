# EverShop Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, REST + GraphQL API surface, JWT auth, the in-process event/subscriber system (no outbound webhooks), install flow, and infra requirements captured from live sources (evershop.io/docs, github.com/evershopcommerce/evershop) on this date. Latest release observed: v2.1.2 (April 2026). Re-verify specifics (Node/Postgres versions, token-expiry defaults, event list, whether managed cloud has launched) against current docs before relying on them.
