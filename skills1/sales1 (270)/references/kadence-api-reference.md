<!-- Source: https://github.com/stellarwp/kadence-blocks ; https://www.liquidweb.com/help-docs/software/kadence/blocks/form-integrations/webhooks-2/ ; https://www.kadencewp.com/support-forums/ (filter names from Kadence docs/changelog + WP Webhooks integration listing) -->

# Kadence Blocks — Developer / Automation Reference

**There is no hosted, outbound REST API for Kadence Blocks.** It is a WordPress plugin (GPLv2, `github.com/stellarwp/kadence-blocks`). The programmatic surface is:

1. The **WordPress core REST API** over the post/page that stores the blocks.
2. **PHP hooks/filters** the plugin exposes.
3. The **Advanced Form webhook** (Pro) — the only outbound push.

This file documents all three. Pricing/plan gates are in `platform-guide.md`.

---

## 1. WordPress REST API on block content

Kadence blocks are stored as block-comment markup inside `post_content`, namespaced `kadence/` (e.g. `kadence/rowlayout`, `kadence/advancedbtn`, `kadence/advancedform`). There is no separate "blocks" endpoint — you read/write the **post**.

**Auth:** WordPress **Application Passwords** (Users → Profile → Application Passwords) over HTTPS, sent as HTTP Basic.

**Read raw markup (simplest authenticated GET):**
```bash
curl -s "https://example.com/wp-json/wp/v2/pages/42?context=edit" \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" | jq -r '.content.raw'
```

Response (truncated):
```json
{
  "id": 42,
  "slug": "landing",
  "status": "publish",
  "content": {
    "raw": "<!-- wp:kadence/rowlayout {\"uniqueID\":\"123_abc\"} -->…<!-- /wp:kadence/rowlayout -->",
    "rendered": "<div class=\"wp-block-kadence-rowlayout\" …>…</div>",
    "protected": false
  }
}
```

**Update markup:**
```bash
curl -s -X POST "https://example.com/wp-json/wp/v2/pages/42" \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" \
  -H "Content-Type: application/json" \
  -d '{"content":"<!-- wp:kadence/rowlayout {\"uniqueID\":\"123_abc\"} -->…<!-- /wp:kadence/rowlayout -->"}'
```

**Pagination (listing posts/pages):** WordPress uses `page` + `per_page` (max 100) query params; total counts come back in `X-WP-Total` / `X-WP-TotalPages` response headers.

```bash
curl -sD - "https://example.com/wp-json/wp/v2/pages?per_page=100&page=2&context=edit" \
  -u "admin:APP_PASSWORD" -o /dev/null | grep -i x-wp-total
```

**Error shape (WordPress core):**
```json
{ "code": "rest_post_invalid_id", "message": "Invalid post ID.", "data": { "status": 404 } }
```

> ⚠️ You are editing **raw block markup**. Preserve every `<!-- wp:kadence/... -->` / `<!-- /wp:kadence/... -->` delimiter and the `uniqueID` attribute, or the block will show "this block contains unexpected or invalid content" in the editor.

---

## 2. Public hooks & filters

Verified filter names from Kadence documentation, support forums, and the changelog. Exact callback arity may vary by version — **verify on staging**.

| Filter | Purpose |
|---|---|
| `kadence_blocks_posts_query_args` | Modify the `WP_Query` args of the **free Posts block**. Args: `( $query_args, $attributes )`. |
| `kadence_blocks_pro_query_loop_query_vars` | Customize query vars (`meta_key`, `meta_value`, `post_type`, `comment_count`, …) of the **Pro Advanced Query Loop** block. |
| `kadence_element_display` | Runs every time Kadence decides whether to show a **Hooked Element** — return a boolean for dynamic/conditional display (Kadence Theme/Elements). |
| `kadence_blocks_table_data_scope_attributes` | Customize table header-cell `scope` attributes (added v3.7.3). |
| Custom-fonts filter | Register/label custom fonts (referenced around v3.5.19). |

**Posts block query example:**
```php
add_filter( 'kadence_blocks_posts_query_args', function ( $query_args, $attributes ) {
    $query_args['meta_key']   = 'featured';
    $query_args['meta_value'] = '1';
    return $query_args;
}, 10, 2 );
```

**Advanced Query Loop (Pro) example:**
```php
add_filter( 'kadence_blocks_pro_query_loop_query_vars', function ( $query_vars, $attributes ) {
    $query_vars['post_type'] = 'product';
    return $query_vars;
}, 10, 2 );
```

> Finding more hooks: search your theme/plugin files for `do_action(` and `apply_filters(`. Kadence Theme action hooks/filters live under `/wp-content/themes/kadence/`. These are advanced and developer-intended — run on a staging site.

---

## 3. Advanced Form webhook (Pro — the only outbound push)

**Requires Kadence Blocks Pro** installed and activated. Both **Kadence Form** and **Kadence Form (Adv)** support webhooks.

**Enable it:**
- *Kadence Form*: add a Form block → form settings → **Actions After Submit** → check **WebHook**.
- *Kadence Form (Adv)*: add a Form (Adv) block → **Submit Actions** → search for and add **WebHook**.

A **Webhook Settings** section then appears (identical for both form types):
- **Webhook URL** — the endpoint your webhook service provides, where submission data is POSTed.
- **Map Fields** — lists every form field so you can map it to the payload key name your receiver expects.

**Payload:** a flat JSON/form-encoded map of your **mapped field names → submitted values** (you control the keys via Map Fields):
```json
{ "email": "jane@example.com", "name": "Jane Doe", "message": "Interested in a demo" }
```
<!-- Constructed from documented behavior — verify against a live test submission -->

**Finding the form id** (used in markup / third-party automators): inspect the published page's HTML and search for `kadence-form-` — the suffix is the form id.

**Testing:** generate a temporary URL at a service like Webhook Tester (webhook-test.com), paste it as the **Webhook URL**, submit a test entry, and inspect what arrived.

**Third-party automators:** WP Webhooks, FlowMattic, and Bit Integrations expose a `kdbl_submit` trigger ("fires once a form was submitted within Kadence Blocks") to route submissions into Zapier/Make/etc. without code.

> No documented signature/HMAC header or delivery log/retry on the native webhook. Make your consumer **idempotent** (dedupe on email + submission time) and validate every field server-side — treat the payload as untrusted user input.

---

## 4. AI & design library

- **Kadence AI** (Pro, "Creative Kit") generates editable block sections from a prompt inside the editor — output is normal `kadence/` block markup, not a separate API.
- **Design Library / Kadence Cloud** syncs reusable patterns/sections into the editor; managed in the UI, no public endpoint.

## Gaps

- No public OpenAPI/Swagger spec, Postman collection, or hosted REST endpoints — the plugin doesn't ship one (confirmed: it's a WordPress plugin).
- Exact filter callback signatures and any version-gated additions should be confirmed against the installed version's source under `/wp-content/plugins/kadence-blocks/` and `/wp-content/plugins/kadence-blocks-pro/`.
- The Advanced Form webhook payload's exact content-type and any envelope fields weren't captured verbatim — test a live submission before building a strict parser.
