<!-- Source: https://github.com/soflyy/breakdance-developer-docs (form-actions, dynamic-data, conditions, hooks, menu, animations, reusable-dependencies) ; https://breakdance.com/documentation/developers/ ; https://breakdance.com/documentation/developers/apis/ ; https://breakdance.com/documentation/forms/actions-and-integrations/webhooks-and-api-integrations/ -->

# Breakdance Developer Reference — Form Actions, Dynamic Data, Conditions, Hooks & WordPress surface

Breakdance is a WordPress plugin. It has **no hosted REST API** and **no platform-level outbound webhook**. Its programmatic surface is:

1. **WordPress core** — the WP REST API (`/wp-json/wp/v2/...`), application-password auth, and WP-CLI. A Breakdance page's *layout* is stored in Breakdance's own **post meta** (opaque), not in portable Gutenberg block markup; `content.rendered` returns the front-end HTML only.
2. **The Breakdance PHP developer APIs** — **Form Actions API**, **Dynamic Data Field API**, and **Conditions API** (register custom extensions; intended for plugin/extension developers).
3. **The `breakdance_*` hooks & filters** — form hooks, save-action filters, AI endpoint filters, posts-list hooks, reusable dependencies, and more.
4. **Form integrations** — native ESP integrations + a no-code **Webhook action** that POSTs submissions to any URL (Zapier/Make).
5. **JavaScript APIs** — the **Menu** and **Animations** client-side APIs.

> Reproduced from Breakdance's public developer documentation. Confirm exact class/function names, hook names, and argument shapes against your installed Breakdance version before relying on them — APIs evolve per release. The official developer docs index is at breakdance.com/documentation/developers/ and the source repo is github.com/soflyy/breakdance-developer-docs.

## Documented public APIs (index)

From breakdance.com/documentation/developers/apis/:

1. **Actions API** — custom actions within Breakdance
2. **AI Endpoints API** — endpoints/filters for AI functionality integration
3. **Animations API** — animation features and effects (JS)
4. **Breakdance Form Submissions Capability** — permissions for form-submission access
5. **Dependencies API** — element/feature dependency management (reusable dependencies)
6. **Dynamic Data API** — dynamic content population and data binding
7. **Form Actions API** — custom actions triggered by form submissions
8. **Global Settings API** — site-wide configuration settings
9. **Menu API** — menu creation/customization (JS)
10. **Popups API** — popup behavior and triggers
11. **Element Display Conditions API** — conditional visibility of elements (Conditions API)
12. **Adding An API Key Field To Breakdance's Settings**
13. **Template Override Filter** — customize template rendering

The public API source documentation in the GitHub repo covers: **Menu JavaScript API**, **Animations JavaScript API**, **Conditions API**, **Dynamic Data API**, **Form Actions API**, **Reusable Dependencies**, and **Hooks**.

---

## Authentication quick-start (WordPress core, not Breakdance-specific)

```bash
# Read a Breakdance-built page's rendered HTML with an application password
curl -s https://example.com/wp-json/wp/v2/pages/123 \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" | jq '.content.rendered'
```

Generate an application password under **Users → Profile → Application Passwords**. The token inherits that user's capabilities. Note: the Breakdance *layout* is in post meta, not the `content` field — REST is useful for managing the post (create/publish/trash) and scraping rendered HTML, not for authoring the Breakdance layout.

---

## Form Actions API

Creating a Breakdance Form Action involves two steps

1. Create an Action class to represent your field
2. Register the action class with Breakdance

### Creating an action class

To get started create a new PHP class. Your class will need to extend the Breakdance base Action class `Breakdance\Forms\Actions\Action`

#### Required Methods

There are three mandatory methods that must be implemented in your action class

**name**

The name method takes no arguments and returns a string that will be used to identify your action in the Form Builder Actions dropdown menu

```php
/**
 * @return string
 */
public function name() {
	return 'My Action';
}
```

**slug**

The slug method takes no arguments and returns a string to identify the form action. This should be unique across all form actions, so it is recommended to prefix the slug appropriately.

```php
/**
 * @return string
*/
public function slug()
{
    return 'my_plugin_form_action';
}
```

**run**

The run method accepts three arguments,  `$form, $settings, $extra` and is called when the form has been submitted

