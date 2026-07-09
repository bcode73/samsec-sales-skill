# Meltwater API Reference

## Overview

The Meltwater API provides programmatic access to media monitoring, social analytics, and AI-powered insights.

**Base URL**: `https://api.meltwater.com` — current endpoints take the form `/v3/<feature>/...`
**API versions**: Both **v3** and **v4** are live. Per the official overview: *"We are currently building out a new API version, version 4, which in time will support all features. For now, newer features are supported by v4 and some features remain in v3."* Most documented endpoints are still v3; check the reference for the version of a given endpoint, and watch the changelog for planned deprecation dates.
**Auth**: API key via `apikey` request header (same header for v3 and v4)
**Protocol**: HTTPS required (plain HTTP will fail)
**OpenAPI spec**: Available for download in YAML format from the developer portal

## Authentication

```
apikey: YOUR_API_TOKEN
```

API tokens are created and managed in the Meltwater application under API Credentials. If a token is compromised, revoke it and create a new one from the same page.

## API Feature Areas

### Listening

Export, stream, search, and analyze mentions from your Meltwater searches.

| Capability | Endpoint(s) | Description |
|---|---|---|
| **Search management** | `GET /v3/searches`, `GET /v3/searches/{id}`, `PUT /v3/searches/{id}` | List saved searches, get an individual search, update a search (pass a search object as the payload) |
| **Mention export** | `GET /v3/exports/one-time/{export_id}`, `GET /v3/exports/recurring/{export_id}` | Batch export mentions matching a saved search; exports are one-time (run once, no auto-refresh) or recurring (run on a schedule). These GET endpoints return the status of an export. |
| **Analytics** | `GET /v3/analytics/{search_id}` | Generate aggregate analytics (summary, plus pre-defined types such as `top_keyphrases` and `top_locations`) from a saved search + time window |
| **Mention streaming / Data Streams** | `POST /v3/hooks`, `GET /v3/hooks`, `DELETE /v3/hooks/{hook_id}` | Real-time push of mentions to your endpoint — see Webhooks (Data Streams) below |
| **Mention tagging** | (Listening) | Apply tags to mentions programmatically |
| **X post rehydration** | (Listening) | Retrieve full X/Twitter post data for mentions |
| **Custom output templates** | (Listening) | Define custom content output formats for exports |

### Explore+

Optimized searching with advanced features.

| Capability | Description |
|---|---|
| **Advanced search** | Optimized mention search with enhanced filtering |
| **Analytical reporting** | Advanced analytics and reporting on search results |
| **Search management** | Create and manage optimized saved searches |
| **Custom fields** | Define and manage custom fields for mention enrichment |

### Social Analytics

Fetch content and metrics from owned social media accounts.

| Capability | Description |
|---|---|
| **Owned posts** | Retrieve posts from connected social accounts |
| **Owned analytics** | Fetch engagement metrics, reach, and performance data |

### Mira API (AI)

AI-powered chat-completion endpoint for media intelligence insights.

| Capability | Endpoint | Description |
|---|---|---|
| **Responses** | `POST /v3/mira/responses` | Chat-completion endpoint — submit one or multiple input messages, receive AI-generated insights with citations. Request body uses an `input` array of message objects (`role` + `content`, where `content` is an array of `{type, text}`). |
| **Streaming** | `POST /v3/mira/responses` (set `streaming: true`) | Server-sent events; chunks end on a `[DONE]` event. The conversation Thread ID is returned in the `Thread-Id` response header. |
| **Threads** | (responses body) | Pass an optional `thread_id` to continue an existing conversation; omit it to start a new thread. |
| **Projects** | `GET /v3/mira/projects` | List your available projects. Associate a project with a request by sending the `Project-ID` header. |
| **MCP Server** | `https://api.meltwater.com/mcp` | Remote MCP server for AI assistants (Claude Desktop, Cursor, etc.). Authenticate with the `apikey` header (e.g. via `npx mcp-remote https://api.meltwater.com/mcp --header "apikey: <key>"`). Limited to 60 requests/minute, shared with the Mira responses endpoint. |

