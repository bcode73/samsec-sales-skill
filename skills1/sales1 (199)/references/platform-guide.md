# GenerateBlocks Platform Reference

## Overview

GenerateBlocks is a minimalist, performance-focused **Gutenberg block plugin** for WordPress by **Tom Usborne / EDGE22 Studios LTD** — the same team behind the **GeneratePress** theme. 200,000+ active installs (v2.x). Its pitch: "add incredible versatility to your editor without bloating it with tons of one-dimensional blocks." Instead of dozens of single-purpose widgets, it ships a few **composable primitives** (Container, Grid) plus Headline, Button, Image, and a Query Loop — you build pricing tables, testimonials, hero sections, etc. out of those. It works with any theme but pairs natively with GeneratePress for the leanest possible stack. It is the **performance/clean-markup** pick among block plugins; the dev-leaning rival to Kadence Blocks, Spectra, and Stackable.

**GenerateBlocks 2.0 was a ground-up rewrite** (2024): a new Styles engine, a unified **Query Loop**, and **Dynamic Tags** (custom dynamic data sources you can register in code). Tutorials predating 2.0 may not match the current editor.

## Capabilities & automation surface

| Capability | What it does | Surface |
|---|---|---|
| **Container block** | Flexbox section/row/column layout primitive — the backbone of every layout | UI-built; output filterable via `render_block` |
| **Grid block** | Advanced flexible/responsive grids | UI-built |
| **Headline block** | Text-rich headings/paragraphs with granular typography | UI-built; Dynamic Data-capable (Pro) |
| **Button block** | Buttons/CTAs | UI-built; Dynamic Data-capable (Pro) |
| **Image block** | Static or dynamic images | UI-built; Dynamic Data-capable (Pro); `generateblocks_image_url` filter |
| **Query Loop block** | Build post lists from any post type (blog/portfolio/CPT grids) | UI-built (free); query is standard `WP_Query` |
| **Dynamic Data** | Bind block content to post title/excerpt/date/meta (incl. ACF, deeply-nested arrays)/terms/author/user fields/comments count, and featured/meta/avatar images | **Pro**, UI-built; filterable + extensible via custom dynamic tags |
| **Global Styles** | Apply reusable styles site-wide from one place | **Pro**, UI-only |
| **Asset / pattern library** | 150+ professional templates/patterns inside the editor | **Pro**, UI-only |
| **Device Visibility** | Show/hide blocks per device (desktop/tablet/mobile) | **Pro**, UI-only |
| **Shape dividers, gradients, scroll effects, custom attributes** | Advanced design/animation controls | **Pro**, UI-only |
| **Custom dynamic tags** | Register your own dynamic data sources | **Developer (PHP)** — `GenerateBlocks_Register_Dynamic_Tag`, see `generateblocks-api-reference.md` |
| **Public hooks/filters** | Modify dynamic tag/content output, image URLs, CSS content sources | **Developer (PHP hooks)** — see `generateblocks-api-reference.md` |

**There is no hosted REST API and no native outbound webhook.** GenerateBlocks is a WordPress plugin; its programmatic surface is WordPress core (the WP REST API, application passwords, WP-CLI) plus GenerateBlocks' own PHP **actions, filters, and the dynamic-tag registration API**. Form lead capture is not built in — pair a form plugin and use its delivery.

## Pricing, limits & plan gates

*Pricing is best-effort from 2026 research, annual, and intro-priced — verify on generateblocks.com/pricing (and generatepress.com) before relying on it.*

| Plan | Approx. price | Sites | Notable inclusions |
|---|---|---|---|
| **Free** (WordPress.org) | $0 | unlimited | Container, Grid, Headline, Button, Image, **Query Loop**; granular typography/spacing/colors/SVG icons; clean HTML5 output |
| **Pro — Personal** | ~$59/yr | **1** | Everything free + Dynamic Data, Global Styles, 150+ templates/asset library, device visibility, shape dividers, gradients, scroll effects, custom attributes |
| **Pro — Professional** | ~$99/yr | up to **500** | Same Pro feature set, more sites |
| **GeneratePress One** (bundle) | ~$149/yr | up to **500** | GP Premium + **GenerateBlocks Pro** + GenerateCloud |

