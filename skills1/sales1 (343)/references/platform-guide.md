# Memberful Platform Guide

Full reference for the `sales-memberful` skill. Read the section you need; don't dump the whole file.

> *Pricing/features are best-effort from research (2026-06) — marketing site + developer docs + reviews. Verify in-account.*

## What Memberful is

A **membership + paid-subscription layer** (owned by **Patreon**) for **creators, publishers, and communities** — podcasters, bloggers, independent journalists, clubs/associations. You add paid memberships, **gated content**, **private podcasts**, **newsletters**, and **digital downloads** to a site you control, charging through **your own Stripe account** (Memberful never holds the funds). It's a membership/payments + auth layer — **not** a hosted course/LMS and **not** an email tool.

**You own the audience and brand.** Add it via the **WordPress plugin**, Memberful's **website builder**, or a **custom site** through the **GraphQL API** + **OAuth**.

## Module map — API vs front-end vs webhook vs UI

| Module | Surface | Notes |
|---|---|---|
| Members / subscriptions / orders | **GraphQL API** | query + mutate; cursor pagination |
| Passes (dashboard "Plans") + Plans (dashboard "Prices") | **GraphQL API** | ⚠️ terminology swap — see below |
| Coupons | **GraphQL API** | create/manage discounts |
| Member metadata (custom JSON) | **GraphQL API only** | 50 keys / 40-char key / 500-char value |
| Checkout (one-click, trials, coupons) | **Hosted UI + WordPress** | runs on your Stripe account |
| Content gating | **WordPress plugin / website builder / OAuth** | restrict pages, posts, downloads |
| Sign in with Memberful (SSO) | **OAuth (server-side middleware)** | member identity in your own app |
| Lifecycle events (signup/renewal/refund…) | **Webhooks (HMAC-SHA256)** | 21 events |
| Discord / Mailchimp / Kit / Zapier | **Native integrations** | role + audience sync |

## ⚠️ The Plan-vs-Pass terminology trap

Dashboard and API names are swapped:

- Dashboard **"Plan"** = API **`Pass`** (the membership members subscribe to).
- Dashboard **"Price"** = API **`Plan`** (a pricing variant, e.g. "$10/month").

Read `memberful-api-reference.md` before writing any query — using the wrong name is the #1 first-integration error.

## Pricing (best-effort, 2026)

- **Free** $0/mo — **10%** Memberful fee.
- **Pro** $25/mo — **4.9%** fee.
- **Premium** $100/mo — **4.9%** fee.
- **Plus Stripe** (2.9% + 30¢) on every transaction; **bring your own Stripe account**.

The fee is the real cost lever: the Free plan's **10%** cut dwarfs the $25/mo Pro upgrade once you have any volume — do the math at your MRR.

## Data model (member / webhook — JSON shapes)

**Member (GraphQL, conceptual — confirm fields in the API Explorer):**

```json
{
  "id": 6945121,
  "fullName": "John Doe",
  "email": "john.doe@example.com",
  "username": "john_doe",
  "subscriptions": [
    { "id": 1, "active": true, "pass": { "id": 10, "name": "Supporter" } }
  ]
}
```

**Webhook payload** (`member_signup`) — see `memberful-api-reference.md` for the full example. Key fields: `event`, `member.id`, `member.email`, `member.stripe_customer_id`, `member.discord_user_id`, `member.signup_method`, `member.tracking_params` (UTMs).

## Quick-start recipes

### Recipe 1 — Query members + their subscriptions (GraphQL, paginated)

```python
import requests
URL = "https://ACCOUNT-URL.memberful.com/api/graphql"
H = {"Authorization": f"Bearer {MEMBERFUL_API_KEY}", "Content-Type": "application/json"}

q = """
query($after: String) {
  members(first: 100, after: $after) {
    pageInfo { hasNextPage endCursor }
    edges { node { id email fullName subscriptions { active pass { name } } } }
  }
}
"""
after, members = None, []
while True:
    r = requests.post(URL, json={"query": q, "variables": {"after": after}}, headers=H).json()
    conn = r["data"]["members"]
    members += [e["node"] for e in conn["edges"]]
    if not conn["pageInfo"]["hasNextPage"]:
        break
    after = conn["pageInfo"]["endCursor"]
```

Remember: HTTP 200 even on error — check `r.get("errors")`. The dashboard "Plan" you see is the API **`pass`** here.

### Recipe 2 — Verify a signed webhook, then re-fetch from the API

```python
import hmac, hashlib

@app.post("/memberful-webhook")
async def memberful_webhook(request):
    raw = await request.body()                                   # RAW bytes
    sig = request.headers.get("X-Memberful-Webhook-Signature", "")
    expected = hmac.new(MEMBERFUL_WEBHOOK_SECRET.encode(), raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):                   # constant-time
        return Response(status_code=401)
    e = json.loads(raw)
    if e["event"] in ("member_signup", "subscription.created"):
        member_id = e["member"]["id"]
        fetch_member_from_graphql(member_id)                     # authoritative current state
    return {"ok": True}
```

HMAC-SHA256 over the **raw body** with the **Webhook secret** (Settings → Webhooks). Then re-query GraphQL for the current record — the payload is a point-in-time snapshot. Note event names mix `_` and `.`.

### Recipe 3 — Gate your own app with "Sign in with Memberful" (OAuth)

Use Memberful **OAuth** so members log into your custom app with their Memberful account. The OAuth callback runs in **server-side middleware** (Node/Python/serverless) — exchange the code for tokens there, then read the member's active passes to authorize. Pair with the GraphQL API to pull subscription state. See `developers` docs under Custom Applications.

## When to route out

- Choosing/comparing membership or course platforms → `/sales-membership`
- Checkout / trial / dunning / upsell **optimization** across tools → `/sales-checkout`
- Email sequences/newsletters to members (Memberful doesn't send marketing email) → `/sales-email-marketing`
- Wiring Memberful into a CRM/warehouse generically → `/sales-integration`
