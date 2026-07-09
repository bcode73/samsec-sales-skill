# Beaver Builder Platform Reference

## Overview

Beaver Builder is a **stable, developer-friendly WordPress drag-and-drop page builder** by **FastLine Media LLC** (the Beaver Builder Team). Unlike the Gutenberg block plugins (Kadence/Spectra/GenerateBlocks/Stackable/Nexter/Greenshift), it is a **standalone builder**: a live front-end editor that builds pages as **Rows → Columns → Modules** over any theme, rendered through its own engine (it does not output `wp-block-*` markup). Its reputation is **stability, clean/semantic HTML, low lock-in, and a real PHP developer API** — the "freelancers start with it, agencies never outgrow it" pick, and the performance/agency contrast to feature-maximal builders. The product family is the **Beaver Builder plugin** (free **Lite** on WordPress.org + paid), the lightweight **Beaver Builder Theme**, **Beaver Themer** (theme builder + dynamic data), and **Assistant Pro** (cloud asset/template library).

It competes with Elementor, Divi, Bricks, Breakdance, Oxygen, and SeedProd; for the leanest output people pick Gutenberg block plugins, for the most templates Elementor/Divi, and for clean markup + maintainability/agency handoff people pick Beaver Builder or Bricks.

## Capabilities & automation surface

| Capability | What it does | Surface |
|---|---|---|
| **Live drag-and-drop editor** | Front-end visual editing: build with **Rows/Columns** (layout) and **Modules** (content blocks); responsive editing, undo/history, copy-paste, global rows | UI-built; output filterable via `fl_builder_*` hooks |
| **Modules** | Heading, Text Editor, Photo, Video, Button, Icon, Callout, Gallery, Slideshow, Slider, Tabs/Accordion, HTML, Sidebar, Menu, **Subscribe Form**, Contact Form, Pricing Table, Posts, Countdown, Map, etc. | UI-built; **custom modules** via PHP (`FLBuilderModule`) |
| **Templates & Saved content** | Pre-built **page/landing/content Templates**, plus **Saved Rows / Columns / Modules** (reusable, optionally **global** so one edit updates everywhere) | UI-built; exportable/importable |
| **Beaver Builder Theme** | A separate lightweight, customizer-driven theme tuned for the builder (header/footer layouts, fonts, colors) | UI-built; theme hooks |
| **Beaver Themer** *(add-on; on all paid tiers)* | Theme builder: dynamic **headers, footers, archives, singular, 404, search** templates with **Location** + **conditional/user rules** | UI-built |
| **Field Connections** *(Themer)* | Bind any row/column/module setting to **WordPress data, custom fields, ACF, EDD, The Events Calendar, BigCommerce, WooCommerce** | UI-built; extend via shortcode/PHP |
| **Loop Builder** *(Themer; on all paid tiers)* | Render dynamic post/CPT listings (grids/lists) with the Posts module + field connections | UI-built |
| **WooCommerce support** *(on all paid tiers)* | Build/customize WooCommerce templates (product, shop, cart, checkout) with Themer | UI-built |
| **Subscribe Form module** | Capture emails to a connected ESP (Mailchimp, etc.) | UI-built; extend services via `fl_builder_subscribe_form_services` |
| **White labeling** *(Unlimited only)* | Rebrand the plugin/theme for clients (name, icon, author, screenshots) | UI + `fl_builder_*` white-label filters |
| **Assistant Pro** | Cloud storage/library for templates, colors, images, and design assets synced across sites | Hosted app; UI-built |
| **Developer API** | **Custom modules** (`FLBuilderModule` + `FLBuilder::register_module()`), the large **`fl_builder_*` hooks/filters** surface, BB Theme hooks | **Developer (PHP)** — see `beaver-builder-api-reference.md` |
| **Layout data** | A page's builder layout is stored in `post_content` + the **`_fl_builder_data`** post meta (serialized) | **WordPress core REST API / WP-CLI / WP_Query** — best-effort, not a public schema |

**There is no hosted Beaver Builder REST API and no native outbound webhook.** Beaver Builder is a WordPress plugin; its programmatic surface is **WordPress core** (the WP REST API, application passwords, WP-CLI, WP_Query) **plus its own PHP API** (custom modules + `fl_builder_*` hooks). No native A/B testing, heatmaps, analytics, cart engine, or email automation — pair external tools for those.

## Pricing, limits & plan gates

*Pricing is best-effort from 2026 research (annual subscription, auto-renew, 30-day money-back guarantee) — verify on wpbeaverbuilder.com/pricing before relying on it.*

