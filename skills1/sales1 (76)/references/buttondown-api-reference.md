<!-- Source: https://docs.buttondown.com/api-introduction, https://docs.buttondown.com/api-authentication, https://docs.buttondown.com/api-rate-limits, https://docs.buttondown.com/api-versioning, https://docs.buttondown.com/api-subscribers-create, https://docs.buttondown.com/events-and-webhooks-introduction, https://docs.buttondown.com/api-webhooks-event-types, https://buttondown.com/features/api -->
<!-- Re-verified against live official docs 2026-06-13. Some docs.buttondown.com pages are JS-rendered; webhook/event details corroborated via official blog (buttondown.com/blog/webhook-examples, /changelog/2024-10-29) and search snippets. Refresh by visiting docs.buttondown.com directly. -->

# Buttondown API Reference

## Overview

Buttondown's API has been designed to be as RESTful and uninteresting as possible: if there's a primitive in Buttondown, you should have a nice interface for it, with the ability to retrieve, create, modify, and delete.

Every feature in Buttondown is built API-first — Buttondown uses the same API to power its own app. No second-class endpoints, no missing functionality, and no surprises. If you can click it, you can script it.

The API is available on **all pricing plans**, including free.

## Base URL

```
https://api.buttondown.com/v1/
```

## Authentication

Clients should authenticate by passing the token key in the `Authorization` HTTP header, prepended with the string `Token ` (note the trailing space!).

```
Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
```

Manage your API keys at: **https://buttondown.com/keys** (Settings → API → Keys).

### Granular / multiple API keys (since 2026-01-24)

Buttondown now supports **multiple API keys per account**, each with an independent label and per-category permissions, instead of one all-powerful key. Create as many keys as you need at API → Keys; if one integration is compromised you can regenerate or delete that specific key without breaking the others.

### Multi-newsletter context

For accounts with multiple newsletters, include the `Buttondown-Context` header:

```
Buttondown-Context: my-newsletter-name
```

### Permission levels

Each API key supports eight distinct permission categories:
- subscriber
- email
- sending
- administrivia
- automations
- forms
- styling
- surveys

Each configurable to: **write** (full access), **read** (view-only), or **none** (blocked).

Attempting an operation without permission returns `403 Forbidden`.

## API versioning

The API is date-versioned. Pass the `X-API-Version` header to pin a request to a specific version; otherwise the newsletter's pinned version (configurable in settings) is used, falling back to the latest version.

- **Current/latest version**: `2026-04-01`
- **Header**: `X-API-Version: 2026-04-01`
- Backwards-incompatible changes (renaming/removing fields, removing/renaming endpoints) trigger a new dated version. Note: an older API version may still use legacy field names — see the field-rename note under Subscribers below.

## Rate limiting

- **All endpoints**: 600 requests per minute. Exceeding this returns `429 Too Many Requests` with a `Retry-After` header (seconds) — use it for backoff.
- **Subscriber creation** (`POST /v1/subscribers`): additionally capped at **100 requests per day**. Exceeding this returns `400` (not 429) directing you to the bulk import path. For initial list loads, import via CSV / the bulk import endpoint instead of one-by-one creates.
- Limits grow over time as the newsletter accumulates reputation; contact Buttondown for higher limits on a specific use case.

## Key endpoints

### Subscribers

- `GET /v1/subscribers` — List all subscribers
- `POST /v1/subscribers` — Create a subscriber
- `GET /v1/subscribers/{id}` — Get a subscriber
- `PATCH /v1/subscribers/{id}` — Update a subscriber
- `DELETE /v1/subscribers/{id}` — Delete a subscriber

### Emails

- `GET /v1/emails` — List all emails
- `POST /v1/emails` — Create an email (draft or send)
- `GET /v1/emails/{id}` — Get an email
- `PATCH /v1/emails/{id}` — Update an email
- `DELETE /v1/emails/{id}` — Delete an email

### Tags

- `GET /v1/tags` — List all tags
- `POST /v1/tags` — Create a tag
- `GET /v1/tags/{id}` — Get a tag
- `PATCH /v1/tags/{id}` — Update a tag
- `DELETE /v1/tags/{id}` — Delete a tag

### Automations

