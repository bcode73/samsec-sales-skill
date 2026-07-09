# Juma Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each
invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-08**: Research baseline — platform docs, MCP server surface, pricing, and the credit model
captured from live sources (juma.ai, juma.ai/pricing, juma.ai/faq, juma.ai/mcp, github.com/team-gpt) on
this date. Re-verify specifics against current docs before relying on them.

**2026-07-08**: Juma is the rebrand of **Team-GPT**; the GitHub org is still `github.com/team-gpt` (repos:
streamdown, jackson SSO fork, etc. — **no API client/SDK/OpenAPI/MCP repo**). Third-party review coverage
(G2/Capterra/AppSumo) is filed under both "Juma" and "Team-GPT."

**2026-07-08**: The **only** programmatic surface is the **MCP server** (`https://mcp.juma.ai/mcp`, HTTP
transport, OAuth, no API keys, 40+ tools). No documented REST API, no webhooks, no Zapier/Make. This is the
key differentiator vs the rest of the persona/idea-validation cluster (all UI-only).

**2026-07-08**: Credit model is the top complaint area (legacy Team-GPT AppSumo buyers bought "seats," Juma
is credit-metered). Defusing facts: **only successful runs charge**, credits **roll over** on Pro, and over
MCP **reading knowledge/brand is free** (only agent sessions burn credits). Features are NOT gated by tier —
Free has full access; tiers differ only by credit allowance + enterprise controls.

**2026-07-08**: Three actions stay UI-only even over MCP: **uploading files as knowledge, editing existing
images, workspace administration**. MCP tasks have a ~30s wait window; longer tasks run in the background
with agent check-ins.
