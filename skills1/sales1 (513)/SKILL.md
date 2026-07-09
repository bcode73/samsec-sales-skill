---
name: sales-sellfy
description: "Sellfy platform help — creator storefront for digital products, print-on-demand merch, physical goods, and subscriptions with 0% transaction fees, PDF stamping/download limits, embeddable buy buttons, email marketing, affiliate program, and a webhook + Zapier automation surface (no public REST CRUD API). Use when setting up a Sellfy store or product, choosing between Sellfy Starter vs Business vs Premium, hitting Sellfy's annual sales-volume cap and being forced to upgrade, wiring Sellfy webhooks (New Order, Subscription, Cart Abandoned) into a CRM or fulfillment app, generating the Zapier API token, embedding Sellfy on an existing site, protecting digital downloads with PDF stamping, or troubleshooting Sellfy VAT/tax (it is NOT a merchant of record). Do NOT use for general digital-product strategy without a Sellfy context (use /sales-digital-products) or checkout-conversion optimization across carts (use /sales-checkout)."
argument-hint: "[describe what you need help with in Sellfy]"
license: MIT
version: 1.0.0
tags: [sales, creator-commerce, digital-products, platform]
github: "https://github.com/Sellfy"
---

# Sellfy Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Set up a new Sellfy store or add my first product
   - B) Sell a specific product type (digital download, print-on-demand merch, physical, subscription)
   - C) Configure pricing, coupons, upsells, or cart abandonment
   - D) Connect Sellfy to my email tool, CRM, or other apps
   - E) Embed Sellfy on my existing website
   - F) Set up or manage my affiliate program
   - G) Wire up webhooks or the Zapier API token for automation
   - H) Troubleshoot a payment, checkout, delivery, or tax issue
   - I) Choose a plan / decide whether to upgrade
   - J) Something else

2. **Which plan are you on (or considering)?**
   - A) Starter — $22/mo annual / $29/mo (up to ~$10k/yr in sales)
   - B) Business — $59/mo annual / $79/mo (up to ~$50k/yr)
   - C) Premium — $119/mo annual / $159/mo (up to ~$200k/yr)
   - D) Not sure / haven't signed up yet

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Digital product pricing/launch strategy (not Sellfy-specific) | `/sales-digital-products [question]` |
| Checkout conversion optimization theory (upsells, AOV, cart abandonment across carts) | `/sales-checkout [question]` |
| Choosing a Merchant of Record for global tax (Sellfy is NOT one) | `/sales-merchant-of-record [question]` |
| Email marketing strategy (sequences, segmentation) | `/sales-email-marketing [question]` |
| Membership/subscription content strategy & retention | `/sales-membership [question]` |
| Affiliate program design (commission models, recruitment) | `/sales-affiliate-program [question]` |

When routing, provide the exact command: "This is a {problem domain} question — run: `/sales-{skill} {user's original question}`"

## Step 3 — Sellfy platform reference

**Read `references/platform-guide.md`** for the full platform reference — product types, store builder, marketing tools, pricing/caps, integrations, data model, and workflows.

**Read `references/sellfy-api-reference.md`** if the question involves webhooks, the Zapier API token, the JSON payloads, or any automation/integration.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

You no longer need the platform guide — focus on the user's specific situation.

- **Product setup**: pick the right product type (digital / POD / physical / subscription), set delivery (auto-delivered download, POD fulfillment), and turn on PDF stamping + download limits for files you want to protect.
- **Plan selection**: model expected *annual revenue* against the tier caps ($10k / $50k / $200k) AND email volume — the cap, not just fees, is what forces an upgrade. There are no per-sale Sellfy fees, so the decision is subscription cost vs cap headroom vs gated features (upsells, cart abandonment, affiliates are Business+).
- **Integrations**: for real-time reactions to a sale, use a **webhook**; for no-code multi-app flows, use the **Zapier API token**. There is no public REST CRUD API to push/pull products or orders.
- **Tax**: Sellfy is NOT a Merchant of Record — you own VAT/GST/sales-tax compliance. If global tax is a dealbreaker, consider an MoR (Lemon Squeezy, Paddle, Gumroad).
- **Troubleshooting**: check Gotchas first, then the platform guide.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially items about plan-gated features, sales-volume caps, and integration gotchas that may be outdated.*

