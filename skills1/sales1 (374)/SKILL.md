---
name: sales-noisely
description: "Noisely (noise.ly) platform help — AI feedback-tracking & product-intelligence tool that aggregates customer feedback from 23+ sources (reviews, app stores, Reddit/HN/GitHub, Zendesk/Intercom, CSV), auto-categorizes into 12 types, scores sentiment + urgency/impact, clusters similar mentions into ranked 'action items', and spike-detects. Pushes to 10 channels (Slack, Linear, Jira, Notion, Google Sheets, Email, Webhooks…). No public REST API documented — the developer surface is outbound webhooks + native integrations + CSV; AI analyses are a monthly credit limit. Use when wiring action-items or spike alerts to your tools via webhook, choosing which sources to monitor, clustering/deduping feedback, reading sentiment or urgency, exporting to a sheet/ticket, or picking Try vs Pro vs Custom. Do NOT use for survey/VoC program strategy across tools (use /sales-customer-feedback), public review collection (use /sales-customer-reviews), or broad brand/social listening (use /sales-social-listening)."
argument-hint: "[describe what you need help with in Noisely]"
license: MIT
version: 1.0.0
tags: [sales, customer-feedback, voice-of-customer, platform]
---

# Noisely Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Push action items / spike alerts to your tools (Slack, Linear, Jira, webhook…)
   - B) Pick which of the 23+ sources to monitor (reviews, social/dev communities, support)
   - C) Understand the AI output — categories, sentiment, urgency/impact, clustered action items
   - D) Export feedback to a sheet/BI, or import your own via CSV
   - E) Tune signal — brand-ambiguity filters, dedupe, spike thresholds
   - F) Decide Try ($29 one-time) vs Pro ($49/mo) vs Custom, or budget the analysis credits