```php
/**
* Log the form submission to a file
*
* @param array $form
* @param array $settings
* @param array $extra
* @return array success or error message
*/
public function run($form, $settings, $extra)
{
    try {
        $this->writeToFile($extra['formId'], $extra['fields']);
    } catch(Exception $e) {
        return ['type' => 'error', 'message' => $e->getMessage()];
    }

    return ['type' => 'success', 'message' => 'Submission logged to file'];
}
```

#### Run Arguments

**$form**

The form argument contains all the form fields, their builder settings and the selected values

- type: the field type
- name: the field name
- options: an array of available options for checkbox, radio or select inputs
- value: the submitted value of the field
- originalValue: the default/original value of the field

**$settings**

The settings argument contains an array of the configured form settings from the Breakdance builder

**$extra**

The extra argument contains additional data

- files: An array of uploaded files
- fields: the submitted form fields in an `$id ⇒ $value` style array
- formId: The ID of the form
- postId: The ID of the post the form was submitted from
- ip: the submitters IP address
- referer: The form submitters referrer URL
- userAgent: The form submitters user agent string
- userId: The form submitters user ID (if applicable)

#### Responses

The response should be an array that contains a `type` and `message` key.

- type: either `error` or `success`
- message: a string message that will be displayed to admins with the submission

**Success**

```php
public function run($form, $settings, $extra)
{
    ...
    return ['type' => 'success', 'message' => 'Submission logged to file'];
}
```

**Error**

```php
public function run($form, $settings, $extra)
{
    ...
    return ['type' => 'error', 'message' => 'Could not write to file'];
}
```

### Register The Action

Register the action by calling the registerAction helper and passing an instance of your action class

**Note:** To prevent file loading race conditions, it is recommended to call the register helper from inside a WordPress action, e.g init.

```php
// register-actions.php included by your plugin

add_action('init', function() {
    // fail if Breakdance is not installed and available
    if (!function_exists('\Breakdance\Forms\Actions\registerAction') || !class_exists('\Breakdance\Forms\Actions\Action')) {
        return;
    }

    require_once('my-action.php');

    \Breakdance\Forms\Actions\registerAction(new MyAction());

});
```

---

## Form Builder Hooks

```php
## breakdance_form_start
add_action('breakdance_form_start', function ($settings) {
    echo "<div class=\"breakdance-form-group\">
        <h4 style='margin: 0;'>{$settings['form']['form_name']}</h4>
    </div>";
});

## breakdance_form_before_field
add_action('breakdance_form_before_field', function ($field, $settings) {
    echo 'The field below is ' . ($field['advanced']['required'] ? '' : 'not') . ' required.';
}, 10, 2);

## breakdance_form_after_field
add_action('breakdance_form_after_field', function ($field, $settings) {
    echo "<span>Type: <strong>{$field['type']}</strong> / ID: {$field['advanced']['id']}</span>";
}, 10, 2);

## breakdance_form_before_footer
add_action('breakdance_form_before_footer', function ($settings) {
    echo '
    <div class="breakdance-form-group">
        <button>AutoFill with LinkedIn</button>
    </div>
    ';
});

## breakdance_form_end
add_action('breakdance_form_end', function ($settings) {
    echo '<div class="breakdance-form-group">By submitting this form you agree to the terms of service.</div>';
});
```

### Webhooks and API Integrations (no-code form delivery)

> A webhook is a unique URL that allows you to send data to interact with another web application.

Setup (the docs use Zapier as the example):

1. **Obtain a webhook URL** from your external platform (e.g. Zapier "Catch Hook").
2. **Add the Webhook action** in the Form Builder's **Actions** section of the Properties Panel.
3. **Map form fields** to the webhook's expected parameters in the edit interface.
4. **Test** by submitting a test entry and confirming the data appears in the external platform.

This enables integrations with platforms that lack a native Breakdance connector. (The docs focus on the workflow; the action POSTs the mapped field data to the URL.)

---

## Dynamic Data Field API

### Overview

Creating a Breakdance Dynamic Field involves two steps

1. Create a field class to represent your field
2. Register the field class with Breakdance

An example WordPress plugin that adds Dynamic Data fields can be found at https://github.com/soflyy/breakdance-sample-dynamic-data

### Base Field Classes

Your class extends one of the Breakdance base classes so Breakdance knows how to work with your data and which elements it's compatible with.

#### StringField — `\Breakdance\DynamicData\StringField`

For any generic string data. Handler return type: `\Breakdance\DynamicData\StringData` (a `$value` string).

