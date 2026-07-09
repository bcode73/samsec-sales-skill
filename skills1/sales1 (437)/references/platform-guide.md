# Productlane Platform Reference

## Overview

Productlane (productlane.com) is an AI-native customer support **and** product-feedback suite **built exclusively on Linear**. It unifies an omnichannel support inbox (email, live chat, Slack Connect, MS Teams, Discord), an AI Agent, a self-updating help center, a customer feedback portal, a public roadmap, and a changelog — all wired to Linear as the single source of truth for issues, projects, and releases. It targets fast-moving B2B SaaS teams that run engineering in Linear (customers include Clerk, Whop, Stytch, Ghost, Bitcoin.com). Its differentiator vs Canny/Frill/Productboard is the deep Linear coupling (feedback → Linear issue, roadmap = Linear projects, changelog auto-drafted from completed Linear issues) plus a bundled support inbox; its closest peer is **Cycle** (also Linear-native). Unlike Rapidr/Quickhunt it ships a **documented REST API**, but unlike UserJot/Sleekplan it has **no MCP server**.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **Omnichannel inbox** | Email, live chat, Slack Connect, MS Teams, Discord in one inbox; turn any conversation into a Linear issue without duplicating | UI-first; conversations → Linear issues; **Pro+** for the full support inbox |
| **AI Agent / Copilot** | Drafts replies, summarizes threads, creates Linear issues with labels + priority, routes minor bugs to coding agents | UI-first; configured in-account; newer feature |
| **Help center** | Self-updating knowledge base auto-generating articles from resolved Linear issues + past conversations; embeddable AI assist | UI-first; **Pro+** |
| **Feedback portal** | Customers submit + upvote requests; status synced from Linear; combines support requests with Linear tickets | **API-accessible** (Portal: `getprojects`, `getprojectupvotes`, `upvoteproject`, `createfeedback`); widget embed; **Starter+** |
| **Public roadmap** | Roadmap mirroring Linear **projects**; customers see real-time status from Linear | **API-readable** (`getprojects`/`getprojectupvotes`); **Starter+** |
| **Changelog (Release Intelligence)** | Auto-drafts changelog entries from completed Linear issues/projects (categorizes by label, writes a draft); distributes via Slack/email/in-app | **API-readable** (`listchangelogs`); **AI Changelog generation = Pro+** |
| **Insights / Notes** | Structured internal feedback notes (text + painLevel) tied to a customer/project | **API-accessible** (`GET/POST/PATCH /insights`); also the **Zapier "Create Note"** action |
| **Companies / Customers** | CRM-style company + customer records with **segments** | **API-accessible** (full CRUD on Customers; list/get/create/delete Companies) |
| **REST API** | `productlane.com/api/v1`, Bearer auth — Companies, Customers, Insights, Portal, Workspaces | **Documented & available** (no per-plan API gate found, but verify) |
| **Webhooks (own)** | Productlane's own outbound webhooks are **not clearly documented publicly** (Linear's webhooks are separate) | **Unconfirmed** — verify in-account; fall back to Zapier/polling |
| **MCP server** | — | **None** — no Productlane MCP server exists |

**Rule of thumb:** Linear is the hub — feedback, roadmap, and changelog all derive from it. Automate *into* Productlane with the REST API (`/insights`, `/customers`) or public `/feedback`; read roadmap/changelog *out* via the Portal endpoints; there is no MCP server, and Productlane's own webhook surface is unconfirmed.

## Pricing, limits & plan gates

*Best-effort, captured 2026-06 from productlane.com + third-party listings — per-user, confirm in-account.*

| Plan | Price (annual / monthly, per user) | Key inclusions | Notable gates |
|---|---|---|---|
| **Starter** | ~$15 / ~$19 | Public roadmap, changelog, feedback hub/portal, feedback widget | No support inbox; no AI changelog gen; no SSO/custom domain |
| **Pro** | ~$29 / ~$39 | Adds in-app support, **email inbox**, **Slack Connect**, **AI Changelog generation** | No SSO; no white-label; no advanced integrations |
| **Scale** | ~$79 / ~$99 | Custom snippets, **custom domains**, **white-labeling**, **SSO (JWT)**, **private portals**, advanced integrations (**HubSpot, Zapier**), support portal, priority support | — |

