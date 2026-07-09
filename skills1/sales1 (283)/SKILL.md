---
name: sales-lagrowthmachine
description: "La Growth Machine (lagrowthmachine.com) platform help — multichannel B2B outbound automation across LinkedIn, email, and X: sequenced campaigns (conditions, branches, A-B), per-identity safety limits, waterfall lead enrichment, lookalike + LinkedIn intent signals, a shared inbox, AI copy + AI voice, and outcome tracking. Developer surface: REST API (apiv2.lagrowthmachine.com/flow, apikey query param) to enroll leads into audiences (POST /flow/leads), list campaigns/audiences/identities, and create inbox webhooks for real-time reply events; native HubSpot/Clay/Make/Slack, Zapier/n8n, and an MCP server — API/webhooks gated to the Ultimate plan. Use when enrolling leads via the API, wiring inbox webhooks (create a CRM contact on reply), managing identities/safety limits, building a multichannel sequence, or choosing LGM vs lemlist. Do NOT use for outbound cadence strategy across tools (use /sales-cadence), email deliverability/warmup (use /sales-deliverability), or generic iPaaS wiring (use /sales-integration)."
argument-hint: "[describe what you need help with in La Growth Machine]"
license: MIT
version: 1.0.1
tags: [sales, outbound, cadence, platform]
github: "https://github.com/lagrowthmachine"
---

# La Growth Machine Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Enroll leads into an audience/campaign via the API (`POST /flow/leads`)
   - B) Wire an inbox webhook (e.g. create a CRM contact when a lead replies)
   - C) Manage identities + per-account safety limits (LinkedIn safety)
   - D) Build/optimize a multichannel sequence (LinkedIn + email + X, conditions, A/B)
   - E) Use enrichment / lookalike / intent signals to fill audiences
   - F) Sync campaign/lead data out, or decide LGM vs lemlist/Waalaxy

2. **API or no-code?** Code → REST API (`apikey`) + inbox webhooks. No endpoint → native HubSpot/Clay/Make/Slack, Zapier, or n8n.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Outbound **sequence/cadence strategy** across tools (channels, timing, copy) | `/sales-cadence {question}` |
| Email **deliverability / warmup** for the email channel | `/sales-deliverability {question}` |
| Generic iPaaS wiring to a CRM/other app | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-cadence design a LinkedIn + email multichannel sequence`".

## Step 3 — La Growth Machine platform reference

**Read `references/platform-guide.md`** for the full reference — the identity/audience/campaign/lead model (what's API vs UI), the per-identity safety model, plan tiers (API/webhooks on Ultimate), enrichment/signals, and quick-start recipes (enroll a lead; create an inbox webhook; list campaigns).

**Read `references/lagrowthmachine-api-reference.md`** for the integration surface — base `https://apiv2.lagrowthmachine.com/flow`, **`apikey` query-param** auth, the operations (`POST /flow/leads` to enroll into an audience, Get Campaigns, List Audiences, List Identities, Create/List Inbox Webhooks), the real-time inbox webhook (lead-reply events), native integrations, and the emerging MCP server.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **The write path is enroll-into-audience.** `POST /flow/leads?apikey=…` adds a lead to an **audience**; a **campaign** running over that audience then works the lead across channels. You don't "send a message" via API — you enroll, and the sequence executes.
- **Identities carry the safety limits.** Outreach runs through connected **identities** (LinkedIn/email accounts), each with per-day caps. List/monitor them (`List Identities`); spreading volume across identities (and not exceeding limits) is how you stay safe — LGM is cloud-based with dedicated proxies.
- **Inbox webhooks are the real-time hook.** Create an **inbox webhook** to fire when a lead replies (the canonical "create a CRM contact on reply" flow). Treat the URL as secret, dedupe on the lead/message id.
- **API + webhooks need Ultimate.** They're gated to the **Ultimate** tier (~€150/mo/identity, best-effort) — Basic/Pro may not expose them. Confirm before building.
- **Enrichment/signals fill audiences.** Waterfall enrichment (verified contacts), lookalike, and LinkedIn **intent signals** auto-import ICP-matching leads — use them to keep audiences fresh rather than manual imports.
- **Don't confuse channel deliverability with the tool.** LGM orchestrates; the *email* channel still needs warmup/deliverability hygiene — route that to `/sales-deliverability`.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — API/pricing from official docs + integration listings; the Postman collection is JS-rendered so confirm exact JSON in-account.*

