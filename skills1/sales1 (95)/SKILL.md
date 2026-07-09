---
name: sales-checkout
description: "Optimizes BUYER-side checkout pages, upsells, order bumps, payment collection, and cart abandonment recovery — increase average order value and reduce checkout friction. Use when checkout conversion rate is too low, cart abandonment is high, average order value isn't growing, not sure which checkout platform to pick, payment plans not converting, or buyers dropping off at the payment step. Do NOT use for full funnel strategy (use /sales-funnel), email follow-up after purchase (use /sales-email-marketing), affiliate tracking on sales (use /sales-affiliate-program), or supply-side / seller-side marketplace payouts to 1099 workers, sellers, drivers, or creators (use /sales-marketplace-payouts). For Groove-specific help, use /sales-groove."
argument-hint: "[describe your checkout question — e.g., 'add an order bump to my checkout' or 'reduce cart abandonment']"
license: MIT
version: 1.0.4
tags: [sales, checkout, payments, conversion, ecommerce]
---
# Checkout Optimization

You are a checkout optimization specialist. Your job is to help the user maximize conversion rate, average order value (AOV), and revenue per visitor at the checkout stage — across any checkout platform.

## Step 1: Gather Context


If `references/learnings.md` exists, read it first for accumulated knowledge.

Before making recommendations, understand the situation. Ask the user for any missing details:

- **Product type**: Digital product, course, SaaS, physical product, coaching/service, membership?
- **Price point**: What is the main offer price? Are there multiple tiers?
- **Current conversion rate**: What percentage of visitors who reach checkout actually complete the purchase? (Industry benchmarks: 30-50% for warm traffic landing on a checkout page; 1-3% for cold traffic on a full sales page with embedded checkout.)
- **Checkout tool**: Which platform are they using? (GrooveSell, ThriveCart, SamCart, Ecwid, Snipcart, Foxy, Stripe Checkout, Paddle, Gumroad, Shopify Checkout, BigCommerce, Medusa, Saleor, Wix eCommerce, WooCommerce, Lemon Squeezy, PayKickstart, Jotform, or another.)

For platform-specific checkout guidance (Jotform, Builderall SuperCheckout, etc.), see `references/platforms.md`.
- **Payment processors**: Stripe, PayPal, Authorize.net, or others? Are both credit card and PayPal enabled?
- **Existing upsells/order bumps**: Do they already have any post-purchase offers or order bumps configured?
- **Traffic source**: Where does checkout traffic come from — ads, organic, email, webinar, sales page?
- **Cart abandonment rate**: If known, what percentage of users start checkout but don't finish?

## Step 2: Strategy

**Read `references/platform-guide.md`** for detailed module documentation, pricing, integrations, and data model.

*You no longer need the platform guide details — focus on the user's specific situation.*

## Step 3: Actionable Guidance

### Checkout Page Layout

