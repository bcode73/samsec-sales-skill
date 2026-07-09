---
name: sales-memberful
description: "Memberful platform help — membership + paid-subscription layer (Patreon-owned, memberful.com) for creators/publishers/communities: checkout, trials, coupons, gated content, private podcasts/newsletters/downloads, and OAuth SSO, on your own Stripe. Developer surface: a GraphQL API (endpoint ACCOUNT.memberful.com/api/graphql, Authorization: Bearer key from Settings > Custom applications; queries + mutations for members/subscriptions/passes/plans/coupons; cursor pagination) and 21 HMAC-SHA256-signed webhooks (X-Memberful-Webhook-Signature; member/subscription/order/plan/download events). WordPress/Discord/Mailchimp/Kit/Zapier integrations. Use when querying/mutating members via GraphQL, verifying a signed webhook, wiring OAuth SSO, untangling the dashboard-Plan-vs-API-Pass terminology, or weighing the 10%/4.9% fees. Do NOT use for membership-platform strategy/comparison (use /sales-membership), checkout-conversion optimization across tools (use /sales-checkout), or email marketing (use /sales-email-marketing)."
argument-hint: "[describe what you need help with in Memberful]"
license: MIT
version: 1.0.0
tags: [sales, membership, creator, platform]
github: "https://github.com/memberful"
---

# Memberful Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Query or mutate members / subscriptions / passes / coupons via the GraphQL API
   - B) Verify a signed webhook and react to a lifecycle event (signup, renewal, refund…)
   - C) Add "Sign in with Memberful" (OAuth SSO) to your own app
   - D) Gate content / set up private podcasts / downloads (WordPress plugin or website builder)
   - E) Sync members to Discord / Mailchimp / Kit / a CRM
   - F) Pick a plan / understand the 10% vs 4.9% transaction fees

