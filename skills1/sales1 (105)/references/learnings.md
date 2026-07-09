# Clearcue Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->
**2026-05-10**: Research baseline (from git history) — platform docs were captured on/around this date and the API surface, pricing, and webhooks have NOT been re-verified against live docs since. Re-verify specifics before relying on them.
**2026-06-13**: API re-verified against live official docs — webhooks are now on ALL plans (not Pro+), MCP is publicly self-serve and included on all plans since Feb 12 2026 (was "on request/contact support") with two auth paths (remote MCP URL via Custom Connectors/OAuth, or personal access token added Apr 30 2026); pricing unchanged (Starter €99/€79, Pro €249/€199, Scale €549/€439; CRM still Scale+, Company AI qualification still Pro+); no public REST API still confirmed. Sources: https://clearcue.ai/pricing, https://clearcue.ai/changelog, https://clearcue.ai/blog/how-to-build-gtm-automation-stack-mcp-claude, https://clearcue.ai/blog/clearcue-faq-intent-signals-pricing-features.
