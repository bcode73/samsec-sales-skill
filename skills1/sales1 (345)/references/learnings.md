# Memberstack — Learnings

Accumulated platform knowledge. Append new findings with the date discovered.

**2026-06-22**: Research baseline. Memberstack (memberstack.com) is a no-code **membership + authentication + Stripe-payments layer** for sites you build yourself — Webflow primary, also WordPress and any script-capable site (custom HTML, React, AI-built). Paste a script + data attributes to add login, paid memberships, and content gating. It's the auth/paywall plumbing, NOT a course/LMS host and NOT an email tool. Target: no-code builders, solo creators, makers, developers. Memberstack 2.0 is the current rebuild (1.0 is legacy with a different API).

- **Two developer surfaces:** (1) **DOM package** — front-end JS, **public key**, runs in the browser for login/signup/gating/Stripe checkout; (2) **Admin package** — server-side, a **REST API** and a **Node.js** library, **secret key**.
- **Admin REST:** base `https://admin.memberstack.com`; auth `X-API-KEY` (test `sk_sb_` capped at 50 test members; live `sk_live_`/`sk_`); **server-side only**. Member CRUD at `/members` (GET list, GET `/:id_or_email`, POST, PATCH, DELETE); `POST /members/verify-token` (JWT verify); `POST /members/:id/add-plan` & `/remove-plan` (free plans only, `pln_*`). Paid plans go through Stripe checkout via the DOM package.
- **Rate limit 25 req/s → 429.** Cursor pagination: `after` + `first`/`limit` (max 100), response has `endCursor`/`hasNextPage`/`totalCount`.
- **Footguns:** (1) `PATCH` **fully replaces `json`** while `customFields`/`metaData` shallow-merge — read-modify-write `json`. (2) Non-existent member returns **200 + `data:null`**, not 404. (3) **Webhook signature verification is NOT supported via REST** — only the Node Admin package; on REST-only, re-fetch the member to confirm.
- **Webhooks (8):** member.created, member.updated, member.deleted, member.plan.added, member.plan.updated, member.plan.canceled, team.member.added, team.member.removed. Enable in **Devtools**; POST JSON.
- **Pricing (best-effort):** Free until launch (no permanent free live tier); Basic ~$25/mo (4% txn fee, 1k members), Professional ~$39 (2%, 5k), Business ~$79 (0.9%, 10k+), Established ~$399 (0% Memberstack fee). **All fees stack on top of Stripe fees.**
- Integrations: Webflow, WordPress, Stripe, Zapier, Pipedream + REST/Node/DOM packages. **No MCP server.**
- Public GitHub org `github.com/memberstack` (packages `@memberstack/dom`, `@memberstack/admin`).
- Adjacent platforms surfaced → backlog: LearnWorlds, MemberPress, Outseta, Memberful. Skipped: Auth0/Firebase/Stytch/Ory/Zitadel (dev auth infra, not GTM), Vimeo OTT (video infra), Mighty Networks/Thinkific (already in backlog).
