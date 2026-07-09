# Bliro Platform Reference

## Overview

Bot-free AI meeting assistant for sales teams. Captures online and in-person meetings via system audio (no visible bot), generates AI summaries, syncs to CRM at field level, and provides anonymous sales coaching. German-based (Munich), GDPR/ISO 27001/SOC 2 compliant, data stored in Germany. Founded 2022, Series A ($2.93M).

## Capabilities & automation surface

| Capability | Description | Access |
|---|---|---|
| Transcription | Real-time transcription in 50+ languages, bot-free via system audio | All plans |
| AI Summaries | Custom summary templates, auto-generated after each meeting | All plans |
| AI Documentation | Voice-input documentation (speak notes, Bliro structures them) | All plans |
| Ask Bliro | AI Q&A across your meeting history | All plans |
| Calendar Integration | Auto-detects meetings from Google Calendar / Outlook | All plans |
| Groups & Collaboration | Share meeting notes with team members | All plans |
| CRM Integration | Field-level sync to Salesforce, HubSpot, SAP, Dynamics 365 | For Revenue Teams+ |
| AI Conversation Analytics | Talk ratios, sentiment, topic tracking | For Revenue Teams+ |
| AI Sales Coaching | Anonymous playbook-based coaching, no ride-alongs or recordings shared | For Revenue Teams+ |
| AI Meta Analytics | Cross-meeting trend analysis | For Revenue Teams+ |
| API Access | OAuth 2.0, `GET /v3/calls` for all org calls | For Revenue Teams+ (bundled with CRM, verified 2026-06-13) |
| Webhook Events | POST on call completion with full transcript + summary | For Revenue Teams+ (bundled with CRM, verified 2026-06-13) |
| SSO | SAML single sign-on | Enterprise only |
| Custom AI Models | Fine-tuning for industry terminology | Enterprise only |
| Proxy/Firewall Support | Organization-wide network configuration | Enterprise only |

## Pricing, limits & plan gates

*Re-verified 2026-06-13 against bliro.io/en/pricing and the help-center pricing article. Bliro moved to a sales-led, 3-tier structure and NO LONGER publishes euro prices or a public free tier on its official pages — pricing is "talk to a human" / book-a-demo. The older Free / Professional €49 / Unlimited €89 numbers are no longer shown on any official Bliro page (only third-party aggregators still cite them) — treat any euro figure as unverified until confirmed with Bliro sales.*

| Plan | Price (official) | CRM | API/Webhooks | SSO / Custom AI | Notes / user minimum |
|---|---|---|---|---|---|
| **Standard** | Sales-led (not public) | No | No | No | Unlimited GDPR transcription 50+ languages, AI summaries, voice docs, calendar, collaboration. Min. 20 users. |
| **For Revenue Teams** | Sales-led (not public) | Yes (Salesforce, HubSpot, SAP, Dynamics) | **Yes — API + Webhooks bundled here** | No | Everything in Standard + CRM integration, AI Conversation Analytics, AI Sales Coaching, **Bliro API and Webhook Access**. Min. 10 users. |
| **Enterprise** | Custom | Yes | Yes | Yes — SSO + custom AI models | Everything above + custom AI models & fine-tuning, SSO, priority support, org-wide admin controls. Requires 50 Standard or 20 Revenue Team licenses. |

**Plan gate gotchas (verified 2026-06-13):**
- **API and webhooks are now bundled with CRM in the "For Revenue Teams" plan** — they are NOT a separate higher tier above CRM anymore. If you have CRM integration on the revenue-teams plan you also have API + Webhook Access.
- The **"Standard"** plan has NO CRM, NO API, NO webhooks.
- Custom AI models require Enterprise.
- SSO requires Enterprise.
- There are **user minimums** (Standard ≥20, For Revenue Teams ≥10, Enterprise ≥50 Standard or ≥20 Revenue Team licenses) — not a per-seat self-serve free signup.

## Integrations

