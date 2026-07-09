---
name: sales-zenler
description: "New Zenler (Zenler) platform help — all-in-one course/membership platform for creators and coaches (newzenler.com) whose edge is built-in live classes + interactive webinars, multi-instructor, and 0% transaction fees. Public REST API (api.newzenler.com/api/v1, auth headers X-API-Key + X-Account-Name, ~25 endpoints for users/courses/funnels/live-classes/webinars/reports, 1000/min limit, Pro-gated) plus Zapier (7 triggers / 7 actions), Make, Integrately; no native webhooks. Use when auto-enrolling buyers from an external cart via the API or Zapier, syncing New Sale or Course Complete events into a CRM, polling sales/enrollment reports, the API or memberships or affiliate needing the Pro plan, your custom domain still showing New Zenler branding, a course getting deleted with no backup, limited control over course layout, or choosing Starter vs Pro vs Premium. Do NOT use for course/membership strategy across tools (use /sales-membership) or live-webinar selling strategy (use /sales-webinar)."
argument-hint: "[describe what you need help with in New Zenler]"
license: MIT
version: 1.0.0
tags: [sales, membership, courses, platform]
---

# New Zenler Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Enroll/create a user from an external purchase or app (API `POST /users` + `/enroll`, or Zapier action)
   - B) Route events out — New Sale, New User, Course Complete, Live Class/Webinar Registration, Funnel Subscription — into a CRM/ESP/Slack (Zapier trigger; there are **no native webhooks**)
   - C) Pull reports — enrollment, sales, course-progress, affiliate — into a warehouse (Reports API)
   - D) Configure a module — courses/drip, memberships, communities, funnels, email, live classes/webinars, coaching, affiliate
   - E) Pick a plan — Starter ($47) vs Pro ($97) vs Premium ($277), or understand what's Pro-gated (API, memberships, affiliate, white-label)
   - F) Fix a problem — branding on custom domain, data loss/backup, limited course-layout control, rate limits

2. **Where does data need to flow?** Into Zenler (create user, enroll, subscribe) → API write / Zapier action. Out of Zenler (sync a sale, route a completion) → Zapier trigger or **poll the Reports API**.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Course/membership strategy, retention, completion, or platform comparison | `/sales-membership {question}` |
| Live-webinar/live-class selling strategy (structure, registration, follow-up, conversion) | `/sales-webinar {question}` |
| Email sequence/broadcast strategy (in Zenler or a connected ESP) | `/sales-email-marketing {question}` |
| Email deliverability / inbox placement | `/sales-deliverability {question}` |
| Funnel/landing-page strategy across tools | `/sales-funnel {question}` |
| Designing an affiliate program (commission structure, recruiting) across tools | `/sales-affiliate-program {question}` |
| Checkout / order-bump / upsell optimization across tools | `/sales-checkout {question}` |

When routing, give the exact command, e.g. "This is a live-selling question — run: `/sales-webinar how do I structure a webinar that sells my course`".

## Step 3 — New Zenler platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's API-accessible vs Zapier vs UI-only), plan gates (the **Pro-gated API/memberships/affiliate/white-label**, custom-domain caps, Starter/Pro/Premium limits), the payment model (Stripe/PayPal/Razorpay at 0% Zenler fee), the user/report data model with JSON shapes, and quick-start recipes (enroll from an external cart; push sales into a CRM via Zapier; nightly report export).

**Read `references/zenler-api-reference.md`** for the integration surface — base `https://api.newzenler.com/api/v1/`, the `X-API-Key` + `X-Account-Name` header auth (key from Site → Developers, Pro+), the full endpoint inventory (users CRUD + enroll/unenroll, courses + bulk enroll, funnels subscribe/unsubscribe, live class/webinar register, and the four report families), pagination (15/page), the 1000/min → 403 limit, the standard `{response_code, message, data, pagination}` envelope, and the Zapier 7-trigger / 7-action surface.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Think API + Zapier, not webhooks.** The REST API handles writes (create user, enroll, subscribe) and report reads; Zapier/Make handle eventing because **there are no native webhooks**. For a pure-API shop, **poll the detailed reports** with `from`/`to` windows and dedupe.
- **API auth is two headers.** `X-API-Key` (from Site → Developers) **and** `X-Account-Name` (your subdomain). Missing the account-name header is the #1 first-call failure.
- **API is Pro-gated.** On Starter there's no Developers area at all. So are memberships, affiliate marketing, and white-label. Size the plan to the integration, not just the student count.
- **Identity is email; the user `id` is a string** (`313.5c109f1b58473`) — store it as text, not an integer.
- **A 403 usually means rate-limited, not unauthorized.** The 1000/min cap returns `403` with body "Rate Limited Exceeded" — branch on the message and back off, don't assume bad credentials.
- **Protect against data loss.** Reviewers have reported courses deleted with no backup. Keep source content off-platform and export students via the Reports API/CSV on a schedule.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing, which change frequently.*

