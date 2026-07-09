# Linked Helper Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-28**: Research baseline — platform docs, webhook field set, pricing, and integration surface captured from live sources on this date (homepage, pricing page, support.linkedhelper.com webhook articles, public webhook-column-headers Google Sheet, apitracker.io). Re-verify specifics against current docs before relying on them.

**2026-06-28**: Key facts to remember — (1) Linked Helper is a **desktop app with its own bundled browser**, not a Chrome extension and not cloud-hosted; campaigns only run while the app is open/awake/online (common fix: run on an always-on VPS). (2) There is **no public inbound REST API** — automation is outbound webhooks + native CRM connectors + Zapier/Make. (3) Webhooks are unsigned, with no delivery log or retry; dedupe on `member_id`. (4) Plan gates: Standard $15/mo = 20 advanced actions/day + 20 webhook profiles/day, 620 data credits; Pro $45/mo = unlimited + 3,100 credits; one license = one LinkedIn account. (5) #1 user pain is LinkedIn account restriction/ban — ~23% restriction within 90 days for aggressive configs per third-party testing; safety settings reduce but don't eliminate risk.

**2026-06-28**: Affiliate program exists — 30% recurring commission, $500 payout threshold (logged in _internal/affiliates.md).
