# Landingi Platform Reference

## Overview

Landingi (landingi.com, founded 2011, Wrocław, Poland) is an AI landing page builder positioned as a "landing page operation system" — build, A/B test, and scale conversion pages without code. It targets marketers, solopreneurs, creators, and agencies, sitting between cheap single-page tools (Carrd) and high-end PPC platforms (Unbounce, Instapage). Its differentiators are the Lunar AI page generator, Smart Sections, Dynamic Text Replacement (DTR), programmatic (bulk) landing pages, and the Orbit MCP server.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| Visual Builder | Drag-and-drop page editor, 400+ templates | UI-only (pages readable/creatable via API — verify in-account) |
| Lunar (AI page generator) | Brief → launch-ready page | UI; reachable via the Orbit MCP server |
| AI Landing Page | AI copy, SEO, and visual enhancement | UI (consumes credits) |
| Form Builder | Lead-capture forms on pages and pop-ups | API-readable (`/forms/{formId}/submissions`); webhook-capable per form |
| Leads | Captured submissions, export | API (`/leads`, `/forms/{formId}/submissions`) + per-form webhook |
| A/B Testing | Variant comparison (Optimize+) | UI-only |
| EventTracker | Click/engagement tracking (Optimize+) | UI-only |
| Smart Sections | Reusable sections synced across pages (Optimize+) | UI-only |
| Dynamic Text Replacement (DTR) | Swap page text from ad URL params for message match | UI config; driven by query string |
| Multi-language | Auto-translate pages into ~35 languages (Optimize+) | UI-only |
| Programmatic Landing Pages | Bulk-generate pages from a data source/template (Scale+) | UI-driven bulk; pages then API-readable |
| Pop-ups / Lightboxes | Display-rule pop-ups (exit, scroll, timed) | UI-only |
| Payments | Sell products/services via PayPal, Stripe, PayU | UI config; orders managed in-app |
| Orbit MCP Server | Connects Lunar + Solis to your LLM (Scale+, in development) | MCP (primary AI/programmatic interface) |
| Solis | AI behavioral insights, alerts, optimization tips | UI; reachable via Orbit MCP |
| Agency / sub-accounts | Client sub-accounts, white-label branding (Scale+) | UI-only |

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify against the live pricing page; annual billing shown ("2 months free" vs monthly).*

| Plan | Price (annual) | Pages | Visits/mo | Domains | Credits/mo | Key unlocks |
|---|---|---|---|---|---|---|
| **Build** | $24/mo | 10 | 2,000 | 1 | 2,500 | Lunar AI, classic builder, forms, basic analytics |
| **Optimize** | $119/mo | 100 | 30,000 | 3 | 10,000 | + Solis AI insights, EventTracker, **A/B testing**, Smart Sections, multi-language |
| **Scale** | $229/mo+ | Unlimited | 100,000–500,000 | 10 | 20,000 | + **Orbit MCP server**, **programmatic pages**, client sub-accounts, agency branding |
| **Enterprise** | $1,199/mo+ | Unlimited | 1M+ | 100 | 60,000 | + domain whitelisting, **enterprise SSO**, dedicated account manager |

- **Free trial**: 14 days, full-feature; 30-day money-back guarantee; credit card required.
- **Credits**: a monthly pool consumed by AI generation (Lunar, AI copy/SEO). Running out blocks AI until top-up or upgrade. Add-on bundles ~$15–$40 pay-as-you-go.
- **Add-ons**: extra custom domain ~$5/mo.
- **Plan-break risk for integrations**: A/B testing/EventTracker/Smart Sections need **Optimize+**; programmatic pages, sub-accounts, and the **Orbit MCP server** need **Scale+**; SSO is **Enterprise**. Visit caps per tier can throttle high-traffic pages.

## Integrations

- **Direction**: Landingi mostly **pushes leads out** (form submission → webhook/ESP/CRM) and lets you **read** pages/forms/leads back via the REST API. It is a lead source, not a system of record.
- **Native**: 170+ integrations across CRMs, ESPs, analytics (Google Analytics, Google Tag Manager), and ad platforms; payment gateways PayPal/Stripe/PayU.
- **Zapier**: lead/form triggers to 6,000+ apps for no-code routing.
- **WordPress plugin** (`landingi-landing-pages`): publish Landingi pages on your WordPress domain; connect with a generated **API token**.
- **MCP**: Orbit (Scale+) exposes Lunar + Solis to an LLM client (Claude, etc.) — generate pages and pull insights from your AI workspace.

## Data model

Key objects: **landing page**, **form**, **form submission / lead**. IDs are per-object; the API is JSON over HTTPS at `https://api.landingi.com/v1` (X-Api-Key) or `/v2` (OAuth Bearer). Shapes below are constructed from community-documented field lists.

