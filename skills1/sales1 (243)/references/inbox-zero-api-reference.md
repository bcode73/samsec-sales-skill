<!-- Source: https://docs.getinboxzero.com/api-reference/introduction + https://docs.getinboxzero.com/openapi.json + https://docs.getinboxzero.com/api-reference/cli — re-verified 2026-06-13 -->

# Inbox Zero API Reference

## Authentication

Include your API key in the header of each request:

```
API-Key: iz_your_key_here
```

Generate API keys from: Inbox Zero dashboard → Settings → API Keys. Select desired permissions and expiry period.

## Base URL

**Hosted (production):** `https://www.getinboxzero.com/api/v1`
**Local development:** `http://localhost:3000/api/v1`
**Self-hosted:** `https://your-domain.com/api/v1` (requires `NEXT_PUBLIC_EXTERNAL_API_ENABLED=true` plus `API_KEY_SALT`)

Security scheme (OpenAPI): `ApiKeyAuth` — `apiKey` in header named `API-Key`.

## Supported Providers

- Gmail (Google Workspace and personal)
- Outlook (Microsoft 365 and personal)

## Endpoints

### Rules

| Method | Path | Description |
|---|---|---|
| GET | `/rules` | List automation rules for the scoped inbox account |
| POST | `/rules` | Create an automation rule for the scoped inbox account |
| GET | `/rules/{id}` | Get a single automation rule |
| PUT | `/rules/{id}` | Replace an automation rule |
| DELETE | `/rules/{id}` | Delete an automation rule |

#### Rule data model (verified against OpenAPI 2026-06-13)

A rule does **not** use a flat `instructions` string. It has a structured `condition`
object plus an `actions` array. Both `condition` and `actions` (min 1) are required
when creating/replacing a rule.

`Rule` response object:
```json
{
  "id": "rule_abc123",
  "name": "Label client emails",
  "enabled": true,
  "runOnThreads": true,
  "createdAt": "2026-04-20T10:30:00Z",
  "updatedAt": "2026-04-20T10:30:00Z",
  "condition": {
    "conditionalOperator": "AND",
    "aiInstructions": "If the email is from a client domain, treat as priority",
    "static": { "from": "@acme.com", "to": null, "subject": null }
  },
  "actions": [
    { "type": "LABEL", "fields": { "label": "Priority" } }
  ]
}
```

`RuleRequestBody` (POST/PUT) — required: `name`, `condition`, `actions` (minItems 1);
optional `runOnThreads` (default `true`). There is **no** `automate` field.

`ActionType` enum (15 values): `LABEL`, `ARCHIVE`, `MARK_READ`, `STAR`, `DRAFT_EMAIL`,
`DRAFT_MESSAGING_CHANNEL`, `REPLY`, `FORWARD`, `SEND_EMAIL`, `MARK_SPAM`, `DIGEST`,
`CALL_WEBHOOK`, `MOVE_FOLDER`, `NOTIFY_MESSAGING_CHANNEL`, `NOTIFY_SENDER`.

`RuleAction` fields: `type` (required), `messagingChannelId`, `delayInMinutes`, and a
`fields` object holding `label`, `to`, `cc`, `bcc`, `subject`, `content`, `webhookUrl`
(target for `CALL_WEBHOOK`), `folderName`. `RuleCondition`: `conditionalOperator`
(`AND`/`OR`), `aiInstructions` (the plain-English instruction), and a `static`
object (`from`/`to`/`subject`).

#### List rules

```bash
curl -H "API-Key: iz_your_key" \
  https://www.getinboxzero.com/api/v1/rules
```

Response: `{ "rules": [ Rule, ... ] }`.

#### Get rule

```bash
curl -H "API-Key: iz_your_key" \
  https://www.getinboxzero.com/api/v1/rules/rule_abc123
```

#### Create rule

```bash
curl -X POST -H "API-Key: iz_your_key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Archive newsletters",
    "condition": {
      "conditionalOperator": "AND",
      "aiInstructions": "If the email is a newsletter I have not read in 30 days"
    },
    "actions": [ { "type": "ARCHIVE" } ]
  }' \
  https://www.getinboxzero.com/api/v1/rules
```

#### Replace rule

