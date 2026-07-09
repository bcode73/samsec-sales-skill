---
name: sales-funnelkit
description: "FunnelKit (funnelkit.com, formerly WooFunnels/Autonami) platform help — WordPress/WooCommerce sales-funnel builder + built-in CRM/marketing-automation suite: checkout, order bumps, one-click upsells/downsells, A/B testing, sliding cart, plus FunnelKit Automations (email/SMS, contact segments, broadcasts, cart-abandonment recovery). Developer surface: FunnelKit Automations REST API (`/wp-json/funnelkit-automations/`, api_key query param) with Tags/Lists/Fields/Contacts CRUD + incoming/outgoing webhooks, and WooCommerce order hooks/REST for funnel revenue. Use when adding or segmenting contacts via the API, wiring incoming/outgoing webhooks, building one-click upsells or order bumps, recovering abandoned carts, reading funnel revenue via WooCommerce, or choosing Funnel Builder vs Automations vs the bundles. Do NOT use for funnel/CRO strategy across tools (use /sales-funnel), checkout-conversion strategy (use /sales-checkout), or generic iPaaS wiring (use /sales-integration)."
argument-hint: "[describe what you need help with in FunnelKit]"
license: MIT
version: 1.0.0
tags: [sales, funnel, wordpress, platform]
github: "https://github.com/funnelkit"
---

# FunnelKit Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Add/update/segment contacts (tags, lists, fields, status) via the Automations REST API
   - B) Wire incoming/outgoing webhooks (receive external events → automation; or send data out)
   - C) Build the funnel — checkout, order bumps, one-click upsells/downsells, A/B testing, sliding cart
   - D) Recover abandoned carts / run email-SMS automations (FunnelKit Automations)
   - E) Read funnel revenue/orders programmatically (via WooCommerce)
   - F) Decide Funnel Builder vs Automations vs a bundle, or Free vs Pro

2. **Which side?** Contacts/email/SMS/automation → **FunnelKit Automations** (REST API + webhooks). Checkout/upsells → **Funnel Builder** (WooCommerce orders).

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Funnel / CRO **strategy** across tools (which builder, funnel design) | `/sales-funnel {question}` |
| Checkout/cart **conversion** strategy across platforms | `/sales-checkout {question}` |
| Connecting FunnelKit to a CRM/ESP generically (iPaaS) | `/sales-integration {question}` |
| Email/SMS sequence **strategy** beyond FunnelKit Automations | `/sales-email-marketing {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-funnel design a post-purchase upsell flow`".

## Step 3 — FunnelKit platform reference

**Read `references/platform-guide.md`** for the full reference — the two-product model (Funnel Builder vs Automations), what's REST-API vs WooCommerce vs UI-only, best-effort pricing/bundles, the contact data model, and quick-start recipes (add+segment a contact; receive an incoming webhook; read orders via WooCommerce).

