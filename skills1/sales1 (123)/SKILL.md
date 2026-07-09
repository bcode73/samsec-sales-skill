---
name: sales-convertri
description: "Convertri platform help — speed-focused sales funnel and landing-page builder (convertri.com): free-form drag-anywhere editor, AMP-fast CDN pages, integrated shopping cart with one-click upsells and bump sells, membership delivery, split testing, interactive video, and dynamic text replacement. Developer surface: a Zapier API key (8 triggers), custom webhooks (Sale, Rebill, Refund, Lead Capture) with cverify SHA-1 signing, and native ESP/payment/webinar integrations — but no public REST API. Use when a Convertri page won't publish or loads slowly, Zapier times out on a funnel with too many pages, you hit impression-overage charges, your cverify webhook signature won't verify, form leads or sales aren't syncing to your CRM, you want to automate without a REST API, or you're choosing between the Convert, Scale, and Maximize plans. Do NOT use for cross-tool funnel/CRO strategy (use /sales-funnel) or checkout conversion across carts (use /sales-checkout)."
argument-hint: "[describe what you need help with in Convertri]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
---

# Convertri Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken page — won't publish, loads slowly, custom domain stuck, page importer failed
   - B) Build a funnel/page — free-form editor, ready blocks, mobile design, split test, DTR, countdown
   - C) Sell — integrated cart, one-click upsells, bump sells, membership delivery, Stripe/PayPal
   - D) Wire automation — Zapier triggers, custom webhooks, sync leads/sales to a CRM or membership tool
   - E) Verify a webhook — the `cverify` signature, payload fields, secret key
   - F) Pick or compare a plan (Convert / Scale / Maximize) or sort out impression/video overages

2. **Which plan are you on?** Convert ($99/mo), Scale (~$199/mo), Maximize ($299/mo), or free trial. Several features below are plan-gated.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, conversion benchmarks across tools | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| Checkout/cart conversion strategy across carts (order bumps, upsells) | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |
| Email sequences after lead capture or purchase | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| Membership/community delivery strategy across platforms | `/sales-membership` — Run: `/sales-membership {user's original question}` |
| Generic CRM/ESP iPaaS wiring (Zapier/Make) | `/sales-integration` — Run: `/sales-integration {user's original question}` |

If the question is Convertri-specific, continue to Step 3.

## Step 3 — Convertri platform reference

