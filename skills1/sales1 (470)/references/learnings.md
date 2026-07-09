# Referral Factory — Learnings

Accumulated, dated platform knowledge. Append new findings with a date stamp so staleness is auditable.

---

**2026-06-27**: Research baseline. Built from the official developer portal (ReadMe; `developers.referral-factory.com`, fetched as Markdown via its `llms.txt` index), the marketing site, the pricing page, and G2/Capterra reviews.

- **API is solid and clean.** REST, base `https://api.referral-factory.com/api/v2`, **Bearer** auth, **one active token per account** (regenerating deactivates the old one — a real footgun for live integrations). Burst limit **600 calls/min**; >3 abuses → temporary IP block. Cursor pagination via `links.next`, `per_page` ≤ 250.
- **Core object is the User**, typed `person_referring` vs `person_invited`. Attribution is via the `referrer` field (`{field: id|code|email, value}`) on `POST /users`, or via the referral link. No `referrer` = standalone referrer, no attribution.
- **Two-step reward flow.** Qualification (`PUT /users/qualification`) makes a reward **due**; you then `POST /rewards/issue/{id}` (or `/cancel/{id}`). Reward `{metric}` enum: `amount`/`commission`/`coupon`/`custom`. Easy to miss that *adding* a user does nothing until *qualified*.
- **Webhooks: no documented HMAC.** Outbound triggers = new user + qualified referral. Inbound = qualify by code/coupon (and issue rewards). No published payload schema (docs suggest inspecting via webhook.site) and no retry semantics — treat endpoint as secret, dedupe, re-verify via `GET /users/{identifier}`.
- **Pricing scales by users**, and it's not cheap: Basic ~$200/mo (20k), Pro ~$400/mo (40k), Enterprise ~$1,000/mo (100k+). API/webhooks on all paid plans; **white-label + custom domain are Pro+**, custom HTML is Enterprise. Reviewers specifically flag custom-domain fees and overall price as "high side."
- **Payout reality:** PayPal cash, gift cards (200+ countries), Stripe credits/coupons, commissions, points, vouchers, swag, custom — **no direct bank transfer** (a recurring review complaint).
- **Integrations:** native HubSpot, Salesforce, Stripe, Pipedrive, Zoho, Intercom, Monday, Service Titan, Tremendous, PayPal, plus Zapier/Make/n8n (50+ tools). HubSpot app marketplace listing exists.
- **Promotion codes** (`promotion: true` on create) only work when **Stripe is connected**.
- **Doc inconsistency:** OpenAPI server is `api.referral-factory.com/api/v2`, but one help article shows `referral-factory.com/api/v2`. Treat the `api.` host as authoritative; verify in-account.
- **Review signal (G2/Capterra ~4.8★):** praised for ease of use, templates by industry, white-label branding, support. Complaints: high learning curve, limited template editing, custom-domain fees, no direct bank payouts, and skepticism that unique referral links capture organic WOM (an *incrementality/attribution* concern — route strategy to `/sales-audience-growth`).
- **Referral ≠ affiliate:** the platform has its own "referral vs affiliate" explainer page; it runs customer referrals (can pay commissions) but isn't a partner-portal affiliate platform.

⚠️ **Fetch note for future runs:** the marketing site is partly JS-rendered, but the developer docs are fully accessible as Markdown via `https://developers.referral-factory.com/llms.txt` (each reference page has a `.md` twin, e.g. `/reference/create-a-user.md`). Fetch those for verbatim API content. Fetch them **in parallel with short timeouts** — sequential loops over ~20 pages time out.