Recommended layout from top to bottom:
1. Logo and product name (keep branding minimal — this is not a sales page)
2. Order summary with product image, name, and price
3. Order bump (checkbox with short benefit copy)
4. Billing information form (name, email, payment)
5. Payment method selector (credit card + PayPal at minimum)
6. Coupon code field (optional — collapsible so it doesn't distract)
7. Trust elements row (guarantee badge, secure checkout badge, payment logos)
8. Purchase button (large, high-contrast, action-oriented text: "Complete My Order" not "Submit")
9. Short testimonial or proof element beneath the button
10. Refund policy link in footer

### Checkout Copy

- **Headline**: Restate the offer, not "Checkout." Use: "Complete Your Order" or "You're almost there — finish your order below."
- **Button text**: Use first-person, benefit-oriented language. "Yes, Give Me Instant Access" converts better than "Buy Now."
- **Bump copy**: Start with "YES!" followed by a one-sentence benefit. Example: "YES! Add the Quick-Start Templates for just $37 and save 10+ hours on setup."
- **Reassurance copy**: Near the payment fields, add: "Your payment info is secured with 256-bit encryption." This reduces anxiety at the exact moment of data entry.

### Mobile Optimization

- Over 60% of checkout traffic is mobile. Test your checkout on an actual phone.
- Stack elements vertically — no side-by-side columns on mobile.
- Make the purchase button full-width and sticky at the bottom of the screen.
- Ensure form fields are large enough to tap easily (minimum 44px height).
- Enable Apple Pay and Google Pay for one-tap mobile purchases.

### A/B Testing Checkout Elements

**Always be testing at least one checkout element.** Systematic A/B testing is the most reliable way to improve checkout conversion. Test one element at a time to isolate impact. Here are the highest-impact elements to test, in priority order:

1. **Price point** — Test $97 vs. $127 vs. $67. You may find a higher price converts nearly as well, increasing revenue.
2. **Payment plan options** — Test offering a payment plan vs. not, and test different split structures.
3. **Order bump** — Test with bump vs. without, and test different bump offers.
4. **Button text** — Test "Complete My Order" vs. "Get Instant Access" vs. "Yes, I Want This."
5. **Checkout page length** — Test minimal (just form) vs. with testimonials and guarantee copy.
6. **Trust elements** — Test with/without testimonials near the buy button, guarantee badge placement, payment method logos.

Run each test until you hit at least 100 conversions per variant (or use a statistical significance calculator). Don't call a winner early — premature conclusions lead to wrong optimizations.

### Abandoned Cart Email Sequence

**Email 1 — Reminder (1 hour after abandonment):**
Subject: "You left something behind"
Body: Remind them what they were buying. Include a direct link back to the checkout with their cart preserved. No discount yet.

**Email 2 — Objection handling (24 hours):**
Subject: "Quick question about [Product]"
Body: Address the top 2-3 objections (price, trust, "is this right for me"). Include a testimonial. Link back to checkout.

**Email 3 — Final chance (48-72 hours):**
Subject: "Last chance — your cart expires soon"
Body: Create urgency. Optionally add a small incentive (bonus or 10% discount). Final link to checkout.

### Payment Plan Configuration

- Set up automated dunning: retry failed payments at day 1, day 3, and day 7 after failure.
- Send a "payment failed" email with a link to update payment info.
- Revoke access to digital products only after all retry attempts fail (typically after 14 days).
- For high-ticket offers ($1,000+), consider a deposit + balance structure instead of equal installments.
- **Platform tip**: GrooveSell charges zero transaction fees on payment plans — you only pay your payment processor's fees (Stripe ~2.9% + $0.30). This makes multi-payment plans more cost-effective than platforms that charge per-transaction fees on each installment.

### Tax Handling

- For digital products sold in the EU, VAT must be collected. Use a merchant-of-record platform (Paddle, Lemon Squeezy) or a tax tool (Stripe Tax, TaxJar, Quaderno).
- In the US, sales tax on digital products varies by state. Stripe Tax or TaxJar can automate calculation and collection.
- Always show tax as a separate line item on the checkout page — never surprise the buyer with a higher total at the last moment.

## Gotchas

1. **Asking for too much information**: Every additional form field reduces conversion. Do not ask for a phone number, company name, or shipping address on digital product checkouts unless absolutely necessary.
2. **Missing payment methods**: Not offering PayPal loses 15-30% of potential buyers who prefer it. Always offer at least two payment methods.
3. **Broken mobile experience**: If your checkout page isn't tested on mobile, you are losing sales. Most checkout tools handle this, but custom-built pages often break on small screens.
4. **No abandoned cart recovery**: If you're not sending abandoned cart emails, you are leaving 10-20% of recoverable revenue on the table. This is the highest-ROI automation you can set up.
5. **Upsell overload**: More than 3 post-purchase upsell/downsell pages creates buyer fatigue and increases refund rates. Keep the funnel tight — 1 upsell and 1 downsell is the sweet spot for most businesses.

- **Self-improving**: If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Before recommending a specific platform skill

This skill covers a strategy domain across many platforms. **Before pointing the user to any specific platform skill** (any `/sales-{platform}` listed in `## Related skills`, e.g., `/sales-mailshake`, `/sales-klaviyo`, `/sales-apollo`), read that platform skill's actual `SKILL.md` first. The 1-line description in `## Related skills` is enough to *identify* a candidate — it's not enough to *commit* to it or to write a prompt that invokes it well.

**How to read it:**
- If `~/.claude/skills/{skill-name}/SKILL.md` exists locally, `Read` it.
- For `sales-*` skills, `WebFetch` directly from this repo: `https://raw.githubusercontent.com/sales-skills/sales/main/skills/{skill-name}/SKILL.md` — e.g., for `sales-mailshake`: `https://raw.githubusercontent.com/sales-skills/sales/main/skills/sales-mailshake/SKILL.md`.
- For non-`sales-*` skills (third-party), look up `{org}/{repo}` in `~/.claude/skills/sales-do/references/skill-sources.md` if installed and fetch the same `skills/{skill-name}/SKILL.md` path under that repo.

**After reading,** ground your recommendation in something concrete from the SKILL.md (its scope, a sub-flow, its `argument-hint` shape, or a "Do NOT use for..." negative trigger). Align any generated invocation with the platform skill's `argument-hint`. If the platform skill turns out not to fit the user's situation, swap to another or handle the question here directly rather than recommending a poor fit.

## Related Skills

- `/sales-groove` — Groove.cm-specific configuration for GrooveSell, GroovePages, GrooveMail, and GrooveMember.
- `/sales-funnel` — Full funnel strategy, page sequencing, and traffic-to-sale architecture.
- `/sales-email-marketing` — Post-purchase email sequences, abandoned cart emails, and nurture campaigns.
- `/sales-affiliate-program` — Setting up affiliate tracking on checkout pages and managing affiliate payouts.
- `/sales-membership` — Delivering digital products and courses after purchase, including access provisioning.
- `/sales-kit` — Kit platform help (Kit Commerce for digital products and subscriptions)
- `/sales-digital-products` — Digital product sales strategy (pricing, platform selection, launch)
- `/sales-gumroad` — Gumroad platform help (digital product checkout, license keys, Discover marketplace)
- `/sales-payhip` — Payhip platform help (embedded checkout, cross-selling, coupons)
- `/sales-lemonsqueezy` — Lemon Squeezy platform help (hosted/overlay/embedded checkout, subscriptions, tax as MoR)
- `/sales-paddle` — Paddle platform help (Merchant-of-Record checkout + subscriptions + global tax; Billing API, HMAC webhooks)
- `/sales-thrivecart` — ThriveCart platform help (lifetime-license cart: order bumps, 1-click upsells, affiliate center, Event Subscription API/webhooks; Pro+ $295/yr gating; no download protection; Learn deprecated)
- `/sales-samcart` — SamCart platform help (subscription-priced cart: order bumps/upsells/A-B testing on Pro, Subscription Saver dunning, Affiliate Center; read-mostly REST API in private beta + unsigned Notify URL webhooks)
- `/sales-checkoutpage` — Checkout Page platform help (no-code Stripe checkout builder for digital products/subscriptions/payment plans/event tickets; 0% platform fee with sales-volume-cap pricing; REST API + unsigned conversion webhooks with decimal-string money + a native MCP server at mcp.checkoutpage.com; Stripe-only; not a Merchant of Record)
- `/sales-ecwid` — Ecwid platform help (embeddable store/checkout for existing sites; REST v3 + HMAC-signed webhooks with the client_secret signing footgun; plan-gated API; 0% platform fees)
- `/sales-snipcart` — Snipcart platform help (developer-first JS cart for static/JAMstack sites; data-item-* products, crawler price validation, REST API + token-validated webhooks, official MCP server; 2% or ~$20/mo)
- `/sales-foxy` — Foxy platform help (hosted cart/checkout layer, Webflow's usual upgrade path; HMAC-signed links + hAPI hypermedia API + signed webhooks with retry/auto-deactivate semantics; 1% capped per-transaction fee)
- `/sales-store-migration` — Moving an existing store between platforms (redirect maps, delta sync, migration tools) — the companion to choosing a new platform here
- `/sales-shopify` — Shopify platform help (full commerce backend: products/orders/customers/checkout; GraphQL Admin API + HMAC-signed webhooks; Checkout Extensibility is Plus-tier; REST legacy)
- `/sales-bigcommerce` — BigCommerce platform help (open-SaaS commerce backend: products/orders/customers/checkout; REST Management API v3 + legacy v2 Orders, GraphQL Storefront/Admin; thin no-HMAC webhooks; $0 fee on embedded payments; not a Merchant of Record)
- `/sales-medusa` — Medusa platform help (open-source MIT headless commerce engine: self-host or Medusa Cloud; Admin/Store REST APIs, JWT/API-key/session auth; events + subscribers instead of native outbound webhooks; 0% GMV fee; not a Merchant of Record)
- `/sales-saleor` — Saleor platform help (open-source BSD-3, GraphQL-first headless commerce: self-host or Saleor Cloud; single GraphQL endpoint, JWT/OIDC + long-lived App tokens, JWKS; native sync/async webhooks with JWS-RS256 signatures — HMAC deprecated; checkoutCreate → orderCreateFromCheckout; not a Merchant of Record)
- `/sales-bagisto` — Bagisto platform help (open-source MIT Laravel/PHP commerce framework by Webkul: self-host or Bagisto Cloud; REST + GraphQL APIs split Shop/Admin, X-STOREFRONT-KEY + Laravel Sanctum bearer auth, guest cart tokens; no native outbound webhooks — use Laravel events/listeners or polling; marketplace/POS are paid extensions; not a Merchant of Record)
- `/sales-spree` — Spree platform help (open-source BSD-3 headless commerce framework on Ruby on Rails: self-host Community Edition or buy Enterprise; Store API publishable-key + order-token, Platform API OAuth2 client-credentials, open-sourced Admin API scoped keys; native outbound webhooks + delivery log; JSON:API pagination; first-class AI-agent tooling/docs MCP; version-upgrade + Rails-ops caveats; not a Merchant of Record)
- `/sales-wix` — Wix eCommerce platform help (no-code website builder + native store: Stores v3 + eCommerce Orders REST APIs, API-key/OAuth auth, signed-JWT webhooks; eCommerce gated to Core+; JS-heavy SEO/perf + template lock-in caveats; not a Merchant of Record)
- `/sales-square-online` — Square Online platform help (free-to-start store unified with Square POS: Catalog/Orders/Inventory/Payments APIs, Bearer/OAuth auth with 30-day token expiry, HMAC webhooks over URL+body, official MCP server; POS↔online inventory-sync/oversell caveat; site builder is UI-only; not a Merchant of Record)
- `/sales-squarespace` — Squarespace platform help (design-first website builder's commerce backend: Orders/Inventory/Products/Transactions/Contacts Commerce APIs, Bearer API-key or OAuth auth, OAuth-only webhooks with HMAC-SHA256 over raw body using a hex secret; Commerce API + abandoned-cart + subscriptions gated to Advanced; no multi-currency; Squarespace Payments holds caveat; site builder is UI-only; not a Merchant of Record)
- `/sales-sellfy` — Sellfy platform help (creator storefront for digital products/POD/subscriptions, 0% platform fee with annual sales-volume caps, PDF stamping + download limits, no REST API — webhooks + Zapier token only, no HMAC; upsells/cart-abandonment are Business+; not a Merchant of Record)
- `/sales-swell` — Swell platform help (API-first headless SaaS commerce backend with a native subscription engine: Backend REST API on api.swell.store + secret key over port 8443, Frontend swell-js/GraphQL with a public key; thin no-HMAC webhooks verified by IP allowlist; subscriptions Basic+, multi-currency Standard+; no transaction fee; not a Merchant of Record)
- `/sales-evershop` — EverShop platform help (open-source GPL-3.0 Node.js/TypeScript/React/GraphQL commerce platform on PostgreSQL: storefront+admin+API in one self-hosted project; REST for writes + GraphQL for reads, JWT auth with a 15-minute admin token; no outbound webhooks — use in-process event subscribers or poll; self-host only, Node 20+/Postgres 13+; no per-sale fee; not a Merchant of Record)
- `/sales-sendowl` — SendOwl platform help (secure-delivery cart for digital goods: download-limit/expiry links, PDF stamping, license keys, subscriptions, drip, upsells; REST API on /api/v1 with orders on /api/v1_3 + HMAC-signed webhooks; subscription pricing with annual order/sales caps and no free tier; the download-protection answer; not a Merchant of Record)
- `/sales-prestashop` — PrestaShop platform help (open-source, self-hosted PHP/MySQL store with a 300+ feature back office + module/hook system; CRUD Webservice REST API at /api/ with HTTP Basic 32-char-key auth, XML/JSON output, ~70 resources; PUT is a full replace, stock lives on stock_availables; the CGIPassAuth 401 footgun; no native outbound webhooks — use a module hook, a third-party Webhooks module, or poll; free Classic vs ~€29/mo Hosted; not a Merchant of Record)
- `/sales-woocommerce` — WooCommerce platform help (the most-installed self-hosted WordPress commerce plugin; REST API v3 at /wp-json/wc/v3 with HTTP Basic consumer key/secret over HTTPS or OAuth 1.0a, offset pagination max 100 + X-WP-Total headers, /batch endpoints; signed webhooks X-WC-Webhook-Signature base64 HMAC-SHA256 that auto-disable after 5 failures; the stripped-Authorization-header 401 footgun; headless Store API; money as decimal string; no platform fee; not a Merchant of Record)
- `/sales-shopware` — Shopware platform help (open-source PHP/Symfony mid-market/B2B commerce; free Community Edition MIT + paid Rise/Evolve/Beyond under a €1M-GMV fair-usage gate; Admin API /api/* with OAuth client-credentials from an Integration + search-Criteria query model POST /api/search/{entity} + Sync API, 300 req/min; headless Store API /store-api/* with sw-access-key; App-system webhooks signed shopware-shop-signature HMAC-SHA256 + Flow Builder; the plugin-key-can't-mint-a-token 401 footgun; UUID ids; not a Merchant of Record)
- `/sales-drupal-commerce` — Drupal Commerce platform help (open-source GPL commerce framework on Drupal/PHP by Centarro; commerce objects are Drupal entities; headless via core JSON:API at /jsonapi/{entity_type}/{bundle} — UUID-addressed, no PUT, page[offset]/page[limit] paging — plus the Commerce Cart API module for cart token/checkout + order-transition webhooks; Simple OAuth/Basic/JWT auth; the add-to-cart-needs-administer-stores permission footgun; 401-vs-403 role model; content-heavy/custom-catalog dev build; not a Merchant of Record)
- `/sales-multichannel-selling` — Selling one catalog across marketplaces (Amazon/eBay/Etsy/Walmart/TikTok Shop) from your store backend — channel selection, oversell prevention, and channel-manager tools (LitCommerce/Sellbrite/Codisto). Use this when the question is about *adding sales channels*, not optimizing the checkout itself.
- `/sales-litcommerce` — LitCommerce platform help (multichannel listing & 15-minute inventory/order sync; no public API — integrate at the store backend)
- `/sales-merchant-of-record` — Choosing a Merchant of Record / payments provider (Paddle vs Lemon Squeezy vs Polar vs Stripe; MoR vs self-managed tax)
- `/sales-vwo` — VWO platform help (A/B test checkout pages, heatmaps, session recordings, form analytics)
- `/sales-jotform` — Jotform platform help (payment forms, order forms, donation collection — simpler than dedicated checkout tools)
- `/sales-builderall` — Builderall platform help (SuperCheckout order bumps/upsells inside a budget all-in-one suite; checkout is UI-only — drive post-purchase flows via MailingBoss tags)
- `/sales-do` — Route any sales question to the right skill.

## Examples

### Example 1: Adding an order bump to a course checkout

**User**: "I'm selling a $197 online course and want to add an order bump. What should I offer and how should I set it up?"

**Approach**:
1. Recommend a complementary resource priced at $37-$67 (30-50% of the main offer). Good options: a workbook/template pack, a quick-start guide, or a bonus module.
2. Place the bump as a checkbox on the checkout page between the order summary and the payment form.
3. Write bump copy: "YES! Add the Implementation Workbook for just $47 — follow along step-by-step and finish the course 3x faster."
4. Target a 20-40% take rate. If take rate is below 20%, test a different offer or lower the bump price.
5. Provide platform-specific setup steps based on their checkout tool.

### Example 2: Diagnosing a low checkout conversion rate

**User**: "My checkout page only converts at 20%. What's wrong?"

**Approach**:
1. Benchmark: 20% is below average for warm traffic (expect 30-50%). Identify whether the issue is traffic quality or checkout friction.
2. Audit the checkout page: count form fields, check for trust badges, verify mobile experience, confirm payment options.
3. Check for surprise costs — tax or shipping added at checkout is a top abandonment driver.
4. Review whether abandoned cart recovery is in place.
5. Recommend specific A/B tests in priority order: simplify form fields, add trust elements, test button copy, add a guarantee badge.

### Example 3: Full checkout funnel setup in Groove.cm

**User**: "Set up a checkout with upsell and payment plan in Groove."

**Approach**:
1. Create the product in GrooveSell with two pricing options: pay-in-full (with a small discount or bonus) and a 3-payment plan.
2. Build a checkout page using GrooveSell's template editor. Add trust badges, order summary, and a guarantee.
3. Add an order bump — configure the bump product, set the price, and write the checkbox copy.
4. Configure the post-purchase upsell: create the upsell product, set it as the next step after purchase, and build a short upsell page with a video and accept/decline buttons.
5. Add a downsell if the upsell is declined — offer a payment plan version or a lighter offer.
6. Connect GrooveMail for the abandoned cart email sequence and post-purchase delivery emails.
7. Set up webhook events for purchase_completed and payment_failed to trigger automations.
8. Test the entire flow end-to-end with a test purchase.

## Troubleshooting

### "My order bump take rate is under 10%"

- Check the bump placement — it should be directly above the payment button, not buried below.
- Rewrite the copy to focus on a specific outcome, not just features. "Save 10 hours" is stronger than "Includes 15 templates."
- Lower the bump price. If the bump is more than 50% of the main offer price, it may feel too expensive as an impulse add-on.
- Ensure the bump is visually distinct — use a colored border or background to draw attention.

### "Customers are abandoning checkout at the payment step"

- Verify both Stripe and PayPal are working. Test a purchase yourself.
- Check for unexpected tax or shipping costs being added at the payment step.
- Add reassurance copy near the payment fields: "Secured with 256-bit encryption. 30-day money-back guarantee."
- Enable Apple Pay and Google Pay for mobile buyers who don't want to type card numbers.
- Review if 3D Secure authentication is causing friction — some payment processors require extra verification steps that add friction.

### "My upsell page converts under 5%"

- Make sure the upsell is directly related to what they just bought. An unrelated offer will convert poorly.
- Shorten the upsell page — after purchase, buyers want confirmation, not another long sales pitch. A short video (60-90 seconds) with a clear offer works best.
- Ensure the "Yes" button is prominent and the "No thanks" link is clearly visible. If buyers feel trapped, they will close the tab instead of declining.
- Test the price — the upsell might be priced too high relative to what they just paid. Try a lower entry point or a payment plan option.
