# Breakdance Platform Reference

## Overview

Breakdance is a **standalone visual website/page builder for WordPress** by **Soflyy** — the team behind **Oxygen** and **WP All Import**. WordPress.org slug: `breakdance`. Unlike Spectra/Kadence/GenerateBlocks (which *extend* the Gutenberg block editor), Breakdance is a **full builder with its own front-end editor** that can replace the theme entirely (**"themeless by default"**) — closer in nature to **Elementor, Beaver Builder, and Oxygen**. It markets clean markup, **conditional asset loading** (a blank page ~45 KB vs Elementor's ~576 KB), and **jQuery-independence**.

Breakdance is positioned as the **modern successor to Oxygen**: **Oxygen 6 is rebuilt on the Breakdance engine**, Oxygen lifetime licenses now include Breakdance, and the two share core builder functionality. It surfaces in 2026 comparisons as a Bricks / Elementor / Beaver Builder alternative.

## Capabilities & automation surface

| Capability | What it does | Surface |
|---|---|---|
| **Elements** | ~80 (Free) / ~145 (Pro) building blocks — sections, headings, buttons, sliders, tabs, accordions, posts list, etc. | UI-built; custom elements via **Element Studio** |
| **Templates & Design Library** | Headers/footers/archives/singular templates + a library of sections and full-site templates | UI-built |
| **WooCommerce Builder** | Customizable product pages, shop/archive filters, cart & checkout templates | **Pro**, UI-built |
| **Form Builder** | Multi-step forms, conditional fields, honeypot + reCAPTCHA v3; **Actions After Submit** (Store Submission, Email, **Webhook**, native integrations) | **Pro**, UI-built; extend via **Form Actions API** |
| **Popup Builder** | Lead-capture / conversion popups with triggers | **Pro**, UI-built |
| **Dynamic Data** | Post loops, repeaters, conditional display, search/filter; binds post/meta/ACF data into elements | UI-built; extend via **Dynamic Data Field API** |
| **Element Studio** | Built-in IDE to create custom elements (incl. PHP/HTML/CSS code + reusable dependencies) | **Developer** |
| **Element Display Conditions** | Show/hide elements on the front end by condition | UI-built; extend via **Conditions API** |
| **Breakdance AI** | In-builder content generation (OpenAI by default) | UI; **model/provider swappable via filters** |
| **Client Mode** | Restricted editing access for clients | **Pro**, UI |
| **Form Webhook action** | POST a submission to any URL (Zapier/Make "Catch Hook") with field mapping | UI-built (the main outbound integration) |
| **`breakdance_*` hooks/filters + JS APIs** | Form hooks, save-action filters, AI endpoint filters, posts-list hooks, Menu/Animations JS APIs | **Developer** — see `breakdance-api-reference.md` |

**There is no hosted Breakdance REST API and no platform-level outbound webhook.** Breakdance is a WordPress plugin; its programmatic surface is **WordPress core** (the WP REST API, application passwords, WP-CLI) **plus its own PHP developer APIs** (Form Actions, Dynamic Data Field, Conditions) and the Form Builder's **Webhook action**. Page layouts are stored in Breakdance's own post meta (not portable Gutenberg block markup).

## Pricing, limits & plan gates

*Pricing is best-effort from 2026 research, annual, and promo-dependent — verify on breakdance.com/get before relying on it. **No lifetime plan**; a **price-lock guarantee** holds your annual rate at renewal; 60-day money-back guarantee.*

| Plan | Approx. price | Sites | Notable inclusions |
|---|---|---|---|
| **Breakdance Free** (WordPress.org) | $0 | unlimited | Core builder + ~80 elements, basic Design Library, basic integrations |
| **Breakdance Pro** | ~$199.99/yr (promo) | unlimited sites + unlimited domain activations | All ~145 elements, full Design Library, **WooCommerce Builder**, **Form Builder + Popup Builder**, Global Blocks, Client Mode |
| **Pro + AI Bundle** | ~$249.99 (limited-time) | unlimited | Pro + Breakdance AI credits/bundle |

- **Plan-gate watch-outs:** the WooCommerce Builder, Form Builder, Popup Builder, Global Blocks, and Client Mode are **Pro**. The Free tier is a genuine builder (good for one-off pages) but lacks the conversion/commerce modules.
- **No native A/B testing, heatmaps, analytics, cart engine, or email** on any tier — bolt on VWO/Clarity for testing and an ESP for email.
- **Oxygen users:** Oxygen 6 runs on the Breakdance engine and is **included in the Oxygen lifetime license**; Soflyy also offered Oxygen users a (historically 1-year, since improved) Breakdance license. Confirm current terms.
- **Affiliate / partner program:** Breakdance runs one — log under `_internal/affiliates.md` if you pursue it.

## Integrations

- **Theme:** any theme, or **themeless** (Breakdance replaces the theme and controls headers/footers/templates).
- **WooCommerce:** deep via the **WooCommerce Builder** (Pro) — build product, shop, cart, and checkout templates; WooCommerce remains the cart/checkout engine.
- **Forms / leads (data out):** the **Form Builder** sends to native ESP/CRM integrations (e.g. Mailchimp, ActiveCampaign), stores entries (Store Submission), emails notifications (Email), or **POSTs to any URL via the Webhook action** (Zapier/Make). For arbitrary destinations or to run server code, write a **custom Form Action** (PHP).
- **AI providers:** Breakdance AI defaults to OpenAI but is **filterable to OpenRouter / Claude / any OpenAI-compatible endpoint** (`breakdance_ai_api_endpoint` + `breakdance_ai_model`).
- **Dynamic data sources:** WordPress posts/meta, **ACF** (incl. ACF Flexible Content), and custom sources via the **Dynamic Data Field API**.
- **iPaaS:** no first-party Zapier/Make app for the builder; automation rides on the **form Webhook action** and the underlying WordPress/WooCommerce connectors.
- **MCP server:** none (as of research). Programmatic control is via the WordPress REST API + the PHP developer APIs.

## Data model

Breakdance has **no remote object model/API**. A page's layout is **Breakdance's own serialized data stored in WordPress post meta** (rendered to clean HTML on the front end), **not** portable Gutenberg block markup. There is no documented public schema for the meta — treat it as opaque and edit pages through the Breakdance editor, not by hand-writing meta.

What you *can* address programmatically:

- **Posts/pages** via the **WordPress core REST API** (`/wp-json/wp/v2/pages/{id}` etc.) — auth with an Application Password. You can create/trash/publish the post and read the rendered `content`, but the Breakdance layout itself lives in meta and is not meant to be authored over REST.
- **Form submissions** stored by the Store Submission action are visible under **Breakdance → Form Submissions** in WP-Admin (each submission shows per-action status for troubleshooting).

```bash
# Read a Breakdance-built page's rendered HTML via the WordPress REST API
curl -s https://example.com/wp-json/wp/v2/pages/123 \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" | jq '.content.rendered'
```

> The Breakdance layout is in post meta, not the `content` field — `content.rendered` returns the front-end HTML, which is read-only-useful (scraping/auditing), not a way to author the layout. Build in the editor; automate the *post* and *form delivery*, not the meta.

## Quick-start recipes

### Recipe 1 — Custom Form Action: forward every submission to your CRM (PHP)

**Trigger:** run your own server-side code on each form submission (push to a CRM, log to a file, call an API).
**Steps:** create a class extending `Breakdance\Forms\Actions\Action`, implement `name()`/`slug()`/`run()`, and register it on `init` with guards.

```php
// my-action.php
class CrmForwardAction extends \Breakdance\Forms\Actions\Action {
    public function name()  { return 'Forward to CRM'; }
    public function slug()  { return 'myplugin_crm_forward'; } // unique, prefixed
    public function run($form, $settings, $extra) {
        // $extra['fields'] is an [id => value] array of the submission
        $resp = wp_remote_post('https://crm.example.com/api/leads', [
            'headers' => ['Authorization' => 'Bearer ' . MY_CRM_TOKEN],
            'body'    => wp_json_encode($extra['fields']),
        ]);
        if (is_wp_error($resp)) {
            return ['type' => 'error', 'message' => $resp->get_error_message()];
        }
        return ['type' => 'success', 'message' => 'Lead sent to CRM'];
    }
}

// register-actions.php
add_action('init', function () {
    if (!function_exists('\Breakdance\Forms\Actions\registerAction')
        || !class_exists('\Breakdance\Forms\Actions\Action')) {
        return; // Breakdance not active — fail gracefully
    }
    require_once __DIR__ . '/my-action.php';
    \Breakdance\Forms\Actions\registerAction(new CrmForwardAction());
});
```

**Gotcha:** `$extra` also carries `formId`, `postId`, `ip`, `referer`, `userAgent`, `userId`, and uploaded `files`. Always register on `init` and guard with `function_exists()`/`class_exists()` to avoid file-loading race conditions.

### Recipe 2 — No-code: POST a form to Zapier/Make via the Webhook action

**Trigger:** send submissions to a platform with no native Breakdance connector.
**Steps:** in Zapier create a **Catch Hook** (or Make a custom webhook) → copy the URL → in the Breakdance Form Builder add the **Webhook** action → paste the URL → **map each form field** to the webhook's expected keys → submit a test entry and confirm it arrives.

```text
Form Builder → Actions After Submit → add "Webhook"
  Webhook URL: https://hooks.zapier.com/hooks/catch/123456/abcdef/
  Map fields:  name → name, email → email, message → message
```

**Gotcha:** to avoid duplicate/spam **emails**, drag the spam-check action **above** Store/Email, or remove the Email action and handle notifications inside Zapier/Make off this webhook. The webhook has no HMAC signature — validate/rate-limit on your side and make the consumer idempotent.

### Recipe 3 — Route Breakdance AI to Claude via OpenRouter (filters)

**Trigger:** use a non-OpenAI model for Breakdance AI.
**Steps:** add the endpoint + model filters, then paste your provider key into Breakdance → Settings → AI Assistant's "OpenAI API Key" field.

```php
add_filter('breakdance_ai_api_endpoint', fn($url) => 'https://openrouter.ai/api');

add_filter('breakdance_ai_model', function ($model_version, $model) {
    return 'anthropic/claude-3.5-sonnet';
}, 10, 2);

// Disable Breakdance AI entirely:
// add_filter('breakdance_ai_enabled', '__return_false');
```

**Gotcha:** the WP-Admin AI Assistant settings UI **won't change** to reflect these filters — verify via the browser console and the provider's usage charts. The key always goes in the "OpenAI API Key" field, even for OpenRouter/Claude. Model availability/credits depend on the provider.

## Integration patterns

- **Programmatic page creation:** there is no "create a Breakdance layout" API. Create the WP post via the WordPress REST API or `wp_insert_post`, but **build the layout in the Breakdance editor** — the layout is opaque post meta, not authorable markup. Reuse via Templates, Global Blocks, and the Design Library.
- **Lead/data out:** the **form Webhook action** (no-code) for Zapier/Make, or a **custom Form Action** (PHP) for server-side delivery to a CRM/endpoint. There's no platform outbound webhook beyond the form action.
- **External/AI data:** Breakdance AI is provider-swappable via filters; for binding arbitrary external APIs into a page, use a custom element (Element Studio) or a custom Dynamic Data field.
- **Spam & notifications pipeline:** order Actions After Submit so the **spam-check runs first**; Breakdance can't intercept the Email action from a plugin, so move email downstream (Make/Zapier) when a filter must gate it. Enable honeypot + reCAPTCHA v3.
- **Performance posture:** lean by default (conditional assets, no jQuery, ~45 KB blank page), but watch layout nesting, Dynamic Data loop size, image weight, and caching — most slow Breakdance pages are misuse, not the builder. Audit the theme/host too.
- **Oxygen migration:** Oxygen 6 shares the Breakdance engine; for **Oxygen Classic** content use a third-party JSON converter (e.g. TransferForge), test on staging, and expect manual cleanup — there's no native one-click importer.
