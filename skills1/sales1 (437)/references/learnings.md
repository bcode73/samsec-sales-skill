# Productlane Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform modules, pricing, API surface, and integrations captured from live sources (productlane.com homepage/feedback page, productlane.com/docs, the ReadMe-hosted API reference at productlane.readme.io, Zapier, and G2/third-party listings) on this date. Re-verify specifics against current docs before relying on them.

**2026-06-29**: **Hard Linear dependency is the defining trait.** Productlane is "built exclusively on Linear" — feedback links to Linear issues, the roadmap mirrors Linear projects, and the changelog (Release Intelligence) auto-drafts from completed Linear issues. There is no standalone mode. Always lead a fit question with "do you use Linear?" — if not, route to a standalone board (`/sales-frill`, `/sales-userjot`, `/sales-featureos`, `/sales-quickhunt`).

**2026-06-29**: **Real, documented REST API** at `https://productlane.com/api/v1`, `Authorization: Bearer API_KEY` (key from `productlane.com/settings/api`). Resources: Companies (list/get/create/delete), Customers (get/create/update/delete; `name` 1–255, `email` req, `segments[]`), Insights (get/list/create/update; `text`+`painLevel`+`customerEmail` req), Portal (`getprojects`, `getprojectupvotes`, `listchangelogs`, `createfeedback`, `upvoteproject`), Workspaces (get). This makes it the opposite of Rapidr/Quickhunt (no/locked API).

**2026-06-29**: **`POST /api/v1/feedback` is PUBLIC (no auth)** — it takes `workspaceId`+`text`+`painLevel`+`email` for widget/portal capture, so a leaked `workspaceId` invites spam; front it with CAPTCHA/rate limit/origin check. By contrast `POST /api/v1/insights` (structured prioritized feedback) **requires** the Bearer key. `painLevel` enum on both: `UNKNOWN|LOW|MEDIUM|HIGH`.

**2026-06-29**: **No MCP server** (unlike UserJot/Sleekplan/Four-Four). Agent integrations go through the REST API or Zapier's "Create Note" action (which maps to Insights). Productlane's **own** outbound webhooks are **not documented publicly** — Linear's webhooks are separate; prefer Linear webhooks or polling for events.

**2026-06-29**: **Pricing is per-user, no free tier** (7-day trial only). Best-effort: Starter ~$15/user (annual) / ~$19 monthly (portal + roadmap + changelog + widget); Pro ~$29/$39 (adds support inbox + AI changelog gen); Scale ~$79/$99 (SSO/JWT, custom domains, white-label, private portals, HubSpot + Zapier). Reviewers flag the entry price as high for small teams and noted portal Google-auth was gated on the low tier (SSO is Scale). Startup discounts offered.

**2026-06-29**: GitHub org exists at github.com/productlane (verified org, 0 public repos, email hello@productlane.com, Germany). Closest competitor is **Cycle** (also Linear-native) — added to backlog alongside **Quackback**. Productlane evolved from a pure feedback/roadmap/changelog tool into an AI-native support suite, but the feedback portal/roadmap/changelog remain core, so it belongs under `/sales-customer-feedback`.
