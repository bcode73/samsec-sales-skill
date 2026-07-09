# MemberVault Platform Guide

Detailed reference for MemberVault — the module map (what's integration-accessible vs UI-only), plan gates, the data model, and quick-start automation recipes.

## What MemberVault is

A **"binge & buy" course/membership platform** for solopreneurs, coaches, and creators (membervault.co). Instead of each offer living in isolation, you put **all your paid AND free products in one marketplace**, drive traffic to the freebies, and let people browse everything. MemberVault tracks who views the sales info of products they *don't* own and tags them **warm/hot lead** — so engagement doubles as lead generation. Strong on relationship-driven selling, gamification (Engagement Points), and audience intelligence; deliberately **light** on features otherwise. Best fit: a creator who wants their whole catalog cross-sold in one place and cares about *who's engaged and ready to buy more*, not pixel-perfect design or built-in email.

## Module map — integration surface

| Module | What it does | Integration surface |
|---|---|---|
| **Products** (course, membership, VIP day, 1:1 portal, download, challenge, summit) | Host & deliver any offer | UI-built; **grant access via inbound webhook** or Zapier "Add User to Product" |
| **Members / Users** | One login per person, products attached to email | **Zapier triggers + actions**; **outbound webhook** pushes contact out |
| **Engagement Points (EP) / gamification** | Points for lessons, quizzes, actions | **Zapier triggers** (Completed Lesson/Module, Earned X EP); UI config |
| **Lead scoring (warm/hot)** | Auto-tags users who view unowned products' sales info | **Zapier trigger** (Hot Lead); automatic |
| **Marketplace page** ("binge & buy") | One page showing all offers | UI-only |
| **Communities** | Gamified discussion spaces, gated or ungated | UI-only |
| **Content delivery** | Progressive / date-drip / timed-drip release, quizzes | UI config; completion fires Zapier triggers |
| **Payments** | Direct Stripe + PayPal, **0% platform fees** | UI config |
| **Email** | ❌ Not built in | Wire an ESP (Kit/MailerLite/ActiveCampaign native; others via Zapier/webhooks) |
| **Video hosting** | Limited — most users host elsewhere | Embed (YouTube/Vimeo/Wistia) |

**Rule of thumb:** there's **no public REST API**. Move data in via the **inbound webhook** ("API URL" from Integrations → Advanced) or Zapier actions; move data out via **outbound webhooks** ("Call a web hook" product action) or Zapier triggers. No MCP server.

## Plans & gates (best-effort — verify; pricing changes often)

> *Pricing and plan limits move fast. Treat every number below as best-effort from 2026-06 research and confirm on membervault.co.*

- **Free plan** — exists; **capped at ~100 members** and limited features. Good for validating an offer.
- **5 Product** — ~$29/mo (5 products, 1 community).
- **15 Product** — ~$49/mo (15 products, 3 communities) — marketed "Best Deal."
- **Unlimited** — ~$109/mo (unlimited products + communities, priority support).
- **Lifetime options** — "Cash Kickstart" and "Unlimited Lifetime" deals appear periodically.
- **All paid plans include all features** — tiers differ only by **product/community counts**. **0% transaction fees on every plan** (you connect your own Stripe/PayPal).

When advising: the cost ceiling is usually **product count + Zapier**, not features. If they need many small offers, the 5/15 caps bite quickly.

## Data model

```json
// Member (identity = email)
{ "email": "jane@example.com", "first_name": "Jane", "last_name": "Doe",
  "ep": 120, "lead_status": "hot" }      // EP = Engagement Points; lead_status: warm|hot

// Product
{ "course_id": 100, "name": "Signature Course", "type": "course" }
```

- **Identity is email** — one login per person; products attach to that email. Dedupe on email.
- **EP** drives gamification and the `Earned X EP` trigger.
- **lead_status** is set automatically when a user repeatedly views the sales info of products they don't own — the engine behind "binge & buy."

## Quick-start recipes

### Recipe 1 — Grant access when someone buys on an external cart (inbound webhook)

Get the URL from **Integrations → Advanced** (pick your ESP/Zapier), then have the cart/ESP POST to it on purchase.

```bash
# Shape is documented; confirm exact URL/params from your Integrations → Advanced screen
curl -X POST "https://YOURSUB.vipmembervault.com/api/webhook?course_id=100" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "email=buyer@example.com" \
  --data-urlencode "first_name=Buyer"
```

### Recipe 2 — Route hot leads into outreach (Zapier, Python webhook handler)

Use the **Hot Lead** Zapier trigger → send to your own endpoint (or directly to a CRM). Example handler:

```python
from flask import Flask, request
import requests
app = Flask(__name__)

@app.post("/membervault/hot-lead")
def hot_lead():
    data = request.get_json(force=True)          # Zapier/webhook payload
    email = data.get("email")
    # push the warm/hot lead into your CRM or outreach tool
    requests.post("https://your-crm.example/api/leads",
                  json={"email": email, "source": "membervault-hot-lead"}, timeout=20)
    return ("", 204)
```

This is the highest-leverage MemberVault automation: it turns catalog browsing into a real-time buying-intent signal.

### Recipe 3 — Sync members to an unsupported ESP (outbound webhook)

In the product's **Actions → "Call a web hook,"** set the trigger (purchase / lesson complete / quiz answer). MemberVault POSTs `email`, `first_name`, `last_name` to your ESP's inbound URL. Capture one delivery against webhook.site first to confirm the exact keys, then map them.

## Known limitations to set expectations on

- **No built-in email** — budget for an ESP, and note that connecting "any" ESP often means paying for **Zapier**, which eats into thin margins (a top complaint).
- **Video** — host on YouTube/Vimeo/Wistia and embed; native upload is limited.
- **Marketplace design** — layout is fairly fixed; don't promise heavy visual customization.
- **Member self-cancellation** — canceling a subscription can be clunky for members; document the steps or handle cancellations via your payment processor.
- **Search** — weak once the library is large; lean on the marketplace structure and tags instead.
