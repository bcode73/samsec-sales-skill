# FeedBear Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, integration/webhook/SSO surface, and pricing captured from live sources on this date (feedbear.com/integrations, /pricing; help.feedbear.com webhooks + SSO articles; G2/Capterra review snippets; alternatives roundups). Re-verify specifics against current docs before relying on them.

**2026-06-29**: Key distinguishing fact — FeedBear has **no public REST/pull API** (only outbound webhooks + JWT SSO + Zapier + native Intercom/Slack/Trello/Jira). This is the main thing that separates it from Frill/FeatureOS/Sleekplan, which all expose REST pull APIs. Design integrations around push, not pull.

**2026-06-29**: Webhook **payload schema was not fetchable** — the help article (help.feedbear.com/article/30-webhooks) renders the per-event payload details client-side at the bottom of the page, and WebFetch could not retrieve them. The constructed payload in the api-reference is a placeholder; capture a live delivery to confirm exact field names and event strings.

**2026-06-29**: Webhooks are **not documented as HMAC-signed** (unlike Frill). Secure via secret URL + IP allowlist + payload validation + dedupe on idea id.

**2026-06-29**: Pricing (best-effort): Lite $19 ($15 yr) / Startup $49 ($40 yr) / Business $99 ($82 yr) / Enterprise $299 ($249 yr). No free tier (14-day trial, no card). Integrations + webhooks gate at Startup; SSO + private projects + remove-branding gate at Business.

**2026-06-29**: No GitHub org found for FeedBear (api.github.com/orgs/feedbear → 404) — `github:` field intentionally omitted from frontmatter.
