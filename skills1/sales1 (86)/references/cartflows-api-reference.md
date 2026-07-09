<!-- Source: https://cartflows.com/docs-category/cartflows/developer-docs/ , https://cartflows.com/docs/wp-cli-commands/ , https://cartflows.com/docs/personalization-shortcodes-cartflows/ , https://cartflows.com/docs/offers-js-triggers-shortcodes/ , https://cartflows.com/docs/filters-to-customize-product-table/ , https://cartflows.com/docs/enable-webhooks-in-woocommerce-cart-abandonment-recovery-plugin/ , https://wordpress.org/plugins/cartflows/ — captured 2026-06 -->

# CartFlows Developer / Automation Reference

> **There is NO hosted CartFlows REST API and NO MCP server.** CartFlows is a self-hosted WordPress + WooCommerce plugin. Its programmatic surface is: **WP-CLI** (Pro), **shortcodes** (personalization + offer JS variables), **WordPress action/filter hooks** (PHP, in your theme/child-theme), **OttoKit / Zapier / Make** automation (1,000+ apps), and **webhooks via the companion Cart Abandonment Recovery plugin**. Funnel revenue (order bumps + one-click upsells) is recorded as **WooCommerce orders** — read it via the **WooCommerce REST API**, not a CartFlows endpoint.

CartFlows registers two custom post types you will see in the database and WooCommerce admin: **`cartflows_flow`** (a funnel) and **`cartflows_step`** (a step within a funnel — checkout / upsell / downsell / optin / thankyou / landing). <!-- Constructed from docs/plugin behavior — verify against live install -->

---

## 1. WP-CLI commands (CartFlows Pro)

> "CartFlows Pro adds support for managing certain actions via WP-CLI — a powerful tool for developers and advanced users who prefer working from the command line."

**Prerequisites:** both the free **CartFlows** plugin and **CartFlows Pro** must be installed and active.

### License activation

```bash
wp cartflows license activate your-license-key-here
```

Replace `your-license-key-here` with your actual CartFlows Pro license key to activate it from the command line. (At time of capture this is the only documented WP-CLI command; the team states WP-CLI support will expand.)

Generic WP-CLI you will combine with CartFlows (standard WordPress, not CartFlows-specific):

```bash
# List all funnels (cartflows_flow CPT)
wp post list --post_type=cartflows_flow --fields=ID,post_title,post_status

# List the steps inside a funnel
wp post list --post_type=cartflows_step --fields=ID,post_title,post_parent
```
<!-- Constructed from CPT names + standard WP-CLI — verify against live install -->

---

## 2. Personalization shortcodes

Display dynamic customer/order data on funnel-step content (works on **checkout, upsell, downsell, and thank-you** steps, inside page-builder content elements).

### Checkout field values

```
[cartflows_order_fields field="FIELD_NAME" default="TEXT"]
```

Shows a value the customer entered on the CartFlows checkout. `field` = which checkout field (e.g. `first_name`, `last_name`, `email`); `default` = fallback text when no data is available.

> **Important:** remove WooCommerce prefixes from field names — use `first_name` (not `billing_first_name`), `last_name` (not `shipping_last_name`).

Example — personalized thank-you headline:

```
Thank you, [cartflows_order_fields field="first_name" default="there"]!
```

### URL parameter values

```
[cartflows_url_fields field="PARAMETER_NAME" default="TEXT"]
```

Shows a value passed through a URL query parameter — lets external sources feed data into CartFlows steps (e.g. `?coupon=SAVE10` → `[cartflows_url_fields field="coupon" default=""]`).

---

## 3. Offer JS triggers & variables (one-click upsell / downsell)

CartFlows fires custom JavaScript on **Upsell** and **Downsell** steps via two trigger points configured under **CartFlows → Funnels → edit funnel → Upsell/Downsell step → Custom Script**:

1. **Offer Accepted** — runs when an upsell/downsell is accepted.
2. **Offer Rejected** — runs when the offer is declined.

### JavaScript variables available in the offer page

**CartFlows Free:**

```
{{order_id}}
{{txn_id}}
{{order_total}}
```

**CartFlows Pro (Upsell/Downsell only):**

```
{{offer_product_name}}
{{offer_product_qty}}
{{offer_product_price}}
```

### Variables available in the Accept/Reject offer scripts

```
{{order_id}}
{{flow_id}}
{{step_id}}
{{product_id}}
{{variation_id}}
{{quantity}}
{{offer_type}}
```

Example — fire a conversion pixel only when an upsell is accepted (paste into the **Offer Accepted** field):

```html
<script>
  // {{order_id}}, {{order_total}}, {{offer_product_name}} are substituted server-side
  gtag('event', 'purchase', {
    transaction_id: '{{order_id}}',
    value: '{{order_total}}',
    items: [{ item_name: '{{offer_product_name}}' }]
  });
</script>
```

> The docs publish the variable placeholders above but do NOT publish button CSS classes or exact event-listener names — capture them from the rendered page if you need to bind your own listeners.

---

## 4. WordPress action / filter hooks (PHP)

CartFlows is extended through standard WordPress hooks added to a **child theme's `functions.php`** (or a small custom plugin). The Cart Abandonment Recovery companion plugin documents these product-table filters verbatim:

### `woo_ca_email_template_table_style`

Customize the product table / image styling in recovery emails.

```php
add_filter( 'woo_ca_email_template_table_style', 'wcar_product_table_styles', 10 );

function wcar_product_table_styles( $style ){
    $style['product_image']['style'] = 'height: 42px; width: 42px;';
    $style['table']['style'] = 'color: #636363; border: 1px solid #e5e5e5; width:250px;';
    $style['table']['attribute'] = 'align="center" ';
    return $style;
}
```

### `woo_ca_recovery_enable_cart_total`

Include the final cart total (with tax + shipping) in the recovery-email product table.

```php
add_filter( 'woo_ca_recovery_enable_cart_total', '__return_true' );
```

> Add filters to your child theme's `functions.php`. CartFlows core also exposes a `wcf_*` / `cartflows_*` hook family (e.g. step/flow rendering and checkout-field filters) — confirm exact hook names in the developer docs for your version before relying on them. <!-- Hook family noted in dev docs; exact names version-specific — verify -->

---

## 5. Webhooks (via Cart Abandonment Recovery plugin)

CartFlows core has no webhook engine; abandoned-checkout events come from the bundled **WooCommerce Cart Abandonment Recovery** plugin.

> "A webhook ... is a listener. When a shopper abandons the checkout, the plugin triggers the webhook to perform an action."

**Trigger:** a shopper abandons the checkout.

**Setup:**
1. **WooCommerce → Cart Abandonment → Settings**
2. Find the **Webhook** section and enable the toggle
3. Paste a webhook URL from your automation tool (e.g. a Zapier **Catch Raw Hook** trigger URL)
4. Click **Trigger a Sample** to send a test payload you can inspect in the automation platform before going live

**Payload:** the docs do NOT publish a fixed field schema — use **Trigger a Sample** and read the live delivery in Zapier/Make to map fields (typically email, cart contents, cart total, checkout URL, and timestamps). <!-- Field list inferred from the plugin's data model — confirm with a live sample -->

Recovery actions you can wire off the webhook: send a coupon email, notify a CRM/marketing platform, or log the event in an external system.

---

## 6. WooCommerce REST API — read funnel revenue (the reliable read path)

Order bumps and one-click upsells are charged to the **WooCommerce order**, so the authoritative way to read CartFlows funnel revenue is the WooCommerce REST API.

**Auth:** WooCommerce → Settings → Advanced → REST API → *Add key* (Consumer key / Consumer secret, HTTP Basic over HTTPS).

```bash
curl https://example.com/wp-json/wc/v3/orders \
  -u ck_xxxxxxxxxxxx:cs_xxxxxxxxxxxx \
  -G --data-urlencode "per_page=20" --data-urlencode "status=completed"
```

```python
import requests

BASE = "https://example.com/wp-json/wc/v3"
AUTH = ("ck_xxxxxxxxxxxx", "cs_xxxxxxxxxxxx")

# Pagination is page/per_page; total pages in the X-WP-TotalPages header.
def iter_orders():
    page = 1
    while True:
        r = requests.get(f"{BASE}/orders", auth=AUTH,
                         params={"per_page": 100, "page": page, "status": "completed"})
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        yield from batch
        if page >= int(r.headers.get("X-WP-TotalPages", 1)):
            break
        page += 1
```

To attribute an order to a funnel, read CartFlows order meta on the WooCommerce order (e.g. the `_wcf_flow_id` / `_wcf_checkout_id` meta keys CartFlows writes). <!-- Meta-key names constructed from CartFlows conventions — verify on a live order -->

**Pagination:** `page` + `per_page` (max 100); `X-WP-Total` / `X-WP-TotalPages` response headers.
**Errors:** WooCommerce returns `{ "code": "...", "message": "...", "data": { "status": 4xx } }`.
**Webhooks:** WooCommerce itself can POST `order.created` / `order.updated` (WooCommerce → Settings → Advanced → Webhooks) — signed with an `X-WC-Webhook-Signature` (base64 HMAC-SHA256 of the payload using the webhook secret).

---

## 7. iPaaS / no-code automation

- **OttoKit** (formerly SureTriggers, by Brainstorm Force) — bundled in the CartFlows Suite; native CartFlows triggers/actions across 1,000+ apps.
- **Zapier / Make / Pabbly** — typically via the Cart Abandonment Recovery webhook (catch hook) and the WooCommerce app for order data.
- **Social pixels** — Facebook/Meta, Google, Pinterest, Snapchat, TikTok pixel tracking is built in (UI-configured).

---

## Gaps / not documented

- No first-party hosted REST API, no GraphQL, no MCP server.
- No published webhook payload schema or HMAC signature for the Cart Abandonment Recovery webhook (use *Trigger a Sample*).
- Offer-page button classes / DOM event names are not published (only the `{{...}}` substitution variables).
- Exact `cartflows_*` / `wcf_*` core hook names are version-specific — verify in the developer docs for your installed version.
- CartFlows order meta keys (`_wcf_flow_id`, etc.) are constructed from convention here — confirm on a live WooCommerce order.
