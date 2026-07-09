---
name: sales-userjot
description: "UserJot (userjot.com) platform help — AI-first customer-feedback suite (Canny/Productboard alternative, no per-seat pricing): feedback boards (posts + voting + comments, AI duplicate detection + auto-categorization), public roadmap, AI changelog, and an in-app widget. Developer surface: REST API (api.userjot.com/v1, Bearer token) for boards/posts/changelogs, webhooks, an MCP server (Claude Code/Cursor/Codex/ChatGPT/Windsurf) so AI agents triage feedback and publish changelogs, plus a Widget SDK (identify users) and a Swift SDK. Use when reading or syncing feedback posts/votes via the API, wiring the UserJot MCP server into Claude Code, reacting to a webhook, embedding the widget or identifying logged-in users, mapping post statuses to a roadmap, or picking a plan (free vs Starter vs Professional). Do NOT use for voice-of-customer / NPS survey program strategy across tools (use /sales-customer-feedback) or aggregating unsolicited feedback across reviews/social (use /sales-noisely)."
argument-hint: "[describe what you need help with in UserJot]"
license: MIT
version: 1.0.0
tags: [sales, customer-feedback, product, platform]
github: "https://github.com/UserJot"
---

# UserJot Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Read/sync feedback posts, votes, comments, or boards via the REST API (`api.userjot.com/v1`, Bearer token)
   - B) React to a webhook (new post / vote / status change) and push it into your app, CRM, or Slack
   - C) Wire the UserJot **MCP server** into Claude Code / Cursor so an agent can triage feedback and publish changelogs
   - D) Embed the **widget** / identify logged-in users (Widget SDK `identify`, or the Swift SDK on iOS)
   - E) Map post statuses to a public roadmap, publish an AI changelog, or organize boards
   - F) Decide UserJot vs Canny/Productboard/Sleekplan/Frill, or pick a plan (Free / Starter / Professional)

2. **API or no-code?** Code → REST API + webhooks + MCP. Front-end → Widget SDK (`identify`) / Swift SDK. AI-client → MCP server.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Voice-of-customer / NPS/CSAT/CES survey **program** strategy across tools | `/sales-customer-feedback {question}` |
| Aggregating **unsolicited** feedback across reviews/social/support | `/sales-noisely {question}` |
| Public review **generation** strategy (Trustpilot/G2) | `/sales-customer-reviews {question}` |
| Connecting UserJot to a CRM/PM tool generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-customer-feedback build a closed-loop feedback program`".

## Step 3 — UserJot platform reference

**Read `references/platform-guide.md`** for the full reference — the Boards/Posts/Roadmap/Changelog module map (what's API vs widget vs MCP vs UI), the AI layer (duplicate detection, auto-categorization, AI changelog), plan tiers + integration gating, the data model, and quick-start recipes (pull posts via the API; create a post idempotently; verify a webhook; configure the MCP server; embed + identify a user).

**Read `references/userjot-api-reference.md`** for the integration surface — **Bearer** token auth, base URL **`https://api.userjot.com/v1`**, the confirmed **Boards** CRUD endpoints + `BoardColor` enum, the **Posts** (`/requests`) and **Changelogs** (`/changelogs`) write endpoints with the optional **`Idempotency-Key`** header, the status-code map (`401`/`409` duplicate-or-quota/`422`/`429` + `Retry-After`), and a **Gaps** section noting which endpoint bodies are JS-rendered and must be confirmed in the live docs.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Bearer auth, one base URL.** `Authorization: Bearer <token>` against `https://api.userjot.com/v1`. Generate the token in your UserJot workspace settings and keep it server-side.
- **Idempotency where it counts.** Only **`POST /requests`** (create a feedback post) and **`POST /changelogs`** accept an optional **`Idempotency-Key`** header — send a stable UUID per logical create so retries don't double-post. Boards and other writes don't take it.
- **Handle 409 and 429 deliberately.** A **`409`** means a duplicate name **or a quota exceeded** (e.g. board limit on your plan) — don't blind-retry; inspect which. A **`429`** carries a **`Retry-After`** header — back off for that many seconds.
- **The MCP server is a first-class interface.** UserJot ships an MCP server with setup guides for Claude Code, Cursor, Codex, ChatGPT, and Windsurf, so an agent can triage feedback, update the roadmap, and publish changelogs. Confirm the exact endpoint/command in the live MCP docs (`userjot.com/docs` → MCP) — don't hard-code an unverified URL.
- **Identify users so feedback isn't anonymous.** Use the Widget SDK's `identify` (or the Swift SDK auth flow) to attach posts/votes to a real account; without it, widget activity is anonymous. SSO ("automatic login") is plan-gated.
- **It's a feedback-board tool, not a VoC survey suite.** UserJot collects *solicited* board feedback + roadmap + changelog. For survey *program* strategy use `/sales-customer-feedback`; for mining *unsolicited* feedback across reviews/social use `/sales-noisely`.
- **Watch the integration gate.** The free plan has unlimited posts/users but **no integrations** (which appears to include webhooks/API/MCP), Starter ($29) allows **1**, Professional ($59) unlimited — confirm in-account before building, and size the plan to how many integrations you need.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — Boards endpoints, base URL, auth, and status codes captured verbatim from userjot.com/docs/api; pricing/feature gating from userjot.com/pricing + third-party reviews. The full request/response bodies for non-Boards endpoints are JS-rendered — confirm in the live docs (and in-account) before relying on them.*

