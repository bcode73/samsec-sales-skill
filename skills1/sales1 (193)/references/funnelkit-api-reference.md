<!-- Source: https://developers.funnelkit.com/ and https://funnelkit.com/docs/autonami-2/webhooks/ (fetched 2026-06) -->
<!-- FunnelKit is a self-hosted WordPress/WooCommerce plugin suite (Funnel Builder + Automations, formerly Autonami). The REST API documented here is FunnelKit AUTOMATIONS (the CRM/email/SMS side). The Funnel Builder side (checkout, order bumps, one-click upsells) is built on WooCommerce orders — read those via the WooCommerce REST API / order webhooks. Endpoints/auth below are reproduced verbatim from the official developer docs. -->

# FunnelKit (Automations) API Reference

## Scope

FunnelKit has two sides:
- **FunnelKit Automations** (CRM / email / SMS / contacts) — has the **REST API** + **webhooks** below.
- **FunnelKit Funnel Builder** (checkout pages, order bumps, one-click upsells/downsells, A/B testing) — built on **WooCommerce**; read revenue/orders via the **WooCommerce REST API / order webhooks** (FunnelKit has no separate funnel-read REST API).

It's a self-hosted WordPress plugin — there is **no hosted SaaS API or MCP**; the API lives on your own site.

## Base URL

```
https://{your-site}/wp-json/funnelkit-automations/
```

(Docs show `http://example.com/wp-json/funnelkit-automations/` — substitute your WordPress site, use HTTPS.)

## Authentication

Generate an **API key** in the FunnelKit Automations admin app: **Settings → REST API**. Pass it as a **query parameter** on every request:

```
?api_key={your_api_key}
```

cURL (list contacts):

```bash
curl "https://yoursite.com/wp-json/funnelkit-automations/contacts?api_key=$FK_API_KEY"
```

> The key is a query param, not a header — keep URLs out of logs/referrers, and prefer server-side calls.

## Response format

```json
{ "code": "success", "data": {  }, "limit": 0, "offset": 0 }
```

`limit`/`offset` indicate offset-based pagination on list endpoints.

## Error codes

`400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found · `405` Method Not Allowed · `406` Wrong Format · `422` Unprocessable Entity · `500` Internal Server Error.

---

## Endpoints

### Tags
- **GET** `/tags` — retrieve all tags
- **POST** `/tag/add` — create tags — body: `{"tags": ["name1", "name2"]}`
- **POST** `/tag/update/{tag_id}` — update — body: `{"tag": "new_name"}`
- **DELETE** `/tag/{tag_id}` — delete

### Lists
- **GET** `/lists` — retrieve all lists
- **POST** `/list/add` — create — body: `{"lists": ["name1", "name2"]}`
- **POST** `/list/update/{list_id}` — update — body: `{"list": "new_name"}`
- **DELETE** `/list/{list_id}` — delete

### Fields (custom fields)
- **GET** `/fields` — retrieve all custom fields
- **POST** `/field/add` — create (body: field_name, type, placeholder, mode, search)
- **POST** `/field/update/{field_id}` — update
- **DELETE** `/field/{field_id}` — delete

### Contacts
- **GET** `/contacts` — retrieve all (filter: email, status, tags, lists, date ranges)
- **GET** `/contact` — get by id or email (query `id` or `email`)
- **POST** `/contact/add` — create a contact
- **POST** `/contact/update/{contact_id}` — update
- **POST** `/contact/update-email/{contact_id}` — change email — body: `{"email": "new@email.com"}`
- **POST** `/contact/change-status/{contact_id}` — body: `{"status": "subscribed|bounced|unsubscribed|verified"}`
- **POST** `/contact/tag-assign/{contact_id}` — body: `{"tags": [1,2]}`
- **POST** `/contact/tag-unassign/{contact_id}` — body: `{"tagId": [1]}`
- **POST** `/contact/list-assign/{contact_id}` — body: `{"lists": [1]}`
- **POST** `/contact/list-unassign/{contact_id}` — body: `{"listId": [1]}`
- **DELETE** `/contact/{contact_id}` — delete

> The contact is the core object: email-keyed, with tags, lists, custom fields, and a status. Tag/list assignment is how you segment and trigger automations.

**CONSTRUCTED example — create a contact** (assembled from the documented `/contact/add` + contact model; verify field names against your install):

```bash
curl -X POST "https://yoursite.com/wp-json/funnelkit-automations/contact/add?api_key=$FK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","first_name":"Jane","tags":[3],"lists":[1]}'
```

---

## Webhooks (FunnelKit Automations)

Two directions:

- **Incoming webhooks (receive data):** FunnelKit gives you a **Webhook URL** to plug into another app. External events POST to it; an automation can then **fetch the data and run actions** (add/segment contact, send email/SMS, etc.). Set up under Automations as a webhook-triggered automation.
- **Outgoing webhooks (send data):** inside an automation, use the **HTTP Request** action to POST selected data to an external endpoint when the automation runs.
- **Conditions:** webhook automations support condition rules to branch on the incoming data.

Exact incoming payload schema, signature/auth, and retry behavior aren't fully published on the overview page — confirm on the **Incoming Webhooks** / **Outgoing Webhooks** subpages and capture a live delivery before coding. Treat the incoming Webhook URL as a secret.

---

## Funnel Builder data (orders/revenue)

Order bumps and one-click upsells/downsells create/modify **WooCommerce orders**. To read funnel **revenue/AOV** programmatically, use the **WooCommerce REST API** (`/wp-json/wc/v3/orders`) or WooCommerce **order webhooks** — there is no separate FunnelKit funnel-read API.

## Other integration surfaces

- **Zapier / Make / Integrately / Pabbly** (100s of apps), **Slack**, **Twilio** (SMS), **WP Fusion**.
- **Payment gateways:** Stripe, PayPal, Mollie, Authorize.Net CIM, Braintree, SagePay (15+).
- **LMS:** LearnDash, LifterLMS, TutorLMS. **Affiliates:** AffiliateWP.
- **WordPress action/filter hooks** for server-side PHP customization.
