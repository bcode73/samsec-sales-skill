---
name: sales-frederick
description: "Frederick AI (frederick.ai) platform help — an AI \"teammate\"/co-founder for startups that executes, not just advises: Coding Agents build and ship landing pages, apps, and APIs; Browser Agents automate web tasks; Background Agents run scheduled recurring work; Market Insights delivers AI market research, competitor tracking, customer signals, and social monitoring on a schedule. Credit-based (\"AI Credits\"): free tier (15 credits, 2 apps) → paid Plus/Pro plans; UI-only, no public API/webhooks/Zapier. Use when running market research or competitor tracking in Frederick, driving its coding/browser/background agents, understanding the credit tiers and free-plan gates, or asking whether it has an API. Its market research is not validated demand — Frederick can build the smoke-test landing page, but a generated report isn't proof anyone will pay. Do NOT use for the validate-before-building method or comparing idea validators (use /sales-idea-validation), or building the landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in Frederick AI]"
license: MIT
version: 1.0.0
tags: [sales, pre-launch, platform]
---

# Frederick AI Platform Help

Frederick AI (**frederick.ai**) is an **AI "teammate" / co-founder for startups** — a workspace of
autonomous agents that **execute** work rather than only advising. Its differentiator vs its idea-validation
siblings (aicofounder, SoloLaunch, Foundra) is that it doesn't stop at a report or a plan: **Coding Agents**
build and ship real software (landing pages, full-stack apps, APIs, internal tools), **Browser Agents**
drive websites (navigate, click, fill forms, extract data), **Background Agents** run recurring scheduled
tasks (SEO content, investor updates, data collection), and **Market Insights** delivers AI market research,
competitor tracking, customer signals, and social monitoring **on a schedule**. A shared **Editor/workspace**
persists plans, research, and files as context across sessions. Work is metered in **"AI Credits."**

The catch for founders: **Market Insights is AI-scanned research, not validated demand.** Frederick can even
*build the smoke-test landing page* (that part is genuinely useful) — but a generated market report is not
proof a stranger will pay. It has **no documented public API** (ironic for a tool that builds APIs for you).

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from Frederick?**
   - A) Run **Market Insights** — market research, competitor tracking, customer signals, social monitoring
   - B) Use the **agents** — Coding (build/ship an app or landing page), Browser (automate a web task), Background (schedule recurring work)
   - C) Understand **AI Credits** and the free-tier gates (what the 15-credit / 2-app free plan blocks)
   - D) Get more useful output (how to frame the idea/task and manage the shared workspace)
