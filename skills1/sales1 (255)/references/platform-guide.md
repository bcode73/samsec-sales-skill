# Instapage Platform Reference

## Overview

Instapage is a premium AI-powered **landing page + post-click optimization** platform (owned by airSlate) aimed at PPC/performance marketers, in-house marketing teams, agencies, and SaaS/SMB advertisers who run paid traffic and need high-converting, ad-matched landing pages. Its differentiators are **AdMap** (visually map ads → pages), deep **A/B testing + AI Experiments**, **Personalization / Dynamic Text Replacement**, and the **Thor Render Engine** for fast mobile/AMP pages. It is positioned at the high end on price; lower-cost alternatives are Landingi, Leadpages, Unbounce.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| Drag-and-drop builder | Pixel-precise page editor, Instablocks® reusable blocks | UI-only (pages are API-readable/creatable via `POST /pages/json`) |
| AI Content Generator | AI headlines, copy, CTAs, page variations | UI-only |
| AdMap® | Visualizes ad-campaign structure, maps ads → landing pages | UI-only |
| A/B testing + AI Experiments | Split-test variants; AI auto-allocates traffic to winners | UI-only (**Optimize+**) |
| Personalization / DTR | Dynamic Text Replacement + audience-based dynamic content | UI-only (**Optimize+**; ad-to-page personalization **Convert** only) |
| Heatmaps | Click/scroll/attention analytics | UI-only (**Convert** only) |
| Analytics | Visitors, conversions, rate, cost metrics | **API-accessible** (`GET /analytics`) |
| Pages | Create/update/publish/unpublish landing pages | **API-accessible** (`/pages`, `/pages/{id}/publication`) |
| Collections | Group page variations for audiences/campaigns | **API-accessible** (`/collections`) |
| Groups | Organize pages into groups | **API-accessible** (`/groups`) |
| Forms + Email | Lead-capture forms with autoresponder/email | Form leads via **API** (`/submissions`) + **per-form submit webhook** |
| Workspaces / Team | Multi-workspace, role-based team members | **API-accessible** (`/workspaces`, `/team-members`) |
| Global Blocks / Elements | Update reusable blocks across many pages at once | UI-only (Global Elements **Convert** only) |
| AMP + Thor Render Engine | Fast, mobile-optimized pages (~0.5s) | UI-only |

## Pricing, limits & plan gates

*Best-effort from research 2026-06 — verify against instapage.com/plans.*

| | Create | Optimize | Convert |
|---|---|---|---|
| **Price** | $99/mo | $199/mo (50k tier higher) | Custom (enterprise) |
| **Unique monthly visitors** | 15,000 | 30,000 / 50,000 | 50,000+ custom |
| **Conversions** | Unlimited | Unlimited | Unlimited |
| **Team members** | 10 | 10 | Custom |
| **Subdomains** | 2 | 10 | Custom |
| **Workspaces** | 1 | 5 | Custom |
| **A/B testing** | ✗ | ✓ | ✓ |
| **AI Experiments** | ✗ | ✓ | ✓ |
| **Personalization (DTR)** | ✗ | ✓ | ✓ |
| **Ad-to-page personalization** | ✗ | ✗ | ✓ |
| **Heatmaps** | ✗ | ✗ | ✓ |
| **Root-domain publishing** | ✗ | ✗ | ✓ |
| **Global Elements** | ✗ | ✗ | ✓ |
| **Direct Lead Bypass** | ✗ | ✗ | ✓ |
| **Enterprise SSO** | ✗ | ✗ | ✓ |
| **API calls/day** | 5,000 | 10,000–15,000 | 30,000+ |

- **Free trial**: 14 days (Create & Optimize only), 2,500-visitor cap, credit card required. Convert has no trial (demo required).
- **Rate limit (all plans)**: 200 requests/minute per token + IP, plus the daily quota above; both return **429 + `Retry-After`**, daily quota resets **00:00 UTC**.
- **Will my integration break on the free plan?** There is no free *plan* — only a 14-day trial. The cheapest paid plan (Create) still has API access (5,000 calls/day) but **no A/B testing** and **no heatmaps**.

## Integrations

- **120+ native integrations** incl. Salesforce, HubSpot, Mailchimp, Marketo, Zapier, Slack, Zendesk, Google Analytics, Shopify, WordPress, plus ad platforms (Google Ads, Facebook).
- **Data flow**: pages publish *out* to a subdomain (or root domain on Convert) or via the WordPress plugin; form submissions flow *out* to CRMs/ESPs via the per-form webhook or native form integrations; the **REST API** reads pages/collections/analytics/submissions and writes pages/workspaces/team members (bidirectional).
- **Zapier**: "New Form Submission" trigger is the common path to push leads into any tool without code.

## Data model

Key objects: **Workspace** → **Pages** / **Collections** / **Groups** / **Team Members**; **Submissions** (form leads) belong to a workspace. IDs are integers. Timestamps are Unix epoch seconds.

