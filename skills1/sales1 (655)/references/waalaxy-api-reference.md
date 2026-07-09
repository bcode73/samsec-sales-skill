<!-- Source: https://docs.waalaxy.com/introduction and https://docs.waalaxy.com/api/* (fetched 2026-06-28) -->

# Waalaxy API Reference

Captured verbatim from the Waalaxy developer portal (`docs.waalaxy.com`). Where examples are reconstructed from the documented field tables rather than copied from a rendered example block, they are marked `<!-- Constructed from docs — verify against live API -->`.

## Welcome to the Waalaxy API

The Waalaxy API lets you integrate the platform with your favorite tools like n8n, Zapier, Make and many others.

- **Marketing Automation**: Connect Waalaxy to n8n, Zapier or Make workflows.
- **Data Enrichment**: Import enriched prospects from external sources.

## Base URL

```
https://developers.waalaxy.com
```

(The introduction page also references `https://api.waalaxy.com`, but every endpoint in the API Reference resolves against `https://developers.waalaxy.com` — use that.)

## Authentication

The Waalaxy API uses **API key authentication**. Every request must include an `Authorization` header with the **Bearer** scheme.

```
Authorization: Bearer YOUR_KEY_HERE
```

> The `Authorization` header is used to authenticate with the API using your API key. Value is of the format `Bearer YOUR_KEY_HERE`.

### Getting your API key

1. Sign in to your Waalaxy account.
2. Open the **CRM Sync** settings page.
3. Click **Generate API key** and copy the value (displayed only once).
4. Store the key in a secure secret manager (or your integration tool's credential store). Keep your API key secure and never share it publicly. Revoke and regenerate if compromised.

(API access is available on the Advanced and Business plans only.)

### Required headers

| Header | Value | When |
|---|---|---|
| `Authorization` | `Bearer YOUR_KEY_HERE` | all requests |
| `Content-Type` | `application/json` | requests with a JSON body |

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/integrations/test` | Validate API key connectivity |
| GET | `/prospectLists/getProspectLists` | Retrieve prospect lists |
| GET | `/campaigns/getAll` | Retrieve campaigns (paused/running) |
| POST | `/prospects/addProspectFromIntegration` | Import / enroll prospects |

---

### GET `/integrations/test` — Test connection

Tests the API connection and validates the API key passed in the `Authorization` header.

```bash
curl --request GET \
  --url https://developers.waalaxy.com/integrations/test \
  --header 'Authorization: Bearer YOUR_KEY_HERE'
```

**Response (200):**
```json
true
```

---

### GET `/prospectLists/getProspectLists` — Get prospect lists

Retrieves all prospect lists owned by the authenticated user. Each list contains its identifier, name, total number of prospects, and visual settings. No query parameters.

```bash
curl --request GET \
  --url https://developers.waalaxy.com/prospectLists/getProspectLists \
  --header 'Authorization: Bearer YOUR_KEY_HERE'
```

**Response (200):**
```json
[
  {
    "_id": "695b86fe3b6b619338a0e14a",
    "user": "690870a9ae969db382d4b424",
    "name": "waapi",
    "totalProspects": 29,
    "iconColor": "#000000",
    "iconLabel": "Waalaxy"
  }
]
```

| Field | Type | Notes |
|---|---|---|
| `_id` | string | Prospect list identifier |
| `user` | string | User ID |
| `name` | string | List name |
| `totalProspects` | number | Count of prospects in list |
| `iconColor` | string | Hex color code for list icon |
| `iconLabel` | string | Label text for list icon |

---

### GET `/campaigns/getAll` — Get campaigns

Retrieves all campaigns owned by the authenticated user that have a **"paused" or "running" status**, returning their total count, identifiers, and names.

```bash
curl --request GET \
  --url https://developers.waalaxy.com/campaigns/getAll \
  --header 'Authorization: Bearer YOUR_KEY_HERE'
```

**Response (200):**
```json
{
  "total": 4,
  "campaigns": [
    { "_id": "6967ccd7cd1b75dbab178b35", "name": "Email Finder" },
    { "_id": "6967ccd7cd1b75dbab178b36", "name": "Email Finder 2" },
    { "_id": "6967ccd7cd1b75dbab178b37", "name": "Email Finder 3" },
    { "_id": "6967ccd7cd1b75dbab178b38", "name": "Email Finder 4" }
  ]
}
```

---

### POST `/prospects/addProspectFromIntegration` — Import / enroll prospects

Imports one or more prospects into a prospect list, optionally enrolling them into a campaign.

**Request body schema:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `prospects` | object[] | Yes | Minimum 1 item. Each prospect requires a LinkedIn URL. |
| `prospectListId` | string | Yes | ID of the destination prospect list. |
| `origin` | object | Yes | Tracks import source; `name` field identifies the integration. |
| `campaignId` | string | No | Optional campaign enrollment ID. |
| `canCreateDuplicates` | boolean | No | Defaults to `false`. Requires special permission. |
| `moveDuplicatesToOtherList` | boolean | No | Defaults to `false`. Moves existing prospects instead of skipping. |
| `shouldOverwriteCustomProfileData` | boolean | No | Defaults to `false`. When `true`, overwrites existing data. |
| `addExistingProspectInCampaign` | boolean | No | Defaults to `false`. Enrolls existing CRM prospects in the campaign. |

**Prospect object fields:**

| Field | Type | Notes |
|-------|------|-------|
| `url` | string | LinkedIn profile URL (required per prospect) |
| `customProfile` | object | Optional: `firstName`, `lastName`, `email` |
| `customVariables` | object[] | Optional: `label`/`value` pairs |

**`origin` field:** mandatory; `name` identifies the source. Use `make`, `zapier`, or `n8n` for native integrations; custom values appear prefixed with `API-` in the interface.

**Example request (cURL):**
```bash
curl --request POST \
  --url https://developers.waalaxy.com/prospects/addProspectFromIntegration \
  --header 'Authorization: Bearer YOUR_KEY_HERE' \
  --header 'Content-Type: application/json' \
  --data '{
    "prospects": [
      {
        "url": "https://www.linkedin.com/in/john-doe-123456",
        "customProfile": {
          "firstName": "John",
          "lastName": "Doe",
          "email": "john@example.com"
        },
        "customVariables": [
          { "label": "Company size", "value": "500" }
        ]
      }
    ],
    "prospectListId": "695b86fe3b6b619338a0e14a",
    "campaignId": "6967ccd7cd1b75dbab178b35",
    "origin": { "name": "make" },
    "canCreateDuplicates": false,
    "moveDuplicatesToOtherList": false,
    "shouldOverwriteCustomProfileData": false,
    "addExistingProspectInCampaign": false
  }'
