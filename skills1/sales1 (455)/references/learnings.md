# Rapidr Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform modules, pricing, integrations, and the SSO flow captured from live sources (rapidr.io homepage/pricing/features/integrations, help.rapidr.io SSO + Slack articles, G2 review snippets) on this date. Key facts: **no public REST/pull API** (G2-confirmed) — automation is JWT SSO + Zapier + native Slack/Intercom/Jira/HubSpot + voter CSV export. SSO (SAML & JWT) and user segmentation are **Business-plan ($199/mo)** features; no free tier (14-day trial). The detailed SSO/JWT docs page (`rapidr.io/docs/sso/`) is JS-rendered — exact JWT claim names, SSO endpoint path, and signing algorithm could not be captured and must be confirmed in-account. Zapier trigger/action names are not published — confirm in the live Zap editor. Several headline features (MRR/priority filters, roadmap prioritization scoring, embeddable roadmap widget, changelog reactions, changelog email digest, GDPR) were marked "Coming Soon" at research time. Re-verify all specifics against current docs before relying on them.
