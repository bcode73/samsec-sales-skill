<!-- Source: https://wordpress.org/plugins/gutenkit-blocks-addon/, https://wpgutenkit.com/, https://wpmet.com/doc/ (GutenKit docs: Dynamic Content, Query Builder, child blocks), https://developer.wordpress.org/rest-api/ -->

# GutenKit Developer / API Reference

**GutenKit has NO hosted REST API and NO outbound webhook.** It is a WordPress plugin by Wpmet (slug `gutenkit-blocks-addon`). The programmatic surface is:

1. The **WordPress core REST API** — read/write `gutenkit/`-namespaced block markup in `post_content`, and read the posts a Query Loop block renders.
2. **WordPress core hooks/filters** — alter rendered block output (`render_block`) or hook standard WP actions; GutenKit ships no public SDK or documented action/filter set.
3. The **Mailchimp opt-in block** — GutenKit's only native lead-capture surface; routing happens on the Mailchimp side, not GutenKit's.

Treat anything below marked *Constructed* as representative and verify against the live install before relying on it.

---

## 1. Auth quick-start (WordPress core REST API)

GutenKit pages/posts are managed through WordPress's own REST API. Authenticate with an **Application Password** (WordPress 5.6+: Users → Profile → Application Passwords), sent as HTTP Basic over HTTPS.

Simplest authenticated GET (current user — verifies auth works):
```bash
curl -s "https://example.com/wp-json/wp/v2/users/me" \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx"
```

Base URL: `https://<your-site>/wp-json/wp/v2/`
Auth header (equivalent): `Authorization: Basic base64(user:app_password)`

---

## 2. Top endpoints (WordPress core, used for GutenKit content)

| Action | Method | Path | Notes |
|---|---|---|---|
| List pages | GET | `/wp/v2/pages` | `?per_page=100&page=2`; read `X-WP-Total`, `X-WP-TotalPages` |
| Get a page (editable) | GET | `/wp/v2/pages/{id}?context=edit` | returns `content.raw` (block markup) — requires edit cap |
| Create a page | POST | `/wp/v2/pages` | body `{ "title": "...", "content": "<!-- wp:gutenkit/... -->", "status": "draft" }` |
| Update a page | POST | `/wp/v2/pages/{id}` | body `{ "content": "<updated block markup>" }` |
| Delete a page | DELETE | `/wp/v2/pages/{id}?force=true` | `force=true` skips trash |
| List posts a Query Loop renders | GET | `/wp/v2/posts` | mirror the loop's filters: `?categories=`, `?tags=`, `?orderby=`, `?order=` |

### Example: GET a page (editable context)
Request:
```bash
curl -s "https://example.com/wp-json/wp/v2/pages/482?context=edit" \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx"
```
Response (truncated):
```json
{
  "id": 482,
  "status": "publish",
  "type": "page",
  "link": "https://example.com/landing/",
  "title": { "raw": "Landing", "rendered": "Landing" },
  "content": {
    "raw": "<!-- wp:gutenkit/container {\"blockId\":\"gkit-Xy90\"} -->\n<div class=\"wp-block-gutenkit-container gutenkit-element gkit-Xy90\">...</div>\n<!-- /wp:gutenkit/container -->",
    "rendered": "<div class=\"wp-block-gutenkit-container gutenkit-element gkit-Xy90\">...</div>",
    "protected": false
  }
}
```
<!-- Constructed from the WordPress core REST API page schema + observed Gutenberg block markup — verify the gutenkit/ namespace and the blockId attribute against the live API. -->

### Example: CREATE a page with a GutenKit block
```bash
curl -s -X POST "https://example.com/wp-json/wp/v2/pages" \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "API Test",
    "status": "draft",
    "content": "<!-- wp:gutenkit/heading {\"blockId\":\"gkit-h1\"} --><h2 class=\"wp-block-gutenkit-heading gutenkit-element gkit-h1\">Hello</h2><!-- /wp:gutenkit/heading -->"
  }'
```

### Example: UPDATE (bulk string swap pattern)
```python
import requests
from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth("admin", "xxxx xxxx xxxx xxxx xxxx xxxx")
site = "https://example.com"
pid = 482
raw = requests.get(f"{site}/wp-json/wp/v2/pages/{pid}",
                   params={"context": "edit"}, auth=auth).json()["content"]["raw"]
requests.post(f"{site}/wp-json/wp/v2/pages/{pid}",
              json={"content": raw.replace("Get Started", "Start Free Trial")},
              auth=auth).raise_for_status()
```

