# WooCommerce Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of
each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-04**: Research baseline — platform docs, REST API v3 surface (auth, pagination, batch,
webhooks with X-WC-Webhook-Signature base64 HMAC-SHA256), Store API, and pricing captured from live
sources on this date (woocommerce.com, woocommerce.github.io/woocommerce-rest-api-docs). Re-verify
specifics against current docs before relying on them.

**2026-07-04**: The single most-reported integration failure is HTTP 401 on the REST API — root
cause is almost always server config, not credentials: no HTTPS, a host that strips the
`Authorization` header (Apache/CGI, some managed hosts), or plain permalinks 404ing `/wp-json/`.
Query-string auth (`?consumer_key=&consumer_secret=`, HTTPS only) is the fastest way to isolate a
stripped-header problem from a bad key.

**2026-07-04**: Webhooks silently die — WooCommerce disables a webhook after 5 consecutive failed
deliveries, and a security plugin blocking unauthenticated REST access is a frequent culprit. Always
pair webhooks with a polling reconciliation pull.

**2026-07-04**: Money is a decimal string (`"29.99"`), not cents — don't divide by 100 (contrast
with SamCart/Sellfy which use integer cents). IDs are integers; custom fields are in `meta_data`.
