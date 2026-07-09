# Referlist Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-19**: Research baseline — platform features, 5 install methods, npm SDK usage, pricing tiers, and REST API capabilities captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-19**: REST API specifics unavailable — docs.referlist.co is a JS-rendered SPA and the public SDK repo (`parthibanloganathan/referlist-sdk`) is client-side only (last pushed 2022). The client-side SDK is fully documented (`initialize({domain})`, element IDs `referlistemail`/`referlistbutton`, `window.referlist.addToWaitlist(domain, email, referralCode)`), but the REST base URL, auth header, and endpoint paths must be verified in the signed-in docs — they are NOT documented in this skill, only the capabilities (add signup / get place in line / list signups). Do not fabricate them.

**2026-06-19**: No webhooks/Zapier found in any source — egress is the Pro REST API (poll) or CSV/Mailchimp/Airtable export. Treat real-time push as unconfirmed.

**2026-06-19**: Pricing is best-effort — an older Product Hunt listing cited "$50/mo unlimited"; current tiers are Free (100) / Growth $29 (500) / Pro $59 (3,000, API) / Enterprise usage-based (~$0.01/signup/mo). Re-check the live pricing page.