- `StringData::fromString(string $string);` → StringData with `$value` = `$string`
- `StringData::emptyString();` → StringData with an empty string

```php
use Breakdance\DynamicData\StringField;
use Breakdance\DynamicData\StringData;

class MyDynamicField extends StringField
{
    public function label()    { return 'Dynamic String'; }
    public function category() { return 'My Plugin'; }
    public function slug()     { return 'my_plugin_string'; }

    public function handler($attributes): StringData
    {
        return StringData::fromString('some string value');
    }
}
```

#### ImageField — `\Breakdance\DynamicData\ImageField`

For fields that return an image. Handler return type: `\Breakdance\DynamicData\ImageData`. Required properties: `$url` and `$sizes` (`$sizes` is keyed by size slug; each value is an array with `file`, `width`, `height`, `mime-type`). Recommended helper: `ImageData::fromAttachmentId($attachmentId)`.

```php
use Breakdance\DynamicData\ImageField;
use Breakdance\DynamicData\ImageData;

class MyDynamicField extends ImageField
{
    public function label()    { return 'Dynamic Image'; }
    public function category() { return 'My Plugin'; }
    public function slug()     { return 'my_plugin_image'; }

    public function handler($attributes): ImageData {
        // build from attachment data, or use the helper:
        $imageData = ImageData::fromAttachmentId($attachmentId);
        return $imageData;
    }
}
```

#### GalleryField — `\Breakdance\DynamicData\GalleryField`

For multiple images (Slideshow/Gallery elements). Handler return type: `\Breakdance\DynamicData\GalleryData` with `$images` = array of `ImageData`.

#### OembedField — `\Breakdance\DynamicData\OembedField`

For video, by oEmbed URL (YouTube/Vimeo) or a direct media-library video. Handler return type: `\Breakdance\DynamicData\OembedData`. Required: `$embedUrl`, `$type` (`video` or `oembed`), and `$provider` for oEmbed sources. Helpers: `OembedData::fromOembedUrl($url)` (XHR retrieval), `OembedData::emptyOembed()`.

### Required Methods (all field classes)

- `label()` → string shown in the Dynamic Data Field selection window
- `category()` → string used to group the fields
- `slug()` → unique (prefixed) identifier for the field handler
- `handler($attributes)` → returns a data object matching the parent field type

### Optional Methods

- `subcategory()` → further group fields in the dialog
- `returnTypes()` → array of return types that determine which elements can use the field

### Return Types

The return types determine which elements have access to a dynamic field (e.g. an Image element only accepts `image_url` data). A field may have multiple.

- `string` — Generic string (default for StringData)
- `image_url` — Array of image properties (default for ImageData)
- `gallery` — Array of ImageData (default for GalleryData)
- `video` — Array of Video/Oembed data (default for Oembed fields)
- `url` — String that represents a URL (compatible with StringData)
- `query` — String that represents a URL query (compatible with StringData)
- `google_map` — Address or lat/long string (StringData; works with the Google Map element)

### Registering The Field Class With Breakdance

```php
add_action('init', function() {
    if (!function_exists('\Breakdance\DynamicData\registerField') || !class_exists('\Breakdance\DynamicData\Field')) {
        return;
    }

    \Breakdance\DynamicData\registerField(new MyField());
});
```

You can also register **multiple instances of the same class** (same handler/data type) by passing field-config data into the constructor and looping `registerField()` over an array — useful for many fields that share a handler.

---

## Conditions API (Element Display Conditions)

Conditions are created using the `breakdance_register_template_types_and_conditions` action hook and the `Breakdance\ConditionsAPI\register` function. Breakdance users can show or hide elements on the front end based on conditions.

```php
add_action(
    'breakdance_register_template_types_and_conditions',
    function() {

        \Breakdance\ConditionsAPI\register(
            [
                'supports' => ['element_display'],
                'slug' => 'unique-prefix-my-condition', // MUST BE UNIQUE
                'label' => 'My Condition',
                'category' => 'My Category',
                'operands' => ['equals', 'not equals'],

                // optional dropdown of values; omit for a text input instead
                'values' => function() { return [
                    [
                        'label' => 'Item Group Title',
                        'items' => [
                            ['text' => 'Item 1', 'value' => 'item-1'],
                            ['text' => 'Item 2', 'value' => 'item-2'],
                        ]
                    ],
                ]; },

                // optionally make the dropdown a multiselect
                'allowMultiselect' => true,

                // return true to show the element, false to hide it
                'callback' => function(string $operand, $value) {

                    $myVal = 'item-1'; // usually derived from context, e.g. global $post; $myVal = $post->ID;

                    // when allowMultiselect is true, $value is an array of strings
                    if ($operand === 'equals') {
                        return in_array($myVal, $value);
                    }
                    if ($operand === 'not equals') {
                        return !in_array($myVal, $value);
                    }
                    return false;
                },
            ]
        );
    }
);
```

