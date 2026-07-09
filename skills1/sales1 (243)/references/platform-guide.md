# Inbox Zero Platform Reference

## Overview

Open-source AI email assistant (~11.2K GitHub stars, as of 2026-06-13) that auto-labels, drafts replies in your voice, blocks cold emails, bulk unsubscribes, and lets you write automation rules in plain English. Works with Gmail and Outlook. Self-hostable via Docker. SOC 2 Type 2 certified.

## Capabilities & automation surface

| Capability | Description | Surface |
|---|---|---|
| AI auto-labeling | Categorizes incoming emails by priority/type | UI + rules via API |
| Reply drafting | Generates drafts in your voice from sent email history | UI-only |
| Automation rules | Plain-English rules (label, archive, draft, forward) | API + CLI + UI |
| Bulk unsubscribe | One-click newsletter removal | UI-only |
| Cold email blocking | AI-powered unsolicited email filter | UI-only |
| Email analytics | Communication patterns, response times, volume | API + CLI + UI |
| Attachment filing | Auto-save PDFs/docs to Google Drive or OneDrive | UI-only (Plus+) |
| Meeting briefings | Pre-meeting context from email + calendar | UI-only |
| Slack/Telegram digest | Email summaries pushed to messaging apps | UI-only (Plus+) |
| Bulk archive | Mass archive old emails matching criteria | UI-only |

## Pricing, limits & plan gates

| Feature | Starter $18/mo | Plus $28/mo | Professional $42/mo |
|---|---|---|---|
| Email accounts | 1 | 2 | 2+ (team) |
| AI labeling & drafts | Yes | Yes | Yes |
| Cold email blocking | Yes | Yes | Yes |
| Bulk unsubscribe | Yes | Yes | Yes |
| Analytics | Basic | Full | Team-wide |
| Slack integration | No | Yes | Yes |
| Telegram integration | No | Yes | Yes |
| Attachment filing | No | Yes | Yes |
| Knowledge base | No | Unlimited | Unlimited |
| Email digests | No | Yes | Yes |
| Priority support | No | No | Yes |
| Dedicated onboarding | No | No | Yes |

- **Prices above are per user / month, billed monthly** (verified 2026-06-13). Annual billing
  is cheaper per month: Starter $14.40/mo (save 10%), Plus $22.40/mo (save 20%),
  Professional $35.28/mo (save 16%).
- 7-day free trial on all plans; 14-day money-back guarantee (email within 14 days of upgrading)
- Enterprise: custom pricing for SSO, SCIM, on-premise deployment, dedicated account manager
- **Self-hosted: free** — BYO infrastructure (Docker + PostgreSQL + Google Cloud for PubSub)
- API access included on all paid plans; self-hosted requires `NEXT_PUBLIC_EXTERNAL_API_ENABLED=true` (plus `API_KEY_SALT`)

## Integrations

| Integration | Direction | Plan required |
|---|---|---|
| Gmail | Bidirectional (read/label/archive/draft) | All |
| Outlook | Bidirectional | All |
| Google Drive | Write (attachment filing) | Plus+ |
| OneDrive | Write (attachment filing) | Plus+ |
| Google Calendar | Read (meeting context for drafts) | All |
| Slack | Write (email digests, channel notifications) | Plus+ |
| Telegram | Write (email digests) | Plus+ |
| Microsoft Teams | AI assistant chat in DMs (setup doc live; channel digests/attachment notifications are Slack-only) | See docs |

**No Zapier/Make/iPaaS.** The only programmatic interfaces are the REST API and CLI.

## Data model

### Automation Rule

<!-- Verified against live OpenAPI 2026-06-13. A rule uses a structured `condition`
     object + `actions` array — NOT a flat `instructions` string, and there is no
     `automate` field. -->
```json
{
  "id": "rule_abc123",
  "name": "Label client emails as Priority",
  "enabled": true,
  "runOnThreads": true,
  "createdAt": "2026-04-20T10:30:00Z",
  "updatedAt": "2026-04-20T10:30:00Z",
  "condition": {
    "conditionalOperator": "AND",
    "aiInstructions": "If the email is from a client domain, treat as priority and draft a brief acknowledgment",
    "static": { "from": "@acme.com", "to": null, "subject": null }
  },
  "actions": [
    { "type": "LABEL", "fields": { "label": "Priority" } },
    { "type": "DRAFT_EMAIL" }
  ]
}
```

`actions[].type` is one of 15 `ActionType` values: `LABEL`, `ARCHIVE`, `MARK_READ`,
`STAR`, `DRAFT_EMAIL`, `DRAFT_MESSAGING_CHANNEL`, `REPLY`, `FORWARD`, `SEND_EMAIL`,
`MARK_SPAM`, `DIGEST`, `CALL_WEBHOOK`, `MOVE_FOLDER`, `NOTIFY_MESSAGING_CHANNEL`,
`NOTIFY_SENDER`. The `CALL_WEBHOOK` action POSTs to `actions[].fields.webhookUrl`.

### Stats by period (GET /stats/by-period)

<!-- Verified against live OpenAPI 2026-06-13. -->
```json
{
  "result": [
    { "startOfPeriod": "2026-06-01", "All": 342, "Sent": 87,
      "Read": 300, "Unread": 42, "Unarchived": 127, "Archived": 215 }
  ],
  "allCount": 342, "inboxCount": 127, "readCount": 300, "sentCount": 87
}
```

