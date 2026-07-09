<!-- Source: https://documentation.kartra.com/ (redirects to https://support.kartra.com/support/solutions/153000133328 "Developers") + https://documentation.kartra.com/section-2-connecting-to-the-api/ + https://documentation.kartra.com/api-post-1/ + https://documentation.kartra.com/section-31-api-limits/ -->
<!-- Live support.kartra.com article pages are JS-rendered/bot-blocked on direct fetch; the action surface, auth, endpoint, and rate limit below are captured verbatim from the official docs' descriptions. Example request/response JSON is CONSTRUCTED from the documented field/command lists and marked as such — verify against the live API. -->

# Kartra API Reference

Kartra exposes two API systems:
- **Inbound API** — your code → Kartra (create/edit leads, manage tags/lists/sequences, read pages, manage transactions/subscriptions, calendars, points).
- **Outbound API / IPN** — Kartra → your endpoint (event webhooks on purchases, tags, leads, sequences, memberships, forms, page visits).

> **Plan gate:** API access appears restricted to the **Professional** tier on current Kartra plans. Confirm the account's plan before building — a key on a lower tier may not authenticate.

## Connecting to the inbound API

- **Endpoint (base URL):** `https://app.kartra.com/api`
- **Method:** `POST`
- **Transport:** HTTPS only. "All API calls must be made using `https://` (not `http://`) as Kartra's API requires SSL encryption." `http://` is rejected.
- **Required parameters on every call:**
  - `app_id` — unique per App; hard-coded by the App developer. "Kartra will not accept any API call that doesn't include a valid App ID."
  - `api_key`
  - `api_password`
- **Where credentials live:** both the App developer and end users find their `api_key` and `api_password` under **Settings » Integrations » My API**. Only the App developer knows the `App ID` (it's coded into the App's calls).

### Request shape

Requests carry an `actions[]` array; each action specifies a `cmd`. Lead data travels in a `lead` object. When creating a lead, **the first `cmd` in the array must be `create_lead`** before any action that operates on that lead.

```
POST https://app.kartra.com/api
Content-Type: application/x-www-form-urlencoded

app_id=...&api_key=...&api_password=...
&lead[email]=jane@example.com
&lead[first_name]=Jane
&actions[0][cmd]=create_lead
&actions[1][cmd]=assign_tag
&actions[1][tag][tag_name]=app-trial
```

## Inbound API — action commands

| Domain | Actions (commands) |
|---|---|
| **Leads** | Retrieve a lead, search for leads, create a lead (`create_lead`), edit/update a lead |
| **Custom fields** | Create a custom field, retrieve all custom fields in the account |
| **Lists** | Retrieve all lists, subscribe a lead to a list, unsubscribe a lead from a list |
| **Tags** | Retrieve all tags, assign a tag to a lead, unassign/remove a tag from a lead |
| **Sequences** | Retrieve all sequences, subscribe a lead to a sequence, unsubscribe a lead from a sequence |
| **Pages** | Retrieve all pages in the account |
| **Payments (transactions)** | Get a transaction's details, retrieve transactions for a lead, search transactions, refund a transaction |
| **Recurring (subscriptions)** | Get a subscription's details, retrieve subscriptions for a lead, search subscriptions, cancel a subscription, edit subscription settings/status |
| **Calendars** | Subscribe a lead to a calendar, cancel a calendar subscription |
| **Points** | Give points to a lead, remove points from a lead |

## Auth quick-start (simplest call)

Retrieve account tags (a read action) to confirm credentials work:

```bash
curl -X POST https://app.kartra.com/api \
  --data-urlencode "app_id=YOUR_APP_ID" \
  --data-urlencode "api_key=YOUR_API_KEY" \
  --data-urlencode "api_password=YOUR_API_PASSWORD" \
  --data-urlencode "actions[0][cmd]=get_tags"
```

## Example requests & responses

<!-- Constructed from documented commands/fields — verify exact field names against the live API -->

**Create + tag a lead** (request body fields):
```
app_id=YOUR_APP_ID
api_key=YOUR_API_KEY
api_password=YOUR_API_PASSWORD
lead[email]=jane@example.com
lead[first_name]=Jane
lead[last_name]=Doe
actions[0][cmd]=create_lead
actions[1][cmd]=assign_tag
actions[1][tag][tag_name]=app-trial
```

**Success response** (shape):
```json
{
  "status": "Success",
  "actions": [
    { "create_lead": { "status": "Success", "lead_id": "9f3c1a7e" } },
    { "assign_tag":  { "status": "Success" } }
  ]
}
```

**Error response** (shape):
```json
{
  "status": "Error",
  "message": "Invalid API credentials"
}
```

**Search transactions for a lead** (request body fields):
```
app_id=YOUR_APP_ID
api_key=YOUR_API_KEY
api_password=YOUR_API_PASSWORD
actions[0][cmd]=retrieve_transactions
actions[0][lead][email]=jane@example.com
```

## Rate limits

- **20 API calls per second, per App** (hardcoded on the inbound API).
- Exceeding it returns a **`429` "Too many requests"** error.
- **Retry strategy:** stay below 20/sec with a client-side limiter; on `429`, back off exponentially (e.g. 1s, 2s, 4s with jitter) and retry. Collapse multi-step lead operations into a single `actions[]` array to spend fewer calls.

## Pagination

Not documented in the public material. The read path is the `search`/`retrieve` actions (e.g. search leads, search transactions, search subscriptions). Request narrow date/criteria windows and reconcile results by their ids rather than assuming a cursor/offset scheme. See **Gaps**.

## Outbound API / IPN (webhooks)

Kartra's outbound API ("IPN") pushes event notifications to a URL you configure. Managed in Kartra under **My Integrations » API** (enable the outbound API and select events).

**Events that fire an IPN:**
- A tag is **applied** to a lead
- A tag is **removed** from a lead
- A lead is **added** or **updated**
- A lead **purchases** a product
- A lead **completes a sequence**
- A lead **fills out a form**
- A lead **gains** membership access
- A lead **loses** membership access
- A lead **subscribes/unsubscribes** to a list or sequence
- A lead **visits** a Kartra page

**Handling guidance:** delivery is at-least-once — make handlers idempotent (dedupe on the transaction/lead identifier), respond `2xx` quickly and process asynchronously, and accept payloads over HTTPS. Field names vary by event type; log a sample payload per event before coding against it.

## Gaps

- **Live article pages** on `support.kartra.com` are JS-rendered/bot-blocked on direct fetch; the command surface, endpoint, auth, and rate limit above are taken verbatim from the official docs' text, but **full request/response JSON schemas per command were not fetchable**. Examples here are constructed and marked.
- **Pagination** for `search` actions is not publicly documented.
- **IPN payload schemas** (exact field names per event) are not published — capture a live sample to confirm.
- **No MCP server** and no OpenAPI/Swagger spec found as of this research.