- **No permanent free plan** — **7-day free trial** only.
- **Per-user pricing** — multiply by seat count; a reviewer flagged the entry price as steep for small teams.
- **Startup discounts** are offered to early-stage companies — worth asking.
- **Two gates to remember:** the **support inbox + AI changelog** appear at **Pro**, and **SSO / custom domain / white-label / HubSpot+Zapier** appear at **Scale**.

## Integrations

Data flow by connector:

- **Linear** — *mandatory, bidirectional, core*. Feedback → Linear issues; roadmap = Linear projects; changelog drafted from completed Linear issues; status synced back to the portal. Productlane does not function without it.
- **Slack** — Slack Connect channels feed the inbox; changelog/notifications push to Slack.
- **MS Teams / Discord** — conversation channels into the inbox.
- **Shared email + live chat** — support channels (Pro+).
- **HubSpot** — advanced integration, **Scale-tier**.
- **Zapier** — **Scale-tier**; documented **action: "Create Note"** (Note Text, Importance, Customer Email, Project ID, optional notify) — maps to the Insights API. Trigger inventory not confirmed — verify in the live Zap editor.
- **REST API** — `productlane.com/api/v1` for Companies/Customers/Insights/Portal/Workspaces (see api-reference).

No native Salesforce/Jira connector was found — route those via Zapier (Scale) or the API, and remember Linear (not Jira) is the issue tracker Productlane expects.

## Data model

> <!-- Constructed from the ReadMe-hosted API reference field lists (productlane.readme.io) — verify exact response shapes against the live API. -->

```jsonc
// Customer (POST /api/v1/customers — auth)
{
  "id": "cust_123",
  "name": "Jane Doe",                       // 1–255 chars
  "email": "jane@acme.com",                 // required
  "segments": ["enterprise", "design-partner"]  // optional array of strings
}
```

```jsonc
// Company (POST /api/v1/companies — auth)
{
  "id": "comp_abc",
  "name": "Acme Inc"
}
```

```jsonc
// Insight / Note (POST /api/v1/insights — auth) — structured internal feedback
{
  "id": "ins_456",
  "text": "Customer wants a Kanban view for requests",  // min length 1
  "painLevel": "HIGH",                       // UNKNOWN | LOW | MEDIUM | HIGH
  "customerEmail": "jane@acme.com",          // required
  "customerName": "Jane Doe",                // optional
  "projectId": "linear_project_id",          // optional — links to a Linear project
  "notify": { }                              // optional notification settings
}
```

```jsonc
// Public feedback (POST /api/v1/feedback — NO AUTH) — widget/portal capture
{
  "workspaceId": "ws_789",                   // required
  "text": "Dark mode please",                // required, min 1
  "painLevel": "MEDIUM",                     // UNKNOWN | LOW | MEDIUM | HIGH
  "email": "user@example.com",               // required
  "projectId": "linear_project_id",          // optional
  "notify": { }                              // optional
}
```

```jsonc
// Portal: a project = a Linear project surfaced on the roadmap (GET /api/v1/portal/...)
// changelogs are read via listchangelogs; upvotes via getprojectupvotes / upvoteproject
{
  "project": { "id": "linear_project_id", "name": "Kanban view", "status": "in_progress", "upvotes": 42 }
}
```

## Quick-start recipes

Base URL `https://productlane.com/api/v1`. Auth header `Authorization: Bearer API_KEY` (generate the key at `productlane.com/settings/api`). `POST /feedback` is the exception — it takes **no** auth.

### Recipe 1 — Push a structured insight (prioritized feedback note) from your backend (auth)

**Trigger:** A user submits feedback in your product; your server forwards it as a prioritized Insight tied to the customer.

