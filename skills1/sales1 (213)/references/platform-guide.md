# Greenshift Platform Reference

## Overview

Greenshift ("Greenshift – animation and page builder blocks") is a **performance-focused Gutenberg page-builder + animation block plugin** for WordPress by **Wpsoul (WP Soul)** — the team behind the **ReHub** theme on ThemeForest. WordPress.org slug: `greenshift-animation-and-page-builder-blocks`; ~4.8★. It **extends** the native block editor (it doesn't replace Gutenberg), so pages are built as standard WordPress blocks. Its angle is **feature breadth + performance**: 50+ blocks, a GSAP-based animation framework, Interaction Layers, 3D/AR-VR/Lottie/Rive, Full Site Editing support, and — unusually for a block plugin — an **API Connector** that binds external REST APIs, Google Sheets/CSV, and **LLM APIs (OpenAI chat/streaming)** into blocks, plus **AI Helpers**, a **Figma/HTML/webpage→blocks converter**, and a **VS Code extension**. It markets ~2 KB base styles, conditional asset loading, and no jQuery. Also sold on AppSumo as a lifetime deal.

It is the **animation- and data-rich / developer-leaning** pick among block plugins; the breadth contrast to minimalist GenerateBlocks/Stackable and a rival to Kadence/Spectra/Nexter.

## Capabilities & automation surface

| Capability | What it does | Surface |
|---|---|---|
| **50+ blocks** | Layout/Container, animated headlines, counters, countdown, tabs/togglers, table of contents, progress bars, sliders/carousels, shape dividers, 3D flip boxes, popups/panels | UI-built; markup filterable via `render_block` |
| **Animation framework (GSAP)** | Scroll animations, hover transitions, parallax, effect presets, pin/smooth scroll, mouse-follow, video scroller | UI-built; advanced GSAP is **paid** (Design/GreenLight PRO) |
| **Interaction Layers** | Assign a trigger (click, scroll, etc.) + an action to any block | UI-built (paid) |
| **3D / AR-VR / Lottie / Rive** | AR/VR 3D viewer block, Spline 3D block, Lottie + Rive animations | UI-built (paid) |
| **Query addon + dynamic blocks** | Dynamic FAQ, Dynamic Chart (Apex, 20+ presets), Filter block, Dynamic Search, Comment/User/Taxonomy builders, breadcrumbs, galleries — bound to dynamic data | **Paid**, UI-built |
| **Dynamic data sources** | Post types, users, taxonomies, comments, options, repeater fields (ACF/ACPT/MetaFields), **external repeaters** | **Paid**, UI-built |
| **API Connector** | Bind external REST APIs / Google Sheet / CSV / **LLM APIs (chat + streaming)** into blocks — server-side or client-side | **Paid (GreenLight PRO)** — see `greenshift-api-reference.md` |
| **AI Helpers / AI agents** | Generate/build blocks with AI using your **own** API key (requests go direct to the provider) | **Paid (GreenLight PRO / All-in-One)** |
| **Converters** | **Figma converter**, HTML-source→blocks, any webpage/website→Greenshift blocks | **Paid (GreenLight PRO)** |
| **VS Code Extension PRO** | Edit/scaffold Greenshift blocks from VS Code | **Paid (GreenLight PRO)** |
| **WooCommerce blocks** | Single Product templates, product loop builder, swatches, variation galleries, 360/3D gallery, bundles, stock/free-shipping bars, quick-buy | **Paid (Woo Pack)** |
| **SEO & Marketing addon** | Schema blocks (Product/FAQ/Event/Video), comparison tables | **Paid (All-in-One)** |
| **`GSPB_API_RESPONSE` JS event** | Client-side hook fired after an API Connector response | **Developer (JS)** — see `greenshift-api-reference.md` |

**There is no hosted REST API and no native outbound webhook from Greenshift.** Greenshift is a WordPress plugin; its programmatic surface is WordPress core (the WP REST API, application passwords, WP-CLI) **plus its own API Connector** (which is itself a no-code consumer of *other* APIs, including AI) and the client-side `GSPB_API_RESPONSE` event. Form lead capture isn't a core module — pair a form plugin and use its delivery.

## Pricing, limits & plan gates

*Pricing is best-effort from 2026 research, often intro/annual, and split across packs — verify on greenshiftwp.com/pricing before relying on it. Lifetime tiers can be paid in cryptocurrency; 14-day money-back guarantee.*

| Pack | Approx. annual | Approx. lifetime | Sites | Notable inclusions |
|---|---|---|---|---|
| **Free** (WordPress.org) | $0 | — | unlimited | 50+ blocks, basic CSS animations/hover, FSE support, ~2 KB base styles |
| **Design Pack** | ~$39.99–$79.99 | ~$79.99–$239.99 | 1 / 5 / Unlimited | Dynamic 3D block, **advanced GSAP animations**, effect presets, video scroller, mouse-follow, pin/smooth scroll, dynamic fields, dynamic Rive/Lottie, custom interactions |
| **Woo Pack** | ~$49.99–$99.99 | ~$89.99–$269.99 | 1 / 5 / Unlimited | Single Product templates, product loop builder + templates, swatches, variation galleries, 360/3D gallery, bundles, stock/free-shipping bars, quick-buy |
| **GreenLight PRO** | ~$51.99–$109.99 | ~$99.99–$299.99 | 1 / 5 / Unlimited | Dynamic fields, Class First system, Light Framework, variable system/presets, **API Connector**, advanced animations/interactions, dynamic placeholders, **Figma converter**, **AI Helpers**, any-webpage converter, **VS Code Extension PRO** |
| **All-in-One Pack** | ~$59.99–$129.99 | ~$109.99–$459.99 | 1 / 5 / Unlimited | **Everything** — GreenLight PRO included, full Wireframe library, **SEO & Marketing addon**, Chart addon, **AI agents**, GreenLight Pulse, GreenLight Dash PRO (1 yr) |

- **Plan-gate watch-outs:** advanced GSAP animations, dynamic fields, the **API Connector**, AI Helpers, the Figma converter, and the VS Code extension are **GreenLight PRO**; **WooCommerce blocks** are the **Woo Pack**; **schema/SEO blocks, charts, and AI agents** are **All-in-One**. The Query addon can be bought separately or comes with Design/SEO/All-in-One. Pages built on paid-only features can **degrade/lose styling** if the license lapses.
- **No native A/B testing, heatmaps, analytics, cart engine, or email** on any tier.
- **Affiliate / partner program** exists (referenced on greenshiftwp.com) — log under `_internal/affiliates.md` if you pursue it.

## Integrations

- **Theme:** any theme; full **Full Site Editing (FSE)** / block-theme support.
- **WooCommerce:** deep via the **Woo Pack** (product templates, loop builder, swatches, galleries, bundles) — display + merchandising blocks, not a separate cart engine.
- **Dynamic data sources:** **ACF, ACPT, MetaFields** repeaters, post types, users, taxonomies, comments, options, and **external repeaters** via the Query addon.
- **External / AI APIs:** the **API Connector** consumes any REST API, Google Sheet/CSV, or LLM API (OpenAI-style chat/streaming) — server-side or client-side. This is the main "integration" surface.
- **Design import:** **Figma converter**, HTML-source→blocks, and any-webpage→Greenshift converters (GreenLight PRO).
- **Forms / leads (data out):** no core form module — pair a form plugin and use its ESP/webhook delivery; or POST via the API Connector to your endpoint.
- **iPaaS:** no first-party Zapier/Make app for Greenshift itself; automation rides on the underlying WordPress/WooCommerce/form plugin's connectors or the API Connector.

## Data model

Greenshift has **no remote object model/API**. Its "data" is **WordPress block markup** stored in `post_content`, plus plugin settings in `wp_options` and generated CSS. Greenshift blocks use the `greenshift-blocks/` namespace and `GSPB`-prefixed CSS classes.

A Greenshift block in `post_content` is a standard Gutenberg block comment with a `greenshift-blocks/`-namespaced name and a JSON attributes object (best-effort shape — copy a real block from the editor as the source of truth):

```html
<!-- wp:greenshift-blocks/element {"id":"gsbp-abc123","tag":"div","animation":{...},"styleAttributes":{...}} -->
<div id="gspb_container-id-gsbp-abc123" class="gspb_container">
  <!-- inner blocks (e.g. greenshift-blocks/heading, greenshift-blocks/button) -->
</div>
<!-- /wp:greenshift-blocks/element -->
```

<!-- Constructed from observed Greenshift markup conventions (greenshift-blocks/ namespace, GSPB classes) — block names/attributes evolve per release; verify against a live install -->

> Confirm exact `greenshift-blocks/*` names and attribute keys against your installed version — copy a real block from the editor rather than hand-authoring from memory.

To read or modify Greenshift content programmatically, use the **WordPress REST API** for posts/pages (block markup is in the `content` field) or `get_post`/`wp_update_post` in PHP. There is no Greenshift-specific record endpoint.

```bash
# Read a page's block markup via the WordPress REST API (application password auth)
curl -s https://example.com/wp-json/wp/v2/pages/123 \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" | jq '.content.rendered'
```

## Quick-start recipes

### Recipe 1 — Server-side API Connector: pull an external REST API into a block

**Trigger:** display live data from an external (or your own WordPress) REST API, with secrets kept server-side.
**Steps:** enable **Dynamic/Repeater Output** on an Element block → add the API URL → set the response field path → **Fetch**. Use placeholders in link/body/header fields; for authenticated endpoints add a Basic-auth header.

```text
# In the block's API Connector (server-side):
Link:   https://api.example.com/v1/items?per_page=25&page={{INCREMENT:1}}
Header: Authorization: Basic <base64 of "USER:APP_PASSWORD">
Response field: data[items]          # array → maps to repeater items
# Map fields onto inner blocks by class; links populate href, images populate src.
```

```bash
# The WordPress endpoint equivalent the connector calls (Application-Password auth):
curl -s "https://example.com/wp-json/wp/v2/product?per_page=1&offset=1" \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx"
```

**Gotcha:** server-side stores the response in the block and keeps keys off the client — prefer it for anything secret. Use `{{INCREMENT:1}}` to bump `offset`/`page` on sequential calls; pagination works when the API uses a `page` param.

### Recipe 2 — Client-side API Connector calling an LLM (OpenAI chat + streaming)

**Trigger:** build an on-page AI chat/answer block.
**Steps:** use a **client-side** connector (browser `fetch`). Configure Chat mode (append messages to a `messages` array) and optionally Streaming. **The key is public client-side** — for production, proxy through the server-side connector or your own endpoint instead of embedding a secret.

```jsonc
// Client-side connector body (OpenAI-style chat)
{
  "model": "gpt-4o-mini",
  "messages": [{ "role": "system", "content": "You are a helpful assistant." }]
}
// Append Field: "messages"
// User message:      { "role": "user", "content": "{{VALUE:.userinput}}" }
// Assistant message: { "role": "assistant", "content": "{{RESPONSE}}" }
// Response field:    choices[0][message]
// Streaming on → elements get .loading then .loaded/.active classes
```

**Gotcha:** never ship a secret API key in a client-side connector — "client-side APIs are always public." Use it only for public data or via a server-side proxy.

### Recipe 3 — Dynamic listing with the Query addon (CPT grid bound to ACF)

**Trigger:** show a grid/list of a custom post type with a custom-field value and featured image.
**Steps:** add a **Query/Repeater builder** block, set the data source (post type), add inner blocks, and bind dynamic fields (post title, ACF/post-meta value, featured image). Tune the underlying `WP_Query` in code if needed:

```php
// Adjust the query for a Greenshift dynamic listing on a CPT archive
add_action( 'pre_get_posts', function ( $q ) {
    if ( is_admin() || ! $q->is_main_query() ) {
        return;
    }
    if ( is_post_type_archive( 'portfolio' ) ) {
        $q->set( 'category__not_in', [ 12 ] );
    }
} );
```

**Gotcha:** the **Query addon and dynamic fields are paid**. Repeater sources include ACF/ACPT/MetaFields and external repeaters; deeply-nested values are addressed by key path (`field[subfield][0][subsub]`).

## Integration patterns

- **Programmatic page creation:** there is no "create a Greenshift page" API. Create/update a WP post/page via the WordPress REST API or `wp_insert_post`, writing **`greenshift-blocks/`-namespaced block markup** into `content`. Build the layout once in the editor, copy the markup, and template it (keep `id`/`GSPB` IDs unique).
- **External & AI data:** the **API Connector** is the integration: server-side for secret-bearing or WordPress endpoints, client-side for public data and AI chat/streaming. Hook client-side completions with the `GSPB_API_RESPONSE` JS event to run custom code on the result.
- **Lead/data out:** Greenshift emits no webhook and has no core form block. Capture leads through a paired form plugin's webhook/ESP integration, or POST from the API Connector to your endpoint.
- **Asset/cache pipeline:** Greenshift generates per-block CSS. On huge pages the inline-CSS save can hit DB/host field limits (switch to inline-in-blocks saving); after migrations/major updates, re-save affected pages and clear page/object/CDN cache.
- **Performance posture:** Greenshift is lean by default (~2 KB base, conditional assets, no jQuery). For Core Web Vitals, watch the *number* of GSAP/3D/Lottie blocks per page, optimize images, and audit the theme + third-party scripts first.
