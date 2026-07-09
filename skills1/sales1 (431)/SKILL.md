---
name: sales-preuve
description: "Preuve AI (preuve.ai) platform help — an AI startup-idea validator that scans 50+ live sources (Crunchbase, Google Trends, Reddit, Product Hunt, G2) to produce a viability score, a source-linked competitor map, TAM/SAM/SOM sizing, and blind-spot analysis, with every claim cited to its origin. Ten agents run in parallel and a cross-validator fact-checks findings; a Radar tier re-scans an idea for market and competitor changes over time. Built on Claude, UI-only, no public API. Use when running an idea through Preuve's free Reality Check or paid Founder Report, interpreting its viability score and source-linked claims, comparing it against fast-score validators like IdeaProof or Validator AI, understanding its one-time-report vs Radar-subscription vs lifetime pricing, or asking whether it has an API or webhooks to export a report. Do NOT use for the validate-before-building method or ranking validators to pick one (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in Preuve AI]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
---

# Preuve AI Platform Help

Preuve AI (preuve.ai) is an **AI startup-idea validator built around cited, live evidence**. Instead of
one model's opinion, it runs **10 agents in parallel** (market analyst, competitor scout, community
researcher, financial analyst, real-time news scanner) plus a **cross-validator** that fact-checks every
claim, searching **50+ live sources** (Crunchbase, Google Trends, G2, Capterra, Product Hunt, Reddit,
Quora, Hacker News, X, SEC filings, LinkedIn, Trustpilot, Indie Hackers, Statista). The output is a
**viability score**, a **competitor map** (up to 15 with funding/pricing), **TAM/SAM/SOM** sizing,
**founder-market fit**, **blind spots**, and **3 pivot suggestions** — with **every key claim linked to
its source**. Scores run **conservative** (median ~55 across thousands of ideas), and it's built on
**Claude**. A **free Reality Check** (60s) previews the score + 2 competitors + a verdict; the **Founder
Report** (paid, one-time) runs the full 50+-source analysis; a **Radar** subscription re-scans an idea for
market/competitor changes over time. It is a **UI tool — no public API, webhooks, or Zapier.**

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from Preuve AI?**
   - A) Run an idea and interpret the viability score, source-linked claims, competitor map, or pivots
   - B) Understand the tiers — free Reality Check vs paid Founder Report vs Investor Package vs Radar
   - C) Set up or interpret **Radar** monitoring (re-scans, competitor threat flags, score tracking)
   - D) Export or automate the report (API / integration reality)
2. **What's the real question — "is this idea worth building?" or "how do I use this tool?"** If it's the
   go/no-go decision itself, that's `/sales-idea-validation` (a validator's output is a gut check, not
   demand) — route in Step 2.

Skip-ahead: if the user wants the validate-before-building *method* or to compare validators across the
whole market to pick one, that's a `/sales-idea-validation` question — route immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| A full **cross-market ranking** of validators (IdeaProof, Validator AI, DimeADozen, WorthBuild… to pick one) — but answer a quick Preuve-vs-X *how-they-differ* inline first (Step 4) | `/sales-idea-validation {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer Preuve-specific questions using Step 3.

## Step 3 — Preuve AI platform reference

**Read `references/platform-guide.md`** for the full reference — the 10-agent/50+-source architecture,
what the free Reality Check includes vs the paid Founder Report and Investor Package, how the source-linked
claims and conservative viability score work, the Radar monitoring tiers, the three-axis pricing (one-time
reports vs Radar subscription vs lifetime), the shareable-dashboard link, and the no-public-API automation
reality.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Treat a source-linked claim as evidence the problem is *discussed*, not that anyone will *pay*.** Preuve's
  differentiator is that every finding is cited to a live source (a Reddit thread, a G2 review, a funding
  record) — that makes the competitor list, risks, and market context far more trustworthy than a pure-LLM
  guess. But a citation proves people *talk about* the problem, not that strangers will buy. Tell the user
  to **keep the cited structured outputs (competitors, pricing, risks, blind spots) to sharpen the pitch**,
  and put the go/no-go on a **real demand test** (smoke test / pre-sale) — route the decision to
  `/sales-idea-validation` and the build to `/sales-funnel`.
