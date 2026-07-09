---
name: sales-ecwid
description: "Ecwid (by Lightspeed) platform help — embeddable ecommerce that adds a store and checkout to any existing site (WordPress, Wix, custom HTML) plus a hosted Instant Site, with 0% transaction fees, multichannel selling (Instagram/TikTok/Google/Amazon), a REST v3 API (app.ecwid.com/api/v3/{storeId}, Bearer secret_/public_ tokens, 600 req/min), and HMAC-signed webhooks. Use when adding a store to a site you already run instead of replatforming, Ecwid webhook signature verification keeps failing (it uses client_secret, not your secret_ token), the free plan's 10-product cap or paid-plan-only API blocks you, product pages load slowly, syncing Ecwid orders into a CRM or warehouse via API/webhooks, QuickBooks inventory won't sync back, or comparing plans after recent price changes. Do NOT use for choosing between store builders or checkout optimization strategy (use /sales-checkout) or full-store platforms like Shopify (use /sales-shopify)."
argument-hint: "[describe what you need help with in Ecwid]"
license: MIT
version: 1.0.0
tags: [sales, checkout, ecommerce, platform]
github: "https://github.com/Ecwid"
---

# Ecwid Platform Help

Ecwid (by Lightspeed) is embeddable ecommerce: a widget that adds a full store — catalog, cart, checkout — to any site you already run, plus a hosted Instant Site. 0% platform transaction fees; automation via a REST v3 API and HMAC-signed webhooks. The core fit: adding commerce to an existing site instead of replatforming.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer from the user's prompt:

1. **What are you trying to do?**
   - A) Embed/add an Ecwid store to an existing site (WordPress/Wix/custom)
   - B) Integrate Ecwid data (orders/products/customers) with a CRM, warehouse, or your app
   - C) Set up or debug webhooks / signature verification
   - D) Decide on a plan (Free/Starter/Venture/Business/Unlimited) or understand limits
   - E) Fix a storefront problem (speed, customization, sync)

2. **Plan tier?** API access requires a paid plan; variations and digital goods are plan-gated — most "why can't I do X" questions are plan questions.

Skip-ahead rule: if the user's prompt already has enough context, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| Which store/checkout platform to pick (Ecwid vs Shopify/Square Online/Snipcart) | `/sales-checkout {question}` |
| Full-store Shopify questions | `/sales-shopify {question}` |
| Checkout-conversion strategy (bumps, upsells, cart abandonment) across tools | `/sales-checkout {question}` |
| Selling digital downloads strategy | `/sales-digital-products {question}` |
| Tax / Merchant-of-Record obligations | `/sales-merchant-of-record {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-checkout {original question}`"

Otherwise, answer Ecwid-specific questions directly using Step 3.

## Step 3 — Ecwid platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface, pricing/plan gates, data model, and quick-start recipes (paginated order sync, signed webhook listener, bulk price update).

For raw auth detail, token types, rate limits, webhook events, and the signature algorithm, read `references/ecwid-api-reference.md`.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **When the user already runs a site (WordPress/Wix/custom), lead with the fit**: Ecwid's embed model adds the store to the site they have — no replatforming, keep existing SEO/pages — before diving into plans or config. That framing is the reason to choose Ecwid at all.
- **The webhook signing key is the app's `client_secret`, not the `secret_*` access token.** Nearly every "signature never matches" report is this mix-up — the docs bold it themselves.
- **Webhook payloads are thin by design** — an ID and event type. Re-fetch the entity via the REST API before acting; never treat the payload as the data.
- **Check the plan gate before debugging.** No API on Free; variations and digital products are paid features. A 403 on a correct call is often a plan issue, not a code issue.
- **Honor `Retry-After` on 429** — 600 req/min per token; use the Batch API for bulk writes.
- **Present plan pricing as best-effort and tell the user to verify at ecwid.com/pricing** — prices changed in March 2026 and have risen repeatedly since the Lightspeed acquisition.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — review these, especially plan pricing (changed 2026-03-02) and EU-compliance status.*