| Integration | Direction | Plan required | Notes |
|---|---|---|---|
| Salesforce | Bliro → SF (write) | For Revenue Teams+ | Task, Event, or Call objects on Opportunities/Accounts/Contacts |
| HubSpot | Bliro → HS (write) | For Revenue Teams+ | Activity Timeline for Deals, Accounts, Contacts |
| SAP | Bliro → SAP (write) | For Revenue Teams+ | Details not publicly documented |
| Microsoft Dynamics 365 | Bliro → Dynamics (write) | For Revenue Teams+ | Details not publicly documented |
| Google Calendar | Read | All plans | Auto-detects upcoming meetings |
| Microsoft Outlook | Read | All plans | Auto-detects upcoming meetings |
| Slack | Bliro → Slack (write) | All plans | Share meeting summaries to channels |
| Confluence | Bliro → Confluence (write) | Unknown | Via webhook + Zapier/Make |
| Zoom | Audio capture | All plans | Bot-free system audio capture |
| Microsoft Teams | Audio capture | All plans | Bot-free system audio capture |
| Google Meet | Audio capture | All plans | Bot-free system audio capture |
| Zapier | Via webhooks | For Revenue Teams+ | Webhook trigger → any Zapier action |
| Make | Via webhooks | For Revenue Teams+ | Webhook trigger → any Make module |

## Data model

### Call object (from API / webhook payload)

```json
{
  "callData": {
    "_id": "unique-call-id",
    "type": "conversation",
    "status": "completed",
    "meta": {
      "title": "Auto-generated meeting title",
      "owner": {
        "userId": "user-123",
        "orgId": "org-456",
        "email": "rep@company.com",
        "name": "Sales Rep"
      },
      "participants": [
        {
          "name": "External Contact",
          "email": "contact@prospect.com",
          "crmId": "sf-contact-789"
        }
      ],
      "startTimestamp": 1704067200000,
      "endTimestamp": 1704070800000
    },
    "summaries": [
      {
        "label": "Key Points",
        "value": "Discussed pricing for Q2...",
        "format": "markdown"
      }
    ],
    "transcriptChunks": [
      {
        "speaker": "Sales Rep",
        "timestamp": 1704067200000,
        "text": "Thanks for joining today..."
      }
    ],
    "groups": ["team-sales"]
  },
  "timestamp": "2025-01-01T00:05:00.000Z"
}
```
<!-- Constructed from webhook docs — verify against live API -->

### Call types
- `"conversation"` — standard meeting (online or in-person)
- `"voice-memo"` — voice documentation input

## Quick-start recipes

### Recipe 1: List all calls from the past 7 days

**Trigger**: On-demand / scheduled job
**Steps**: Authenticate → GET /v3/calls with date filter → process results

```bash
# Step 1: Get access token
TOKEN=$(curl -s -X POST https://accounts.bliro.io/oauth/token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "client_credentials",
    "audience": "https://api.bliro.io",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
  }' | jq -r '.access_token')

# Step 2: List calls
curl -s https://api.bliro.io/v3/calls \
  -H "Authorization: Bearer $TOKEN" | jq '.[] | {id: ._id, title: .meta.title, start: .meta.startTimestamp}'
```

```python
import requests
from datetime import datetime, timedelta

# Authenticate
token_resp = requests.post("https://accounts.bliro.io/oauth/token", json={
    "grant_type": "client_credentials",
    "audience": "https://api.bliro.io",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
})
token = token_resp.json()["access_token"]

# List calls
calls = requests.get(
    "https://api.bliro.io/v3/calls",
    headers={"Authorization": f"Bearer {token}"},
).json()

for call in calls:
    print(f"{call['meta']['title']} — {call['meta']['owner']['name']}")
```

**Gotcha**: Token has an `expires_in` value — cache it and refresh before expiry. Filtering parameters are documented at `api.bliro.io/docs/#/Calls/get_v3_calls` (Swagger UI, may require JS).

### Recipe 2: Webhook receiver with HMAC signature verification

**Trigger**: Bliro fires POST on call completion
**Steps**: Verify signature → extract transcript → forward to downstream system