### Stats response time (GET /stats/response-time)

```json
{
  "summary": { "medianResponseTime": 45, "averageResponseTime": 62,
    "within1Hour": 0.58, "previousPeriodComparison": { "medianResponseTime": 51, "percentChange": -11.8 } },
  "distribution": { "lessThan1Hour": 120, "oneToFourHours": 80, "fourTo24Hours": 60,
    "oneToThreeDays": 30, "threeToSevenDays": 10, "moreThan7Days": 4 }
}
```

## Quick-start recipes

### Recipe 1: List and create rules via CLI

**Use case:** Manage email automation rules from Claude Code or any AI coding agent.

```bash
# Install CLI
npm install -g @inbox-zero/api

# Authenticate
export INBOX_ZERO_API_KEY=iz_your_key_here

# List all rules as JSON
npx @inbox-zero/api rules list --json

# Create a new rule from stdin (condition + actions required, no flat "instructions")
echo '{
  "name": "Archive marketing emails",
  "condition": {
    "conditionalOperator": "AND",
    "aiInstructions": "If the email is a marketing newsletter and I have not replied to this sender in the last 30 days"
  },
  "actions": [ { "type": "ARCHIVE" }, { "type": "LABEL", "fields": { "label": "Newsletters" } } ]
}' | npx @inbox-zero/api rules create

# Get inbox stats for the past week
npx @inbox-zero/api stats by-period --period week --json
```

**Gotcha:** The CLI requires an API key from Settings → API Keys in the Inbox Zero dashboard. Self-hosted users must set `NEXT_PUBLIC_EXTERNAL_API_ENABLED=true` (and `API_KEY_SALT`).

### Recipe 2: Manage rules via REST API

**Use case:** Programmatically CRUD automation rules from your own app or script.

```bash
# List all rules
curl -H "API-Key: iz_your_key" \
  https://www.getinboxzero.com/api/v1/rules

# Create a rule (name + condition + actions are required)
curl -X POST -H "API-Key: iz_your_key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flag urgent client emails",
    "condition": {
      "conditionalOperator": "AND",
      "aiInstructions": "If subject contains URGENT and sender is from a known client domain",
      "static": { "subject": "URGENT" }
    },
    "actions": [ { "type": "LABEL", "fields": { "label": "Urgent" } }, { "type": "DRAFT_EMAIL" } ]
  }' \
  https://www.getinboxzero.com/api/v1/rules

# Delete a rule
curl -X DELETE -H "API-Key: iz_your_key" \
  https://www.getinboxzero.com/api/v1/rules/rule_abc123
```

**Self-hosted base URL:** Replace `https://www.getinboxzero.com` with your deployment URL.

### Recipe 3: Self-hosted deployment with Docker

**Use case:** Run Inbox Zero for free on your own infrastructure.

```bash
# Install CLI (requires Docker + Node.js v24+)
npm install -g @inbox-zero/cli
# or: brew install inbox-zero/inbox-zero/inbox-zero

# Interactive setup (configures OAuth, database, PubSub)
npx @inbox-zero/cli setup

# Start the application (containers)
npx @inbox-zero/cli start

# Access at http://localhost:3000
```

**Prerequisites:**
- Docker running
- Node.js v24+
- Google Cloud project with Gmail API + PubSub API enabled
- OAuth 2.0 credentials (client ID + secret)
- PostgreSQL database (Docker Compose includes one)

**Common failure:** Missing `GOOGLE_PUBSUB_TOPIC_NAME` env var — Gmail push notifications won't work without it.

## Integration patterns

### AI agent integration (Claude Code / Codex)

The CLI is designed for AI agent consumption — all commands support `--json` output:

1. Agent reads rules: `npx @inbox-zero/api rules list --json`
2. Agent analyzes inbox stats: `npx @inbox-zero/api stats by-period --period day --json`
3. Agent creates/modifies rules based on user request (each rule needs `name` + `condition` + `actions`)
4. Agent confirms changes by re-reading rules

### REST API integration

- **Auth:** `API-Key: iz_...` header on every request (OpenAPI scheme `ApiKeyAuth`)
- **Base URL:** `https://www.getinboxzero.com/api/v1` (hosted) or `https://your-domain.com/api/v1` (self-hosted)
- **Endpoints:** Rules CRUD (`GET/POST /rules`, `GET/PUT/DELETE /rules/{id}`) and analytics (`GET /stats/by-period`, `GET /stats/response-time`). There is no `/group-emails` endpoint in the live spec; the public surface is just `/rules` + `/stats`.
- **Format:** JSON request/response
- **Rate limits:** Not publicly documented — treat as standard SaaS (respect 429 responses, exponential backoff)
- **Pagination:** Not documented in the OpenAPI spec

### Webhook / push notifications (self-hosted only)

Self-hosted deployments use Google PubSub for real-time Gmail notifications:
1. Gmail detects new email → pushes to PubSub topic
2. PubSub delivers to Inbox Zero's webhook endpoint
3. Rule engine evaluates the email against all enabled rules
4. Actions execute (label, archive, draft, etc.)

The hosted version handles this automatically — no user configuration needed.
