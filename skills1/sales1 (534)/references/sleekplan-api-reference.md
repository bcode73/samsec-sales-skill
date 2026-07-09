<!-- Source: https://sleekplan.com/docs/api/ , https://sleekplan.com/docs/webhooks/ , https://sleekplan.com/docs/single-sign-on/ , https://sleekplan.com/docs/mcp-server/ , https://sleekplan.com/docs/sdk/overview/ , https://sleekplan.com/docs/llms.txt — captured 2026-06-28 -->

# Sleekplan API & Integration Reference

> Captured verbatim from Sleekplan's public docs. **Sleekplan does not publish a separate public API specification** — the orientation docs (below) list resources, but the **full endpoint reference (exact paths, parameters, request bodies, examples) lives in the dashboard at Settings → Developer (`app.sleekplan.com/settings/developer`)**. JSON shapes marked `<!-- Constructed -->` are assembled from the docs and must be verified against the live in-app reference. Secret-shaped values are placeholders.

## Four authentication mechanisms

From the docs index: *"four authentication mechanisms — JWT SSO for users, API keys for the REST API, OAuth for MCP clients, and secret tokens for webhooks and Canvas."*

| Surface | Mechanism |
|---|---|
| REST API | **API key** — `Authorization: Bearer YOUR_API_KEY` (from Settings → Developer) |
| Widget users | **JWT SSO** — HS256-signed token with your SSO secret |
| MCP clients | **OAuth 2.1** (PKCE, dynamic client registration) |
| Webhooks + Canvas | **Secret token** — passed as a GET parameter on your endpoint URL |

---

## REST API

### Authentication (verbatim)
The API requires Bearer token authentication: `Authorization: Bearer YOUR_API_KEY`. Users obtain keys via the dashboard at **Settings → Developer** (`https://app.sleekplan.com/settings/developer`).

> "the full endpoint reference (parameters, request bodies, examples) lives in the Sleekplan dashboard at **Settings → Developer**." The company does not publish a separate public API specification document. The page does not explicitly specify a public base URL or version prefix — confirm the base, paths, and pagination in the in-app reference.

### Resources (verbatim, from docs/api and docs/llms.txt)

- **Feedback / Posts** — create, read, update, manage feedback items. *"Returns a list of feedback posts. Sorted by trend by default."*
- **Comments** — create, retrieve, update, delete; **like** a comment; **list comments for a post**.
- **Votes & Interactions** — create/update a vote; list votes on a post.
- **Metadata** — add, update, retrieve, remove metadata keys associated with feedback posts.
- **Intelligence & Surveys** — submit content to an **intelligence queue**; create + list **NPS** responses and **satisfaction** survey responses.
- **Changelog Updates** — create, retrieve, update, delete, list updates; create + list satisfaction responses tied to a changelog entry.
- **End-Users** — create, retrieve, update, list, delete end-user accounts. *"Permanently deletes an end-user… Anonymizes the user's references"* across all activity.
- **Tags** — read and assign to feedback.
- **Topics** — manage category structures.

### Auth quick-start (cURL)
```bash
# Exact base/path/params are in the in-app reference (Settings → Developer).
curl -s https://api.sleekplan.com/v1/post \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Constructed request/response shapes
> `<!-- Constructed from docs — verify against live API (paths/fields may differ) -->`

**List feedback posts** (`GET` posts — sorted by trend by default):
```json
{ "data": [
  { "id": 1234567890, "title": "Add dark mode", "status": {"id": 3, "name": "Planned"},
    "votes": 42, "topics": [{"id": 9, "name": "UI"}], "tags": ["mobile"] }
] }
```

**Create a feedback post** (`POST` post):
```json
{ "title": "Add dark mode", "description": "Please add a dark theme", "user": { "mail": "user@example.com" } }
```

**Add a comment** (`POST` comment on a post):
```json
{ "post": 1234567890, "value": "We're considering this for Q3", "user": { "mail": "pm@example.com" } }
```

**Create a vote** (`POST` vote on a post):
```json
{ "post": 1234567890, "user": { "mail": "user@example.com" } }
```

**Create an end-user** (`POST` user):
```json
{ "mail": "user@example.com", "name": "user", "img": "https://example.com/a.png", "weight": 4 }
```

Pagination, rate limits, and exact error shapes are not in the public orientation docs — confirm in the in-app reference.

---

## Webhooks (verbatim)

Webhooks deliver real-time POST notifications to your endpoint when feedback, votes, comments, or changelog entries change. Create a public HTTP endpoint that accepts POST requests and returns a `2xx` status code.

### Security (verbatim)
For verification, append a secret key as a GET parameter: `https://endpoint.yourapp.com/webhooks?key=MY_SECRET_KEY`. The docs state: *"Sleekplan does not sign webhook payloads with an HMAC signature. Using a secret GET parameter is the recommended way to verify that requests originate from Sleekplan."*

### Registration steps (verbatim)
1. Open product **Settings → Developer**.
2. Scroll to **Webhooks** and click **"Add webhook"**.
3. Enter your endpoint URL (including the `?key=` parameter).
4. Save; Sleekplan begins delivering events immediately.