```python
import hmac
import hashlib
import json
from flask import Flask, request, abort

app = Flask(__name__)
BLIRO_WEBHOOK_SECRET = "your-security-token"

def verify_signature(parsed_payload: dict, signature_header: str) -> bool:
    """Verify Bliro webhook HMAC-SHA256 signature.

    NOTE (verified 2026-06-13): Bliro signs timestamp + "." + JSON.stringify(callData),
    i.e. ONLY the inner callData object — NOT the full raw request body. The official
    Node sample is: `${timestamp}.${JSON.stringify(payload.callData)}`.
    """
    # Bliro-Signature format: t=<timestamp>,v1=<hash>
    parts = dict(p.split("=", 1) for p in signature_header.replace(" ", "").split(","))
    timestamp = parts["t"]
    expected_sig = parts["v1"]

    # Sign timestamp + "." + JSON of callData ONLY. Match JS JSON.stringify output:
    # compact separators, no extra whitespace. Test against a real delivery first —
    # if key order/whitespace differs from Bliro's, extract the callData substring
    # from the raw body instead of re-serializing.
    call_data_json = json.dumps(
        parsed_payload["callData"], separators=(",", ":"), ensure_ascii=False
    )
    signed_payload = f"{timestamp}.{call_data_json}"
    computed = hmac.new(
        BLIRO_WEBHOOK_SECRET.encode(),
        signed_payload.encode(),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(computed, expected_sig)

@app.route("/webhook/bliro", methods=["POST"])
def handle_bliro_webhook():
    sig = request.headers.get("Bliro-Signature", "")
    if BLIRO_WEBHOOK_SECRET and not verify_signature(request.json, sig):
        abort(403)

    data = request.json
    call = data["callData"]
    print(f"Call: {call['meta']['title']}")
    print(f"Speakers: {[c['speaker'] for c in call['transcriptChunks'][:3]]}")
    print(f"Summary: {call['summaries'][0]['value'][:200]}")

    # Forward to your system here (BigQuery, Slack, CRM, etc.)
    return "", 200
```

**Gotcha**: Webhooks are deactivated by default — you must activate them at `app.bliro.io/orgs/settings/webhook` after creation. TLS 1.2+ required. Return 2xx promptly to avoid retries.

### Recipe 3: Sync Bliro calls to Slack via webhook

**Trigger**: Bliro webhook fires → forward summary to Slack channel
**Steps**: Receive webhook → extract summary → POST to Slack incoming webhook

```python
import requests

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/T.../B.../xxx"

def forward_to_slack(bliro_payload: dict):
    call = bliro_payload["callData"]
    title = call["meta"]["title"]
    owner = call["meta"]["owner"]["name"]
    summary = call["summaries"][0]["value"] if call["summaries"] else "No summary"
    participants = ", ".join(p["name"] for p in call["meta"].get("participants", []))

    slack_msg = {
        "text": f"*{title}*\n"
                f"Rep: {owner} | Participants: {participants}\n"
                f"Summary: {summary[:500]}"
    }
    requests.post(SLACK_WEBHOOK_URL, json=slack_msg)
```

## Integration patterns

### CRM sync architecture

Bliro handles CRM sync natively on the "For Revenue Teams" plan and above:
- **Salesforce**: Writes to Task, Event, or Call objects. Maps AI summary sections to CRM fields. Linked to Opportunities, Accounts, or Contacts based on participant email matching.
- **HubSpot**: Writes to Activity Timeline. Associated with Deals, Accounts, Contacts. Configured via HubSpot marketplace app.
- **SAP / Dynamics 365**: Native connectors, field mapping details not publicly documented.

For custom CRM sync beyond native connectors, use the webhook + API approach (same "For Revenue Teams" plan that bundles CRM, API, and webhooks):
1. Receive webhook with call data
2. Match participants to CRM records by email
3. Create/update CRM objects via CRM API
4. Store mapping in your middleware for reconciliation

### Webhook setup

1. Navigate to `app.bliro.io/orgs/settings/webhook`
2. Create webhook: name, HTTPS URL, optional security token
3. Click "Test Webhook" to verify endpoint
4. Activate the webhook (deactivated by default)
5. Webhooks fire once transcription is finalized and summary is generated

**Security**: Enable the security token for HMAC-SHA256 signature in `Bliro-Signature` header. Verify on every request.

### Batch pipeline (polling)

For backfilling or reconciliation:
1. Authenticate via OAuth 2.0 client credentials
2. `GET /v3/calls` with date/time filters
3. Page through results (pagination pattern undocumented — test with production data)
4. Store raw JSON, normalize for analytics

**Recommendation**: Use webhooks for real-time, polling for nightly reconciliation to catch missed events.