2. **Front-end or back-end?** Browser gating/checkout = WordPress plugin / website builder. Server-side member ops, OAuth callback, and webhook verification = **GraphQL API + middleware** (Bearer key, server-side only). This decides everything.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Choosing or comparing membership/course platforms | `/sales-membership {question}` |
| Checkout / trial / dunning / upsell **optimization** across tools | `/sales-checkout {question}` |
| Email sequences/newsletters to members (Memberful doesn't send marketing email) | `/sales-email-marketing {question}` |
| Wiring Memberful into a CRM/warehouse or other tools generically | `/sales-integration {question}` |
| Membership/community structure, pricing, and retention strategy | `/sales-membership {question}` |

When routing, give the exact command, e.g. "Platform comparison — run: `/sales-membership Memberful vs a hosted course platform`".

## Step 3 — Memberful platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (GraphQL vs front-end vs webhook vs UI), the Plan-vs-Pass terminology trap, plan/transaction-fee gates, the member data model with JSON shapes, and quick-start recipes (query members paginated; verify a webhook + re-fetch; OAuth SSO).

**Read `references/memberful-api-reference.md`** for the integration surface — the GraphQL endpoint `https://ACCOUNT-URL.memberful.com/api/graphql`, **Bearer** API-key auth (from Settings → Custom applications), example query/mutation, Relay cursor pagination, member-metadata limits, the GraphQL error convention (HTTP 200 + `errors`), the **21 webhook events**, the **HMAC-SHA256** signature scheme (`X-Memberful-Webhook-Signature`), and OAuth.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **GraphQL, not REST.** One endpoint, `POST …/api/graphql`, `Authorization: Bearer <key>` (key from Settings → Custom applications, server-side only). Build/test in the in-dashboard **API Explorer**.
- **Mind the Plan-vs-Pass swap.** Dashboard **"Plan" = API `Pass`** (the membership); dashboard **"Price" = API `Plan`** (a pricing variant). Using the wrong name is the #1 first-integration bug.
- **Check `errors`, not the status code.** The API returns **HTTP 200 even on failure** — inspect the `errors` array in the body.
- **Verify webhooks with HMAC-SHA256.** Compute `HMAC-SHA256(rawBody, webhookSecret)` and constant-time compare to `X-Memberful-Webhook-Signature`. Then **re-query GraphQL** for authoritative state — the payload is a snapshot. Event names mix `_` and `.` — match exact strings.
- **OAuth needs server-side middleware.** The "Sign in with Memberful" callback can't run purely client-side — exchange the code on your server.
- **Fees are the lever.** Free = **10%**, Pro/Premium = **4.9%**, all **on top of Stripe** (2.9%+30¢) on your own Stripe account. The 10%→4.9% drop pays for Pro quickly at any volume.
- **It's a layer, not a host.** No course/LMS hosting and no marketing email — pair with an LMS and an ESP if you need those.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — API verbatim from memberful.com/docs; pricing from marketing/reviews. Confirm in-account.*

1. **Dashboard "Plan" ≠ API `Plan`.** API `Pass` = dashboard Plan (the membership); API `Plan` = dashboard Price (a pricing variant). Read the terminology table before querying.
2. **HTTP 200 on errors.** GraphQL returns 200 with an `errors` array even when the operation fails — never branch on the status code alone.
3. **Webhooks are HMAC-SHA256 signed — verify them.** Header `X-Memberful-Webhook-Signature`, key = Webhook secret, over the **raw** body. Then re-fetch via GraphQL; treat the payload as a trigger, not the source of truth.
4. **Event names are inconsistently cased.** Some use `snake_case` (`member_signup`, `member_updated`), some `dot.case` (`member.deleted`, `subscription.created`). Match the exact event string.
5. **Member metadata is API-only and capped.** 50 keys, 40-char keys, 500-char values — and you can't set it from the dashboard.
6. **Transaction fees stack on Stripe.** Free **10%**, Pro/Premium **4.9%**, plus Stripe's 2.9%+30¢. Bring your own Stripe account.
7. **It's a layer, not a host.** No LMS/course hosting, no marketing email — connect an LMS and an ESP if needed.

## Related skills

- `/sales-membership` — Membership/course platform strategy, pricing, and retention, and choosing Memberful vs a hosted course platform or another paywall layer
- `/sales-memberstack` — Memberstack (the closest direct alternative: no-code auth/paywall + Stripe for Webflow/custom sites; REST Admin API)
- `/sales-checkout` — Checkout, trial, and subscription optimization (Memberful runs payments through your Stripe)
- `/sales-email-marketing` — Newsletters/sequences for members (Memberful doesn't send marketing email — connect an ESP)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Export all members + their active membership via the API (developer/automation)
**User says**: "How do I pull every member and which plan they're on out of Memberful?"
**Skill does**: Shows a GraphQL `members(first: 100, after: …)` query against `https://ACCOUNT-URL.memberful.com/api/graphql` with `Authorization: Bearer <key>`, looping on `pageInfo.hasNextPage`/`endCursor` (Recipe 1), and reading each node's `subscriptions { pass { name } }` — flagging that the dashboard "Plan" is the API **`pass`**, and to check the `errors` array since the API returns HTTP 200 on failure.
**Result**: A complete, paginated member + membership export.

### Example 2: Trust a Memberful webhook before granting access
**User says**: "Memberful POSTs to my endpoint on signup — how do I know it's real?"
**Skill does**: Explains **HMAC-SHA256** verification — compute `HMAC-SHA256(rawBody, webhookSecret)` and constant-time compare to **`X-Memberful-Webhook-Signature`** (Recipe 2 + Gotcha 3) — then **re-query GraphQL** for the member's current state rather than trusting the snapshot. Notes the 21 events and the `_` vs `.` casing.
**Result**: Authenticated, tamper-evident webhook intake that grants access on confirmed state.

### Example 3: Memberful or Memberstack for a paid membership?
**User says**: "I want paid memberships + gated content on my own site — Memberful or Memberstack?"
**Skill does**: Frames it — **Memberful** is membership-first (own-your-audience subscriptions, private podcasts/newsletters/downloads, WordPress, GraphQL API, fees 10%/4.9% on your Stripe), **Memberstack** is auth/paywall-first for Webflow/custom sites (REST Admin API, JWT gating). Recommends by primary need and routes deeper platform selection: "run: `/sales-membership Memberful vs Memberstack for a paid community`."
**Result**: A need-based choice between the two closest tools.

## Troubleshooting

### My GraphQL query "succeeds" but returns no data
**Symptom**: You get an HTTP 200 but `data` is null or empty.
**Cause**: Memberful follows the GraphQL convention — **errors come back as HTTP 200** with an `"errors"` array (bad field name, wrong type, auth issue), and querying the wrong type name (`Plan` vs `Pass`) returns nothing.
**Solution**: Inspect the `errors` array in the response body, and confirm you're using the **API** names: `Pass` = dashboard "Plan", `Plan` = dashboard "Price". Test the query in the in-dashboard **API Explorer** first.

### My webhook signature check fails
**Symptom**: The HMAC you compute doesn't match `X-Memberful-Webhook-Signature`.
**Cause**: Hashing a re-serialized body (not the raw bytes), the wrong Webhook secret, or normalizing the event name.
**Solution**: Compute **HMAC-SHA256 over the raw request body** with the **Webhook secret** (Settings → Webhooks) and constant-time compare to the header. Match the docs' Ruby/JS examples exactly. Don't normalize event strings — some use `_`, some use `.`. Once verified, re-fetch the record via GraphQL before acting.

### "Sign in with Memberful" callback fails on my static site
**Symptom**: The OAuth redirect comes back but you can't complete the token exchange.
**Cause**: The OAuth code-for-token exchange **must run server-side** — it can't execute on a purely static/client-only site.
**Solution**: Add server-side middleware (Node/Python or a serverless function on Cloudflare Workers / AWS Lambda) to handle the callback, exchange the code, then read the member's passes to authorize. For platform selection beyond auth, use `/sales-membership`.
