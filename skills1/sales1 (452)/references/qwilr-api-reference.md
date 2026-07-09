### Qwilr API Reference

**Base URL**: `https://api.qwilr.com/v1`
**Auth**: `Authorization: Bearer <access-token>` (security scheme: Bearer, format JWT). Generate the token at `https://app.qwilr.com/#/settings/api` — it is shown only once on creation.
**Docs**: https://docs.qwilr.com/ (API reference: https://docs.qwilr.com/api-reference/)
**Plan gate**: Per Qwilr's docs and API page, API access requires an Enterprise account with API access enabled, and extra fees apply (talk to Qwilr sales). Verified 2026-06-13.

#### Endpoints

| Endpoint | Method | What it does |
|---|---|---|
| `/pages` | POST | Create page from a `templateId` OR a `blocks` array, with top-level `substitutions`, quote sections (inside blocks), `metadata`, `tags`, `published` |
| `/pages/{id}` | GET | Get page details (expand: metadata, acceptance, previewAcceptance) |
| `/pages/{id}` | PUT | Update published status |
| `/blocks/saved` | GET | List saved blocks (id, name, type) |
| `/webhooks` | GET | List webhook subscriptions |
| `/webhooks` | POST | Create webhook subscription |
| `/webhooks/{subscriptionId}` | DELETE | Delete a webhook subscription (id returned when the subscription was created) |
| `/users` | GET | List account users (for ownerId) |

#### Webhook events

| Event | When it fires |
|---|---|
| `pageAccepted` | Prospect accepts the full proposal |
| `pagePartiallyAccepted` | Prospect selects some items but not all |
| `pagePreviewAccepted` | Internal preview was accepted |
| `pageViewed` | Prospect views the page (fires on each view) |
| `pageFirstViewed` | First time a prospect views the page |
| `pageSetLive` | Page is published/set live |
| `pageRevivedLive` | Previously unpublished page is re-published |

#### Creating a page

Two approaches: `templateId` (consistent structures) or `blocks` (saved blocks — required if you want to pass a Quote Block). In BOTH approaches, variable values go in a single top-level `substitutions` object (NOT per-block, NOT named `tokens`), and the draft flag is `published` (boolean), NOT `isPublished`.

**Template approach:**

```bash
curl -X POST https://api.qwilr.com/v1/pages/ \
  -H "Authorization: Bearer $QWILR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "templateId": "your-template-id",
    "name": "Proposal for Acme Corp",
    "published": false,
    "tags": ["auto-generated", "hubspot"],
    "substitutions": {
      "company_name": "Acme Corp",
      "contact_first_name": "Jane",
      "contact_title": "VP Engineering",
      "deal_amount": "$48,000"
    },
    "metadata": {}
  }'
```

**Saved-blocks approach with a Quote Block** (quote data overrides the entire quote contents of that block). Note the real quote field names: `quoteSections` and `quoteSettings` live INSIDE the block (keyed by `id`), line items are `lineItems` (not `items`), price is `unitPrice` with `quantity` (not `fixedCost.amount`), the buyer-selectable flag is `optional` (not `isOptional`), and recurrence is `billingSchedule` (not `billing.type`/`billing.frequency`):

```bash
curl -X POST https://api.qwilr.com/v1/pages/ \
  -H "Authorization: Bearer $QWILR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Proposal for Acme Corp",
    "published": false,
    "tags": ["auto-generated", "hubspot"],
    "substitutions": { "company_name": "Acme Corp" },
    "metadata": {},
    "blocks": [
      {
        "id": "your-saved-block-id",
        "foldable": { "enabled": false, "isFolded": false, "label": "" },
        "quoteSettings": { "selectionType": "multi" },
        "quoteSections": [
          {
            "description": "Annual License",
            "lineItems": [
              {
                "type": "fixedCost",
                "description": "Platform License — 25 seats",
                "unitPrice": 48000,
                "quantity": 1,
                "optional": false,
                "billingSchedule": "annual"
              },
              {
                "type": "fixedCost",
                "description": "Premium Support — dedicated CSM + priority SLA",
                "unitPrice": 12000,
                "quantity": 1,
                "optional": true,
                "billingSchedule": "annual"
              }
            ],
            "settings": { "selected": true, "showUnitPrice": true, "showQuantity": true, "showCost": true }
          }
        ]
      }
    ]
  }'
```

> Field names above (`unitPrice`, `quantity`, `quantityRange.min/max`, `optional`, `selected`, `billingSchedule`, `recommended`, `featuresList`, section `settings`, `quoteSettings.selectionType`) are taken from the live Quote data lifecycle guide. Exact value enums (e.g. allowed `billingSchedule` / `selectionType` values) should be confirmed against your account's saved quote block.

#### Discovering saved blocks

Before creating pages, list available blocks to find the block `id` values (used as `blocks[].id` in the create payload):

```bash
curl -X GET https://api.qwilr.com/v1/blocks/saved \
  -H "Authorization: Bearer $QWILR_TOKEN" \
  -H "Content-Type: application/json"
```

Response includes block `id`, `name`, and `type`.

#### Subscribing to webhooks

```bash
curl -X POST https://api.qwilr.com/v1/webhooks \
  -H "Authorization: Bearer $QWILR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/webhooks/qwilr",
    "events": ["pageFirstViewed", "pageViewed", "pageAccepted", "pagePartiallyAccepted"]
  }'
```

