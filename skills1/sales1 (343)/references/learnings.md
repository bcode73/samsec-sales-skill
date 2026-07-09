# Memberful — Learnings

Accumulated, dated platform knowledge. Append new findings with a date stamp so staleness is auditable.

---

**2026-06-28**: Research baseline. Built from the marketing site (memberful.com), the developer docs (memberful.com/docs/api-reference/* — GraphQL API, webhooks, webhook-event-reference), and pricing/comparison content.

- **Category:** **membership + paid-subscription** layer, **owned by Patreon**. For creators/publishers/communities (podcasters, bloggers, journalists, clubs). Gated content, **private podcasts** (per-member RSS), newsletters, digital downloads — on **your own Stripe account** (Memberful never holds funds). NOT a hosted course/LMS, NOT an email tool. Audience: indie creators / makers / small publishers — strong fit.
- **API = GraphQL only** (no REST). Single endpoint `https://ACCOUNT-URL.memberful.com/api/graphql`, `Authorization: Bearer <key>`, key from **Settings → Custom applications**. Queries + mutations (members, subscriptions, passes, plans, coupons). The **API Explorer / Documentation Explorer** (in-dashboard) is the live, authoritative schema.
- **⚠️ Terminology swap:** dashboard **"Plan" = API `Pass`** (the membership), dashboard **"Price" = API `Plan`** (a pricing variant). Single biggest first-integration gotcha.
- **Pagination:** Relay-style cursor (`first`/`after`/`before`/`last`, `pageInfo { hasNextPage endCursor }`, `edges { node }`).
- **Member metadata:** custom JSON **via API only** — max 50 keys, 40-char keys, 500-char values.
- **Errors:** GraphQL convention — **HTTP 200 even on failure**; check the `errors` array, not the status code.
- **Webhooks (21 events, HMAC-signed):** Settings → Webhooks. Signature **HMAC-SHA256**, header **`X-Memberful-Webhook-Signature`**, key = Webhook secret, message = **raw body** (Ruby `OpenSSL::HMAC.hexdigest` / JS `crypto.createHmac('sha256',…)` examples in docs). Events: member_signup, member_updated, member.deleted, tax_id.updated, custom_fields.updated; subscription.created/updated/renewed/activated/deactivated/deleted; order.purchased/refunded/suspended/completed; subscription_plan.created/updated/deleted; download.created/updated/deleted. **Recommended pattern:** webhook is a trigger → re-query GraphQL for authoritative state.
- **⚠️ Event-name casing is inconsistent:** some events use `snake_case` (`member_signup`, `member_updated`) and some use `dot.case` (`member.deleted`, `subscription.created`). Match exact strings.
- **OAuth (Sign in with Memberful):** SSO for your own app; **callback requires server-side middleware** (Node/Python/serverless) — can't run purely client-side.
- **Integrations:** WordPress plugin, Discord (role sync), Mailchimp, Kit (ConvertKit), Stripe (BYO), Zapier.
- **Pricing (2026):** Free $0 (**10%** fee), Pro **$25/mo** (**4.9%**), Premium **$100/mo** (4.9%) — all **plus Stripe** 2.9%+30¢. The 10%→4.9% drop usually justifies Pro fast.
- **Competitive set:** Memberstack (no-code auth/paywall — direct, already a skill), MemberSpace, Outseta, Patreon (parent), Podia, Ghost (memberships), Substack, Circle, Pico, Whop, Gumroad. Memberful's angle: own-your-audience memberships on your Stripe, with a real GraphQL API + signed webhooks + private podcasts.

⚠️ **Fetch note for future runs:** marketing site + `memberful.com/docs/api-reference/*` fetch fine. The **API Explorer** (live schema) is in-dashboard only — exact mutation argument names / full type fields must be confirmed there or via the Documentation Explorer. Gaps: full per-mutation argument lists, exact webhook payloads for non-`member_signup` events, OAuth scope names.