```

**Example response (200; same shape on 429):**
```json
{
  "result": [
    {
      "importCode": "success",
      "addToCampaignCode": "success",
      "prospect": {
        "_id": "695b86fe3b6b619338a0e14b",
        "profile": {
          "firstName": "John",
          "lastName": "Doe",
          "publicIdentifier": "john-doe-123456",
          "memberId": "ACoAAB1234",
          "salesMemberId": "ACwAAB1234"
        }
      }
    },
    {
      "importCode": "duplicated_prospect",
      "prospect": {
        "profile": {
          "firstName": "Jane",
          "lastName": "Smith",
          "publicIdentifier": "jane-smith",
          "memberId": "ACoAAB5678",
          "salesMemberId": "ACwAAB5678"
        }
      },
      "message": "Prospect already exists in another list."
    }
  ]
}
```

`importCode` reflects per-prospect outcome (`success`, `duplicated_prospect`, …); when a `campaignId` was supplied, `addToCampaignCode` reflects enrollment outcome.

## Errors

Responses follow the **RFC 7807 Problem Details** standard, including `type`, `title`, `status`, `detail`, and `instance` fields.

```json
<!-- Constructed from docs — verify against live API -->
{
  "type": "about:blank",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Invalid or missing API key.",
  "instance": "/prospects/addProspectFromIntegration"
}
```

Handle `401` (missing/invalid key, or a plan without API access) and back off on `429`.

## Rate limits

Not specified in the developer documentation. Apply your own throttling/backoff. The practical ceiling on outreach volume is the per-plan **monthly LinkedIn invitation cap** (Free 80 / Pro 300 / Advanced & Business 800) plus Waalaxy's deliberate daily ramp, not an API request-rate limit.

## Webhooks

No outbound webhook (e.g. reply/connection events) is documented in the public Waalaxy developer API as of this capture. For reply handling, use the native HubSpot/Pipedrive sync, the Make/Zapier/n8n connectors, or poll. (Some iPaaS marketplaces expose Waalaxy triggers via polling.)

## Native integrations & iPaaS

- **CRM**: HubSpot, Pipedrive (native sync).
- **iPaaS**: Make, Zapier, n8n (documented `origin.name` values for imports).
- **Other connector marketplaces** listing Waalaxy: noCRM, Pabbly Connect, ApiX-Drive.
- **CSV**: full import/export with history.
