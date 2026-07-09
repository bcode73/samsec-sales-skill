---
name: sales-sendowl
description: "SendOwl platform help — sell and securely deliver digital products (ebooks, software, audio, video, courses) with download-link protection, PDF stamping, license keys, drip, subscriptions, and upsells, plus a REST API (Basic Auth) and HMAC-signed webhooks. Use when SendOwl download links are being shared and you need expiring/limited links, verifying the X-SENDOWL-HMAC-SHA256 webhook signature, syncing SendOwl orders to a CRM or spreadsheet via the API, issuing or checking software license keys, setting up subscriptions or drip content, the order_completed webhook isn't firing, or weighing SendOwl's plan tiers and recent price changes against Gumroad/Payhip/Lemon Squeezy. Do NOT use for choosing between digital-product platforms in general (use /sales-digital-products) or checkout-conversion strategy across carts (use /sales-checkout)."
argument-hint: "[describe what you need help with in SendOwl]"
license: MIT
version: 1.0.0
tags: [sales, digital-products, platform]
github: "https://github.com/SendOwl"
---

# SendOwl Platform Help

SendOwl sells and securely delivers digital products — download links with expiry/limits, PDF stamping, license keys, drip content, subscriptions, bundles, and upsells — with a REST API and HMAC-signed webhooks.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer from the user's message:

1. **What are you trying to do?**
   - A) Stop customers from sharing download links / tighten delivery security
   - B) Build an API or webhook integration (sync orders to a CRM, warehouse, Slack, or your own app)
   - C) Set up products, subscriptions, drip, license keys, or upsells
   - D) Compare SendOwl plans/pricing to alternatives, or weigh a price change
   - E) Troubleshoot a broken flow (webhook not firing, email not sending, file not delivering)

2. **Are you connecting SendOwl to another tool?** Which one, and which direction should data flow?

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

Map the request to the right home. When routing, give the exact command.

| The user's need | Route to |
|-----------------|----------|
| "Which platform should I sell on — SendOwl, Gumroad, Payhip?" | `/sales-digital-products {question}` |
| Checkout-conversion strategy (order bumps, upsells, cart abandonment) across carts | `/sales-checkout {question}` |
| VAT/GST/sales-tax handling for global sales (SendOwl is **not** a merchant of record) | `/sales-merchant-of-record {question}` |
| Pricing/packaging strategy for the product itself | `/sales-digital-products {question}` |
| Recurring-access / course-membership strategy | `/sales-membership {question}` |
| Wiring SendOwl events into other tools via an iPaaS | `/sales-integration {question}` |

If it's a SendOwl setup, API, webhook, delivery-security, or pricing question, answer it here using Step 3.

## Step 3 — SendOwl platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities and automation surface, pricing/plan gates, data model, integration recipes (order→CRM sync, webhook listener, license issuing), and code examples.

For raw endpoint details, request/response JSON, auth, pagination, and the webhook payload schema, **read `references/sendowl-api-reference.md`**.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

You no longer need the platform guide — focus on the user's situation.

- **Delivery security first**: for shared-link complaints, layer defenses — set download-limit + link-expiry on the product, turn on PDF stamping for ebooks, and issue license keys for software. No single control stops sharing alone.
- **Trust webhooks over polling** for order events, but always verify the `X-SENDOWL-HMAC-SHA256` signature against the raw request body before acting, and make handlers idempotent (retries send duplicates).
- **Respect the rate limit**: ~1 request/second or the IP can be blocked. For bulk exports, page with `per_page=50` and sleep between calls; contact support for higher throughput.
- **Read the order state from the payload, the event from the header** — SendOwl sends the order's current state in the body and the trigger in `X-SENDOWL-EVENT`.
- **Model annual sales/orders, not just features** — plans cap orders/year and sales/year; crossing a cap forces an upgrade.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — review these, especially plan-gated features and pricing that may be outdated.*