| Plan | Approx. annual | Sites | Notable inclusions |
|---|---|---|---|
| **Lite** (WordPress.org) | $0 | unlimited | Reduced module set; **no Themer, no Templates/Saved-row library**; good for trying the editor |
| **Starter** | ~$89/yr | 1 | Full plugin + Beaver Builder Theme + **Beaver Themer** + **Loop Builder** + **WooCommerce support** + Priority email support + 6 mo Assistant Pro |
| **Plus** | ~$179/yr | 3 | Everything in Starter |
| **Professional** | ~$299/yr | 50 | Everything in Plus + **Multisite** support (manage BB network-wide) + advanced training |
| **Unlimited** | ~$546/yr | unlimited | Everything in Professional + **White Labeling** + advanced training for power users |

- **Plan-gate watch-outs:** **Themer + Loop Builder + WooCommerce support ship on every paid tier** (a change from older "Themer is a separate add-on" guidance — confirm). **Multisite is Professional+**; **White Labeling is Unlimited-only**. The free **Lite** has no Themer/templates and a reduced module set.
- **Site counts** never include **staging/development sites** — those don't count toward the limit. Prorated upgrades are available.
- **No rate limit / API quota** to worry about — there's no hosted API; automation runs against your own WordPress install.
- **Affiliate / partner program:** **25% recurring** commission, **30-day cookie**, ~$100 payout threshold, PayPal monthly (wpbeaverbuilder.com/affiliates).

## Integrations

- **Theme:** works with **any** WordPress theme; ships its own optional **Beaver Builder Theme**. Full classic-theme support; pairs with page-level building rather than Full Site Editing.
- **Dynamic data (Themer Field Connections):** **WordPress** core data, **custom fields**, **ACF (Advanced Custom Fields)**, **Easy Digital Downloads**, **The Events Calendar**, **BigCommerce**, **WooCommerce** — read into any setting.
- **WooCommerce:** build/customize store templates via Themer (product/shop/cart/checkout); not a separate cart engine — WooCommerce is the cart.
- **Email/leads (data out):** the **Subscribe Form** module posts to a connected **ESP** (Mailchimp and others; extend the service list via `fl_builder_subscribe_form_services`). For arbitrary destinations, use a third-party form plugin + Zapier.
- **iPaaS:** no first-party Zapier/Make app for the builder itself; automation rides on the underlying WordPress/WooCommerce/form-plugin connectors.
- **Add-on ecosystem:** a large third-party module market (e.g. PowerPack, Ultimate Addons for Beaver Builder, Beaver Themer add-ons) extends the module set — all built on the same `FLBuilderModule` API.
- **Assistant Pro:** cloud library that syncs templates/assets across all your BB sites.

## Data model

Beaver Builder does **not** expose a documented public object schema or hosted API. A page built with Beaver Builder stores its layout in two places on the WordPress post:

- **`post_content`** — published/rendered HTML (so the page still shows content if BB is deactivated; text remains in the default editor).
- **`_fl_builder_data`** (post meta) — the serialized builder layout: an array of **nodes**, each a Row, Column, or Module with a `type`, a parent reference, and a `settings` object. There are companion meta keys (e.g. `_fl_builder_enabled`, `_fl_builder_data_settings`, draft variants). This is **internal, serialized PHP — treat it as best-effort, not a stable public schema.**

<!-- Constructed from docs/observed behavior — verify against a live install before relying on exact meta keys -->
```jsonc
// Representative shape of a single node inside _fl_builder_data (illustrative)
{
  "nodeId": "5f2a1b3c4d5e",
  "type": "module",            // "row" | "column" | "module"
  "parent": "a1b2c3d4e5f6",    // nodeId of the parent column/row (null for top-level rows)
  "position": 0,
  "settings": {
    "type": "heading",          // module slug (core or custom)
    "heading": "Welcome",
    "tag": "h1",
    "color": "111111"
  }
}
```

Read/write it through **WordPress**, not a Beaver Builder API: `GET /wp-json/wp/v2/pages/{id}` (with `context=edit` and a meta-exposing setup) or WP-CLI `wp post meta get {id} _fl_builder_data`. To create BB layouts programmatically, the supported path is the **PHP API on the server** (register modules, manipulate via `FLBuilderModel`) rather than POSTing raw serialized meta.

## Quick-start recipes