<!-- Constructed from docs — verify against live API -->
```json
// Landing page (GET /landing_pages → list; GET /landing_pages/{id} → one)
{
  "id": "lp_8421",
  "name": "Spring Webinar Registration",
  "url": "https://go.example.com/spring-webinar",
  "status": "published",
  "account_id": "acc_1207",
  "created_at": "2026-06-01T10:22:00Z",
  "updated_at": "2026-06-20T14:03:00Z"
}
```

<!-- Constructed from docs — verify against live API -->
```json
// Form submission / lead (GET /forms/{formId}/submissions)
{
  "id": "sub_55123",
  "form_id": "frm_902",
  "landing_page_id": "lp_8421",
  "submitted_at": "2026-06-21T09:15:42Z",
  "fields": {
    "email": "jane@example.com",
    "name": "Jane Doe",
    "company": "Acme Co"
  }
}
```

<!-- Constructed from docs — verify against live API -->
```json
// Webhook payload pushed to your endpoint on form submit
// (configured per form; format mirrors the mapped fields + your extra params)
{
  "email": "jane@example.com",
  "name": "Jane Doe",
  "source": "landingi"
}
```

## Quick-start recipes

### Recipe 1 — Pull new leads into a CRM (API poll)

Trigger: scheduled job (cron) reconciles leads into your CRM. Steps: list submissions for a form → map fields → upsert into CRM.

```bash
curl -s "https://api.landingi.com/v1/forms/frm_902/submissions" \
  -H "X-Api-Key: $LANDINGI_API_KEY" \
  -H "Accept: application/json"
```

```python
import os, requests, time

BASE = "https://api.landingi.com/v1"
HEADERS = {"X-Api-Key": os.environ["LANDINGI_API_KEY"], "Accept": "application/json"}

def get_submissions(form_id):
    url = f"{BASE}/forms/{form_id}/submissions"
    for attempt in range(5):
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 429:                      # rate limited
            wait = int(r.headers.get("Retry-After", 2 ** attempt))
            time.sleep(wait); continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("rate limited after retries")

for sub in get_submissions("frm_902").get("data", []):
    f = sub.get("fields", {})
    crm_upsert(email=f.get("email"), name=f.get("name"), source="landingi")
```

Gotchas: handle `429` with `Retry-After` backoff; the exact response envelope (`data` vs root array) and field key for email vary — confirm against a live call.

### Recipe 2 — Real-time lead webhook (no polling)

Trigger: form submission. Steps: in the page editor open the form's **Settings → Integrations → Webhook**, set the **Request URL**, choose **POST**, map form fields to your server fields, optionally add a static param (e.g. `source:landingi`) and a custom header (e.g. `API_KEY: ...`), then **publish**.

```python
from flask import Flask, request, abort
app = Flask(__name__)

@app.post("/landingi-lead")
def landingi_lead():
    # Optional shared-secret check via the custom header you set in Landingi
    if request.headers.get("API_KEY") != os.environ["LANDINGI_WEBHOOK_SECRET"]:
        abort(401)
    data = request.form or request.json or {}        # POST body (form-encoded or JSON)
    crm_upsert(email=data.get("email"), name=data.get("name"), source="landingi")
    return ("", 204)
```

Gotchas: webhooks are **per-form**, fire on **submission only**, and have **no published HMAC signature** — use the custom-header shared secret to authenticate. GET-method webhooks pass fields as query params instead of a body.

### Recipe 3 — Generate a page from your LLM via Orbit MCP

Trigger: you want to draft/optimize pages without leaving Claude/Cursor. Steps: on a **Scale+** plan, enable the **Orbit MCP server**, add it to your MCP client config, then prompt the LLM to generate a page (Lunar) or pull insights (Solis). Orbit is in development — confirm current availability and the exact connection string in-account.

## Integration patterns

- **CRM sync architecture**: webhook for real-time inserts + a nightly `GET /forms/{formId}/submissions` reconciliation to catch missed deliveries (no delivery guarantee on form webhooks). Dedupe on email; map Landingi form fields → CRM properties once and keep the mapping in code.
- **Auth choice**: use a dashboard **API key** (`X-Api-Key`) for server-to-server scripts you own; use **OAuth 2.0** (authorization code grant, Bearer token, scopes like `read_landing_pages`) when building an app that accesses other users' Landingi accounts.
- **Rate limits**: treat `429` as the signal; honor `Retry-After`, exponential backoff, and cap concurrency. No published quota numbers — measure and stay conservative.
- **Versions**: community sources show both `/v1` (X-Api-Key) and `/v2` (OAuth) and both `/landing_pages` and `/landing-pages` path styles — verify the active version and path against your account's API docs before hardcoding.
