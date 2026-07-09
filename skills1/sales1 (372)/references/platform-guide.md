# Nexter Platform Reference

## Overview

Nexter is an **all-in-one WordPress Gutenberg ecosystem** by **POSIMYTH Innovations** (the makers of The Plus Addons for Elementor, WDesignKit, UiChemy, and SproutUI). It is the rebrand of the long-running **"The Plus Addons for Block Editor"** plugin — WordPress.org slug `the-plus-addons-for-block-editor`, **GPLv3**, ~10,000+ active installs, 4.8★, v4.7.x (tested to WP 7.0, PHP 7.4+). It comes in three parts:

1. **Nexter Blocks** — 90+ Gutenberg blocks (~45+ free, ~45+ Pro) with in-editor AI (ChatGPT + Gemini) and 1000+ templates.
2. **Nexter Extension** — 50+ site tools plus the **Theme Builder**, security hardening, performance optimization, code snippets, and White Label (agency).
3. **Nexter Theme** — a lightweight, jQuery-free starter theme (Gutenberg + Elementor compatible).

Like Spectra/Kadence/GenerateBlocks/Stackable it **extends** the native block editor rather than replacing it (the contrast with Elementor/Divi). Its differentiator is **feature breadth** — it ships a form builder, popup builder, mega menu, and header/theme builder (which lean plugins like Stackable/GenerateBlocks lack) — plus **Nexter Abilities, a native MCP server** that lets AI assistants build pages. It is **not** an all-in-one *business* suite — no native cart/checkout engine, no email sequences, no A/B testing.

## Capabilities & automation surface

| Capability | What it does | Surface |
|---|---|---|
| 90+ blocks — layout/containers, typography, buttons, pricing tables, countdowns, counters, tabs/accordions/flipboxes, post grids/carousels/masonry, testimonials, team, social feeds/embeds, maps, animated SVGs | Page/section building inside the block editor | UI-built; `tpgb/`-namespaced markup |
| **Form Builder** | Forms with 9 field types; login/registration/password-reset forms; **Mailchimp** integration (Pro) | UI-built; data out via the form's integration |
| **Popup Builder** | 6 popup types (modal, slide-in, bar, full screen, inline, widget), 10+ triggers, 16+ display rules | UI-only (**advanced/Pro**) |
| **Mega Menu** builder | Build mega menus inside the editor | UI-only |
| **Header / Theme Builder** | Build headers/footers/templates and theme parts | UI-only (**Theme Builder = Professional+**) |
| **Dynamic Content** | Bind block content to **ACF, Toolset, Pods**, and native WordPress custom fields | **Pro**, UI-only |
| WooCommerce blocks | Product grids/carousels/masonry | **Pro**, UI-only |
| Animations | Lottie, Spline 3D, parallax, heading animations, scroll sequences | **Pro**, UI-only |
| In-editor **AI** | Content generation, text-to-image, repeater auto-fill, toolbar refine — via **ChatGPT (OpenAI)** or **Gemini** (choose model in AI settings) | UI; uses your AI key |
| Analytics blocks | GA4 + Facebook Pixel trackers | **Pro**, UI-only |
| Smart asset delivery | 1 CSS + 1 JS file per page regardless of block count; disabled blocks load nothing; zero jQuery | Auto; tune via `tpgb_defer_css_js` / `tpgb_delay_css_js` |
| **Nexter Abilities (MCP server)** | 115 server-side tools exposing block composition to MCP clients (Claude, Cursor, VS Code…) | **Developer / AI** — see `nexter-api-reference.md` |
| White Label | Rebrand for agency/client sites | **Professional+** |

**There is no hosted REST API and no native outbound webhook.** Nexter is a WordPress plugin; its programmatic surface is (1) the **Nexter Abilities MCP server**, (2) WordPress core (the WP REST API, Application Passwords, WP-CLI — block markup is `tpgb/`-namespaced in `post_content`), and (3) PHP option/filter flags. There is **no first-party Zapier/Make app**.

## Pricing, limits & plan gates

*Pricing is best-effort from 2026 research, annual unless noted — verify on nexterwp.com/pricing before relying on it. A Lifetime option exists; an Agency Bundle adds the maker's other products. 60-day money-back guarantee.*

