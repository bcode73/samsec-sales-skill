<!-- Source: developers.frill.co (api/authentication.md, api/pagination.md, api/reference/* via llms.txt) + help.frill.co/article/93-webhooks (fetched 2026-06). Auth/base-URL/pagination/webhook specifics are verbatim from the official docs. The GitBook docs also support a dynamic query: GET https://developers.frill.co/api/<page>.md?ask=<question> -->

# Frill API Reference

## Base URL

```
https://api.frill.co/v1/
```

## Authentication

Every request needs your **API key** (from the Frill Dashboard → **app.frill.co/settings/company**). Three methods — **Bearer header is recommended**:

```bash
# Recommended: HTTP Header — Bearer
curl https://api.frill.co/v1/ideas -H "Authorization: Bearer $FRILL_API_KEY"

# Query string
curl "https://api.frill.co/v1/ideas?api_key=$FRILL_API_KEY"

# Basic auth (API key as the username, no password)
```

> The key has many privileges — keep it secret (server-side only; never in client code/GitHub).

## Responses

JSON. List endpoints return an `idea`/`comment`/etc. array plus a `pagination` object.

## Pagination (cursor-based)

List responses include a `pagination` object:

```json
{
  "pagination": {
    "count": 25,
    "total": 312,
    "hasNextPage": true,
    "startCursor": "CURSOR",
    "endCursor": "CURSOR"
  }
}
```

To get the next page, pass `pagination.endCursor` as the **`after`** query param:

```
GET https://api.frill.co/v1/ideas?after=END_CURSOR_FROM_PREVIOUS_REQUEST
```

## Resources (endpoints)

REST resources (each supports list/get; many support create/update/delete — confirm per-resource):

- **Ideas** — `/v1/ideas` — feedback/suggestions from customers; each has a **Status** and **Topics**.
- **Comments** — `/v1/comments` — discussion on Ideas.
- **Votes** — `/v1/votes` — user support/preference on Ideas.
- **Statuses** — `/v1/statuses` — an Idea's stage (suggestion → in progress → done).
- **Topics** — `/v1/topics` — tag-like grouping (an Idea can have many).
- **Followers** — `/v1/followers` — users tracking a board/Idea/Announcement ("tracked users").
- **Announcements** — `/v1/announcements` — changelog/release posts.
- **Announcement Categories** — `/v1/announcement-categories` — group announcements.
- **Notes** — `/v1/notes` — (newer) internal notes on Ideas.

Example — list ideas (cURL):

```bash
curl "https://api.frill.co/v1/ideas?after=$CURSOR" \
  -H "Authorization: Bearer $FRILL_API_KEY"
```

## Webhooks (real-time, HMAC-signed)

**Set up:** log in → profile avatar → **Settings → Webhooks** (Company Settings).

**Payload** (HTTP POST) fields:

```json
{
  "triggered_at": "2026-06-27T10:00:00Z",   // UTC timestamp
  "event": "idea.created",                    // event name
  "data_type": "idea",                        // type classification
  "data": {  }                              // the entity payload
}
```

**Events:**
- **Ideas:** created, updated, deleted, archived, status changed, roadmap visibility, merged
- **Votes:** voted, unvoted
- **Comments:** created, updated, deleted
- **Notes:** created, updated, deleted
- **Announcements:** created, published, updated, deleted

**Signature verification (HMAC-SHA256):**
1. Get your **Webhook Secret** from **Company Settings → Webhooks**.
2. Compute `HMAC-SHA256(rawJsonPayload, webhookSecret)`.
3. Compare to the incoming **signature header**; reject on mismatch.

```php
// PHP example (from docs)
$computedSignature = hash_hmac('sha256', $payloadJson, $webhookSecret);
if ($computedSignature != $frillSignature) { die('Signatures do not match!'); }
```

Use a constant-time compare in production, and dedupe on the entity id + `triggered_at`.

## Frill-Script (front-end), SSO, integrations

- **Frill-Script** — embed the **widget**, run **surveys**, and **identify users** (pass logged-in user data so votes/ideas attach to a real user). See `developers.frill.co/frill-script/*`.
- **SSO** — single sign-on so your users are auto-authenticated on your Frill board.
- **15+ native integrations:** Slack, Jira, Trello, Zendesk, Intercom, Help Scout, Zapier, Linear, Asana, Airtable, Monday.com, Miro, Basecamp, Google Docs/Sheets, Azure DevOps.

## Pricing (best-effort)

Lowest paid **~$25/mo**, up to **Enterprise ~$349/mo**; 14-day free trial (no card); discounted rates for startups / nonprofits / charities / open-source on application. Verify on frill.co/pricing.

## Docs note

GitBook docs: append `.md` to any page URL, full index at `developers.frill.co/llms.txt` / `llms-full.txt`, and a dynamic query `GET .../<page>.md?ask=<question>` for specifics. Use these to confirm exact per-resource create/update fields.
