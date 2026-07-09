# Maximizer Platform Reference

## Overview

Maximizer is a Canadian, customizable CRM (cloud "CRM Live" or on-premise) aimed at SMB sales teams and, distinctively, **financial-services / wealth-advisory** firms. Its differentiators are the Financial Advisor edition (households, investment/insurance data views, family-connection visualization) and tight Microsoft Outlook/365 integration. It is not a free-tier, PLG product — it sells on annual seats and a 30-day trial.

## Capabilities & automation surface

| Module / capability | What it does | Automation surface |
|---|---|---|
| **AbEntry** (Companies / Contacts / Individuals) | Core address-book records | **API** (`/Read` `/Create` `/Update` `/Delete`) + **webhook** |
| **Opportunities** | Deals on a Dynamic Pipeline with stages/methodologies | **API** + **webhook** |
| **Leads** | Lead records kept separate from deals | **API** + **webhook** |
| **Cases** | Customer-service/case records | **API** + **webhook** |
| **Activities / Appointments / Notes / InteractionLog** | Activity timeline (calls, emails, appts, notes) | **API** + **webhook** |
| **Campaigns** | Marketing campaigns | **API** |
| **User / SalesTeam / Territory** | Org structure, assignment | **API** (mostly read) |
| **User-Defined Fields (UDFs)** | Custom fields, incl. table UDFs | **API** via `Udf/$TYPEID` notation |
| **Documents / binaries** | File attachments on records | **API** (`/BinaryUpload`, `/BinaryDownload/{key}`) |
| **Workflows** | Automation workflows | **API** (`/WorkflowStart`) |
| **Email & Calendar sync (Outlook/M365)** | Two-way email/calendar | **UI-only** (Outlook add-in; per-email linking is manual) |
| **Reports & dashboards (IQ / IQ Boost AI)** | Out-of-box dashboards, AI insights | **UI-only**; export raw data via API + PowerBI connector |

## Pricing, limits & plan gates

Best-effort (annual billing, per user/month — re-verify at maximizer.com/pricing):

| Edition | Price (annual) | For |
|---|---|---|
| **Base / For Sales** | ~$65 | Core CRM, pipeline, activity tracking |
| **Sales Leader** | ~$79 | Team management, advanced pipeline |
| **Financial Advisor** | ~$79–100 | Households, investment/insurance views, family connections, compliance |
| **On-premise** | Quote | Self-hosted deployment |

- **No free tier** — 30-day trial only. **Monthly billing runs ~10–20% higher** than annual.
- **Rate limits are per-edition** (see API reference): Core ~30 calls / 10 s, Business/Financial ~90 / 30 s, Enterprise custom.
- AI features (IQ Boost) and the Financial Advisor data views are edition-gated. The legacy **Ferret API** still exists but Octopus is the forward path.
- Reviewer-noted gotcha: the shift to annual-license "rental" raised effective cost vs. older perpetual licensing.

## Integrations

- **Reads from / writes to**: bidirectional via the Octopus API for AbEntry, Opportunity, Lead, Case, Activity, Note objects.
- **Native**: Microsoft Outlook / Microsoft 365 (email + calendar), Microsoft Power BI (reporting connector), Mailchimp, QuickBooks (varies by edition), Zapier.
- **Webhooks**: outbound only — Maximizer POSTs change events to a target you register (see API reference). Use these to push changes into a warehouse, Slack, or another CRM.
- **iPaaS**: Zapier connector; Make/n8n via the REST (Octopus) API. There is no documented inbound webhook — write into Maximizer through the API.

## Data model

Records are addressed by an opaque, base64-encoded composite **`Key`** that encodes the entity type and internal IDs. **Never construct a Key by hand** — read a record, then reuse its `Key` on update/delete.

**AbEntry (a Company), create request:**
```json
{
  "AbEntry": {
    "Data": { "Key": null, "Type": "Company", "CompanyName": "E. Brown Enterprise" }
  },
  "Compatibility": { "AbEntryKey": "2.0" }
}
```
**Response:**
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
`Code: 0` = success. `Type` is one of `Company`, `Contact` (a person at a company), or `Individual`.

**Opportunity** (deal) — key fields: `Key`, `Description`, `AbEntry` (linked company/contact), `Leader` (owner), `CloseDate`, `CorporateRevenue`, `Stage`, `Status` (Won/Lost/InProgress), `CreationDate`.

**Lead**, **Case**, **Note**, **Activity/Appointment** follow the same `{ "<Object>": { "Data": {...} } }` envelope. UDFs appear under `Udf/$TYPEID` keys.

## Quick-start recipes

