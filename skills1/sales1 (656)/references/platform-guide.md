# Waitlister Platform Reference

## Overview

Waitlister (waitlister.me) is a no-code pre-launch waitlist platform with hosted landing pages, a points-based viral referral system, and — unusually for the category — **built-in email broadcasts**, so you can message your waitlist without wiring up an external ESP. Its developer surface (REST API, five HMAC-signed webhook events) is the most complete in the indie waitlist family. Targets startup founders, e-commerce launches, mobile app betas, and course creators.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Landing pages | Drag-and-drop builder + AI page builder (credit-gated: 2 free / 15 Launch / 40 Growth / 100 Business per month), templates, custom domains (Growth+: 3, Business: unlimited) | UI-only |
| Embeddable forms | Form embeds for 20+ site builders (Framer, Webflow, Shopify, WordPress, Bubble, Squarespace…) | Embed install; **API-accessible** via add-subscriber for custom forms |
| Referral system | Points-based queue jumping, leaderboard, position inflation, milestones (Launch+) | API: `points` writable via update-subscriber; webhooks: `referral_completed`, `milestone_reached` |
| Email | Welcome emails, broadcast campaigns, double opt-in, custom email domains (Growth+) | UI-only (no send-email API); monthly caps 2,500/10K/50K |
| Spam & fraud | CAPTCHA, email validation, referral fraud detection (Growth+) | API signups participate only if you forward `metadata.client_ip` + `fingerprint` |
| Analytics | Growth metrics, geo, referral performance, conversion tracking via GTM/FB Pixel (Growth+) | **API-accessible**: `POST /log-view` for custom-page view tracking |
| Subscribers | CSV export, custom fields, surveys, phone collection | **API-accessible**: add / list / get / update (no delete) |
| Webhooks | 5 events, HMAC SHA-256 signed, retries, auto-disable after 10 failures | **Webhook-accessible** (Growth+) |
| Team | 5 seats | UI-only (Business) |
| Zapier / Make / MCP | — | **Does not exist** — webhooks/API are the only automation path |

## Pricing, limits & plan gates

> Best-effort from waitlister.me/pricing as of 2026-06-06 — verify before committing. Monthly or yearly (yearly ≈ 2 months free).

| Plan | Price | Limits | Key unlocks |
|---|---|---|---|
| Free | $0 | 100 subscribers, 1 waitlist | Landing/AI page builder (2 credits), embeds, surveys, phone collection, CSV export, basic spam prevention, basic analytics |
| Launch | $15/mo ($12/mo annual) | Unlimited subscribers, 3 waitlists, 2,500 emails/mo | **Referral program**, double opt-in, position inflation, welcome emails, **broadcasts**, advanced spam prevention, remove branding, custom thank-you page |
| Growth | $49/mo (~$41/mo annual) | Unlimited waitlists, 10,000 emails/mo, 3 custom domains, 1 custom email domain | **API + webhooks**, Klaviyo/Mailchimp/Kit integrations, **fraud detection**, bulk import, conversion tracking, translations, advanced analytics |
| Business | $129/mo (~$108/mo annual) | 50,000 emails/mo, unlimited custom domains, 3 custom email domains | Team (5 seats), priority API access, 120 RPM rate limit (vs 60) |

**Gates that bite:**
- **API, webhooks, ESP integrations, and fraud detection all start at Growth ($49/mo)** — any programmatic pipeline forces Growth minimum. Free/Launch = UI + CSV export.
- **Referrals and broadcasts start at Launch ($15/mo)** — the free tier is capture-only.
- **Email sends are capped monthly** (2,500/10K/50K); overage behavior is undocumented — plan broadcast cadence against the cap, or hand off to your ESP via the Klaviyo/Mailchimp/Kit connector.
- Custom domains require Growth+ ($49/mo minimum).
- Rate limits: 60 RPM (Growth) / 120 RPM (Business) on subscriber endpoints.

## Integrations

**Data egress** (Growth+): native Klaviyo / Mailchimp / Kit connectors, webhooks (5 events), REST API (list/get), CSV export (all plans).
**Data ingress**: REST API add-subscriber, embeddable forms, hosted pages, bulk import (Growth+).
**No Zapier, no Make, no MCP server** — competitors like KickoffLabs and UpViral have Zapier; with Waitlister you build the glue yourself on webhooks/API.
Site builders (embed-only): Framer, Webflow, Shopify, WordPress, Bubble, Squarespace + ~20 more.

