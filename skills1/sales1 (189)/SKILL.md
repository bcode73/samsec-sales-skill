---
name: sales-freshlearn
description: "FreshLearn (freshlearn.com) platform help — budget all-in-one LMS/creator platform for courses, cohorts, digital products, memberships, communities, email, and an AI Studio (AI course creation, chat-with-content, coaching), with unlimited learners and 0% transaction fees. REST API (api.freshlearn.com/v1, api-key header, cursor pagination; No Brainer+ gated) + native webhooks + Zapier (6 triggers / 9 actions), Make, Pabbly. Use when auto-enrolling buyers from an external cart via the API or Zapier, syncing new members or course-completion events into a CRM, paginating members/payments with the cursor, the API or workflows needing the No Brainer+ plan, Zapier/community/certificates locked on the Pro plan, the page builder feeling limited (coding header/footer per page), billing/refund/cancellation friction, or choosing Free vs Pro vs No Brainer vs No Brainer+. Do NOT use for course/membership strategy across tools (use /sales-membership) or email-marketing strategy (use /sales-email-marketing)."
argument-hint: "[describe what you need help with in FreshLearn]"
license: MIT
version: 1.0.0
tags: [sales, membership, courses, platform]
---

# FreshLearn Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Enroll/create a member from an external purchase or app (API enroll-in-product, or Zapier action)
   - B) Route events out — new member, course/masterclass/bundle/download enrollment, course completed — into a CRM/ESP/Slack (native webhook or Zapier trigger)
   - C) Export members/payments/assessments into a warehouse (cursor-paginated reads)
   - D) Configure a module — courses/drip, cohorts, AI Studio, community, email, certificates/assessments, referral/affiliate, live classes
   - E) Pick a plan — Free vs Pro ($35) vs No Brainer ($46) vs No Brainer+ ($89), or understand the gates (Zapier=No Brainer; API/workflows=No Brainer+)
   - F) Fix a problem — limited page builder, no-refund/billing, glitches, API 401/403 on the wrong plan

2. **Where does data need to flow?** Into FreshLearn (create member, enroll) → API write / Zapier action. Out of FreshLearn (sync a member, route a completion) → native webhook / Zapier trigger / cursor-paginated read.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Course/membership strategy, retention, completion, or platform comparison | `/sales-membership {question}` |
| Email sequence/broadcast strategy (in FreshLearn or a connected ESP) | `/sales-email-marketing {question}` |
| Email deliverability / inbox placement | `/sales-deliverability {question}` |
| Funnel/landing-page strategy across tools | `/sales-funnel {question}` |
| Checkout / order-bump / upsell optimization across tools | `/sales-checkout {question}` |
| Designing an affiliate program (commission structure, recruiting) across tools | `/sales-affiliate-program {question}` |
| Live/webinar-based selling strategy | `/sales-webinar {question}` |

When routing, give the exact command, e.g. "This is a retention question — run: `/sales-membership how do I reduce course churn`".

## Step 3 — FreshLearn platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's API-accessible vs Zapier vs UI-only), plan gates (the **No Brainer+ API/workflows** vs **No Brainer Zapier/community/certificates** split), the payment model (Stripe/PayPal/Razorpay at 0% FreshLearn fee, unlimited learners), the member/enrollment data model with JSON shapes, and quick-start recipes (enroll from a cart; push completions to a CRM; nightly export).

**Read `references/freshlearn-api-reference.md`** for the integration surface — base `https://api.freshlearn.com/v1`, the `api-key` header auth (key from Settings → User → API Key, No Brainer+), cursor pagination (`cursor`/`limit` 1–200/`order`, `pageInfo.nextCursor`+`hasMore`, Unix-second date filters), the documented sections (Members, Courses, Product Enrollments, Payments, Assessments), and the Zapier 6-trigger / 9-action surface. Note exact REST paths are JS-rendered — the reference marks constructed paths.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Mind the two-step plan gate.** **Zapier** unlocks at **No Brainer ($46)**, but the **REST API and
  unlimited automations** unlock at **No Brainer+ ($89)**. Buying Pro to script enrollments is a dead end.
- **Auth is one header.** `api-key` (from Settings → User → API Key). The key is account-scoped, so every
  response is your academy's data only.
- **Enroll actions are upserts.** Enroll-in-product creates the member if the email is new — you rarely
  need a separate create call. Identity is email everywhere.
- **Pagination is cursor-based.** Follow `pageInfo.nextCursor` until `hasMore` is false; `limit` maxes at
  200; date filters are **Unix seconds**, not ISO strings.
- **Set expectations on the builder.** The page builder is limited (reviewers mention coding header/footer
  per page). For bespoke design, plan around templates rather than promising pixel control.
- **Flag the no-refund policy.** Billing/cancellation friction and a no-refund stance are recurring
  complaints — advise testing on the Free plan before committing to an annual/bi-annual term.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing, which change frequently.*

