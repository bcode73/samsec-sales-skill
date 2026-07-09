# Frill Platform Guide

Full reference for the `sales-frill` skill. Read the section you need; don't dump the whole file.

> *Pricing/features are best-effort from research (2026-06) — marketing site + docs + reviews. Verify in-account.*

## What Frill is

An **affordable customer-feedback suite** — feedback boards + public roadmap + changelog/announcements + surveys + an embeddable widget. Positioned as a cheaper, simpler **Canny / Nolt / UserVoice alternative** (~$25/mo vs Canny's ~$400). Target users: SaaS/product teams, early-stage startups, indie makers (special pricing for startups/nonprofits/open-source).

**Solicited board feedback — not surveys or aggregation.** Frill collects ideas *users submit + vote on* and publishes a roadmap/changelog. For NPS/CSAT *programs* → `/sales-customer-feedback`; for mining *unsolicited* feedback across reviews/social → `/sales-noisely`.

## Module map — API vs widget vs UI

| Module | Surface | Notes |
|---|---|---|
| Ideas / feedback boards | **REST API + widget** | submit, vote, comment; Status + Topics |
| Public roadmap | **API (statuses) + UI** | Idea **Status** = roadmap column |
| Announcements / changelog | **REST API + widget** | release posts + categories |
| Surveys | **Frill-Script** | in-app surveys |
| Embeddable widget | **Frill-Script** | board/roadmap/changelog in your app |
| User identification | **Frill-Script + SSO** | attach votes/ideas to real users |
| Prioritization matrix | **UI** | Benefit/Cost scores → Quick Wins / Major Projects |
| Events | **Webhooks (HMAC-signed)** | idea/vote/comment/announcement |
| 15+ integrations | **Native** | Slack, Jira, Linear, Intercom, Zapier, … |

## Pricing (best-effort)

- Entry **~$25/mo**, up to **Enterprise ~$349/mo**; **14-day free trial** (no card).
- Higher tiers add more boards/admins, white-label, and integrations.
- Discounts for **startups / nonprofits / charities / open-source** on application. Verify on frill.co/pricing.

## Data model (idea / webhook — JSON shapes)

**Idea** (conceptual — confirm exact fields via the `.md` docs / `?ask=`):

```json
{
  "idx": "abc123",
  "name": "Dark mode",
  "status": { "name": "In Progress" },
  "topics": [{ "name": "UI" }],
  "vote_count": 87,
  "comment_count": 12
}
```

**List response** carries `pagination`:

```json
{ "pagination": { "count": 25, "total": 312, "hasNextPage": true, "endCursor": "CURSOR" } }
```

**Webhook payload:** `{ "triggered_at": "…", "event": "idea.created", "data_type": "idea", "data": { … } }`.

## Quick-start recipes

### Recipe 1 — Sync ideas + votes via the API (cursor pagination)

```python
import requests
H = {"Authorization": f"Bearer {FRILL_API_KEY}"}
url, ideas = "https://api.frill.co/v1/ideas", []
while url:
    r = requests.get(url, headers=H).json()
    ideas += r["data"]
    p = r["pagination"]
    url = f"https://api.frill.co/v1/ideas?after={p['endCursor']}" if p["hasNextPage"] else None
```

`Authorization: Bearer` is the recommended auth; loop on `pagination.endCursor` (→ `after`) until `hasNextPage` is false. Keep the key server-side.

### Recipe 2 — Verify a signed webhook (HMAC-SHA256)

Set the webhook in **Settings → Webhooks** (Company Settings) and grab the **Webhook Secret**.

```python
import hmac, hashlib

@app.post("/frill-webhook")
async def frill_webhook(request):
    raw = await request.body()                       # RAW bytes
    sig = request.headers.get("X-Frill-Signature", "")  # confirm exact header name in docs
    expected = hmac.new(FRILL_WEBHOOK_SECRET.encode(), raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):        # constant-time
        return Response(status_code=401)
    e = json.loads(raw)
    if e["event"] == "idea.created" and not seen(e["data"].get("idx"), e["triggered_at"]):
        sync_idea(e["data"])
    return {"ok": True}
```

Events: idea created/updated/deleted/archived/status-changed/merged, voted/unvoted, comment created/updated/deleted, announcement created/published/updated/deleted, notes.

### Recipe 3 — Embed the widget + identify the logged-in user (Frill-Script)

Add the Frill-Script snippet and pass your user's identity so votes/ideas attach to a real account (and enable **SSO** so they're auto-authenticated):

```js
window.Frill_Config = window.Frill_Config || [];
window.Frill_Config.push({
  key: 'YOUR_WIDGET_KEY',
  ssoToken: 'JWT_FROM_YOUR_BACKEND',   // identifies the user (see developers.frill.co/single-sign-on)
});
```

Without identification, board activity is anonymous. See `developers.frill.co/frill-script/identifying-users`.

## When to route out

- VoC / survey **program** strategy (NPS/CSAT) across tools → `/sales-customer-feedback`
- Aggregating **unsolicited** feedback across reviews/social/support → `/sales-noisely`
- Public **review generation** strategy → `/sales-customer-reviews`
- Generic CRM/PM wiring (iPaaS) → `/sales-integration`
