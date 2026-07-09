# Gutenverse Platform Reference

## Overview

Gutenverse is a **free, Gutenberg-native block plugin and Full Site Editing (FSE) ecosystem** for WordPress, built by **Jegstudio / Jegtheme** (an Envato Power Elite seller). It *extends* the native block editor with 57 blocks, a 600+ starter-template library, a popup builder, and global colors/fonts — it does **not** replace the editor the way Elementor/Divi do. Its angle is breadth of ready-made blocks + an FSE/site-building ecosystem (companion **Unibiz** theme, separate **Gutenverse Form** plugin) at a generous free tier. ~20,000–34,000+ active installs, 4.9★; WP 5.9+ / PHP 7.0+, tested to WP 6.9.x; current v3.8.x.

## Capabilities & automation surface

| Module | What it does | Automation tag |
|---|---|---|
| **57 blocks** (Layout, Content, Interactive, Post/Query, Social, Google Maps) | Drag-and-drop building inside the native block editor; output is `gutenverse/`-namespaced block markup | UI-first; markup readable/writable via **WordPress core REST API** |
| **Starter template library** (600–800+ templates/layouts/sections) | Importable demo designs and sections | UI-only (import in editor) |
| **Popup builder** (Popup Builder + Popup Container blocks) | On-page popups/modals for opt-ins and announcements | UI-only |
| **Global colors & fonts** | Site-wide color palette + typography presets | UI-only (stored in theme/global styles) |
| **Mega menu builder** (Pro) | Multi-column navigation menus | UI-only |
| **Animations / Lottie / cursor & sticky effects** (Pro) | Motion and scroll/cursor interactions | UI-only |
| **Dynamic data + display/visibility conditions** (Pro) | Bind block content to data; show/hide by condition | UI-only |
| **Gutenverse Form** (separate free plugin) | Form blocks; entries **stored in WordPress** + CSV export; admin/user email notifications; reCAPTCHA | Entries readable via WP DB/REST; **no webhook/Zapier in free** |
| **`gutenverse-core` framework** | Developer framework powering the blocks (hooks, ES6 packages, Redux-style store) | **Developer-extensible** (PHP/JS hooks) |

**Not shipped / "coming soon" (verify against changelog):** WooCommerce blocks, custom fields, Query Loop for custom post types were marketed as upcoming. No native A/B testing, heatmaps, or analytics on any tier.

## Pricing, limits & plan gates

*Best-effort from research (2026-06); sources disagree on exact numbers — confirm on gutenverse.com/pricing. Annual billing.*

| Tier | Approx. price | Sites | Highlights |
|---|---|---|---|
| **Free** | $0 (WordPress.org) | unlimited | All 57 blocks, template library, popup builder, global colors/fonts, responsive editing; **Gutenverse Form** free plugin (basic fields, WP-stored entries, CSV, email notifications, reCAPTCHA) |
| **Pro — Personal/Single** | ~$55–69/yr (intro vs renewal) | 1 | Pro blocks/templates, dynamic data, display conditions, custom fonts, advanced form features |
| **Pro — Professional** | ~$79–99/yr (intro vs renewal) | ~10 | Everything in Personal across more sites |
| **Pro — Agency** | ~$199/yr (≈$16.6/mo) | ~100 | Agency-scale site count |

- **Plan-gated features:** form builder advanced features (conditional logic, multi-step, calculation/payment fields), dynamic data, display/visibility conditions, custom fonts, premium templates/blocks, mega menu, advanced animations.
- **License lapse:** Pro-only styling/features stop applying when the license expires — test on staging before relying on them for a live launch.
- **Licensing/payments:** Gutenverse Pro uses the **LemonSqueezy** gateway (added v3.8.0) for checkout/license management. "Lifetime support and updates" + money-back guarantee are advertised; verify whether a true one-time lifetime *license* exists vs annual.

## Integrations

- **Reads/writes:** Page/post content via the **WordPress core REST API** (`gutenverse/`-namespaced block markup in `post_content`). No proprietary Gutenverse API.
- **Forms (Gutenverse Form, free):** writes entries to the WordPress database (CSV export); sends admin + user **email notifications**. **No** native webhook, Zapier, Make, Mailchimp, or CRM connector in the free plugin — those advanced routes are Pro/roadmap.
- **External services used by blocks:** Google Maps API (Maps block), Google Fonts (typography), social-share URLs.
- **Companion theme:** **Unibiz** (50+ demo sites) for a turnkey FSE starting point.
- **iPaaS:** No first-party Zapier/Make app. To push form leads outward without Pro, capture the WordPress entry (DB/REST) and forward it yourself, or pair a form plugin that has native iPaaS.

## Data model

Gutenverse stores everything as **WordPress block markup** inside the post/page `post_content`. There is no separate object database to query via a Gutenverse API — you operate on WordPress posts.

A Gutenverse block in `post_content` looks like this (shape constructed from observed block markup):

```html
<!-- wp:gutenverse/button {"elementId":"guten-AB12cd","align":"center"} -->
<div class="wp-block-gutenverse-button guten-element guten-AB12cd">
  <a class="guten-button" href="/signup">Get Started</a>
</div>
<!-- /wp:gutenverse/button -->
```
<!-- Constructed from observed Gutenverse block markup — verify attribute names against the live editor/`block.json`. -->

