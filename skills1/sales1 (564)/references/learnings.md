# Squarespace Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, Commerce API surface (Orders v1.0, Inventory v1.0, Products v2, Transactions v1.0, Contacts, Webhook Subscriptions v1.0), pricing, and webhook signature verification captured from live sources (developers.squarespace.com + pricing roundups) on this date. Re-verify specifics against current docs before relying on them.

**2026-06-29**: Plan-naming ambiguity — Squarespace docs reference both the legacy "Business / Commerce Basic / Commerce Advanced" plans and the current "Basic / Core / Plus / Advanced" plans. Dev docs list Orders/Inventory APIs on Core/Plus/Advanced/Commerce Advanced; some third-party reviews claim Commerce API access is Advanced ($99/mo) only. Treat the exact API plan gate as best-effort and confirm against the target site's plan.

**2026-06-29**: Webhook Subscriptions API requires **OAuth** — an API key cannot create webhook subscriptions. A single-site automation using an API key can still poll `GET /commerce/orders?modifiedAfter=...&modifiedBefore=...`. This is the most common "why won't my webhook register" confusion.

**2026-06-29**: HMAC secret is **hex-encoded** and must be decoded to raw bytes before computing HMAC-SHA256, signed over the **raw** request body. Hashing a re-serialized parsed JSON body, or using the hex string directly as the key, both fail verification. Header is `Squarespace-Signature`.

**2026-06-29**: Money is a `{currency, value}` decimal object, NOT integer cents (contrast with Square Online and Sellfy which use cents). Easy to get wrong when reusing a Square/Sellfy integration as a template.

**2026-06-29**: No official Squarespace MCP server found at research time. Don't claim one exists.
