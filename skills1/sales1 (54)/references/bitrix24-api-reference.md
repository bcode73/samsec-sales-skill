<!-- Source: https://apidocs.bitrix24.com (local-integrations/local-webhooks.html, api-reference/crm/deals/crm-deal-add.html) and bitrix24.com/features (fetched 2026-06). Verbatim from the official REST API docs. -->

# Bitrix24 REST API Reference

## Shape of the API

Bitrix24's API is **method-based RPC over REST** (not resource/path REST). You call named methods like `crm.deal.add`, `crm.lead.list`, `crm.contact.get` and pass params. It runs on **your portal** (cloud `{portal}.bitrix24.com` or self-hosted on-prem). There's also an **MCP server** for AI tools and a 740+ app **Market**.

## Authentication — pick one

**1. Inbound webhook** (single account you control — simplest):
A static URL with an embedded secret code, **no expiry**. Create at **Applications → Developer resources → "Ready-made scenarios" tab → Other → Incoming webhook**; rename it, pick methods via the request generator, **set access-permission scopes** (CRM, tasks, …), test with Execute. Keep the code secret.

URL pattern (verbatim):

```
https://{portal}.bitrix24.com/rest/{user_id}/{webhook_code}/{method}.json?parameters
```

- `{user_id}` — the webhook creator's id
- `{webhook_code}` — secret authorization code
- `{method}` — e.g. `crm.contact.get`
- `.json` — optional (default format)

Example call:

```
https://yourportal.bitrix24.com/rest/1/173glortu42lvpju/crm.contact.get.json?ID=42
```

**2. OAuth 2.0** (multi-tenant / marketplace apps, or apps with UI):
Use OAuth for a **local application** (Developer resources → Other → Local application) or a Market app — anything multi-account. OAuth tokens **expire** (refresh required); webhooks don't.

> Use a **webhook** for "my own portal automation"; use **OAuth** for "an app other portals install."

## Calling methods

GET or POST; params appended/sent as JSON. POST example (`crm.deal.add`):

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"FIELDS":{"TITLE":"New Deal #1","STAGE_ID":"PREPARATION","CATEGORY_ID":0,"CURRENCY_ID":"EUR","OPPORTUNITY":1000000,"CONTACT_IDS":[84,83],"ASSIGNED_BY_ID":1},"PARAMS":{"REGISTER_SONET_EVENT":"N"}}' \
  https://yourportal.bitrix24.com/rest/1/{webhook_code}/crm.deal.add
```

**Response shape** (verbatim):

```json
{
  "result": 394,
  "time": { "start": 1725013197.6, "finish": 1725013198.6, "duration": 0.945,
            "date_start": "2024-08-30T12:19:57+02:00", "date_finish": "2024-08-30T12:19:58+02:00" }
}
```

`result` holds the return value (e.g. the new deal's ID). Errors return `{"error": "...", "error_description": "..."}`.

## Core CRM methods

Each CRM entity follows a consistent verb set: `*.add`, `*.update`, `*.get`, `*.list`, `*.delete`, `*.fields`.

- **Leads:** `crm.lead.add` / `.list` / `.get` / `.update` / `.delete`
- **Deals:** `crm.deal.add` / `.list` / `.get` / `.update` / `.delete` (+ `crm.deal.contact.items.*`, `crm.dealcategory.*` for pipelines)
- **Contacts:** `crm.contact.*` · **Companies:** `crm.company.*`
- **Activities, products, statuses (stages), currencies:** `crm.activity.*`, `crm.product.*`, `crm.status.*`, `crm.currency.*`
- **Smart Process Automation (custom CRM objects):** `crm.item.*` with an `entityTypeId`

### `crm.deal.add` — key `FIELDS`

`TITLE` (string), `CATEGORY_ID` (**pipeline/funnel id**, ≥0), `STAGE_ID` (`crm_status`), `TYPE_ID`, `CURRENCY_ID`, `OPPORTUNITY` (amount, double), `CONTACT_IDS` (array), `COMPANY_ID`, `CLOSEDATE` (date), `ASSIGNED_BY_ID` (user), `SOURCE_ID`, `PROBABILITY` (%), `IS_RECURRING` (Y/N), `COMMENTS`. `PARAMS.REGISTER_SONET_EVENT` (Y/N) controls activity-stream logging.

### `crm.lead.add`

Same pattern with lead fields (`TITLE`, `NAME`, `STATUS_ID`, `OPPORTUNITY`, `ASSIGNED_BY_ID`, `SOURCE_ID`, plus multi-fields `PHONE`/`EMAIL` as arrays of `{VALUE, VALUE_TYPE}`).

## Listing & batching

- `*.list` supports `filter`, `order`, `select`, and **pagination via `start`** (returns 50 rows/page; response includes `next` + `total`). For large pulls, page with `start=50,100,…` or use the **`crm.item.list`** keyset where available.
- **`batch`** — run up to **50 commands in one request** (and reference earlier results with `$result[...]`) to cut round-trips and stay under rate limits.

## Outbound webhooks (events)

Create at **Developer resources → Other → Outgoing webhook**: name it, give your **handler URL**, pick the **triggering event** (e.g. `ONCRMDEALADD`, `ONCRMDEALUPDATE`, `ONCRMLEADADD`), and Bitrix24 fires a POST when that data changes. An **application token** is generated for verification — check it on each delivery. Event payload (verbatim shape):

```json
{ "event": "ONCRMDEALUPDATE", "data": { "FIELDS": { "ID": 662 } } }
```

Note the payload carries the **entity ID**, not the full record — call `crm.deal.get` to fetch current data. (On-prem outbound webhooks need an active license.)

## Limits & gotchas

- **Rate limits:** Bitrix24 enforces request throttling (a per-method "operating time"/leaky-bucket limit, ~2 req/sec sustained on cloud) — batch and back off on errors.
- **Some methods are unavailable to webhooks** (certain application-only operations, telephony, some chatbot events) — those need an OAuth app.
- Cloud vs **on-prem (Bitrix24 Self-Hosted)** differ slightly; on-prem unlocks source/extra control but you host it.
- Full method catalog + per-method docs: **`https://apidocs.bitrix24.com`**.
