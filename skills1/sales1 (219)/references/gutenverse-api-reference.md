<!-- Source: https://github.com/Jegstudio/gutenverse-core (README), https://github.com/Jegstudio/gutenverse, https://wordpress.org/plugins/gutenverse/, https://developer.wordpress.org/rest-api/ -->

# Gutenverse Developer / API Reference

**Gutenverse has NO hosted REST API and NO outbound webhook.** It is a WordPress plugin (open source under `github.com/Jegstudio`). The programmatic surface is:

1. The **WordPress core REST API** — read/write `gutenverse/`-namespaced block markup in `post_content`.
2. The **`gutenverse-core` framework** — PHP action/filter hooks and a JS package/store system for extending the editor.
3. **Gutenverse Form** entries — stored in the WordPress database, exportable as CSV (no documented public entries API in the free plugin).

Treat anything below marked *Constructed* as representative and verify against the live install before relying on it.

---

## 1. Auth quick-start (WordPress core REST API)

Gutenverse pages/posts are managed through WordPress's own REST API. Authenticate with an **Application Password** (WordPress 5.6+: Users → Profile → Application Passwords), sent as HTTP Basic over HTTPS.

Simplest authenticated GET (current user — verifies auth works):
```bash
curl -s "https://example.com/wp-json/wp/v2/users/me" \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx"
```

Base URL: `https://<your-site>/wp-json/wp/v2/`
Auth header (equivalent): `Authorization: Basic base64(user:app_password)`

---

## 2. Top endpoints (WordPress core, used for Gutenverse content)

| Action | Method | Path | Notes |
|---|---|---|---|
| List pages | GET | `/wp/v2/pages` | `?per_page=100&page=2`; read `X-WP-Total`, `X-WP-TotalPages` |
| Get a page (editable) | GET | `/wp/v2/pages/{id}?context=edit` | returns `content.raw` (block markup) — requires edit cap |
| Create a page | POST | `/wp/v2/pages` | body `{ "title": "...", "content": "<!-- wp:gutenverse/... -->", "status": "draft" }` |
| Update a page | POST | `/wp/v2/pages/{id}` | body `{ "content": "<updated block markup>" }` |
| Delete a page | DELETE | `/wp/v2/pages/{id}?force=true` | `force=true` skips trash |

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
    "raw": "<!-- wp:gutenverse/section {\"elementId\":\"guten-Xy90\"} -->\n<section class=\"wp-block-gutenverse-section guten-element guten-Xy90\">...</section>\n<!-- /wp:gutenverse/section -->",
    "rendered": "<section class=\"wp-block-gutenverse-section guten-element guten-Xy90\">...</section>",
    "protected": false
  }
}
```
<!-- Constructed from the WordPress core REST API page schema + observed Gutenverse block markup — verify against the live API. -->

### Example: CREATE a page with a Gutenverse block
```bash
curl -s -X POST "https://example.com/wp-json/wp/v2/pages" \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "API Test",
    "status": "draft",
    "content": "<!-- wp:gutenverse/heading {\"elementId\":\"guten-h1\"} --><h2 class=\"wp-block-gutenverse-heading guten-element guten-h1\">Hello</h2><!-- /wp:gutenverse/heading -->"
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

## 6. `gutenverse-core` framework (extend the editor)

From the `gutenverse-core` README — the developer framework that powers Gutenverse blocks.

**Build:** install deps in `gutenverse-core` root, then `npm start` (dev) / `npm run build` (prod). Environment: **Node v14.20.1, npm 6.14.17**.

**PHP hooks (confirmed in README):**
- `do_action( 'gutenverse_after_init_framework' )` — fires after the framework initializes; enqueue scripts/styles here.
- `do_action( 'gutenverse_include_block', $block )` — fires as a block is included/enqueued.
- `apply_filters( 'gutenverse_block_config', $config )` — inject additional configuration into the editor.
- Dedicated action hooks exist for adding supplementary **column** and **section** styles.

```php
add_action( 'gutenverse_after_init_framework', 'my_enqueue' );
add_filter( 'gutenverse_block_config', function ( $c ) { $c['flag'] = true; return $c; } );
```

**JS packages (≈21):** accessible via ES6 imports or the `gutenverseCore.*` window object — e.g. `gutenverseCore.animation`, plus packages for assets, backend, dashboard, data, and routing. A **Redux-style store** manages block lists, global styling variables, library data, and routing state (select/dispatch). A routing system with components, HOCs, helpers, and request handlers supports custom dashboard UIs.

<!-- Hook names/signatures are from the gutenverse-core README; confirm against the installed version before relying on them. -->

---

## 7. Gutenverse Form (entries)

The **Gutenverse Form** plugin (separate free install) provides 15+ form-field blocks. Behavior:
- **Storage:** submissions stored in WordPress; **CSV export** from the admin.
- **Notifications:** admin email + user email notifications.
- **Anti-spam:** reCAPTCHA block (connects to Google's verification service). A third-party Cloudflare **Turnstile-for-Gutenverse-forms** add-on exists for forms with the `.guten-form-builder` class.
- **Validation:** required-field + type validation (email/phone/number/date).
- **Free tier does NOT include:** webhooks, Zapier/Mailchimp/CRM integrations, conditional logic, multi-step forms, or payment fields — these are Pro.

There is no documented public REST endpoint for form entries in the free plugin; integrate by exporting CSV or querying the WordPress side directly.

## Gaps

- **No hosted Gutenverse REST API / outbound webhook / Zapier app** — confirmed; all programmatic access is via WordPress core.
- **`gutenverse/` block attribute names** (e.g. `elementId`) are representative; read a block's `block.json` / inspect saved markup for the exact attribute schema per block.
- **Gutenverse Form entries API** — not documented publicly; treat CSV export / WP DB as the integration path until/unless a Pro endpoint is confirmed.
- **Exact Pro pricing/site counts** vary across sources — verify on gutenverse.com/pricing.
