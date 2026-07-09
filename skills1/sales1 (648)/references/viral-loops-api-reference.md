<!-- Source: https://developers.viral-loops.com/ (API docs — several pages JS-rendered/404 at capture) -->
<!-- Source: https://documentation.viral-loops.com/en/articles/12080870-api-endpoint-articles -->
<!-- Source: https://zapier.com/apps/viral-loops/integrations -->
<!-- Captured 2026-06-27. Base URL, auth (publicToken), the participant endpoint, and the webhook/Zapier
     surface are from the knowledge base + Zapier app. The full developer reference is partly JS-rendered
     (some pages returned 404/403). JSON below is CONSTRUCTED from documented fields and marked — verify
     against the live reference / a real campaign before relying. -->

# Viral Loops API Reference

Viral Loops is **campaign-scoped**: you build a campaign (referral / waitlist / giveaway / milestone /
ambassador) in the dashboard, and the API + webhooks let you register participants, read the leaderboard,
and react to referral events. Most integration is done with the **`publicToken`** (a per-campaign public
key) — the same token the front-end widget uses.

## Base URL & authentication

- **Base URL:** `https://app.viral-loops.com/api/v3/`
- **Auth:** a **`publicToken`** (public API key) found in the campaign's **installation / settings**. Pass
  it in the request body or header per the endpoint. It's scoped to one campaign — a different campaign has
  a different token.
- Some server-side/admin operations may use a separate **private/apiToken** — confirm in the live docs.

### Auth quick-start (register a participant)

```bash
curl -s -X POST "https://app.viral-loops.com/api/v3/campaign/participant" \
  -H "Content-Type: application/json" \
  -d '{
        "apiToken": "YOUR_CAMPAIGN_PUBLIC_TOKEN",
        "user": { "firstname": "Sam", "lastname": "Rivera", "email": "sam@example.com" },
        "referrer": { "referralCode": "abc123" }
      }'
```
<!-- Body shape constructed from the documented participant endpoint — verify field names against the live API -->

## Core endpoints

| Operation | Method | Path | Notes |
|---|---|---|---|
| Register / upsert a participant | POST | `/api/v3/campaign/participant` | adds someone to the campaign; optionally attributes a `referrer` so the referral counts |
| Get a participant | GET | `/api/v3/campaign/participant` | fetch by email (returns referral count, position, referral code) |
| Leaderboard | GET | `/api/v3/campaign/leaderboard` | top referrers (for gamified UI) |
| Convert a participant | POST | `/api/v3/campaign/participant/convert` | mark a participant as converted (paid/qualified) <!-- verify path --> |
| Redeem a reward | POST | (reward endpoint) | mark a milestone reward as redeemed <!-- verify path --> |

> Exact paths/params for convert/reward/leaderboard weren't fully fetchable (docs partly JS-rendered) —
> confirm at `developers.viral-loops.com`. The participant POST is the documented core.

## Data model

Identity is **email** within a campaign.

**Participant** <!-- Constructed — verify against live API -->
```json
{
  "user": { "firstname": "Sam", "lastname": "Rivera", "email": "sam@example.com" },
  "referralCode": "abc123",
  "referralCountTotal": 6,
  "rank": 12,
  "referrer": { "email": "friend@example.com", "referralCode": "xyz789" },
  "metadata": { "plan": "trial" }
}
```

## Webhooks

Set up in the **Campaign Wizard** (campaign → integrations/webhooks). Viral Loops **POSTs JSON** to your URL
when campaign events occur. The events mirror the Zapier triggers:

- **New participant** — someone joins the campaign
- **New referral count** — a participant's referral count changes (e.g. 5 → 6)
- **Participant converted** — a participant is marked converted
- **Reward redeemed** — a milestone reward is redeemed (dashboard or API)

**Payload (shape)** <!-- Constructed from the trigger fields — verify against a live delivery -->
```json
{
  "event": "participant.referral_count",
  "campaignId": "cmp_123",
  "participant": {
    "email": "sam@example.com", "firstname": "Sam",
    "referralCountTotal": 6, "referralCode": "abc123",
    "referrer": { "email": "friend@example.com" }
  }
}
```
> No documented HMAC signature was found — restrict the webhook to a secret URL and/or re-verify the
> participant via `GET /campaign/participant` before granting a reward. Make handlers idempotent on
> (email, event) since referral-count events can repeat.

## Zapier (two-way)

The official Zapier app is the no-code path:
- **Triggers:** New Participant, New Referral Count (referral count changed), Participant Converted, Reward
  Redeemed.
- **Actions:** create a new participant in a campaign (e.g. push a lead from another app into Viral Loops).

Make and Pipedream connectors also exist. Use these when you don't want to host a webhook endpoint.

## Pagination, rate limits, errors

Not published in the fetchable docs. Treat list endpoints (leaderboard) as potentially paginated, back off
on 429/5xx, and confirm limits in the live reference.

```python
import requests, time
def vl_post(path, token, payload):
    url = f"https://app.viral-loops.com/api/v3/{path.lstrip('/')}"
    body = {"apiToken": token, **payload}
    for attempt in range(4):
        r = requests.post(url, json=body, timeout=30)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(2 ** attempt); continue
        r.raise_for_status(); return r.json()
    r.raise_for_status()
```

## Gaps / not documented here

- The developer reference (`developers.viral-loops.com`) is partly JS-rendered; exact paths for
  convert/reward/leaderboard, full field schemas, the public-vs-private token split, pagination, and rate
  limits need confirming in-account. The participant POST, webhook events, and Zapier surface are solid.
- No documented webhook HMAC signature; no OpenAPI/Postman found; no MCP server.
- The marketing site (`viral-loops.com`) returned 403 to automated fetches — use the knowledge base
  (`documentation.viral-loops.com`) and the in-app campaign settings instead.
