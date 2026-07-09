# Stackable Platform Reference

## Overview

Stackable ("The complete companion to the WordPress block editor") is a **Gutenberg-native block plugin** for WordPress by **Gambit Technologies** (developer **gambitph** / Benjamin Intal). It **extends** the native block editor — like Spectra, Kadence Blocks, and GenerateBlocks — rather than replacing it (the contrast with Elementor/Divi). It is **GPLv3 and open source** (`github.com/gambitph/Stackable`), with 100k+ active installs on WordPress.org (200k+ sites claimed) and a 4.9★ rating. Its differentiators are **design depth** (rich style controls, a Global Design System) and a **lean footprint** (~10–75KB added; consistently rated among the fastest block plugins). It is **not** an all-in-one — no cart, no email, no A/B testing — and notably **no form builder, popup builder, header/footer builder, or WooCommerce blocks.**

## Capabilities & automation surface

| Capability | What it does | Surface |
|---|---|---|
| 42 blocks — **Essential** (Columns, Heading, Text, Image, Button, Icon, Icon List, Spacer/Divider), **Special** (Carousel, Tabs, Accordion, Timeline, Map, Pricing Box, Testimonial, Count Up, Progress Bar/Circle, Notification, Expand/Read-more, Video Popup, Number Box, Image Box), **Section** (Hero, Call to Action, Feature, Feature Grid, Card, Team Member, Blog Posts, Posts) | Page/section building inside the block editor | UI-built; output filterable via `render_block` |
| Columns / section layout | Flexbox rows/columns layout primitive | UI-only |
| Design Library | 375+ pre-made block patterns, UI Kits, page/section designs (≈107 free) | UI-only |
| Global Design System | Global Colors, Global Typography, block defaults applied site-wide | UI-only |
| theme.json / block-theme support | Inherit colors/typography from a block theme; FSE-friendly | UI-only |
| Responsive editing | Desktop/tablet/mobile controls, custom breakpoints, block visibility | UI-only |
| **Dynamic Content** | Bind block content to native fields, **ACF, Metabox, JetEngine**, post/site data | **Pro**, UI-only |
| **Motion Effects / Transforms** | Scroll/entrance animations, transform & transition controls | **Pro**, UI-only |
| **Conditional Display** | Show/hide blocks by role, login, date, device, etc. | **Pro**, UI-only |
| **Role Manager** | Restrict which editor controls each role can use; agency tools | **Pro**, UI-only |
| **Per-block Custom CSS** | Add custom CSS to an individual block | **Pro**, UI-only |
| **Advanced copy-paste styles** | Copy a block's full style set to another block | **Pro**, UI-only |
| CSS optimization | Loads Stackable CSS only on pages containing Stackable blocks; optimized image loading | Auto; override via `stackable_force_css_load` |
| Public filters | Force CSS load, modify rendered block output | **Developer (PHP hooks)** — see `stackable-api-reference.md` |

**There is no hosted REST API and no native outbound webhook.** Stackable is a WordPress plugin; its programmatic surface is WordPress core (the WP REST API, Application Passwords, WP-CLI) plus a small set of Stackable PHP filters.

## Pricing, limits & plan gates

*Pricing is best-effort from 2026 research, annual unless noted, and toggled by site count — verify on wpstackable.com/premium before relying on it. A Lifetime toggle exists; exact multi-site/lifetime figures aren't always displayed.*

| Plan | Approx. price | Sites | Notable inclusions |
|---|---|---|---|
| **Free** (WordPress.org) | $0 | unlimited | All **42 blocks**, Global Design System (Global Colors/Typography, block defaults), responsive editing, part of the Design Library (≈107 patterns), 2 color schemes, 10 color presets, 11 font pairs |
| **Premium** | ~$49/yr | 1 (toggle 10 / Unlimited) | Free + **Dynamic Content**, **Motion Effects/transforms**, **Conditional Display**, **Role Manager**, **per-block Custom CSS**, advanced copy-paste, full Design Library (375+), unlimited color schemes, 50 presets, 97 font pairs, integrations (ACF/Metabox/JetEngine), priority support |
| **All Access Pass** | ~$89/yr | 1 (toggle 10 / Unlimited) | Premium + the maker's other products/bundle (annual only) |

- **30-day money-back guarantee.** Annual subscriptions auto-renew; a **Lifetime** option exists via the pricing toggle.
- **Affiliate program:** wpstackable.com/affiliate/.
- **Plan-gate watch-outs:** Dynamic Content, Motion Effects, Conditional Display, Role Manager, per-block Custom CSS, advanced copy-paste, and the expanded Design Library/presets are **Pro**. Pro-only styling/features can stop applying if Premium is deactivated/expired.
- **Not included on any tier:** form builder, popup builder, header/footer builder, WooCommerce-specific blocks, native A/B testing/heatmaps/analytics.

## Integrations

- **Themes:** works with any block-editor theme; benefits from block themes (theme.json inheritance). Commonly paired with GeneratePress, Astra, Blocksy, Kadence, Neve.
- **Dynamic data sources (Pro):** **ACF, Metabox, JetEngine**, and native WordPress fields feed Dynamic Content.
- **Filtering/search:** the Blog Posts block can be paired with **FacetWP** for faceted post filtering (per Stackable docs).
- **Lead capture (data out):** Stackable has **no form block** — add a third-party form plugin (Gravity Forms, FluentForms, WPForms) and use its ESP/webhook delivery; route the sequence via `/sales-email-marketing`.
- **iPaaS:** **no first-party Zapier/Make app** for Stackable; automation rides on the underlying form/CRM/WooCommerce plugin's connectors.

