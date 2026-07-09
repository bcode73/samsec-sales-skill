# Drupal Commerce Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of
each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-04**: Research baseline — platform docs, JSON:API surface (core `/jsonapi/{entity_type}/{bundle}`,
UUID-addressed, `application/vnd.api+json`, no PUT, `page[offset]`/`page[limit]` paging, filter/include/
fields), the Commerce API / Commerce Cart API contrib module (cart tokens, cart/checkout, Commerce-Current-Store
header, order state-transition webhooks), and Simple OAuth/Basic/JWT auth captured from live sources on this
date (drupalcommerce.org, drupal.org docs, github.com/drupalcommerce). Re-verify specifics against current
docs before relying on them.

**2026-07-04**: The #1 headless footgun — adding an item to a cart via raw JSON:API fails unless
anonymous users are granted "administer stores" (a security hole). Don't grant it; use the Commerce Cart
API module + a cart token, which abstracts order/order_item creation and scopes anonymous access.

**2026-07-04**: 401 ≠ 403 on this platform. 401 = missing/invalid OAuth token (or Simple OAuth not set
up); 403 = authenticated but the Drupal role lacks the per-permission access for that entity/operation.
Fix roles, don't over-permission. CORS must be configured for browser consumers.

**2026-07-04**: No core webhook UI. Order events come from the Commerce API module's order state-transition
webhook, or from a Drupal event subscriber (`commerce_order.place.post_transition` / `OrderEvents`), the
contrib Webhooks module, or Rules + HTTP. Always pair with a polling reconciliation pull and dedupe on the
order UUID. The public Commerce API webhook doc subpage was unreachable at research time — verify payload/
signature against the installed module version.