**Access**: Mira API is sold as a separate package. Contact your account manager.

### Bring Your Own Content (BYOC)

Import custom content into Meltwater for analysis.

| Capability | Endpoint | Description |
|---|---|---|
| **Content import** | `POST /v3/imports/documents` | Upload custom documents/articles for analysis. Up to **500 documents per request**; send multiple requests for more. The `id` field must be unique within a batch — duplicate IDs reject the whole batch with `400 Bad Request`. If any document fails schema validation, the entire batch is rejected with per-document error messages; fix and re-submit the whole batch. |
| **Import monitoring** | `/v3/imports/batches`, `/v3/imports/import_tags` | Track the progress and status of import jobs. |

BYOC is actively maintained — recent changelog entries (through Jan 2026) added duplicate detection, an `Explore+ Custom Fields` link, and a `user.imageUrl` field.

### BI Integrations

Connect Meltwater data to business intelligence tools.

| Tool | Integration method |
|---|---|
| **Power BI Desktop** | Direct connector |
| **Power BI Service** | Cloud connector |
| **Looker Data Studio** | Data connector |

## Usage Limits

API feature access and usage limits depend on your Meltwater package. Check the Usage Statistics page in your Meltwater application or contact your account manager.

## Rate Limits

Rate limits ARE publicly documented on the developer portal (Usage Limits page). As of 2026-06-13:

| Scope | Limit |
|---|---|
| **General endpoints** | 100 calls / minute |
| **Platform-wide** | 2000 requests / hour, per IP address |
| **Export endpoints** | 20 calls / minute |
| **Earned media analytics endpoints** | 5 calls / second AND 100 calls / minute |
| **Mira API (and MCP server, shared)** | 60 requests / minute |

In addition, package-level usage limits apply: analytics calls are capped per day, and Mira prompts are capped per calendar month, both per your contract. Check the Usage Statistics page in the Meltwater app for your current allotments.

## Webhooks (Data Streams)

Meltwater DOES support webhooks — called **Data Streams** in the product and **hooks** in the API (for historical reasons). Available if data streaming is included in your package; your contract states how many streams you can run concurrently.

**Set up a stream** — `POST /v3/hooks` with a JSON body:
```json
{
  "search_id": <search_id>,
  "target_url": "<your_https_endpoint>",
  "template": { "name": "api.json" }
}
```
Returns a `hook_id` (needed to delete the hook). List running streams with `GET /v3/hooks`; tear one down with `DELETE /v3/hooks/{hook_id}`.

**Delivery**: Meltwater POSTs `Content-Type: application/json` to your `target_url`. Your service must respond `2xx` (HTTP 200) within a **30-second timeout**. The API retries **5 times** with a **5-minute delay** between attempts; if your endpoint never returns 2xx across those attempts, **the hook is deleted**.

**Signing / document verification**: Each delivery includes an `X-Hub-Signature` header — an HMAC-SHA1 hex digest of the JSON payload, 40 chars, prefixed `sha1=`. The shared secret is either supplied by you via the `X-Hook-Secret` request header on `POST /v3/hooks` (min 16, max 64 chars) or auto-generated by Meltwater; either way you read it back from the `X-Hook-Secret` response header. Verify by recomputing the HMAC over the raw body with your secret and comparing to `X-Hub-Signature`.

## SDKs & Developer Resources

- **Developer Portal**: https://developer.meltwater.com/docs/
- **OpenAPI Spec**: Downloadable YAML from the reference page
- **API Guides**: https://developer.meltwater.com/docs/meltwater-api/guides/
- **Academy**: https://academy.meltwater.com (training and certification)
- **Community**: https://help.meltwater.com (help articles and guides)

## Status Codes

Standard HTTP status codes. Key ones:
- `200` — Success
- `401` — Unauthorized (invalid or missing API key)
- `403` — Forbidden (feature not included in your package)
- `429` — Rate limit exceeded
- `500` — Server error

All requests include a `X-Request-Id` header for debugging and support escalation.

## Multi-Company Support

The API supports multi-company accounts. If your organization manages multiple Meltwater accounts, you can access data across companies with appropriate credentials.
