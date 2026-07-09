<!-- Source: https://greenshiftwp.com/api-connector/ , https://greenshiftwp.com/documentation/blocks/query-addon-and-dynamic-blocks/ , https://greenshiftwp.com/documentation/greenshift-extra/dynamic-options/ , https://greenshiftwp.com/documentation/troubleshooting/ -->

# Greenshift Developer Reference — API Connector, Dynamic Data & WordPress surface

Greenshift is a WordPress plugin. It has **no hosted REST API** and **no native outbound webhook**. Its programmatic surface is:

1. **WordPress core** — the WP REST API (`/wp-json/wp/v2/...`), application-password auth, and WP-CLI. Greenshift block content lives in `post_content` as `greenshift-blocks/`-namespaced block markup (`GSPB`-prefixed CSS classes).
2. **The Greenshift API Connector** — a no-code consumer of *external* APIs (REST, Google Sheet/CSV, and LLM/AI APIs) that runs **server-side** (on the WP server) or **client-side** (browser `fetch`). This is the standout developer feature.
3. **Dynamic data / the Query addon** — repeatable WordPress data sources bound into blocks.
4. **The `GSPB_API_RESPONSE` client-side JS event.**

> Reproduced from Greenshift's public documentation. Confirm exact placeholder names, field paths, auth steps, and block attribute keys against your installed Greenshift version before relying on them — features evolve per release and most live in paid packs (GreenLight PRO for the API Connector).

## Authentication quick-start (WordPress core, not Greenshift-specific)

```bash
# Read a page's Greenshift block markup with an application password
curl -s https://example.com/wp-json/wp/v2/pages/123 \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" | jq '.content.rendered'
```

Generate an application password under **Users → Profile → Application Passwords**. The token inherits that user's capabilities. To write block markup, `POST`/`PUT` to `/wp-json/wp/v2/pages/{id}` with a `content` field containing `greenshift-blocks/`-namespaced block comments.

---

## API Connector

The API Connector enables WordPress blocks to connect with external APIs and display dynamic data using custom designs. It operates in two modes: **Server-Side** (processes on the WordPress server) and **Client-Side** (executes in the browser via the JavaScript `fetch` API).

### Server-Side API Connector

**Setup:** requires enabling **"Dynamic/Repeater Output"** in the Element block. Add API data and click fetch to retrieve and store information in blocks.

**Basic API examples** (for WordPress sites with the default REST API enabled):
- `https://site.com/wp-json/wp/v2/product?per_page=25` — retrieves 25 products
- `/wp-json/wp/v2/posts/25` — gets a specific post by ID

The system automatically converts JSON responses and retrieves featured images for posts.

**Data handling:**
- **Single Items** — enable the "Single Item" option when the API returns a non-array response.
- **Complex Arrays** — use the Response field with syntax like `field[subfield][0][subsub]`.
- **Test API** — a built-in panel validates API responses without dynamic placeholders.

**Dynamic placeholders (server-side)** — supported in link, body, and header fields:

| Placeholder | Function |
|---|---|
| `{{FORM:fieldname\|fallback}}` | Form input values |
| `{{INCREMENT:value}}` | Increases by the specified amount on each call |
| `{{RANDOM:0-100}}` | Random number between a range |
| `{{RANDOM:value1\|value2}}` | Random selection from options |
| `{{USER_META:field}}` | Current user metadata |

**AJAX loading options:**
- **Form Submit Trigger** — attach API calls to form submissions using selectors (e.g. `.submitform`).
- **Custom Interaction Trigger** — copy the connector ID and use it in Interaction Layers with custom triggers (click, scroll position, etc.).
- **Loop Trigger** — repeated API calls at a set interval (recommended **4–5s+ minimum** to avoid hammering the host).

**Pagination** — results containers automatically receive CSS classes: `.loading` while fetching; `.loaded` and `.active` after retrieval; `.result-loaded` for newly added items. Pagination works when the API uses a `page` parameter.

**WordPress authentication (for authenticated endpoints):**
1. Create an **Application Password** in the WordPress admin Profile page (distinct from the user password).
2. Format credentials as `UserName:Password`.
3. Base64-encode the string.
4. Add to the API header: `Authorization: Basic [encodedCode]` (include a space between `Basic` and the encoded value).

### Client-Side API Connector

Operates entirely in the browser using the JavaScript `fetch` API — no WordPress database connection. **Warning: "Client-side APIs are always public, so users can see your API keys."** Never place a secret key in a client-side connector.

**Dynamic placeholders (client-side):**

| Placeholder | Purpose |
|---|---|
| `{{TEXT:.selector}}` | Text content from any page element |
| `{{VALUE:.selector}}` | Form input field values |
| `{{COOKIE:name}}` | Cookie retrieval |
| `{{STORAGE:name}}` | Local/session storage values |
| `{{ATTR:attr\|selector}}` | Custom attribute values |
| `{{SESSION_ID}}` | Unique session identifier |
| `{{FORMDATA:.selector}}` | Send an entire form using the FormData API |