## Data model

One core object: the **subscriber**. Shape from the list endpoint:

```json
{
  "id": "xyzABC123",
  "email": "user@example.com",
  "deliverability": "unconfirmed",
  "name": "John Doe",
  "phone": "+1234567890",
  "position": 42,
  "inflated_position": 42,
  "points": 150,
  "referral_code": "happy-star-4f3d",
  "referred_by": "cool-moon-9e2a",
  "referral_count": 3,
  "sign_up_token": "abc123xyz",
  "thank_you_url": "https://waitlister.me/thank-you/...",
  "metadata": {},
  "referring_domain": "twitter.com",
  "ip_address": "192.168.1.1",
  "country": "US",
  "city": "San Francisco",
  "joined_with": "api",
  "joined_at": 1682345678901
}
```

- `referral_code` = the subscriber's own share code; `referred_by` = the code of whoever referred them
- `points` drives `position`; `inflated_position` reflects the position-inflation display setting
- `joined_with` distinguishes `api` vs landing-page signups
- Webhook envelopes wrap event-specific shapes — see `waitlister-api-reference.md` for all five verbatim payloads

## Quick-start recipes

### Recipe 1 — Server-side signup with referral attribution + fraud protection

For custom signup forms posting to your backend. Forward the end-user's IP and a browser fingerprint or fraud detection silently skips API signups.

```bash
curl -X POST "https://waitlister.me/api/v1/waitlist/YOUR_WAITLIST_KEY/sign-up" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $WAITLISTER_API_KEY" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "metadata": {
      "referred_by": "happy-star-4f3d",
      "client_ip": "203.0.113.42",
      "fingerprint": "abc123def456",
      "plan_interest": "pro"
    }
  }'
```

Use the response: show `position` (or `inflated_position`) and `referral_code` on your own thank-you screen, or redirect to `redirect_url`. If `is_pending_confirmation` is true (double opt-in), show "check your email" instead of a position.

**Gotchas**: `referred_by` carries the *referrer's* code parsed from your `?ref=` URL param — your frontend must pass it through. API key stays server-side.

### Recipe 2 — Signed webhook handler routing events to CRM/ESP (Growth+)

```python
import hmac, hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
SECRET = "your-webhook-secret"
seen_deliveries = set()  # durable store in production

@app.route("/hooks/waitlister", methods=["POST"])
def waitlister_hook():
    # Verify HMAC over the RAW body (docs-provided scheme)
    raw = request.get_data(as_text=True)
    expected = "sha256=" + hmac.new(SECRET.encode(), raw.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(request.headers.get("X-Webhook-Signature", ""), expected):
        return jsonify(ok=False), 401

    # Dedupe on delivery id — Waitlister retries failed deliveries
    delivery_id = request.headers.get("X-Waitlister-Delivery")
    if delivery_id in seen_deliveries:
        return jsonify(ok=True)
    seen_deliveries.add(delivery_id)

    body = request.get_json()
    event, data = body["event"], body["data"]

    if event == "waitlist.signup_created":
        add_to_crm(email=data["email"], name=data.get("name"),
                   position=data["position"], referred_by=data.get("referred_by"),
                   utm_source=data["metadata"].get("source"))
    elif event == "waitlist.referral_completed":
        bump_crm_score(data["referrer"]["email"], data["referrer"]["total_referrals"])
    elif event == "waitlist.milestone_reached":
        fulfill_reward(data["subscriber"]["email"], data["milestone"]["points"])
    elif event == "waitlist.subscriber_unsubscribed":
        mark_unsubscribed(data["subscriber"]["email"])

    return jsonify(ok=True)  # respond 2xx within 15 seconds
```

**Gotchas**: respond within 15s or the delivery counts as failed — do slow work async. After 10 consecutive failures the webhook is auto-**Disabled** and stays off until you manually re-enable it; monitor for the Inactive state.

### Recipe 3 — Reward fulfillment: top referrers + programmatic point bumps (Growth+)

