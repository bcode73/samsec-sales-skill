<!-- Source: https://ontraport.com/support/Integrations/use-ontraport-api + https://ontraport.com/support/Getting-started/api + https://ontraport.com/support/integrations/webhooks/ + https://ontraport.com/blog/engineering/the-new-ontraport-api/ + https://tray.ai/documentation/connectors/service/ontraport — interactive reference at https://api.ontraport.com/doc (Swagger) and live tester at https://api.ontraport.com/live -->
<!-- The official reference is an interactive Swagger UI (JS-rendered) that requires credentials and was not fetchable verbatim via WebFetch. Base URL, auth headers, the object model, pagination params, rate limit, and webhook events below are captured from the official support docs, the API announcement, and the tray.ai connector docs (which document the live API). Request/response JSON is CONSTRUCTED from documented fields and marked — verify against the live API / Swagger doc. -->

# Ontraport API Reference

Object-oriented REST API (JSON, Swagger-documented) for an Ontraport account — contacts, custom objects, transactions, tags, campaigns, and webhooks. Everything is an "object" addressed by a numeric `objectID`.

## Base URL

`https://api.ontraport.com/1`

Interactive docs: `https://api.ontraport.com/doc` (Swagger reference) and `https://api.ontraport.com/live` (enter credentials to build/test calls).

## Authentication

Two headers on **every** request:

| Header | Value |
|---|---|
| `Api-Key` | Your account API key |
| `Api-Appid` | Your application ID |

- Both are generated in **Administration → Integrations** (Ontraport API section).
- **Send them in headers only** — Ontraport explicitly warns against putting `Api-Key`/`Api-Appid` in GET query params or POST body for security.
- Keys are highly sensitive (full account data access) — Ontraport support will never ask for them.

## Auth quick-start (simplest call)

List object types to confirm credentials work:

```bash
curl -X GET "https://api.ontraport.com/1/objects/meta" \
  -H "Api-Key: YOUR_API_KEY" \
  -H "Api-Appid: YOUR_APP_ID"
```

The response's `data` array lists each object you can access — e.g. the first entry `"Contact"` with `"id": 0` is the Contacts database (objectID 0).

## The object model

There is **no `/contacts` resource**. Instead, you operate on `/objects` and pass an `objectID`:

| objectID | Object |
|---|---|
| `0` | Contact |
| (varies) | Custom objects, transactions, products, tags, etc. — discover via `GET /1/objects/meta` |

## Core endpoints

HTTP methods: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.

| Operation | Method + path | Notes |
|---|---|---|
| List object types | `GET /1/objects/meta` | Returns every object name + objectID |
| Get object metadata/fields | `GET /1/objects/getInfo` | Field-level metadata for an objectID |
| List/search objects | `GET /1/objects?objectID=0` | + `range`, `start`, `listFields`, `sort`, `condition`, `search` |
| Get single object | `GET /1/object?objectID=0&id=1234` | One record by id |
| Create object | `POST /1/objects` | Body: `objectID` + fields |
| Create-or-update | `POST /1/objects/saveorupdate` | Upsert by a unique field (e.g. email) |
| Update object | `PUT /1/objects` | Body: `objectID` + `id` + fields |
| Delete object | `DELETE /1/objects?objectID=0&id=1234` | |
| Add tag to contact | `PUT /1/objects/tag` | Add a tag to one/many objects |
| Remove tag | `DELETE /1/objects/tag` | |
| Subscribe webhook | `POST /1/objects` (webhook objectID) | See Webhooks below |

## Example requests & responses

<!-- Constructed from documented fields — verify exact keys against the live Swagger doc -->

**Create a contact** — `POST /1/objects` (form-encoded):
```
objectID=0
email=jane@example.com
firstname=Jane
lastname=Doe
```
Response (shape):
```json
{ "code": 0,
  "data": { "id": "1234", "email": "jane@example.com", "firstname": "Jane" },
  "account_id": 55555 }
```

**Create-or-update (upsert by email)** — `POST /1/objects/saveorupdate`:
```
objectID=0
email=jane@example.com
firstname=Jane
```

**List contacts (paginated)** — `GET /1/objects?objectID=0&range=50&start=0&listFields=id,email`:
```json
{ "code": 0,
  "data": [ { "id": "1234", "email": "jane@example.com" } ],
  "account_id": 55555 }
```

**Add a tag** — `PUT /1/objects/tag`:
```
objectID=0
ids[]=1234
add_list=88
```

**Error response** (shape):
```json
{ "code": 41, "data": "Api-Appid or Api-Key is invalid" }
```

## Pagination

Offset-based, capped at **50 records per call**:

| Param | Meaning |
|---|---|
| `range` | Records per page (max 50) |
| `start` | Offset — advance by `range` each loop |
| `listFields` | Comma-separated fields to return (limit payload size) |
| `sort` / `sortDir` | Field to sort by + direction |
| `condition` | JSON filter criteria for complex queries |
| `search` | Free-text search across fields |

Loop: request `range=50&start=0`, then `start=50`, `start=100`… until an empty `data` array returns.

## Rate limits

- **180 requests per minute** (rolling limit, resets continuously).
- Track remaining budget via the rate-limit response headers.
- On `429`, back off exponentially with jitter and retry. Batch with `range` (50/call) and request only needed `listFields` to spend fewer calls.

## Webhooks

Subscribe an endpoint **via the API** (create a webhook object) with a valid `Api-Key` + `Api-Appid` and a receiving URL. When the subscribed event fires, Ontraport POSTs JSON to your URL.

**Available events:**

- **Object is created** (Contact or custom object record)
- **Form is submitted**
- **Tag is added**
- **Tag is removed**
- **Product is purchased**
- **Transaction is added**

**Operational notes:**
- Pass `Api-Key`/`Api-Appid` in **headers**, not GET/POST data.
- Inspect/replay via **Administration → Integrations → Webhook Logs** (stores up to **10,000** webhook activities).
- Treat delivery as at-least-once: respond `2xx` quickly, process async, and dedupe on the resource id.
- Payload follows JSON standards; exact field names per event aren't fully published — log a sample before coding against them.

## Gaps

- The **official reference is an interactive Swagger UI** (`api.ontraport.com/doc` / `/live`) that requires credentials and is JS-rendered — full per-endpoint request/response schemas weren't fetchable via WebFetch. Base URL, auth, object model, pagination params, the 180/min limit, and webhook events above are sourced from the official support docs, the API announcement, and the tray.ai connector docs; **example JSON is constructed and marked**.
- **Exact webhook payload schemas** per event are not published — capture a live sample.
- **No MCP server** found. Official SDKs/repos exist under `github.com/Ontraport`.
- Third-party "Rollout" SDK guides appear partly auto-generated — prefer the official Swagger doc + a live test call.
