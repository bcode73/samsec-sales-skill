---
name: sales-userback
description: "Userback platform help — visual customer-feedback and bug-reporting: in-app widget with annotated screenshots, video, auto-captured console/network logs, and session replay, plus feature-request boards, public roadmap, surveys, and a Feature Portal. Developer surface: REST API (rest.userback.io/1.0, Bearer), webhooks, a ~12-tool MCP server (OAuth) for Claude/Cursor/ChatGPT, and JS/React/Vue/Next/mobile SDKs. Use when setting up the Userback widget, identifying logged-in users in feedback, syncing feedback to Jira/Linear/a CRM via API or webhooks, pulling feedback or session recordings programmatically, configuring the Userback MCP server, hitting API/webhook plan gates (Business Plus), or comparing Userback plan tiers. Do NOT use for choosing among feedback tools or NPS/CSAT survey methodology (use /sales-customer-feedback)."
argument-hint: "[describe what you need help with in Userback]"
license: MIT
version: 1.0.0
tags: [sales, customer-feedback, product, platform]
github: "https://github.com/userback"
---

# Userback Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Install / configure the **feedback widget** (annotated screenshots, video, console + network capture) and **identify** the logged-in user via the JS SDK
   - B) **Read** feedback/comments/projects/session recordings **out** via the REST API (`rest.userback.io/1.0`, `Authorization: Bearer`)
   - C) **Push** feedback in, or sync to **Jira / Linear / GitHub / Slack / a CRM** via native connectors, webhooks, or Zapier
   - D) Set up **webhooks** (feedback + comment events) or the **MCP server** for Claude/Cursor/ChatGPT
   - E) Use **feature-request boards + roadmap + Feature Portal**, **session replay**, or **surveys**
   - F) Pick a plan / hit a **plan gate** (API & webhooks are **Business Plus**; session replay + SDK = Business), or compare Userback vs Marker.io/BugHerd/Usersnap/Canny

2. **Which plan are you on?** This gates everything programmatic. **API + webhooks + mobile SDK require Business Plus**; session replay, surveys, and JS-SDK methods require Business; Zapier requires Team. Free retains feedback only 7 days.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Choosing a feedback/bug tool across the market, or VoC / NPS/CSAT/CES **survey-program** strategy | `/sales-customer-feedback {question}` |
| Aggregating **unsolicited** feedback across reviews/social/support | `/sales-noisely {question}` |
| Public review **generation** strategy (Trustpilot/G2) | `/sales-customer-reviews {question}` |
| In-app message / onboarding survey **strategy** across tools | `/sales-in-app-messaging {question}` |
| Connecting Userback to another tool generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a tool-selection question — run: `/sales-customer-feedback compare Userback vs Marker.io for visual bug reporting`".

## Step 3 — Userback platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (widget, session replay, surveys, boards/roadmap/Feature Portal, Workflows, Insights) tagged API-/webhook-/UI-only, pricing tiers + plan gates (Free/Team/Business/Business Plus), the data model (Feedback, Project, Workflow, Comment, SessionRecording with JSON shapes), and quick-start recipes (install + identify; paginated export; webhook listener; MCP triage).

