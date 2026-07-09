<!-- Source: https://help.convertri.com/article/264-custom-webhooks-reference -->
<!-- Source: https://help.convertri.com/article/306-how-to-integrate-zapier -->
<!-- Source: https://help.convertri.com/article/392-how-to-use-webhooks -->
<!-- Source: https://help.convertri.com/category/377-webhooks -->
<!-- Source: https://zapier.com/apps/convertri/integrations -->

# Convertri Developer / Automation Reference

> **No public REST API.** Convertri does **not** publish a REST API for creating or reading pages, funnels, products, or orders. The only programmatic surfaces are: (1) a **Zapier API key** that authenticates the Convertri app inside Zapier, and (2) **custom webhooks** that POST JSON on commerce and lead events. Everything below documents those two surfaces.

---

## 1. Authentication (Zapier API key)

There is one account-level API key, used only to connect Convertri to Zapier.

**Finding/enabling the key (verbatim from docs):**
> Navigate to the Dashboard, select Account, then click Integrations. Locate Zapier and select Setup. "Toggle Enable Integration to On. Click to copy the API key to your clipboard."
>
> Access Zapier.com and log in. In your dashboard, go to My Apps and search for Convertri in the connection dropdown. "Paste in the Convertri API key, and click Continue."

The key is **not** used against a public HTTP endpoint you can call directly — it only authorizes the Convertri Zapier app. There is no documented base URL, bearer-token REST surface, or cURL endpoint for CRUD on Convertri objects.

---

## 2. Zapier triggers

Available triggers (verbatim list from the integration docs):

1. **New Submission Trigger** — "triggers when a form or checkout is submitted from anywhere in your Convertri account"
2. **New Submission from Page** — activates for submissions from a specific page
3. **New Product Sale** — "triggers when the product selected has been sold from any sales page"
4. **New Product Sale from Page** — activates when a specific product sells from a designated page
5. **Product Subscription Cancelled** — "triggers when someone cancels a subscription of a product"
6. **Product Refund** — "triggers when someone refunds the sale of a product"
7. **New Sale of Any Product** — "triggers whenever a sale is made within your Convertri account"
8. **New Sale of Any Product From Page** — activates for sales from a selected page

**Important limitation (verbatim):**
> "Having too many pages in a funnel means that Zapier will time out and not be able to load them all" — maintain 20 pages or fewer per funnel.

---

## 3. Custom webhooks

**What webhooks do (verbatim):**
> "Webhooks simply POST data (or JSON) to a specific URL every time we see something new."
>
> "Webhooks open up extra possibilities for your customers. You can assign a webhook to your product, and you can automatically add buyers to third party services (e.g. membership sites like ProductDyno or Everlesson) when they purchase from your Convertri page."

**Configuration:**
- A **secret key** must be configured in **Account settings** (used for the `cverify` signature).
- Webhook URLs are added in the **product's Advanced settings** or in **form configurations** (Configure Form → Zapier and Webhooks).
- Limits: **up to 5 webhook URLs per form**; **unlimited per product**.
- The webhook also sends **query strings (hidden fields)** and **custom fields** if they have been set up and attached to inputs in the page editor.
- Lead-capture webhooks **are not fired unless you configure the webhook URL on the page**.

### 3.1 Webhook types (verbatim)

- **Sale** — sent after a regular or a recurring product has been purchased
- **Rebill** — sent after a recurring product's next payment date has passed, and is fired even if no charge happens
- **Rebill Cancellation** — sent after recurring payments on an order have been cancelled, and is fired only if the order has any recurrent payments left
- **Refund** — sent after a payment has been refunded, but not fired for products that haven't been paid for
- **Lead Capture** — sent after form submission, but webhooks aren't fired unless you configure the webhook URL on the page

`ctransaction` (transaction type) values seen across these: `SALE`, `BILL` (rebills), `CANCEL-REBILL`, `RFND` (refund). Payment methods are limited to **Stripe** or **PayPal**.

### 3.2 Payload fields (verbatim field keys + descriptions)

All of the following fields are present in every webhook message, but some may be empty.

