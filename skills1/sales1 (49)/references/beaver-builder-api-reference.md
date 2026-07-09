<!-- Source: https://docs.wpbeaverbuilder.com/beaver-builder/developer/ , https://docs.wpbeaverbuilder.com/beaver-builder/developer/custom-modules/ , https://docs.wpbeaverbuilder.com/beaver-builder/developer/tutorials-guides/common-beaver-builder-plugin-filter-examples/ , https://hooks.wpbeaverbuilder.com/ (fetched 2026-06-29) -->

# Beaver Builder Developer API Reference

> **There is no hosted Beaver Builder REST API and no native outbound webhook.** Beaver Builder is a WordPress plugin, so its "API" is a **PHP developer API** — a **custom-module system** (extend `FLBuilderModule`, register with `FLBuilder::register_module()`) plus a large surface of **`fl_builder_*` action/filter hooks**. Programmatic read/write of page content runs through **WordPress core** (the WP REST API, application passwords, WP-CLI, WP_Query) — the builder layout lives in `post_content` + the serialized `_fl_builder_data` post meta. The verbatim docs content below is the developer-API surface; the WordPress REST usage is enriched developer context.

## Hooks Reference

Beaver Builder publishes a searchable **Hooks Reference** at **https://hooks.wpbeaverbuilder.com/** covering hooks across three products:

- **Beaver Builder** (the core plugin)
- **BB Theme** (the Beaver Builder Theme)
- **Beaver Themer**