### Event types (verbatim)
**Feedback/Suggestion events:** `item.create`, `item.update`, `item.delete`, `comment.create`, `comment.update`, `comment.delete`, `vote.create`, `subscription.create`, `subscription.delete`

**Other events:** `user.create`, `user.update`, `user.delete`, `changelog.create`, `changelog.update`, `changelog.subscribe`, `satisfaction.create`

### Payload structure (verbatim)
```json
{
  "product_id": 5456534244,
  "action": "item.create",
  "data": {},
  "timestamp": "1506985999999"
}
```
Fields: `product_id` (number), `action` (string), `data` (object matching the REST API response for that object), `timestamp` (Unix milliseconds).

> The docs contain **no information about retry behavior**. Payload `data` structures match the corresponding REST API responses.

---

## MCP Server (verbatim)

Server endpoint: `https://mcp.sleekplan.com/mcp`

**Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "sleekplan": {
      "url": "https://mcp.sleekplan.com/mcp"
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add sleekplan --transport streamable-http https://mcp.sleekplan.com/mcp
```
Then launch Claude Code and run `/mcp` to authorize via OAuth.

**Authentication (verbatim):** *"OAuth 2.1 with dynamic client registration."* On initial connection your AI client opens a browser to sign into Sleekplan and select which workspace to authorize; future connections authenticate automatically. *"OAuth 2.1 with PKCE"* — only access tokens reach the AI client; all traffic uses HTTPS.

**Capabilities (resource categories):** Feedback (list, create, retrieve, modify, remove, analyze stats, find similar items, merge, apply tags), Comments, Changelog, Surveys, Votes, Users, Topics, Tags, Workspace (view configuration and settings).

---

## JWT Single Sign-On (verbatim)

Sleekplan SSO is JWT-based. Flow: a user performs an authenticated action → the SDK calls `$sleek.sso` → your server generates a signed token → you pass it back via callback for Sleekplan to verify and authenticate the user.

**Token signing:** signed using **HMAC SHA-256 (HS256)** with your private SSO secret key (from Settings → Developer). *"Your SSO secret key must only ever be used server-side."*

**JWT payload fields:**

| Field | Required | Purpose |
|---|---|---|
| `mail` | Yes | Email uniquely identifying the user |
| `id` | No | Your internal user ID (recommended) |
| `name` | No | Username (lowercase, letters/numbers only) |
| `img` | No | Avatar image URL |
| `weight` | No | User weighting 1–10 for impact scoring |
| `meta` | No | Additional key-value pairs |

**Example (Node.js, verbatim — secret is a placeholder):**
```javascript
const jwt = require('jsonwebtoken');
const key = 'PRIVATE_SSO_KEY';

function createSSOToken(localUser) {
    const userData = {
        mail: localUser.mail,
        id: localUser.id,
        name: localUser.name,
        img: localUser.imgStr,
        weight: 4,
        meta: { companyName: localUser.cName }
    };
    return jwt.sign(userData, key, { algorithm: 'HS256' });
}
```

**Integration options (verbatim):**
- **Widget on page load:** set `window.SLEEK_USER` before the snippet loads.
- **Single-page apps:** call `$sleek.setUser()` after the `sleek:init` event.
- **On-demand:** assign a function to the `$sleek.sso` callback.
- **Standalone/Iframe:** pass the token as the GET parameter `?sso=YOURTOKEN`.

---

## JavaScript SDK (`$sleek`) (verbatim)

Programmatic control via the **`$sleek`** global object.

**Widget control:** `$sleek.open(view, callback)`, `$sleek.close()`, `$sleek.toggle(view)`, `$sleek.showButton()` / `$sleek.hideButton()`, `$sleek.shutdown()`.
**User & session:** `$sleek.setUser()` (identify users).
**Events & binding:** `$sleek.on()` (listen to widget lifecycle events), `$sleek.rebind()` (re-register HTML triggers after DOM changes).

**Available views:** `home`, `feedback.add`, `feedback.{ID}`, `changelog`, `notifications`, `popup.update.{ID}`.

**HTML triggers (no-code data attributes):** `data-sleek` (opens home), `data-sleek-feedback`, `data-sleek-changelog`, `data-badge` (notification count).

**Configuration globals (set before the SDK loads):** `window.SLEEK_SETTINGS` (override widget settings), `window.SLEEK_COOKIE_DOMAIN` (share sessions across subdomains). The SDK prefers `localStorage`, falling back to cookies or in-memory storage.

---

## Installation & deployment options (from docs index)

- **Install the widget** (`/install/widget`) — single JavaScript snippet.
- **Custom domain / standalone portal** (`/install/standalone`).
- **Iframe / webview** (`/install/iframe`) — embed via a parameterized URL.
- **Canvas** — custom integrations for interactive admin experiences (secret-token auth).

## Gaps

- Public REST spec: **not published.** Base URL, exact paths, request bodies, pagination, rate limits, and error shapes are only in the **in-app reference** (Settings → Developer). The `https://api.sleekplan.com/v1/...` paths above are illustrative — verify before building.
- Webhook retry/backoff behavior: **not documented.**
- No documented Zapier integration as of this capture.
