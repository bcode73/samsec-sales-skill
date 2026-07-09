<!-- Source: https://wpspectra.com/docs/public-actions-and-hooks-v3/ and https://wpspectra.com/docs/filters-actions-for-post/ and https://wpspectra.com/docs/controlling-access/ -->

# Spectra Developer Reference — Public Actions & Hooks

Spectra is a WordPress plugin. It has **no hosted REST API** and **no native outbound webhook**. Its programmatic surface is:

1. **WordPress core** — the WP REST API (`/wp-json/wp/v2/...`), application-password auth, and WP-CLI. Spectra block content lives in the `post_content` field as `uagb/`-namespaced block markup.
2. **Spectra's own public actions & filters** (PHP `add_action` / `add_filter`) — to extend, modify, or hook into block rendering, queries, assets, Global Styles, and REST controllers.

> Hook names below are reproduced verbatim from Spectra's public documentation. Parameter signatures should be confirmed against your installed Spectra/Spectra Pro version before relying on them.

## Authentication quick-start (WordPress core, not Spectra-specific)

```bash
# Read a page's Spectra block markup with an application password
curl -s https://example.com/wp-json/wp/v2/pages/123 \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" | jq '.content.rendered'
```

Generate an application password under **Users → Profile → Application Passwords**. The token inherits that user's capabilities.

## Public actions & filters (Spectra v3)

### Block management

| Hook | Type | Purpose |
|---|---|---|
| `block_categories_all` | Filter | Modify block categories shown in the editor |
| `block_type_metadata_settings` | Filter | Configure block settings during registration |

### Extension asset hooks

| Hook | Type | Purpose |
|---|---|---|
| `spectra_3_extensions_editor_assets` | Action | Fires after enqueuing editor assets for extensions |
| `spectra_pro_2_extensions_editor_assets` | Action | Fires after enqueuing editor assets for Spectra Pro v2 extensions |

### Block rendering

| Hook | Type | Purpose |
|---|---|---|
| `render_block` | Filter | Modify block content during rendering (WordPress core filter) |
| `render_block_data` | Filter | Process block data before rendering (WordPress core filter) |
| `spectra_blocks_responsive_default_layout` | Filter | Modify default layout configurations for responsive controls |
| `spectra_enable_css_cache` | Filter | Control whether responsive CSS caching is enabled |
| `spectra_responsive_attr_definitions` | Filter | Modify responsive attribute definitions for block-specific CSS generation |

### Global Styles

| Hook | Type | Purpose |
|---|---|---|
| `spectra_pro_gs_theme_colors` | Filter | Modify theme colors for the Global Styles system |

### REST API

| Hook | Type | Purpose |
|---|---|---|
| `spectra_pro_rest_api_get_controllers` | Filter | Add/modify REST API controllers for Spectra Pro v2 (push a `WP_REST_Controller` subclass onto the array) |

### Block-specific

| Hook | Type | Purpose |
|---|---|---|
| `spectra_countdown_context` | Filter | Modify Countdown block context before rendering |
| `spectra_slider_params` | Filter | Modify Swiper parameters for slider blocks |
| `spectra_slider_modules` | Filter | Add Swiper modules |
| `spectra_icon_chunks` | Filter | Add custom icons |

### WordPress standard hooks Spectra relies on

| Hook | Type |
|---|---|
| `wp_enqueue_scripts` | Action |
| `enqueue_block_editor_assets` | Action |
| `save_post` | Action |

## Post block query filters (Post Grid / Masonry / Carousel / Timeline)

These filters modify the `WP_Query` arguments for the dynamic post blocks. Signature: `( array $query_args, array $attributes )`.

| Hook | Block |
|---|---|
| `uagb_post_query_args_grid` | Post Grid |
| `uagb_post_query_args_masonry` | Post Masonry |
| `uagb_post_query_args_carousel` | Post Carousel |
| `uagb_post_query_args_timeline` | Post Timeline |

```php
// Limit the Post Grid block to a custom post type and exclude one category
add_filter( 'uagb_post_query_args_grid', function ( $args, $attributes ) {
    $args['post_type']        = 'portfolio';
    $args['category__not_in'] = [ 12 ];
    return $args;
}, 10, 2 );
```

> The `uagb_` prefix is a legacy of the plugin's former name, **Ultimate Addons for Gutenberg (UAG)**. Newer hooks use the `spectra_` prefix.

## Register a custom REST controller (Spectra Pro v2)

```php
add_filter( 'spectra_pro_rest_api_get_controllers', function ( $controllers ) {
    $controllers[] = 'My_Spectra_REST_Controller';
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

This filter only exists when **Spectra Pro v2** is active.

## Controlling Spectra design-library access by user role

Spectra's Starter Templates / design library is gated by a capability. Add roles that should reach it with the Astra/Spectra capability filter:

```php
// Allow Editors (not just Admins) to use the Spectra design library
add_filter( 'ast_block_template_capability_additional_roles', function ( $roles ) {
    $roles[] = 'editor';
    return $roles;
} );
```

## Gaps / not documented

- **No public hosted REST API** for Spectra objects — use the WordPress core REST API against posts/pages, whose `content` holds the `uagb/` block markup.
- **No native outbound webhook** — form-lead delivery rides on the connected form/ESP plugin, not Spectra.
- **No first-party Zapier/Make app** for Spectra itself.
- Full parameter signatures and the complete hook list may evolve per release; confirm against `wpspectra.com/docs` and the installed version. Source pages: `public-actions-and-hooks-v3`, `filters-actions-for-post`, `controlling-access`.