1. **Annual sales-volume caps force upgrades** — each tier caps yearly revenue (Starter ~$10k, Business ~$50k, Premium ~$200k). Cross the cap in a rolling 12-month window and Sellfy prompts an upgrade; even Premium tops out at ~$200k/yr, which can be a hard ceiling for scaling sellers.
2. **No public REST CRUD API** — you cannot programmatically create/read/update products or orders. The only developer surfaces are outbound **webhooks** and a **Zapier API token**. Plan integrations around those, not a REST API.
3. **Webhooks have NO HMAC signature** — Sellfy POSTs JSON but doesn't sign it. Protect your endpoint with a secret URL path / token query param and an IP/UA check; never trust payload contents blindly.
4. **Not a Merchant of Record** — Sellfy does not collect/remit VAT or GST for you. Selling internationally makes *you* liable for tax in the buyer's country.
5. **Key conversion features are Business+** — product upselling, cart abandonment, affiliate marketing, custom fields, branding removal, and store-design migration are gated above Starter. Confirm the lever you need is on your tier.
6. **Limited design & SEO** — ~10 themes, no category-page/URL customization, no built-in blog, limited metadata. For brand control, embed Sellfy's buy buttons/cart on your own site instead of relying on the hosted store.
7. **Only Stripe + PayPal** — no native gateway and a short processor list; processor fees (~2.9% + 30¢) still apply on top of Sellfy's 0% platform fee.

## Related skills

- `/sales-digital-products` — Digital product pricing, launch strategy, and platform comparison
- `/sales-checkout` — Checkout page optimization (upsells, order bumps, payment plans, cart abandonment)
- `/sales-merchant-of-record` — Choosing a MoR for global tax (Sellfy is not one)
- `/sales-membership` — Subscription/membership structure, pricing, and retention
- `/sales-affiliate-program` — Affiliate program design (commissions, recruitment, tracking)
- `/sales-payhip` — Payhip platform help (digital downloads, courses, all-features-on-free-tier alternative)
- `/sales-gumroad` — Gumroad platform help (digital products, license keys, MoR tax handling)
- `/sales-customcat` — CustomCat platform help (budget standalone US print-on-demand fulfillment if you want cheaper merch than Sellfy's built-in POD)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: First store setup
**User says**: "I want to sell a $19 ebook and a print-on-demand t-shirt on Sellfy"
**Skill does**: Walks through creating a digital product (upload file, enable PDF stamping + download limit) and a POD product (pick garment, upload design, set margin), recommends Starter while annual sales are under ~$10k, enables coupons, and connects an email tool for post-purchase follow-up.
**Result**: Both products live with download protection and a follow-up email path configured.

### Example 2: Plan / cap decision
**User says**: "I'm on Sellfy Starter doing about $1,200/mo — do I need to upgrade?"
**Skill does**: Annualizes to ~$14.4k, which exceeds the Starter ~$10k cap, so an upgrade to Business (~$59/mo annual) is required regardless of features; notes Business also unlocks upsells, cart abandonment, and affiliates; flags the ~$50k Business cap as the next ceiling.
**Result**: User upgrades to Business for headroom and the conversion features, before hitting the cap mid-launch.

### Example 3: Automation / developer question
**User says**: "How do I send every new Sellfy sale into my CRM and trigger fulfillment?"
**Skill does**: Explains there's no REST API — set up a **New Order webhook** (Integrations → Webhooks → title + HTTPS URL), parse the JSON (`id`, `products[]` with `key`/`variant`, `customer`, `amount` in cents), secure the endpoint with a secret path + IP check (no HMAC), and for no-code routing use the **Zapier API token** from `sellfy.com/user/integrations/apps/zapier` with a Completed-payment trigger. Points to `references/sellfy-api-reference.md` for payloads.
**Result**: Sales flow into the CRM in real time and kick off fulfillment.

## Troubleshooting

### Sale happened but my webhook/CRM didn't get it
**Symptom**: A purchase completed but no event reached your endpoint or Zap.
**Cause**: Webhook URL not HTTPS / unreachable, the Zap is filtered to the wrong event type, or amounts confused (Sellfy sends money in **cents**).
**Solution**: Verify the webhook URL is public HTTPS and returns 2xx fast. In Zapier, set the trigger event explicitly (Completed payment vs Refund vs leave blank for all). Treat `amount`/`plan_amount`/`total` as cents (449 = $4.49). Since there's no HMAC, dedupe on the order/subscription `id` to ignore retries.

### Buyers in the EU complain about missing/incorrect VAT
**Symptom**: International customers expect VAT handling or you get a tax bill.
**Cause**: Sellfy is not a Merchant of Record and does not remit tax for you.
**Solution**: Configure your own VAT/tax settings where available, keep records, and remit yourself — or move tax-heavy international sales to an MoR (Lemon Squeezy, Paddle, Gumroad). Run `/sales-merchant-of-record` to choose.

### My digital file is being shared / I hit a plan limit
**Symptom**: A purchased download is circulating, or a feature (upsell, cart abandonment, affiliates) is greyed out.
**Cause**: Download protection not enabled, or the feature is gated above Starter.
**Solution**: Enable **PDF stamping** and **download limits** on the product, and deliver via the unique auto-generated link rather than a public URL. For gated features, confirm you're on Business+ — upselling, cart abandonment, and affiliate marketing require it.