| Plan | Yearly | Lifetime | Sites | Notable inclusions |
|---|---|---|---|---|
| **Starter** | ~$39/yr | ~$139 once | 1 | 90+ blocks, 1000+ templates, in-editor AI, free MCP abilities |
| **Professional** | ~$89/yr | ~$249 once | 5 | Starter + **Theme Builder**, **White Label** |
| **Studio** | ~$129/yr | ~$349 once | Unlimited | Professional + unlimited sites |
| **Agency Bundle** | ~$399/yr | ~$899 once | — | Nexter Theme + Extension + Blocks + Abilities **+ The Plus Addons for Elementor + WDesignKit** |

- **Free** (WordPress.org): ~45+ blocks, the Form Builder, in-editor AI, and **68 of the 115 MCP abilities**.
- **Plan-gate watch-outs:** **Theme Builder and White Label are Professional+ (5 sites).** **Dynamic Content (ACF/Toolset/Pods), WooCommerce blocks, the advanced Popup Builder, Lottie/Spline/scroll animations, GA4/Pixel blocks, and the Pro half (47) of the MCP abilities are Pro.** Pro-only blocks/styling can fall back or stop applying if the license lapses.
- **Affiliate program:** up to ~$440+ per sale (nexterwp.com).
- **Not included on any tier:** native cart/checkout/upsell engine, email sequences/automation, native A/B testing/heatmaps/analytics.

## Integrations

- **Themes:** works with any block-editor theme — Nexter Theme, Astra, Kadence, Blocksy, GeneratePress, OceanWP, Neve, Hello Elementor, and the Full Site Editor.
- **Dynamic data sources (Pro):** **ACF, Toolset, Pods**, and native WordPress fields feed Dynamic Content.
- **AI:** in-editor AI connects to **ChatGPT (OpenAI)** and **Gemini** — pick the model in the AI settings dashboard (you supply the key).
- **Lead capture (data out):** Nexter's **Form Builder** sends to its configured integration (e.g. **Mailchimp**, Pro); for arbitrary destinations pair a dedicated form plugin or route via the ESP. Route the sequence via `/sales-email-marketing`.
- **Commerce:** WooCommerce blocks (Pro) display products; there's no cart/upsell engine — add WooCommerce + a funnel plugin (CartFlows/FunnelKit) for checkout. Compatible with WPML, RTL, and multisite.
- **iPaaS:** **no first-party Zapier/Make app** for Nexter; automation rides on the underlying form/CRM/WooCommerce plugin's connectors, or the MCP server.

## Data model

Nexter has **no remote object model/API**. Its "data" is **WordPress block markup** stored in `post_content`, plus Nexter settings in `wp_options` (option flags like `default_tpgb_load_opt`, `tpgb_defer_css_js`, `tpgb_delay_css_js`) and generated CSS.