- **Read the score as deliberately conservative — but still an AI opinion.** Preuve's viability score runs
  **low by design** (median ~55) compared with fast-score validators that inflate (IdeaProof ~78). Tell the
  user a middling Preuve score is not a death sentence and a high one is not proof of demand — the number is
  a directional gut check that can still be wrong; the citations are the useful part.
- **When asked how it compares to a fast-score validator, give the model-level contrast inline, then offer the route.**
  If the user asks Preuve vs IdeaProof / Validator AI / DimeADozen, answer *how they differ* directly:
  Preuve **cites every claim to 50+ live sources and scores conservatively**, whereas IdeaProof **scores in
  ~120s and bundles a broad pre-launch kit** (brand/logo/deck/ads), and DimeADozen is a **one-time
  citation-backed report you buy and keep**. Tell the user to pick by **evidence rigor vs speed/breadth**,
  then offer `/sales-idea-validation` for a full validator-market ranking. Don't just route the question away.
- **Explain the three pricing axes and present them as best-effort.** Preuve mixes **one-time reports** (free
  Reality Check → paid Founder Report → discounted report packs → an Investor-Ready Package), a **Radar
  monthly subscription** (re-scans/monitoring), and **lifetime** plans. A one-time report is **not** a
  subscription; Radar **is**. Prices move (report-pack prices in particular vary between pages), so present
  any figure as best-effort and point the user to **preuve.ai/pricing** to confirm.
- **Frame Radar as competitor/market monitoring, not demand tracking.** Radar re-scans an idea on a schedule
  and flags competitor moves, funding, and score changes over time — genuinely useful for watching a space
  after you've committed. But it monitors **published signals**, not your customers; it is not a substitute
  for measuring whether real users convert. Say so when a user leans on Radar as validation.
- **There's no public API — don't plan an integration around it.** If asked to export or automate, say
  plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP server** — it's a UI tool.
  The only shareable/programmatic-ish surface is the **shareable dashboard link** (`preuve.ai/share/{slug}`);
  otherwise copy/save the report manually (print-to-PDF). The thing actually worth automating is the real
  signal (landing-page conversions), not the report — route that to `/sales-funnel`.
- **Treat the Investor-Ready Package as a draft, not diligence.** Its pitch deck, investment memo, 18-month
  financial model, and competitive teardown are AI-generated starting points — verify every number and claim
  before showing an investor; source-linking helps but doesn't make the projections real.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — Preuve's tiers, agent set, and pricing move; verify at preuve.ai.*

- **Cited ≠ demand.** Source-linked claims are the platform's whole pitch and they *do* beat a pure-LLM
  guess — but a citation shows the problem is *talked about*, not that a stranger will pay. Follow any score
  with a real-behavior test (smoke test / pre-sale).
- **The score is conservative on purpose (median ~55).** A middling number isn't a death sentence and a high
  one isn't proof; read it as directional. Don't compare Preuve's number to an inflated IdeaProof-style
  score as if they're on the same scale.
- **Three pricing axes are easy to confuse.** One-time reports (free Reality Check → paid Founder Report →
  packs → Investor Package) vs a **Radar monthly subscription** vs **lifetime** plans. Report-pack prices
  vary between pages — treat all figures as best-effort and confirm at preuve.ai/pricing.
- **The free Reality Check is a preview, not the full report.** It gives the score, top risks, ~2 competitor
  previews, and a verdict; the full competitor map (up to 15), sizing, pivots, and business plan are behind
  the paid Founder Report.
- **No public API, no webhooks, no Zapier/Make, no MCP.** It's a web tool. The only sharing surface is the
  shareable dashboard link (`preuve.ai/share/{slug}`); otherwise copy/print reports manually.
- **Radar monitors published signals, not your customers.** Re-scans track competitors/market/score over
  time — useful, but it's AI monitoring of public data, not evidence your users will convert.