### Recipe 1 — Authenticate (cloud PAT) and read contacts
Cloud uses a **Personal Access Token** sent as a Bearer token; base URL `https://api.maximizer.com/octopus`.

```bash
# Read up to 3 contacts (Type = Contact), selecting a few fields
curl -X POST "https://api.maximizer.com/octopus/Read" \
  -H "Authorization: Bearer $MAX_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "AbEntry": {
      "Scope": { "Fields": { "Key": 1, "FirstName": 1, "LastName": 1 } },
      "Criteria": { "SearchQuery": { "Type": { "$EQ": "Contact" } }, "Top": 3 }
    },
    "Configuration": { "Drivers": { "IAbEntrySearcher": "Maximizer.Model.Access.Sql.AbEntrySearcher" } }
  }'
```
```python
import requests, os
BASE = "https://api.maximizer.com/octopus"
H = {"Authorization": f"Bearer {os.environ['MAX_PAT']}", "Content-Type": "application/json"}

body = {
  "AbEntry": {
    "Scope": {"Fields": {"Key": 1, "FirstName": 1, "LastName": 1}},
    "Criteria": {"SearchQuery": {"Type": {"$EQ": "Contact"}}, "Top": 3},
  },
  "Configuration": {"Drivers": {"IAbEntrySearcher": "Maximizer.Model.Access.Sql.AbEntrySearcher"}},
}
r = requests.post(f"{BASE}/Read", json=body, headers=H)
data = r.json()
assert data["Code"] == 0, data        # always check Code, even on HTTP 200
for c in data["AbEntry"]["Data"]:
    print(c["Key"], c.get("FirstName"), c.get("LastName"))
```
**Gotcha**: omit/misname `Configuration.Drivers` and you get an empty list, not an error.

### Recipe 2 — Incremental opportunity export (rate-limit safe)
Pull only recently-changed opportunities, page through results, select minimal fields.

```python
body = {
  "Opportunity": {
    "Scope": {"Fields": {"Key": 1, "Description": 1, "CloseDate": 1,
                          "CorporateRevenue": 1, "Status": 1}},
    "Criteria": {
      # opportunities whose close date falls in the next 6 months
      "SearchQuery": {"CloseDate": {"$OFFSET()": {"From": "0d", "To": "6M"}}},
      "Top": 100
    },
    "OrderBy": {"Fields": [{"CreationDate": 1}]}   # stable order for pagination
  },
  "Configuration": {"Drivers": {"IOpportunitySearcher": "Maximizer.Model.Access.Sql.OpportunitySearcher"}}
}
# Core edition ~30 calls/10s, Business/Financial ~90/30s. Back off on HTTP 429.
```
**Gotcha**: a `408` means a single `/Read` ran too long — narrow `Scope.Fields` and lower `Top`.

### Recipe 3 — Subscribe to a webhook for opportunity changes
The Webhooks API (base `https://api.maximizer.com/webhooks`) is a two-step REST flow: register a **target** (your endpoint), then create a **subscription**.

```bash
# 1) Register a target endpoint
curl -X POST "https://api.maximizer.com/webhooks/v1/targets" \
  -H "Authorization: Bearer $MAX_PAT" -H "Content-Type: application/json" \
  -d '{ "Name": "warehouse-sink", "Endpoint": { "Url": "https://example.com/hooks/max" } }'

# 2) Subscribe that target to Opportunity create/update events
curl -X POST "https://api.maximizer.com/webhooks/v1/subscriptions" \
  -H "Authorization: Bearer $MAX_PAT" -H "Content-Type: application/json" \
  -d '{ "Entity": "Opportunity", "Op": "Update", "TargetId": "<target-id>",
        "Recipients": [], "Filter": [] }'
```
Your endpoint **must return `200 OK` within 2 seconds**; Maximizer retries twice then drops the event. There is **no HMAC** — secure the endpoint with an allowlist or secret path. ACK fast, enqueue, process async.

## Integration patterns

- **CRM sync architecture**: treat the base64 `Key` as the join key; map `Type` (Company/Contact/Individual) onto your account/contact model. Reconcile with a periodic incremental `/Read` even if you use webhooks, because webhooks can be dropped.
- **Webhook listener**: return `200` immediately, push the payload onto a queue, verify origin (IP allowlist / secret URL), de-dupe on the payload `Id`, and use `Data.Op` (Create/Update/Delete) + `Data.New`/`Data.Original` to apply the change.
- **Batch/export**: filter on a date field with `$OFFSET()`/`$RANGE`, page with `OrderBy` + `Top`, request only needed `Scope.Fields`, and honor the per-edition rate window with exponential backoff on `429`. Use `GroupBy` (`$COUNT`/`$SUM`/`$AVG`) server-side to avoid pulling raw rows when you only need aggregates.
