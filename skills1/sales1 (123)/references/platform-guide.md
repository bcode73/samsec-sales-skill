# Convertri Platform Reference

## Overview

Convertri (convertri.com) is a cloud-based sales-funnel and landing-page builder that markets itself as "the world's fastest" — pages served from a CDN with a focus on sub-3-second load times and a free-form "Photoshop-for-your-browser" editor (drag elements anywhere, no rows/columns). It targets digital marketers, online entrepreneurs, and small e-commerce/course sellers who want fast pages plus a built-in cart, upsells, and a members area without stitching tools together. Primary differentiator: page speed + a truly free-form canvas. Primary limitation for builders: there is **no public REST API** — automation runs through a Zapier API key and custom webhooks.

## Capabilities & automation surface

| Capability | What it does | Automation tag |
|---|---|---|
| Free-form page editor | Drag-anywhere placement, ready-made content blocks, mobile-specific design | UI-only |
| Funnels | Multi-page funnel flows (keep ≤20 pages for Zapier) | UI-only (events out via webhook/Zapier) |
| Integrated shopping cart | Checkout with Stripe/PayPal, one-click upsells, bump sells | UI-only; **Sale/Rebill/Refund webhooks** + Zapier triggers |
| Membership delivery | Build + deliver members areas (Scale+) | UI-only; grant access via purchase webhook to a 3rd-party tool |
| Split testing | A/B test pages | UI-only |
| Interactive video | Viewer-tracking, buy buttons at video points, pixel firing on progress | UI-only |
| Dynamic Text Replacement (DTR) | Swap page copy from ad keyword/URL params | UI-only |
| Countdown timers, pop-ups, lightboxes, bars | Urgency + conversion elements | UI-only |
| Page importer | Clone an existing page from another builder | UI-only (Maximize) |
| CDN hosting, free SSL, custom domains | Fast hosting, HTTPS, bring-your-own domains | UI-only |
| Forms / lead capture | Capture leads; map fields | **Lead Capture webhook** (5/form) + Zapier "New Submission" |
| Zapier API key | One account-level key powers all Zaps | API-key |
| Custom webhooks | POST JSON on Sale/Rebill/Refund/Lead Capture with `cverify` signing | webhook-accessible |
| Native integrations | ESPs, payment, webinar, analytics (see below) | UI config (some via Zapier) |

**There is no documented REST API** to programmatically create, read, or update pages/funnels/products. Treat Convertri as "build in the UI, get data out via webhook/Zapier."

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify against convertri.com/pricing.*

| Plan | Price (monthly / annual) | Pages | Custom domains | Impressions/mo | Notable gates |
|---|---|---|---|---|---|
| **Convert** | $99 / $75 | 100 | 5 | 250,000 | Landing pages + fast tech, lead collection |
| **Scale** (popular) | ~$199 | Unlimited | 10 | 500,000 | Funnels, membership sites, A/B testing, pop-ups, advanced analytics, video hosting, DTR |
| **Maximize** | $299 / $199 | Unlimited | Unlimited | Unlimited | Page importer, custom HTML injection, client sub-accounts, no traffic limit |

- **14-day free trial** on all plans.
- **Impression overage**: $30 per additional 250,000 impressions (Convert + Scale).
- **Video bandwidth**: self-hosted video (Scale/Maximize) includes 100GB/mo; overage $10 per additional 100GB.
- **Will my integration break on the cheap plan?** Zapier + custom webhooks are available across plans (the Zapier API key is in Account → Integrations). Membership delivery, video hosting, DTR, and A/B testing are **Scale+**; page importer + custom HTML injection + client sub-accounts are **Maximize**.

## Integrations

Data-flow direction: Convertri mostly **writes out** (form submissions, sales, rebills, refunds) to downstream tools via native connectors, custom webhooks, or Zapier. It does not expose a public read API.

- **Email/Autoresponders (native):** AWeber, Mailchimp, ActiveCampaign, ConvertKit, Drip, GetResponse, MailerLite, SendLane, SendGrid, iContact, Sendiio, Blastable, MarketHero
- **Payments (native):** Stripe, Shopify
- **Webinar (native):** Demio, GoToWebinar, WebinarJam, Zoom Webinar, Webinar JEO
- **CRM/automation (native):** Infusionsoft (Keap)
- **Analytics/tags:** Google Analytics, Google Search Console, Google Tag Manager, Data Layer, Facebook (pixel)
- **Membership/delivery (via webhook):** ProductDyno, Everlesson, Membership.io
- **Other:** WordPress, YouZign, Quizitri (quiz funnels)
- **iPaaS:** Zapier (8 triggers — see API reference) and custom webhooks (5 types)

## Data model

There is no public object/REST schema. The observable data model is the **webhook payload** Convertri POSTs on commerce/lead events. Key objects appear as flat fields:

**Sale webhook (representative shape):**
<!-- Constructed from documented field list — verify against live API -->
```json
{
  "ctransaction": "SALE",
  "corderid": "123456",
  "ctransreceipt": "789012",
  "cprodtitle": "Funnel Masterclass",
  "cproditem": "PROD_ABC",
  "cprodtype": "recurring",
  "cquantity": "1",
  "ccurrency": "USD",
  "ctransamount": "1000",
  "ctaxamount": "0",
  "cshippingamount": "0",
  "ctranspaymentmethod": "Stripe",
  "ctranstime": "1719446400",
  "cordermode": "live",
  "ccustname": "Jane Doe",
  "ccustfirstName": "Jane",
  "ccustlastName": "Doe",
  "ccustemail": "jane@example.com",
  "ccustphone": "+15551234567",
  "ccustaddress": "1 Main St",
  "ccustcity": "Austin",
  "ccuststate": "TX",
  "ccustzipCode": "78701",
  "ccustcc": "US",
  "ip": "203.0.113.10",
  "fbp": "fb.1.123",
  "fbclid": "abc123",
  "gclid": "xyz789",
  "utm_source": "facebook",
  "utm_medium": "cpc",
  "utm_campaign": "launch",
  "utm_content": "ad1",
  "utm_term": "funnel",
  "cverify": "A1B2C3D4"
}
```

- **Amounts are integers in pennies/smallest unit** (`ctransamount` `1000` = $10.00). Same for `ctaxamount`, `cshippingamount`.
- **`ctransaction`** values: `SALE`, `BILL` (rebill), `CANCEL-REBILL`, `RFND` (refund).
- **`ctranspaymentmethod`**: Stripe or PayPal.
- **`cverify`** = first 8 uppercase chars of `SHA1( sorted-values-pipe-joined | secret )` — see verification recipe below.
- Every field is present on every message but some may be empty.

## Quick-start recipes

### Recipe 1 — Verify + ingest a Sale webhook (Python)

Trigger: a customer buys a product with a webhook URL configured. Steps: receive POST → verify `cverify` → normalize amount → upsert to CRM.

```python
import hashlib

SECRET = "your_account_webhook_secret"  # Account settings → webhook secret

def verify_convertri(payload: dict) -> bool:
    sig = payload.pop("cverify", "")
    # sort remaining keys alphabetically, pipe-join their values, append the secret
    ordered = [str(payload[k]) for k in sorted(payload.keys())]
    base = "|".join(ordered) + "|" + SECRET
    digest = hashlib.sha1(base.encode("utf-8")).hexdigest()
    return digest[:8].upper() == sig.upper()

# Flask example
from flask import Flask, request, abort
app = Flask(__name__)

@app.post("/convertri-webhook")
def hook():
    data = request.form.to_dict() or request.get_json(force=True)
    if not verify_convertri(dict(data)):
        abort(401)
    amount = int(data.get("ctransamount", "0")) / 100.0
    crm_upsert(email=data["ccustemail"], name=data["ccustname"],
               product=data["cprodtitle"], amount=amount,
               kind=data["ctransaction"])
    return "", 200
```

Gotcha: pop `cverify` BEFORE sorting; values are pipe-joined in **key-alphabetical** order; the secret is appended last after a final `|`.

### Recipe 2 — Configure a product/form webhook (no-code)

Trigger: you want every sale (or lead) sent to your endpoint. Steps:
1. Account settings → set the **webhook secret key**.
2. For a **product**: open the product's **Advanced** settings → add your webhook URL (unlimited URLs per product).
3. For a **form/lead capture**: open Configure Form → **Zapier and Webhooks** → add the URL (up to **5 per form**). Lead-capture webhooks only fire when a URL is set on the page.
4. Your endpoint receives a POST with the payload above (query strings / hidden fields and custom fields are included).

### Recipe 3 — Zapier "New Product Sale" → Google Sheet / CRM (cURL of the enable step)

Trigger: enable Zapier, then build the Zap. The API key lives in **Account → Integrations → Zapier → Setup** (toggle Enable Integration on, copy the key). In Zapier, add Convertri as an app and paste the key. There is no public cURL endpoint to create Zaps; the key only authenticates the Convertri app inside Zapier. Available triggers (pick one):

```
New Submission                  New Submission from Page
New Product Sale                New Product Sale from Page
Product Subscription Cancelled  Product Refund
New Sale of Any Product         New Sale of Any Product From Page
```

Gotcha: a funnel with too many pages makes Zapier time out when listing pages — keep ≤20 pages per funnel.

## Integration patterns

- **CRM/ESP sync architecture**: Convertri is the source-of-truth for the sale/lead event; your endpoint (or Zapier) is the integrator. Map `ccustemail` (dedupe key) → CRM contact; `cprodtitle`/`corderid`/`ctransamount` → deal/order; UTM/`fbclid`/`gclid` → attribution fields. There is no API to read back, so persist everything you need at write time.
- **Webhook listener pattern**: Always verify `cverify` (reject on mismatch). Webhooks have no documented retry/delivery log, so make your handler **idempotent** on `corderid` + `ctransaction` and reconcile missed events manually (no API to poll). Return 200 fast; do downstream work async.
- **Membership grant pattern**: For a paid members area or a 3rd-party tool (ProductDyno/Everlesson/Membership.io), attach the delivery tool's webhook URL to the product so a `SALE` provisions access and a `RFND`/`CANCEL-REBILL` revokes it.
- **Batch/backfill**: No API + no delivery log means you cannot backfill historically via Convertri. Export order data from the UI and import it manually if you need history.