**Read `references/platform-guide.md`** for the full platform reference — modules, pricing/plan gates, data model, integration recipes, code examples. For raw webhook/auth/trigger detail, read `references/convertri-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **No public REST API.** Convertri has no documented REST API to create or read pages/funnels programmatically. Automation runs through the **Zapier API key** (Account → Integrations → Zapier → Setup) and **custom webhooks**. If a user wants to "build pages via API," set that expectation up front and route them to webhooks/Zapier for the data-out side.
- **Keep funnels small for Zapier.** A funnel with too many pages makes the Zapier connection time out — keep **20 pages or fewer per funnel** when wiring Zaps.
- **Impression-based pricing.** Convert/Scale meter monthly **impressions**; overage is **$30 per extra 250k**. High-traffic pages can surprise the bill — Maximize removes the cap.
- **Verify webhooks with `cverify`.** Drop `cverify`, sort the remaining keys alphabetically, pipe-join the values, append `|<secret>`, UTF-8 encode, SHA-1 hash, uppercase the first 8 chars — that must equal `cverify`. Set the secret in Account settings.
- **Amounts are in pennies.** `ctransamount`/`ctaxamount`/`cshippingamount` are integers in the smallest currency unit ($10.00 = `1000`). Divide before display.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

1. **No public REST API.** You cannot programmatically create funnels/pages. Data-out automation is Zapier (one API key) + custom webhooks only. Plan integrations around that.
2. **Zapier times out on large funnels.** "Too many pages in a funnel means Zapier will time out and not load them all" — keep ≤20 pages per funnel when selecting pages in a Zap.
3. **Impression overages add up.** Convert (250k/mo) and Scale (500k/mo) charge **$30 per additional 250k impressions**; only Maximize is uncapped.
4. **Video hosting bandwidth is capped.** Self-hosted video (Scale/Maximize) includes 100GB/mo; overage is **$10 per additional 100GB**.
5. **`cverify` is SHA-1, first 8 chars, uppercase.** Easy to get wrong — keys must be sorted alphabetically and values pipe-joined with the secret appended last before hashing.
6. **Webhook caps differ by attach point.** Up to **5 webhook URLs per form**, but **unlimited per product**. Lead-capture webhooks don't fire unless you set the URL on the page.
7. **Pricing entry point is steep.** $99/mo (Convert) is high versus budget builders (LanderLab, Carrd); justify it with speed/cart/membership needs, not page count alone.

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, conversion optimization, and A/B testing methodology across tools
- `/sales-checkout` — Checkout/cart conversion strategy (order bumps, upsells, dunning) across cart platforms
- `/sales-clickfunnels` — ClickFunnels platform help — the all-in-one funnel/checkout/membership alternative
- `/sales-landingi` — Landingi platform help (AI landing pages, DTR, programmatic pages) — a lower-cost landing-page alternative
- `/sales-instapage` — Instapage platform help (AdMap, AI Experiments, post-click optimization) — the premium PPC alternative
- `/sales-membership` — Membership/community delivery strategy across platforms
- `/sales-email-marketing` — Email sequences to run after lead capture or purchase
- `/sales-integration` — Connect Convertri to a CRM or ESP via Zapier, Make, or webhooks
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync new sales into a CRM via webhook
**User**: "How do I push every Convertri sale into my CRM automatically?"
**Approach**: Convertri has no REST API, so use a **custom webhook** (or Zapier). Set a secret key in Account settings, then add your endpoint URL on the product's Advanced settings (unlimited webhooks per product). Convertri POSTs a **Sale** payload with `ccustemail`, `ccustname`, `cprodtitle`, `corderid`, `ctransamount` (pennies), `ctranspaymentmethod`, `ctranstime`, plus UTM/`fbclid`/`gclid` tracking. **Verify `cverify`** before trusting it, divide `ctransamount` by 100, then upsert into the CRM. For no-code, use the Zapier "New Product Sale" trigger instead. Pull the cURL/Python recipe + payload JSON from `references/convertri-api-reference.md`.

### Example 2: A page loads slowly / won't publish
**User**: "My Convertri page is supposed to be fast but it's crawling."
**Approach**: Convertri's selling point is sub-3s pages on its CDN — slowness usually traces to heavy custom HTML/CSS, large un-optimized images, third-party scripts/pixels, or self-hosted video exceeding bandwidth. Strip custom embeds to isolate, compress images, and confirm the custom domain's DNS/SSL finished provisioning before assuming a publish bug.

### Example 3: Choosing a plan for a launch with traffic + membership
**User**: "I'm running paid traffic to a funnel with a members area — which plan?"
**Approach**: Membership delivery and self-hosted video are **Scale+**; if paid traffic will exceed ~500k impressions/mo, the **$30/250k** overage on Scale can outweigh moving to **Maximize** (uncapped impressions, unlimited domains, client sub-accounts). Size the plan to expected ad volume, not page count — Scale already gives unlimited pages.

## Troubleshooting

### Zapier won't load my funnel's pages
**Symptom**: Selecting a page in a Zap trigger spins or errors.
**Cause**: The funnel has too many pages; Zapier times out before loading them all.
**Solution**: Keep the funnel to **20 pages or fewer**, or split it into multiple funnels. Re-test the Zap after trimming.

### Webhook `cverify` never matches
**Symptom**: Your signature check rejects every webhook.
**Cause**: Wrong key order, values not pipe-joined, secret not appended last, or hashing/encoding mismatch.
**Solution**: Remove `cverify`, **sort remaining keys alphabetically**, join values with `|`, append `|<secret>`, UTF-8 encode, **SHA-1** hash, take the **first 8 chars uppercased** — compare to `cverify`. Confirm the secret in Account settings matches the one in code.

### Surprise impression/bandwidth charges
**Symptom**: The bill is higher than the plan price.
**Cause**: Monthly impression cap (250k Convert / 500k Scale) or video bandwidth cap (100GB/mo) was exceeded.
**Solution**: Impressions overage is **$30/250k**, video bandwidth **$10/100GB**. Move high-traffic pages to **Maximize** (uncapped impressions) or offload video to YouTube/Vimeo to avoid bandwidth overage.