2. **Code or no-code?** Custom routing → outbound **webhook**. Otherwise use the native channels (Linear/Jira/Slack/Sheets) — no endpoint to host.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Survey / VoC **program** strategy (NPS/CSAT/CES design) across tools | `/sales-customer-feedback {question}` |
| Collecting **public reviews** (Trustpilot/G2 generation) strategy | `/sales-customer-reviews {question}` |
| Broad **brand/social listening** across tools | `/sales-social-listening {question}` |
| Wiring Noisely into a CRM/ticketer generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-customer-feedback design a closed-loop VoC program`".

## Step 3 — Noisely platform reference

**Read `references/platform-guide.md`** for the full reference — the source/analysis/output model (what's UI-config vs webhook vs CSV), the credit-based pricing, the action-item data model, and quick-start recipes (route action items to Linear/webhook; export to Sheets; tune brand-ambiguity filters).

**Read `references/noisely-api-reference.md`** for the integration surface — **no public REST API is documented**; the surface is **incoming sources** (23+, UI-config), the **AI pipeline** (12 categories → sentiment → urgency/impact → clustered **action items** → spike detection), **10 outbound channels** including **webhooks** (payload schema not published — capture a live delivery), and **CSV** import/export.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **The unit of automation is the "action item," not the mention.** Noisely clusters/dedupes similar feedback across sources into ranked action items. Wire downstream logic (tickets, alerts) to the **action-item id**, not raw mentions.
- **No public REST API — use webhooks + native channels.** To create tickets, push action items to **Linear/Jira/Asana**; for chat alerts use **Slack/Teams/Discord**; for custom routing use the **webhook**. The webhook payload schema isn't published — capture a test delivery (webhook.site) and pin your mapping to it.
- **Watch the analysis credits.** "AI analyses" are a **monthly credit limit** (≈2,000/mo on Pro). High-volume sources (Reddit/app stores) can burn credits — scope sources and use brand-ambiguity filters to cut noise.
- **Brand-ambiguity filters matter for noisy names.** If your brand name is also a common word, the filters reduce off-topic mentions — invest in them early or your action items will be polluted.
- **CSV is the reliable structured export.** Absent an API, export the dashboard to CSV for BI, or import your own support data as a source.
- **Right-size the plan.** **Try** ($29 one-time, ≤500 mentions) to validate, **Pro** ($49/mo, 23+ sources, 10 channels, unlimited seats) for ongoing, **Custom** for higher limits/SLA. Pricing best-effort — verify.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — features/pricing verified against the marketing + comparison pages; no public API docs exist, so the developer surface is inferred from documented channels. Confirm in-account.*

1. **No public REST API.** The docs/webhooks path 404s; automation is outbound **webhooks** + native integrations + CSV. Don't assume an `api.noise.ly` exists — confirm with Noisely (Custom plan mentions custom integrations).
2. **Webhook payload isn't documented.** Event names and fields are unpublished — capture a live delivery before coding, and there's no documented HMAC (secret URL + dedupe on action-item id).
3. **Credits are the real limit.** AI analyses are capped monthly (~2,000 on Pro); noisy sources eat them fast — scope sources, not just plans.
4. **Brand ambiguity pollutes results.** Common-word brand names pull off-topic mentions until you train the ambiguity filters.
5. **It's aggregation, not surveys.** Noisely mines existing feedback (reviews/social/support) — it does **not** run NPS/CSAT survey programs. For survey strategy use `/sales-customer-feedback`.
6. **Overlaps social listening & reviews.** It ingests Reddit/HN and Trustpilot/G2 — but it's framed for *product feedback intelligence*, not broad PR monitoring or review *generation*. Route those to `/sales-social-listening` / `/sales-customer-reviews`.
7. **Source coverage shifts.** The 23+ source list changes; verify a specific source (e.g. a niche forum) is supported before relying on it.

## Related skills

- `/sales-customer-feedback` — Voice-of-customer / survey program strategy across tools (Noisely is the aggregation/intelligence option vs survey tools) — program design, tool selection
- `/sales-customer-reviews` — Public review collection/generation strategy (Noisely *reads* reviews; this is about getting more)
- `/sales-social-listening` — Brand/social monitoring across tools (Noisely overlaps on Reddit/HN/social but is product-feedback-framed)
- `/sales-integration` — Wiring Noisely action items into a CRM/ticketer via webhooks/native channels
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Route high-urgency action items into Linear via webhook (developer/automation)
**User says**: "When Noisely flags an urgent bug cluster, I want it to open a Linear issue automatically."
**Skill does**: Recommends the **native Linear integration** first (turn an action item into an issue, no code). If custom logic is needed (e.g. only `urgency=high` + specific category), use the **webhook** outbound channel → your handler → Linear API. Warns the **payload schema isn't documented** (capture a live delivery, key on the **action-item id**), there's **no HMAC** (secret URL + dedupe), and that high-volume sources burn **analysis credits**.
**Result**: Urgent clusters become Linear issues without manual triage.

### Example 2: Which sources should I turn on, and will I blow my credits?
**User says**: "I sell a mobile app. What should I monitor in Noisely without wasting analyses?"
**Skill does**: Suggests high-signal sources for an app (App Store, Play Store, Reddit, support via Zendesk/Intercom, G2/Trustpilot) and warns that broad sources (Reddit/Google News) can burn the **~2,000/mo Pro credit** fast. Recommends tuning **brand-ambiguity filters** and starting on **Try ($29)** to validate volume before committing. Routes survey-based VoC to `/sales-customer-feedback`.
**Result**: A focused source set that fits the credit budget.

### Example 3: Noisely vs a survey tool — which do I need?
**User says**: "Is Noisely a replacement for our NPS surveys?"
**Skill does**: Clarifies Noisely **aggregates existing feedback** (reviews, social, support) into AI action items — it's **not** a survey platform and won't run NPS/CSAT. They're complementary: surveys = solicited/structured, Noisely = unsolicited/at-scale. Routes program design: "run: `/sales-customer-feedback design an NPS + VoC program`," and notes Noisely's edge is affordable cross-source mining ($49/mo vs enterprise tools).
**Result**: User understands the categories and picks the right mix.

## Troubleshooting

### My action items are full of off-topic mentions
**Symptom**: Clusters include posts that aren't about your product.
**Cause**: Your brand name is ambiguous (also a common word/another brand), so the source crawlers pull unrelated mentions.
**Solution**: Train the **brand-ambiguity filters** (Noisely learns to exclude off-topic mentions), narrow the source set, and remove the noisiest sources. Re-run analysis after tuning. This also conserves **AI analysis credits**, which off-topic mentions waste.

### I want to pull Noisely data into our data warehouse / app but can't find an API
**Symptom**: Looking for a REST endpoint to read action items/mentions.
**Cause**: Noisely doesn't publish a public REST API.
**Solution**: Use the **webhook** outbound channel to stream action items to your endpoint (capture the payload shape from a live delivery; key on the action-item id), the **Google Sheets** channel for BI, or **CSV export** from the dashboard for batch. For higher-volume/custom needs, ask Noisely about Custom-plan custom integrations. For generic iPaaS wiring, use `/sales-integration`.

### I burned through my monthly analyses
**Symptom**: AI analyses hit the cap before month-end.
**Cause**: Credits (~2,000/mo on Pro) are consumed per analyzed mention; high-volume sources exhaust them.
**Solution**: Reduce/disable the noisiest sources, tighten brand-ambiguity filters to drop off-topic mentions before analysis, and consider the **Custom** plan for higher limits. Prioritize sources where your buyers actually post.