**Read `references/funnelkit-api-reference.md`** for the integration surface — **FunnelKit Automations REST API** (base `/wp-json/funnelkit-automations/`, **`?api_key=` query-param** auth from Settings → REST API; Tags/Lists/Fields/Contacts CRUD, offset pagination, `{code,data,limit,offset}` responses), **incoming + outgoing webhooks**, and **WooCommerce** order hooks/REST for funnel revenue.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Two products, two surfaces.** **Automations** (CRM/email/SMS) has the **REST API + webhooks**; the **Funnel Builder** (checkout/upsells) rides on **WooCommerce** — read its revenue via the **WooCommerce REST API**, not a FunnelKit endpoint.
- **The API key is a query param.** Auth is `?api_key=...` (from Automations **Settings → REST API**) — not a header. Keep URLs out of logs/referrers and call server-side.
- **Contacts are tag/list-driven.** Create with `POST /contact/add`, then `tag-assign`/`list-assign` to segment — automations trigger off tags/lists/status. Status is `subscribed|bounced|unsubscribed|verified`.
- **Webhooks go both ways.** Use the **incoming Webhook URL** to feed external events into an automation; use the **HTTP Request** action for **outgoing** webhooks. Treat the incoming URL as a secret and capture a live payload (schema isn't fully published).
- **AOV is the funnel job.** Rule-based **order bumps** + **one-click upsells/downsells** (post-purchase, charged to the original WooCommerce order) + **sliding cart** are the revenue levers; A/B test the offers.
- **It's WordPress-only.** No hosted SaaS/MCP; you need a self-hosted WordPress + WooCommerce site. Free version exists; advanced funnel + Automations features are Pro/bundle-gated (best-effort pricing — verify).

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — pricing/feature specifics verified against the marketing site, developer docs, and comparison articles; confirm in-account.*

1. **API is the Automations side only.** `/wp-json/funnelkit-automations/` manages **contacts/tags/lists/fields** — there's **no funnel-builder read API**; funnel orders/revenue come from **WooCommerce**.
2. **`?api_key=` is a query param.** Not a header — it can leak via logs/referrers; keep calls server-side and rotate the key if exposed.
3. **WordPress + WooCommerce required.** No hosted API/MCP; everything runs on your self-hosted site, and commerce needs WooCommerce.
4. **Webhook payloads aren't fully documented.** The overview lists incoming/outgoing + conditions but not full schemas/signatures — capture a live delivery and treat the incoming URL as secret.
5. **Two products + bundles.** Funnel Builder and Automations are separate (each Free + Pro); bundles (Plus/Professional/Elite) gate which you get. Price the **bundle**, not just one plugin (best-effort ~$99.50–$399/yr).
6. **One-click upsells need gateway support.** Post-purchase one-click charges require a compatible WooCommerce gateway (Stripe/PayPal/etc.).
7. **Formerly WooFunnels/Autonami.** Old docs/threads use those names — "Autonami" = FunnelKit Automations.

## Related skills

- `/sales-funnel` — Sales-funnel / CRO strategy across tools (FunnelKit is one of the WordPress funnel builders covered) — funnel design, tool selection vs CartFlows/WPFunnels
- `/sales-checkout` — Checkout/cart conversion (order bumps, one-click upsells, AOV) across platforms
- `/sales-email-marketing` — Email/SMS sequence strategy beyond FunnelKit Automations
- `/sales-integration` — Connecting FunnelKit to a CRM/ESP via REST API/webhooks/Zapier/WooCommerce
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Add and segment a contact via the Automations API (developer/automation)
**User says**: "When someone buys in my app, how do I add them to FunnelKit Automations and tag them via the API?"
**Skill does**: Walks Recipe 1 — `POST /wp-json/funnelkit-automations/contact/add?api_key=...` with the email/name, then `POST /contact/tag-assign/{contact_id}` with `{"tags":[id]}` (and `list-assign` for a list). Notes the **api_key query-param** auth (Settings → REST API), the `{code,data,limit,offset}` response, status values, and that tags/lists are what trigger automations. Flags keeping the key server-side.
**Result**: Buyers land in Automations correctly tagged, ready to trigger a flow.

### Example 2: Receive an external event via incoming webhook
**User says**: "My payment processor should add a contact to a FunnelKit automation when a subscription renews."
**Skill does**: Explains the **incoming Webhook URL** (set up a webhook-triggered automation in FunnelKit Automations), plug that URL into the processor, and use **Conditions** to branch on the payload; the automation can then add/tag the contact and send email/SMS. Notes the payload schema isn't fully published (capture a live delivery) and to treat the URL as secret. Offers Zapier as a no-code alternative.
**Result**: Renewals drive a FunnelKit automation in real time.

### Example 3: Funnel Builder vs Automations vs a bundle — what do I buy?
**User says**: "Do I need FunnelKit Funnel Builder, Automations, or both?"
**Skill does**: Distinguishes **Funnel Builder** (checkout, order bumps, one-click upsells, A/B testing — the AOV/checkout layer) from **Automations** (CRM, email/SMS, cart-abandonment, segments — the marketing layer), notes each has Free + Pro and that **bundles (Plus/Professional/Elite)** combine them. Recommends both for a full WooCommerce funnel + recovery stack; frames pricing as best-effort (~$99.50–$399/yr) and routes tool-selection vs CartFlows/WPFunnels to `/sales-funnel`.
**Result**: User buys the right combination for their stack.

## Troubleshooting

### My API calls return 401/403
**Symptom**: Requests to `/wp-json/funnelkit-automations/...` are rejected.
**Cause**: Missing/invalid **`api_key`** query param, or the key wasn't generated/enabled in Automations **Settings → REST API**.
**Solution**: Generate the key in Automations → Settings → REST API, append `?api_key={key}` to every request (it's a query param, not a header), and use HTTPS. Confirm the base path is `/wp-json/funnelkit-automations/` on your site. 403 can also mean a security plugin/host is blocking the REST route.

### I can't find an API to read my funnel's orders/upsells
**Symptom**: Looking for a FunnelKit endpoint for funnel revenue.
**Cause**: The REST API is the **Automations** (contacts) side; the Funnel Builder runs on **WooCommerce orders** and has no separate read API.
**Solution**: Read order bumps + one-click upsells as **WooCommerce orders** via the **WooCommerce REST API** (`/wp-json/wc/v3/orders`) or WooCommerce order webhooks. Use FunnelKit Automations' API/webhooks for the contact/marketing side.

### My one-click upsell isn't charging
**Symptom**: Post-purchase upsell doesn't complete the charge.
**Cause**: One-click upsells require a **WooCommerce payment gateway that supports post-purchase charges** (e.g. Stripe/PayPal as integrated by FunnelKit); not all gateways qualify.
**Solution**: Use a supported gateway, confirm FunnelKit Funnel Builder Pro is active, rebuild the upsell step, and test a full checkout. For AOV strategy across tools, use `/sales-checkout`.