The reference distinguishes **Actions** (run code at specific points) from **Filters** (modify data before it's processed/displayed), and lets you filter to all hooks or a single product. (Hook data loads dynamically on that site.)

## Custom modules

Custom modules are PHP classes that **extend `FLBuilderModule`**. You configure the module in the constructor, then register it (with its settings UI) via `FLBuilder::register_module()`. Beaver Builder ships an example plugin you can clone, and the docs walk through steps 01–20 (create the plugin, add a module, define settings, styling, JavaScript, custom fields, aliases, etc.).

### Module class (constructor properties)

<!-- Verbatim from docs.wpbeaverbuilder.com/.../custom-modules/add-a-module-to-your-plugin/ -->
```php
class MyModuleClass extends FLBuilderModule {
  public function __construct() {
    parent::__construct(array(
      'name'            => __( 'My Module', 'fl-builder' ),
      'description'     => __( 'A totally awesome module!', 'fl-builder' ),
      'group'           => __( 'My Group', 'fl-builder' ),
      'category'        => __( 'My Category', 'fl-builder' ),
      'dir'             => MY_MODULES_DIR . 'my-module/',
      'url'             => MY_MODULES_URL . 'my-module/',
      'icon'            => 'button.svg',
      'editor_export'   => true,
      'enabled'         => true,
      'partial_refresh' => false,
      'include_wrapper' => false
    ));
  }
}
```

Key configuration properties:
- **name** — display name in the editor
- **description** — brief module explanation
- **group / category** — organizational grouping in the Content Panel
- **dir / url** — file paths and URLs for the module's assets
- **icon** — SVG icon filename
- **editor_export / enabled / partial_refresh / include_wrapper** — editor/runtime behavior flags

### Including the module in your plugin

<!-- Verbatim from docs -->
```php
function my_load_module_examples() {
  if ( class_exists( 'FLBuilder' ) ) {
    require_once 'my-module/my-module.php';
  }
}
```

**Important (from docs):** use **lowercase, dash-separated names with a prefix** (e.g. `john-button`) to avoid conflicts with core modules.

### Registering settings — `FLBuilder::register_module()`

The second argument defines the settings UI as **tabs → sections → fields**.

<!-- Verbatim from docs.wpbeaverbuilder.com/.../custom-modules/define-module-settings/ -->
**Basic tab structure:**
```php
FLBuilder::register_module( 'MyModuleClass', array(
  'my-tab-1'      => array(
      'title'         => __( 'Tab 1', 'fl-builder' ),
  ),
  'my-tab-2'      => array(
      'title'         => __( 'Tab 2', 'fl-builder' ),
  ),
) );
```

**With sections:**
```php
FLBuilder::register_module( 'MyModuleClass', array(
  'my-tab-1'      => array(
    'title'         => __( 'Tab 1', 'fl-builder' ),
    'sections'      => array(
      'my-section-1'  => array(
        'title'            => __( 'Section 1', 'fl-builder' ),
      ),
      'my-section-2'  => array(
        'title'            => __( 'Section 2', 'fl-builder' ),
      )
    )
  )
) );
```

**Complete example with fields:**
```php
FLBuilder::register_module( 'MyModuleClass', array(
  'my-tab-1'      => array(
    'title'         => __( 'Tab 1', 'fl-builder' ),
    'sections'      => array(
      'my-section-1'  => array(
        'title'         => __( 'Section 1', 'fl-builder' ),
        'fields'        => array(
          'my-field-1'     => array(
            'type'          => 'text',
            'label'         => __( 'Text Field 1', 'fl-builder' ),
          ),
          'my-field-2'     => array(
            'type'          => 'text',
            'label'         => __( 'Text Field 2', 'fl-builder' ),
          )
        )
      )
    )
  )
) );
```

Field `type` values include `text`, `textarea`, `photo`, `video`, `color`, `link`, `select`, `unit`, `dimension`, `icon`, and more (see the module-settings docs for the full field-type list). Each module instance also receives a **`filter_settings`** method you can override to transform settings before they're consumed.

### Custom fields

Register custom field types so Beaver Builder autoloads them with the **`fl_builder_custom_fields`** filter (see "14: Create custom fields" in the docs).

## Common filters & hooks (verbatim list)

<!-- Verbatim from docs.wpbeaverbuilder.com/.../common-beaver-builder-plugin-filter-examples/ -->
A selection of commonly used Beaver Builder filters/hooks and what each does:

1. **`fl_builder_admin_edit_sort_bb_enabled`** — removes the Beaver Builder filter option in WordPress post lists
2. **`fl_module_upload_regex`** — adds support for file types like SVG in image fields
3. **`fl_builder_content_elements_data`** — removes Box module aliases from the Content Panel
4. **`fl_builder_subscribe_form_services`** — adds mail services to the Subscribe module
5. **`fl_font_subset`** — adds Latin-Extended capabilities to Google fonts
6. **`fl_builder_crash_white_label_text`** — white labels the Ajax crash message
7. **`fl_photocaptionregex`** — allows special characters in lightbox captions
8. **`fl_remember_settings_tabs_enabled`** — controls whether settings windows remember the last tab
9. **`is_module_disable_enabled`** — shows module usage counts or prevents disabled modules from loading
10. **`fl_inline_editing_enabled`** — disables inline editing in the editor
11. **`fl_disable_notifications`** — disables Beaver Builder notifications in the UI
12. **`fl_builder_mailchimp_double_option`** — enables double opt-in for MailChimp
13. **`fl_ajax_*`** — filters front-end AJAX action results
14. **`fl_builder_admin_settings_post_types`** — modifies post types shown in settings
15. **`fl_builder_row_custom_class`** — modifies custom class names for rows
16. **`fl_builder_column_custom_class`** — modifies custom class names for columns
17. **`fl_builder_module_custom_class`** — modifies custom class names for modules
18. **`fl_builder_get_cache_dir`** — modifies the cache directory path
19. **`fl_builder_get_upload_dir`** — modifies the upload directory path
20. **`fl_builder_global_posts`** — specifies posts to load CSS/JS globally
21. **`fl_builder_layout_style_dependencies`** — adds dependencies to the CSS file
22. **`fl_builder_module_categories`** — adds custom module categories
23. **`fl_builder_post_types`** — modifies post types that can use Beaver Builder
24. **`fl_builder_register_module`** — overrides which modules are enabled
25. **`fl_builder_register_settings_form`** — customizes settings forms
26. **`fl_builder_render_css`** — modifies compiled and cached CSS
27. **`fl_builder_render_js`** — modifies compiled and cached JavaScript
28. **`fl_builder_render_settings_field`** — modifies field configuration arrays
29. **`fl_builder_render_shortcodes`** — prevents shortcode rendering in the editor
30. **`fl_builder_settings_form_defaults`** — changes defaults for settings forms
31. **`fl_builder_upgrade_url`** — modifies the upgrade URL in Beaver Builder Lite

Other documented examples include adding custom HTML attributes to rows/columns/modules via **`fl_builder_module_attributes`**, and registering autoloaded custom fields via **`fl_builder_custom_fields`**. Use the **Hooks Reference** (hooks.wpbeaverbuilder.com) to find the exact action/filter for a given extension point across Beaver Builder, BB Theme, and Beaver Themer.

## Beaver Themer: Field Connections

Beaver Themer extends the builder into a **theme builder** (custom headers, footers, archives, singular templates, 404, search, WooCommerce layouts) and adds **Field Connections** — dynamic data bound into any row/column/module setting.

- Any setting that accepts a field connection shows a **plus (+) icon** on the right of the field.
- Connections pull from **WordPress data** (site info), **page-by-page content** (Post Title, Post Featured Image, Post Date, author, etc.), **WordPress custom fields**, and plugins: **Advanced Custom Fields (ACF)**, **BigCommerce**, **Easy Digital Downloads**, **The Events Calendar**, and **WooCommerce**.
- This makes a Themer layout act as a **template** — the same layout renders the correct data wherever it appears (across all posts/products/etc.).
- There is a **field-connection shortcode syntax** for using dynamic data outside the visual picker (see the Themer "Field Connection Shortcode Syntax" docs).

## WordPress REST / data access (enriched developer context)

Beaver Builder stores a page's layout in the WordPress post:

- **`post_content`** — the rendered HTML (so content survives if the plugin is deactivated).
- **`_fl_builder_data`** (post meta) — the **serialized PHP** builder layout (nodes: rows/columns/modules with `type`, parent, and `settings`). Companion keys include `_fl_builder_enabled` and `_fl_builder_data_settings`. **This is internal serialized data — treat as best-effort, not a documented public schema; parse it server-side (WP-CLI/PHP), don't hand-build a blob to POST.**

**Auth (WordPress, not Beaver Builder):** create an **Application Password** (Users → Profile) and use HTTP Basic auth.

**Read rendered page content:**
```bash
curl -s -u "user:application_password" \
  "https://example.com/wp-json/wp/v2/pages/123?context=edit" | jq '.content.rendered'
```

**Read the raw serialized layout (server-side):**
```bash
wp post meta get 123 _fl_builder_data --format=json
```

**Error shape (WordPress core):**
```json
{ "code": "rest_post_invalid_id", "message": "Invalid post ID.", "data": { "status": 404 } }
```

**No documented rate limit** — there's no hosted API; you call your own WordPress install, so capacity is your host/server. There is **no Beaver Builder webhook** — for event-driven flows, hook WordPress actions (`save_post`, `publish_page`) and `fetch` your endpoint yourself, or use a form plugin's webhook for lead events.

## Gaps

- The full custom-module tutorial (frontend.php rendering, CSS/JS, `$this->settings`, field types beyond `text`, aliases, deprecations) spans docs steps 01–20 — capture specific steps verbatim from docs.wpbeaverbuilder.com when needed.
- The **complete** action/filter inventory is on hooks.wpbeaverbuilder.com (loads dynamically) — the list above is the documented "common examples" subset, not exhaustive.
- `_fl_builder_data` is **undocumented serialized internal data** — verify exact node/meta shapes against a live install before building tooling on top of it.
