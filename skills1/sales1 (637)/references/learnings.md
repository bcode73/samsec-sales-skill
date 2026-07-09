# UpViral — Accumulated Learnings

Append durable, non-obvious findings here as they surface. Keep entries dated.

## 2026-06-02 — Initial research

- **API/webhooks gate at Business tier ($119/mo annual), not Starter ($79/mo).** This is the single biggest gotcha — Starter users cannot use the API or Callback URL at all. Always confirm tier before promising an integration.
- **Auth is form params, not a header.** `uvapikey` + `uvmethod` are form-encoded POST fields to `https://app.upviral.com/api/v1/`. No `Authorization: Bearer`.
- **Eight documented methods only**: `add_contact`, `get_lead_details`, `get_lead_details_by_email`, `get_leads`, `get_leads_points`, `add_points`, `get_custom_fields`, `lists`. No documented update/delete-contact method — flag if a user needs destructive ops.
- **Webhook = "Callback URL"**, configured per campaign, fires on events like reward-unlock. No documented HMAC signing.
- **Fraud detection is IP-matching + manual triage** (activate/delete/blacklist). Watch false positives from shared NAT/office/CGNAT IPs.
- **API page is JS-rendered** — WebFetch summarizes, doesn't reproduce verbatim. Per-endpoint bodies aren't public. Reference assembled from the official endpoint listing + apitracker.io/apirefs.com + support center + Zapier/Make/Pipedream listings.
- **No MCP server** (confirmed via research, June 2026).
- **Integration flakiness**: ClickFunnels, Shopify, funnel builders flagged unreliable in reviews; no native WordPress plugin despite "WordPress" in integration lists. Prefer Zapier/API.
- **B2C-only fit, fragile drag-and-drop builder, long first-campaign setup** — recurring review themes (socialrails, JoinSecret, Capterra). Capterra ~4.7/5 from 100+ reviews despite these.
- **Owned by Emarky**; live since 2015; 32,600+ businesses / 72.7M+ leads (vendor stats).
- **PHP SDK** exists (`composer require upviral/php-sdk`); no official JS/Python SDK.

## Sources
- https://upviral.com , https://upviral.com/pricing , https://www.upviral.com/api
- https://support.upviral.com/ (fraud detection, callback URL, Zapier integration articles)
- https://socialrails.com/blog/upviral-review , https://www.joinsecret.com/upviral/reviews
- https://www.queueform.com/blog/what-are-the-7-best-upviral-alternatives
- https://apitracker.io/a/upviral