> **Query Builder Conditions** and **Templating Conditions**: "A public API for query builder conditions is planned for the future." / "A public API for templating conditions is planned for the future."

---

## AI Endpoints API (filters)

Breakdance AI has filters to change the model or provider being used. **The Breakdance → Settings → AI Assistant screen in WP-Admin will NOT change** when you use these filters — verify via the developer console and your provider's usage charts. Add your provider's API key to the **"OpenAI API Key"** input at Breakdance → Settings → AI Assistant; Breakdance uses that key for whatever endpoint is set.

Filters:

- `breakdance_ai_model` — define the model Breakdance AI will use.
- `breakdance_ai_api_endpoint` — change the AI provider endpoint.
- `breakdance_ai_enabled` — show/hide Breakdance AI within Breakdance.

```php
// Example 1: change the OpenAI model to gpt-4
function override_breakdance_ai_model($model_version, $model) {
    return 'gpt-4';
}
add_filter('breakdance_ai_model', 'override_breakdance_ai_model', 10, 2);

// Example 2: use OpenRouter with Anthropic Claude 3.5 Sonnet
function override_breakdance_ai_endpoint($url) {
    $url = 'https://openrouter.ai/api';
    return $url;
}
add_filter('breakdance_ai_api_endpoint', 'override_breakdance_ai_endpoint');

function override_breakdance_ai_model_or($model_version, $model) {
    $model_version = 'anthropic/claude-3.5-sonnet'; // requires OpenRouter credits
    return $model_version;
}
add_filter('breakdance_ai_model', 'override_breakdance_ai_model_or', 10, 2);
// then paste the OpenRouter key into the "OpenAI API Key" field.

// Example 3: disable Breakdance AI entirely
add_filter('breakdance_ai_enabled', '__return_false');
```

---

## Other Hooks

```php
// Filter the content of singular Breakdance documents
add_filter("breakdance_singular_content", function ($content) {
    if ($something) { return $content; }
    else { return "not authorized"; }
});

// Fires after the Save button is clicked and the post is saved
add_action("breakdance_after_save_document", function ($postId) {
    // the save button in Breakdance was clicked and the post was saved
});

// Filter registered fonts (e.g. disable all Google Fonts)
add_filter("breakdance_register_font", function ($font) {
    $isGoogleFont = !!$font['dependencies']['googleFonts'];
    if ($isGoogleFont) { return false; }
    return $font;
});

// Modify/remove appended dependencies
add_filter("breakdance_append_dependencies", function ($dependenciesToAppend) {
    return $dependenciesToAppend;
});

// Add a class to an element's HTML class attribute
add_filter("breakdance_element_classnames_for_html_class_attribute", function ($classNames) {
    $classNames[] = 'another-class';
    return $classNames;
});

// Modify the query for the query builder input (example from Breakdance core)
add_filter('breakdance_query_builder_input_query', '\Breakdance\Integrations\FacetWp\enableFacetWpForCustomQueries');
function enableFacetWpForCustomQueries($query) {
  if (is_string($query)) { return $query . "&facetwp=true"; }
  else { $query['facetwp'] = true; return $query; }
}
```

### Editor Save Actions (experimental filters)

These filters only run when clicking "Save" while editing a page/template inside the Breakdance editor. They return `true` by default. **Experimental — may change or be removed.**

- `breakdance_save_global_settings` — enable/disable saving Global Settings on Save
- `breakdance_save_presets` — enable/disable saving Design Presets on Save
- `breakdance_save_selectors` — enable/disable saving Custom Selectors and Classes on Save
- `breakdance_save_ai_settings` — enable/disable saving the Breakdance AI Settings on Save

