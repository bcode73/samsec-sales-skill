<!-- Source: https://apitracker.io/a/builderall-mailingboss -->
<!-- Source: https://ajuda.builderall.com/books/integracoes (MailingBoss 5.0 - Integração API) -->
<!-- Source: https://www.scribd.com/document/547473786/2020-Mailing-Boss-Integration-US-1 -->
<!-- Source: search-captured endpoint paths (member.mailingboss.com integration API) -->

# Builderall (MailingBoss) API Reference

> **Accuracy note (research baseline 2026-06-22).** Builderall's live site, pricing page, and help-center API pages either exceeded the fetch size limit or returned 404 during research. The endpoint paths and field names below were captured verbatim from the MailingBoss Integration API documentation as surfaced through API-tracker and integration listings. **Confirm exact list/campaign endpoint paths and custom-field tags against the API page inside your own MailingBoss account before building.** Nothing here is invented — gaps are flagged explicitly.

## What has an API

Builderall is an all-in-one suite, but the **only first-party programmatic surface is MailingBoss** (the email/autoresponder module). Funnels, SuperCheckout, courses/membership, CRM, chatbot, and webinars are **UI-built**; you integrate them by:

- Pulling/pushing contacts through the **MailingBoss API** (below),
- **Inbound webhooks** — MailingBoss gives each list a webhook URL so an external form/app can add a lead to that list,
- **iPaaS** — Zapier, Make, Pabbly Connect, Integrately (the common pattern is *MailingBoss as an action* — "Create MailingBoss contact" — triggered by an external event).

There is **no public MCP server** and **no broad REST API** spanning funnels/checkout/courses.

## Lineage (developer context)

MailingBoss is built on a **MailWizz**-style codebase. If a field tag or behavior isn't documented in the Builderall help center, the MailWizz subscriber/list API conventions (uppercase field tags like `EMAIL`, `FNAME`, `LNAME`; list-scoped subscriber resources; `subscriber_uid`/`list_uid` identifiers) are a reliable reference for the shape — but verify against your account.

## Base URL

```
https://member.mailingboss.com/integration/index.php/
```

## Authentication

API-key (token) based. **The token is part of the URL path**, appended as the last path segment (`<TOKEN>`). Other parameters go in the **request body**, not the URL.

- Get the token from inside **MailingBoss → account/profile menu → API / Integrations** (exact label best-effort — confirm in-app).
- Treat the token as a secret; rotate it if it leaks (anyone with the URL can write to your lists).

```bash
# Pattern: ...<endpoint>/<TOKEN>
https://member.mailingboss.com/integration/index.php/lists/subscribers/create/<TOKEN>
```

## Subscriber endpoints (verified verbatim)

All are `POST` with a form-encoded (or JSON) body. `list_uid` identifies the target list; `subscriber_uid` identifies a contact within a list.

### Create subscriber

```
POST lists/subscribers/create/<TOKEN>
```
Body fields:
- `email` — subscriber email (required)
- `list_uid` — target list UID (required)
- `taginternals` — tag(s) to apply (optional)
- custom fields — pass MailingBoss field tags (e.g. `FNAME`, `LNAME`) as additional body params

```bash
curl -X POST \
  "https://member.mailingboss.com/integration/index.php/lists/subscribers/create/<TOKEN>" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "list_uid=<LIST_UID>" \
  --data-urlencode "email=jane@example.com" \
  --data-urlencode "FNAME=Jane" \
  --data-urlencode "taginternals=app-trial"
```

Documented response fields (shape): `subscriber_uid`, `email`, `taginternals`, `status`.
```json
{
  "subscriber_uid": "ab12cd34ef",
  "email": "jane@example.com",
  "taginternals": "app-trial",
  "status": "confirmed"
}
```
> Field set above is what the docs show on create; the exact JSON envelope (e.g. a wrapping `status`/`data` object) should be confirmed against your account's response.

### Search subscriber by email

```
POST lists/subscribers/search-by-email/<TOKEN>
```
Body fields: `email`, `list_uid`.

Use this to resolve a `subscriber_uid` before an update/unsubscribe, and to implement upsert-by-email (search → create if absent, else update).

### Update subscriber

```
POST lists/subscribers/update/<TOKEN>
```
Body fields: `subscriber_uid`, `list_uid`, `email`, `taginternals` (+ custom field tags).

### Unsubscribe subscriber

```
POST lists/subscribers/unsubscribe/<TOKEN>
```
Body fields: `subscriber_uid`, `list_uid`.

## List & campaign endpoints (documented to exist — paths to confirm)

The MailingBoss Integration API documentation references list-level operations (e.g. retrieving lists, creating a list) and campaign operations under the same base URL and token-in-path pattern. **Exact paths and response shapes were not captured verbatim during research** — open the API page in your MailingBoss account to confirm the `lists/...` and `campaigns/...` routes before relying on them. Do not assume MailWizz's `/lists` paths map 1:1.

## Webhooks (inbound)

- Each MailingBoss **list exposes a webhook URL**. POST a lead payload to it (or point an external form's webhook at it) to add subscribers to that list without calling the create endpoint directly.
- This is the standard "landing page form → add to list" pattern Builderall promotes, and what Zapier/Make/Pabbly/Integrately use under the hood.
- MailingBoss is predominantly an **action target** in iPaaS (it receives data); native *outbound* event triggers (e.g. "subscriber opened") are limited — confirm available triggers in your iPaaS connector.

## Rate limits

Not documented in the captured material. Assume an undocumented soft limit: batch writes, add backoff/retry on non-2xx, and avoid tight loops. Confirm any published limit in-app before high-volume syncs.

## Pagination

Not documented in the captured material for list/subscriber reads. If you build a full-list export, expect a paginated read pattern (MailWizz-style page/per-page params are likely but **unconfirmed**) — verify in your account.

## Integration recipes

See `platform-guide.md` for working create-contact-and-tag, upsert-by-email, and form-webhook-to-list recipes (cURL + Python).
