<!-- Source: https://developers.featureos.app/docs/authentication , /docs/errors , /docs/webhooks , /docs/webhooks/examples , /docs/webhooks/setup , /docs/webhooks/retry , /docs/oauth-apps , /docs/oauth-apps/authorization-flow , /docs/oauth-apps/scopes , /docs/oauth-apps/access-tokens , /docs/oauth-apps/webhooks , /docs/widgets (captured 2026-06-28) -->

# FeatureOS API Reference

FeatureOS (formerly **Hellonext**) v3 REST API. The product rebranded from Hellonext to FeatureOS, but several **legacy identifiers persist**: API keys are prefixed `hn_`, and the JS widget class is `HellonextWidget`. The org/company is Skcript (github.com/skcript).

The endpoint catalog at `/docs/api` is rendered client-side (an interactive reference that WebFetch/curl cannot capture). Authentication, errors, OAuth, webhooks, and widgets were captured verbatim below. Resource paths are confirmed where noted; others are constructed from the OAuth **scopes** list and marked accordingly — verify against the live `/docs/api` reference.

## Base URL & API version

- **Base URL:** `https://api.featureos.app/api/v3`
- **Version:** v3 (current)
- All requests must use **HTTPS**; plain HTTP is rejected.

## Authentication (verbatim)

Pass your organization API key in the `API-KEY` header on every request:

```
-H 'API-KEY: hn_your_api_key'
```

- All API keys begin with the `hn_` prefix (since November 30, 2022).
- Generate a key: log in → **Dashboard → Organization Settings → Advanced**. (Per the Help Center, API-key usage is gated to higher plans — see Pricing in the platform guide; confirm in-account.)

For operations **on behalf of a user**, include that user's SSO JWT in the `Authorization` header:

```
-H 'Authorization: Bearer <user_sso_jwt>'
```

**Security guidelines (verbatim):** never expose keys in client-side code; do not commit keys to version control; regenerate immediately if exposed; HTTPS only.

### Auth quick-start (simplest GET)

```bash
curl -s 'https://api.featureos.app/api/v3/feature_requests' \
  -H 'API-KEY: hn_your_api_key'
```

`GET /api/v3/feature_requests` (the Posts resource — feedback posts are called **feature_requests** in v3) and `GET /api/v3/buckets` (boards) are confirmed paths.

## Rate limiting (verbatim)

- **100 requests per minute per API key.**
- Exceeding the limit returns **`429 Too Many Requests`** (`ERROR_CODE_RATE_LIMITED`). Wait and retry after a brief pause; back off on 429.

## Pagination (verbatim)

- Requests returning multiple items are paginated to **30 items by default**.
- Use the **`page`** parameter for further pages.
- Use **`per_page`** for a custom page size, **up to 100**.

```bash
curl -s 'https://api.featureos.app/api/v3/feature_requests?page=2&per_page=100' \
  -H 'API-KEY: hn_your_api_key'
```

## Errors (verbatim)

### HTTP status codes

| Status | Meaning | Description |
|---|---|---|
| 200 | Success | Request served successfully. |
| 201 | Created | Resource created successfully. |
| 400 | Bad Request | The request body or parameters are invalid. |
| 401 | Unauthorized | The API key or JWT token is missing or invalid. |
| 403 | Forbidden | Your account lacks the required permissions. |
| 404 | Not Found | The requested resource does not exist. |
| 422 | Unprocessable Entity | Well-formed but contains semantic errors. |
| 429 | Too Many Requests | Rate limit exceeded — 100 requests per minute per API key. |
| 500 | Internal Server Error | Something went wrong on our end. |
| 503 | Service Unavailable | The API is temporarily down for maintenance. |

### Application error codes (returned in the response body)

