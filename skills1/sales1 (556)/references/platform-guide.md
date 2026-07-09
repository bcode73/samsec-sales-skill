# Spectra Platform Reference

## Overview

Spectra is a Gutenberg-native WordPress website/page builder plugin by **Brainstorm Force** (the team behind the Astra theme, CartFlows, and SureCart). It was formerly **Ultimate Addons for Gutenberg (UAG)** — which is why many of its hooks and CSS classes still use the `uagb_` prefix. It extends the **native block editor** (rather than replacing it like Elementor/Divi) with 30+ advanced blocks, a flexbox Container, Starter Templates, a Popup Builder, and animations. 1M+ active installs. Differentiator: leaner DOM output and "build on Gutenberg, don't replace it." Companion full-site-editing block theme: **Spectra One**.

## Capabilities & automation surface

| Capability | What it does | Surface |
|---|---|---|
| 30+ blocks (Container, Heading, Buttons, Info Box, Post Grid/Masonry/Carousel, Sliders, Tabs, FAQ, Forms, Table of Contents, Countdown, Testimonials, Team, Icon List, Lottie…) | Page/layout building inside the block editor | UI-built; output filterable via `render_block` / block-specific filters |
| Container block (flexbox) | Sections/rows/columns layout primitive | UI-only |
| Starter Templates / template kits | Import full sites, pages, and section patterns | UI-only (Astra Starter Templates engine) |
| Popup Builder | Modal/exit-intent popups | UI-only |
| Coming Soon mode | Sitewide pre-launch/maintenance page | UI-only |
| Animations | Fade/slide/zoom/flip on scroll or loop | UI-only |
| Local Google Fonts | Self-host fonts for GDPR/perf | UI-only |
| Global Styles / Copy-Paste / Presets | Site-wide block styling and reuse | UI-only; theme colors filterable via `spectra_pro_gs_theme_colors` |
| Spectra AI | In-editor AI assistance | UI-only |
| **Loop Builder** | Dynamic query loops / custom post displays | **Pro**, UI-built; queries filterable via `uagb_post_query_args_*` |
| **Dynamic Content** | Bind block content to post meta, ACF, featured image, site data | **Pro**, UI-only |
| **Display Conditions** | Show/hide blocks by user role, login, date, etc. | **Pro**, UI-only |
| **Role permissions / white label** | Restrict editor features by role; rebrand the plugin | **Pro**, UI-only; design-library access via `ast_block_template_capability_additional_roles` |
| Forms (Contact/Newsletter, reCAPTCHA) | Lead capture; submissions to email/ESP | UI-built; **no native outbound webhook** — data exits via the form/ESP integration |
| Public actions & filters | Extend/modify block rendering, queries, assets, REST controllers | **Developer (PHP hooks)** — see `spectra-api-reference.md` |

**There is no hosted REST API and no native outbound webhook.** Spectra is a WordPress plugin; its programmatic surface is WordPress core (the WP REST API, application passwords, WP-CLI) plus Spectra's own PHP **actions and filters**.

## Pricing, limits & plan gates

*Pricing is best-effort from 2026 research, annual, and intro-priced — verify on wpspectra.com/pricing before relying on it. Lifetime deals exist.*

| Plan | Approx. price | Sites | Notable inclusions |
|---|---|---|---|
| **Free** (WordPress.org) | $0 | unlimited | 30+ blocks, Container, Starter Templates, Popup Builder, Coming Soon, animations, local fonts, Spectra AI block |
| **Spectra Pro** | ~$49–69/yr (lifetime ~$199) | 1–3 | Everything free + Loop Builder, Dynamic Content, display conditions, role permissions, white label, extra blocks, finer styling (shadows/gradients/borders) |
| **Essential Toolkit** | ~$79–119/yr (lifetime ~$399) | ~10 | Spectra Pro + **Astra Pro theme**, Premium Starter Templates, Ultimate Addons for Elementor |
| **Business Toolkit** | ~$149–159/yr (lifetime ~$599) | ~1,000 | Essential + SureFeedback, SureWriter, bonus software (CartFlows, OttoKit, ZipWP, etc.) |

- **14-day money-back guarantee.** Priority support on paid tiers.
- **Plan-gate watch-outs:** Loop Builder, Dynamic Content, display conditions, white label, and role permissions are **Pro**. Pages built on Pro-only blocks **fall back to fallback content** if Pro is deactivated/expired.
- **No native A/B testing, heatmaps, or analytics** on any tier.

## Integrations

- **Themes:** works with any theme; optimized for **Spectra One**, Astra, Blocksy, GeneratePress, Kadence, Neve.
- **Plugins (data flows into Spectra blocks/templates):** WooCommerce, Gravity Forms, FluentForms, FluentCRM, SureCart, MemberPress, LearnDash, TutorLMS, GiveWP, PrestoPlayer, The Events Calendar, Yoast SEO.
- **Forms → ESP/CRM (data out):** Spectra's form blocks send submissions to email/ESP via the configured integration; there is **no Spectra webhook** — for arbitrary destinations, route through the connected form plugin (e.g. Gravity Forms/FluentForms) or a generic iPaaS connector.
- **iPaaS:** no first-party Zapier/Make app for Spectra itself; automation rides on the underlying form/WooCommerce/CRM plugin's connectors.

