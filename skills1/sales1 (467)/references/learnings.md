# Redreach Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->
**2026-05-10**: Research baseline (from git history) — platform docs were captured on/around this date and the API surface, pricing, and webhooks have NOT been re-verified against live docs since. Re-verify specifics before relying on them.
**2026-06-13**: API re-verified against live official docs — no API/MCP added (still no public REST API; alerts remain push-only via Slack/Telegram/email/webhooks). Drift fixed: first paid tier is officially "Startup" not "Starter" (tiers Startup/Growth/Professional = 1/2/3 seats); 48-hour money-back guarantee unchanged; 3-day pass grants Pro access except daily mention tracking. Added missing capabilities surfaced by current docs: Outbound built-in CRM (track DM conversations, organize by campaign, response rates), spintax DM personalization, and 100,000+ subreddits scanned daily. Exact Growth/Professional monthly prices remain JS-rendered/behind signup (unverified). Sources: https://redreach.ai/, https://redreach.ai/feature/lead-generation-with-reddit, https://redship.io/reddit-tool/redreach, https://www.revavenues.ai/tools/redreach-ai.
