<!-- Source: https://developer.maximizer.com/ (Octopus API docs, llms.txt) + https://github.com/maximizercrm/octopus-api (Postman collection) + https://github.com/maximizercrm/webhooks (openapi.json) -->

# Maximizer API Reference

Maximizer exposes two APIs:

1. **Octopus API** (a.k.a. **Maximizer.Web.Data**) — a JSON web service over Maximizer CRM data, available to cloud and on-premise customers. POST-RPC style: every operation is a `POST` to a verb path (`/Read`, `/Create`, `/Update`, `/Delete`, …) under a single base URL.
2. **Webhooks API** — a REST API (base `https://api.maximizer.com/webhooks`) for registering **targets** (your endpoints) and **subscriptions** (which events go where).

> For machine-readable docs, Maximizer publishes `https://developer.maximizer.com/llms.txt` (Markdown index + OpenAPI endpoints). Postman collections live at `github.com/maximizercrm/octopus-api` and `github.com/maximizercrm/webhooks`.

---

## Base URLs

| Deployment | Octopus base URL |
|---|---|
| Cloud (CRM Live) | `https://api.maximizer.com/octopus` |
| On-premise | `https://{your-server}/MaximizerWebData/...` (set during install) |

Webhooks API base (cloud): `https://api.maximizer.com/webhooks`

---

## Authentication

Three options for the Octopus API:

1. **Personal Access Token (PAT)** — mint in Maximizer account settings; send as a Bearer token:
   `Authorization: Bearer <PAT>`. Recommended for server-to-server integrations. (PATs are JWTs that carry the workspace id and an `exp` claim.)
2. **`/Authenticate` endpoint** — exchange credentials for a token.
3. **OAuth2** — for multi-tenant / user-delegated apps.

### `POST /Authenticate` — cloud (CRM Live)
```json
{
  "Database": "{{Database}}",
  "UID": "{{UID}}",
  "Password": "{{Password}}",
  "VendorId": "{{VendorId}}",
  "AppKey": "{{AppKey}}"
}
```

### `POST /Authenticate` — on-premise
```json
{
  "Database": "{{Database}}",
  "UID": "{{UID}}",
  "Password": "{{Password}}"
}
```

### `POST /TokenValid` — check a token is still valid
Request body: `{}` (token in the `Authorization` header).
Response:
```json
{ "Code": 0 }
```
`Code: 0` means valid. There is also `GET /VerifyToken`.

### Auth quick-start (cURL)
```bash
curl -X POST "https://api.maximizer.com/octopus/TokenValid" \
  -H "Authorization: Bearer $MAX_PAT" \
  -H "Content-Type: application/json" \
  -d '{}'
# -> {"Code":0}  (token is valid)
```

---

## Octopus endpoint catalog (all `POST` under the base URL)

| Endpoint | Purpose |
|---|---|
| `/Authenticate` | Exchange credentials for a token |
| `/TokenValid` , `/VerifyToken` | Validate the current token |
| `/Read` | Query records (the workhorse — Scope/Criteria/GroupBy/OrderBy) |
| `/Create` | Create a record |
| `/Update` | Update a record (requires the record `Key`) |
| `/Delete` | Delete a record (requires the record `Key`) |
| `/Validate` | Validate a record/payload without writing |
| `/BinaryUpload` | Upload a document/attachment |
| `/BinaryDownload/{document-key}` | Download a stored document |
| `/WorkflowStart` | Start an automation workflow |
| `/PayloadExecute` | Execute a composite payload |
| `/GetSessionInfo` , `/GetSystemInfo` , `/GetVersionInfo` | Session / system / version metadata |
| `/ConfigurationRead` | Read configuration |

Every request body is wrapped in the target object name (`AbEntry`, `Opportunity`, `Lead`, `Case`, `Note`, …) plus a `Configuration` block. Responses return a numeric **`Code`** (`0` = success).

---

## Read query syntax

A `/Read` body has up to four clauses inside the object wrapper, plus a top-level `Configuration`:

- **`Scope.Fields`** — the fields to return (`{ "FieldName": 1 }`). Check available fields via the object's Metadata read.
- **`Criteria.SearchQuery`** — the filter (operators below). `Criteria.Top` caps the row count.
- **`GroupBy.Fields`** — server-side aggregation with `$COUNT` / `$MIN` / `$MAX` / `$AVG` / `$SUM`.
- **`OrderBy.Fields`** — sort; combine with `Top` + paging for pagination.
- **`Configuration.Drivers`** — names the entity *searcher* to use (mandatory). Wrong/missing driver → empty result.

