# Userback Platform Reference

## Overview

Userback is an in-context **visual feedback + bug-reporting** platform: users (or internal
QA/clients) click a widget, annotate a screenshot or record a video, and Userback attaches
the technical context developers need to reproduce — console logs, network requests,
browser/OS/screen metadata, and (on paid plans) a session replay. On top of bug capture it
adds **feature-request boards, a public roadmap, surveys, and a Feature Portal**, making it a
single tool that spans "report a bug" and "request a feature." Best fit: SaaS product and
maker teams who want actionable bug reports + lightweight feature voting. It is more
SaaS/product-centric than agency client-review tools like Marker.io/BugHerd.

## Capabilities & automation surface

| Capability | What it does | Automation |
|---|---|---|
| Feedback widget | In-app button → annotated screenshot / video / general feedback / bug / idea, with auto-captured console + network logs and device metadata | **API-accessible** (create/read), **webhook-accessible** (events), widget via **JS SDK** |
| Feature-request boards | Public/private boards with voting + comments | **API-accessible** (Feedback resource, `feedbackType: Idea`) |
| Roadmap / Feature Portal | Public roadmap + portal (vote, comment, status) | Add-on; **UI-managed**, statuses readable via Workflows API |
| Session Replay | Replays the user's session around the feedback | **API-accessible** (`/sessionRecording` list/get); **Business+** to capture |
| Surveys / micro-surveys | NPS/CSAT-style and product micro-surveys | Triggered via **JS SDK** (`openSurvey`); **Business+** |
| Workflows (statuses) | Board status columns | **API-accessible** (`/workflow` CRUD) |
| Comments | Internal + public comments on feedback | **API-accessible** (`/feedback/comment` CRUD), **webhook events** |
| Userback Insights | AI summarization/clustering of feedback | **UI-only** (AI) |
| User identification | Attribute feedback to a logged-in user + custom data | **JS SDK** (`identify`, `setData`) |
| MCP server | AI agents read/triage feedback with console/network context | **MCP** (`mcp.userback.io/v1/mcp/`, OAuth, ~12 tools) |
| Integrations | Jira, Linear, GitHub, Slack, Trello, Asana, CRM, etc. | Native + **Zapier** (Team+) |

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify current pricing in-account.*

| Plan | Price (annual/monthly per seat) | Projects | Notable inclusions |
|---|---|---|---|
| **Free Forever** | $0 | 2 (max 2 seats) | Core feedback capture; **feedback retained only 7 days** |
| **Team** | $7 / $9 | Unlimited (2 base) | Unlimited retention, **Zapier**, project-management integrations |
| **Business** (most popular) | $15 / $19 | 25 | **Session replay**, surveys, behavioral targeting, custom branding |
| **Business Plus** | $23 / $29 | Unlimited | **REST API**, **webhooks**, **mobile SDK**, advanced privacy, support integrations |
| Roadmap / Feature Portal | add-on $31–$39/mo | — | Public roadmap + portal |

**The integration cliff:** the **REST API and webhooks are Business Plus only.** Zapier
appears on Team. If you plan to build a CRM/warehouse sync, budget for Business Plus from the
start — a Team/Business prototype that relies on the API will not work. Session replay and
the JS SDK methods require Business; mobile SDK requires Business Plus.

**Other limits:** API list pages cap at **50 records/page**. Exact rate limits are not
published — handle `429` with backoff. Free-plan feedback is purged after 7 days.

## Integrations (data-flow view)

- **Issue trackers (write):** Jira, Linear, GitHub, Asana, Trello, ClickUp, Azure DevOps —
  push feedback as issues with the screenshot + technical context attached. Most are
  one-way (Userback → tracker) by default; check two-way sync per connector.
- **Slack (read/notify):** capture feedback from Slack and post new-feedback notifications.
- **CRM / data (bidirectional via API):** no first-class CRM connector for every CRM — use
  the REST API + webhooks (Business Plus) or Zapier (Team+) to sync into HubSpot/Salesforce
  or a warehouse.
- **Zapier (Team+):** triggers on new feedback; actions to create feedback/route elsewhere.
- **MCP (read/write):** AI agents create/update/comment/search feedback and read console +
  network logs.

## Data model

Key objects (camelCase properties; see `userback-api-reference.md` for full schemas):