- `GET /v1/automations` — List automations
- `POST /v1/automations` — Create an automation
- `GET /v1/automations/{id}` — Get an automation

### Newsletters

- `GET /v1/newsletters` — List newsletters
- `POST /v1/newsletters` — Create a newsletter

### Data exports

- `POST /v1/exports` — Request a data export
- `GET /v1/exports/{id}` — Get export status

### Webhooks

- `GET /v1/webhooks` — List webhooks
- `POST /v1/webhooks` — Create a webhook
- `GET /v1/webhooks/{id}` — Get a webhook
- `PATCH /v1/webhooks/{id}` — Update a webhook
- `DELETE /v1/webhooks/{id}` — Delete a webhook

A webhook subscribes to one or more event types (multi-event subscription supported since 2024-10-29). See the **Events & webhooks** section below for event types, payload shape, and signature verification.

## Subscriber fields (field-name note)

On the current API version the create-subscriber body uses **`email_address`** (the primary email field) and **`type`** — NOT `email` / `subscriber_type`. Older docs/SDKs may show `email`; that maps to a legacy API version. Documented create fields include:

- `email_address` — the subscriber's email (required)
- `type` — e.g. `"regular"` to bypass double opt-in (otherwise subject to double opt-in)
- `tags` — array of tag strings
- `ip_address` — requester IP, used to determine location and validate legitimacy / spam-check
- `metadata` — arbitrary key-value object (also readable in templates as `{{ subscriber.metadata.* }}`)

## Code examples

### Python — Create a subscriber

```python
import requests

response = requests.post(
    "https://api.buttondown.com/v1/subscribers",
    headers={"Authorization": "Token YOUR_API_KEY"},
    json={
        "email_address": "reader@example.com",
        "type": "regular",            # bypass double opt-in
        "tags": ["welcome-series"],
        "ip_address": "203.0.113.7",  # for spam validation
        "metadata": {"source": "website"}
    }
)
print(response.json())
```

### JavaScript — Send an email

```javascript
const response = await fetch("https://api.buttondown.com/v1/emails", {
    method: "POST",
    headers: {
        "Authorization": "Token YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        subject: "Weekly Update",
        body: "# Hello\n\nThis is a **Markdown** email.",
        status: "draft"  // or "about_to_send" to send immediately
    })
});
```

### cURL — List subscribers

```bash
curl -s https://api.buttondown.com/v1/subscribers \
  -H "Authorization: Token YOUR_API_KEY" | jq .
```

## Events & webhooks

Buttondown emits **events** when something happens to your newsletter; **webhooks** POST those events to a URL you control. A single webhook can subscribe to multiple event types.

### Event types (corroborated from official docs/blog)

Subscriber events: `subscriber.created`, `subscriber.confirmed`, `subscriber.unsubscribed`, `subscriber.opened`, `subscriber.clicked`, `subscriber.deleted`.
Email events: `email.created`, `email.sent`.
Comment events: `comment.created`.

> The full enumerated list lives at https://docs.buttondown.com/api-webhooks-event-types (an `ExternalEventType` enum). The page is JS-rendered; the identifiers above are confirmed from official docs and blog examples, but treat the list as non-exhaustive.

### Payload shape

Webhook bodies are JSON with top-level fields:

```json
{
  "event_type": "subscriber.created",
  "data": { "subscriber": { "id": "...", "email_address": "..." } }
}
```

`data` is a nested object (e.g. `data.subscriber`). Some no-code tools (e.g. Slack's builder) can't parse the nested structure.

### Signature verification (HMAC-SHA256)

When a webhook has a signing key configured, Buttondown sends an
`X-Buttondown-Signature: sha256=<hmac>` header on every request, computed as HMAC-SHA256 of the **raw request body** using your key.

- Verify against the **raw body**, not re-serialized JSON.
- Do **not** IP-allowlist Buttondown — it does not deliver from a stable set of IPs.

```python
import hmac, hashlib

def verify(raw_body: bytes, header: str, signing_key: str) -> bool:
    expected = hmac.new(signing_key.encode(), raw_body, hashlib.sha256).hexdigest()
    sent = header.removeprefix("sha256=")
    return hmac.compare_digest(expected, sent)
```

## Changelog

API changes are documented at: https://docs.buttondown.com/api-changelog