- **Seat limits:** `ERROR_CODE_ADMIN_LIMIT_REACHED`, `ERROR_CODE_CSM_LIMIT_REACHED`, `ERROR_CODE_MANAGER_LIMIT_REACHED` — purchase seats or upgrade.
- **User & team:** `ERROR_CODE_USER_ALREADY_PRESENT`, `ERROR_CODE_INVITE_ALREADY_SENT`.
- **Validation:** `ERROR_CODE_INVALID_PARAM`, `ERROR_CODE_MISSING_PARAM`, `ERROR_CODE_INVALID_FORMAT`.
- **Resource:** `ERROR_CODE_NOT_FOUND`, `ERROR_CODE_ALREADY_EXISTS`, `ERROR_CODE_CANNOT_DELETE`.
- **Rate limiting:** `ERROR_CODE_RATE_LIMITED`.

### Error response format (verbatim)

```json
{ "error": "ERROR_CODE_INVALID_PARAM", "message": "The parameter 'title' is not valid." }
```

For validation errors with multiple fields:

```json
{ "errors": { "title": ["can't be blank"], "bucket_id": ["is not a valid bucket"] } }
```

## Resources

Confirmed v3 paths: `GET /api/v3/feature_requests` (posts), `GET /api/v3/buckets` (boards),
`GET /api/v3/session_info`, `POST /api/v3/votes_on_behalf`.

<!-- Constructed from the OAuth scopes inventory — verify exact paths/methods against the live /docs/api reference -->
The OAuth scopes inventory implies these resource families (read/write scopes shown):

| Resource | Scopes | Likely path |
|---|---|---|
| Posts / feature requests | `posts:read`, `posts:write` (create, update, delete, assign) | `/api/v3/feature_requests` |
| Comments | `comments:read`, `comments:write` | `/api/v3/comments` |
| Votes | `votes:read`, `votes:write` (add/remove) | `/api/v3/votes`, `POST /api/v3/votes_on_behalf` |
| Changelog | `changelog:read`, `changelog:write` | `/api/v3/changelog` |
| Roadmap | `roadmap:read` | `/api/v3/roadmap` |
| Knowledge base articles | `articles:read`, `articles:write` | `/api/v3/articles` |
| KB collections | `collections:read` | `/api/v3/collections` |
| Tags | `tags:read`, `tags:write` | `/api/v3/tags` |
| Customers | `customers:read`, `customers:write` (add/update/delete/import) | `/api/v3/customers` |
| Members | `member:read`, `member:write` | `/api/v3/members` |
| Buckets (boards) | — | `/api/v3/buckets` (confirmed) |

### Session info (verbatim — resolve the acting identity)

`GET /api/v3/session_info` (requires `posts:read`) returns who a token acts as:

```bash
curl -s https://api.featureos.app/api/v3/session_info \
  -H "Authorization: Bearer foot_xxxxxxxxxxxxxxxx"
# → {
#   "success": true,
#   "user": { "id": 4521, "name": "Acme Integration", "email": "...", "profile_picture": null },
#   "actor": "app",
#   "organization": { "id": 88, "subdomain": "feedback", "name": "FeatureOS" }
# }
```

## OAuth Apps (v3) — for integrations other workspaces install

Use OAuth 2.0 (authorization-code grant) when building an app **other organizations connect** (a Slack bot, a Jira sync). For scripting against **your own** org, a plain `API-KEY` is simpler. All OAuth endpoints are on `https://api.featureos.app`.

### Token formats (verbatim)

| Token | Prefix | Notes |
|---|---|---|
| Client ID | `foapp_` | Public identifier for your app. |
| Client secret | `fosec_` | Shown once at creation (and on rotate). Store securely. |
| Authorization code | `fooc_` | Single-use, expires in 5 minutes. |
| Access token | `foot_` | Bearer token, expires in 24 hours (`expires_in: 86400`). |
| Refresh token | `foor_` | Rotates the access token; valid until the install is revoked. |

An OAuth request sends **no** `API-KEY` and **no** per-user JWT — org, actor, and scopes are resolved from the token:

```
Authorization: Bearer foot_xxxxxxxxxxxxxxxx
```

### Authorization flow (verbatim)

1. **Register an app** (owner-org admin; auth = user JWT + `X-Organization` header):

```bash
curl -sX POST https://api.featureos.app/oauth/apps \
  -H "Authorization: Bearer <USER_JWT>" \
  -H "X-Organization: your-org" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Integration",
    "redirect_uris": ["https://myapp.com/callback"],
    "allowed_actor_modes": ["app", "self"],
    "declared_scopes": ["posts:read", "posts:write"]
  }'
# response includes client_id and client_secret (shown once)
```

`redirect_uris` must be absolute `https` (http only for loopback hosts: `localhost`, `127.0.0.1`, `[::1]`).

2. **Authorize** — `GET https://api.featureos.app/oauth/authorize` (params: `client_id` [req], `redirect_uri` [req], `scope` [optional, subset of declared], `actor` [optional: `app` or `self`]). Returns consent metadata.

3. **Consent** — `POST https://api.featureos.app/oauth/authorize/consent` (org admin approves into a `target_organization_id`; mints a single-use `fooc_` code, returns `redirect_to`).

4. **Token exchange / refresh** — `POST https://api.featureos.app/oauth/token`:

```bash
curl -sX POST https://api.featureos.app/oauth/token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "refresh_token",
    "client_id": "foapp_…",
    "client_secret": "fosec_…",
    "refresh_token": "foor_…"
  }'
# → { "access_token": "foot_… (new)", "refresh_token": "foor_… (new)",
#     "token_type": "Bearer", "expires_in": 86400, "scope": "posts:read posts:write" }
```

Refresh is a **rotation**: both the access and refresh token are replaced; the old pair stops working immediately — always store the newest pair. `invalid_grant` means the install was revoked → restart authorization.

### Scopes (verbatim)

`posts:read|write`, `comments:read|write`, `votes:read|write`, `changelog:read|write`, `roadmap:read`, `articles:read|write`, `tags:read|write`, `collections:read`, `customers:read|write`, `member:read|write`, `webhooks:manage`. Request the **minimum** scopes — admins decline broad requests. `declared_scopes` (app max) ⊇ `granted_scopes` (per install). A request to an endpoint whose scope the token lacks returns:

```json
{ "message": "Missing required OAuth scope: posts:write", "status": 403, "success": false }
```

Endpoints not opened to OAuth also return 403 (default-deny).

### Actor modes (verbatim)

- **`app`** — a dedicated bot identity owned by your app (server-to-server; changes attributed to your app; not role-capped).
- **`self`** — acts as the consenting user, respecting their permissions. **Role-capped, re-evaluated every request:** Members/CSMs/collaborators lose `:write`/`:manage` scopes (reduced to read); if the user is downgraded or removed, the token's effective permissions shrink immediately.

## Webhooks (verbatim)

Webhooks subscribe to FeatureOS events and POST JSON to your endpoint. Managed with the same API key (Dashboard → **Webhooks** → **Add Webhook**; fill URL + description, select events, Save). Your endpoint must use a valid SSL cert (`https`), be publicly accessible, and **return `200`**. Currently supports events from two modules: **Posts** (creation, updates, status changes, votes, merges, etc.) and **Changelog** (published/updated entries).

### Supported events

- Dashboard webhooks: post status updates, voting, merges, moderation, assignee changes, visibility, AI analysis; changelog published/updated.
- OAuth-app webhooks (snake_case event names, via `subscribed_webhook_events` + `webhooks:manage` scope): `post_created`, `post_updated`, `post_completed`, `changelog_created`, `changelog_updated`, `changelog_published`. At consent the installing org may restrict delivery via `granted_webhook_events` (a subset).

### Example payload (verbatim — `postCompleted`)

