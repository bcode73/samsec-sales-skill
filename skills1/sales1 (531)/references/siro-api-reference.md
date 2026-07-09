<!-- Source: https://docs.siro.ai/getting-started -->

# Siro API Reference

## Authentication & Base URLs

**Main API Base URL:**
```
https://functions.siro.ai/api-externalApi/v1
```

**Alternative API Base URL (for recordings/entities):**
```
https://api.siro.ai
```

**Authentication Methods:**
- Organization API Token: `Authorization: Bearer <token>` header
- OAuth Access Token: `x-siro-auth-token: <token>` header

---

## Core Endpoints

### 1. Sync Engagements
**Method:** `PUT`
**Endpoint:** `/v1/integrations/sync/engagements`
**Authentication:** Organization API Token

**Required Fields:**
- `externalId` (string)
- `startTime` (ISO 8601)
- `endTime` (ISO 8601)
- `subject` (string)
- `engagementType.activityType` (MEETING, CALL, APPOINTMENT, EMAIL, TEXT, EVENT — note: only MEETING, APPOINTMENT, and EVENT surface in the in-app Appointment List feature)
- `engagementUsers` (array)

**Optional Fields:**
- `account.externalId`
- `opportunity.externalId`

---

### 2. Sync Opportunities
**Method:** `PUT`
**Endpoint:** `/v1/integrations/sync/opportunities`
**Authentication:** Organization API Token

**Required Fields:**
- `externalId` (string)
- `name` (string)

**Optional Fields:**
- `amount` (number)
- `closedAt` (ISO 8601)
- `disposition` (WON, LOST, etc.)
- `account.externalId`
- `opportunityUsers` (array)

---

### 3. Get Engagement Details
**Method:** `GET`
**Endpoint:** `/v1/integrations/engagements/{id}`
**Authentication:** Organization API Token

**Response Fields:**
- `id`, `externalId`, `recordingId`, `engagementType`, `opportunityId`, `accountId`

---

### 4. Get Recording Details
**Method:** `GET`
**Endpoint:** `/v1/core/recordings/{recordingId}`
**Base URL:** `https://api.siro.ai`
**Authentication:** OAuth Access Token

**Query Parameters:**
- `showSummary` (boolean, default: false)
- `showEntityExtractions` (boolean, default: false)

**Response Includes:**
- `summary` (concatenated LLM summary)
- `entityExtractions` (array with CRM field mappings)

---

### 5. Get Entity Extractions
**Method:** `GET`
**Endpoint:** `/v1/core/entities/extractions/{recordingId}`
**Base URL:** `https://api.siro.ai`
**Authentication:** OAuth Access Token

**Response:** Array of extraction objects with `name`, `value`, `mappings`

---

### 6. Get Recording Summaries
**Method:** `GET`
**Endpoint:** `/v1/core/recordings/{recordingId}/summaries`
**Authentication:** Organization API Token

**Response Fields:** `id`, `name`, `content`

---

### 7. List Mobile Events
**Method:** `GET`
**Endpoint:** `/v1/core/mobile-events`
**Base URL:** `https://functions.siro.ai/api-externalApi/v1`
**Authentication:** Organization API Token (Bearer)

**Query Parameters:**
- `pageSize` (e.g. `pageSize=100`)

Returns mobile app events. Documented in the official quickstart as the canonical example call for verifying organization API token auth. Response schema and full pagination mechanics beyond `pageSize` are not specified in the official docs.

---

## OAuth Endpoints

### Create OAuth App
**Method:** `POST`
**Endpoint:** `/v1/core/oauth/apps`
**Required Fields:** `appName`, `owner` (user-id), `organizationId`

### Generate OAuth Token
**Method:** `POST`
**Endpoint:** `/v1/core/oauth/apps/{clientId}/access-token`
**Required Fields:** `clientSecret`, `userId`, `scope: "read"`
**Token Lifespan:** 16 hours

---

## Webhook Events

**Supported Event Types:**
- `integrations.recordingProcessed` — fired when recording processing completes
- `integrations.recordingLinked` — fired when recording links to CRM record

**Payload Structure:**
```json
{
  "recordingId": "rec-abc-def",
  "siroUserId": "siro-user-123",
  "recordingProcessed": true,
  "recordingLinked": true,
  "eventType": "integrations.recordingProcessed",
  "crm": {
    "integrationConnectionId": "conn-123",
    "users": [{ "id": "user-uuid", "externalId": "crm-user-123" }],
    "engagement": { "id": "eng-uuid", "externalId": "appt-456" },
    "opportunity": { "id": "opp-uuid", "externalId": "opp-101" },
    "account": { "id": "acct-uuid", "externalId": "account-789" }
  }
}
```

Each `crm` object carries both Siro's internal `id` (UUID) and the native CRM `externalId`. Pair `externalId` with `integrationConnectionId` when targeting a specific CRM connection. The `crm.users[]` array maps Siro users to CRM user external IDs. **Process the event only when both `recordingProcessed` and `recordingLinked` are `true`.**

**Webhook Headers for Verification (Svix):**
- `svix-id` — unique message identifier
- `svix-timestamp` — epoch seconds
- `svix-signature` — base64 signature(s) in the format `v1,<signature>`

---

## Deep Linking Format

```
siro://record?appointmentId={external-id}&title={customer-name}&opportunityId={opp-external-id}
```
