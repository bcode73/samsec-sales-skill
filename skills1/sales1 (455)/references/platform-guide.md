# Rapidr Platform Reference

## Overview

Rapidr (rapidr.io) is a product-feedback & feature-request management suite for SaaS teams: collect ideas on public/private boards, prioritize by votes, communicate a public roadmap, and announce shipped work via a changelog. It positions as a polished, more-affordable **Canny / Productboard / Frill alternative** for product teams that want the full feedback loop in one portal. Its defining constraint for builders: **there is no public REST/pull API** — automation is push/identify only (JWT SSO, Zapier, native connectors, embeddable widget).

## Capabilities & automation surface

For each module: what it does, then how (if at all) you can automate it.

### Feedback boards
- Unlimited public **and private** boards; ideas/feature requests with **voting**, **proxy voting** (log + vote on behalf of a customer), custom **statuses**, **tags**, public + private (internal) **comments**, **@mentions**, **admin badge**, markdown.
- **Duplicate merging** + "similar feedback" detection at submission time.
- **User/feedback segmentation** by group, account type, geography (Business+).
- **Customer profiles** (activity history, traits, account attributes).
- **Voter list CSV export** for outreach.
- **Smart sorting** surfaces popular + recently-active feedback.
- *Automation:* **UI-only** for direct reads. New feedback/comment/vote events are **Zapier-** and **Slack-accessible** (push). Voters are exportable via **CSV** (manual). **No API read.**

### Public roadmap
- Customizable columns (rename to match your workflow) with workflow-specific statuses; an idea's status drives its roadmap column.
- *Coming soon:* roadmap prioritization scoring (custom fields/segments), embeddable roadmap widget.
- *Automation:* **UI-only**; status changes can fan out to Slack/Zapier (push).

### Changelog / release notes
- Standalone changelog page + **embeddable changelog widget**; markdown rich-text editor, customizable categories, **drafts**, sort/filter.
- *Coming soon:* changelog reactions (emoji), changelog email digest.
- *Automation:* **UI-authored**; publish events may be **Zapier-accessible** (confirm in the live Zap editor).

### Embeddable widget & portal
- In-app **feedback widget** (embed boards) + **changelog widget**; full portal hostable on a **custom domain** (e.g. `roadmap.example.com`) with custom branding (colors, header, logo).
- *Automation:* embed snippet is **front-end**; user identity flows through **JWT SSO**.

### Authentication / identity
- Built-in auth (email) + **SSO via JWT and SAML** (Okta, OneLogin, Azure AD). Identifying users attaches votes/posts to real accounts instead of anonymous.
- *Automation:* **JWT SSO** is the primary developer integration (server-side token mint). **Business+.**

## Pricing, limits & plan gates

> Best-effort from rapidr.io/pricing (2026-06) — **confirm in-account**. No free tier; 14-day trial, no card.

| Plan | Price | Includes | Integration-relevant gates |
|---|---|---|---|
| **Startup** *(most popular)* | **$49/mo** | 5 team members, basic integrations (Slack, Intercom, Jira, HubSpot, Zapier), roadmap & changelog, widgets & portal, custom statuses, **private boards**, **custom domain** | Zapier + basic native connectors included; **no SSO**, **no segmentation** |
| **Business** | **$199/mo** | Everything in Startup + 50 members, **user segmentation**, **advanced integrations**, **SAML & JWT SSO**, priority support, concierge migration, remove "Powered by Rapidr" | **SSO, segmentation, advanced integrations unlock here** |
| **Enterprise** | Custom | Everything in Business + unlimited members, full white-label, 99.9% uptime SLA, custom contract, invoice/PO | — |

**Key gate:** there is **no middle tier** — SSO and segmentation jump straight from $49 → $199. Frame plan choice around whether SSO/segmentation is needed.

**Rate limits / overage:** N/A — no public API to rate-limit. Zapier task limits are governed by your Zapier plan, not Rapidr.

## Integrations

Direction of data flow matters more than logos. Rapidr is mostly an **intake + notify** hub; it does not expose a queryable read surface.

| Integration | Direction | What it does | Notes |
|---|---|---|---|
| **Slack** | bidirectional | `/rapidr` slash command captures feedback from Slack; Rapidr pushes new-feedback/comment/vote notifications to channels | Filterable per channel by board + event type; multiple channels supported |
| **Intercom** | inbound | Track feedback & votes from Inbox and Messenger | Native |
| **Jira** | bidirectional | Sync feedback & status with Jira issues | Native; also an Atlassian Marketplace app |
| **HubSpot** | inbound | Track feedback on behalf of contacts & deals | Native |
| **Zapier** | outbound (push) + actions | Realtime **triggers** for events on Rapidr + create/update-record **actions** into 5,000+ apps | The no-code stand-in for the missing pull API; exact trigger names unconfirmed |
| **SSO** (Okta, OneLogin, Azure AD, SAML, JWT) | inbound auth | Identify users into the portal | Business+ |
| *Coming soon* | — | Zendesk (tickets), Salesforce, GitHub (sync feedback & status), Segment | Not yet live at research time |

## Data model

Rapidr does not publish a schema or API, so these are **constructed** from documented terminology to help you reason about Zapier field-mapping and CSV exports. Verify exact field names against a live Zapier payload or CSV export.

```jsonc
// <!-- Constructed from documented terminology — verify against a live Zapier payload / CSV export -->
// An "idea" / feedback post on a board
{
  "id": "idea_…",                 // identifier (shape unconfirmed)
  "title": "Add dark mode",
  "description": "Please add a dark theme",
  "board": "Feature Requests",     // board name
  "status": "Planned",             // custom status → drives roadmap column
  "votes": 42,
  "tags": ["ui", "accessibility"],
  "author": { "name": "Jane Doe", "email": "jane@example.com" },
  "segment": { "account_type": "Pro", "geo": "US" },  // Business+ segmentation
  "created_at": "2026-06-29T10:00:00Z"
}
```