2. **What stage are you at?** A raw idea, or an existing project you want to research/build/automate?
3. **Is the real question "should I build this?"** If so, that's a `/sales-idea-validation` question — route in Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or comparing idea/startup-builder tools across the market | `/sales-idea-validation {question}` |
| Building the actual **landing page / smoke test** as a strategy (design, copy, conversion) | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand signal | `/sales-audience-growth {question}` |
| **Social listening / competitor monitoring** strategy across dedicated tools | `/sales-social-listening {question}` |
| **SEO / content-marketing** strategy (what the Background Agent's content work feeds into) | `/sales-content {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer Frederick-specific questions using Step 3.

## Step 3 — Frederick platform reference

**Read `references/platform-guide.md`** for the full reference — the four agent types and what each can/can't
do, the Market Insights research modules, the **AI-Credit** metering and free-vs-Plus-vs-Pro tier gates
(best-effort pricing), how to frame a task and use the shared workspace for better output, and the
no-public-API automation reality.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Separate what Frederick *builds* from what it *proves*.** Its agents genuinely ship things — a real
  landing page, a working app, a scheduled research digest. But **Market Insights is AI-scanned research, not
  validated demand**: competitor tracking and "customer signals" describe what's *discussed online*, not that
  a stranger will pay. If the real question is "should I build this?", keep Frederick's research to sharpen
  the pitch and route the go/no-go to `/sales-idea-validation` (a smoke test / pre-sale earns the decision).
- **Use the Coding Agent to build the smoke test, then measure real behavior.** Frederick's standout move for
  validation is that it can *build the fake-door / smoke-test landing page itself* — that's the one output
  that produces real signal. Have it ship the page, then drive a little traffic and read the conversion
  (`/sales-funnel` for the page strategy, `/sales-audience-growth` to capture signups). The built page is the
  proof; the market report isn't.
- **Model the pricing as credit-metered tiers and flag it as best-effort.** Every action spends **AI
  Credits**; name the tiers when cost comes up: a **free** tier (~15 credits, 1GB, **2 apps**, *limited*
  Market Insights, no recurring background agents) → **Plus** (~$25/mo, ~1,000 credits, 10GB, unlimited apps,
  full Market Insights, recurring background agents) → **Pro** (~$50/mo, ~2,500 credits, 30GB), annual ~24%
  off. Sources conflict (some third-party listings quote ~$8/$16 — likely stale/promo), so tell the user to
  **confirm live at frederick.ai/pricing**. Frame value as "how many credit-heavy agent runs per month" vs
  the monthly fee.
- **There's no public API — don't design an integration around it.** Despite building APIs *for* you,
  Frederick exposes **no documented public API, webhooks, MCP, or Zapier/Make**. If asked to automate/export,
  say so plainly: copy outputs from the workspace manually, or (for a validation pipeline) automate the
  *real* signal — landing-page analytics / waitlist events — not the generated research. Use the Background
  Agent for recurring work *inside* Frederick; it isn't an outbound integration surface.
- **Frame the task richly and lean on the shared workspace.** Agent output tracks input depth — give a
  specific customer, the exact problem, and the differentiation, and store plans/research/files in the Editor
  so agents carry context between runs. Treat every generated asset (page, plan, report) as an editable first
  draft, and re-run variants.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — Frederick's agent lineup, credit costs, and pricing move fast; verify at frederick.ai.*

- **Market Insights is research, not demand.** Competitor tracking and "customer signals" report what's
  discussed online; they don't prove anyone will pay. Pair with a real demand test (`/sales-idea-validation`).
- **Credits meter everything.** Agent runs (coding, browser, background, insights) all draw down **AI
  Credits**; the free tier's 15 credits and 2-app cap run out fast, and recurring background agents are gated
  to paid tiers. Watch the credit balance before scheduling recurring work.
- **No documented public API / webhooks / Zapier.** It's a UI workspace — don't plan an external integration
  around it. The Background Agent automates work *within* Frederick, not out to your stack.
- **Pricing sources conflict.** Homepage vs third-party listings disagree (e.g. ~$25/$50 vs ~$8/$16) — treat
  all figures as best-effort and confirm live at frederick.ai/pricing.
- **A shipped app isn't a validated app.** Frederick will happily build a full product for an idea nobody
  wants. Building is cheap now; the scarce thing is evidence of demand — get that first.
- **Output tracks input depth.** A thin, one-line task yields generic output; frame a specific customer +
  problem + differentiation and use the shared workspace for context.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator/builder landscape (use this to actually decide build-or-not; Frederick is one option among aicofounder, SoloLaunch, IdeaProof, Preuve, …)
- `/sales-aicofounder` — aicofounder — a close sibling AI co-founder with phased idea→launch workflow + grounded Reddit/X demand research
- `/sales-sololaunch` — SoloLaunch — a sibling AI startup builder that generates a "startup foundation" (names, logo, timeline, marketing strategy)
- `/sales-funnel` — Build the smoke-test / landing page the demand test runs on (Frederick's Coding Agent can ship it; this is the page strategy)
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture the real demand signal
- `/sales-social-listening` — Competitor / social monitoring strategy across dedicated tools (what Market Insights overlaps)
- `/sales-content` — SEO / content-marketing strategy (what Frederick's Background Agent content work feeds)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "Frederick's Market Insights says the market's great — am I validated?"
**User says**: "Frederick ran competitor tracking and market analysis on my idea and it looks promising. Good to build?"
**Skill does**: Separates Frederick's AI-scanned research from validated demand — competitor tracking and
"customer signals" describe what's *discussed online*, not that a stranger will pay. Keeps the research to
sharpen the pitch (competitors, positioning, risks) and routes the go/no-go to `/sales-idea-validation`: use
Frederick's Coding Agent to *build the smoke-test landing page*, then measure real conversions.
**Result**: The founder gets a decision from stranger behavior, using Frederick for the research and the page, not the verdict.

### Example 2: Have Frederick build and schedule the launch work
**User says**: "Can Frederick build my landing page and then keep researching my competitors every week?"
**Skill does**: Confirms the **Coding Agent** can ship the landing page and the **Background Agent** can run
recurring weekly Market Insights (competitor tracking) on a schedule — but flags that recurring background
agents are gated to paid tiers and that every run spends **AI Credits**, so watch the balance. Points the
page's conversion strategy to `/sales-funnel` and frames the weekly research as monitoring, not demand proof.
**Result**: A concrete plan — build once, schedule the research — with clear credit/tier expectations.

### Example 3: Can I automate Frederick via API? (developer/automation)
**User says**: "I want to trigger Frederick's agents and pull the research out from a script — what's the API?"
**Skill does**: States plainly there's **no documented public API, webhooks, MCP, or Zapier/Make** (ironic,
since Frederick *builds* APIs for you), so there's no supported way to trigger agents or export research
programmatically — copy outputs from the workspace manually, or automate the *real* signal (landing-page
analytics / waitlist events) instead. Notes the Background Agent handles recurring work *inside* Frederick,
not outbound integration.
**Result**: The user avoids building on a non-existent API and picks a workable path.

## Troubleshooting

### Ran out of credits / can't schedule recurring research
**Symptom**: Agents stopped, or a recurring Background Agent won't run.
**Cause**: Every agent run spends **AI Credits**; the free tier caps at ~15 credits and 2 apps, and recurring
background agents are gated to paid tiers.
**Solution**: Check the credit balance and tier — full Market Insights and recurring background agents need
Plus/Pro. Weigh how many credit-heavy runs you'll do per month against the monthly fee; confirm current
credits/limits at frederick.ai/pricing (treat figures as best-effort).

### Output feels generic / like plain ChatGPT
**Symptom**: The generated research, plan, or page could fit any product.
**Cause**: The task input was thin, and the agents lacked shared context.
**Solution**: Re-run with a rich brief — specific customer, exact problem, differentiation, current stage —
and store plans/research/files in the Editor workspace so agents carry context between runs. Compare variants.

### "Is there an API to automate this?"
**Symptom**: Looking for API docs, webhooks, or a Zapier connector.
**Cause**: Frederick is a UI workspace with **no documented public API/webhooks/Zapier**; the Background Agent
automates work *within* Frederick, not out to your stack.
**Solution**: Don't build an integration around it — copy outputs manually. For a validation pipeline,
automate the real demand signal (landing-page analytics, waitlist events) instead. See `/sales-idea-validation`.
