---
name: sales-memberstack
description: "Memberstack platform help — no-code membership, auth, and Stripe-payments layer for sites you build yourself (memberstack.com): add login (email/password, passwordless, social, 2FA), paid memberships, and content gating to Webflow, WordPress, or any custom site via a script tag + data attributes. Developer surface: a front-end DOM package (public key) plus an Admin REST API (base admin.memberstack.com, X-API-KEY secret key, member CRUD, verify-token, cursor pagination, 25 req/s) and 8 webhooks (member.created/updated/deleted, member.plan.*, team.*). Use when building a Memberstack Admin API or webhook integration, syncing members from your backend, verifying a member JWT to gate your own API, webhook signatures can't be verified via REST, a PATCH wiped the json field, or transaction-fee/plan questions. Do NOT use for course/membership-platform strategy or comparison (use /sales-membership), checkout-conversion optimization across tools (use /sales-checkout), or email marketing (use /sales-email-marketing)."
argument-hint: "[describe what you need help with in Memberstack]"
license: MIT
version: 1.0.0
tags: [sales, membership, no-code, platform]
github: "https://github.com/memberstack"
---

# Memberstack Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Manage members from your backend (create/read/update/delete) via the Admin REST API
   - B) Verify a member's JWT to gate your own API or app
   - C) React to events via webhooks (member.created, member.plan.*) — sync to a CRM/warehouse
   - D) Configure front-end auth, gating, or Stripe checkout (DOM package + data attributes)
   - E) Pick a plan / understand transaction fees
   - F) Fix a problem — webhook verification, json overwrite, member-not-found, 1.0→2.0 migration