- **SendOwl hosts links, not files** — it stores download links (historically capped around 250 files), not unlimited raw file hosting. For large media libraries, host the file elsewhere (S3/Bunny/Cloudflare) and deliver the link through SendOwl.
- **Download protection is a deterrent, not a lock** — expiring/limited links + PDF stamping + license keys reduce casual sharing but don't stop a determined re-uploader. Gate high-value access off the `order_completed` webhook in your own app.
- **Webhooks POST raw JSON (order "Liquid"), not form params** — read the raw request body to parse it, and compute the HMAC over that exact raw body.
- **Rails header renaming** — the signature arrives as `HTTP_X_SENDOWL_HMAC_SHA256`, not `X_SENDOWL_HMAC_SHA256`.
- **Version-split paths** — most resources are `/api/v1/...` but orders live at `/api/v1_3/orders`; mixing versions returns unexpected results.
- **Abrupt repricing risk** — reviewers report large, short-notice price increases. Keep an export/migration path ready and don't hard-code a single-vendor dependency.
- **`check_valid` license endpoint leaks credentials if embedded** — never call it from shipped client software; validate server-side.

## Related skills

- `/sales-digital-products` — Digital product strategy: pricing, launch, delivery, and platform selection across tools. Install: `npx skills add sales-skills/sales --skill sales-digital-products -a claude-code`
- `/sales-checkout` — Checkout-conversion strategy (order bumps, upsells, cart abandonment) across carts. Install: `npx skills add sales-skills/sales --skill sales-checkout -a claude-code`
- `/sales-merchant-of-record` — Global tax handling via a merchant of record (SendOwl is not one). Install: `npx skills add sales-skills/sales --skill sales-merchant-of-record -a claude-code`
- `/sales-gumroad` — Gumroad platform help (a common SendOwl alternative). Install: `npx skills add sales-skills/sales --skill sales-gumroad -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Customers are sharing my download link
**User says**: "People are passing around the download link to my $49 course PDF — how do I lock it down in SendOwl?"
**Skill does**: Explains layering — set a download limit and link expiry on the product, enable PDF stamping so each copy carries the buyer's name/email, and (for software) issue license keys. Notes that true access-gating means validating the `order_completed` webhook in the user's own app, since links can still be re-shared.
**Result**: User applies limit + expiry + stamping and understands the deterrent-vs-lock tradeoff.

### Example 2: Sync completed orders into a CRM via the API/webhook
**User says**: "How do I push every completed SendOwl sale into HubSpot automatically?"
**Skill does**: Recommends the `order_completed` webhook over polling; walks through verifying `X-SENDOWL-HMAC-SHA256` against the raw body with the signing-key secret, parsing the raw-JSON order payload (buyer name/email/country, cart items, transactions), and upserting to the CRM idempotently. Gives the polling fallback (`GET /api/v1_3/orders?updated_after=`) for reconciliation.
**Result**: User has a signed, idempotent listener plus a catch-up poller.

### Example 3: order_completed webhook isn't firing
**User says**: "My SendOwl webhook never hits my endpoint when a sale completes."
**Skill does**: Checks the webhook is enabled and the event is `Order completed` (not just `New payment`), confirms the URL returns 2XX/3XX (SendOwl retries 10× with backoff on failures), verifies HTTPS reachability, and confirms the handler reads the raw body rather than parsed form params.
**Result**: User fixes the event selection / response code and receives events.

## Troubleshooting

### Download links are being shared
**Symptom**: Buyers forward the download URL and others download for free.
**Cause**: Default links have generous or unset limits; nothing ties a link to a person.
**Solution**: Set per-product download-limit + link-expiry, enable PDF stamping (embeds buyer identity), and use license keys for software. For real gating, deliver via your own app keyed off the purchase webhook. If you reset a buyer's access, `PUT /api/v1/orders/{id}/download_restrictions`.

### Webhook signature verification keeps failing
**Symptom**: Computed HMAC never matches `X-SENDOWL-HMAC-SHA256`.
**Cause**: Hashing a re-serialized/parsed body instead of the raw request, wrong secret, or framework-renamed header.
**Solution**: Compute HMAC-SHA256 over the **raw** request body using the Signing Key Secret from the API settings page, base64-encode, and compare to the header. In Rails read `request.raw_post` and `HTTP_X_SENDOWL_HMAC_SHA256`.

### Hitting rate limits / IP blocked during export
**Symptom**: Requests start failing or the IP is blocked when pulling many orders/products.
**Cause**: Exceeding ~1 request/second.
**Solution**: Throttle to ≤1 req/sec, page with `per_page=50&page=N`, and use `updated_after` to pull only changed orders. Contact SendOwl support to request a higher limit for legitimate bulk jobs.