```bash
curl -X POST https://productlane.com/api/v1/insights \
  -H "Authorization: Bearer $PRODUCTLANE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Wants a Kanban view for requests",
    "painLevel": "HIGH",
    "customerEmail": "jane@acme.com",
    "customerName": "Jane Doe"
  }'
```

```python
import os, requests

def push_insight(text, email, pain="MEDIUM", name=None, project_id=None):
    payload = {"text": text, "painLevel": pain, "customerEmail": email}
    if name:       payload["customerName"] = name
    if project_id: payload["projectId"] = project_id
    r = requests.post(
        "https://productlane.com/api/v1/insights",
        headers={"Authorization": f"Bearer {os.environ['PRODUCTLANE_API_KEY']}"},
        json=payload, timeout=15,
    )
    r.raise_for_status()
    return r.json()
```

**Gotchas:** Set `painLevel` deliberately (`UNKNOWN|LOW|MEDIUM|HIGH`) — it's how Productlane prioritizes feedback to engineering. Keep the API key server-side; never ship it to the browser.

### Recipe 2 — Capture public feedback from an in-browser widget (no auth)

**Trigger:** An anonymous/end-user submits feedback from your site or portal — you don't want to expose the API key.

```bash
curl -X POST https://productlane.com/api/v1/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "workspaceId": "YOUR_WORKSPACE_ID",
    "text": "Dark mode please",
    "painLevel": "MEDIUM",
    "email": "user@example.com"
  }'
```

**Gotchas:** This endpoint takes **no auth**, so a leaked `workspaceId` invites spam. Front it with a CAPTCHA, a rate limit, and an origin/referer check. Get `workspaceId` from `GET /api/v1/workspaces` (auth) or in-account settings.

### Recipe 3 — Read the public roadmap / changelog for an embed (auth)

**Trigger:** You want to mirror Productlane's roadmap or "what's new" in your own UI.

```python
import os, requests
H = {"Authorization": f"Bearer {os.environ['PRODUCTLANE_API_KEY']}"}
base = "https://productlane.com/api/v1"

projects  = requests.get(f"{base}/portal/projects", headers=H, timeout=15).json()   # roadmap items (Linear projects)
changelog = requests.get(f"{base}/portal/changelogs", headers=H, timeout=15).json() # release notes
# upvotes per project: GET /portal/projects/{id}/upvotes  (confirm exact path in api-reference)
```

**Gotchas:** Roadmap projects are **Linear projects** — their status reflects Linear, so don't try to mutate roadmap status here; change it in Linear. Confirm exact Portal paths/params against the api-reference and your account, and treat changelog auto-drafting (AI) as a **Pro+** feature.

## Integration patterns

- **Linear-first mental model.** Treat Linear as the database. Productlane writes feedback *to* Linear (as issues) and reads roadmap/changelog *from* Linear. When designing a sync, decide whether your system of record is Linear (then drive everything from Linear's API/webhooks) or your own app (then push Insights into Productlane and let it create Linear issues).
- **API intake, two trust boundaries.** Server-side, prioritized feedback → `POST /insights` (auth, carries `customerEmail`/`painLevel`). Untrusted in-browser capture → `POST /feedback` (no auth, needs abuse controls). Don't blur them.
- **Customer/company enrichment.** Create/upsert Customers (with `segments`) and Companies via the API so feedback is attributed and segmentable — Insights reference `customerEmail`, so seed the customer first for clean joins.
- **Event push is uncertain — design for it.** Productlane's own outbound webhooks aren't publicly documented. If you need real-time push, (a) confirm what Productlane emits in-account, (b) use Linear's webhooks for issue/status changes since Linear is the source of truth, or (c) poll the Portal endpoints. Don't assume HMAC-signed Productlane webhooks exist.
- **Plan-gate guardrails.** Confirm the plan before promising features: support inbox + AI changelog = **Pro**; SSO/custom domain/white-label/HubSpot/Zapier = **Scale**; everything is **per-user** with no free tier.