### Recipe 1 — Register a minimal custom module
**Goal:** add your own module to the editor.
```php
// my-modules.php (in your plugin)
function acme_load_bb_modules() {
    if ( class_exists( 'FLBuilder' ) ) {
        require_once 'modules/acme-button/acme-button.php';
    }
}
add_action( 'init', 'acme_load_bb_modules' );
```
```php
// modules/acme-button/acme-button.php
class AcmeButtonModule extends FLBuilderModule {
    public function __construct() {
        parent::__construct( array(
            'name'            => __( 'Acme Button', 'acme' ),
            'description'     => __( 'A custom CTA button.', 'acme' ),
            'group'           => __( 'Acme Modules', 'acme' ),
            'category'        => __( 'Acme', 'acme' ),
            'dir'             => ACME_MODULES_DIR . 'acme-button/',
            'url'             => ACME_MODULES_URL . 'acme-button/',
            'icon'            => 'button.svg',
            'editor_export'   => true,
            'enabled'         => true,
            'partial_refresh' => false,
        ) );
    }
}
FLBuilder::register_module( 'AcmeButtonModule', array(
    'general' => array(
        'title'    => __( 'General', 'acme' ),
        'sections' => array(
            'content' => array(
                'title'  => __( 'Content', 'acme' ),
                'fields' => array(
                    'text' => array( 'type' => 'text',  'label' => __( 'Button Text', 'acme' ) ),
                    'url'  => array( 'type' => 'link',  'label' => __( 'Button URL', 'acme' ) ),
                ),
            ),
        ),
    ),
) );
```
**Gotchas:** use a **prefixed, dash-separated slug** (`acme-button`) to avoid colliding with core modules; render markup in the module's `frontend.php`; always guard with `class_exists( 'FLBuilder' )`.

### Recipe 2 — Read a page's builder layout via the WordPress REST API
**Goal:** export/inspect what a page contains without opening the editor.
```bash
# Requires an application password and the meta to be REST-exposed
curl -s -u "user:application_password" \
  "https://example.com/wp-json/wp/v2/pages/123?context=edit" | jq '.content.rendered'

# Or pull the raw serialized layout with WP-CLI on the server:
wp post meta get 123 _fl_builder_data --format=json
```
```python
import requests
r = requests.get(
    "https://example.com/wp-json/wp/v2/pages/123",
    params={"context": "edit"},
    auth=("user", "application_password"),
    timeout=30,
)
page = r.json()
print(page["content"]["rendered"])   # rendered HTML; _fl_builder_data is serialized PHP, read via WP-CLI/PHP
```
**Gotchas:** `_fl_builder_data` is **serialized PHP**, not JSON — read/parse it server-side (WP-CLI/PHP), don't try to POST a hand-built blob. There's no Beaver Builder endpoint; this is plain WordPress.

### Recipe 3 — Capture leads from the Subscribe Form into your ESP
**Goal:** wire opt-ins to email automation.
- In the editor, add the **Subscribe Form** module → choose your **service** (e.g. Mailchimp) → connect the account/list. The module submits directly to the ESP.
- To add an unsupported ESP, register it on the PHP side with the **`fl_builder_subscribe_form_services`** filter (see `beaver-builder-api-reference.md`).
- For arbitrary destinations (CRM/webhook), use a third-party form plugin (with webhook/Zapier output) instead of the core Subscribe Form, then trigger your sequence in `/sales-email-marketing`.

## Integration patterns

- **No hosted webhook → poll or hook in PHP.** Since BB emits no outbound webhook, "notify on new page/lead" patterns must use **WordPress** mechanisms: a `save_post`/`publish_page` action that `fetch`es your endpoint, or a form plugin's own webhook for leads. Own the retries/signing/logging yourself.
- **Reading content programmatically.** Use the **WordPress REST API** (`/wp/v2/pages`, `/wp/v2/posts`) for rendered HTML and WP-CLI/PHP for `_fl_builder_data`. For dynamic/templated content built with Themer, the *rendered* output already includes the resolved Field Connections.
- **Migrating sites safely.** Beaver Builder stores serialized layout data, so **always use a serialized-data-safe search-replace** (WP-CLI `search-replace --all-tables` or a proper migration plugin) — a naive SQL find-replace breaks layouts and is the usual cause of "builder deactivated on all pages but the home page."
- **Performance pipeline.** Clean markup helps but isn't enough at scale: image optimization (right size + WebP), a caching/minification plugin (exclude the editor screens), fewer heavy modules per page, and splitting long pages. Re-test with PageSpeed Insights.
- **A/B testing / heatmaps.** Not native — layer **VWO** (split testing) or **Microsoft Clarity** (heatmaps/recordings) on top.