```json
{
  "type": "postCompleted",
  "data": {
    "id": 80874,
    "title": "Time specification for Changelogs",
    "object": "post",
    "description": "It would be beneficial to have the option to specify ... time for when the changelog should be published",
    "description_html": "<p>...</p>\n",
    "status": { "label": "Completed", "value": "completed" },
    "assignee": {},
    "approval_status": "approved",
    "hidden": false,
    "pinned": false,
    "downvotes_count": 0,
    "upvotes_count": 1,
    "etc_date": null,
    "parent_id": null,
    "created_at": 1648026486,
    "updated_at": 1651686939,
    "submitter": { "name": "Swathy R", "email": "..." },
    "url": "https://feedback.featureos.app/admin/p/time-specification-for-changelogs",
    "sentiment_type": "positive",
    "resource_keywords": [
      { "name": "changelogs", "slug": "changelogs" },
      { "name": "time specification", "slug": "time-specification" }
    ],
    "ai_summary": "Request for specifying precise time for publishing changelog",
    "nice_to_have_ratings_count": 0,
    "important_ratings_count": 0,
    "critical_ratings_count": 0,
    "total_ratings_count": 0,
    "bucket": { "id": 1, "slug": "feature-requests", "display_name": "Feature Requests" },
    "before": { "status": { "label": "Planned", "value": "planned" }, "completed_at": null },
    "after": { "status": { "label": "Completed", "value": "completed" }, "completed_at": "2022-05-04 17:55:39 UTC" }
  },
  "created": 1651686939
}
```

Note the **`before`/`after`** diff blocks on status-change events and the **unix-second** `created_at`/`updated_at`/`created` timestamps. There is no documented HMAC signature on dashboard webhooks (unlike Frill) — restrict by URL secrecy/IP and respond 200 fast; OAuth-app webhooks "use the same delivery system."

### Retry policy (verbatim)

- If your endpoint does not return `200`, the delivery is treated as failed.
- **3 retries** at intervals of **5 minutes, 30 minutes, and 2 hours**.
- If all three retries fail, FeatureOS **stops retrying and disables the webhook** (email notification sent). Re-enable via Dashboard → Organization Settings → Webhooks after fixing.
- View per-delivery attempt logs in the webhook's view.

## Widget embed (verbatim — note the legacy `HellonextWidget` class)

```html
<button id="featureosWidget">Click Here ✨</button>
<script>
  const widget = new window.HellonextWidget({
    token: 'YOUR ORGANIZATION WIDGET TOKEN',
    modules: ['feature_requests', 'changelog'],
    selector: '#featureosWidget'
  });
  widget.init();
</script>
```

Find the **widget token** in organization settings. Key options:

- `token` — org widget token. `ssoToken` — a user JWT signed with your org's **SSO key** (JSON `{ "email": "...", "name": "..." }`); **required** so users can create feature requests and vote (else activity is anonymous). `jwtToken` is **deprecated** — use `ssoToken`.
- `modules` — `feature_requests`, `changelog`, `knowledge_base`. `selector`, `placement` (`left`/`right`/`sticky-left`/`sticky-right`), `openFrom` (`center`/`left`/`right`), `type` (`popover`/`modal`), `theme` (`light`/`dark`), `accent` (hex or `{background, primary, button}`), `triggerText`.
- `enableIndicator`, `showChangelogIndicator` (new-changelog dot), `submissionBucketIds`, `hideBucketSelection`, `showOnlySubmission`, `suggestSimilarPost`, `postOnBehalf` (`{name, email, add_as_customer}`), `changelogFilters` (`{per_page, ids, labels, published_at}`), `hideChangelogLabels`, `locale`.

## Gaps

- The full endpoint catalog (`/docs/api`) is client-side-rendered and was not capturable; resource paths above are confirmed where stated and otherwise **constructed from the scopes inventory** — verify exact methods/params/bodies against the live reference before relying on them.
- Exact request/response bodies for create/update on comments, votes, changelog, customers, and tags were not in the static docs.
