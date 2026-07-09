<!-- Source: https://nexterwp.com/nexter-abilities/ (Nexter Abilities / MCP), https://nexterwp.com/docs/ (docs portal), https://github.com/posimyth/the-plus-addons-for-block-editor (GPLv3 source), and https://wordpress.org/plugins/the-plus-addons-for-block-editor/ — captured 2026-06-29. Nexter has no hosted REST API; the developer surface is the MCP server + WordPress core + PHP option/filter flags. -->

# Nexter Developer Reference — Nexter Abilities (MCP), the WordPress REST surface & option flags

Nexter is a WordPress plugin. It has **no hosted REST API** and **no native outbound webhook**. Its programmatic surface is:

1. **Nexter Abilities** — a built-in **MCP (Model Context Protocol) server** that exposes 115 server-side tools so AI assistants compose Nexter Gutenberg blocks.
2. **WordPress core** — the WP REST API (`/wp-json/wp/v2/...`), Application-Password auth, and WP-CLI. Nexter block content lives in the `post_content` field as **`tpgb/`-namespaced** block markup.
3. **PHP option/filter flags** — performance and load-option flags (e.g. `default_tpgb_load_opt`, `tpgb_defer_css_js`, `tpgb_delay_css_js`) stored in `wp_options`.
4. **The source code** — Nexter Blocks is **GPLv3** and open source (`github.com/posimyth/the-plus-addons-for-block-editor`); deeper extension means forking and building it.

