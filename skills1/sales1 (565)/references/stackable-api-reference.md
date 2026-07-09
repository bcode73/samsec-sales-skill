<!-- Source: https://github.com/gambitph/Stackable (GPLv3 source + README), https://docs.wpstackable.com/ (Customizing Blocks, Advanced Features), and https://wordpress.org/plugins/stackable-ultimate-gutenberg-blocks/ -->

# Stackable Developer Reference — Hooks & the WordPress REST surface

Stackable is a WordPress plugin. It has **no hosted REST API** and **no native outbound webhook**. Its programmatic surface is:

1. **WordPress core** — the WP REST API (`/wp-json/wp/v2/...`), Application-Password auth, and WP-CLI. Stackable block content lives in the `post_content` field as `stackable/`-namespaced block markup.
2. **A small set of Stackable PHP filters** plus the WordPress core block filters (`render_block`, `render_block_data`).
3. **The source code** — Stackable is **GPLv3** and open source (`github.com/gambitph/Stackable`); deeper extension means forking and building it.

> Only `stackable_force_css_load` is documented verbatim in Stackable's public docs at the time of research. The other entries below are WordPress **core** hooks that apply to any block plugin, not Stackable-specific inventions. Confirm any additional `stackable_*` hooks against the installed version's source (search the repo for `apply_filters(` / `do_action(`) before relying on them — do not assume undocumented hooks exist.

## Authentication quick-start (WordPress core, not Stackable-specific)

```bash
# Read a page's Stackable block markup with an application password
curl -s https://example.com/wp-json/wp/v2/pages/123 \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" | jq '.content.rendered'
```

Generate an application password under **Users → Profile → Application Passwords**. The token inherits that user's capabilities. There is no Stackable-specific endpoint — operate on the WordPress posts/pages whose `content` holds the `stackable/` block markup.

## Stackable-specific filter (documented)

| Hook | Type | Purpose |
|---|---|---|
| `stackable_force_css_load` | Filter | Return `true` to always enqueue Stackable's frontend CSS, even on pages where Stackable doesn't detect its blocks (e.g. dynamically-injected markup via shortcode/REST/another builder). Default behavior loads CSS only on pages that contain Stackable blocks. |

```php
// Always load Stackable's frontend CSS
add_filter( 'stackable_force_css_load', '__return_true' );

// Or scope it to specific contexts to keep the optimization elsewhere
add_filter( 'stackable_force_css_load', function ( $force ) {
    return is_singular( 'landing_page' ) ? true : $force;
} );
```

## WordPress core block filters Stackable output flows through

These are WordPress core hooks (not Stackable-owned), useful for modifying or branching on Stackable blocks by their `stackable/` block name.

| Hook | Type | Purpose |
|---|---|---|
| `render_block` | Filter | Modify a block's rendered HTML at output time. Signature: `( string $block_content, array $block )`; branch on `$block['blockName']` (e.g. `stackable/card`, `stackable/hero`). |
| `render_block_data` | Filter | Modify a parsed block's data before it renders. |
| `block_categories_all` | Filter | Modify the block categories shown in the editor. |

```php
// Append a tracking attribute to every Stackable Card block on the frontend
add_filter( 'render_block', function ( $block_content, $block ) {
    if ( ( $block['blockName'] ?? '' ) === 'stackable/card' ) {
        $block_content = str_replace( '<div ', '<div data-track="card" ', $block_content );
    }
    return $block_content;
}, 10, 2 );
```

## Block namespace & markup

Stackable blocks are registered under the **`stackable/`** namespace and stored in `post_content` as standard Gutenberg block comments. Observed shape:

```html
<!-- wp:stackable/hero {"uniqueId":"hero1","version":"3"} -->
<div class="stk-block stk-block-hero wp-block-stackable-hero stk-hero1"> ... </div>
<!-- /wp:stackable/hero -->
```

- Attributes commonly include `uniqueId` (the per-block id used in generated CSS class names like `stk-<uniqueId>`) and `version` (the block version, central to the v2→v3 migration). **Verify exact attribute keys against a live install** — copy real block markup from the editor rather than hand-authoring it.
- v2 blocks are loaded as **separate blocks**; whether they load is controlled in **Settings → Other Settings → Migration** (load v2 blocks for existing posts / allow both v2+v3 / v3-only).

## Reading/writing Stackable pages via the WordPress REST API

```bash
# Create a page whose body is Stackable block markup
curl -s -X POST https://example.com/wp-json/wp/v2/pages \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" \
  -H "Content-Type: application/json" \
  -d '{"title":"Launch","status":"publish","content":"<!-- wp:stackable/hero {\"uniqueId\":\"hero1\"} -->...<!-- /wp:stackable/hero -->"}'
```

```python
import requests
from requests.auth import HTTPBasicAuth

WP = "https://example.com/wp-json/wp/v2"
AUTH = HTTPBasicAuth("admin", "xxxx xxxx xxxx xxxx xxxx xxxx")

# Update an existing page's Stackable markup
page_id = 123
markup = '<!-- wp:stackable/card {"uniqueId":"card1"} -->...<!-- /wp:stackable/card -->'
r = requests.post(f"{WP}/pages/{page_id}", auth=AUTH, json={"content": markup})
r.raise_for_status()
print(r.json()["link"])
```

## Building/extending from source

```bash
# From the Stackable GitHub repo (GPLv3)
# 1. Clone into wp-content/plugins of a local WP dev site
# 2. Install dependencies
npm install
# 3. Activate Stackable in the local site, then watch for changes
npm run start
```

Tech stack per the repo: JavaScript (~60%), PHP (~34%), SCSS (~6%).

## Gaps / not documented

- **No public hosted REST API** for Stackable objects — use the WordPress core REST API against posts/pages, whose `content` holds the `stackable/` block markup.
- **No native outbound webhook** and **no form block** — lead delivery rides on a separate form/ESP plugin, not Stackable.
- **No first-party Zapier/Make app** for Stackable itself.
- **Documented public hook list is minimal** — only `stackable_force_css_load` is documented verbatim. Additional `stackable_*` hooks (if any) must be confirmed in the GPLv3 source for your installed version; do not assume undocumented hooks. Source: `github.com/gambitph/Stackable`, `docs.wpstackable.com`, WordPress.org plugin page.