**Workspace (list response, verbatim shape):**
```json
{
  "data": [
    {
      "workspaceId": 1177,
      "ownerId": 1319,
      "workspaceName": "Personal Projects",
      "accessLevel": "owner",
      "createdAt": 1262304000
    }
  ],
  "meta": {
    "pagination": {
      "currentPage": 1,
      "perPage": 100,
      "totalItemsCount": 4,
      "totalPagesCount": 1
    }
  }
}
```

**Team member (list response, verbatim shape):**
```json
{
  "data": [
    {
      "userId": 4379,
      "email": "example_user@example.com",
      "invitedAt": 1685608225,
      "fullName": "John Smith",
      "accessLevel": "editor",
      "inheritOwnerContextInPublicApi": true,
      "invitationStatus": "accepted",
      "lastLoginAt": 1685608226,
      "lastActivityInWorkspaceAt": null
    }
  ],
  "meta": []
}
```

**Form submission (lead) — webhook payload shape** <!-- Constructed from docs — verify against live API. Instapage sends internal field IDs, not labels. -->
```json
{
  "field_1": "Jane Doe",
  "field_2": "jane@example.com",
  "field_3": "+1 555 0100",
  "page_id": 9910,
  "submitted_at": 1685608225
}
```

## Quick-start recipes

### Recipe 1 — Pull new form submissions and sync to a CRM (API poll)
Trigger: cron every N minutes. Steps: list workspaces → poll `/submissions` → upsert to CRM.

```bash
# 1. Find your workspace
curl "https://api.instapage.com/v1/workspaces" \
  -H "Authorization: Bearer API_KEY"

# 2. Pull form submissions (page through with ?page=N)
curl "https://api.instapage.com/v1/workspaces/1177/submissions?page=1" \
  -H "Authorization: Bearer API_KEY"
```

```python
import requests, time

TOKEN = "API_KEY"            # personal token from app.instapage.com/account
WORKSPACE = 1177
H = {"Authorization": f"Bearer {TOKEN}"}

def fetch_all_submissions(ws):
    page, out = 1, []
    while True:
        r = requests.get(
            f"https://api.instapage.com/v1/workspaces/{ws}/submissions",
            headers=H, params={"page": page})
        if r.status_code == 429:                       # rate limited
            time.sleep(int(r.headers.get("Retry-After", 60)))
            continue
        r.raise_for_status()
        body = r.json()
        out += body["data"]
        pg = body["meta"]["pagination"]
        if pg["currentPage"] >= pg["totalPagesCount"]:
            break
        page += 1
    return out

for lead in fetch_all_submissions(WORKSPACE):
    pass  # map field_1/field_2/... to CRM properties, then upsert
```
Gotcha: submissions use internal `field_N` keys, not your form labels — keep a field-map. `DELETE /submissions` removes up to 100 at a time and is irreversible.

### Recipe 2 — Real-time lead capture via the Form Submit webhook
Trigger: visitor submits a form. Steps: configure the webhook on the form → receive POST → ack within 20s → enqueue.

```python
from flask import Flask, request, jsonify
app = Flask(__name__)

FIELD_MAP = {"field_1": "name", "field_2": "email", "field_3": "phone"}

@app.post("/instapage-webhook")
def hook():
    payload = request.get_json(silent=True) or request.form.to_dict()
    lead = {FIELD_MAP.get(k, k): v for k, v in payload.items()}
    enqueue(lead)               # do CRM work async — DO NOT block
    return jsonify(ok=True), 200 # must return fast (<20s) or the page redirect breaks
```
Gotchas: no documented HMAC signature — validate the payload yourself (e.g. shared-secret query param, IP allowlist, or required hidden field). Use HTTPS. The 20-second timeout is on the *visitor's* thank-you/redirect, so always ack first and process in the background.

### Recipe 3 — Publish a page programmatically
Trigger: new campaign. Steps: create page JSON → publish.

```bash
# Create a page from JSON
curl -X POST "https://api.instapage.com/v1/workspaces/1177/pages/json" \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "name": "Spring Promo" }'

# Publish it (subdomain; root-domain publishing is Convert-only)
curl -X POST "https://api.instapage.com/v1/workspaces/1177/pages/9910/publication" \
  -H "Authorization: Bearer API_KEY"
```

## Integration patterns

- **CRM sync**: prefer the webhook for real-time + the `/submissions` poll as a nightly reconcile backstop (webhooks can be missed; there is no documented redelivery/signing). De-dupe on `page_id` + email + `submitted_at`.
- **Field mapping**: maintain a `field_N → property` map per form; Instapage's internal IDs don't match visible labels and can shift if you re-order form fields, so re-verify after editing a form.
- **Rate-limit handling**: respect `Retry-After` on 429, back off exponentially, and spread bulk/backfill jobs to stay under both the 200/min and the daily quota (resets 00:00 UTC).
- **Token hygiene**: a personal API token inherits the issuing user's permissions and can read every workspace that user can access — store it as a secret, rotate on staff change, and use `inheritOwnerContextInPublicApi` deliberately when inviting team members.
