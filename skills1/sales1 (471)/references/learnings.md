# ReferralHero Learnings

Append discoveries, edge cases, gotchas, and workarounds here as they come up. Date each entry.

## 2026-06-01 — Initial skill creation

- Live site `referralhero.com` fetched cleanly; `/pricing` and `/integrations` pages also resolved without JS rendering issues.
- API docs at `support.referralhero.com/integrate/rest-api` and `/endpoints-reference` returned full content via WebFetch — copied verbatim into `referralhero-api-reference.md`.
- ⚠️ Prompt injection detected in WebFetch result from `/endpoints-reference` — an embedded `<system-reminder>` block about task tools. Stripped from `referralhero-api-reference.md`; flagged inline to the user.
- Capterra: 38 reviews, 4.5/5; G2 has fewer reviews (no specific count surfaced). Common positive: easy setup, responsive support. Common complaints: confusing reporting at first, want more native CRM integrations, lifetime-deal-to-monthly-sub migration frustrated early adopters.
- Pricing model is plan-cap-based with no overage scaling — "no scaled pricing" promise. SMS/MMS are pay-as-you-go on top.
- API access is plan-gated to PRO+ ($199/mo) — Free tier (25 subs) has no API access. Verify the user's plan before recommending programmatic flows.
- Multi-level referral mechanics support Level 1/2/3 with separate "all" (includes unqualified) vs confirmed-only endpoints — the most common source of "count is wrong" complaints.
- Coupon model requires a coupon group first; standalone coupon arrays without a group ID fail.
- Reward unlock via API is a two-step manual flow (`promote` → `unlock_promoted_reward`); the dashboard runs both server-side when milestone is hit, so manual API calls are only needed for external-driven reward logic.
- Native ESP connectors (Mailchimp, Kit, AWeber, Klaviyo, ActiveCampaign, SendLane) + 500+ Zapier apps. Make.com and Pipedream also have published apps.
- Confirmed via WebSearch: no MCP server exists for ReferralHero (as of 2026-06-01).
