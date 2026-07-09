<!-- Source: https://github.com/sisbell/chatgpt-plugin-store/blob/main/specs/theresanaiforthat.com.json -->
<!-- OpenAPI spec retrieved from ChatGPT plugin store archive -->

# There's an AI for That API Reference

> **STATUS — verified 2026-06-13.** This API was the search backend for TAAFT's **ChatGPT plugin**. OpenAI discontinued ChatGPT plugins (new plugin chats ended **March 19, 2024**; all plugin chats shut down **April 9, 2024**), so the plugin surface is dead. The `/api/search/` endpoint and `/openapi.json` still resolve on theresanaiforthat.com but now sit behind a **Cloudflare bot challenge** (scripted GET returns HTTP 403 with a "Just a moment…" interstitial), so this can no longer be confirmed as an openly callable public API. TAAFT publishes **no public REST API, no webhooks, and no SDKs**. Treat everything below as historical/best-effort — do not build a supported integration on it.

## OpenAPI Specification

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "There's An AI For That",
    "version": "v1.0"
  },
  "servers": [
    {
      "url": "https://theresanaiforthat.com"
    }
  ],
  "paths": {
    "/api/search/": {
      "get": {
        "operationId": "searchQuery",
        "summary": "Search API",
        "parameters": [
          {
            "name": "q",
            "in": "query",
            "description": "Search query",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string"
                      },
                      "task": {
                        "type": "string"
                      },
                      "url": {
                        "type": "string"
                      },
                      "use_case": {
                        "type": "string"
                      }
                    }
                  },
                  "example": [
                    {
                      "name": "Example Name",
                      "task": "Example Task",
                      "url": "https://theresanaiforthat.com/ai/example/?ref=search&term=example&from=chatgpt",
                      "use_case": "Example Use Case"
                    }
                  ]
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## Authentication

- **Type**: Service HTTP with bearer token
- **User authentication required**: No
- **OpenAPI spec URL**: https://theresanaiforthat.com/openapi.json

## Plugin manifest

- **Name (human)**: There's An AI For That
- **Name (model)**: theresanaiforthat
- **Description**: Find the right AI tools for any use case, from the world's largest database of AI tools.
- **Contact**: plugin@theresanaiforthat.com
- **Legal**: https://theresanaiforthat.com/terms/

## Endpoint details

### GET /api/search/

Search TAAFT's database of 50,000+ AI tools by task/query. (Now Cloudflare-gated — see status banner above.)

**Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| q | query | string | Yes | Search query (task, problem, or use case) |

**Response (200):**
Array of matching AI tools:

| Field | Type | Description |
|---|---|---|
| name | string | Tool name |
| task | string | Task category the tool addresses |
| url | string | TAAFT tool page URL (includes referral tracking params) |
| use_case | string | Specific use case description |

**Notes:**
- Results are returned as a JSON array — the ChatGPT plugin reorders by relevance
- URLs include tracking parameters (`ref=search`, `term={query}`, `from=chatgpt`)
- The API powered the (now-deprecated) ChatGPT plugin for AI tool discovery
- No rate limit documentation is publicly available
- As of 2026-06-13 the endpoint is behind Cloudflare bot protection (HTTP 403 / "Just a moment…" to scripted requests), so unauthenticated programmatic access can no longer be confirmed
