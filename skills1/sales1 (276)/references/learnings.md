# KickoffLabs Learnings

Append discoveries, edge cases, gotchas, and workarounds here as they come up. Date each entry.

## 2026-06-01 — Initial skill creation

- Homepage `kickofflabs.com` fetched cleanly. `/pricing` redirects 301 to `app.kickofflabs.com/pricing` which also fetches cleanly.
- Two API versions coexist: v1 (form-encoded `/subscribe`, `/info` at `api.kickofflabs.com/v1/{CAMPAIGN_ID}`) and v2 (JSON at `api.kickofflabs.com/v2/{CAMPAIGN_ID}` with tags, leads, actions, leaderboard, approve, block, waitlist, verify, SMS, bulk endpoints). v1 still active for simple lead adds.
- API key + CampaignId are the auth primitives. KickoffLabs explicitly warns: "Your API Key should never be used in client side JavaScript." Use AnyForm/KOL.js for browser-side.
- v2 endpoint index pages at `dev.kickofflabs.com/api/` exist but per-endpoint pages mostly do NOT include full request/response JSON examples — captured what was available and noted gaps in the API reference.
- Webhook payload schema captured verbatim from a public GitHub gist by KickoffLabs employee Scott Watermasysk: `__event`, `__fraudulent`, `__referral`, `__reward_level`, `__score_change`, `__tagged` blocks layered on the base lead envelope.
- ⚠️ `duplidate_email` is a typo in KickoffLabs's own webhook payload docs — matches the literal string with the typo, NOT "duplicate_email". When writing handlers, match both to be safe.
- Webhook signing is undocumented in public material. No HMAC/signature header published. Flagged in API reference Gaps section.
- Rate limits scale with plan tier per support docs: ~10/min Hobby → ~100/min Enterprise. Specific headers + back-off response shape not documented in public pages.
- Reward-level emails, A/B testing, and tracking pixels are Premium+ (Hobby excludes them).
- Custom email templates + custom domains are Business+ ($99/mo annual).
- SMS Contests / SMS verification is Premium+ at $50/mo add-on; Enterprise includes.
- Auto-upgrade at $8 per 1,000 overage leads — campaign spikes can silently inflate bills. Recommend campaign-level lead caps + billing alerts.
- Leaderboard endpoint capped at 50 results — no pagination on `/leaderboard` itself.
- Capterra reviews flag: design customization limits ("section mechanic requires more options"), learning curve, pricing concerns. Customer support praised as fast and helpful.
- KickoffLabs's own guidance: "In most cases, we recommend using the AnyForm for custom pages instead of adding leads directly via the API."
- Native ESP connectors live: Klaviyo, Mailchimp, ActiveCampaign, Brevo. Website builders: Webflow, Wix, Squarespace, Weebly. E-commerce: Shopify. Other: Facebook Audiences, Slack, Zapier, Pipedream, Integrately.
- Community .NET SDK exists: `KickLib` (NuGet, not official).
- Confirmed via WebSearch: no MCP server exists for KickoffLabs (as of 2026-06-01).
- WebFetch on `/api/leads` and `/api/webhooks` returned 404 — the docs are structured per-endpoint at `dev.kickofflabs.com/{endpoint-name}/` (e.g. `/approve/`, `/leadtags/taglead/`, `/campaign-leaderboard/`).