```jsonc
// <!-- Constructed — verify against the live CSV export -->
// Voter export row (CSV)
{ "idea": "Add dark mode", "voter_name": "Jane Doe", "voter_email": "jane@example.com", "voted_at": "2026-06-29" }
```

```jsonc
// <!-- Constructed — verify in the live changelog editor -->
// Changelog entry
{ "title": "v2.3 — Dark mode", "category": "New", "status": "published", "body_markdown": "We shipped dark mode…", "published_at": "2026-06-29" }
```

## Quick-start recipes

### Recipe 1 — Push every new feature request into your tool (no API → Zapier)
**Trigger:** new feedback submitted on a Rapidr board. **Goal:** land it in your internal tool/CRM/Slack without an API.

Steps:
1. In Zapier, create a Zap with **Rapidr** as the trigger app; pick the realtime "new feedback / new post" trigger (**confirm the exact trigger name in the live Zap editor** — Rapidr advertises realtime triggers but doesn't publish names).
2. Connect your Rapidr account (OAuth in Zapier).
3. Add an action step into your destination (e.g. Linear/Jira/Sheets/Slack/your webhook).
4. Map fields (title, description, board, author email, votes — verify field availability in the Zap preview).

```jsonc
// If your destination is your own endpoint, use Zapier's "Webhooks by Zapier → POST" action.
// You receive Rapidr's data as the Zap's mapped payload — NOT a Rapidr API call.
// Dedupe on the idea id (or title+board) since you can't re-GET from Rapidr to reconcile.
{ "title": "{{idea_title}}", "board": "{{board}}", "email": "{{author_email}}", "votes": "{{votes}}" }
```

Gotcha: there is **no polled API fallback** — if the Zap is off, you miss events. Rely on the **voter CSV export** for periodic reconciliation.

### Recipe 2 — Identify logged-in users with JWT SSO (so votes aren't anonymous)
**Trigger:** a logged-in user clicks "Feedback." **Goal:** carry their identity into Rapidr. **Plan:** Business+.

Steps:
1. In **Company Settings → SSO**, generate the **Secret Key** (keep it server-side) and set your **login redirect URL**.
2. On your redirect page, after the user is authenticated, mint a JWT from their identity and redirect to Rapidr's SSO endpoint with the token, preserving the `redirect` query param so they return to where they started.
3. Validate the token with Rapidr's **JWT debugger**, then enable SSO (this disables other login methods).

```python
# <!-- Flow confirmed from Rapidr SSO help docs; exact claim names + algorithm are JS-rendered — verify in-account -->
import jwt  # PyJWT
from urllib.parse import quote

SECRET_KEY = "…"  # from Company Settings → SSO; server-side only

def rapidr_sso_redirect(user, return_to):
    token = jwt.encode(
        {"name": user["name"], "email": user["email"]},  # confirm exact claim keys in the in-account docs
        SECRET_KEY,
        algorithm="HS256",  # confirm algorithm in-account
    )
    # SSO endpoint + redirect param — confirm the exact path in your account's SSO settings
    return f"https://feedback.example.com/sso?token={token}&redirect={quote(return_to)}"
```

```bash
# There is NO REST API to curl. The closest "API call" is the SSO redirect above (a browser redirect, not a fetch).
# Do not attempt: curl https://api.rapidr.io/...  — no such public API exists.
```

Gotcha: SSO is **Business-plan only**. On Startup, users self-identify by email or stay anonymous.

### Recipe 3 — Embed the feedback + changelog widget on a custom domain
**Goal:** in-app feedback widget + a branded portal at `roadmap.yourdomain.com`.

Steps:
1. In Rapidr, set up your **custom domain** (Startup+) and branding (colors/logo/header).
2. Add the **widget embed snippet** from your Rapidr settings to your app (front-end). Pair it with the **JWT SSO** flow (Recipe 2) so widget activity is attributed to real users (Business+).
3. Add the **changelog widget** to surface release notes in-app.

Gotcha: confirm the exact embed snippet + any data attributes in your account — the public help article describes the concept but doesn't expose the script verbatim.

## Integration patterns

- **No-API sync architecture.** Treat Rapidr as a **source that pushes**, never one you poll. Build a webhook receiver fed by **Zapier** (Webhooks by Zapier → POST) for realtime events, and run a **periodic CSV export** reconciliation for voters/ideas to catch anything Zapier missed. Idempotency: dedupe on the idea id (or `title+board`) since you can't re-read from Rapidr to reconcile.
- **Identity pattern (JWT SSO).** Stand up a server-side login-redirect endpoint that mints the JWT from your auth session and 302s to Rapidr's SSO endpoint with `?token=…&redirect=…`. Keep the secret key in server config; never expose it client-side. Test with the JWT debugger before enabling (enabling disables other auth).
- **Native-connector-first.** If you already run **Jira** (bidirectional status sync) or **HubSpot/Intercom** (inbound feedback capture), prefer the native connector over Zapier — it carries status both ways (Jira) and avoids Zapier task costs. Reserve Zapier for destinations without a native connector.
- **Plan-aware design.** Before building SSO or segmentation-dependent flows, confirm the customer is on **Business ($199/mo)** — both are gated there. A Startup-plan ($49) build can only use email identification + basic Slack/Zapier/Jira/HubSpot/Intercom.
