# FunnelKit — Learnings

Accumulated, dated platform knowledge. Append new findings with a date stamp so staleness is auditable.

---

**2026-06-27**: Research baseline. Built from the marketing site (funnelkit.com), the developer docs (developers.funnelkit.com), the Automations webhooks docs, and CartFlows/ClickFunnels comparison articles.

- **Two-plugin suite on WordPress/WooCommerce** (formerly **WooFunnels**; automation plugin formerly **Autonami**): **Funnel Builder** (checkout, rule-based order bumps, one-click upsells/downsells, A/B testing, sliding cart, opt-in/sales/thank-you pages, analytics) + **Automations** (CRM, email/SMS, segments, broadcasts, transactional email, cart-abandonment, workflow builder). Self-hosted — **no hosted SaaS/MCP**.
- **REST API is the Automations side.** Base `https://{site}/wp-json/funnelkit-automations/`, auth via **`?api_key=` query param** (generate in Automations → Settings → REST API). Endpoints: **Tags**, **Lists**, **Fields** (custom fields), **Contacts** (CRUD + `update-email`, `change-status`, `tag-assign/unassign`, `list-assign/unassign`). Responses `{code,data,limit,offset}` (offset pagination). Error codes 400/401/403/404/405/406/422/500.
- **Contact** is the core object: email-keyed, `status` ∈ subscribed|bounced|unsubscribed|verified, with tags/lists/fields. **Tags/lists drive automations.**
- **Webhooks (Automations):** **incoming** (a Webhook URL you plug into other apps → triggers an automation; supports **Conditions**) and **outgoing** (an **HTTP Request** action inside an automation). Full payload schema/signatures not on the overview page — confirm on the Incoming/Outgoing subpages; capture a live delivery; treat incoming URL as secret.
- **Funnel revenue = WooCommerce orders.** Order bumps + one-click upsells are WooCommerce orders; **no funnel-read REST API** — use the **WooCommerce REST API** (`/wp-json/wc/v3/orders`) / order webhooks. This is the #1 dev gotcha (people look for a funnel API that doesn't exist).
- **Integrations:** WooCommerce, Divi (+ other builders), 15+ payment gateways (Stripe/PayPal/Mollie/Authorize.Net CIM/Braintree/SagePay), Zapier/Make/Integrately/Pabbly, Slack, Twilio (SMS), WP Fusion, LMS (LearnDash/LifterLMS/TutorLMS), AffiliateWP. New: **Sublium** (WooCommerce Subscriptions).
- **Pricing:** free Lite (both plugins) + Pro; **bundles** Plus/Professional/Elite (~$99.50–$399/yr, up to ~30 sites on Elite). 14-day money-back. Restructures often — verify. Peers: CartFlows ~$79–$449/yr, WPFunnels (free + Pro). 40,300+ store owners, 4.9★ (981+ reviews).
- **Positioning:** more than a funnel builder — the **built-in CRM/automation engine** is the differentiator vs checkout-only CartFlows and the lighter WPFunnels (which bundles Mail Mint instead).

⚠️ **Fetch note for future runs:** marketing site + `developers.funnelkit.com` + `/docs/autonami-2/webhooks/` all render via WebFetch. Exact bundle names/prices and full webhook payload schemas are the known gaps — verify in-account.