2. **Front-end or back-end?** Browser auth/gating/checkout = **DOM package** (public key). Server-side member ops + token/webhook verification = **Admin REST/Node** (secret key). This decides everything.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Choosing or comparing membership/course platforms | `/sales-membership {question}` |
| Checkout-conversion / order-bump / upsell strategy across tools | `/sales-checkout {question}` |
| Email sequences and broadcasts (Memberstack doesn't send email) | `/sales-email-marketing {question}` |
| Wiring Memberstack into a CRM/warehouse or other tools | `/sales-integration {question}` |
| Membership/community structure, pricing, and retention strategy | `/sales-membership {question}` |

When routing, give the exact command, e.g. "Platform comparison — run: `/sales-membership Memberstack vs a hosted course platform`".

## Step 3 — Memberstack platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (DOM vs Admin, what's front-end vs server-side vs webhook), the plan/transaction-fee gates, the member data model with JSON shapes, and quick-start recipes (create a member server-side; verify a member JWT to gate your API; sync member.created to a CRM via webhook).

**Read `references/memberstack-api-reference.md`** for the Admin REST API — base `https://admin.memberstack.com`, `X-API-KEY` auth (`sk_sb_` test / `sk_live_` live, server-side only), the member CRUD + verify-token + add/remove-plan endpoints, cursor pagination, the 25 req/s limit, the 8 webhook events, and the webhook-signature-verification caveat.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Two packages, two keys.** Front-end DOM package uses a **public** key (login/signup/gating/Stripe checkout in the browser); the Admin REST/Node package uses a **secret** key (server-side member ops). Never put a secret key client-side.
- **Verify member JWTs to protect your own backend.** `POST /members/verify-token` turns a logged-in Memberstack session into a trusted member ID for your API.
- **Webhook signatures need the Node package.** REST can't verify them — if you're REST-only, re-fetch the member by ID to confirm an event before trusting it.
- **Watch the `json` PATCH trap.** `customFields`/`metaData` shallow-merge, but `json` is **fully replaced** — read-modify-write to avoid wiping it.
- **Handle member-not-found as 200 + data:null**, not 404.
- **Respect 25 req/s** — back off on 429; paginate lists with `after`/`endCursor` (max 100).
- **Fees stack on Stripe.** 0.9–4% by tier; only the $399 Established plan is 0% — run the math before pricing memberships.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing, which change frequently.*

1. **Webhook signature verification is NOT supported via REST.** Use the Node Admin package, or verify events out-of-band (re-fetch the member). Don't trust raw webhook payloads on a REST-only stack.
2. **`json` is fully replaced on PATCH** (while `customFields`/`metaData` shallow-merge). Read-modify-write the `json` object or you'll silently wipe data.
3. **Secret keys are server-side only.** The DOM package's public key is fine in the browser; an `sk_*` key in client code or a public repo is a breach.
4. **Transaction fees stack on Stripe.** 4% (Basic) / 2% (Pro) / 0.9% (Business) / 0% (Established $399) — plus Stripe's own fees. Only the top tier is fee-free.
5. **No permanently free live tier.** Free until launch; the test key (`sk_sb_`) caps at 50 test members.
6. **Member-not-found returns 200 with `data: null`,** not 404 — handle it explicitly.
7. **It's a layer, not a host.** No course/LMS hosting, no marketing email — pair with an LMS and an ESP if you need those.
8. **1.0 vs 2.0.** 2.0 is the current rebuild with this API; 1.0 is legacy with a different API. Confirm which you're on.

## Related skills

- `/sales-membership` — Membership/course platform strategy, pricing, and retention, and choosing Memberstack vs a hosted course platform
- `/sales-memberful` — Memberful (the closest membership-first alternative: own-your-audience subscriptions, private podcasts/newsletters, GraphQL API + signed webhooks + OAuth, on your own Stripe)
- `/sales-checkout` — Checkout, subscription, and upsell optimization (Memberstack runs payments through Stripe)
- `/sales-integration` — Wiring Memberstack's API/webhooks into a CRM, warehouse, or other tools
- `/sales-email-marketing` — Email sequences for members (Memberstack doesn't send email — connect an ESP)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Create a member from my backend after an external signup (developer/automation)
**User says**: "When someone signs up through my own form, how do I create them in Memberstack from my server?"
**Skill does**: Shows `POST https://admin.memberstack.com/members` with the `X-API-KEY` secret key (server-side only), sending `email` + `password` (+ `customFields`) — Recipe 1 in `references/platform-guide.md`. Notes the 25 req/s limit, that the response returns a `mem_*` id, and that paid plans go through Stripe checkout on the front-end while free plans use the add-plan endpoint.
**Result**: User creates members server-side and understands key safety + the free-vs-paid-plan split.

### Example 2: Gate my own backend API to logged-in members
**User says**: "My Webflow front-end uses Memberstack. How do I protect my custom API so only logged-in members can call it?"
**Skill does**: Points to `POST /members/verify-token` (Recipe 2) — the front-end sends the member's Memberstack JWT to your backend, which verifies it via the Admin API and gets the member ID before serving data. Explains the public-key (browser) vs secret-key (server) split.
**Result**: User validates Memberstack sessions server-side to authorize API calls.

### Example 3: My webhook fires but I can't verify it / my json data got wiped
**User says**: "I'm syncing member.created to my CRM but can't verify the signature, and a PATCH erased my custom json."
**Skill does**: Explains **webhook signature verification isn't supported via REST** — use the Node package or re-fetch the member by ID to confirm (Recipe 3 + Gotcha 1). For the data loss, explains **`json` is fully replaced on PATCH** (unlike `customFields`/`metaData`) and to read-modify-write it (Gotcha 2).
**Result**: User hardens webhook trust and stops overwriting `json`.

## Troubleshooting

### I can't verify my webhook signatures
**Symptom**: No way to validate that a webhook POST really came from Memberstack via the REST API.
**Cause**: Webhook signature verification is only implemented in the **Node.js Admin Package**, not the REST API.
**Solution**: Use the Node Admin package for verification, or on a REST-only stack verify out-of-band — treat the payload as a hint and re-fetch the member with `GET /members/:id` before acting. Lock your webhook endpoint to a secret path and validate the member exists.

### A PATCH wiped my member's custom data
**Symptom**: Updating a member erased fields you didn't send.
**Cause**: On `PATCH /members/:id`, `customFields` and `metaData` are shallow-merged, but **`json` is fully replaced**.
**Solution**: For `json`, read the current value first, merge your changes in app code, then send the complete object. Use `customFields`/`metaData` when you want partial updates.

### Looking up a member returns nothing but no error
**Symptom**: `GET /members/:id_or_email` returns `200` and you expected a 404 for a missing member.
**Cause**: Memberstack returns `200` with `"data": null` for a non-existent member.
**Solution**: Check `data === null` rather than relying on the status code. URL-encode emails when looking up by email.

### Hitting 429 / sync is throttled
**Symptom**: Bulk member operations start returning 429.
**Cause**: You've exceeded the **25 requests/second** limit.
**Solution**: Throttle to ≤25 req/s, add exponential backoff on 429, and paginate reads with `after` + `endCursor` (max 100 per page) instead of hammering the list endpoint.
