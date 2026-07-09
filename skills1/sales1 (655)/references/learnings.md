# Waalaxy Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-28**: Research baseline — platform docs, API surface, pricing, and integrations captured from live sources on this date. Re-verify specifics against current docs before relying on them.

- **API base is `https://developers.waalaxy.com`** even though the intro page also names `api.waalaxy.com`. All endpoint examples resolve against `developers.waalaxy.com`.
- **API is gated to Advanced (€49) and Business (€69).** The `Generate API key` button lives in **CRM Sync settings** and isn't present on Free/Pro.
- **`origin` is required** on `addProspectFromIntegration`; native values `make`/`zapier`/`n8n`, custom values appear prefixed `API-` in the UI.
- **Every prospect needs a LinkedIn `url`** — Waalaxy is LinkedIn-identity-centric; an email alone won't create a prospect.
- **`campaigns/getAll` only returns paused/running campaigns** — drafts/finished campaigns won't appear, so don't expect a full campaign inventory.
- **No documented reply webhook** in the public API — use native HubSpot/Pipedrive sync, Make/Zapier/n8n, or polling for reply handling.
- **No rate limit published** — the binding constraint is the monthly LinkedIn invite cap (Free 80 / Pro 300 / Advanced & Business 800) + the daily ramp, because it's a Chrome extension acting on the real LinkedIn session.
- **No GitHub org found** for Waalaxy (`api.github.com/orgs/waalaxy` → 404); `github:` field omitted from frontmatter.
- **Pricing changed in 2026**: Advanced email-finder credits jumped from 25 → 500/mo; some review sites quote older/higher USD prices ($59–179). Treat pricing as best-effort.
