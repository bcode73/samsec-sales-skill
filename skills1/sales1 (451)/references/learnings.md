# Quickhunt Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform modules, pricing, and integration surface captured from live sources (quickhunt.app homepage, /pricing, /integrations) on this date. Re-verify specifics against current docs before relying on them.

**2026-06-29**: No public API/developer docs exist — `quickhunt.app/docs` returns HTTP 404, and no `/api`, `/developers`, or `developers.quickhunt.app` page rendered. The REST API is listed only on the **Premium ($99/mo)** plan with a "dedicated account manager." Treat the API as unavailable and undocumented below Premium; do not reconstruct endpoints/auth.

**2026-06-29**: **Integrations are gated to Growth ($49/mo)** — Free and Starter have **no integrations at all** (Slack/Zapier/ClickUp/GitHub/HubSpot/Jira/viaSocket). Quickhunt advertises "all integrations included in every [paid integration] plan, unlike Canny's one-integration limit." Intercom was marked "coming soon."

**2026-06-29**: Webhooks are mentioned as a feature but **no payload schema or HMAC/signing scheme is documented** — capture a live delivery to learn the shape and secure the endpoint by secret URL/IP allowlist.

**2026-06-29**: Distinct positioning vs the other feedback-board skills — Quickhunt's hooks are (1) a **genuinely free lifetime tier** (FeedBear/Rapidr have none; cheaper to start than Frill) and (2) the **broadest all-in-one bundle**: boards + roadmap + changelog + in-app messages (surveys/checklists/banners) + knowledge base + AI assistant + live chat. Trade-off is the most API-restrictive of the affordable boards (API at $99 only). GitHub org exists at github.com/QuickHUnt (login "QuickHUnt", 0 public repos).
