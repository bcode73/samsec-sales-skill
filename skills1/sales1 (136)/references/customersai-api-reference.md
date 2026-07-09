<!-- Source: https://customers.ai/help/l/en/category/doq3ewxla3-public-api -->
<!-- Source: https://customers.ai/api (public chatbot/contact API overview) -->
<!-- Note: API docs are JS-rendered and sparse. This reference captures what was available via WebFetch. -->
<!-- Re-verified 2026-06-13: core api.mobilemonkey.com endpoints (Update Contact PUT, Send JSON Message, Lookup Users) UNCHANGED. -->
<!-- The /api overview page gates the public contact/chatbot API to legacy "PRO, PRO Unicorn and Team" MobileMonkey plans (naming predates current Customers.ai plans). -->
<!-- Note: api.mobilemonkey.com Swagger UI remains JS-rendered and was not machine-readable at re-verification. -->

# Customers.ai Public API Reference

## Overview

Customers.ai uses a legacy MobileMonkey API at `api.mobilemonkey.com`. The API is limited — most operations happen through the dashboard and native Klaviyo/Shopify integrations.

**Swagger docs**: https://api.mobilemonkey.com/swagger/dist/index.html?url=/apidocs

## Authentication

Not documented in public help articles. Likely API key-based — request access via the Customers.ai dashboard or support.

## Endpoints

### Update Contact Attributes

**URL**: `https://api.mobilemonkey.com/public/contacts/{contact_id}/`

**Parameters**:
- `contact_id` (path, required): MobileMonkey numeric ID. Obtain from the Lookup Users endpoint.

**Request body** (JSON):
```json
{
  "city": "Boston",
  "PHONE": "+123456789"
}
```

**Constraints**:
- Maximum 10 attributes per request
- Attributes must already exist for the contact — this endpoint updates existing values, it does not create new attributes

### Send JSON Message

**URL**: `https://api.mobilemonkey.com/public/contacts/{contact_id}/send_json_message`

**Parameters**:
- `contact_id` (path, required): MobileMonkey numeric ID.
- `json_message` (body, required): Message payload.

**Text message**:
```json
{
  "json_message": {
    "text": "hello, world!"
  }
}
```

**Quick question with options**:
```json
{
  "json_message": {
    "text": "Would you like to know more?",
    "quick_replies": [
      {
        "content_type": "text",
        "title": "Yes",
        "payload": "Yes|GOTO_PAGE_ID:146057|BID:43414"
      }
    ]
  }
}
```

**Image message**:
```json
{
  "json_message": {
    "attachment": {
      "type": "image",
      "payload": {
        "url": "https://example.com/image.jpg",
        "is_reusable": true
      }
    }
  }
}
```

**Also supports**: Video attachments and gallery/carousel layouts (same attachment structure).

### Lookup Users

Referenced in other endpoint docs but full documentation not captured. Used to obtain `contact_id` values for the Update Contact and Send JSON Message endpoints.

### Get Contacts

The `/api` overview page also surfaces a **GET Contacts** operation ("Retrieve and Update Contact Data from Your Chat Contacts via API") on the same contact resource. Full request/response schema is not published in the help center.

### Send Dialogue

A **POST Dialogues** operation is referenced for sending a "custom chatbot dialogue" built in the Customers.ai advanced chatbot builder. Full schema not published.

### Plan gating (legacy)

Per the `/api` overview, the public contact/chatbot API is available on "PRO, PRO Unicorn and Team Plans." These are legacy MobileMonkey plan names and do not map to current Customers.ai plans (which are now priced by total Klaviyo profile count + product selection). Confirm API access with Customers.ai support for your specific plan.

## Consumer Data Enrichment API

Separate product from the public API above. Accessed via https://customers.ai/api.

- **Purpose**: Enrich contacts with business and employment information, updated monthly.
- **Query by**: Name, email, or phone to retrieve a match with additional fields.
- **Security**: Visitor data encrypted before transmission.
- **Access**: Request API key through the Customers.ai website.

Full endpoint documentation for the enrichment API was not publicly available at time of research (JS-rendered page).

## Webhooks / Integration

Customers.ai supports JSON Webhooks and integration via Shopify's Custom API. Details available in the help center under integration articles.

## Limitations

- Legacy API with MobileMonkey branding (predates Customers.ai rebrand)
- Authentication method not publicly documented
- Very limited public endpoints (2 documented + lookup)
- No documented rate limits (though likely exist)
- Consumer Data Enrichment API docs are gated/JS-rendered
- Most functionality accessed through dashboard UI and native integrations, not API