```bash
curl -X PUT -H "API-Key: iz_your_key" \
  -H "Content-Type: application/json" \
  -d '{ "name": "Archive newsletters", "condition": {...}, "actions": [{"type":"ARCHIVE"}] }' \
  https://www.getinboxzero.com/api/v1/rules/rule_abc123
```

#### Delete rule

```bash
curl -X DELETE -H "API-Key: iz_your_key" \
  https://www.getinboxzero.com/api/v1/rules/rule_abc123
```

### Analytics

| Method | Path | Description |
|---|---|---|
| GET | `/stats/by-period` | Email statistics grouped by time period |
| GET | `/stats/response-time` | Email response-time statistics (summary + distribution + trend) |

#### Stats by period

```bash
curl -H "API-Key: iz_your_key" \
  "https://www.getinboxzero.com/api/v1/stats/by-period?period=week"
```

Query params: `period` (`day`|`week`|`month`|`year`, default `week`), optional
`fromDate`/`toDate` (numeric, nullable). Response:
```json
{
  "result": [
    { "startOfPeriod": "2026-06-01", "All": 342, "Sent": 87,
      "Read": 300, "Unread": 42, "Unarchived": 127, "Archived": 215 }
  ],
  "allCount": 342, "inboxCount": 127, "readCount": 300, "sentCount": 87
}
```

#### Stats response time

```bash
curl -H "API-Key: iz_your_key" \
  "https://www.getinboxzero.com/api/v1/stats/response-time"
```

Query params: optional `fromDate`/`toDate` (numeric, nullable). Response has a
`summary` (`medianResponseTime`, `averageResponseTime`, `within1Hour`,
`previousPeriodComparison`) and a `distribution` (`lessThan1Hour`, `oneToFourHours`,
`fourTo24Hours`, `oneToThreeDays`, `threeToSevenDays`, `moreThan7Days`).

<!-- NOTE: the previously-documented GET /group-emails "learned patterns" endpoint
     is NOT present in the live OpenAPI spec (docs.getinboxzero.com/openapi.json,
     verified 2026-06-13). The introduction invites requesting new endpoints via
     GitHub, so the public API surface is currently just /rules and /stats. -->

## CLI Wrapper

The CLI wraps the REST API with JSON-first output for AI agent consumption.

```bash
# Install
npm install -g @inbox-zero/api

# Authenticate
export INBOX_ZERO_API_KEY=iz_your_key

# Commands (binary is `inbox-zero-api`)
npx @inbox-zero/api rules list [--json]
npx @inbox-zero/api rules get <rule_id> [--json]
npx @inbox-zero/api rules create [--file <path>]   # else reads stdin JSON
npx @inbox-zero/api rules update <rule_id> [--file <path>]
npx @inbox-zero/api rules delete <rule_id>
npx @inbox-zero/api stats by-period [--period day|week|month|year] [--json]
npx @inbox-zero/api stats response-time [--json]
npx @inbox-zero/api openapi [--json]               # Fetch live OpenAPI schema
```

Config: `INBOX_ZERO_API_KEY` (required), optional `INBOX_ZERO_BASE_URL` (or `--base-url`)
for self-hosted. Config file: `~/.inbox-zero-api/config.json`.

## Gaps

- Pagination pattern not documented in the OpenAPI spec.
- Rate limits not documented — treat as standard SaaS, respect 429 responses.
- No *inbound* webhook/event-notification API for rule executions. (There IS an
  outbound `CALL_WEBHOOK` rule action that POSTs to a `webhookUrl` you set, gated by
  `NEXT_PUBLIC_WEBHOOK_ACTION_ENABLED` on self-hosted; the signing scheme for those
  outbound calls is not documented in the public docs — UNVERIFIED, do not assume a
  specific signature header.)
- No direct email read/send/archive REST endpoints — the public API is limited to
  `/rules` and `/stats`. (Email actions like SEND_EMAIL, REPLY, FORWARD, ARCHIVE,
  MARK_SPAM, MOVE_FOLDER, FORWARD exist only as rule *actions*, executed by the rule
  engine — not as standalone API calls.)
- The hosted OpenAPI spec is at `https://docs.getinboxzero.com/openapi.json` (also via
  `npx @inbox-zero/api openapi --json`).