```php
function disable_saving_for_other_users($allow_save) {
    $user_id = get_current_user_id();
    if ($user_id != 69420) { return false; }
    return $allow_save;
}
add_filter('breakdance_save_global_settings', 'disable_saving_for_other_users');
add_filter('breakdance_save_presets', 'disable_saving_for_other_users');
add_filter('breakdance_save_selectors', 'disable_saving_for_other_users');
add_filter('breakdance_save_ai_settings', 'disable_saving_for_other_users');
```

### Posts List element hooks

Hooks to inject HTML into the Breakdance Posts List element:

```
breakdance_posts_list_before_loop
breakdance_posts_list_before_post
breakdance_posts_list_after_image
breakdance_posts_list_inside_wrap_start
breakdance_posts_list_after_title
breakdance_posts_list_after_meta
breakdance_posts_list_after_tax
breakdance_posts_list_after_content
breakdance_posts_list_inside_wrap_end
breakdance_posts_list_after_post
breakdance_posts_list_after_loop
breakdance_posts_list_after_pagination
```

---

## Reusable Dependencies

Register reusable dependencies usable in any element in Element Studio.

```php
add_action('breakdance_reusable_dependencies_urls', function ($urls) {
   $urls['bootstrap'] = 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.2.3/js/bootstrap.min.js';
   return $urls;
});
```

Use it in Element Studio → Dependencies tab → add a dependency → in the Script URL field write `%%BREAKDANCE_REUSABLE_BOOTSTRAP%%` (replace `BOOTSTRAP` with your dependency name).

Predefined reusable dependencies: `%%BREAKDANCE_REUSABLE_GSAP%%`, `%%BREAKDANCE_REUSABLE_SCROLL_TRIGGER%%`.

Change the globally-loaded GSAP version:

```php
add_action('breakdance_reusable_dependencies_urls', function ($urls) {
   $urls['gsap'] = 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.8.0/gsap.min.js';
   return $urls;
});
```

Notes: you don't need to register a dependency if you won't reuse it (use the URL directly in the element). Variables defined in camelCase must be used as snake_case in Element Studio.

---

## Animations JavaScript API

Replay/reset Breakdance entrance animations via dispatched events.

```js
// Replay animations on a specific element
const panel = document.querySelector('.bde-accordion__panel');
panel.dispatchEvent(new Event("breakdance_play_animations", { bubbles: true }));

// Replay animations on the entire website
document.dispatchEvent(new Event("breakdance_play_animations", { bubbles: true }));

// Reset entrance animations to their initial hidden state
panel.dispatchEvent(new Event("breakdance_reset_animations", { bubbles: true }));
```

**New in 2.0**: animations auto-retrigger in Slider, Advanced Accordion, Tabs, and Popup elements (e.g. when a new slide appears or an accordion panel opens).

---

## Menu JavaScript API

Access the Breakdance Menu instance on its HTMLElement after the page loads:

```js
const menu = document.querySelector('.breakdance-menu').bdMenu;

const dropdown = document.querySelector('.bde-menu-dropdown-72-105 .breakdance-dropdown');
menu.openDropdown(dropdown);
menu.closeDropdown(dropdown);
menu.closeAll();
menu.toggleMobileMenu();
```

API: `openDropdown(node)`, `closeDropdown(node)`, `closeAll()`, `getOpenDropdown() => DropdownElement | null`, `refreshDropdowns()`, `toggleMobileMenu() => Promise<void>`, `isDesktop() => boolean`, `isMobile() => boolean`, `isVertical() => boolean`.

---

## Gaps / not documented

- **No public hosted REST API** for Breakdance objects — use the WordPress core REST API against posts/pages (the Breakdance *layout* lives in opaque post meta, not the `content` field).
- **No platform-level outbound webhook** — the only built-in outbound integration is the Form Builder's **Webhook action** (per-form, POSTs mapped fields; no documented HMAC signature — validate/de-dupe on your side).
- **No first-party Zapier/Make app** for the builder itself; iPaaS rides on the form webhook + WordPress/WooCommerce connectors.
- **Public APIs for Query Builder Conditions and Templating Conditions are "planned for the future"** (not yet available).
- Exact `breakdance_*` hook names, class/method signatures, and the Global Settings / Popups / Actions API details evolve per release — confirm against breakdance.com/documentation/developers/ and the installed version. Source repo: github.com/soflyy/breakdance-developer-docs; sample Dynamic Data plugin: github.com/soflyy/breakdance-sample-dynamic-data.