### `POST /Read` — list 3 contacts with names (verbatim from the Postman collection)
```json
{
    "AbEntry": {
        "Scope": {
            "Fields": {
                "Key": 1,
                "FirstName": 1,
                "LastName": 1
            }
        },
        "Criteria": {
            "SearchQuery": {
                "Type": {
                    "$EQ": "Contact"
                }
            },
            "Top": 3
        }
    },
    "Configuration": {
        "Drivers": {
            "IAbEntrySearcher": "Maximizer.Model.Access.Sql.AbEntrySearcher"
        }
    }
}
```

### `POST /Read` — count AbEntries grouped by type (GroupBy, verbatim)
```json
{
    "AbEntry": {
        "Scope": {
            "Fields": {
                "Type": 1,
                "$COUNT(type)": 1
            }
        },
        "GroupBy": {
            "Fields": [ "type" ]
        }
    },
    "Configuration": {
        "Drivers": {
            "IAbEntrySearcher": "Maximizer.Model.Access.Sql.AbEntrySearcher"
        }
    }
}
```

### Searcher driver names (`Configuration.Drivers`)
| Object | Driver key | Driver value |
|---|---|---|
| AbEntry (companies/contacts) | `IAbEntrySearcher` | `Maximizer.Model.Access.Sql.AbEntrySearcher` |
| Opportunity | `IOpportunitySearcher` | `Maximizer.Model.Access.Sql.OpportunitySearcher` |
| Lead | `ILeadSearcher` | `Maximizer.Model.Access.Sql.LeadSearcher` |
| Case | `ICaseSearcher` | `Maximizer.Model.Access.Sql.CaseSearcher` |

(Other objects follow the same `I{Object}Searcher` → `Maximizer.Model.Access.Sql.{Object}Searcher` pattern. Confirm exact names in the live docs.)

### Criteria operators
- **Comparison**: `$EQ`, `$NE`, `$GT`, `$GE`, `$LT`, `$LE`, `$IN`, `$NIN`, `$ALL`
- **Text**: `$LIKE`, `$NLIKE` (substring), `$PHRASE` (starts-with across FirstName/LastName/CompanyName)
- **Range**: `$RANGE`, `$NRANGE`
- **Logical**: `$AND`, `$OR` (nestable)
- **Date helpers**: `$NOW()`, `$TODAY()`, `$THISWEEK()`, `$THISMONTH()`, `$THISYEAR()`, `$OFFSET()` (relative window, e.g. "past 90 days")
- **Nested property** searches are supported (e.g. filter a company by `Address.ZipCode`).
- **FavoriteList**: read all AbEntries / Opportunities / Cases / Leads belonging to a saved Favorite List.

### Pagination
There is no cursor; page with `OrderBy` + `Top` and a stable sort field (e.g. `CreationDate`), advancing the filter window each page. Keep `Scope.Fields` minimal to avoid `408` timeouts on large pages.

---

## Write operations

Writes wrap the record under `<Object>.Data` plus a `Compatibility` block that pins the key-encoding version.

### `POST /Create` — create a company (verbatim)
```json
{
    "AbEntry": {
        "Data": { "Key": null, "Type": "Company", "CompanyName": "E. Brown Enterprise" }
    },
    "Compatibility": { "AbEntryKey": "2.0" }
}
```
Response:
```json
{
    "Code": 0,
    "AbEntry": {
        "Data": {
            "Key": "Q29tcGFueQkyNDA4MTMyNTIwMTMzNTMzNjAwNzhDCTA=",
            "Type": "Company",
            "CompanyName": "E. Brown Enterprise"
        }
    }
}
```

### `POST /Update` — update a field (verbatim)
```json
{
    "AbEntry": {
        "Data": {
            "Key": "Q29tcGFueQkyNDA4MTMyNTIwMTMzNTMzNjAwNzhDCTA=",
            "WebSite": "http://www.newsiteupdated.com"
        }
    },
    "Compatibility": { "AbEntryKey": "2.0" }
}
```
The `Key` is **mandatory** on update. It is an opaque base64 composite — read the record first, then send its `Key` back.

