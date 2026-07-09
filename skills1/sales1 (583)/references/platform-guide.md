# SweepWidget Platform Guide

Full reference for the `sales-sweepwidget` skill. Read the section you need; don't dump the whole file.

> *Pricing/features are best-effort from research (2026-07) — captured from the marketing site, help docs, and third-party listings. Verify in-account before relying on specifics.*

## What SweepWidget is

A **giveaway, contest, and sweepstakes builder** for viral list/social growth (sweepwidget.com). You build a **giveaway** (aka "competition") with a drag-and-drop builder, collect **entries** via **100+ entry methods** across **30+ social platforms** (follows, likes, shares, comments, email subscribe, refer-a-friend, custom form fields, leaderboard scores, photo/video, API-verified actions, crypto/NFT airdrops), draw winners, and sync/export the entrant list. Free-forever plan up to Enterprise. Positioned as a lower-cost, higher-limit alternative to Gleam/ShortStack, with unlimited entries and unlimited contests on all plans.

**Contest/giveaway, not affiliate.** Refer-a-friend here is a giveaway *entry mechanic* (bonus entries for referrals), not commission-based affiliate tracking. For affiliates use `/sales-affiliate-program`. (SweepWidget *also* runs its own 25%-recurring affiliate/partner program for reselling SweepWidget itself — separate thing; see the affiliate note below.)

## Module map — API vs webhook vs UI-only

| Module | Surface | Notes |
|---|---|---|
| Giveaway ("competition") builder | **UI + API** | drag-and-drop in UI; also `create-giveaway` / `update-giveaway` / `delete-giveaway` (Enterprise API) |
| Entry methods / actions (110+) | **UI + API** | `create-entry-method` / `update-entry-method` / `delete-entry-method` |
| Entry / lead capture | **API (read) + webhook** | entrant identity flows out here |
| Read entries / users / winners | **API** | `/entries`, `/users`, `/winners`, `/user-entries`, `/user-entered-giveaways` |
| Real-time entry push | **Signed webhook** | `X-SweepWidget-Signature` HMAC-SHA256; Enterprise-only |
| Client-side events | **JavaScript callbacks** | `window.addEventListener('sweepwidget.entry_submitted', …)` — no Enterprise needed |
| Prizes / unlock rewards / coupons | **API + UI** | `create-prize`, `create-reward` (coupon codes, locked rewards) |
| Manual entries | **API** | `add-manual-entries` |
| Email whitelist | **API** | `white-list-emails` (Premium+ feature) |
| Winner selection | **UI** | random draw / leaderboard |
| Anti-spam / fraud (device fingerprint) | **UI-only** | 300+ data points; flag resolution via support, not API |
| Native ESP/CRM (38+ email APIs, 65+ total) | **Integration** | Mailchimp, etc. |
| Zapier / WordPress plugin / Shopify app | **iPaaS / plugin** | |

## Pricing & plan gates (best-effort)

| Plan | Monthly | Annual | Key gates |
|---|---|---|---|
| **Free** | $0 | $0 | Unlimited entries, but entrant personal info (name/email/location) **truncated past 10 users**; **no verified entries** |
| **Pro** | $29 | $290 | Unlimited verified entries + full entrant data; 1 brand; 40 actions/contest; 5 repeatable; 50 winners; 100 purchases tracked |
| **Business** | $59 | $590 | 2 brands/team; 60 actions; 250 winners; 5,000 coupons; unlocks crypto, advanced Reddit/Telegram/Discord/LinkedIn entry methods |
| **Premium** | $119 | $1,190 | 3 brands/team; 80 actions; 1,000 winners; **remove branding**; geo-blocking, email whitelisting, CSV imports |
| **Enterprise** | $249 | $2,490 | 5 brands/team; 125 actions; unlimited winners; **API access**, **server-side webhooks**, phone verification, custom SMTP, dedicated support/account manager |

**The integration gate that matters:** the **REST API and server-side webhooks are Enterprise-only** ($249/mo or $2,490/yr, best-effort). No code integration below Enterprise — use native ESP connectors, Zapier, or client-side JavaScript callbacks instead. Annual billing ≈ 17% off. Verify current pricing in-account.

**Affiliate/partner program:** SweepWidget pays **25% recurring** on referred paid users (e.g. Pro monthly $29 → $7.25/mo). Cookie-based attribution, payout eligible 30 days after payment (no refund/cancel), paid as account credit or cash. Referral link is in Account Settings; a free plan can join. (This is for reselling SweepWidget — distinct from giveaway refer-a-friend.)

## Data model (JSON shapes)

### Entry (from `GET /entries`)

```json
{ "data": [
  {
    "user_id": 123,
    "user_name": "Test User",
    "user_email": "jane@example.com",
    "birthday": "04-25-1994",
    "custom_identifier": "your-reference-id",
    "entry_type": "Twitter Follow",
    "action": "Follow @SweepWidget On Twitter",
    "value": "@MyTwitter",
    "entry_amount": "5",
    "timestamp": "2020-06-26 11:18:21",
    "country": "United States"
  }
] }
```

### Giveaway (from `GET /giveaways`)

