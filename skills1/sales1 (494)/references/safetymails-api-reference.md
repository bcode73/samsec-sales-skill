# SafetyMails API Reference

> **Documentation status:** SafetyMails publishes a help-center docs site (docs.safetymails.com) plus an official developer SDK repo at [github.com/SafetyMails-Team/safetymails-sdk](https://github.com/SafetyMails-Team/safetymails-sdk) (code examples in JS, PHP, Python, Java, Go) and a Swagger spec for the batch API. As of the 2026-06-13 re-verification, SafetyMails DOES offer a custom HTTP REST API for real-time validation and a separate batch validation API — earlier "no REST API" framing was wrong. Some details (rate limits, webhooks, Email Finder programmatic access) remain undocumented and are flagged below.

## Overview

| Field | Value |
|-------|-------|
| Platform | SafetyMails — email verification (bulk + real-time API + Email Finder) |
| Documentation | [docs.safetymails.com](https://docs.safetymails.com) |
| Official SDK / examples | [github.com/SafetyMails-Team/safetymails-sdk](https://github.com/SafetyMails-Team/safetymails-sdk) |
| Batch API Swagger | [panel.safetymails.com/swagger_api2.html](https://panel.safetymails.com/swagger_api2.html) |
| Panel / Dashboard | [panel.safetymails.com](https://panel.safetymails.com) |
| Authentication | HMAC-SHA256 signature in the `Sf-Hmac` header, generated with your API Key (real-time API). Batch API requires credentials issued by support. |
| Trial | 1,000 free real-time-API credits for 15 days (plus 100 free verification credits on signup) |

---

## Real-Time API

Two ways to consume the real-time validator:

1. **Standard script** — a drop-in `<script>` embed for forms/landing pages (no code).
2. **Custom HTTP REST API** — a direct server-side POST for developers who want full control.

**Response time:** < 1 second

### Standard Script (no-code embed)

Created from the dashboard: **Real-time API → Create a new source → Standard installation**, name the origin, set the domain, choose which email statuses to allow/block, then copy the generated `<script>` into the page footer.

```html
<script src='https://optin.safetymails.com/main/safetyscript/<TICKET>/safetyoptin.js'></script>
```

**Supported platforms:**

- HTML forms / custom forms
- WordPress (Forminator, Smart Forms, Form Maker — via plugin or manual embed)
- Google Tag Manager
- Landing page platforms (RD Station, Unbounce, Instapage, Landingi, E-goi)
- CRMs and marketing automation tools

### Custom HTTP REST API (developer)

For server-side integration via direct HTTP requests (not the script).

| Item | Value |
|------|-------|
| Method | `POST` |
| URL format | `https://<TICKET_ORIGEM>.safetymails.com/api/<CODE_TICKET>` |
| Auth header | `Sf-Hmac: <hash>` where `hash = HMAC_SHA256(VALUE=email, KEY=API Key)` |
| Body | form-data, field named exactly `email` (the email address to verify) |
| Response | JSON |

`TICKET_ORIGEM` (origin subdomain) and `CODE_TICKET` come from the Real-time API panel; the API Key is the HMAC secret.

**Success response:**

```json
{
  "Success": true,
  "Email": "<the verified address>",
  "Status": "valid",
  "Score": 97
}
```

**Error response:**

```json
{
  "Success": false,
  "ErrorCode": "401",
  "Message": "Invalid API Key"
}
```

The response reports whether verification succeeded, the email `Status`, a `Score`, and (per the marketing/API page) remaining account credits. `Status` values mirror the bulk result categories (valid / invalid / catch-all / disposable / spamtrap / role-based / risky / unknown).

### Features

- Syntax check
- MX record validation
- Disposable email detection
- Domain typo correction (e.g., "gmial.com" -> "gmail.com")
- Customizable error messages (script mode)
- Flood / abuse protection

### How the script works

1. Add the JavaScript snippet to the form page footer
2. Snippet intercepts form submission
3. Email is validated via SafetyMails servers
4. Callback returns validation result
5. Form submission is allowed or blocked based on configured allow/block statuses

> **GAP:** Rate limits / throttling for the real-time REST API are not documented. One SDK example file (`examples/realtime-validation.php`) shows an alternate `POST https://api.safetymails.com/v2/validation/email` with a JSON body and an `apikey` header instead of HMAC — this is a rough placeholder example and contradicts the authoritative `docs/realtime-api-custom.md`; treat the `<TICKET_ORIGEM>.safetymails.com/api/<CODE_TICKET>` + `Sf-Hmac` form as the documented surface and confirm any `/v2/validation/email` route with support before relying on it.

---

## Bulk / Batch Verification

Two paths:

1. **Panel upload (no-code):** upload a list in the dashboard.
2. **Batch validation API (developer):** programmatic list validation, documented via Swagger.

### Batch Validation API

| Item | Value |
|------|-------|
| Swagger docs | [panel.safetymails.com/swagger_api2.html](https://panel.safetymails.com/swagger_api2.html) |
| Access | Requires API credentials + authorization issued by the SafetyMails team (contact SafetyMails support to enable batch access) |
| Auth | HMAC-SHA256 / issued credentials (all requests must be authenticated) |
| Operations | List submission, job status checks, download of results |

The batch API supports submitting a list, polling job status, and downloading results — so programmatic bulk verification IS possible (earlier "UI-only" framing was wrong); it is just gated behind support-provisioned credentials and the Swagger spec rather than the open help-center docs.

### Upload Options (panel)

- CSV file
- TXT file
- Paste email list directly

### Limits

- Up to 2,000,000 emails per batch
- 1 credit = 1 email verified

### Verification Process

- 19-step verification algorithm (proprietary)

### Result Categories

| Category | Description |
|----------|-------------|
| Valid | Deliverable email address |
| Invalid | Undeliverable email address |
| Catch-All | Domain accepts all addresses (deliverability uncertain) |
| Disposable | Temporary/throwaway email service |
| Spamtrap | Known spam trap address |
| Role-Based | Generic address (e.g., info@, support@) |
| Syntax Error | Malformed email format |
| Domain Error | Domain does not exist or has no MX records |

### Export

- Results downloadable as CSV from the panel
- Or via the batch API's "download of results" operation (see Swagger)

---

## Email Finder

**Input:** First name + last name + domain

**Output:** Verified corporate email address

### Credit Costs

| Outcome | Credits |
|---------|---------|
| Email found (verified) | 7 credits |
| Risky or invalid domain | 1 credit |
| Email not found | 0 credits |

### Constraints

- Results stored for 30 days in dashboard
- Individual lookups only — no bulk or scraping
- No separate API endpoint documented

> **GAP:** Email Finder API access is unclear. This feature may be UI-only (panel dashboard). No REST endpoint, request format, or response schema is documented for programmatic Email Finder lookups.

---

## Integrations

### Native Integrations

- RD Station
- SendGrid
- HubSpot
- Mailchimp
- ActiveCampaign
- WordPress
- E-goi
- Pipedrive
- Brevo (formerly Sendinblue)
- Salesforce

### Automation Platforms

- Zapier
- Make (formerly Integromat)
- n8n
- Pabbly Connect
- Pluga

---

## Authentication

API keys / ticket origins are generated in the SafetyMails panel under **Real-time API**:

1. Log in to [panel.safetymails.com](https://panel.safetymails.com)
2. Open the Real-time API panel and create/open a source to get the API Key, `TICKET_ORIGEM`, and `CODE_TICKET`
3. For the batch API, request credentials from SafetyMails support

**How the key is used (real-time REST API):** the API Key is NOT sent directly. Instead it is the HMAC secret — you compute `hash = HMAC_SHA256(value=email, key=API Key)` and send it in the `Sf-Hmac` request header. Official examples are provided for JavaScript, PHP (CURL), Python, Java (SHA1 + HMAC), and Go in the SDK repo.

> **GAP:** Key rotation, scoping, and revocation are not documented. The standard `<script>` embed handles auth internally (the ticket is baked into the script URL).

---

## Known Documentation Gaps

The following areas still lack public documentation and should be flagged for manual review:

| Gap | Details |
|-----|---------|
| **No rate limit documentation** | Throttling behavior, concurrency limits, and retry guidance are undocumented for both the real-time REST API and the batch API |
| **No webhook support documented** | No callbacks/webhooks for async batch verification completion are documented (job status is polled, not pushed) |
| **Email Finder API access unclear** | No REST endpoint, request format, or response schema documented for programmatic Email Finder lookups — appears panel-only |
| **Batch API spec is gated** | Full request/response schemas live in the Swagger spec at panel.safetymails.com/swagger_api2.html and require support-issued credentials to access |
| **Alternate real-time route unconfirmed** | An SDK example shows `POST api.safetymails.com/v2/validation/email` with an `apikey` header; this conflicts with the documented `Sf-Hmac` flow and is unconfirmed |
| **Error catalog incomplete** | Only a `401 Invalid API Key` error example is published; full error code list is not documented |
| **Real-time API versioning** | No version prefix or changelog for the `<TICKET_ORIGEM>.safetymails.com/api/<CODE_TICKET>` route |

---

*Last updated: 2026-06-13 (re-verified against live docs + official SDK repo)*
*Status: Real-time REST API and batch API confirmed; rate limits, webhooks, and Email Finder API remain undocumented.*