### `POST /Delete` — delete a record (verbatim)
```json
{
    "AbEntry": {
        "Data": { "Key": "Q29tcGFueQkyNDA4MTMyNTIwMTMzNTMzNjAwNzhDCTA=" }
    },
    "Compatibility": { "AbEntryKey": "2.0" }
}
```

### User-Defined Fields (UDFs)
Custom fields are addressed with the **`Udf/$TYPEID`** notation (not the display name) in both queries and webhook filters. Table UDFs work with `$ALL`/`$IN`.

---

## Rate limits & error handling

| HTTP code | Meaning |
|---|---|
| `200 OK` | Request completed (still check the `Code` in the body) |
| `401 Unauthorized` | Invalid/expired token |
| `408 Request Timeout` | The call exceeded its duration limit (narrow the query) |
| `429 Too Many Requests` | Rate limit exceeded — back off and retry |
| `5xx` | Server error |

**Per-edition rate limits:**

| Edition | Limit | Window |
|---|---|---|
| Core | 30 calls | 10 s |
| Business / Financial | 90 calls | 30 s |
| Enterprise | Custom | Custom |

**Retry snippet (Python):**
```python
import time, requests

def call(path, body, headers, base="https://api.maximizer.com/octopus", tries=5):
    for i in range(tries):
        r = requests.post(f"{base}{path}", json=body, headers=headers)
        if r.status_code == 429:
            time.sleep(2 ** i)           # exponential backoff
            continue
        r.raise_for_status()
        data = r.json()
        if data.get("Code") != 0:        # 200 but logical failure
            raise RuntimeError(f"Octopus error Code={data.get('Code')}: {data}")
        return data
    raise RuntimeError("rate-limited after retries")
```

---

## Webhooks API

Base URL: `https://api.maximizer.com/webhooks`. REST endpoints (from `openapi.json`):

| Method + path | Purpose |
|---|---|
| `POST /v1/targets` | Create a target (your endpoint) |
| `GET/DELETE /v1/targets/{TargetId}` | Read / delete a target |
| `POST /v1/targets/{TargetId}/enable` | Enable a target |
| `POST /v1/targets/{TargetId}/disable` | Disable a target |
| `POST /v1/subscriptions` | Create a subscription |
| `GET/DELETE /v1/subscriptions/{SubscriptionId}` | Read / delete a subscription |
| `.../subscriptions/{SubscriptionId}/recipients/{Recipient}` | Manage recipients |

**`TargetRequestDto`**: `Name` (string), `Endpoint` (a `TargetWebHookEndpointDto`, e.g. `{ "Url": "https://..." }`).

**`SubscriptionRequestDto`**: `Entity` (string, e.g. `Opportunity`), `Op` (string: `Create` / `Update` / `Delete` / `Read`), `TargetId` (string), `Recipients` (array), `Filter` (array — uses `Udf/$TYPEID` for custom-field filters).

### Delivered webhook payload shape
```json
{
  "Id": "<unique webhook id>",
  "Timestamp": "<when the event occurred>",
  "ProcessedTimestamp": "<when Maximizer forwarded it>",
  "WorkspaceId": "<source database/workspace>",
  "Entity": "Opportunity",
  "Data": {
    "Op": "Update",
    "Original": { /* pre-change fields — present for Update/Delete/Read */ },
    "New":      { /* post-change fields — present for Create/Update */ },
    "Version": "<object version in the source system>"
  }
}
```

### Delivery rules (important)
- Your target **must respond `200 OK` within 2 seconds**.
- On failure, Maximizer **retries twice** (3 attempts total), then **discards** the event.
- **No HMAC signature is documented** — authenticate the source yourself (IP allowlist, secret URL/header).
- De-dupe on `Id`; ordering is not guaranteed; reconcile with a periodic `/Read` to catch dropped events.

---

## Gaps

- The developer portal renders endpoint detail via JS / a docs UI; exact request schemas above are captured from the official **Postman collections** and **OpenAPI spec** in `github.com/maximizercrm`. Confirm field-level specifics and the full driver-name list against the live docs / `llms.txt` before relying on them.
- On-premise base URL is install-specific; the cloud base (`https://api.maximizer.com/octopus`) is from the published Postman environment.
- The legacy **Ferret API** is documented separately and is being superseded by Octopus; new integrations should target Octopus.