1. **The feedback-post resource is `/requests`, not `/posts`.** The product UI calls them "posts," but the create endpoint that accepts `Idempotency-Key` is **`POST /requests`** — don't assume `/posts`.
2. **`409` is overloaded.** It means a **duplicate name OR quota exceeded** (board limit, etc.). Branch on the cause; a duplicate is a no-op-ish conflict, a quota means you've hit a plan cap.
3. **API/webhooks/MCP may count against the "integrations" cap.** Free = no integrations, Starter = 1, Professional = unlimited. An integration built against a free workspace may be blocked — verify which surfaces the cap applies to in-account.
4. **Only `/requests` and `/changelogs` are idempotent.** Sending `Idempotency-Key` elsewhere is ignored; design retries accordingly (or guard duplicates yourself for boards/votes/comments).
5. **Full endpoint reference is JS-rendered.** `userjot.com/docs/api` lazy-loads sections beyond Boards; sub-paths like `/docs/api/requests` 404 in the migrated docs app. Confirm bodies/params in the live page — don't reconstruct from memory.
6. **Newer/indie tool.** UserJot launched in early 2025 and is built in public by a solo founder — feature depth and the published spec are evolving. Re-verify capabilities (especially multi-language, advanced prioritization, integration breadth) before committing.

## Related skills

- `/sales-customer-feedback` — Voice-of-customer / survey program strategy across tools (UserJot is a feedback-board option) — program design, metric choice, tool selection. Install: `npx skills add sales-skills/sales --skill sales-customer-feedback -a claude-code`
- `/sales-sleekplan` — The closest like-for-like **AI feedback board with an MCP server** (Canny/Frill alternative); compare on webhooks (Sleekplan verifies via secret GET-param, not HMAC) and AI-credit model. Install: `npx skills add sales-skills/sales --skill sales-sleekplan -a claude-code`
- `/sales-frill` — Affordable feedback-board competitor with **HMAC-SHA256-signed** webhooks + cursor pagination — useful contrast if signed-webhook verification matters. Install: `npx skills add sales-skills/sales --skill sales-frill -a claude-code`
- `/sales-featureos` — FeatureOS (formerly Hellonext) feedback boards + roadmap + changelog + knowledge base; REST API v3 (`API-KEY` header), OAuth 2.0 apps, auto-disabling webhooks. Install: `npx skills add sales-skills/sales --skill sales-featureos -a claude-code`
- `/sales-feedbear` — Budget feedback board with **no pull API** (webhooks/JWT SSO/Zapier only) — the contrast when API read access is the deciding factor. Install: `npx skills add sales-skills/sales --skill sales-feedbear -a claude-code`
- `/sales-noisely` — AI aggregation of **unsolicited** feedback across reviews/social/support (complement: UserJot = solicited boards, Noisely = unsolicited mining). Install: `npx skills add sales-skills/sales --skill sales-noisely -a claude-code`
- `/sales-integration` — Connecting UserJot to a CRM/PM tool via API/webhooks. Install: `npx skills add sales-skills/sales --skill sales-integration -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync feedback posts + votes into our system via the API (developer/automation)
**User says**: "How do I pull all our feedback posts and their vote counts out of UserJot?"
**Skill does**: Shows authenticating with **`Authorization: Bearer <token>`** against **`https://api.userjot.com/v1`**, listing **boards** (`GET /boards`) and then the feedback posts (the **`/requests`** resource — confirm the list path/params in the live docs since the page is JS-rendered), and reading each post's status/votes. Notes the token stays server-side, that pagination/exact bodies must be confirmed in-app, and that **webhooks** (new post / vote / status change) beat polling for ongoing sync.
**Result**: A correct, auth'd export plan with the JS-rendered-spec caveat and a webhook recommendation.