- **Signature verification footgun**: HMAC-SHA256 of `{eventCreated}.{eventId}` keyed with **`client_secret`** (from app registration), Base64-encoded, in `X-Ecwid-Webhook-Signature`. Using the `secret_*` token as the key fails every time.
- **API is paid-plan-only** — a Free-plan store can't use the REST API at all; budget the plan cost into any integration.
- **Post-acquisition pricing drift** — repeated price increases and the narrowed free tier are the top review complaints; re-verify plan features before recommending a tier.
- **Cancellation friction** — reviewers report a 10+-click cancellation flow, immediate cutoff, and no prorating; advise users to time cancellations to the end of the billing period.
- **Storefront speed** — product pages 4s+ in reviews; the embedded widget adds JS weight to the host page. Mitigate with lightweight host themes and fewer apps; don't promise Core-Web-Vitals miracles.
- **QuickBooks sync is one-way** — sales flow to QuickBooks, but QuickBooks inventory changes do NOT flow back into Ecwid.
- **EU B2B e-invoicing (mandatory from Sept 2026)** — reviewers report Ecwid has no readiness plan; EU B2B sellers should verify compliance status before committing.

## Related skills

- `/sales-checkout` — Checkout strategy and store/cart platform selection (Ecwid vs Shopify vs Square Online vs Snipcart)
- `/sales-shopify` — Shopify platform help (the replatform alternative when you outgrow embedded commerce)
- `/sales-square-online` — Square Online platform help (the free-tier competitor with unified in-person inventory)
- `/sales-digital-products` — Selling digital downloads (Ecwid digital goods are Venture+)
- `/sales-merchant-of-record` — Tax/VAT handling (Ecwid is not a Merchant of Record)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Webhook signatures never match (developer/automation)
**User says**: "My Ecwid webhook handler rejects every request — the X-Ecwid-Webhook-Signature never matches my computed HMAC."
**Skill does**: Identifies the classic key mix-up — the signature is Base64(HMAC-SHA256(`{eventCreated}.{eventId}`, `client_secret`)), where `client_secret` is the value issued at app registration, NOT the `secret_*` access token — and provides the verified Python/PHP listener from the platform guide, plus the thin-payload re-fetch pattern.
**Result**: Verification passes and the handler re-fetches full order data via the REST API.

### Example 2: Add a store to an existing site
**User says**: "I have a WordPress site that ranks well — can I add a store without rebuilding on Shopify?"
**Skill does**: Explains Ecwid's embed model (widget on existing pages, catalog/checkout hosted by Ecwid, 0% platform fees), maps plan gates to their catalog size (10 free / 100 Venture / 2,500 Business), flags the JS-weight speed trade-off, and contrasts with Snipcart (dev-first JS cart) and Shopify Buy Button for the same job via `/sales-checkout`.
**Result**: User embeds commerce on the site they already rank with, on the right plan tier.

### Example 3: Plan decision after the price changes
**User says**: "Which Ecwid plan do I need to sell 40 digital products and use the API?"
**Skill does**: Maps requirements to gates — digital goods need Venture+, API needs any paid plan, 40 products fit Venture's 100-product cap (~$29/mo annual) — and flags all pricing as best-effort post-2026-03 changes, pointing to ecwid.com/pricing to confirm.
**Result**: User picks Venture with verified current pricing.

## Troubleshooting

### Webhook signature verification always fails
**Symptom**: Computed HMAC never equals `X-Ecwid-Webhook-Signature`.
**Cause**: Wrong key (used the `secret_*` access token instead of the app's `client_secret`), wrong message (must be `{eventCreated}.{eventId}` with a dot), or missing Base64 encoding of the digest.
**Solution**: Key with `client_secret` from app registration, encode HMAC-SHA256 output as Base64, compare constant-time. Use the recipe in `references/platform-guide.md`.

### API calls return 403 even with a valid token
**Symptom**: Correct Bearer token, but calls are rejected.
**Cause**: Store is on the Free plan (no API access), or the token lacks the required access scope (`read_orders`, `read_catalog`, …), or a `public_*` token was used for a privileged operation.
**Solution**: Upgrade to a paid plan, check the app's scopes, and use the `secret_*` token server-side (never in the browser).

### Store pages load slowly
**Symptom**: Product pages take 4+ seconds; Core Web Vitals suffer.
**Cause**: The embedded widget loads Ecwid's JS bundle on top of the host page; heavy host themes and many App Market apps compound it.
**Solution**: Slim the host page (defer non-critical JS, lightweight theme), remove unused Ecwid apps, use the Instant Site for landing-speed-critical campaigns, and set expectations — an embedded widget won't match a static product page.