### Example: DELETE
```bash
curl -s -X DELETE "https://example.com/wp-json/wp/v2/pages/482?force=true" \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx"
```

---

## 3. Pagination

WordPress core uses **page-number pagination**:
- `?per_page=<1-100>&page=<n>`
- Response headers: `X-WP-Total` (total items), `X-WP-TotalPages` (total pages).
- Loop until `page > X-WP-TotalPages`.

```python
import requests
from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth("admin", "xxxx ...")
site, page, out = "https://example.com", 1, []
while True:
    r = requests.get(f"{site}/wp-json/wp/v2/pages",
                     params={"per_page": 100, "page": page, "context": "edit"}, auth=auth)
    if r.status_code == 400:  # past the last page
        break
    out += r.json()
    if page >= int(r.headers.get("X-WP-TotalPages", 1)):
        break
    page += 1
```

---

## 4. Error response shape

WordPress core REST errors are JSON with a `code`, `message`, and `data.status`:
```json
{
  "code": "rest_cannot_edit",
  "message": "Sorry, you are not allowed to edit this post.",
  "data": { "status": 403 }
}
```
Common: `401 rest_not_logged_in` (bad/missing app password), `403 rest_cannot_edit` (insufficient cap or `context=edit` without auth), `404 rest_post_invalid_id`.

---

## 5. Rate limits & retry

WordPress core has **no built-in REST rate limit** — limits come from your host/CDN/security plugin (often surfaced as `429` or a `Retry-After` header). Strategy:
- Honor `Retry-After` when present; otherwise exponential backoff (1s, 2s, 4s…).
- Throttle bulk writes (e.g. ≤2–5 req/s) to avoid host WAF throttling.
```python
import time, requests
def get(url, auth, tries=5):
    for i in range(tries):
        r = requests.get(url, auth=auth)
        if r.status_code != 429:
            return r
        time.sleep(int(r.headers.get("Retry-After", 2 ** i)))
    r.raise_for_status()
```

---

## 6. Extending GutenKit (no SDK — use WordPress core)

GutenKit publishes no documented action/filter API. Extend via WordPress core mechanisms against the rendered block output:

```php
// Post-process GutenKit's rendered HTML (runs for every block)
add_filter( 'render_block', function ( $html, $block ) {
    if ( isset( $block['blockName'] ) && str_starts_with( $block['blockName'], 'gutenkit/' ) ) {
        // mutate $html for gutenkit/* blocks here
    }
    return $html;
}, 10, 2 );
```
<!-- Constructed: render_block is a WordPress core filter; the gutenkit/ block-name prefix is representative — confirm exact block names by inspecting saved markup or the plugin's block.json files. -->

For editor-side or asset behavior, the realistic levers are core WordPress hooks (`enqueue_block_assets`, `wp_enqueue_scripts`) and standard dequeue/allowlist patterns in your minify/optimization plugin — there is no GutenKit-specific config API.

---

## 7. Dynamic Content & Query Loop (Pro) — what they read

GutenKit's **Dynamic Content** module binds block text/links/images to WordPress data sources: post fields (title, excerpt, featured image, permalink), site fields (title, tagline), author/user fields, and **custom fields** (ACF-style meta). The **Query Loop Builder** filters posts by post type, taxonomy, meta query, date query, author, and post status, then renders a chosen block template per item.

Neither exposes a GutenKit endpoint — both operate on WordPress data. To read the same data programmatically:
- Post/meta fields → `/wp/v2/{post_type}/{id}` (meta requires the field to be `show_in_rest` registered, or read via `context=edit`).
- The posts a Query Loop renders → reproduce its filters as `/wp/v2/{post_type}` query params (see Recipe 3 in `platform-guide.md`).

## Gaps

- **No hosted GutenKit REST API / outbound webhook / Zapier app** — confirmed; all programmatic access is via WordPress core.
- **`gutenkit/` block namespace and attribute names** (e.g. `blockId`) are representative — read a block's `block.json` / inspect saved markup for the exact namespace and attribute schema per block before relying on string transforms.
- **No documented GutenKit action/filter API** — extension is via WordPress core hooks against rendered output.
- **Exact Pro pricing, site counts, and free-vs-Pro block counts** vary across sources — verify on wpgutenkit.com/pricing and the live WordPress.org listing.
- **No GitHub org located** for Wpmet at the time of research (the `wpmet` org 404'd) — source distribution is the WordPress.org repository.
