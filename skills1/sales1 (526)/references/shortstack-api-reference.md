<!-- Source: ShortStack Help Center — Entries API (help.shortstackapp.com/hc/en-us/articles/29277366901901-Entries-API) and Securing Webhook Form Integrations (…/234467468) and apitracker.io/a/shortstack (fetched 2026-06). The help center is Cloudflare-protected (WebFetch/curl blocked); the verbatim auth/base-URL/params/response below were captured from indexed search results quoting those pages. Confirm exact endpoint list + payload schema against the live developer docs / OpenAPI spec in-account. -->

# ShortStack API Reference

## Overview

ShortStack exposes a developer surface for **reading entry/lead data** and **receiving real-time entries via signed webhooks**, plus a **Webhooks management API**, a **Sandbox** environment, and an **OpenAPI/Swagger** spec (per apitracker). Campaigns themselves are built in the ShortStack app (UI).

## Entries API

Read the entries (form submissions / contest entries) collected in your account.

**Base URL / endpoint:**

```
https://entries.shortstack.com/entries
```

**Authentication (verbatim):** every request needs the header

```
Authorization: Token token=YOUR_API_KEY
```

(Generate the API key in your ShortStack account settings.)

**Query parameters:**
- `per_page` — how many entries to return. **Default 100, max 5000.**
- `sort` — field to sort by (e.g. `received`).
- `direction` — `ascending` | `descending` (e.g. `descending`).

**Example requests (verbatim):**

```bash
curl -i -H "Authorization: Token token=$API_KEY" \
  "https://entries.shortstack.com/entries?per_page=25"

curl -i -H "Authorization: Token token=$API_KEY" \
  "https://entries.shortstack.com/entries?sort=received&direction=descending&per_page=50"
```

**Response format (verbatim):** successful calls return JSON shaped like

```json
{ "data": [ /* entry objects */ ] }
```

> Each entry object carries the lead/entry fields captured by the campaign form (email, name, custom fields, timestamps). The exact per-entry schema isn't published here — inspect a real response. Use `per_page` + `sort=received&direction=descending` to page newest-first; confirm the cursor/offset mechanism for >5000 entries in the live docs.

## Webhooks (real-time entries)

A webhook sends a **HTTP POST** to your URL **each time a campaign receives a new entry** — pushing the form's data to your server (or to "hundreds of tools" via Zapier).

**Signature verification (verbatim):** ShortStack uses your **secret key** to generate an encoded string sent in the **`X-Ss-Signature`** request header. The signature is created by **combining the request body with your secret key** (HMAC). Verify it server-side before trusting the payload:

1. Take the raw request body.
2. Compute the HMAC using your shared **secret key**.
3. Compare your computed value to the **`X-Ss-Signature`** header (constant-time compare); reject on mismatch.

This is a real signed webhook — unlike many giveaway tools, you can cryptographically verify authenticity. Still dedupe on the entry id (retries/duplicates can occur).

**Trigger:** new entry on the campaign. **Payload:** the entry/form data (same fields as an Entries API entry). Confirm the exact JSON against a live delivery (e.g. webhook.site) since the help center is bot-protected.

**Webhooks management API + Sandbox:** ShortStack also exposes a Webhooks management API and a sandbox environment (per apitracker) for programmatically configuring/testing webhooks — see the live developer docs.

## Integrations (non-API)

- **Native:** Mailchimp (direct), HubSpot, Salesforce.
- **iPaaS:** Zapier (and "hundreds of tools" via webhooks), LeadsBridge.
- **Export:** lead export (CSV) from the dashboard.

## Notes / gaps

- **No MCP server** documented.
- The help center (help.shortstackapp.com) is **Cloudflare-protected**, so the full endpoint catalog (campaigns API?, fields, pagination beyond `per_page`) and the exact entry/webhook payload schema weren't directly fetchable — verify against the in-account developer docs / OpenAPI spec. Auth, base URL, the `per_page`/`sort`/`direction` params, the `{ "data": [...] }` response, and the `X-Ss-Signature` webhook signature are confirmed.