- **Investor docs are AI drafts.** The Investor Package's deck/memo/financial model are starting points;
  verify the numbers before anyone with a checkbook sees them.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator landscape (use this to actually decide build-or-not; a validator's output is a gut check, not demand)
- `/sales-ideaproof` — IdeaProof platform help (the fast-score-in-120s + broad pre-launch-suite contrast to Preuve's cite-everything, conservative-score model)
- `/sales-readysetlaunch` — ReadySetLaunch platform help (interrogation-style validator that surfaces gaps — the rigor-over-speed sibling)
- `/sales-validator-ai` — Validator AI platform help (a free score-and-report validator — the fast-score sibling)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "Preuve scored my idea 61 and cited a bunch of Reddit threads — should I build it?"
**User says**: "Preuve gave my idea a viability score of 61 with links to real Reddit and G2 posts about the problem. That's real evidence, right?"
**Skill does**: Credits the citations as better than a pure-LLM guess — they show the problem is genuinely
discussed — but reframes them: a linked thread proves people *talk about* the pain, not that they'll *pay*.
Notes 61 is middling on Preuve's deliberately conservative scale (median ~55), so it's neither a green light
nor a kill. Tells the user to keep the cited competitor list, risks, and blind spots to sharpen the pitch,
then earn a real go/no-go with a smoke-test landing page (pre-set ≥5% join threshold) or a pre-sale —
routing the decision to `/sales-idea-validation` and the build to `/sales-funnel`.
**Result**: The founder uses the evidence to sharpen, and decides on stranger behavior, not the score.

### Example 2: Can I pull my Founder Reports into a spreadsheet via the API? (developer/automation)
**User says**: "I want to run 15 ideas through Preuve and pull the reports into a database via the API or a webhook."
**Skill does**: States plainly Preuve has **no documented public API, no webhooks, no Zapier/Make, and no MCP
server** — it's a UI tool, so there's no supported way to batch or export programmatically. Notes the only
sharing surface is the **shareable dashboard link** (`preuve.ai/share/{slug}`), and that reports can be
saved by print-to-PDF. Suggests that if scripting is essential, use a validator built for programmatic use,
and that the thing worth automating is a real demand signal (landing-page analytics), not a generated
report — pointing to `/sales-idea-validation` and `/sales-funnel`.
**Result**: The user avoids building on a non-existent API and picks a workable path.

### Example 3: "Is the $29 report a subscription, and what's Radar?" (pricing / tiers)
**User says**: "How does Preuve pricing work — is the Founder Report a monthly thing, and what does Radar add?"
**Skill does**: Separates the **three axes**: one-time reports (free Reality Check → a one-time Founder
Report → discounted packs → a one-time Investor-Ready Package) are **not** subscriptions; **Radar is a
monthly subscription** that re-scans an idea and flags competitor/market/score changes; and there are
**lifetime** plans. Frames Radar as competitor/market monitoring — useful after you commit, but not proof
of demand — and presents every figure as best-effort, pointing to preuve.ai/pricing since report-pack prices
vary between pages.
**Result**: The user understands they can buy a single report without any recurring charge, and what Radar is for.

## Troubleshooting

### "Preuve's score is way lower than the score another tool gave me"
**Symptom**: A founder ran the same idea through Preuve and IdeaProof (or Validator AI) and got a much lower number from Preuve.
**Cause**: Preuve scores **conservatively by design** (median ~55) while fast-score validators inflate
(IdeaProof ~78). The two numbers aren't on the same scale, so a direct comparison is meaningless.
**Solution**: Don't average them. Read each score as directional, keep Preuve's *cited* structured outputs
(competitors, risks) for their evidence value, and settle the go/no-go with a real demand test via
`/sales-idea-validation` — not by trusting whichever tool gave the friendlier number.

### "The free scan only showed 2 competitors and a verdict"
**Symptom**: The user expected the full competitor map and business plan but got a short preview.
**Cause**: The free **Reality Check** is a 60-second **preview** — score, top risks, ~2 competitor previews,
and a verdict. The full map (up to 15 competitors), TAM/SAM/SOM, pivots, and business plan are behind the
paid Founder Report.
**Solution**: If the preview verdict is promising and the user wants the full analysis, the paid Founder
Report unlocks it (best-effort — confirm at preuve.ai/pricing). But remind them even the full report is a
cited gut check, not demand — pair it with a smoke test.

### "I want an API / to export reports automatically"
**Symptom**: Wants to script Preuve or pull reports into another system.
**Cause**: Preuve has **no documented public API, webhooks, or iPaaS connectors** — it's a web tool.
**Solution**: Use the shareable dashboard link (`preuve.ai/share/{slug}`) to share, or print/copy the report
manually; if programmatic validation is essential, choose a tool that exposes an API. Automate the real
demand signal (landing-page analytics) instead — see `/sales-idea-validation` and `/sales-funnel`.
