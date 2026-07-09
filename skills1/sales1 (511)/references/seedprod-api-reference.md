<!-- Source: https://www.seedprod.com/announcement-abilities-api/ , https://www.seedprod.com/docs-categories/developer/ , https://www.seedprod.com/docs/permission-filters/ , https://www.seedprod.com/docs/seedprod-shortcodes/ -->

# SeedProd Developer / Automation Reference

SeedProd is a WordPress plugin, not a hosted SaaS — there is **no public outbound REST API and no native webhook surface**. Its programmatic surface is: (1) the **WordPress Abilities API** integration (the primary remote/AI automation path), (2) **permission filters** (PHP), (3) **shortcodes**, and (4) developer escape-hatch **filters**. Downstream data movement is via the connected ESP or **Zapier (Pro+)**.

---

## 1. Abilities API (WordPress 6.9 Abilities API)

> SeedProd integrates with WordPress 6.9's Abilities API — "a new standard in WordPress 6.9 that lets plugins register named actions and expose them to any REST API client." Connected tools like **WPVibe** and **Claude** "automatically discover what SeedProd can do and trigger it directly, without touching the dashboard."

**Requirements:** WordPress **6.9+**, SeedProd **6.20.0+**. Registers **automatically** — no separate configuration.

### Exposed abilities (v6.20.0+)

| Ability | What it does |
|---|---|
| `get-status` | Returns SeedProd's current operational state including coming-soon mode, maintenance mode, theme-builder status, and license information. |
| `toggle-coming-soon` | Enables or disables coming-soon mode. |
| `toggle-maintenance` | Enables or disables maintenance mode. |
| `list-pages` | Returns all SeedProd pages with their IDs. |
| `save-page` | Creates or updates a SeedProd page. |
| `toggle-theme` | Enables or disables the SeedProd theme builder. |
| `import-theme` | Imports a SeedProd theme from a ZIP URL. |
| `activate-license` | Activates a Pro license key. |

**Authentication & invocation:** The announcement provides no auth details or code examples. Abilities are exposed "to any REST API client" through the WordPress Abilities API, so the standard WordPress REST authentication applies — typically an **application password** (Users → Profile → Application Passwords) sent over HTTPS, or cookie + nonce for first-party requests. Discover the exact route/namespace from the site's Abilities API index rather than hard-coding it.

<!-- Constructed from docs — verify exact route against your WP/SeedProd version -->
```bash
# Pattern only — confirm the ability route via the Abilities API index on your site.
curl -s https://example.com/wp-json/wp/v2/abilities/seedprod/get-status \
  -u "wpuser:APPLICATION_PASSWORD"

curl -s -X POST https://example.com/wp-json/wp/v2/abilities/seedprod/toggle-coming-soon \
  -u "wpuser:APPLICATION_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'
```

---

## 2. Permission filters

> "SeedProd provides a set of WordPress filters that let you control which user roles and capabilities can access different areas of the SeedProd interface." Use them in your theme's `functions.php` or a custom plugin.

**Menu / interface access filters** — default capability `edit_others_posts`:
- `seedprod_main_menu_capability`
- `seedprod_dashboard_menu_capability`
- `seedprod_subscribers_menu_capability`
- `seedprod_growthtools_menu_capability`
- `seedprod_settings_menu_capability`
- `seedprod_templates_menu_capability`
- `seedprod_builder_menu_capability`

**Page-management action filters** — default capability `list_users`:
- `seedprod_delete_subscriber_capability`
- `seedprod_unarchive_pages_capability`
- `seedprod_archive_pages_capability`
- `seedprod_trash_pages_capability`

**Plugin-management action filters:**
- `seedprod_install_plugins_capability` — defaults to `install_plugins`
- `seedprod_update_plugins_capability` — defaults to `update_plugins`
- `seedprod_activate_plugins_capability` — defaults to `activate_plugins`

**Example** — restrict the builder to administrators:
```php
add_filter( 'seedprod_builder_menu_capability', function() {
    return 'manage_options';
} );
```
Apply the same pattern to any filter, substituting the hook name and desired WordPress capability.

---

## 3. Developer escape-hatch filters (WooCommerce / theme load)

- `seedprod_pro_remove_brw_hooks` — if a theme has heavily customized WooCommerce templates and the SeedProd WooCommerce Theme Builder is on, this filter keeps some hooks attached.
- `seedprod_disable_theme_load` — the developer escape hatch to keep the underlying (non-SeedProd) theme active on specific URLs.

---

## 4. Shortcodes

SeedProd includes built-in shortcodes that power its blocks and template tags. Verbatim list:

| Shortcode | Renders |
|---|---|
| `[businessreview]` | Business Reviews block, pulling reviews from Google Places or Yelp. |
| `[sp_edd_downloads_grid]` | Easy Digital Downloads product grid. |
| `[sp_buy_now_button]` | EDD Buy Now button for a specific product. |
| `[sp_edd_cart]` | EDD cart section or page. |
| `[sp_edd_checkout]` | EDD checkout section or page. |
| `[sp_edd_add_to_cart]` | SeedProd EDD Add to Cart button for the current product. |
| `[defaultposts]` | Posts from the current query string. |
| `[customposts]` | Posts using custom query filters (post type, categories, tags, authors). |
| `[manualposts]` | A manually selected set of posts. |
| `[sp_archive_products]` | WooCommerce product archive (Shop pages, category/tag archives). |
| `[seedprodnestedmenuwidget]` | A selected WordPress navigation menu inside the builder. |
| `[seedprodwpwidget]` | A selected WordPress widget inside the builder. |
| `[seedprod_get_permalink]` | Permalink of the current post or page. |
| `[seedprod]` | WordPress template tags for SeedProd page/theme templates. |
| `[seedprod_edd]` | Easy Digital Downloads template tags inside SeedProd templates. |
| `[seedprod_wc]` | WooCommerce template tags inside SeedProd templates. |
| `[sp_template_part]` | A saved SeedProd template part by its ID. |
| `[sp_custom_field]` | Value of a custom field (post meta) for a specified post. |
| `[sp_menu_cart]` | WooCommerce Menu Cart block. |
| `[sp_add_to_cart]` | SeedProd WooCommerce Add to Cart button for the current product. |
| `[sp_product_meta]` | WooCommerce product meta (SKU, categories, tags). |
| `[sp_product_data_tabs]` | WooCommerce product data tabs for the current product. |
| `[sp_product_gallery_images]` | WooCommerce product gallery image carousel. |
| `[sp_additional_info]` | WooCommerce product additional-information tab content. |
| `[sp_product_related]` | WooCommerce related-products section. |
| `[sp_product_upsells]` | WooCommerce upsell-products section. |
| `[sp_product_rating]` | WooCommerce product star rating. |
| `[sp_product_stock]` | WooCommerce product stock status. |
| `[seed_contact_form]` | Legacy SeedProd contact form. |

---

## Gaps

- **No public outbound REST API** for external SaaS-style calls and **no native webhook** — lead/subscriber data exits via the connected ESP or Zapier (Pro+), not via SeedProd.
- **Abilities API auth, exact REST routes, and request/response schemas are not documented** in the announcement; verify against the live Abilities API index on your WordPress site and the running SeedProd version.
- Shortcode **parameters/attributes** are not enumerated in the public shortcode reference; confirm in-app.
