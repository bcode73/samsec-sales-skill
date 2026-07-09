# UserJot Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs (userjot.com/docs), the API reference (userjot.com/docs/api), pricing (userjot.com/pricing), and the dev.to build-in-public writeup captured on this date. Re-verify specifics against current docs before relying on them.

**2026-06-29**: The live site bot-blocks WebFetch (HTTP 403 on userjot.com pages); the API reference page is JS-rendered and lazy-loads sections beyond Boards (sub-paths like /docs/api/requests 404 in the migrated docs app). Boards CRUD, base URL (`https://api.userjot.com/v1`), Bearer auth, the status-code map, and the `Idempotency-Key`-on-`/requests`-and-`/changelogs` note were captured verbatim via a reader proxy; the rest must be confirmed in the live docs / in-account. No OpenAPI spec or Postman collection found.

**2026-06-29**: The feedback-post resource is **`/requests`** (the UI calls them "posts"). `409` is overloaded (duplicate name OR quota/plan-cap). API/webhooks/MCP appear to count under the "integrations" cap (Free = none, Starter = 1, Professional = unlimited) — verify in-account which surfaces the cap actually gates before building against a free workspace.
