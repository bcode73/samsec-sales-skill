<!-- Source: https://developers.surfe.com/ (Introduction, API Key, Webhooks, Changelog) + https://intercom.help/surfe/ (Getting Started, Enrich Companies, Get Credits) — captured 2026-06-28 -->

# Surfe API Reference

Captured verbatim from the Surfe developer docs (`developers.surfe.com`) and the Surfe Help Center API articles. Secret-shaped example values are placeholders only.

## Base URL & versions

- **Base URL:** `https://api.surfe.com`
- **Current version:** `v2` (e.g. `https://api.surfe.com/v2/people/enrich`)
- **`v1` is deprecated** for search. The March 2025 update reworked `/v2/people/search`; `/v1/people/search` is marked deprecated. The deprecated `companyID` field was replaced with `organizationIDMappings`.
- Some utility endpoints still answer on `v1` (e.g. `GET /v1/credits`).
- **Support:** api.support@surfe.com

## Authentication

The Surfe API uses user-specific API keys.

- Generate the key at **API Settings**: `https://app.surfe.com/api-settings`.
- API Keys are unique per user — **each user can have only one at any given time**.
- Pass it in the `Authorization` header using the Bearer scheme.
- "If you suspect your API Key has been compromised, delete it as soon as possible and create a new one in the Surfe dashboard."

```
curl --location 'https://api.surfe.com/v1/*SOME ENDPOINT*/' \
--header 'Authorization: Bearer *YOUR API KEY*' \
--data ''
```

Authorization header format:

```
Authorization: Bearer YOUR_API_KEY
```

## Rate limits & quotas

- **Up to 10 requests per second**, with bursts up to 20.
- Daily allowance: **~2,000 requests per day** (people enrichment quota 2,000/day; search results quota 200/day).
- Quotas reset daily at midnight (user's local timezone).
- Exceeding limits returns **`429 Too Many Requests`**.

## Credit system

Three separate credit pools track usage independently:

- **Email** credits
- **Mobile** (phone) credits
- **Search** credits

You only spend a credit **when data is successfully found** (no charge for misses). Search credit formula was updated June 2026 from `⌈results / 25⌉` to `⌈results / 10⌉`.

### Get Credits — `GET /v1/credits`

A simple GET request. No payload needed — just your API token in the header.

```
curl --location 'https://api.surfe.com/v1/credits' \
--header 'Authorization: Bearer YOUR_API_TOKEN'
```

Response:

```json
{
  "message": "You are out of {email | mobile | email and mobile} credits, buy more here: https://surfe.com/buy-credits",
  "totalEmail": 42,
  "totalMobile": 43,
  "totalSearch": 44
}
```

Check your balance before large enrichment requests, on a schedule, or after purchasing new credits.

## Async enrichment model

People and company enrichment works in **two steps**:

1. **Start** the enrichment (`POST`) → receive an `enrichmentID` (and an `enrichmentCallbackURL`).
2. **Fetch** the results using that ID (`GET .../enrich/{enrichmentID}`), **or** receive them via a webhook (recommended over manual polling).

## Endpoint inventory

**People Operations**
- `POST /v2/people/search` — Search people
- `POST /v2/people/enrich` — Start bulk people enrichment
- `GET /v2/people/enrich/{enrichmentID}` — Fetch people enrichment results
- Enrich by email (POST)

**Company Operations**
- `POST /v2/companies/search` — Search companies
- `POST /v2/companies/enrich` — Start company enrichment
- `GET /v2/companies/enrich/{enrichmentID}` — Fetch company enrichment results

**Recommendations** (launched April 2026)
- Create/update ICP (POST)
- Fetch recommendations (POST)
- Get ICP filters (GET)

**Utility**
- `GET /v1/credits` — Get credits
- Get filters (GET)

---

## Enrich People (start) — `POST /v2/people/enrich`

Initiates an asynchronous bulk enrichment job for a list of people, checking quota and credits before processing.

**Request body fields**

- `enrichmentOptions` (object): Configuration for enrichment behavior
  - `acceptedEmailType`: `"professional"` or `"personal"`
  - `skipMobileEnrichmentIfNoEmailFound`: boolean
- `include` (object, required): Fields to include in results
  - `email`: boolean
  - `jobHistory`: boolean
  - `linkedInUrl`: boolean
  - `mobile`: boolean
- `notificationOptions` (object): Webhook configuration
  - `webhookUrl`: string for completion notifications
- `people` (array, required): **Up to 10,000 people** to enrich
  - `firstName`, `lastName`: strings
  - `companyName` or `companyDomain`: identifier
  - `linkedinUrl`: LinkedIn profile URL
  - `externalID`: optional reference identifier

**Headers**
- `Authorization`: Bearer token (required)
- `X-Request-Origin`: Request source identifier

**Example request (cURL)**

```bash
curl -X POST "https://api.surfe.com/v2/people/enrich" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "enrichmentOptions": {
      "acceptedEmailType": "professional",
      "skipMobileEnrichmentIfNoEmailFound": false
    },
    "include": {
      "email": true,
      "jobHistory": false,
      "linkedInUrl": false,
      "mobile": true
    },
    "notificationOptions": {
      "webhookUrl": ""
    },
    "people": [
      {
        "companyDomain": "surfe.com",
        "companyName": "Surfe",
        "externalID": "external-id",
        "firstName": "David",
        "lastName": "Chevalier",
        "linkedinUrl": "https://www.linkedin.com/in/david-maurice-chevalier"
      }
    ]
  }'
```

**Example response (202)**

```json
{
  "enrichmentCallbackURL": "https://api.surfe.com/v2/people/enrich/0195be44-1a0d-718a-967b-042c9d17ffd7",
  "enrichmentID": "0195be44-1a0d-718a-967b-042c9d17ffd7",
  "message": "Your enrichment has started ✨, estimated time: 2 seconds."
}
```

## Fetch People enrichment results — `GET /v2/people/enrich/{enrichmentID}`

```bash
curl -X GET "https://api.surfe.com/v2/people/enrich/YOUR_ENRICHMENT_ID" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Returns the enrichment job status and the enriched people once `status` is `COMPLETED`.

---

## Enrich Companies (start) — `POST /v2/companies/enrich`

**Request body fields**
- `companies` array (**up to 500 companies**)
  - `domain`: company domain
  - `externalID`: your identifier
- `notificationOptions`: webhook configuration

**Example request**

```bash
curl --location 'https://api.surfe.com/v2/companies/enrich' \
--header 'Authorization: Bearer YOUR_API_TOKEN' \
--header 'Content-Type: application/json' \
--data '{
    "companies": [
      {
        "domain": "surfe.com",
        "externalID": "external-id"
      }
    ],
    "notificationOptions": {
      "webhookUrl": ""
    }
  }'
