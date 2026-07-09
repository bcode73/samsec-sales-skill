# ClickFunnels Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-21**: Research baseline — platform docs, API surface, pricing, and webhooks captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-21**: Two products — **ClickFunnels 2.0** (current, V2 REST API at `developers.myclickfunnels.com`) and **Classic 1.0** (legacy, V1 API at `apidocs.clickfunnels.com` — DEPRECATED). Always confirm which one the user is on before answering an API question.

**2026-06-21**: The dev hub is JS-rendered but publishes an OpenAPI schema at `developers.myclickfunnels.com/openapi/clickfunnels-api.json` and an LLM index at `/llms.txt` — use those for the full endpoint list and exact schemas instead of scraping the rendered pages. The full endpoint inventory was captured from llms.txt.

**2026-06-21**: V2 API quirks — TWO base URLs: `accounts.myclickfunnels.com/api/v2` (team/workspace lookups) and `{workspace}.myclickfunnels.com/api/v2` (workspace data). A `User-Agent` header is REQUIRED alongside `Authorization: Bearer`. Tokens are generated per-team (Developer Portal) and access all workspaces. Payloads use the internal `id`, NOT the `public_id` shown in URLs (common 422 cause). Bootstrap: GET /teams → GET /teams/:id/workspaces → workspace data. Pagination is cursor + offset; `expand[]` inlines nested resources. Webhooks are signed — verify the signature.

**2026-06-21**: API access is plan-gated to the higher tier (Pro ~$297; some plan generations name it Scale/Optimize/Dominate). Entry plan (Startup ~$97) can't call the API. ClickFunnels has repriced/renamed plans repeatedly — treat plan names/prices as best-effort and verify live.

**2026-06-21**: Top user pain points from reviews — 2.0 stability (page previews that won't load, under-tested features), among the highest-priced funnel builders, per-send email pricing that escalates with list size (run the math before importing a big list), no bulk contact import (long-standing gap), Classic→2.0 migration risk, and email deliverability complaints.

**2026-06-21**: Affiliate — 30% lifetime recurring commission, plus the famous Dream Car contest (100 active customers → $500/mo toward a car lease, 200 → $1,000/mo). "Backpack" is ClickFunnels' built-in affiliate-management feature for your OWN products (UI-only, no public affiliate API). Logged in `_internal/affiliates.md`.