## Data model

Spectra has **no remote object model/API**. Its "data" is **WordPress block markup** stored in `post_content`, plus Spectra settings in `wp_options` and generated CSS assets.

A Spectra block in `post_content` looks like a standard Gutenberg block comment with a `uagb/`-namespaced block name and a JSON attributes object:

```html
<!-- wp:uagb/container {"block_id":"a1b2c3d4","variantSelected":"flex","directionDesktop":"row"} -->
<div class="wp-block-uagb-container uagb-block-a1b2c3d4 ...">
  <!-- wp:uagb/post-grid {"block_id":"e5f6g7h8","postType":"post","postsToShow":6,"taxonomyType":"category"} /-->
</div>
<!-- /wp:uagb/container -->
```

<!-- Constructed from docs/observed markup — verify against a live install -->

To read or modify Spectra content programmatically, use the **WordPress REST API** for posts/pages (block markup is in the `content` field), or `get_post`/`wp_update_post` in PHP. There is no Spectra-specific record endpoint.

```bash
# Read a page's block markup via the WordPress REST API (application password auth)
curl -s https://example.com/wp-json/wp/v2/pages/123 \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" | jq '.content.rendered'
```

## Quick-start recipes

### Recipe 1 — Register a custom REST controller for Spectra Pro

**Trigger:** you want your own REST endpoint registered alongside Spectra Pro's.
**Steps:** hook `spectra_pro_rest_api_get_controllers`, append your controller class, implement `register_routes()`.

```php
// functions.php or a small mu-plugin
add_filter( 'spectra_pro_rest_api_get_controllers', function ( $controllers ) {
    $controllers[] = 'My_Spectra_REST_Controller'; // extends WP_REST_Controller
    return $controllers;
} );

class My_Spectra_REST_Controller extends WP_REST_Controller {
    public function register_routes() {
        register_rest_route( 'my-spectra/v1', '/ping', [
            'methods'             => 'GET',
            'callback'            => fn() => rest_ensure_response( [ 'ok' => true ] ),
            'permission_callback' => fn() => current_user_can( 'edit_posts' ),
        ] );
    }
}
```

```bash
# Then call it with an application password
curl -s https://example.com/wp-json/my-spectra/v1/ping \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx"
```

**Gotcha:** the filter is **Spectra Pro v2**-specific; it won't exist on the free plugin.

### Recipe 2 — Change what the Post Grid block queries

**Trigger:** the Post Grid/Masonry/Carousel block should pull a custom post type, exclude a category, or change ordering.
**Steps:** filter the matching `uagb_post_query_args_*` hook and modify the `WP_Query` args.

```php
// Exclude the "news" category from every Spectra Post Grid block
add_filter( 'uagb_post_query_args_grid', function ( $args, $attributes ) {
    $args['category__not_in'] = [ 12 ]; // term_id of "news"
    return $args;
}, 10, 2 );
// Variants: uagb_post_query_args_masonry, uagb_post_query_args_carousel, uagb_post_query_args_timeline
```

### Recipe 3 — Fix Spectra CSS not loading on inner pages

**Trigger:** blocks render correct on the homepage, broken elsewhere.
**Steps:** programmatically (or in Settings) ensure assets regenerate and aren't cached stale.

```php
// Force Spectra to regenerate its file-based assets (run once, e.g. via WP-CLI eval)
if ( class_exists( 'UAGB_Helper' ) && method_exists( 'UAGB_Admin_Helper', 'create_specific_stylesheet' ) ) {
    UAGB_Admin_Helper::create_specific_stylesheet();
}
// Or in the UI: Spectra → Settings → set "Generate CSS/JS File" then "Regenerate Assets", then clear page cache + CDN.
```

**Gotcha:** an aggressive minify/optimization plugin can strip the inline/critical CSS — allowlist the Spectra uploads asset path.

## Integration patterns

- **Programmatic page creation:** there is no "create a Spectra page" API. Create/update a WP post/page via the WordPress REST API or `wp_insert_post`, writing **`uagb/`-namespaced block markup** into `content`. Build the markup once in the editor, copy it, and template it.
- **Lead/data out:** Spectra emits no webhook. Capture form leads through the connected form plugin's webhook/ESP, or read submissions/orders from the underlying plugin (Gravity Forms, FluentForms, WooCommerce REST).
- **Asset/cache pipeline:** Spectra generates per-page CSS/JS files cached under `wp-content/uploads`. After bulk content changes or migrations, **regenerate assets** and clear page/object/CDN cache, or inner pages render unstyled.
- **Extending blocks:** prefer the documented filters (`render_block`, `uagb_post_query_args_*`, `spectra_slider_params`, `spectra_countdown_context`, `spectra_icon_chunks`, `spectra_pro_gs_theme_colors`) over editing block markup, so changes survive plugin updates. See `references/spectra-api-reference.md`.
