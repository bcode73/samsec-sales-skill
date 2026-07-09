# WPFunnels — Learnings

Accumulated, dated platform knowledge. Append new findings with a date stamp so staleness is auditable.

---

**2026-06-27**: Research baseline. Built from the marketing site, the official webhooks doc, and CartFlows/FunnelKit comparison articles.

- **It's a WordPress plugin for WooCommerce, not a SaaS.** No hosted REST API, no MCP. Programmatic surface = **per-funnel outbound webhooks**, **Mail Mint** (bundled email automation, same vendor), **WooCommerce** order hooks/REST for the underlying orders, and **WordPress action/filter hooks**.
- **Webhook setup is documented; payload is NOT.** Funnel canvas → three-dot → **Webhook → Add Webhook**; fields **Name / Request URL / Request Method / Request Format / Webhook Event**; **Request Body = All Fields or Select Fields**; multiple webhooks per funnel; toggle/edit/delete from the list. The docs do **not** publish event names, the payload schema, custom-header support, or HMAC. Use **Select Fields** to pin keys and capture a live delivery before coding.
- **Revenue is WooCommerce.** Order bumps + one-click upsells/downsells are WooCommerce orders → read via the **WooCommerce REST API / order webhooks** (there's no WPFunnels read API). This is the #1 thing to tell a developer.
- **Mail Mint** is the bundled email engine (separate plugin, same team). Funnel **Event triggers** start Mail Mint automations (welcome, abandoned cart, post-purchase). Use it to keep email in WP; otherwise webhook→Zapier→ESP.
- **Page builders:** Elementor, Gutenberg, Divi, Bricks, Oxygen. **eCommerce:** WooCommerce. Positioned as easier than FunnelKit, broader than checkout-only CartFlows.
- **Pricing:** free on WordPress.org + **Pro** (webhooks, one-click upsells, order bumps, A/B testing, conditional steps). WPFunnels' exact Pro prices weren't captured (pricing page mentions a "Large Bundle" for agencies + 15-day money-back). Peer anchors: FunnelKit ~$99.50–$399/yr, CartFlows ~$79–$449/yr (+ lifetime). Confirm on site.
- **Competitive set:** CartFlows (checkout-focused), FunnelKit (funnels + built-in CRM/automation), plus the broader ClickFunnels/Systeme.io/Kartra SaaS funnel builders (already have skills). WPFunnels' angle: WordPress-native, WooCommerce, lower learning curve, bundled Mail Mint.

⚠️ **Fetch note for future runs:** the marketing homepage and `/docs/wpfunnels-webhooks-support/` render fine via WebFetch. Exact Pro pricing and the webhook payload schema are the known gaps — verify in-account.