1. **API access is Pro+.** Buying Starter to script enrollments is a dead end — there's no Developers area or API key on Starter. Memberships, affiliate, and white-label are also Pro+.
2. **Two auth headers are mandatory.** `X-API-Key` plus `X-Account-Name` (subdomain). Calls 401/fail silently if you send only the key.
3. **403 = rate limit, not auth.** 1000 calls/min returns `403 "Rate Limited Exceeded"`. Don't rotate keys in a panic — back off and retry.
4. **No native webhooks.** Don't promise webhook endpoints; eventing is Zapier/Make (connect with API key + subdomain) or polling the Reports API.
5. **Custom domains/branding are gated.** Starter has 0 custom domains, so pages stay on `*.newzenler.com`; removing Zenler branding (white-label) is Pro+. This is a frequent "looks unprofessional" complaint.
6. **Catastrophic data loss is a reported risk.** At least one reviewer lost a whole course with no notice/backup. Keep off-platform copies and export regularly.
7. **Limited course-layout control.** Customization is constrained vs WordPress/LMS stacks — set expectations for content-heavy or bespoke layouts.
8. **The API user `id` is a string, not an int** (`313.5c109f1b58473`). Persisting it as a number truncates/breaks it.

## Related skills

- `/sales-membership` — Course/membership strategy across tools (New Zenler is one of the live-session-first creator platforms covered), retention, completion, and platform comparison
- `/sales-webinar` — Live and automated webinar selling strategy (New Zenler runs live classes/interactive webinars natively)
- `/sales-email-marketing` — Email sequence and broadcast strategy (in Zenler or the ESP you connect via Zapier)
- `/sales-funnel` — Funnel and landing-page strategy across tools (Zenler has a built-in funnel builder)
- `/sales-affiliate-program` — Designing an affiliate program (commission structure, recruiting) — pairs with Zenler's built-in Pro+ affiliate module
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Auto-enroll a buyer from my external cart (developer/automation)
**User says**: "I sell my course on ThriveCart but host it in New Zenler. How do I auto-enroll buyers via the API?"
**Skill does**: Points to **Recipe 1** — on the ThriveCart purchase, `POST /api/v1/users` (with `X-API-Key` + `X-Account-Name` headers) to create the user if new, then `POST /api/v1/users/{id}/enroll` with the `course_id`. Notes the `id` comes back as a string, the API is **Pro-gated**, and the no-code path is the **Create User → Enroll User** Zapier actions. Flags that `X-Account-Name` (subdomain) is required alongside the key.
**Result**: External purchases enroll students in New Zenler automatically.

### Example 2: Notify my CRM when a sale or completion happens
**User says**: "When someone buys or finishes a course in Zenler, I want them tagged in HubSpot."
**Skill does**: Explains there are **no native webhooks**, so use the **New Sale** / **Course Complete** Zapier triggers mapped to a HubSpot create/update-contact action (Recipe 2); or, for a pure-API setup, **poll `GET /reports/sales/detailed`** with `from`/`to` and dedupe on `order_id`. Routes nurture design to `/sales-email-marketing`.
**Result**: Sales and completions flow into the CRM without manual entry.

### Example 3: My custom domain still shows "New Zenler"
**User says**: "I'm on a paid plan but my course pages still look like a free New Zenler site."
**Skill does**: Identifies this as a plan-gate issue — **custom domains are 0 on Starter** and **white-label (removing Zenler branding) is Pro+**. Recommends upgrading to Pro/Premium to add a custom domain and strip branding, and verifies the domain is connected under the site settings. Notes pricing/limits are best-effort and should be confirmed live.
**Result**: User understands the branding is a tier limitation and how to resolve it.

## Troubleshooting

### My first API call returns 401 / nothing works
**Symptom**: Every request is rejected even though the key looks right.
**Cause**: Missing the **`X-Account-Name`** header (subdomain), calling on a **Starter** plan (no API access), or a malformed base URL.
**Solution**: Send **both** `X-API-Key` and `X-Account-Name` on every call, confirm you're on **Pro/Premium** (generate/copy the key at Site → Developers), and use base `https://api.newzenler.com/api/v1/`. If you're still blocked, regenerate the key and retry.

### My integration suddenly returns 403
**Symptom**: Calls that worked start failing with 403.
**Cause**: You've crossed the **1000 calls/minute** rate limit — the body says "Rate Limited Exceeded". A 403 here is rate-limit, not auth.
**Solution**: Branch on the response message, add exponential backoff (1→2→4→8s), batch where possible (bulk-enroll via `POST /courses/{id}/enroll`), and spread report pulls. Don't assume your key is bad.

### A course/content disappeared, or I want to be safe
**Symptom**: Content is gone, or you're worried about losing it.
**Cause**: Reviewers have reported a course deleted with no notification/backup; the platform is your only copy if you didn't export.
**Solution**: Treat Zenler as a delivery layer, not a vault. Keep source videos/lessons off-platform, and export students + sales via the **Reports API** (`/reports/enrollments/detailed`, `/reports/sales/detailed`) or CSV on a schedule. Contact support immediately if content vanishes.
