# Waalaxy Platform Reference

## Overview

Waalaxy is a LinkedIn-first (LinkedIn + email) outreach automation tool that runs as a Chrome extension on top of your real LinkedIn session. It targets solopreneurs, founders, recruiters, and small sales teams who want ready-made prospecting sequences without a cloud-infra setup. Differentiator: low price, a Free tier, and 99+ prebuilt sequence templates — at the cost of higher account-safety risk than cloud-based tools (it executes in your browser).

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| **LinkedIn prospecting** | Build prospect lists from LinkedIn Search, Sales Navigator, or Recruiter Lite; target by intent signals (post reactions, group/event members) | UI-only to *source*; imported lists are **API-readable** (`getProspectLists`) |
| **Prospect lists** | Containers of prospects with name, count, icon | **API-accessible** (read: `getProspectLists`; write: import via `addProspectFromIntegration`) |
| **Campaigns (sequences)** | Multi-step LinkedIn (+ email on Business) flows: connection request, message, profile visit, follow-ups with human-like timing | Campaign list is **API-readable** (`campaigns/getAll`, paused/running only); building/launching a sequence is **UI-only**; prospects **API-enrollable** via `campaignId` on import |
| **Email Finder** | Finds + verifies professional emails (61%+ match rate); credit-metered | UI + part of enrichment; credits gated by plan |
| **Lead enrichment** | Enriches imported prospects with profile/company data | UI-only (runs as part of import/campaign) |
| **Cold email sequences** | Automated email follow-ups alongside LinkedIn (multichannel) | **Business plan only**; UI-built |
| **LinkedIn Inbox (Inbox Waalaxy)** | Unified inbox: saved replies, scheduling, tags | Paid add-on (~€20/user/mo); UI-only |
| **CRM sync** | Push prospects/activity to HubSpot, Pipedrive | Native connectors + **API** + Make/Zapier/n8n |

**No "send message" endpoint.** The API imports/enrolls prospects; the campaign sequence (built in the UI) does the actual LinkedIn/email sending through the connected account.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify in-account; Waalaxy raised prices and changed credit allotments in 2026.*

| Plan | Price (monthly) | LinkedIn invites/mo | Email Finder credits/mo | API | Cold email |
|---|---|---|---|---|---|
| **Free** | €0 | 80 | 30 | No | No |
| **Pro** | €19/user | 300 | 25 | No | No |
| **Advanced** | €49/user | 800 | 500 | **Yes** | No |
| **Business** | €69/user | 800 | 500 | **Yes** | **Yes** (multichannel) |

- **API access is gated to Advanced + Business.** The `Generate API key` button doesn't exist on Free/Pro.
- **Cold email / multichannel sequences require Business.** Pro/Advanced get the Email Finder but not automated email sending.
- **LinkedIn Inbox (Inbox Waalaxy)** is a separate paid add-on (~€20/user/mo), 500 free conversations included.
- **Annual billing** gives ~50% off but must be paid in full upfront.
- **Rate limits**: not published in the developer docs. Apply your own throttling/backoff; the practical ceiling is the per-plan monthly invite cap + Waalaxy's daily ramp (it deliberately ramps new accounts slowly).
- **Account-safety limits**: because it's a Chrome extension acting on the real LinkedIn session, exceeding the daily/weekly action volume is the #1 cause of restricted accounts.

## Integrations

- **Direction**: bidirectional with CRMs — push prospects to **HubSpot / Pipedrive**; pull lists/campaigns out via the API.
- **iPaaS**: native **Make**, **Zapier**, **n8n** apps (these are the documented `origin.name` values for imports). 2,000+ tools reachable via those plus CSV import/export with history.
- **API**: REST, `Bearer` token. Read prospect lists + campaigns; write prospect imports (optionally enrolling into a campaign).
- **noCRM, Pabbly, ApiX-Drive** and other connector marketplaces also list Waalaxy triggers/actions.

## Data model

**Prospect list** (`GET /prospectLists/getProspectLists` returns an array):
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

**Campaign** (`GET /campaigns/getAll` — only paused/running campaigns):
```json
{
  "total": 4,
  "campaigns": [
    { "_id": "6967ccd7cd1b75dbab178b35", "name": "Email Finder" },
    { "_id": "6967ccd7cd1b75dbab178b36", "name": "Email Finder 2" }
  ]
}
```

