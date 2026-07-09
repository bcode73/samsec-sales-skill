# Dodo Payments — Learnings

Accumulated, dated platform knowledge. Append new findings with a date stamp so staleness is auditable.

---

**2026-06-27**: Research baseline. Built from docs.dodopayments.com (API intro + `llms.txt` endpoint index + webhooks doc) and the marketing site.

- **Category:** developer-first **Merchant of Record (MoR)** for SaaS / AI / digital products. As MoR, Dodo is the legal seller and **remits global sales tax/VAT/GST** (220+ countries, 40+ payment methods) — the core value vs a raw processor (Stripe). 50,000+ users; PCI DSS L1; 99.99% uptime. Active (recent changelog: v1.105.0 June 2026).
- **API:** base **`https://test.dodopayments.com`** (test) / **`https://live.dodopayments.com`** (live). Auth **`Authorization: Bearer YOUR_API_KEY`** (Developer → API Keys, **read-only or read-write** per key). **Tiered dual-window rate limits** (Tier 0: 40/sec + 240/min; up to Tier 2: 500/5000; unauth 20/100); `X-RateLimit-*` headers; `429` → back off.
- **Endpoint groups:** Payments (one-time, list/get, invoice, line-items), Subscriptions (create/list/get/update, change-plan + preview + cancel-change, on-demand charge, usage history, update payment method), Products (CRUD, images/files, **localized prices**, short links, archive), Customers (CRUD, **customer-portal session**, payment methods, wallets + ledger), **Checkout Sessions** (create/get/preview), **License Keys** (create/get/activate/deactivate/instance) + Entitlements (grants/revoke/fulfill/files), Discounts (CRUD/validate/by-code), Refunds (create/list/get/receipt), Disputes (list/get), Payouts (list/breakup/CSV), Addons, Brands, Credit Entitlements/wallets, Balance Ledger.
- **Webhooks: Standard Webhooks spec.** Headers `webhook-id` / `webhook-signature` / `webhook-timestamp`; **verify with the `standardwebhooks` library** (don't hand-roll). Signing key from dashboard or `GET /webhooks/{id}/signing-key`. Full **webhook management API** (create/list/update/delete, headers, signing-key). Events cover payment/subscription/refund/dispute/license lifecycle — confirm exact event strings in the webhooks doc.
- **Local dev:** **Dodo CLI** `dodo wh trigger` forwards events over WebSocket (test-mode keys only); CLI mocks are **unsigned** → use `unsafe_unwrap()` in tests only.
- **DX is the differentiator:** **9 official SDKs** (TypeScript, Python, Go, PHP, Java, Kotlin, C#, Ruby, React Native), **framework adapters** (Next.js, Nuxt, Remix, SvelteKit, Astro, Bun, Express, Fastify, Hono, Tanstack, Convex, Better Auth, Supabase), Billing SDK (React/ShadCN), **MCP server** + "Agent Skills", and the CLI. This is the angle vs Paddle/Lemon Squeezy.
- **Pricing:** **~4% + $0.40/txn**, no monthly/setup fee (Standard); Enterprise custom. Higher than a processor because it includes tax handling/remittance. Payouts on a schedule (Payouts endpoints), not instant.
- **Competitive set:** Paddle (skill exists), Lemon Squeezy, Polar, Creem, Gumroad (MoR); Stripe + Stripe Tax (processor, calculates not remits). Covered by the `/sales-merchant-of-record` strategy skill.

⚠️ **Fetch note for future runs:** docs.dodopayments.com is fully fetchable, and **`docs.dodopayments.com/llms.txt`** is an excellent structured index (all endpoints as `.md`). The marketing site renders fine. Exact per-endpoint JSON + webhook event-type strings are the gap — pull the specific `/api-reference/{group}/{endpoint}.md` pages or the webhooks doc when needed.