1. **API + unlimited workflows are No Brainer+ ($89) only.** No API key area on Free/Pro/No Brainer. Don't promise API automation below the top self-serve tier.
2. **Zapier, community, certificates, assessments, and branding removal are No Brainer ($46)+.** Pro is courses + email + checkout only — a common "where's my community/Zapier?" surprise.
3. **Enroll endpoints upsert the member.** Calling create-then-enroll can double-handle; the enroll action already creates the member if the email is new.
4. **Cursor pagination, Unix-second dates.** Page via `pageInfo.nextCursor`/`hasMore` (not page numbers); `limit` ≤ 200; date filters are epoch seconds. ISO strings will be rejected/ignored.
5. **No published webhook signature.** Re-verify the member via `GET /v1/members` before granting sensitive access; restrict listeners to a secret URL.
6. **Limited page builder.** Reviewers report having to code the header/footer on each page — set design expectations and lean on templates.
7. **No-refund policy + billing/cancellation friction.** A recurring complaint — test on Free first and understand the cancellation flow before an annual/bi-annual commitment.
8. **Exact REST paths are JS-rendered in the docs.** The api-reference marks constructed paths; confirm method+path against the live reference before shipping.

## Related skills

- `/sales-membership` — Course/membership strategy across tools (FreshLearn is one of the budget all-in-one creator platforms covered), retention, completion, and platform comparison
- `/sales-email-marketing` — Email sequence and broadcast strategy (in FreshLearn or the ESP you connect)
- `/sales-funnel` — Funnel and landing-page strategy across tools (FreshLearn has a built-in but limited page builder)
- `/sales-affiliate-program` — Designing an affiliate program (commission structure, recruiting) — pairs with FreshLearn's built-in referral/affiliate module
- `/sales-webinar` — Live and webinar-based selling strategy (FreshLearn runs live classes via Zoom)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Auto-enroll a buyer from my external cart (developer/automation)
**User says**: "I sell my course on ThriveCart but host it in FreshLearn. How do I auto-enroll buyers via the API?"
**Skill does**: Points to **Recipe 1** — on the ThriveCart purchase, POST to the product-enrollments endpoint with `api-key` header, the buyer's email + `course_id`; the enroll action **creates the member if new** (no separate create call). Flags that the **API is No Brainer+**, identity is email, and the no-code path is the **Enroll Member in Course Product** Zapier action (Zapier needs No Brainer+). Notes exact paths are best-effort — confirm in the live reference.
**Result**: External purchases enroll learners in FreshLearn automatically.

### Example 2: Notify my CRM when someone enrolls or finishes
**User says**: "When someone buys or completes a course in FreshLearn, I want them in HubSpot."
**Skill does**: Uses the **Get Member Data** / **Get Course Completed Members** Zapier triggers (or a native webhook) mapped to a HubSpot create/update-contact action (Recipe 2). Notes the webhook isn't signed, so re-verify via `GET /v1/members` first, and routes nurture design to `/sales-email-marketing`.
**Result**: Enrollments and completions flow into the CRM without manual entry.

### Example 3: I'm on a paid plan but can't find Zapier or the API
**User says**: "I upgraded to Pro but there's no Zapier and no API key — why?"
**Skill does**: Identifies the plan-gate split — **Zapier is No Brainer ($46)+** and the **REST API is No Brainer+ ($89)+**; Pro only includes courses, email, and checkout. Recommends the tier that matches the integration need (No Brainer for Zapier/community/certificates, No Brainer+ for API/workflows/Course AI), and frames pricing as best-effort to verify live.
**Result**: User understands which capability needs which tier and upgrades intentionally.

## Troubleshooting

### My API call returns 401/403
**Symptom**: Requests are rejected even with a key that looks right.
**Cause**: The account isn't on **No Brainer+** (no API access on Free/Pro/No Brainer), the `api-key` header is missing/misspelled, or you're hitting the wrong base URL.
**Solution**: Confirm the plan is **No Brainer+**, copy the key from **Settings → User → API Key**, send it as the **`api-key`** header, and use base `https://api.freshlearn.com/v1`. Remember the key is account-scoped — it only ever returns your academy's data.

### My pagination loop never ends or misses records
**Symptom**: Exports loop forever, duplicate, or skip members.
**Cause**: Treating the cursor like a page number, ignoring `hasMore`, or exceeding `limit`.
**Solution**: Pass `pageInfo.nextCursor` back as `cursor`, stop when `hasMore` is `false`, keep `limit` ≤ 200, and use **Unix-second** timestamps for date filters. Dedupe on member id/email.

### Where are my community / certificates / automations?
**Symptom**: Features you expected aren't visible on your plan.
**Cause**: Plan gating — community, certificates, assessments, Zapier, and branding removal start at **No Brainer ($46)**; the **REST API, unlimited workflows, and Course AI are No Brainer+ ($89)**. Pro is courses + email + checkout only.
**Solution**: Match the plan to the feature: upgrade to **No Brainer** for community/certificates/Zapier/apps, or **No Brainer+** for the API, automations, and AI features. Verify against the current pricing page before committing.
