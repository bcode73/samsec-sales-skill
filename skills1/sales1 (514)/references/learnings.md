# Sembly Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-13**: API re-verified against live official docs — pricing/plans unchanged (Basic $17/$10, Pro $29/$20, MAX $39/$30; Pro up to 40 users, MAX 3-500; AI docs/insights 5 Pro / 40 MAX per user; HIPAA/SSO/audit MAX+), 48 languages and 10 CRM connectors confirmed. Drift fixed: media upload is per-user-hours not unlimited (Basic 5h / Pro 10h / MAX 15h per user). n8n has NO dedicated Sembly node (corrected from "official Sembly AI node") — n8n connects via the Sembly MCP server or generic HTTP/Webhook nodes. NEW: Sembly MCP is now a hosted, token-based, read-only MCP server (Pro+) that is disabled by default until a workspace admin enables it, supporting Claude/Cursor/n8n; this gives programmatic read access despite no public REST API. NEW automation filter: by meeting owner; Test button simulates the POST. Sources: https://www.sembly.ai/pricing/, https://www.sembly.ai/automations/, https://www.sembly.ai/automations/custom/, https://www.sembly.ai/why-choose-sembly/, https://n8n.io/integrations/webhook/and/sembly-ai/, https://helpdesk.sembly.ai/hc/en-us/articles/43974465872785-Activate-Sembly-MCP.
