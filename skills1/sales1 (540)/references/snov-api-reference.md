# Snov.io API Reference

## Overview

Snov.io provides a REST API for email finding, verification, prospect management, sender-account and warmup management, drip campaign automation, and CRM pipelines. The API uses a mix of v1 and v2 endpoints; **v2 is the current surface** for finder/verifier/campaigns/prospects/sender-accounts/warmup/CRM (most v2 finder/verifier endpoints follow an asynchronous task pattern), while v1 retains auth, the balance check, and webhook management. (Verified against live docs 2026-06-13.)

- **Base URL**: `https://api.snov.io`
- **Protocol**: HTTPS only
- **Format**: JSON request and response bodies
- **Rate Limit**: 60 requests per minute

---

## Authentication

Snov.io uses OAuth 2.0 client credentials flow.

### Obtain Access Token

```
POST /v1/oauth/access_token
```

**Parameters** (form body):

| Parameter | Type | Required | Description |
|---|---|---|---|
| `grant_type` | string | Yes | Must be `client_credentials` |
| `client_id` | string | Yes | Your API client ID |
| `client_secret` | string | Yes | Your API client secret |

**Response**:
```json
{
  "access_token": "xxxxxxxxxx",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

- Token lifespan: **1 hour** (3600 seconds). Refresh by requesting a new token before expiry.
- Include on all subsequent requests as: `Authorization: Bearer {access_token}` header.

---

## Rate Limits

- **60 requests per minute** across all endpoints.
- Exceeding the limit returns an error response. Implement exponential backoff on rate limit errors.

---

## Async Task Pattern (v2 Endpoints)

Most v2 endpoints follow a two-step async pattern:

1. **Start**: `POST /v2/{resource}/start` — submits the task and returns a `task_hash`.
2. **Result**: `GET /v2/{resource}/result/{task_hash}` — poll for results.

**Task statuses**:

| Status | Meaning |
|---|---|
| `completed` | Results are ready |
| `in_progress` | Still processing; poll again |
| `not_enough_credits` | Insufficient credits to complete |

**Webhook alternative**: Many async endpoints accept a `webhook_url` parameter. When provided, Snov.io sends results to your URL on completion instead of requiring polling.

---

## Endpoints

### Email Finder & Data Enrichment

#### Domain Search

```
POST /v2/domain-search/start
GET  /v2/domain-search/result/{task_hash}
```

Search for company information and emails by domain. Returns company details, technologies, and associated emails.

- **Cost**: 1 credit per unique request
- **Params**: `domain` (required)

#### Domain Search — Prospect Profiles

```
POST /v2/domain-search/prospects/start
GET  /v2/domain-search/prospects/result/{task_hash}
```

Retrieve prospect profiles associated with a domain.

- **Cost**: 1 credit per prospect with email found
- **Params**: `domain` (required), `positions[]` (optional, filter by job title), `page` (optional, pagination)

#### Domain Search — Prospect Email Lookup

```
POST /v2/domain-search/prospects/search-emails/start/{prospect_hash}
GET  /v2/domain-search/prospects/search-emails/result/{task_hash}
```

Find the email for a specific prospect identified by prospect hash (from prospect profiles endpoint).

- **Cost**: 1 credit per email found

#### Domain Emails

```
POST /v2/domain-search/domain-emails/start
GET  /v2/domain-search/domain-emails/result/{task_hash}
```

Get all known emails for a domain.

- **Cost**: 1 credit per unique request

#### Generic Company Contacts

```
POST /v2/domain-search/generic-contacts/start
GET  /v2/domain-search/generic-contacts/result/{task_hash}
```

Get generic company emails (e.g., info@, support@, sales@).

- **Cost**: 1 credit per unique request

#### Domain Email Count

```
POST /v1/get-domain-emails-count
```

Check how many emails Snov.io has for a domain without retrieving them.

- **Cost**: Free
- **Params**: `domain` (required)

#### Email Finder by Name + Domain

```
POST /v2/emails-by-domain-by-name/start
GET  /v2/emails-by-domain-by-name/result/{task_hash}
```

Find email addresses by providing first name, last name, and domain.

- **Cost**: 1 credit per email found
- **Params**: `rows[]` (array of objects with `first_name`, `last_name`, `domain`), `webhook_url` (optional)

#### Company Domain by Name

```
POST /v2/company-domain-by-name/start
GET  /v2/company-domain-by-name/result/{task_hash}
```

Look up a company's domain by its name.

- **Cost**: 1 credit per domain found
- **Params**: `names[]` (array of company names), `webhook_url` (optional)

#### LinkedIn Profile Enrichment

```
POST /v2/li-profiles-by-urls/start
GET  /v2/li-profiles-by-urls/result/{task_hash}
```

Enrich LinkedIn profiles by URL. Returns name, job title, company, emails, and social links.

- **Cost**: 1 credit per profile
- **Params**: `urls[]` (array of LinkedIn profile URLs), `webhook_url` (optional)

#### Profile by Email

```
POST /v1/get-profile-by-email
```

Enrich a contact profile using their email address.

- **Cost**: 1 credit (free if no data found)
- **Params**: `email` (required)

---

### Email Verifier

```
POST /v2/email-verification/start
GET  /v2/email-verification/result
```

Verify up to 10 email addresses per request.

- **Params**: `emails[]` (array, max 10), `webhook_url` (optional)

**Response fields per email**:

| Field | Description |
|---|---|
| `smtp_status` | SMTP verification result: `valid`, `unknown`, `not_valid` |
| `is_valid_format` | Whether the email format is valid |
| `is_disposable` | Whether the email is from a disposable provider |
| `is_webmail` | Whether the email is a webmail address (Gmail, Yahoo, etc.) |
| `is_gibberish` | Whether the local part appears to be random characters |
| `unknown_status_reason` | Explanation when status is `unknown` (see values below) |

**`unknown_status_reason` values** (when `smtp_status` is `unknown`):

| Value | Meaning |
|---|---|
| `banned` | High deliverability risk; could not be verified with certainty |
| `catchall` | Catch-all domain — accepts all addresses; sender-reputation risk |
| `connection_error` | Technical issue reaching the mail server; potential bounce risk |
| `greylist` | Receiving server uses greylisting filters; deliverability risk |
| `hidden_by_owner` | Email owner/domain requested removal |

---

### Email Accounts (Sender Accounts)

Manage the mailboxes you send campaigns from. (v2)

```
POST  /v2/sender-accounts/emails           # Add a sender email account
PATCH /v2/sender-accounts/emails/{id}      # Update a sender email account
GET   /v2/sender-accounts/emails           # List sender email accounts
GET   /v2/sender-accounts/check-sender-status
```

- **Cost**: Free

---

### Email Warmup

Programmatically manage mailbox warm-up. (v2)

```
POST   /v2/warm-up                # Start warm-up for a mailbox
GET    /v2/warm-up                # List warm-ups
GET    /v2/warm-up/{id}           # Get a warm-up
PATCH  /v2/warm-up/{id}           # Update a warm-up
DELETE /v2/warm-up/{id}           # Stop/delete a warm-up
GET    /v2/warm-up/{id}/statistics
```

- **Cost**: Free (consumes warm-up slots per plan)

---

### Campaign Management (v2)

> Campaign endpoints migrated to **v2**. The earlier v1 campaign endpoints
> (`/v1/get-user-campaigns`, `/v1/get-emails-replies`, `/v1/change-recipient-status`,
> `/v1/prospect-finished`, `/v1/emails-sent`, etc.) are superseded by the v2
> resource-style routes below.

#### Campaign CRUD

```
GET    /v2/campaigns                    # View all campaigns
POST   /v2/campaigns                    # Create campaign
GET    /v2/campaigns/{id}               # Get campaign info
PATCH  /v2/campaigns/{id}               # Update campaign
POST   /v2/campaigns/{id}/change-state  # Change campaign state (start/pause/etc.)
DELETE /v2/campaigns/{id}               # Delete campaign
GET    /v2/schedules                    # View all sending schedules
```

#### Campaign Email Step Content

```
POST   /v2/email-step-content        # Create email step content
GET    /v2/email-step-content/{id}   # Get email step content
PATCH  /v2/email-step-content/{id}   # Update email step content
DELETE /v2/email-step-content/{id}   # Delete email step content
```

#### Recipients & Do-Not-Email

```
GET    /v2/recipient-status/{id}     # Check recipient status
POST   /v2/recipient-status/{id}     # Change recipient status
GET    /v2/finished-prospects        # Prospects that completed a sequence
POST   /v2/do-not-email-list         # Add to do-not-email list
GET    /v2/do-not-email-lists        # View all do-not-email lists
```

- **Cost**: Free

#### Campaign Analytics & Activity (v2)

```
GET /v2/campaigns/{id}/analytics
GET /v2/campaigns/{id}/progress
GET /v2/campaigns/{id}/recipients-activity-report
GET /v2/campaigns/{id}/emails-sent
GET /v2/campaigns/{id}/emails-opened
GET /v2/campaigns/{id}/emails-clicked
GET /v2/campaigns/{id}/replies
GET /v2/campaigns/{id}/email-replies
```

A cross-campaign analytics endpoint is also available:

```
GET /v2/statistics/campaign-analytics
```

- **Cost**: Free
- **Params** (cross-campaign): `campaign_id`, `sender_email`, `sender_linkedin`, `campaign_owner`, `date_from`, `date_to` (all optional filters)

---

### CRM

```
GET /v2/pipelines              # List CRM pipelines
GET /v2/pipelines/{id}/stages  # List stages within a pipeline
```

- **Cost**: Free

---

### Prospect Management (v2)

> Prospect endpoints are documented on the current API reference under **v2**
> resource-style routes. (Some older docs reference v1 names such as
> `/v1/add-prospect-to-list`, `/v1/get-prospect-by-id`, `/v1/get-user-lists`;
> the v2 routes below reflect the current API page.)

```
POST /v2/prospects                  # Add prospect to a list
POST /v2/prospects/{id}             # Find prospect by ID
POST /v2/prospects/find-by-email    # Find prospect by email
GET  /v2/prospects/{id}/custom-fields
GET  /v2/lists                      # List all prospect lists
POST /v2/lists/{id}/prospects       # View prospects in a list
POST /v2/lists                      # Create a new prospect list
```

- **Cost**: Free

---

### Account

#### Check Credit Balance

```
POST /v1/user/balance
```

Check remaining credit balance for the authenticated account.

- **Cost**: Free

---

## Webhooks

Snov.io supports two webhook mechanisms:

### 1. Per-Request Callbacks

Many async v2 endpoints accept a `webhook_url` parameter. Results are POSTed to that URL when the task completes. This is a one-time callback for that specific request.

### 2. Persistent Webhooks (CRUD)

Manage persistent webhook subscriptions that receive ongoing notifications.

#### List Webhooks

```
GET /v1/webhooks
```

#### Add Webhook

```
POST /v1/webhooks
```

**Params**: `webhook_url` (required)

#### Update Webhook (change status)

```
PUT /v1/webhooks
```

The current API page documents `PUT /v1/webhooks` as "Change webhook status."
Older docs showed a per-id form (`PUT /v1/webhooks/{id}`).

**Params**: `webhook_url` (required)

#### Delete Webhook

```
DELETE /v1/webhooks/{id}
```

---

## Error Handling

- **Authentication errors**: Returned when the token is expired or invalid. Re-authenticate by requesting a new access token.
- **Rate limit errors**: Returned when exceeding 60 requests/minute. Implement backoff and retry.
- **Credit errors**: Async tasks return `not_enough_credits` status. Check balance with `/v1/check-user-balance` before bulk operations.
- **Standard HTTP status codes**: 200 (success), 400 (bad request), 401 (unauthorized), 429 (rate limited), 500 (server error).

---

## SDKs & Libraries

No official SDKs are provided. Third-party options:

- **PHP**: [HelgeSverre/snov-io](https://github.com/HelgeSverre/snov-io)
- **Python**: dltHub (data loading tool with Snov.io source)