### Example 2: Wire the UserJot MCP server into Claude Code so an agent triages feedback (developer/automation)
**User says**: "Can I use UserJot from Claude so it reads, categorizes, and replies to feedback and drafts our changelog?"
**Skill does**: Points to UserJot's **MCP server** (setup guides for Claude Code / Cursor / Codex / ChatGPT / Windsurf at `userjot.com/docs` → MCP), explains it lets an agent triage feedback, update the roadmap, and publish changelogs, and tells the user to grab the exact endpoint/command from the live MCP docs rather than hard-coding an unverified URL. Flags that MCP may count against the plan's integration cap.
**Result**: A connected MCP server Claude can use, with the plan-gating caveat surfaced.

### Example 3: UserJot vs Canny vs Sleekplan — which feedback tool, and is the API on the free plan?
**User says**: "We're a small SaaS — UserJot, Canny, or Sleekplan for a feedback board + roadmap, and can I use the API on UserJot free?"
**Skill does**: Frames the tradeoff — **UserJot** is the AI-first, **no-per-seat** affordable pick (free tier with unlimited posts/users + AI duplicate detection + AI changelog + an MCP server), **Sleekplan** is similarly AI-forward with its own MCP server, and **Canny** is pricier/enterprise. Flags that on UserJot **free there are no integrations** (likely including API/webhooks/MCP) — those start on Starter ($29, 1 integration) / Professional ($59, unlimited), best-effort, confirm in-account — and routes broader selection: "run: `/sales-customer-feedback choose a product-feedback board tool`."
**Result**: A price-, AI-, and integration-grounded board-tool choice with the free-plan API caveat.

## Troubleshooting

### My `POST /requests` (or `POST /changelogs`) is creating duplicates on retry
**Symptom**: A network retry or re-run creates two identical feedback posts / changelog entries.
**Cause**: The create succeeded but the response was lost, so your client retried without idempotency.
**Solution**: Send a stable **`Idempotency-Key`** header (a UUID per logical create) on **`POST /requests`** and **`POST /changelogs`** — UserJot dedupes on it. Note this header is **only** honored on those two endpoints; for boards/votes/comments, guard duplicates yourself (e.g. check by name/board first).

### My API call returns `409` and I can't tell why
**Symptom**: A create (e.g. a board) fails with `409 Conflict`.
**Cause**: `409` is overloaded — it means **either a duplicate name OR a quota exceeded** (you've hit a plan limit such as the board cap: 2 on Free, 5 on Starter, unlimited on Professional).
**Solution**: Branch on the cause — if it's a duplicate name, reuse the existing object (`GET /boards` and match); if it's a quota, upgrade the plan or delete unused objects. Don't blind-retry; the retry will keep 409-ing.

### My integration works on a test workspace but is blocked / I can't generate a token on free
**Symptom**: Auth fails, or the API/webhooks/MCP aren't available on the free plan.
**Cause**: **Integrations are plan-gated** — Free has **no integrations**, Starter allows **1**, Professional unlimited; the API/webhooks/MCP surfaces appear to fall under that cap.
**Solution**: Upgrade to **Starter** ($29/mo) for one integration or **Professional** ($59/mo) for unlimited, then issue/use the token. Confirm in-account exactly which surfaces the cap counts, since the gating wording is best-effort. For survey-program strategy beyond boards, use `/sales-customer-feedback`.