```json
{ "data": [
  {
    "competition_id": 123,
    "competition_url": "ahej14f9",
    "type": "Live",
    "title": "My Giveaway Title",
    "description": "This is the description of my awesome giveaway!",
    "rules": "US, CA, 18+",
    "start_time": "2020-07-28 00:00:00",
    "end_time": "2020-08-28 00:00:00",
    "time_zone": "America/Chicago",
    "number_of_winners": "5",
    "image_loc": "https://sweepwidget.com/images/my-image.jpg",
    "giveaway_embed_code": "PGRpdiBpZD0i..."
  }
] }
```

### Webhook payload (`entry_submitted`)

```json
{
  "event": "entry_submitted",
  "data": {
    "competition_id": "12345",
    "user": { "email": "jane@example.com", "name": "Jane Smith" },
    "entries": 5,
    "referral_url": "https://sweepwidget.com/c/my-giveaway-abc123"
  }
}
```

- **Identity = user email + `competition_id`.** Dedupe/reward on that pair (there's a numeric `user_id` in API reads; webhooks key on email).
- The three webhook events (`entry_submitted`, `task_completed`, `all_entries_completed`) share this envelope; `task_completed` adds task details + remaining-task counts.

## Quick-start recipes

### Recipe 1 — Pull entries via the REST API (Enterprise)

```bash
# scope to one giveaway; loop page_start (50 rows/page) until a short page
curl -i -H "Authorization: Bearer $SWEEPWIDGET_API_KEY" \
  "https://sweepwidgetapi.com/sw_api/entries?competition_id=123&page_start=1"
```

Python (page through all entrants):

```python
import requests

BASE = "https://sweepwidgetapi.com/sw_api"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def all_entries(competition_id):
    page, out = 1, []
    while True:
        r = requests.get(f"{BASE}/entries",
                         headers=HEADERS,
                         params={"competition_id": competition_id, "page_start": page})
        rows = r.json().get("data", [])
        out.extend(rows)
        if len(rows) < 50:      # short page => done (fixed 50/page)
            break
        page += 1
    return out
```

Reads are Enterprise-gated. Always pass `competition_id`. `/winners` and `/users` follow the same shape/paging.

### Recipe 2 — Verify the signed webhook (real-time entries, Enterprise)

SweepWidget POSTs each event to your HTTPS URL with `X-SweepWidget-Signature: sha256=<hmac>` where the HMAC is HMAC-SHA256 of the **raw body** using your signing secret (shown when you first save the webhook URL under Integrations → Webhooks).

```python
import hmac, hashlib, json

@app.post("/sweepwidget-webhook")
async def sweepwidget_webhook(request):
    raw = await request.body()                      # RAW bytes, before JSON parse
    header = request.headers.get("X-SweepWidget-Signature", "")
    sent = header.split("=", 1)[1] if "=" in header else header   # strip 'sha256='
    digest = hmac.new(SIGNING_SECRET.encode(), raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(digest, sent):       # constant-time
        return Response(status_code=401)
    evt = json.loads(raw)
    key = (evt["data"]["user"]["email"], evt["data"]["competition_id"])
    if not already_processed(key, evt["event"]):    # dedupe: events repeat
        upsert_entrant(evt)
        mark_processed(key, evt["event"])
    return {"ok": True}
```

Use the **Send Test** button in the dashboard to confirm your endpoint receives and verifies. Prefer the webhook over polling for real-time.

### Recipe 3 — No-Enterprise path: client-side callback + ESP/Zapier

If you're not on Enterprise, you can't use the REST API or server-side webhooks. Options:

```javascript
// Client-side event on the page where the widget is embedded (no Enterprise needed).
// Good for tracking pixels, custom UI, analytics — NOT a trusted server signal.
window.addEventListener('sweepwidget.entry_submitted', function (e) {
  console.log(e.detail.user.email);
});
```

For server-side data on lower plans, connect a **native email/ESP integration** (38+ email APIs) so entrants sync to your list automatically, or route via **Zapier**. These are the supported no-code paths below Enterprise.

## Integration patterns

- **CRM/warehouse sync (Enterprise):** poll `/entries` per live `competition_id` on a schedule, or (better) receive the signed webhook and upsert. Key on `user_email` + `competition_id`; store `custom_identifier` if you pass your own reference id. Handle the fixed 50-row paging.
- **Webhook listener:** HTTPS endpoint, verify `X-SweepWidget-Signature` (HMAC-SHA256 of raw body), respond 2xx fast, dedupe on (email, competition_id, event) — the three events fire independently and can retry.
- **Fraud handling:** SweepWidget's device fingerprint (300+ points) blocks most bots/dupes but false-positives happen (resolved via support). Add your own email validation (block disposable domains) before rewarding, and prefer login-required/verified entry methods. Honor-system entries (YouTube likes/comments) are unverifiable — don't count them as verified.

## Fraud & quality watch

Viral giveaways attract fake/disposable emails, duplicate entries, and self-referrals. SweepWidget mitigates with device fingerprinting and login-required entry methods, but you should still validate emails before counting/rewarding and review top referrers. For list quality/deliverability of the collected emails afterward, use `/sales-deliverability`.

## When to route out

- Which giveaway tool / viral mechanics across tools → `/sales-audience-growth`
- Generic CRM/ESP wiring (iPaaS) → `/sales-integration`
- Email sequences for the collected list → `/sales-email-marketing`
- Deliverability of the emails you collect → `/sales-deliverability`
- Commission-based **affiliate** program (not giveaway referrals) → `/sales-affiliate-program`