**Read `references/userback-api-reference.md`** for the developer surface — base URL `https://rest.userback.io/1.0`, `authorization: Bearer <TOKEN>` (token from Workspace Settings → API Token), the endpoint inventory (Feedback, Comments, Screenshots, Members, Projects, Session Recordings, Workflows), page/limit pagination (max 50) + OData `filter`/`sort`, webhook payload shape, MCP setup, and a **Gaps** section (rate limits + webhook signature not documented).

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **The API is the top tier.** REST API **and** webhooks are **Business Plus only**; Zapier is Team+. If they're prototyping a CRM/warehouse sync on Free/Team/Business, the API won't be available — budget for Business Plus before building. This is the #1 surprise.
- **Identify users before they submit.** Anonymous feedback can't be tied to an account. Call `Userback.identify(id, {name,email,plan})` (and `setData({...})` for custom context) in the widget init — these SDK methods require Business.
- **It's a *visual* feedback tool first.** Userback's edge over board-only tools (Canny/Frill) is the auto-captured **console logs, network requests, device metadata, and session replay** that make a bug reproducible. Lead with that when the use case is bug reporting; if they only want feature voting, a cheaper board may fit.
- **Webhooks are unsigned.** No documented HMAC. Verify `User-Agent: Userback-Webhook`, keep the URL secret, dedupe on `data.id`, and re-fetch via `GET /feedback/{id}` rather than trusting the thin payload.
- **MCP for agent-driven triage.** `claude mcp add Userback https://mcp.userback.io/v1/mcp/ -t http -s user` (OAuth). ~12 tools — an agent can search/cluster feedback and read console/network logs without ID-copying.
- **Mind retention + paging.** Free purges feedback after **7 days**; list endpoints cap at **50/page**; handle `429` with backoff.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — modules/pricing/API captured from docs.userback.io, support.userback.io, and userback.io/pricing on this date. Re-verify plan gates, the API surface, and webhook details against current docs/in-account before relying on them.*

1. **REST API + webhooks are Business Plus.** The biggest integration footgun — they're gated to the top tier ($23–29/seat). Session replay, surveys, and JS-SDK methods are Business; Zapier is Team. Don't promise an API/webhook build on a lower plan.
2. **Webhooks have no documented signature.** Payloads are thin and unsigned (`User-Agent: Userback-Webhook` only). Treat them as untrusted: secret URL, dedupe on id, and re-read via the REST API for authoritative data.
3. **Free retention is 7 days.** Feedback older than a week is purged on Free Forever — fine for a trial, not for anything you need to keep. Upgrade (or export) before relying on history.
4. **Steep learning curve / feature sprawl.** A recurring review complaint is that Userback is "too complex for simple bug tracking" and onboarding/notification settings overwhelm new users. For a dead-simple board, a lighter tool may fit better — say so rather than overselling.
5. **List paging caps at 50.** `limit` max is 50 records/page; exact rate limits are unpublished. Paginate with `page`/`limit` and back off on `429`.
6. **Anonymous-by-default.** If you don't call `identify()` before submission, feedback isn't attributed to the user — a common "why are all my reports anonymous?" gotcha.
7. **Plan-gated capture, not just API.** Session replay capture and mobile SDK are gated (Business / Business Plus) — confirm the plan unlocks the *capture* feature, not just the API to read it.

## Related skills