| Field | Description |
|---|---|
| `ccurrency` | Currency of charge |
| `ccustcc` | Customer country |
| `ccustemail` | Customer email |
| `ccustname` | Customer name |
| `ccuststate` | Customer state |
| `cproditem` | Convertri product ID |
| `ccusttitle` | Customer title |
| `ccustfirstName` | Customer first name |
| `ccustlastName` | Customer last name |
| `ccustmiddleNames` | Customer middle names |
| `ccustphone` | Customer phone |
| `ccustaddress` | Customer address |
| `ccustaddress2` | Customer address2 |
| `ccustcity` | Customer city |
| `ccustzipCode` | Customer zipCode |
| `ccustshippingAddress` | Customer shipping address |
| `ccustshippingAddress2` | Customer shipping address2 |
| `cshippingamount` | Amount charged for shipping a product in pennies |
| `ccustshippingCity` | Customer shipping city |
| `ccustshippingState` | Customer shipping state |
| `ccustshippingCountry` | Customer shipping country |
| `ccustshippingZipCode` | Customer shipping zip code |
| `ccustwebsite` | Customer website |
| `ccustnotes` | Customer notes |
| `cprodtitle` | Product name |
| `corderid` | Order ID in Convertri |
| `cordermode` | Checkout mode used for making order |
| `cquantity` | number |
| `cprodtype` | Product type (recurring or not) |
| `ctaxamount` | Amount charged for tax for a product purchase in pennies |
| `ctransaction` | Transaction type |
| `ctransamount` | Amount charged for a product in pennies ($10.00 = 1000) |
| `ctranspaymentmethod` | Payment method selected by the customer |
| `ctransreceipt` | Convertri order product ID |
| `ctranstime` | Unix timestamp transaction occured at (in seconds) |
| `cverify` | Transaction verification signature |
| `ip` | IP address of a customer at the moment of checkout |
| `fbp` | Facebook pixel ID |
| `fbclid` | Facebook click ID |
| `gclid` | Google click ID |
| `utm_campaign` | UTM campaign value |
| `utm_source` | UTM source value |
| `utm_medium` | UTM medium value |
| `utm_content` | UTM content value |
| `utm_term` | UTM term value |
| `cprodvar1` | Variant category |
| `cprodvar2` | Variant category |
| `cprodvar3` | Variant category |

**Tracking data (verbatim):** "UTM tag data, FB Click ID and Google Click ID are sent with the webhook payload."

### 3.3 Example payload (constructed)

<!-- Constructed from the documented field list — verify against live API -->
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

### 3.4 `cverify` signature verification (verbatim algorithm)

The `cverify` field is generated from a combination of your webhook secret key, the webhook payload, and a cryptographic function, allowing you to check that the webhook genuinely came from Convertri and that none of the information in the payload has been tampered with.

To verify webhooks:
> "(1) Remove the 'cverify' key and its value from the request payload. (2) Alphabetically sort the remaining payload by key name. (3) Combine the values of the remaining payload into one long string with a pipe '|' character between each value. (4) At the end of the long string, append another pipe '|' followed by your secret key. (5) Ensure that the string is UTF-8 encoded. (6) Hash the string using SHA-1. (7) Change the first 8 characters of the resulting hash to uppercase."
>
> "Those first 8 uppercase characters should now match the 'cverify' that was included in the webhook payload."

**Python implementation:**
```python
import hashlib

def cverify_ok(payload: dict, secret: str) -> bool:
    sig = payload.pop("cverify", "")
    values = [str(payload[k]) for k in sorted(payload.keys())]
    base = "|".join(values) + "|" + secret
    digest = hashlib.sha1(base.encode("utf-8")).hexdigest()
    return digest[:8].upper() == sig.upper()
```

---

## 4. Pagination, rate limits, error handling

- **Pagination**: N/A — there is no public list/read API. Webhooks are push-only; Zapier triggers poll Convertri internally.
- **Rate limits**: none documented for webhooks. The only documented throughput constraint is the Zapier page-listing timeout (keep ≤20 pages per funnel).
- **Error handling / delivery**: there is **no documented webhook retry policy, delivery log, or signed-timestamp** beyond `cverify`. Make handlers idempotent on `corderid` + `ctransaction`; you cannot reconcile missed events via an API (export from the UI instead). Return HTTP 200 quickly and process downstream work asynchronously.

## 5. Gaps

- No documented base URL, REST endpoints, or OAuth flow — confirmed absent as of 2026-06.
- No documented webhook retry/backoff, delivery dashboard, or HMAC header (verification is the in-payload `cverify` only).
- Exact Zapier action (write) inventory is not fully published; triggers are documented above.
- Example payloads in §3.3 / §3.2 default values are constructed from the documented field list — verify field presence and casing against a live test webhook before relying on them.
