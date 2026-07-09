# ShortStack Platform Guide

Full reference for the `sales-shortstack` skill. Read the section you need; don't dump the whole file.

> *Pricing/features are best-effort from research (2026-06) — the marketing site; the help center is Cloudflare-protected. Verify in-account.*

## What ShortStack is

A **campaign platform** for **contests, giveaways, sweepstakes, and lead-capture promotions** — plus landing pages, pop-ups, quizzes, refer-a-friend, instant-win, and social promos (hashtag contests, comment-to-enter). You build a **campaign** with a drag-and-drop builder, collect **entries/leads**, draw a winner automatically, and sync/export the list. 50,000+ businesses; big-brand customers (UFC, Netflix, Live Nation, Ticketmaster) alongside SMBs/agencies. 1 billion+ entries processed.

**Contest/giveaway, not affiliate.** Refer-a-friend here is a contest entry mechanic (more entries for referrals), not commission-based affiliate tracking. For affiliates use `/sales-affiliate-program`.

## Module map — API vs webhook vs UI-only

| Module | Surface | Notes |
|---|---|---|
| Campaign builder / templates | **UI-only** | contests, quizzes, pages — no create-campaign API |
| Entry / lead capture | **API (read) + webhook** | the entrant identity flows out here |
| Entries API | **API** | `GET https://entries.shortstack.com/entries` |
| Real-time new-entry push | **Signed webhook** | `X-Ss-Signature` HMAC |
| Webhooks management | **API** | configure/test webhooks programmatically |
| Sandbox | **API** | test environment |
| Winner selection | **UI (automatic)** | random draw |
| Native ESP/CRM | **Integration** | Mailchimp (direct), HubSpot, Salesforce |
| Zapier / hundreds of tools | **iPaaS** | via webhooks |
| Lead export | **UI** | CSV |
| Analytics | **UI** | campaign dashboard |

## Pricing & plan gates (best-effort)

- **Free-forever** plan (no credit card) — basic campaigns.
- **Paid tiers** scale entry volume, advanced campaign types, white-labeling, and team/agency/enterprise features (specific prices not published on the landing page — verify). ShortStack serves up to enterprise (big brands/agencies), so confirm what your tier includes (entry caps, API access, white-label).

## Data model (entry — JSON shape)

Entries API returns:

```json
{ "data": [
  {
    "id": 987654,
    "campaign_id": 123,
    "email": "jane@example.com",
    "first_name": "Jane",
    "received": "2026-06-27T10:00:00Z",
    "fields": { "custom_q": "answer" }
  }
] }
```

- **Identity = email** (+ `id`). Dedupe/reward on the entry `id`.
- Exact per-entry fields depend on the campaign form — inspect a real response (help center is bot-protected, so the published schema is partial).
- The **webhook payload** is the same entry shape, POSTed on each new entry.

## Quick-start recipes

### Recipe 1 — Pull entries via the Entries API

```bash
# newest-first, 50 at a time (per_page max 5000)
curl -i -H "Authorization: Token token=$SHORTSTACK_API_KEY" \
  "https://entries.shortstack.com/entries?sort=received&direction=descending&per_page=50"
```

Python:

```python
import requests
r = requests.get(
    "https://entries.shortstack.com/entries",
    headers={"Authorization": f"Token token={API_KEY}"},
    params={"sort": "received", "direction": "descending", "per_page": 100},
)
entries = r.json()["data"]
```

Note the literal `Token token=` prefix. Page newest-first; for >5000 confirm the cursor/offset in the live docs.

### Recipe 2 — Verify the signed webhook (real-time entries)

ShortStack POSTs each new entry to your URL with an `X-Ss-Signature` header = HMAC(raw body + your secret).

```python
import hmac, hashlib

@app.post("/shortstack-webhook")
async def shortstack_webhook(request):
    raw = await request.body()                 # RAW bytes, before JSON parse
    expected = request.headers.get("X-Ss-Signature", "")
    digest = hmac.new(SHORTSTACK_SECRET.encode(), raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(digest, expected):   # constant-time
        return Response(status_code=401)
    entry = json.loads(raw)
    if not already_processed(entry["id"]):     # dedupe on entry id
        upsert_lead(entry)
        mark_processed(entry["id"])
    return {"ok": True}
```

Confirm the exact HMAC algorithm/encoding against a live delivery (the docs are bot-protected; the signature = body + secret is confirmed, the hash function is to verify). Prefer the webhook over polling for real-time.

### Recipe 3 — Sync entrants to an ESP (no code)

Connect **Mailchimp** (direct), **HubSpot**, or **Salesforce** in the campaign settings so entrants sync automatically; or use **Zapier** (new-entry trigger via webhook) for other tools. Turn on double opt-in to filter junk.

## Fraud & quality watch

Viral contests attract fake/disposable emails and same-person multi-entry. Validate emails before counting/rewarding, add friction (double opt-in), and review entries before the automatic winner draw. For list quality/deliverability afterward, use `/sales-deliverability`.

## When to route out

- Which contest tool / viral mechanics across tools → `/sales-audience-growth`
- Generic CRM/ESP wiring (iPaaS) → `/sales-integration`
- Email sequences for the collected list → `/sales-email-marketing`
- Deliverability of the emails you collect → `/sales-deliverability`
- Commission-based **affiliate** program (not contest referrals) → `/sales-affiliate-program`