- **30-day money-back guarantee.** Pro is intro-priced and renews at full rate — flag this.
- **Plan-gate watch-outs:** Dynamic Data, Global Styles, the asset/template library, device visibility, shape dividers, gradients, scroll effects, and custom attributes are **Pro**. Pages built on Pro-only features can **degrade/lose styling** if Pro is deactivated/expired.
- **No native A/B testing, heatmaps, analytics, cart, or email** on any tier.
- **Affiliate program:** ~25% commission, 30-day cookie, $75 minimum payout, PayPal monthly (generateblocks.com/affiliates/).

## Integrations

- **Theme:** any theme; optimized for **GeneratePress** (lightest combined stack). Works inside the standard Gutenberg/block editor and block (FSE) themes.
- **Dynamic data sources:** **ACF** and post meta are first-class via Dynamic Data; deeply-nested meta arrays are addressable by key. Custom sources can be registered as dynamic tags in PHP.
- **Forms / leads (data out):** GenerateBlocks has **no form block and no webhook** — pair a form plugin (e.g. GenerateBlocks is often used with a separate forms plugin) and use that plugin's ESP/webhook delivery.
- **Commerce:** no native cart — add WooCommerce, or pair a WooCommerce funnel plugin (CartFlows/FunnelKit) for checkout + upsells. Use `/sales-checkout` for strategy.
- **iPaaS:** no first-party Zapier/Make app for GenerateBlocks itself; automation rides on the underlying WordPress/WooCommerce/form plugin's connectors.

## Data model

GenerateBlocks has **no remote object model/API**. Its "data" is **WordPress block markup** stored in `post_content`, plus plugin settings in `wp_options` and generated CSS.

A GenerateBlocks block in `post_content` is a standard Gutenberg block comment with a `generateblocks/`-namespaced name and a JSON attributes object:

```html
<!-- wp:generateblocks/element {"uniqueId":"a1b2c3d4","tagName":"div","styles":{"display":"flex","flexDirection":"row"}} -->
<div class="gb-element-a1b2c3d4">
  <!-- wp:generateblocks/query {"uniqueId":"e5f6g7h8","query":{"post_type":"post","posts_per_page":6}} -->
    <!-- wp:generateblocks/looper -->
      <!-- wp:generateblocks/text {"uniqueId":"i9j0k1l2","tagName":"h2"} /-->
    <!-- /wp:generateblocks/looper -->
  <!-- /wp:generateblocks/query -->
</div>
<!-- /wp:generateblocks/element -->
```

<!-- Constructed from docs/observed 2.x markup — block names/attributes evolve per release; verify against a live install -->

> Block names changed in the 2.0 rewrite (e.g. unified element/query/looper blocks). Confirm exact `generateblocks/*` names and attribute keys against your installed version — copy a real block from the editor as the source of truth.

To read or modify GenerateBlocks content programmatically, use the **WordPress REST API** for posts/pages (block markup is in the `content` field) or `get_post`/`wp_update_post` in PHP. There is no GenerateBlocks-specific record endpoint.

```bash
# Read a page's block markup via the WordPress REST API (application password auth)
curl -s https://example.com/wp-json/wp/v2/pages/123 \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" | jq '.content.rendered'
```

## Quick-start recipes

### Recipe 1 — Register a custom dynamic tag (GenerateBlocks 2.0+)

**Trigger:** you need a dynamic data source GenerateBlocks doesn't ship (e.g. an external value, a computed field).
**Steps:** instantiate `GenerateBlocks_Register_Dynamic_Tag` on `init` with a config array and a `return` callback; emit output through the helper so truncation/link-wrapping still work.

