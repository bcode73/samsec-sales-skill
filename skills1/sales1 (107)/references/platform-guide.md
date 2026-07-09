# ClickFunnels Platform Reference

## Overview

ClickFunnels (clickfunnels.com) is the platform that popularized the "sales funnel" category — an all-in-one for entrepreneurs, creators, coaches, and small businesses to build, sell, and deliver online without a dev team. The current product is **ClickFunnels 2.0** (a full rebuild with the V2 REST API); **Classic (1.0)** is legacy with a deprecated V1 API. It organizes everything around the "Funnel Mindset": **Attract → Sell → Upsell → Ascend → Repeat**. Closest peers: GoHighLevel, Kartra, Systeme.io, Groove. Trade-offs: it's among the highest-priced funnel builders, bills email per-send, and 2.0 still draws stability complaints.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **Funnels + Pages** | Drag-and-drop funnel/page builder (PML markup), split tests, conditional splits, stats | **API-accessible** (funnels, pages, split_test_steps); external SDK pages |
| **Contacts / CRM** | Contact records, tags, opportunities, sales pipelines | **API-accessible** (contacts, upsert, applied_tags, sales_pipelines, sales_opportunities) + webhooks; GDPR "Redact Contact" |
| **E-commerce / Products** | Products, variants, prices, stores, shipping | **API-accessible** (products/variants/prices, stores, shipping_*) |
| **Checkout** | Order forms, one-click upsells/downsells, order bumps | Build **UI-only**; resulting orders/transactions **API-accessible** |
| **Orders / Subscriptions** | Orders, invoices, transactions, subscription changes | **API-accessible** (orders, invoices, transactions, line_item changes) + webhooks |
| **Email + Workflows** | Broadcasts, automation Workflows, templates, topics | Broadcasts/templates **API-accessible**; Workflow build **UI-only** |
| **Courses** | Courses, sections, lessons, enrollments, completions | **API-accessible** (courses read; enrollments/completions write) |
| **Forms** | Forms, field sets, fields, submissions | **API-accessible** (forms, submissions, answers) |
| **Backpack (affiliates)** | Native affiliate-program management | **UI-only** (no public affiliate API surface) |
| **Blogs** | Blog + posts + tags | **API-accessible** (blogs, posts) |
| **Webhooks** | Outbound signed event notifications | **API-accessible** (webhook_endpoints, webhook_events) |

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify against clickfunnels.com/pricing; ClickFunnels has repriced and renamed plans repeatedly (Startup/Pro and Launch/Scale/Optimize/Dominate naming both circulate).*

| Plan | Price | Highlights |
|---|---|---|
| **Startup** | ~$97/mo (~$81 annual) | 3 workspaces, 20 funnels, 100 pages, 10,000 contacts, 3 courses, CRM, Workflows, A/B testing, checkout/upsells, 1 seat |
| **Pro** | ~$297/mo (~$248 annual) | Unlimited funnels/pages/contacts/courses, 5 workspaces, Backpack affiliates, advanced analytics, **API access**, 5 seats |

**Notes for integrators:**
- **API access is plan-gated** — the higher tier (Pro, or Scale/Optimize/Dominate in other plan generations). Verify before building; an entry-plan account can't call the API.
- **Per-send email pricing** — ClickFunnels charges per email send, so cost scales with list size and send frequency (a top cost complaint). Run the math before importing a large list.
- **No bulk contact import** in 2.0 has been a long-standing gap — the API is the practical bulk path.
- **14-day free trial**; no free plan.

## Integrations

- **V2 REST API** — base `https://{workspace}.myclickfunnels.com/api/v2` (workspace data) and `https://accounts.myclickfunnels.com/api/v2` (team/workspace lookups). Bearer token + required `User-Agent`, or OAuth 2.0 for public apps.
- **Webhooks** — signed outbound events (contact, order, subscription, funnel). Register `webhook_endpoints`.
- **iPaaS** — Zapier, Make (ClickFunnels 2.0 app), Pabbly, APIX-Drive.
- **Direction of flow:** external → ClickFunnels via `contacts`/`orders`/`products` writes; ClickFunnels → external via signed webhooks.

## Data model

Resources are workspace-scoped. URLs expose a `public_id`; **payloads use the internal `id`**. Use `expand[]` to inline nested resources.

**Contact**:
```json
<!-- Constructed from documented fields — verify against live API -->
{
  "id": "abc123",
  "public_id": "cont_9f3c",
  "email": "jane@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "time_zone": "America/New_York",
  "tags": [ { "id": "tag_88", "name": "app-trial" } ]
}
```

**Order**:
```json
<!-- Constructed from documented fields — verify against live API -->
{
  "id": "ord_5521",
  "contact_id": "abc123",
  "total": "297.00",
  "currency": "USD",
  "financial_state": "paid",
  "line_items": [ { "product_id": "prod_12", "price_id": "price_3", "quantity": 1 } ],
  "created_at": "2026-06-21T14:05:00Z"
}
```

