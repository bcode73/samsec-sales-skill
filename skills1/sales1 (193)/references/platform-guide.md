# FunnelKit Platform Guide

Full reference for the `sales-funnelkit` skill. Read the section you need; don't dump the whole file.

> *Pricing/plan gates are best-effort from research (2026-06) — the marketing site, developer docs, and comparison articles. Verify in-account.*

## What FunnelKit is

A **WordPress/WooCommerce sales-funnel builder + built-in CRM/marketing-automation suite** (formerly **WooFunnels**; the automation plugin was **Autonami**). The leading CartFlows/WPFunnels rival, positioned as a WordPress **ClickFunnels alternative**. 40,300+ store owners; 4.9★ on WordPress.org. Two plugins:

- **FunnelKit Funnel Builder** — checkout, order bumps, one-click upsells/downsells, A/B testing, sliding cart, opt-in/sales/thank-you pages, funnel analytics.
- **FunnelKit Automations** (ex-Autonami) — CRM (rich contact profiles), email + SMS marketing, segmented broadcasts, transactional emails, cart-abandonment recovery, a workflow builder, and the **REST API + webhooks**.

Self-hosted WordPress — **no hosted SaaS/MCP**. For funnel *strategy/tool selection*, use `/sales-funnel`.

## Module map — REST API vs WooCommerce vs UI-only

| Module | Surface | Notes |
|---|---|---|
| Funnel canvas / steps | **UI-only** | build in WP admin |
| Checkout / opt-in / sales / thank-you pages | **UI (page builder)** | Divi + others |
| Order bumps | **WooCommerce (Pro)** | rule-based; WooCommerce orders |
| One-click upsell/downsell | **WooCommerce (Pro)** | post-purchase, original order |
| Sliding cart | **UI (Pro)** | recommendations/rewards/add-ons |
| A/B testing | **UI (Pro)** | split traffic across page versions |
| Contacts / tags / lists / fields | **REST API** | `/wp-json/funnelkit-automations/` |
| Segments / broadcasts / email-SMS | **Automations UI + API** | tag/list-driven |
| Cart-abandonment recovery | **Automations** | workflow recipe |
| Incoming/outgoing webhooks | **Webhook** | incoming URL + HTTP Request action |
| Order/revenue read | **WooCommerce REST/hooks** | no funnel-read API |
| Server-side customization | **WordPress hooks** | PHP actions/filters |

## Pricing & plan gates (best-effort)

- **Free** — Funnel Builder Lite and Automations Lite on WordPress.org (basic funnels, basic automations).
- **Pro** — each plugin has a Pro; **bundles** combine them:

| Bundle (typical) | Approx. price | Scope |
|---|---|---|
| **Plus** | ~$99.50/yr+ | Funnel Builder Pro + Automations basics, ~1 site |
| **Professional** | mid | more sites + full automation/CRM |
| **Elite** | ~$399/yr | up to ~30 sites, full automation + CRM stack |

- 14-day money-back guarantee. Requires **WooCommerce** + a page builder; self-hosted WordPress site. Treat exact tier names/prices as best-effort (FunnelKit restructures bundles) — verify on the pricing page. Peers: CartFlows ~$79–$449/yr, WPFunnels (free + Pro).

## Data model (contact — JSON shape)

The Automations **contact** is the core API object (email-keyed):

```json
{
  "id": 123,
  "email": "jane@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "status": "subscribed",          // subscribed | bounced | unsubscribed | verified
  "tags": [3, 7],
  "lists": [1],
  "fields": { "company": "Acme" }
}
```

- Segment via **tags** and **lists**; automations trigger off tag/list/status changes.
- API responses wrap data as `{ "code": "success", "data": {…}, "limit": 0, "offset": 0 }` (offset pagination).
- **Funnel revenue is a WooCommerce order**, not a contact field — read it via the WooCommerce REST API.

## Quick-start recipes

### Recipe 1 — Add + tag a contact via the Automations API

```bash
# 1. Create the contact (api_key is a QUERY param, from Automations → Settings → REST API)
curl -X POST "https://yoursite.com/wp-json/funnelkit-automations/contact/add?api_key=$FK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","first_name":"Jane"}'
# -> { "code":"success", "data": { "id": 123, ... } }

# 2. Tag it (tags/lists drive automations)
curl -X POST "https://yoursite.com/wp-json/funnelkit-automations/contact/tag-assign/123?api_key=$FK_API_KEY" \
  -H "Content-Type: application/json" -d '{"tags":[3]}'
```

Python:

```python
import requests
BASE = "https://yoursite.com/wp-json/funnelkit-automations"
P = {"api_key": FK_API_KEY}
c = requests.post(f"{BASE}/contact/add", params=P, json={"email": "jane@example.com", "first_name": "Jane"}).json()
cid = c["data"]["id"]
requests.post(f"{BASE}/contact/tag-assign/{cid}", params=P, json={"tags": [3]})
```

### Recipe 2 — Receive an external event (incoming webhook)

In FunnelKit Automations, create a **webhook-triggered automation** → copy its **incoming Webhook URL** → plug it into the external app (payment processor, form, etc.). Use **Conditions** to branch on the payload, then add/tag the contact and send email/SMS. The payload schema isn't fully published — capture a live delivery (webhook.site) and treat the URL as a secret. For outgoing, add an **HTTP Request** action inside an automation.

### Recipe 3 — Read funnel revenue via WooCommerce (not FunnelKit)

Order bumps + one-click upsells are **WooCommerce orders**:

```bash
curl "https://yoursite.com/wp-json/wc/v3/orders?after=2026-06-01T00:00:00" \
  -u ck_xxx:cs_xxx
```

Or subscribe to WooCommerce **order.created/updated** webhooks. This is the reliable read for funnel AOV — FunnelKit has no funnel-read REST API.

## When to route out

- Which funnel builder / funnel design across tools → `/sales-funnel`
- AOV / order-bump / upsell **strategy** across platforms → `/sales-checkout`
- Email/SMS sequence strategy beyond Automations → `/sales-email-marketing`
- Generic CRM/ESP wiring (iPaaS) → `/sales-integration`