**Prospect import** (`POST /prospects/addProspectFromIntegration` body): a `prospects[]` array where each item is keyed on the LinkedIn `url`, plus `prospectListId` (destination), optional `campaignId` (enroll), and a required `origin`:
```json
{
  "prospects": [
    {
      "url": "https://www.linkedin.com/in/john-doe-123456",
      "customProfile": { "firstName": "John", "lastName": "Doe", "email": "john@example.com" },
      "customVariables": [ { "label": "Company size", "value": "500" } ]
    }
  ],
  "prospectListId": "695b86fe3b6b619338a0e14a",
  "campaignId": "6967ccd7cd1b75dbab178b35",
  "origin": { "name": "make" },
  "canCreateDuplicates": false,
  "moveDuplicatesToOtherList": false,
  "shouldOverwriteCustomProfileData": false,
  "addExistingProspectInCampaign": false
}
```

**Import response** — per-prospect `importCode` (`success`, `duplicated_prospect`, …) and `addToCampaignCode`, with the resolved `prospect.profile` (incl. `publicIdentifier`, `memberId`, `salesMemberId`). See `references/waalaxy-api-reference.md` for the full shape.

## Quick-start recipes

### Recipe 1 — Import a LinkedIn lead and enroll it in a campaign
Trigger: a new lead in your app. Steps: (1) resolve a `prospectListId` and `campaignId`, (2) POST the prospect.

```bash
# 1. Get a prospect list id
curl -s https://developers.waalaxy.com/prospectLists/getProspectLists \
  -H "Authorization: Bearer $WAALAXY_KEY"

# 2. Get a (paused/running) campaign id
curl -s https://developers.waalaxy.com/campaigns/getAll \
  -H "Authorization: Bearer $WAALAXY_KEY"

# 3. Import + enroll
curl -s -X POST https://developers.waalaxy.com/prospects/addProspectFromIntegration \
  -H "Authorization: Bearer $WAALAXY_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prospects": [{ "url": "https://www.linkedin.com/in/john-doe-123456",
      "customProfile": {"firstName":"John","lastName":"Doe"} }],
    "prospectListId": "695b86fe3b6b619338a0e14a",
    "campaignId": "6967ccd7cd1b75dbab178b35",
    "origin": { "name": "my-app" }
  }'
```

```python
import os, requests
BASE = "https://developers.waalaxy.com"
H = {"Authorization": f"Bearer {os.environ['WAALAXY_KEY']}", "Content-Type": "application/json"}

list_id = requests.get(f"{BASE}/prospectLists/getProspectLists", headers=H).json()[0]["_id"]
camp_id = requests.get(f"{BASE}/campaigns/getAll", headers=H).json()["campaigns"][0]["_id"]

body = {
    "prospects": [{"url": "https://www.linkedin.com/in/john-doe-123456",
                   "customProfile": {"firstName": "John", "lastName": "Doe"}}],
    "prospectListId": list_id,
    "campaignId": camp_id,            # omit to import without enrolling
    "origin": {"name": "my-app"},     # required; appears as "API-my-app" in the UI
}
r = requests.post(f"{BASE}/prospects/addProspectFromIntegration", headers=H, json=body)
for item in r.json()["result"]:
    print(item["importCode"], item.get("addToCampaignCode"))
```
Gotchas: `origin` is required; every prospect needs a LinkedIn `url`; `campaigns/getAll` only lists paused/running campaigns; the API only works on Advanced/Business.

### Recipe 2 — Validate the key before building
Run `GET /integrations/test` (returns `true`) as a health check / connectivity probe inside CI or your integration's setup step.
```bash
curl -s https://developers.waalaxy.com/integrations/test -H "Authorization: Bearer $WAALAXY_KEY"
# -> true
```

### Recipe 3 — No-code: sync inbound leads via Make/Zapier/n8n
Trigger on a new CRM/form lead in Make (or Zapier/n8n) → Waalaxy "Add prospect" action with the LinkedIn URL mapped in. Set `origin.name` to `make`/`zapier`/`n8n` so the source is traceable. Use this when you don't want to host code; it wraps the same `addProspectFromIntegration` endpoint.

## Integration patterns

- **CRM sync architecture**: treat Waalaxy as a downstream actuator. Your CRM/app is the source of truth; on a "start outreach" event, import the prospect (with LinkedIn URL) and enroll into the right campaign. Pull replies/status back via the native HubSpot/Pipedrive connector or by polling, since there's no documented reply webhook in the public API.
- **Idempotency/dedup**: rely on `importCode: "duplicated_prospect"` rather than pre-checking; set `canCreateDuplicates: false` (default) and use `moveDuplicatesToOtherList` / `addExistingProspectInCampaign` to control behavior for prospects already in the CRM.
- **Error handling**: errors follow RFC 7807 Problem Details (`type`, `title`, `status`, `detail`, `instance`). Handle 401 (bad/missing key or unsupported plan) and back off on 429.
- **Safety throttling**: the binding constraint isn't an API rate limit, it's LinkedIn — keep daily action volume under Waalaxy's ramp and the plan's monthly cap; spread sourcing across time rather than dumping thousands of prospects into one campaign.
