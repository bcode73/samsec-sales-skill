---
name: sales-linkedhelper
description: "Linked Helper (Linked Helper 2) platform help — standalone desktop LinkedIn automation app (its own built-in browser, not a Chrome extension) for auto connect/message/InMail drip campaigns, profile scraping, email finder, a built-in CRM, native CRM sync, and outbound webhooks. Use when your LinkedIn account got restricted or banned after running Linked Helper, campaigns stop because the desktop app has to stay open, configuring auto-connect and follow-up message sequences or funnels, sending scraped profiles and messaging history to HubSpot/Salesforce/Pipedrive via webhook or native sync, getting duplicate contacts in your CRM, data credits or email-finder lookups running out, hitting the Standard plan's 20 advanced-actions-per-day cap, or running Linked Helper on a cloud VPS so your computer doesn't have to stay on. Do NOT use for choosing among LinkedIn automation tools or designing the sequence strategy and copy itself (use /sales-cadence)."
argument-hint: "[describe what you need help with in Linked Helper]"
license: MIT
version: 1.0.0
tags: [sales, outbound, platform]
---

# Linked Helper Platform Help

Linked Helper (a.k.a. Linked Helper 2) is a long-running desktop LinkedIn automation app — it runs in its own bundled browser on your machine (not a Chrome extension, not cloud), auto-executing connection requests, messages, InMail, endorsements, and profile scraping inside drip-style campaigns ("funnels"). It has a built-in mini-CRM, an email finder, native CRM connectors, and outbound webhooks. There is **no public inbound REST API** — automation is webhook-out + native integrations + Zapier/Make.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you need (skip if the prompt already says):

1. **What's the goal?** (a) account restricted/banned & recovery, (b) build/configure a campaign funnel, (c) push data to a CRM/webhook, (d) plan/credits/limits question, (e) run it without keeping my computer on, (f) something else.
2. **Which plan?** Trial / Standard ($15/mo) / Pro ($45/mo) — gates daily action volume and webhook count.
3. **How is it running?** Local desktop, or on a VPS / dedicated cloud machine?

## Step 2 — Route or answer directly

| If the user wants… | Route to |
|---|---|
| To design the *sequence strategy/copy* (timing, touches, A/B) | `/sales-cadence {question}` |
| General LinkedIn deliverability of the *email* channel found via email finder | `/sales-deliverability {question}` |
| To compare Linked Helper vs Waalaxy/Dripify/Expandi/HeyReach/PhantomBuster | `/sales-cadence {question}` (cross-platform selection) |

When routing, give the exact command: "This is a {domain} question — run: `/sales-cadence {user's original question}`".

Otherwise answer directly from Step 3.

## Step 3 — Linked Helper platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface, pricing/limits, data model, webhook recipes, and CRM-sync patterns. For the verbatim webhook field list and integration docs, read `references/linkedhelper-api-reference.md`.

Answer using only the relevant section — don't dump the whole guide.

## Step 4 — Actionable guidance

- **Restricted account?** Stop all automation immediately, reduce daily limits drastically, and re-warm over weeks. Restriction risk scales with daily action volume — the "safety features" reduce but never eliminate it.
- **Computer-on problem?** The desktop app only runs while open and online. The standard fix is to run it on a small always-on VPS / dedicated cloud machine with one proxy per LinkedIn account.
- **CRM duplicates?** Always include LinkedIn IDs in the webhook/sync field mapping so the CRM dedupes on a stable key.
- **Hitting caps?** Standard = 20 advanced actions/day + 20 webhook profiles/day; Pro = unlimited. One license drives exactly one LinkedIn account.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

- **Account-restriction risk is real and the #1 complaint.** Third-party tests cite ~23% restriction within 90 days for aggressive configs. Stay well under safe daily limits and ramp new accounts slowly; LinkedIn has been detecting Linked Helper more in recent cycles.
- **Desktop-only.** Campaigns pause when the computer sleeps, the app closes, or the internet drops. It is not cloud-hosted — keep it running or move it to a VPS.
- **LinkedIn-only.** No native email *sending* channel. The email finder discovers addresses, but you export them to a separate sending tool.
- **No inbound REST API.** Programmatic output is via outbound webhooks (Send person / Send replied / Send organization to webhook) and native CRM connectors, not an API you POST into.
- **One license = one LinkedIn account.** Multi-account = multiple licenses/seats (Workspace for teams).
- **Webhook profiles are metered on Standard** (20/day); messaging-history columns are configurable per action.

## Related skills

- `/sales-cadence` — Design the multi-channel outbound cadence (timing, touches, copy, A/B) that Linked Helper executes. Install: `npx skills add sales-skills/sales --skill sales-cadence -a claude-code`
- `/sales-deliverability` — Email deliverability for addresses found via the email finder. Install: `npx skills add sales-skills/sales --skill sales-deliverability -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Account got restricted
**User says**: "My LinkedIn account got restricted even though I followed Linked Helper's safe-limit recommendations. What now?"
**Skill does**: Explains restriction risk scales with volume regardless of safety toggles, gives an immediate stop-and-cool-down plan, lower daily limits, slow re-warm, and one-proxy-per-account hygiene; notes recent increased detection.

### Example 2 (developer/automation): Push replied leads to a CRM via webhook
**User says**: "How do I send everyone who replies in my campaign — with their email and message history — into HubSpot automatically?"
**Skill does**: Points to the "Send replied to Webhook" plug-in (or native HubSpot connector), shows the JSON field set (profile_url, email, first_name, last_name, last reply, messaging history), how to map LinkedIn IDs to avoid duplicates, and a Zapier/Make catch-hook → HubSpot recipe.

### Example 3: Run without keeping my laptop on
**User says**: "I have to leave my computer on all day for campaigns to run. Is there a better way?"
**Skill does**: Explains the desktop-only execution model, recommends a small always-on VPS / dedicated cloud machine with a single matching-geo proxy per account, and warns against running multiple LinkedIn accounts off one IP.

## Troubleshooting

### LinkedIn account restricted/banned
**Cause**: Daily action volume too high; LinkedIn detected automated patterns.
**Solution**: Halt automation, drop daily limits, randomize delays, run one proxy per account with geo-matching, and re-warm over 2-4 weeks. Accept that safety settings reduce — not eliminate — risk.

### Campaigns stop running
**Cause**: It's a desktop app — it only runs while open, awake, and online.
**Solution**: Disable sleep, keep the app foregrounded, or migrate to an always-on VPS/dedicated machine.

### Duplicate or missing contacts in the CRM
**Cause**: Sync keyed on name/email instead of a stable LinkedIn ID; or webhook profile cap hit on Standard.
**Solution**: Include LinkedIn IDs (member_id / profile_url) in the field mapping so the CRM dedupes; upgrade to Pro for unlimited webhook profiles if you're hitting the 20/day Standard cap.