**Feedback** — the central object.
```json
{
  "id": 4455,
  "projectId": 123,
  "feedbackType": "Bug",            // General | Bug | Idea
  "email": "user@example.com",
  "name": "John Doe",
  "title": "Button malfunction",
  "description": "The submit button doesn't respond",
  "priority": "high",               // low | neutral | high | urgent
  "rating": "star_4",               // star_1 .. star_5
  "assigneeId": 1234,
  "dueDate": "2024-02-01",
  "created": "2024-01-15T09:00:00Z",
  "modified": "2024-01-15T10:30:00Z"
}
```

**Project** → `{ id, name, url, logo, isArchived, created, createdBy }`
**Workflow** (status column) → `{ id, name, sort, color, Project{...} }`
**Comment** → `{ id, userId, comment, isPublic, isResolved, reaction[], created, Feedback{...} }`
**SessionRecording** → `{ id, shareUrl, duration, userAgent, location, userIdentification, tag, domain, created }`

Relationships: a Project has many Feedback; Feedback belongs to a Workflow status, has many
Comments and Screenshots, and may link to a SessionRecording.

## Quick-start recipes

### 1. Install the widget and attribute feedback to the logged-in user

```html
<script>
  (function(d){var s=d.createElement('script');s.async=true;
   s.src='https://static.userback.io/widget/v1.js';
   s.onload=function(){
     Userback.init('<ACCESS_TOKEN>');           // from Project Settings
     Userback.identify(String(currentUser.id), {  // attribute feedback
       name: currentUser.name,
       email: currentUser.email,
       plan: currentUser.plan
     });
     Userback.setData({ orgId: currentUser.orgId, mrr: currentUser.mrr });
   };
   d.head.appendChild(s);})(document);
</script>
```
*Gotcha:* `identify`/`setData` and session replay are **Business+**. Call `identify` before
the user submits or feedback lands anonymous.

### 2. Pull all feedback into a warehouse / CRM (paginated, Business Plus)

```python
import requests, time

BASE = "https://rest.userback.io/1.0"
H = {"authorization": "Bearer <TOKEN>"}

def list_all(resource, **params):
    page, out = 1, []
    while True:
        params.update(page=page, limit=50)
        r = requests.get(f"{BASE}/{resource}", headers=H, params=params)
        if r.status_code == 429:           # rate limited — back off
            time.sleep(2 ** page); continue
        r.raise_for_status()
        body = r.json()
        out += body["data"]
        if page >= body["_pagination"]["totalPages"]:
            break
        page += 1
    return out

bugs = list_all("feedback", filter="feedbackType eq 'Bug'", sort="created,desc")
print(len(bugs), "bugs")
```
*Gotcha:* `limit` maxes at 50. Use the OData `filter` to slice by type/status server-side.

### 3. Listen for new feedback and create a CRM task (webhook, Business Plus)

```python
from flask import Flask, request, abort
app = Flask(__name__)

@app.post("/userback-webhook")
def hook():
    # No HMAC signature is documented — verify User-Agent and keep the URL secret.
    if request.headers.get("User-Agent") != "Userback-Webhook":
        abort(401)
    e = request.get_json()
    if e["action"] == "create" and e["type"] == "feedback":
        fb_id = e["data"]["id"]
        # Best practice: re-fetch from the API rather than trust the payload body.
        # requests.get(f"{BASE}/feedback/{fb_id}", headers=H) -> create CRM task
    return "", 200
```
*Gotcha:* payloads are thin and unsigned — re-read the entity via `GET /feedback/{id}` for
trustworthy data.

### 4. Let a Claude/Cursor agent triage feedback (MCP)

```bash
claude mcp add Userback https://mcp.userback.io/v1/mcp/ -t http -s user
# then: "Use Userback MCP to find this week's open bugs, cluster duplicates,
#        and draft a status update for each." (OAuth on first call)
```

## Integration patterns

- **CRM/warehouse sync:** poll `GET /feedback?sort=modified,desc` on a schedule **or** use
  webhooks for near-real-time, then upsert by Userback `id`. Store `modified` as your
  high-water mark for incremental polling. Map `feedbackType`/`priority`/Workflow status to
  your CRM's fields. **Requires Business Plus.**
- **Webhook listener:** no signature is documented — restrict by source IP/secret URL,
  verify `User-Agent: Userback-Webhook`, dedupe on `data.id` + `action` (delivery/ordering
  not guaranteed), and re-fetch via REST for the authoritative record.
- **Issue-tracker bridge:** prefer the native Jira/Linear/GitHub connector for the
  screenshot + console/network attachment fidelity; fall back to the API only when you need
  custom routing the connector can't express.
- **Batch export:** paginate at `limit=50`, back off on `429`, and use `filter` to avoid
  pulling resolved/archived items you don't need.