Retrieved via the WordPress REST API, a page is a standard post object:

```json
{
  "id": 482,
  "status": "publish",
  "type": "page",
  "content": {
    "raw": "<!-- wp:gutenverse/section ... --> ... <!-- /wp:gutenverse/section -->",
    "rendered": "<section class=\"wp-block-gutenverse-section ...\">...</section>"
  }
}
```
<!-- Constructed from the WordPress core REST API page schema — `content.raw` requires `context=edit` + auth. -->

A **Gutenverse Form** entry (stored in WordPress, exportable as CSV) carries the submitted field values plus metadata (form id, timestamp, page). The free plugin surfaces these in the admin and via CSV — there is no documented public entries API.

## Quick-start recipes

> Gutenverse has **no hosted API**. These recipes use the **WordPress core REST API** and the **`gutenverse-core`** developer hooks. Base URL = your site, e.g. `https://example.com/wp-json/wp/v2/`. Auth = **Application Passwords** (Users → Profile → Application Passwords) over HTTPS, sent as HTTP Basic.

### Recipe 1 — Read a page's Gutenverse block markup
**Trigger:** you need the raw block markup to audit or transform it.

cURL:
```bash
curl -s "https://example.com/wp-json/wp/v2/pages/482?context=edit" \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['content']['raw'])"
```

Python:
```python
import requests
from requests.auth import HTTPBasicAuth

site = "https://example.com"
auth = HTTPBasicAuth("admin", "xxxx xxxx xxxx xxxx xxxx xxxx")  # Application Password

r = requests.get(f"{site}/wp-json/wp/v2/pages/482",
                 params={"context": "edit"}, auth=auth)
r.raise_for_status()
raw = r.json()["content"]["raw"]
print(raw[:500])  # gutenverse/-namespaced block markup
```
**Gotcha:** `context=edit` (needed for `content.raw`) requires an authenticated user who can edit the post; without it you only get `content.rendered` HTML.

### Recipe 2 — Bulk-update CTA text inside Gutenverse blocks
**Trigger:** swap a string across many pages.

Python:
```python
import re, requests
from requests.auth import HTTPBasicAuth

site = "https://example.com"
auth = HTTPBasicAuth("admin", "xxxx xxxx xxxx xxxx xxxx xxxx")
page_ids = [482, 483, 484]

for pid in page_ids:
    r = requests.get(f"{site}/wp-json/wp/v2/pages/{pid}",
                     params={"context": "edit"}, auth=auth)
    raw = r.json()["content"]["raw"]
    updated = raw.replace("Get Started", "Start Free Trial")
    # POST the transformed markup back; WordPress re-parses the blocks
    requests.post(f"{site}/wp-json/wp/v2/pages/{pid}",
                  json={"content": updated}, auth=auth).raise_for_status()
    print(f"updated {pid}")
```
**Gotcha:** edit the block *markup* string, not the rendered HTML — POSTing rendered HTML strips the `<!-- wp:gutenverse/... -->` block delimiters and the page stops being editable as blocks. Test on staging; back up first.

### Recipe 3 — Extend the editor / force config via `gutenverse-core` hooks
**Trigger:** you're building a child plugin that adds styles or injects config into Gutenverse blocks.

PHP (in a small companion plugin):
```php
// Enqueue extra assets once the Gutenverse framework is initialized
add_action( 'gutenverse_after_init_framework', function () {
    // register your scripts/styles here
} );

// Run logic when a Gutenverse block is included/enqueued
add_action( 'gutenverse_include_block', function ( $block ) {
    // $block = the block being processed
} );

// Inject additional configuration into the editor
add_filter( 'gutenverse_block_config', function ( $config ) {
    $config['myFeatureFlag'] = true;
    return $config;
} );
```
**Gotcha:** hook names are from the `gutenverse-core` README — confirm signatures against the installed `gutenverse-core` version before shipping, since the framework evolves.

## Integration patterns

- **CRM/lead sync:** the free Form plugin has no outbound connector. Two options: (a) poll/export form entries (admin CSV or a custom query on the WordPress side) and push them to your CRM; (b) replace the lead-capture step with a form plugin that has native webhooks/iPaaS and route via `/sales-email-marketing`. Don't assume webhook delivery from Gutenverse Form's free tier.
- **Programmatic page management:** treat Gutenverse pages as ordinary WordPress posts. Use the core REST API with Application Passwords; operate on `content.raw` block markup (`context=edit`). Paginate list endpoints with `?page=` + `per_page=` and read the `X-WP-Total` / `X-WP-TotalPages` headers.
- **Performance/asset handling:** Gutenverse loads styling per page and added a styling-cache mechanism in v3.4.0+. When markup is injected dynamically or served from cache, regenerate the style cache and exclude Gutenverse's CSS/JS from aggressive minify/combine so the frontend matches the editor.
- **Extending blocks:** build against `gutenverse-core` (npm build toolchain; Node v14.20.1 / npm 6.14.17 per the README), using the documented action/filter hooks and the `gutenverseCore.*` ES6/window packages and Redux-style store. Source is under `github.com/Jegstudio`.
