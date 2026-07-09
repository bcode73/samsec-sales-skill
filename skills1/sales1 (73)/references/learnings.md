# Builderall — Learnings

Accumulated platform knowledge. Append new findings with the date discovered.

**2026-06-22**: Research baseline. Builderall is a budget all-in-one suite (builderall.com, founded 2011 by Erick Salgado, 100k+ users) — website + 3 funnel builders, MailingBoss email, SuperCheckout, CRM, courses/membership, webinars, chatbot, booking, heatmaps, A/B testing. Positioned vs ClickFunnels/Kartra/Kajabi/Systeme.io.

- ⚠️ Live homepage and `/pricing` exceeded the WebFetch size limit; help-center API pages (ajuda.builderall.com) returned 404. Research assembled from API-tracker, integration listings (Pabbly/Integrately/Pipedream), and review sites (G2/Capterra/Trustpilot). Re-verify pricing and exact endpoint paths on the live site before relying on them.
- **API surface = MailingBoss only.** Base `https://member.mailingboss.com/integration/index.php/`, token is the last URL path segment, params in body. Verified subscriber endpoints: `lists/subscribers/create|search-by-email|update|unsubscribe/<TOKEN>`. List/campaign endpoints are documented to exist but exact paths weren't captured verbatim — confirm in-account.
- MailingBoss is built on a **MailWizz**-style codebase (explains uppercase field tags `EMAIL`/`FNAME`, `subscriber_uid`/`list_uid`, per-list subscriber scoping).
- No public MCP server. No broad REST API across funnels/checkout/courses. Integrate via MailingBoss API + per-list inbound webhooks + Zapier/Make/Pabbly/Integrately (MailingBoss is typically an iPaaS *action* target).
- **Plan gate to flag:** the funnel builder has historically required a higher tier (~$79.90/mo), not the free/entry (~$14.90–17/mo) plan. "Cheap" is true for entry, misleading for funnels.
- **Top review pain points:** periodic outages (site/SuperCheckout/email sends); slow support (multi-day, no phone); MailingBoss deliverability weaker than dedicated ESPs; dated templates; steep learning curve (1–2 weeks); reports of affiliate revenue being cut.
- **Affiliate program:** Builderall runs a well-known affiliate program (2-tier historically) — relevant for `_internal/affiliates.md` if tracking.
- Adjacent platform surfaced and added to backlog: **MemberVault** (membership/course platform, appeared in Builderall-vs comparison roundups).