## Data model

Stackable has **no remote object model/API**. Its "data" is **WordPress block markup** stored in `post_content`, plus Stackable settings in `wp_options` and generated CSS.

A Stackable block in `post_content` is a standard Gutenberg block comment with a `stackable/`-namespaced block name and a JSON attributes object:

```html
<!-- wp:stackable/columns {"uniqueId":"a1b2c3d","version":"3"} -->
<div class="stk-block stk-block-columns wp-block-stackable-columns stk-a1b2c3d">
  <!-- wp:stackable/column ... -->
  <!-- wp:stackable/card {"uniqueId":"e5f6g7h"} /-->
  <!-- /wp:stackable/column -->
</div>
<!-- /wp:stackable/columns -->
```

<!-- Constructed from observed markup — verify the exact attribute keys (uniqueId/version) against a live install -->

To read or modify Stackable content programmatically, use the **WordPress REST API** for posts/pages (block markup is in the `content` field), or `get_post`/`wp_update_post` in PHP. There is no Stackable-specific record endpoint.

```bash
# Read a page's block markup via the WordPress REST API (application password auth)
curl -s https://example.com/wp-json/wp/v2/pages/123 \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" | jq '.content.rendered'
```

## Quick-start recipes

### Recipe 1 — Force Stackable's CSS to load everywhere

**Trigger:** a page renders unstyled because Stackable markup was injected dynamically (shortcode, REST, another builder) and Stackable didn't detect its blocks.
**Steps:** return `true` from the `stackable_force_css_load` filter so Stackable always enqueues its frontend CSS.

```php
// functions.php or a small mu-plugin — always load Stackable's frontend CSS
add_filter( 'stackable_force_css_load', '__return_true' );
```

**Gotcha:** this disables the "only load CSS where blocks exist" optimization site-wide — scope it (e.g. check `is_singular()` or a template) if you only need it on certain pages.

### Recipe 2 — Programmatically create/update a Stackable page

**Trigger:** you want to template a landing page built from Stackable blocks and push it from a script.
**Steps:** there's no "create a Stackable page" API. Build the page once in the editor, copy the `stackable/` block markup, then write it into a WP post/page via the WordPress core REST API.

```bash
# Create a page whose body is Stackable block markup (block markup elided for brevity)
curl -s -X POST https://example.com/wp-json/wp/v2/pages \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Launch",
    "status": "publish",
    "content": "<!-- wp:stackable/hero {\"uniqueId\":\"hero1\"} -->...<!-- /wp:stackable/hero -->"
  }'
```

```python
import requests
from requests.auth import HTTPBasicAuth

WP = "https://example.com/wp-json/wp/v2"
AUTH = HTTPBasicAuth("admin", "xxxx xxxx xxxx xxxx xxxx xxxx")

hero = '<!-- wp:stackable/hero {"uniqueId":"hero1"} -->...<!-- /wp:stackable/hero -->'
r = requests.post(f"{WP}/pages", auth=AUTH,
                  json={"title": "Launch", "status": "publish", "content": hero})
r.raise_for_status()
print(r.json()["link"])
```

**Gotcha:** keep the `uniqueId`/`version` attributes Stackable expects; copy a real block's markup rather than hand-writing attributes.

### Recipe 3 — Modify rendered block output with `render_block`

**Trigger:** you want to inject markup, wrap, or tweak a specific Stackable block's frontend HTML.
**Steps:** filter the WordPress core `render_block` hook and branch on the block name.

```php
add_filter( 'render_block', function ( $block_content, $block ) {
    if ( ( $block['blockName'] ?? '' ) === 'stackable/card' ) {
        // e.g. append a data attribute or wrapper for analytics
        $block_content = str_replace( '<div ', '<div data-track="card" ', $block_content );
    }
    return $block_content;
}, 10, 2 );
```

## Integration patterns

- **Programmatic page creation:** no Stackable API — create/update a WP post/page via the WordPress REST API or `wp_insert_post`, writing **`stackable/`-namespaced block markup** into `content`. Build once in the editor, copy, template.
- **Lead/data out:** Stackable emits no webhook and has no form block. Capture leads through a connected form plugin's webhook/ESP, or read submissions/orders from the underlying plugin (Gravity Forms/FluentForms/WooCommerce REST).
- **Asset/CSS pipeline:** Stackable loads its CSS only on pages containing its blocks. For dynamically-injected markup, use `stackable_force_css_load`. After migrations/bulk edits, clear page/object/CDN cache and allowlist Stackable assets in any minify plugin.
- **Version migration:** v3 was a rewrite; v2 blocks persist as separate blocks controlled by **Settings → Other Settings → Migration** (load v2 blocks / allow both / v3-only). Migrate on staging; existing v2 pages render only while v2 block loading is enabled.
- **Extending blocks:** prefer documented filters (`stackable_force_css_load`, the WordPress `render_block`) over editing block markup so changes survive updates. For deeper changes the plugin is GPLv3 — fork and build (`npm install`, `npm run start`). See `references/stackable-api-reference.md`.