```

**Example response**

```json
{
    "message": "Your enrichment has started ✨, estimated time: 1s.",
    "enrichmentID": "019841ef-c288-76ab-9311-41392ea079ad",
    "enrichmentCallbackURL": "https://api.surfe.com/v2/companies/enrich/019841ef-c288-76ab-9311-41392ea079ad"
}
```

## Fetch Company enrichment results — `GET /v2/companies/enrich/{enrichmentID}`

**Completed response example**

```json
{
  "status": "COMPLETED",
  "percentCompleted": 100,
  "companies": [
    {
      "externalID": "external-id",
      "name": "Surfe",
      "description": "Sales teams waste too much time on repetitive admin tasks...",
      "linkedInURL": "https://linkedin.com/company/surfe",
      "websites": ["surfe.com"],
      "founded": "2020",
      "revenue": "10-50M",
      "employeeCount": 65,
      "industry": "IT Services",
      "subIndustry": "Internet Services & Infrastructure",
      "isPublic": false,
      "followersCountLinkedin": 8896,
      "hqCountry": "FR",
      "hqAddress": "52 Rue Chaussée D'antin Paris FR 75009",
      "keywords": ["crm updates", "linkedin sales", "waterfall enrichment", "sales automation"],
      "digitalPresence": [{"name": "LinkedIn", "url": "https://www.linkedin.com/company/surfe"}],
      "fundingRounds": [{"name": "Seed Round - Surfe", "amount": 9999999, "amountCurrency": "$", "announcedDate": "2021-01-01", "leadInvestors": ["Investor A", "Investor B"]}],
      "status": "COMPLETED"
    }
  ]
}
```

---

## Search — `POST /v2/people/search` and `POST /v2/companies/search`

Primary search endpoints for querying people and organizations.

**People filters:** seniorities, departments, industries, countries, states, exactJobTitles, previousCompanyDomains, jobChangePeriodInDays, countriesExcluded, statesExcluded.

**Company filters:** industries, departments, technologies, countries, states, localities (with `isExcluded` flag), naicsCodes, names, departmentSizes, keywords, yearFounded, and more.

**Location-based:** the `localities` filter supports searching by countries, regions within countries, zip codes, or free text within company addresses.

Country filter limits were expanded from 100 to 250 entries (June 2026). Search credits are charged as `⌈results / 10⌉`.

---

## Webhooks

Surfe webhooks send real-time event notifications via HTTP POST to your endpoint, eliminating polling. To enable them, include `notificationOptions.webhookUrl` in the enrichment request. **Only HTTPS endpoints are accepted; HTTP is rejected.**

### Supported event types

1. `person.enrichment.completed` — individual contact enrichment finished
2. `person.batch-enrichment.completed` — all contacts in a bulk enrichment complete
3. `company.enrichment.completed` — company enrichment finished

### Event structure

```json
{
  "eventType": "string",
  "data": {}
}
```

### Setup snippet

```json
"notificationOptions": {
  "webhookUrl": "https://your-secure-endpoint.com/webhook"
}
```

### Signature verification

Each webhook includes an `x-surfe-signature` header containing a timestamp and an HMAC-SHA256 signature:

```
x-surfe-signature: t=1758468698287,v0=ac18feb8cdbcaf4bf98beb90586f95159646a21629326f8bb6f63305f82155ea
```

Verification steps:

1. Extract timestamp (`t=`) and signature (`v0=`) from the header.
2. Recreate the signed payload: `timestamp.request_body`.
3. Compute HMAC-SHA256 using your webhook secret.
4. Compare the computed signature with the received one.
5. Validate the timestamp falls within an acceptable tolerance (replay-attack prevention).

Retrieve your **webhook shared secret** from the [API settings page](https://app.surfe.com/api-settings) **after receiving your first webhook notification**.

**Python**

```python
import hmac
import hashlib