> Caveats: The **`tpgb/`** block namespace and the option-flag names are **observed/inferred** (consistent with Nexter's `tpgb_*` option flags and the legacy "The Plus Addons" name) — not confirmed verbatim in public developer docs. The MCP **config snippet/endpoint path and token** are **generated per-site in WP admin** and were not captured verbatim. Confirm all of these against your installed version before relying on them. Do not invent additional hook names.

---

## 1. Nexter Abilities — the MCP server

**What it is (verbatim from nexterwp.com/nexter-abilities):** *"115 server-side tools that compose real Nexter Blocks from a single prompt, screenshot, or URL."* The AI calls block-add abilities to compose headings, containers, pricing tables, testimonials, forms, and more — *"Every attribute editable afterwards in Gutenberg."*

### Ability inventory (115 total)

| Group | Count | Examples |
|---|---|---|
| **Free blocks** | ~58–68 | Containers/layout, headings/paragraphs/buttons, **Forms (9 field types)**, post-listing & dynamic content |
| **Pro blocks** | ~43–47 | CTA banners, process steps, timeline, repeater, accordion-inner, **Popup builder**, **Mailchimp**, **Lottie**, **Spline 3D**, scroll sequence |
| **Workflow skills** | 8 | Performance & Core Web Vitals enforcement, typography/font-weight standardization, image-to-page translator, documentation post builder |
| **Button Preset CRUD** | 5 | List, create, update/rename, delete (with fallback handling) presets |
| **Page Inspection** | 1 | Extract Google Fonts, color palettes, images, video embeds, and heading hierarchy from a live URL |

Headline split: **68 free abilities / 47 Pro abilities** (plus the workflow/CRUD/inspection tools above). *"If your AI workspace supports MCP, it can call every ability Nexter ships."*

### Connected AI clients (any MCP-compatible client)

Claude Desktop · Cursor · VS Code · Windsurf · Cline · Zed · Continue.

### Setup (5 steps, verbatim flow)

1. **Install WordPress MCP Plugin** — deploy Nexter Blocks (includes the MCP endpoint and all 115 abilities).
2. **Connect Nexter** — authenticate your Nexter Blocks account.
3. **Enable Permissions** — configure MCP access settings and resource scoping.
4. **Add MCP Configuration** — copy the generated snippet into your AI assistant.
5. **Start Automation** — build through AI workflows.

### Authentication & scoping (verbatim)

- **Token-based authentication** — *"The MCP endpoint is authenticated with a token you generate, scoped to the post types and abilities you allow."*
- **Granular scoping** — control which post types and abilities the AI can access.
- **WordPress capability checks** — every call respects user permissions.
- **Toggle capability** — disable the MCP endpoint anytime; existing pages remain intact.

### Performance & consistency guarantees (verbatim)

- **Performance enforcement:** *"Every build starts with a page-type budget: image weight ceilings, font-family caps, animation limits that the AI must plan within before placing a single block."*
- **Typography control:** font-weight and text-decoration are top-level parameters on all typography-bearing blocks.
- **Global Button Presets:** single source of truth — change a preset once and every consuming block updates.
- **URL & screenshot recreation:** the inspect-page ability extracts real assets from a URL; the image-to-page skill translates a mockup into matching block structure.

### Architecture note

Per the Nexter Abilities page, this is a **custom MCP server architecture** — it does **not** use WordPress's native Abilities API framework (contrast with SeedProd, which exposes its actions through the WordPress Abilities API). A clean Markdown version of the abilities page is published at `https://nexterwp.com/nexter-abilities.md`.

### Illustrative MCP client config

```jsonc
// ILLUSTRATIVE ONLY — Nexter generates the exact URL + scoped token per-site in WP admin.
// Verify the real endpoint path and auth header shape against your install.
{
  "mcpServers": {
    "nexter": {
      "url": "https://example.com/wp-json/nexter/mcp",
      "headers": { "Authorization": "Bearer <SCOPED_TOKEN>" }
    }
  }
}
```

---

## 2. WordPress core REST surface (not Nexter-specific)

There is no Nexter-specific record endpoint — operate on the WordPress posts/pages whose `content` holds the `tpgb/` block markup.

```bash
# Read a page's Nexter block markup with an application password
curl -s https://example.com/wp-json/wp/v2/pages/123 \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" | jq '.content.rendered'
```

Generate an application password under **Users → Profile → Application Passwords**. The token inherits that user's capabilities.

### Block namespace & markup

Nexter blocks are stored in `post_content` as standard Gutenberg block comments. Observed/inferred namespace: **`tpgb/`** (The Plus Gutenberg Blocks — consistent with the `tpgb_*` option flags).

```html
<!-- wp:tpgb/heading {"blockId":"tpgb-abc123"} -->
<div class="wp-block-tpgb-heading tpgb-abc123"> ... </div>
<!-- /wp:tpgb/heading -->
```

- **Verify the exact namespace and attribute keys against a live install** — copy real block markup from the editor rather than hand-authoring it.
- In **v4.7.0**, all blocks were converted to WordPress **ApiVersion 3** (*"better performance, stability, and alignment with latest WordPress standards"*). Treat that release as a migration boundary.

### Reading/writing Nexter pages via the WordPress REST API

```python
import requests
from requests.auth import HTTPBasicAuth

WP = "https://example.com/wp-json/wp/v2"
AUTH = HTTPBasicAuth("admin", "xxxx xxxx xxxx xxxx xxxx xxxx")

# Update an existing page's Nexter markup
page_id = 123
markup = '<!-- wp:tpgb/heading {"blockId":"tpgb-h1"} -->...<!-- /wp:tpgb/heading -->'
r = requests.post(f"{WP}/pages/{page_id}", auth=AUTH, json={"content": markup})
r.raise_for_status()
print(r.json()["link"])
```

### WordPress core block filters Nexter output flows through

These are WordPress **core** hooks (not Nexter-owned), useful for modifying or branching on Nexter blocks by their `tpgb/` block name.

| Hook | Type | Purpose |
|---|---|---|
| `render_block` | Filter | Modify a block's rendered HTML at output time. Signature: `( string $block_content, array $block )`; branch on `$block['blockName']` (e.g. `tpgb/heading`). |
| `render_block_data` | Filter | Modify a parsed block's data before it renders. |
| `block_categories_all` | Filter | Modify the block categories shown in the editor. |

```php
// Append a tracking attribute to a Nexter block on the frontend
add_filter( 'render_block', function ( $block_content, $block ) {
    if ( strpos( $block['blockName'] ?? '', 'tpgb/' ) === 0 ) {
        $block_content = str_replace( '<div ', '<div data-nexter="1" ', $block_content );
    }
    return $block_content;
}, 10, 2 );
```

---

## 3. Performance / load option flags (observed)

Nexter exposes asset-delivery controls in its settings, persisted in `wp_options`. Observed flag names (verify against your version):

| Option | Purpose |
|---|---|
| `default_tpgb_load_opt` | Default block-loading option (smart/conditional asset loading). |
| `tpgb_defer_css_js` | Defer Nexter's CSS/JS. |
| `tpgb_delay_css_js` | Delay-load Nexter's CSS/JS (until interaction). |

```php
// Inspect the current state of a Nexter performance flag
$defer = get_option( 'tpgb_defer_css_js' );
```

**Smart asset delivery (claimed):** 1 CSS file + 1 JS file per page regardless of block count; disabled blocks load no code; zero jQuery (pure vanilla JS). Third-party tests (PluginTests.com) still measure ~0.24–0.35s added page-load time and ~6–9 MiB memory across recent versions — benchmark on your own pages.

---

## 4. Building/extending from source

```bash
# From the GitHub repo (GPLv3)
# 1. Clone into wp-content/plugins of a local WP dev site:
#    github.com/posimyth/the-plus-addons-for-block-editor
# 2. Build per the repo's instructions (build system not documented in the README at capture time).
```

External services the plugin talks to (per README): Instagram, Facebook SDK, Google Maps API, Vimeo, and the ThePlus Addons API.

## Gaps / not documented

- **No public hosted REST API** for Nexter objects — use the WordPress core REST API against posts/pages, whose `content` holds the `tpgb/` block markup, or the MCP server.
- **No native outbound webhook** and **no first-party Zapier/Make app** — form leads exit through the form's configured integration (e.g. Mailchimp).
- **The MCP endpoint path, config snippet, and token** are generated per-site in WP admin and were not captured verbatim — use the snippet Nexter generates.
- **The `tpgb/` namespace, attribute keys, and option-flag names are observed/inferred** — confirm against the installed version's markup/settings; do not assume undocumented hooks exist. Source: `nexterwp.com/nexter-abilities`, `nexterwp.com/docs`, `github.com/posimyth/the-plus-addons-for-block-editor`, WordPress.org plugin page.
