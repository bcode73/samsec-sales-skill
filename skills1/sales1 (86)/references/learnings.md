# CartFlows Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-28**: Research baseline — platform docs, developer surface (WP-CLI, personalization/offer-JS shortcodes, PHP filter hooks, Cart Abandonment Recovery webhook), pricing, and WooCommerce-read pattern captured from live sources (cartflows.com docs via text proxy, wordpress.org plugin page, comparison articles) on this date. Re-verify specifics against current docs before relying on them.

<!-- Notable facts worth remembering -->
- **No hosted REST API and no MCP.** CartFlows is a self-hosted WP+WooCommerce plugin; the programmatic surface is WP-CLI (Pro), shortcodes, WordPress hooks, OttoKit/Zapier, and Cart Abandonment Recovery webhooks. Funnel revenue is read from **WooCommerce orders**, not CartFlows.
- **WP-CLI is minimal** — at capture, the only documented command was `wp cartflows license activate <key>` (Pro; requires both free + Pro plugins). The team says WP-CLI will expand.
- **Offer JS variables are plan-split:** Free exposes `{{order_id}}`, `{{txn_id}}`, `{{order_total}}`; Pro adds `{{offer_product_name/qty/price}}`. Accept/Reject scripts also see `{{flow_id}}`, `{{step_id}}`, `{{product_id}}`, `{{variation_id}}`, `{{quantity}}`, `{{offer_type}}`.
- **Personalization shortcodes strip WooCommerce prefixes:** use `field="first_name"`, NOT `billing_first_name`.
- **Top real-world pain:** checkout 404 / "Page Not Found" (usually the WooCommerce checkout page isn't created/assigned, or a flow was deleted/trashed), the funnel falling back to the default WooCommerce checkout, and conflicts with third-party checkout-field-editor plugins (CartFlows has its own field editor) or themes. Standard fix = deactivate everything except CartFlows + WooCommerce, re-enable one by one.
- **Suite vs plugin pricing confuses sources:** the CartFlows Suite (~$199/yr) bundles 5 products (CartFlows Pro + Modern Cart Pro + Cart Abandonment Recovery Pro + Power Coupons Pro + OttoKit Pro); the standalone CartFlows Pro plugin is Starter/Plus/Pro tiered by site count. Lifetime deals exist (~$699 Plus / ~$999 Pro).
- **Affiliate program:** 20% commission, 60-day cookie, PayPal payout, $210 minimum / 2 referrals (cartflows.com/affiliates).
