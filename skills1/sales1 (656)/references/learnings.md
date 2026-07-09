# Waitlister Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-06**: Initial research. Richest developer surface in the indie waitlist family: REST API (`waitlister.me/api/v1`, `X-Api-Key` header) with add/list/get/update subscriber + log-view, page/limit pagination (max 100), per-plan rate limits (Growth 60 RPM / Business 120 RPM on subscriber endpoints; 200/400 on log-view), and five HMAC-SHA-256-signed webhook events with retries + auto-disable after 10 consecutive failures. API + webhooks + Klaviyo/Mailchimp/Kit connectors + fraud detection ALL gate at Growth $49/mo.

**2026-06-06**: Distinctive vs siblings: built-in email broadcasts (monthly caps 2,500/10K/50K — overage undocumented) and unlimited subscribers from Launch $15/mo. NO Zapier/Make/MCP — confirmed absent; webhooks/API are the only automation path. No delete-subscriber endpoint. API signups bypass referral fraud detection unless `metadata.client_ip` + `fingerprint` are forwarded. `points` on PUT update-subscriber is absolute (write-the-total), not an increment.

**2026-06-06**: Waitlister runs its own comparison content (growth-hub guide + /alternatives pages vs Waitlist/GetWaitlist, Prefinery, LaunchList, Viral Loops, KickoffLabs, EarlyBird, Mailchimp, Kit, GrowSurf, Carrd) — useful for competitor discovery but it's first-party marketing; corroborate claims. AppSumo reviews (4.54/5, 13 reviews) flag limited referral reward-tier customization and missing advanced email segmentation. No affiliate program found. No GitHub org.