A Nexter block in `post_content` is a standard Gutenberg block comment with a **`tpgb/`-namespaced** block name (best-effort — consistent with Nexter's `tpgb_*` option flags; verify against a live install) and a JSON attributes object:

```html
<!-- wp:tpgb/heading {"blockId":"tpgb-abc123"} -->
<div class="wp-block-tpgb-heading tpgb-abc123"> ... </div>
<!-- /wp:tpgb/heading -->
```

<!-- Block namespace/attribute keys observed/inferred — copy real block markup from a live install rather than hand-authoring -->

To read or modify Nexter content programmatically, use the **WordPress REST API** for posts/pages (block markup is in the `content` field), or `get_post`/`wp_update_post` in PHP. There is no Nexter-specific record endpoint — the MCP server (Nexter Abilities) is the higher-level way to compose blocks.

```bash
# Read a page's block markup via the WordPress REST API (application password auth)
curl -s https://example.com/wp-json/wp/v2/pages/123 \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" | jq '.content.rendered'
```

## Quick-start recipes

### Recipe 1 — Build a page with the Nexter Abilities MCP server

**Trigger:** you want an MCP client (Claude Desktop, Cursor, VS Code) to compose Nexter pages from a prompt, screenshot, or URL.
**Steps:** install Nexter Blocks (it includes the MCP endpoint + all 115 abilities) → connect your Nexter account → enable MCP permissions and **scope which post types + abilities** the AI may use → generate a token → paste the generated MCP config into your AI client → start prompting. The AI calls block-add abilities and produces **real, editable `tpgb/` Gutenberg blocks**.

```jsonc
// Illustrative MCP client config — Nexter generates the exact snippet (URL + token)
// in WP admin per-site. Confirm against your install; do not hardcode this verbatim.
{
  "mcpServers": {
    "nexter": {
      "url": "https://example.com/wp-json/nexter/mcp",   // verify the real endpoint path
      "headers": { "Authorization": "Bearer <SCOPED_TOKEN>" }
    }
  }
}
```

**Gotcha:** 68 abilities are free, 47 are Pro; every call still respects WordPress capabilities, and you can disable the endpoint anytime (existing pages stay intact). The endpoint path/auth shape above is illustrative — use the snippet Nexter generates.

### Recipe 2 — Programmatically create/update a Nexter page via the WordPress REST API

**Trigger:** you want to template a landing page built from Nexter blocks and push it from a script (without MCP).
**Steps:** build the page once in the editor, copy the `tpgb/` block markup, then write it into a WP post/page via the WordPress core REST API.

```bash
# Create a page whose body is Nexter block markup (markup elided for brevity)
curl -s -X POST https://example.com/wp-json/wp/v2/pages \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Launch",
    "status": "publish",
    "content": "<!-- wp:tpgb/heading {\"blockId\":\"tpgb-h1\"} -->...<!-- /wp:tpgb/heading -->"
  }'
```

```python
import requests
from requests.auth import HTTPBasicAuth

WP = "https://example.com/wp-json/wp/v2"
AUTH = HTTPBasicAuth("admin", "xxxx xxxx xxxx xxxx xxxx xxxx")

markup = '<!-- wp:tpgb/heading {"blockId":"tpgb-h1"} -->...<!-- /wp:tpgb/heading -->'
r = requests.post(f"{WP}/pages", auth=AUTH,
                  json={"title": "Launch", "status": "publish", "content": markup})
r.raise_for_status()
print(r.json()["link"])
```

**Gotcha:** keep the block attribute keys (e.g. `blockId`) Nexter expects; copy a real block's markup rather than hand-writing attributes.

### Recipe 3 — Tame asset loading for Core Web Vitals

**Trigger:** PageSpeed flags render-blocking CSS/JS or excess weight on Nexter pages.
**Steps:** Nexter already loads 1 CSS + 1 JS per page and disabled blocks load nothing — beyond that, enable Nexter's defer/delay controls, turn off unused blocks, and cache.

```php
// Option flags live in wp_options; toggle them in Nexter settings, or read/set in PHP.
// (Flag names observed: tpgb_defer_css_js, tpgb_delay_css_js — verify against your version.)
$opts = get_option( 'tpgb_defer_css_js' );   // inspect current state
```

**Gotcha:** allowlist Nexter's handles in any minify/optimization plugin, then benchmark before/after — third-party tests still measure ~0.2–0.35s and ~6–9 MiB added per request. For deeper remediation use `/sales-seo`.

## Integration patterns

- **AI page building:** prefer the **Nexter Abilities MCP server** for prompt/screenshot/URL → editable pages. Scope the token to specific post types + abilities; disable the endpoint when not in use.
- **Programmatic page creation (no MCP):** create/update a WP post/page via the WordPress REST API or `wp_insert_post`, writing **`tpgb/`-namespaced block markup** into `content`. Build once in the editor, copy, template.
- **Lead/data out:** Nexter's Form Builder emits no platform webhook — capture leads through the form's configured integration (Mailchimp/ESP) or a paired form plugin's webhook. Route the sequence via `/sales-email-marketing`.
- **Asset/CSS pipeline:** smart delivery loads 1 CSS + 1 JS per page; use `tpgb_defer_css_js`/`tpgb_delay_css_js`, disable unused blocks, cache, and allowlist Nexter handles in minify plugins.
- **Version updates:** v4.7.0 converted all blocks to WordPress **ApiVersion 3**; major updates can introduce regressions — back up + test on staging before updating a live site.
- **Extending:** prefer the MCP abilities and documented option flags over editing block markup so changes survive updates. For deeper changes the plugin is GPLv3 — fork and build (`github.com/posimyth/the-plus-addons-for-block-editor`). See `references/nexter-api-reference.md`.