```php
// functions.php or a small mu-plugin
add_action( 'init', function () {
    if ( ! class_exists( 'GenerateBlocks_Register_Dynamic_Tag' ) ) {
        return; // GenerateBlocks Pro 2.0+ not active
    }

    new GenerateBlocks_Register_Dynamic_Tag(
        [
            'title'    => __( 'Reading Time', 'mytheme' ),
            'tag'      => 'reading_time',
            'type'     => 'post',
            'supports' => [ 'source' ],
            'return'   => 'mytheme_reading_time_callback',
        ]
    );
} );

function mytheme_reading_time_callback( $options, $block, $instance ) {
    $post_id = $options['id'] ?? get_the_ID();
    $words   = str_word_count( wp_strip_all_tags( get_post_field( 'post_content', $post_id ) ) );
    $minutes = max( 1, (int) ceil( $words / 200 ) );
    $content = sprintf( '%d min read', $minutes );

    return GenerateBlocks_Dynamic_Tag_Callbacks::output( $content, $options, $instance );
}
```

**Gotcha:** `GenerateBlocks_Register_Dynamic_Tag` is **Pro 2.0+** only — guard with `class_exists()`. Exact `supports`/`options` keys evolve; confirm against the installed version.

### Recipe 2 — Build a custom-post-type grid with Dynamic Data

**Trigger:** show a grid of a CPT with a custom-field value and the featured image.
**Steps:** (in the editor) add a **Query Loop**, set its `WP_Query` to the CPT; inside the loop add a Headline bound (Dynamic Data) to the post title, another Headline bound to the post-meta/ACF field, and an Image block bound to the featured image. Tune the query in code if needed:

```php
// Adjust the WP_Query for a GenerateBlocks Query Loop (filter the standard query)
// GenerateBlocks Query Loop uses core WP_Query; target it via pre_get_posts on your CPT/template,
// or build the query in a custom dynamic source. Example: exclude a category sitewide on the CPT archive.
add_action( 'pre_get_posts', function ( $q ) {
    if ( is_admin() || ! $q->is_main_query() ) {
        return;
    }
    if ( is_post_type_archive( 'portfolio' ) ) {
        $q->set( 'category__not_in', [ 12 ] );
    }
} );
```

**Gotcha:** Query Loop is **free**, but **Dynamic Data binding is Pro**. Without Pro you can loop but not bind post meta/ACF into the inner blocks.

### Recipe 3 — Filter dynamic-tag / dynamic-content output

**Trigger:** post-process what a dynamic tag prints (sanitize, append a suffix, swap an image URL).
**Steps:** hook the output filter for your GenerateBlocks version.

```php
// 2.0+ dynamic tag output
add_filter( 'generateblocks_dynamic_tag_output', function ( $output, $options ) {
    // e.g. append a unit to a numeric meta value
    return $output;
}, 10, 2 );

// 1.x legacy dynamic content output (and related image fallbacks)
add_filter( 'generateblocks_dynamic_content_output', fn( $output ) => $output, 10, 1 );
add_filter( 'generateblocks_image_url', fn( $url ) => $url, 10, 1 );
```

## Integration patterns

- **Programmatic page creation:** there is no "create a GenerateBlocks page" API. Create/update a WP post/page via the WordPress REST API or `wp_insert_post`, writing **`generateblocks/`-namespaced block markup** into `content`. Build the layout once in the editor, copy the markup, and template it (mind the `uniqueId` attributes — keep them unique).
- **Lead/data out:** GenerateBlocks emits no webhook and has no form block. Capture leads through a paired form plugin's webhook/ESP integration, or read submissions/orders from the underlying plugin (form plugin, WooCommerce REST).
- **Asset/cache pipeline:** GenerateBlocks generates block CSS per page. After bulk content changes, a migration, or a major version jump, re-save affected pages and clear page/object/CDN cache, or inner pages render unstyled.
- **Extending blocks:** prefer the documented filters (`generateblocks_dynamic_tag_output`, `generateblocks_dynamic_content_output`, `generateblocks_do_content`, `generateblocks_image_url`, `generateblocks_dynamic_image_fallback`) and the dynamic-tag registration API over editing block markup, so changes survive updates. See `references/generateblocks-api-reference.md`.
- **Performance posture:** GenerateBlocks is already lean. For Core Web Vitals, optimize the theme, images (use the Image block + featured-image dynamic data, serve modern formats), and third-party scripts first. GeneratePress + GenerateBlocks + a caching plugin is the standard fast stack.
