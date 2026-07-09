# Surfe Platform Reference

## Overview

Surfe (formerly Leadjet) is a LinkedIn-to-CRM data tool: a Chrome extension that pushes LinkedIn and Sales Navigator contacts straight into HubSpot, Salesforce, Pipedrive, or Copper, plus a **waterfall enrichment** layer (15+ providers) that finds verified professional emails and mobile numbers. Built for individual SDRs/BDRs and small sales teams who live on LinkedIn; less suited to high-volume, background bulk enrichment.

## Capabilities & automation surface

| Capability | What it does | Surface |
|---|---|---|
| CRM Chrome extension | One-click add LinkedIn profiles to CRM; sync messages/notes; see CRM data on the profile | UI-only (extension) |
| Waterfall enrichment | Cascades 15+ providers for verified email + mobile; triple-verified | API-accessible (`/v2/people/enrich`) + extension |
| Company enrichment | Firmographics, revenue, headcount, industry, funding rounds, keywords | API-accessible (`/v2/companies/enrich`) |
| People search | Find contacts by seniority, department, industry, country, job title, job-change window | API-accessible (`/v2/people/search`) |
| Company search | Find companies by industry, tech, locality, NAICS, headcount, keywords | API-accessible (`/v2/companies/search`) |
| Sales Navigator list export | Bulk-export a Sales Nav search/list to CRM or sheet | UI-only (extension) |
| Job change alerts | Notify when a tracked contact changes jobs | UI-only / app |
| Recommendations (ICP) | Create an ICP, fetch recommended accounts/contacts | API-accessible (Recommendations endpoints) |
| Webhooks | `person.enrichment.completed`, `person.batch-enrichment.completed`, `company.enrichment.completed` | Webhook-accessible |
| CRM connectors | HubSpot, Salesforce, Pipedrive, Copper, Google Sheets; Salesloft/Outreach in the stack | In-app (not via REST) |

**Key gotcha:** the extension enriches in-session (you must be viewing a LinkedIn profile/list); the **REST API** is where true background/bulk enrichment lives (up to 10,000 people or 500 companies per job).

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify against surfe.com/pricing.*

| Plan | Price | Credits (note: **per YEAR**, not per month) |
|---|---|---|
| Free | $0 | ~20 email + 5 phone credits/year |
| Essential | ~$39/seat/mo ($29.25 annual) | ~150 email + 50 phone credits/year |
| Pro | ~$79/seat/mo ($59.25 annual) | ~1,000 email + 100 phone credits/year |
| Enterprise | Custom | Custom |

- **Annual credit caps are the #1 cost gotcha** — Essential's "150 email credits/year" is ~12/month; a rep enriching 10 contacts/day exhausts the annual pool in ~2 weeks. Budget around the annual number, not a monthly one.
- Three **separate** credit pools (email, mobile, search) — running out of one doesn't touch the others.
- API credits are spent **only on successful finds** (misses are free).
- API quotas: ~2,000 people enrichments/day, ~200 search results/day; 10 req/s (burst 20); `429` on overage.
- Pricing is **per seat** — costs rise quickly as the team grows.

## Integrations

- **CRMs (bidirectional, in-app):** HubSpot, Salesforce (AppExchange listing), Pipedrive, Copper. Niche CRMs are not supported — a recurring complaint.
- **Sheets:** Google Sheets export.
- **Sales engagement:** Salesloft, Outreach appear in the stack.
- **Developer:** REST API (reads search/enrichment, writes nothing to CRM), webhooks (event-driven), n8n nodes, GitHub code examples.
- Data flow: the **API** is a read/enrich service (people/company → verified contact + firmographics); CRM writes happen through the **extension/native connectors**, not the public REST API.

## Data model

People enrichment job (start) response:

```json
{
  "enrichmentCallbackURL": "https://api.surfe.com/v2/people/enrich/0195be44-1a0d-718a-967b-042c9d17ffd7",
  "enrichmentID": "0195be44-1a0d-718a-967b-042c9d17ffd7",
  "message": "Your enrichment has started ✨, estimated time: 2 seconds."
}
```

Company enrichment result (key object):