Pull the leaderboard for prize fulfillment, or grant bonus points (e.g., "+50 points for completing our survey") via the update endpoint.

```python
import requests, time

BASE = "https://waitlister.me/api/v1/waitlist/YOUR_WAITLIST_KEY"
H = {"X-Api-Key": "your-api-key"}

# Top referrers, paginated (limit max 100; 60 RPM on Growth)
def top_referrers(min_referrals=3):
    page, out = 1, []
    while True:
        r = requests.get(f"{BASE}/subscribers",
                         params={"limit": 100, "page": page,
                                 "sort_by": "referral_count", "sort_dir": "desc"},
                         headers=H)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("X-RateLimit-Reset", 60)) - time.time() + 1)
            continue
        d = r.json()["data"]
        batch = [s for s in d["subscribers"] if s["referral_count"] >= min_referrals]
        out += batch
        if len(batch) < len(d["subscribers"]) or page >= d["pages"]:
            return out
        page += 1

# Grant bonus points (merges, doesn't replace other fields)
def grant_points(email, new_total):
    return requests.put(f"{BASE}/subscribers/{email}", headers=H,
                        json={"points": new_total}).json()
```

**Gotchas**: `points` is an absolute value, not an increment — read current points first, then write the new total. Watch `X-RateLimit-Remaining`; back off exponentially on 429 (max 30s across 5 attempts per docs).

## Integration patterns

- **ESP handoff**: Waitlister's broadcasts have monthly caps and no advanced segmentation — for segmented or high-volume sends, sync via the native Klaviyo/Mailchimp/Kit connector (Growth+) or the `signup_created` webhook, and broadcast from the ESP.
- **Webhook trust**: always verify `X-Webhook-Signature` (HMAC SHA-256 over raw body); dedupe on `X-Waitlister-Delivery`; treat deliveries as at-least-once.
- **Fraud**: rely on built-in fraud detection (Growth+) for landing-page signups; for API signups, forward `client_ip`/`fingerprint` or they bypass detection. Use `referral_completed` webhooks to maintain your own velocity checks (same-IP bursts) before fulfilling rewards.
- **Double opt-in pipelines**: gate CRM/ESP adds on `deliverability` ≠ `unconfirmed`, or subscribe to `subscriber_pending_expired` to prune contacts who never confirmed.

## Comparison grid

| Platform | Pricing model | API | Webhooks | Email broadcasts | Best for |
|---|---|---|---|---|---|
| **Waitlister** | Free–$129/mo | ✅ Growth $49+ | ✅ 5 events, HMAC | ✅ built in (capped) | Multi-project founders wanting pages + referrals + email in one |
| LaunchList | One-time $0–$79+ | ❌ (planned) | ✅ Grow $79, unsigned | ❌ | One-time-payment waitlists (`/sales-launchlist`) |
| KickoffLabs | $13–$202/mo | ✅ v1+v2 | ✅ fraud flags | ✅ reward emails Premium+ | Waitlists + giveaways + fraud webhooks (`/sales-kickofflabs`) |
| GetWaitlist | $15–$250/mo | ✅ | — | — | Developer-quick widget waitlists (backlog) |
| Prefinery | $39–$399/mo | ✅ | ✅ | ✅ | Beta-launch management at scale (backlog) |
| Viral Loops | $35–$299/mo | ✅ | ✅ | — | Template-driven referral campaigns (backlog) |
| UpViral | $79–$319/mo | ✅ Business+ | ✅ Callback URL | ✅ | B2C sweepstakes/points campaigns (`/sales-upviral`) |
| ReferralHero | $199–$399/mo | ✅ 40+ endpoints | ✅ | — | Multi-level L1/2/3 referral stacks (`/sales-referralhero`) |

**Use Waitlister when**: you want hosted pages + referrals + broadcasts in one tool with a real signed-webhook/API surface, unlimited subscribers from $15/mo, and you're fine building automation glue yourself (no Zapier).

**Don't use Waitlister when**: you need Zapier/Make (KickoffLabs, UpViral), one-time pricing (LaunchList), giveaway/contest mechanics beyond a waitlist (KickoffLabs, UpViral, Gleam), multi-level referral tracking (ReferralHero), or advanced email segmentation (hand off to a full ESP).
