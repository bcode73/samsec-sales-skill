# Wix eCommerce Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, API surface (Stores Products v3, eCommerce Orders), auth (API keys + OAuth), webhook JWT verification + resend policy, and pricing/plan gates captured from live sources (dev.wix.com REST docs + third-party pricing roundups) on this date. Re-verify specifics against current docs before relying on them.

**2026-06-29**: Wix dev docs expose a markdown mode — append `.md` to any `https://dev.wix.com/docs/` URL for clean machine-readable content; full index at `https://dev.wix.com/docs/llms.txt`, full concat at `https://dev.wix.com/docs/llms-full.txt`. Use this when fetching additional endpoint specs.

**2026-06-29**: eCommerce is plan-gated to **Core ($29/mo)+** — the Light plan can't run a store. Pricing (Light ~$17, Core ~$29, Business ~$39, Business Elite ~$159) is best-effort and changes; always confirm the specific feature isn't paywalled.

**2026-06-29**: Query Products (v3) does NOT return variant or price data — fetch via Get Product or the Variants API. Only id/handle/slug/createdDate/updatedDate/visible/options.id are filterable; unsupported filter fields error out.

**2026-06-29**: Webhooks are signed JWTs (not raw JSON) — verify with the app public key. Respond 200 within 1250 ms or Wix retries up to 12 times (1 min → escalating to 12 h). Expect duplicate + out-of-order delivery; some payloads are partial (do a follow-up GET).