```json
{
  "status": "COMPLETED",
  "percentCompleted": 100,
  "companies": [
    {
      "externalID": "external-id",
      "name": "Surfe",
      "linkedInURL": "https://linkedin.com/company/surfe",
      "websites": ["surfe.com"],
      "founded": "2020",
      "revenue": "10-50M",
      "employeeCount": 65,
      "industry": "IT Services",
      "hqCountry": "FR",
      "fundingRounds": [{"name": "Seed Round - Surfe", "amount": 9999999, "amountCurrency": "$", "announcedDate": "2021-01-01"}],
      "status": "COMPLETED"
    }
  ]
}
```

Credits object:

```json
{ "totalEmail": 42, "totalMobile": 43, "totalSearch": 44 }
```

The `externalID` you pass on each person/company echoes back in results — use it to map enriched records to your own row IDs.

## Quick-start recipes

### 1. Bulk-enrich a list of people via the API (start → webhook)

```bash
curl -X POST "https://api.surfe.com/v2/people/enrich" \
  -H "Authorization: Bearer $SURFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "enrichmentOptions": {"acceptedEmailType": "professional", "skipMobileEnrichmentIfNoEmailFound": true},
    "include": {"email": true, "mobile": true, "linkedInUrl": true, "jobHistory": false},
    "notificationOptions": {"webhookUrl": "https://yourapp.com/surfe-webhook"},
    "people": [
      {"firstName": "David", "lastName": "Chevalier", "companyDomain": "surfe.com", "externalID": "row-42"}
    ]
  }'
```

The response returns an `enrichmentID`. Set `skipMobileEnrichmentIfNoEmailFound: true` to avoid burning mobile credits on dead rows.

### 2. Poll for results (if not using a webhook)

```python
import os, time, requests

KEY = os.environ["SURFE_API_KEY"]
H = {"Authorization": f"Bearer {KEY}"}

start = requests.post("https://api.surfe.com/v2/people/enrich",
    headers={**H, "Content-Type": "application/json"},
    json={"include": {"email": True, "mobile": True},
          "people": [{"firstName": "David", "lastName": "Chevalier",
                      "companyDomain": "surfe.com", "externalID": "row-42"}]})
eid = start.json()["enrichmentID"]

while True:
    r = requests.get(f"https://api.surfe.com/v2/people/enrich/{eid}", headers=H).json()
    if r.get("status") == "COMPLETED":
        break
    time.sleep(2)
print(r)
```

Prefer the webhook (`notificationOptions.webhookUrl`) over tight polling so you don't waste your ~2,000 req/day quota.

### 3. Verify a webhook signature before trusting the payload

The webhook carries `x-surfe-signature: t=<ts>,v0=<hmac-sha256>`. Recreate `"{t}.{raw_body}"`, HMAC-SHA256 it with your webhook secret (from API settings, available after the first webhook fires), and `hmac.compare_digest` against `v0`. Reject stale timestamps to block replays. (Full Python/JS/Go in `surfe-api-reference.md`.)

### 4. Check credits before a big batch

```bash
curl "https://api.surfe.com/v1/credits" -H "Authorization: Bearer $SURFE_API_KEY"
# {"totalEmail":42,"totalMobile":43,"totalSearch":44}
```

Gate large jobs on `totalEmail`/`totalMobile` so you don't half-finish a batch when the annual pool runs dry.

## Integration patterns

- **CRM sync architecture:** the public API does **not** write to your CRM — it returns enriched data. To land data in HubSpot/Salesforce, either use the native extension/connector or take the API result and call the CRM's own API. Map records with `externalID`.
- **Webhook listener:** require HTTPS, verify `x-surfe-signature` (HMAC-SHA256 of `t.body`), respond 200 fast, process async. Handle all three event types; `person.batch-enrichment.completed` is your "whole job done" signal.
- **Batch pipeline:** chunk people into ≤10,000-per-job (companies ≤500), submit, collect via webhook, retry `429` with backoff, and reconcile by `externalID`. Set `skipMobileEnrichmentIfNoEmailFound` to conserve the mobile pool.
- **Credit budgeting:** because credits are annual and split into 3 pools, poll `/v1/credits` on a schedule and alert before depletion; reveal mobiles only for must-call contacts.