**Result template mapping** — two-block structure:
1. **Template Block** — a hidden block with static design elements that carry unique classes (also serve as fallback values).
2. **Result Container** — the visible block where results display.

Mapping rules: links automatically populate `href`; images/video automatically populate `src`; other elements receive text replacement. Array-like access is supported (e.g. `urls[small]` retrieves a nested value).

**Custom loader/animation:** add a unique class to a loader block; it receives the `.active` class during loading; trigger animation presets on the `.active` condition.

### Chat and Streaming (client-side)

**Chat mode** maintains conversation context by appending new messages to previous requests — useful for AI model interactions requiring message history. Configuration requires:
- An initial body with a system role.
- An **"Append Field"** identifying the array that stores messages (e.g. `messages`).
- A user-message JSON format with the `{{VALUE}}` placeholder.
- An assistant-message format with the `{{RESPONSE}}` placeholder.
- A **response extraction field** (e.g. `choices[0][message]` for OpenAI).

**Streaming** delivers responses chunk-by-chunk without waiting for the complete answer. Elements receive `loading` before data arrives, then `loaded` and `active` when retrieved.

### API presets

- **WordPress Site Latest Items** — generates REST endpoints for external WordPress sites; select a post type to retrieve.
- **Google Sheet / CSV** — converts spreadsheet/CSV data into an API source; configurable row or column orientation.

### Developer hook (client-side JS event)

```javascript
document.addEventListener("GSPB_API_RESPONSE", (event) => {
    const { resultElem, responseData } = event.detail;
    // run custom code on the API Connector response
});
```

### Authentication note

For write operations (posting data), WordPress requires **Application Passwords** — distinct from user login credentials — encoded in Basic-Authentication headers.

---

## Query addon and dynamic blocks

The Query addon supplies Greenshift's dynamic-data features: "dynamic blocks allow you to use dynamic data which is different for different pages." It can be purchased separately or comes included in the Design/SEO and All-in-One plans.

### Supported data sources (Repeater Builder)

- Post types
- Users
- Taxonomies
- Comments
- Custom repeater fields (from plugins like **ACF, ACPT, MetaFields**)
- **External repeaters**
- Options data

### Available dynamic blocks

| Block | Purpose |
|---|---|
| Dynamic FAQ | Custom meta/taxonomy support via repeater fields |
| Dynamic Chart | Apex Chart integration with 20+ presets |
| Filter Block | Multiple filter types (checkboxes, radio, select, range slider) |
| Dynamic Search | Custom-designed search results |
| Comment Query Builder | Comment-specific queries with author/post data |
| User Grid/List Builder | User data display and author boxes |
| Taxonomy Repeater | Taxonomy term listings |
| Breadcrumbs | Post-hierarchy navigation |
| Gallery / 360 Gallery | Image grids with styling options |

### Dynamic options / API Connector data sources

Beyond post types, many other dynamic, repeatable WordPress data sources can be retrieved: **options, users, taxonomies, comments, repeater fields from extra plugins, and even external repeaters.** The server-side API Connector can use the offset parameter in a WordPress REST API link — e.g. `https://woocommerce.greenshiftwp.com/wp-json/wp/v2/product?per_page=1&offset=1`. Use `{{INCREMENT:1}}` to increase `offset` by 1 on each sequential call (retrieve items individually rather than all at once). Functional placeholders like `{{RANDOM:0-100}}` generate a random value in range, and `{{RANDOM:blue|grey|yellow}}` picks one provided value per call.

---

## Block markup namespace

Greenshift blocks are stored in `post_content` under the **`greenshift-blocks/`** namespace, with `GSPB`-prefixed CSS classes/IDs. Block names and attribute keys evolve per release — **copy a real block from the editor as the source of truth** rather than hand-authoring from memory.

```html
<!-- wp:greenshift-blocks/element {"id":"gsbp-abc123","tag":"div"} -->
<div id="gspb_container-id-gsbp-abc123" class="gspb_container"> ... </div>
<!-- /wp:greenshift-blocks/element -->
```

---

## Gaps / not documented

- **No public hosted REST API** for Greenshift objects — use the WordPress core REST API against posts/pages, whose `content` holds the `greenshift-blocks/` block markup.
- **No native outbound webhook and no core form block** — lead delivery rides on a paired form plugin, or POST from the client/server API Connector to your own endpoint.
- **No first-party Zapier/Make app** for Greenshift itself.
- The **API Connector, dynamic fields, and Query addon are paid** (GreenLight PRO / Design / All-in-One). The free WordPress.org plugin does not include them.
- Exact placeholder lists, response-field path syntax, chat/streaming config keys, and `greenshift-blocks/*` attribute schemas evolve per release. Confirm against greenshiftwp.com/documentation and the installed version. Public code for the AI tooling: github.com/wpsoul/greenshift-ai-lab.