1. **API key is a query param.** `?apikey=…` (from Settings → API), not a header — keep it server-side (logs/referrers leak query strings).
2. **API/webhooks are Ultimate-only.** Webhooks + advanced integrations are gated to the **Ultimate** plan; Basic/Pro can't use them. Verify your tier first.
3. **You enroll, you don't send.** The API adds leads to an **audience**; the **campaign sequence** does the sending. There's no "send LinkedIn message" endpoint — model your flow around enroll + sequence.
4. **Identities have safety limits.** Per-account LinkedIn/email caps exist for safety — exceeding them risks the account. Spread across identities; monitor via `List Identities`.
5. **Webhook signing is undocumented publicly.** Treat the inbox-webhook URL as a secret, dedupe on lead/message id, and confirm any signature scheme in the Postman collection.
6. **Endpoint detail lives in Postman.** Full per-endpoint JSON/params/rate-limits aren't published outside the (JS-rendered) Postman collection — pull them from there or the help center.
7. **It's LinkedIn-first.** LGM's edge is cloud LinkedIn safety + multichannel orchestration; email-first teams may prefer lemlist — compare via `/sales-cadence`.

## Related skills

- `/sales-cadence` — Outbound & LinkedIn/multichannel sequence/cadence strategy across tools (LGM is one of the multichannel platforms covered) — channel mix, timing, copy, tool selection vs lemlist/Waalaxy/Apollo
- `/sales-deliverability` — Email warmup + inbox placement for LGM's email channel
- `/sales-integration` — Wiring LGM into a CRM via the API / inbox webhooks / Zapier / n8n
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Enroll leads into a campaign via the API (developer/automation)
**User says**: "When a lead is created in my app, how do I push it into a La Growth Machine campaign automatically?"
**Skill does**: Walks Recipe 1 — `POST https://apiv2.lagrowthmachine.com/flow/leads?apikey=YOUR_KEY` with the lead fields + the target **audience id** (get audiences via **List Audiences**); the **campaign** running over that audience then works the lead across LinkedIn/email/X. Stresses that you **enroll into an audience** (there's no send-message endpoint), keeping the `apikey` server-side, and that the API needs the **Ultimate** plan.
**Result**: New app leads flow straight into the right multichannel sequence.

### Example 2: Create a CRM contact when a lead replies (inbox webhook)
**User says**: "I want a HubSpot contact created the moment someone replies in La Growth Machine."
**Skill does**: Recommends the native **HubSpot** integration if it covers it, else the **Create Inbox Webhook** operation pointing at your endpoint — LGM POSTs the reply event (lead + message); your handler creates the HubSpot contact. Notes treating the URL as secret, deduping on the lead/message id, and that inbox webhooks are **Ultimate-tier**. Offers Zapier/n8n as a no-code path.
**Result**: Replies become CRM contacts in real time.

### Example 3: LGM vs lemlist — which multichannel tool?
**User says**: "Should I use La Growth Machine or lemlist for outbound?"
**Skill does**: Frames the split — **LGM is LinkedIn-first** (cloud-based LinkedIn safety since 2017, dedicated proxies, multichannel orchestration, shared inbox), while **lemlist is email-first** (built-in lead DB, lemwarm warmup, deep email personalization). Recommends LGM when LinkedIn + multichannel is the core, and routes the broader decision: "run: `/sales-cadence choose a multichannel outbound tool for a LinkedIn-led motion`." Notes pricing is per-identity (Basic €50 → Ultimate €150 with API/webhooks).
**Result**: A grounded tool choice based on channel emphasis.

## Troubleshooting

### My API calls are unauthorized / 401
**Symptom**: Requests to `apiv2.lagrowthmachine.com/flow/...` are rejected.
**Cause**: Missing/invalid **`apikey`** query param, or the API isn't enabled on your plan.
**Solution**: Append `?apikey=YOUR_API_KEY` (from app.lagrowthmachine.com/settings/api) to every request — it's a **query parameter**, not a header. Confirm you're on the **Ultimate** plan (API/webhooks are gated there). Test with a read op like **List Identities** first.

### Leads don't get worked after I add them
**Symptom**: `POST /flow/leads` succeeds but no outreach happens.
**Cause**: The lead was added to an **audience** that no active **campaign** is running over, the assigned **identity** is paused/over its safety limit, or required channel data (LinkedIn URL/email) is missing.
**Solution**: Enroll into an audience that a **launched campaign** targets, verify the **identity** is connected and under its daily limit (`List Identities`), and ensure the lead has the channel fields the sequence needs. Enrichment can fill missing contact data.

### My LinkedIn account got restricted
**Symptom**: LinkedIn flags/restricts an identity used by LGM.
**Cause**: Exceeding safe per-day action limits (connections/messages) or aggressive sequences.
**Solution**: Respect the per-identity **safety limits** (LGM sets them from years of data — don't override upward), warm up new identities slowly, spread volume across identities, and keep sequences human-paced. For channel-mix/volume strategy, use `/sales-cadence`; for the email side, `/sales-deliverability`.