**Cursor-paginated list response** (shape):
```json
<!-- Constructed from documented pagination behavior — verify against live API -->
{
  "data": [ { "id": "abc123", "email": "jane@example.com" } ],
  "meta": { "pagination": { "next_cursor": "eyJpZCI6..." , "has_more": true } }
}
```

## Quick-start recipes

> Two base URLs: `accounts.myclickfunnels.com/api/v2` for `teams`/`workspaces` lookups, then `{workspace}.myclickfunnels.com/api/v2` for workspace data. Every request needs `Authorization: Bearer {token}` **and** a `User-Agent` header. See `references/clickfunnels-api-reference.md`.

### Recipe 1 — Bootstrap, then upsert + tag a contact
Use when an app signup should become a ClickFunnels contact.

**Python**:
```python
import requests

ACCOUNTS = "https://accounts.myclickfunnels.com/api/v2"
H = {"Authorization": f"Bearer {TOKEN}", "User-Agent": "MyApp/MyOrg",
     "Content-Type": "application/json"}

# 1) Discover team + workspace (do once, cache the ids)
team = requests.get(f"{ACCOUNTS}/teams", headers=H).json()["data"][0]
ws = requests.get(f"{ACCOUNTS}/teams/{team['id']}/workspaces", headers=H).json()["data"][0]
WS = f"https://{ws['subdomain']}.myclickfunnels.com/api/v2"

# 2) Upsert contact by email, then tag
c = requests.post(f"{WS}/contacts/upsert", headers=H,
                  json={"contact": {"email": "jane@example.com", "first_name": "Jane"}}).json()["data"]
requests.post(f"{WS}/contacts/{c['id']}/applied_tags", headers=H,
              json={"applied_tag": {"tag_id": TAG_ID}})
```
**Gotchas:** the `User-Agent` header is **required**; use the internal `id` (not `public_id`) in payloads; API access needs the Pro tier; cache the team/workspace ids so you don't re-fetch them every call.

### Recipe 2 — React to a new order via signed webhook (no polling)
Register an endpoint subscribed to the order-created event, then verify the signature.

**Register**:
```bash
curl -X POST "https://{workspace}.myclickfunnels.com/api/v2/workspaces/{id}/webhook_endpoints" \
  -H "Authorization: Bearer $TOKEN" -H "User-Agent: MyApp/MyOrg" \
  -H "Content-Type: application/json" \
  -d '{"webhook_endpoint":{"url":"https://yourapp.com/hooks/cf","event_type_ids":["order.created"]}}'
```

**Flask listener**:
```python
from flask import Flask, request, abort
app = Flask(__name__)
seen = set()

@app.post("/hooks/cf")
def cf_hook():
    # verify the signature header against your endpoint secret before trusting the body
    if not verify_signature(request.headers, request.get_data()):
        abort(401)
    evt = request.json or {}
    eid = evt.get("id")
    if eid in seen:            # at-least-once delivery — dedupe
        return "", 200
    seen.add(eid)
    # ... fulfill / write to CRM / notify ...
    return "", 200            # respond 2xx fast; do slow work async
```
**Gotchas:** always verify the webhook signature; respond `2xx` quickly; dedupe on the event id; the exact event-type ids and payload keys come from the webhook-events docs — log a sample first.

### Recipe 3 — Export all contacts (cursor pagination)
Loop on the cursor until `has_more` is false.

```python
def all_contacts(WS, H):
    params = {"per_page": 100}
    while True:
        r = requests.get(f"{WS}/workspaces/{WS_ID}/contacts", headers=H, params=params)
        if r.status_code == 429:
            time.sleep(2); continue
        body = r.json()
        yield from body["data"]
        page = body.get("meta", {}).get("pagination", {})
        if not page.get("has_more"):
            break
        params["cursor"] = page["next_cursor"]
```
**Gotchas:** the API supports both cursor and offset paging — cursor is safest for large/changing sets. Use `expand[]` to inline related records and `filter[...]` for server-side filtering instead of pulling everything.

## Integration patterns

- **CRM sync (ClickFunnels → CRM/warehouse):** prefer signed webhooks (order.created, contact.created, subscription.*) for real-time; reserve cursor-paginated `GET` for backfills. Join on `email`.
- **CRM sync (external → ClickFunnels):** `POST /contacts/upsert` (by email) then `applied_tags` to drive Workflows; `POST /orders` to record external sales.
- **Bootstrap once:** resolve `team` → `workspace` ids and cache them; all workspace resources hang off the `{workspace}` subdomain.
- **Rate-limit handling:** limits apply per workspace/user — back off on `429`, page with the cursor, request only needed fields/`expand[]`, and avoid tight polling loops (use webhooks).