The create response returns a subscription id. To remove a subscription, DELETE the specific subscription by id (the path takes `{subscriptionId}`, not a bare `/webhooks`):

```bash
curl -X DELETE https://api.qwilr.com/v1/webhooks/SUBSCRIPTION_ID \
  -H "Authorization: Bearer $QWILR_TOKEN"
```

> The current docs do not document webhook HMAC/signature verification or a published rate limit. Treat handlers as idempotent and verify the source out-of-band until Qwilr documents signing.

#### Checking page status

```bash
curl -X GET "https://api.qwilr.com/v1/pages/PAGE_ID?expand=acceptance,metadata" \
  -H "Authorization: Bearer $QWILR_TOKEN"
```

#### Token / variable substitution

In the Qwilr API and docs, template/block variables are called **substitutions**. When creating a page, pass all values in a SINGLE top-level `substitutions` object (not per-block, not named `tokens`), keyed by the variable name:

```json
{ "substitutions": { "num_contacts": "3", "date": "Feb 4 2021" } }
```

Repeating variables take an array of objects:

```json
{ "substitutions": { "contact": [ { "name": "Allison Reynolds", "location": "Shermer, IL" } ] } }
```

**Variables are strings only** — there is no formatting applied, so dates and numbers must be passed as the exact final string you want rendered (e.g. `"$48,000"`, `"March 30, 2026"`). Omitted values default to empty strings. The variable mapping below uses the same logical names you would define in your template/block:

| Token | Typical CRM Source | Example |
|---|---|---|
| `{{company_name}}` | Company name | Acme Corp |
| `{{contact_first_name}}` | Contact first name | Jane |
| `{{contact_last_name}}` | Contact last name | Smith |
| `{{contact_title}}` | Contact title | VP Engineering |
| `{{contact_email}}` | Contact email | jane@acme.com |
| `{{rep_name}}` | Deal owner name | Alex Johnson |
| `{{rep_email}}` | Deal owner email | alex@company.com |
| `{{deal_amount}}` | Deal amount | $48,000 |
| `{{close_date}}` | Expected close date | March 30, 2026 |
| `{{industry}}` | Industry field | Financial Services |
| `{{product_name}}` | Product field | Enterprise Plan |
| `{{seat_count}}` | Custom field | 25 seats |

**Guidelines:**
- Always auto-populate: company_name, contact names, rep info, deal amount
- Semi-auto (verify after population): industry, company_size, product
- Always manual: executive summary, pain points, custom scope
- Set fallback values for optional tokens so pages don't show raw `{{token}}` text

#### Quote block structure

A Quote Block must use the saved-blocks approach. `quoteSections` and `quoteSettings` live INSIDE the block object (keyed by `id`). Passing quote data overrides the entire quote contents of that block.

Each section (`quoteSections[]`) supports: `description`, `lineItems[]`, and `settings`.

`lineItems[]` properties (from the live Quote data lifecycle guide):

| Property | Type | Description |
|---|---|---|
| `type` | string | e.g. `fixedCost`, `text` |
| `description` | string | Line item description |
| `unitPrice` | number | Per-unit price (NOT `fixedCost.amount`) |
| `unitLabel` | string | Label for the unit |
| `quantity` | number | Quantity |
| `quantityRange` | object | `{ "min": n, "max": n }` for buyer-adjustable quantity |
| `optional` | boolean | If true, buyer can select/deselect (NOT `isOptional`) |
| `selected` | boolean | Default selection state |
| `billingSchedule` | string | Recurrence/billing schedule (NOT `billing.type`/`billing.frequency`) |
| `recommended` | boolean | Flag a recommended item |
| `featuresList` | array | Feature bullets for the item |
| `metadata` | object | Item metadata |

Section `settings` include: `selected`, `selectionRequired`, `showUnitPrice`, `showQuantity`, `showCost`, `sectionDiscount` (`{ "type", "amount" }`), `groupItemsByBillingSchedule`, `showFeatures`, `metadata`.
Block-level `quoteSettings.selectionType` accepts values such as `multi`, `single`, `combined`.

> These are the field NAMES confirmed from current docs; confirm exact value enums against your own saved quote block.

#### Common automation recipes

**Auto-create proposal when deal hits Stage 3:**
- Trigger: CRM deal moves to "Proposal" stage
- Action: `POST /pages` with deal data mapped to tokens
- Then: Update CRM deal with Qwilr page URL

**Notify Slack when proposal is viewed:**
- Trigger: Qwilr webhook `pageFirstViewed`
- Action: Post to Slack channel with prospect name, page title, timestamp
- Then: Rep follows up within 24 hours

**Update CRM when proposal is accepted:**
- Trigger: Qwilr webhook `pageAccepted`
- Action: Update CRM deal stage to "Closed Won", record accepted amount
- Then: Trigger onboarding workflow

#### Testing checklist

- [ ] Auth: Verify API token works with `GET /blocks/saved`
- [ ] Block discovery: Confirm saved block IDs match your template
- [ ] Token mapping: Create a test page with all tokens populated — verify each substitution renders
- [ ] Quote block: Verify pricing, optional items, and billing types render correctly
- [ ] Webhook delivery: Send a test event and confirm your endpoint receives it
- [ ] CRM sync: If using native integration, create a test deal and verify auto-population
- [ ] Error handling: Test what happens when a required CRM field is empty
- [ ] Publish flow: Verify `published: false` creates a draft, then test publishing via `PUT /pages/{id}`