def verify_webhook_signature(payload, secret, signature_header):
    parts = signature_header.split(',')
    timestamp = ''
    signature = ''
    for part in parts:
        if part.startswith('t='):
            timestamp = part.replace('t=', '')
        if part.startswith('v0='):
            signature = part.replace('v0=', '')
    if not timestamp or not signature:
        raise ValueError('invalid signature header format')

    message = f"{timestamp}.{payload}"
    mac = hmac.new(secret.encode(), message.encode(), hashlib.sha256)
    expected_signature = mac.hexdigest()

    return hmac.compare_digest(expected_signature, signature)
```

**JavaScript**

```javascript
const crypto = require('crypto');

function verifyWebhookSignature(payload, secret, signatureHeader) {
  const parts = signatureHeader.split(',');
  let timestamp = '';
  let signature = '';
  for (const part of parts) {
    if (part.startsWith('t=')) {
      timestamp = part.replace('t=', '');
    }
    if (part.startsWith('v0=')) {
      signature = part.replace('v0=', '');
    }
  }
  if (!timestamp || !signature) {
    throw new Error('invalid signature header format');
  }

  const message = `${timestamp}.${payload}`;
  const hmacObj = crypto.createHmac('sha256', secret);
  hmacObj.update(message);
  const expectedSignature = hmacObj.digest('hex');

  return expectedSignature === signature;
}
```

**Go**

```go
package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"strings"
)

func VerifyWebhookSignature(payload, secret, signatureHeader string) (bool, error) {
	parts := strings.Split(signatureHeader, ",")
	var timestamp, signature string
	for _, part := range parts {
		if strings.HasPrefix(part, "t=") {
			timestamp = strings.TrimPrefix(part, "t=")
		}
		if strings.HasPrefix(part, "v0=") {
			signature = strings.TrimPrefix(part, "v0=")
		}
	}
	if timestamp == "" || signature == "" {
		return false, errors.New("invalid signature header format")
	}

	message := timestamp + "." + payload
	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write([]byte(message))
	expectedSignature := hex.EncodeToString(mac.Sum(nil))

	return hmac.Equal([]byte(expectedSignature), []byte(signature)), nil
}
```

Your endpoint must respond **HTTP 200 OK** to confirm receipt; non-200 responses may trigger retries based on configuration.

## Other integration surfaces

- **n8n** integration support and **GitHub code examples** are referenced in the docs.
- Native CRM connectors (HubSpot, Salesforce, Pipedrive, Copper) and Google Sheets are managed in-app, not via this REST API.

## Gaps

- Full request/response JSON for `POST /v2/people/search`, `POST /v2/companies/search`, the "Enrich by email" endpoint, and the Recommendations (ICP) endpoints are documented on individual JS-rendered pages not fully captured here. Filters lists above are from the changelog. Verify exact payloads against `https://developers.surfe.com/` before building.