- `/sales-customer-feedback` — Feedback/VoC strategy across tools — board-tool selection, survey-program design, metric choice (Userback is one visual-feedback option). Install: `npx skills add sales-skills/sales --skill sales-customer-feedback -a claude-code`
- `/sales-userjot` — AI-first feedback **board** with a REST API **+ MCP server** and no per-seat pricing — the contrast when you want feature voting + an agent loop without per-user billing (and don't need visual bug capture). Install: `npx skills add sales-skills/sales --skill sales-userjot -a claude-code`
- `/sales-frill` — Affordable standalone board with a documented REST API + **HMAC-SHA256-signed** webhooks — the pick when you need *signed* webhooks (Userback's are unsigned) and a board over visual bug reports. Install: `npx skills add sales-skills/sales --skill sales-frill -a claude-code`
- `/sales-sleekplan` — AI feedback suite (auto-categorization + MCP server) with a REST API + a free Indie tier — contrast for AI triage plus an API without Userback's Business-Plus gate. Install: `npx skills add sales-skills/sales --skill sales-sleekplan -a claude-code`
- `/sales-fourfour` — AI voice-of-customer copilot (OData API + MCP server) that mines existing calls/tickets rather than soliciting widget feedback — pair when you already have rich conversation data. Install: `npx skills add sales-skills/sales --skill sales-fourfour -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "Export all our Userback bugs into Snowflake nightly" (developer/automation)
**User says**: "I want a nightly job that pulls every bug report out of Userback into our warehouse with the screenshot and session-replay links."
**Skill does**: Confirms the **REST API requires Business Plus**, then gives the pattern: `GET https://rest.userback.io/1.0/feedback` with `authorization: Bearer <TOKEN>` (token from Workspace Settings → API Token), `filter=feedbackType eq 'Bug'`, `sort=modified,desc`, paginating with `page`/`limit=50` (the max) and backing off on `429`. Each Feedback object carries screenshots/session data; for replay URLs, join against `GET /sessionRecording`. Recommends storing `modified` as a high-water mark for incremental pulls. Points to the paginated Python recipe in `references/platform-guide.md`.
**Result**: A correct, plan-aware, incremental export pipeline.

### Example 2: "All our feedback comes in anonymous" (troubleshooting / SDK)
**User says**: "Feedback shows up but with no user — I can't tell who reported what."
**Skill does**: Explains Userback is anonymous unless you identify the user, and shows the fix: call `Userback.identify('<userId>', { name, email, plan })` (plus `Userback.setData({...})` for org/MRR context) in the widget init, before submission. Flags that `identify`/`setData` and session replay require **Business**. Notes you can also prefill fields, and that for backfilling attribution you'd update records via the API.
**Result**: Attributed feedback with the right SDK call and plan caveat.

### Example 3: "Is Userback the right tool, or should we use Marker.io / Canny?" (selection)
**User says**: "Small SaaS team. We want users to report bugs with screenshots and also vote on features. Userback vs Marker.io vs Canny?"
**Skill does**: Frames the axis: **Userback** = visual bug capture (annotated screenshots/video + console/network logs + session replay) **plus** feature boards/roadmap in one tool — but API/webhooks are Business Plus and webhooks are unsigned; **Marker.io** = deeper two-way issue-tracker (Jira) sync for QA/dev workflows; **Canny/Frill/UserJot** = stronger pure feature-voting boards (Frill has signed webhooks, UserJot has an MCP server + no per-seat). Recommends Userback when bug-reproduction context matters most and you want voting in the same tool; routes the broader comparison: "run: `/sales-customer-feedback compare visual bug tools vs feature-voting boards`".
**Result**: A capability-grounded pick with the right cross-skill routing.

## Troubleshooting

### The API returns 401 / I can't find where to build the integration
**Symptom**: API calls fail with 401, or there's no API option in the UI.
**Cause**: Two things — the **REST API is Business Plus only**, and the token must be created in **Workspace Settings → API Token → Create API Token**, then sent as `authorization: Bearer <TOKEN>`.
**Solution**: Confirm the workspace is on Business Plus (Team/Business have no API). Generate a token, send it in the `authorization` header (note: lowercase header, `Bearer ` prefix). Tokens are account-wide; use a separate token per account. If you only have Team, use **Zapier** instead, or upgrade.

### My webhook fires but I can't trust / verify the payload
**Symptom**: You receive webhook calls but there's no signature to validate, and the body is thin.
**Cause**: Userback webhooks (Business Plus) send `User-Agent: Userback-Webhook` and a payload of `action` / `type` / `data` / `timestamp` / `url` — **no documented HMAC signature**.
**Solution**: Keep the endpoint URL secret, verify the `User-Agent`, dedupe on `data.id` + `action` (ordering/delivery aren't guaranteed), and re-fetch the authoritative record via `GET /feedback/{id}` (or `/feedback/comment/{id}`) before acting. Use the built-in test feature under Connect → Webhooks to validate setup.

### Old feedback disappeared / reports lack reproduction detail
**Symptom**: Feedback older than a week is gone, or bug reports don't have enough to reproduce.
**Cause**: **Free Forever retains feedback only 7 days.** And session replay + full technical capture are plan-gated (session replay = Business).
**Solution**: Upgrade past Free (or export via API) to keep history. To get reproducible bugs, ensure you're on **Business+** for session replay, and rely on the auto-captured console logs / network requests / device metadata that ship with each report — surface those to your devs (or push them into the linked Jira/Linear issue).
