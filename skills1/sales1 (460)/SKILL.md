---
name: sales-rebeccai
description: "RebeccAi (rebecc.ai) platform help — a cheap AI business-idea evaluator + one-off business-plan generator for solo founders and indie hackers: describe an idea (plus team size, budget, and a chosen \"feedback personality\") and it returns a quick evaluation, a strengths/weaknesses assessment, improvement tips, and an optional ready-to-use business plan. Use when running an idea through RebeccAi, interpreting its score or evaluation points, using the improve-my-idea suggestions, buying the one-time business plan, understanding the free tier's daily-idea and character caps vs Premium, wondering why the feedback feels flattering (the personality toggle biases tone), or asking whether it has an API. UI-only, NO public API/webhooks/Zapier/MCP; an AI evaluation is not validated demand and its plan financials are AI estimates. Do NOT use for the validate-before-building method or comparing idea validators across the market (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in RebeccAi]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
---

# RebeccAi Platform Help

RebeccAi (**rebecc.ai** — note: rebeccai.com is a parked/for-sale domain, not the product) is a
**low-cost AI business-idea evaluator and one-off business-plan generator** for solo founders, indie
hackers, and first-time entrepreneurs. You describe an idea in a **single text box** — plus your team
size, budget, and a chosen **"feedback personality"** — and it returns a **quick evaluation**, a
**strengths/weaknesses assessment** across its evaluation points, **improvement suggestions**
("improve your idea"), and an optional **ready-to-use business plan** (a ~15–25 page document sold as a
one-time product). Its pitch is **price**: among the cheapest ways to get an AI take plus a plan. It's a
**UI web app — no public API** — and both the evaluation and the plan's financials are **AI estimates,
not proof anyone will pay**.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from RebeccAi?**
   - A) **Evaluate/assess** an idea — the quick evaluation + strengths/weaknesses
   - B) **Improve** an idea with its refinement suggestions
   - C) Interpret a **score / evaluation point** it produced
   - D) Buy/understand the **one-time business plan** (what's in it, is it worth it)
   - E) Understand **pricing** — the free tier's daily-idea and character caps vs Premium
   - F) Get reports out / automate them (export / API reality)
2. **What's the real question — "is this idea worth building?" or "how do I use this tool?"** If it's the
   go/no-go decision or a cross-market validator comparison, that's `/sales-idea-validation` (an AI
   evaluation is not demand) — route in Step 2.

Skip-ahead: if the user wants the validate-before-building *method* or to rank validators across the
market, route to `/sales-idea-validation` immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| Comparing RebeccAi against other validators (Validator AI, IdeaProof, Informly, DimeADozen…) | `/sales-idea-validation {question}` |
| Deep **Reddit demand-signal** discovery / scoring as its own workflow | `/sales-trendseeker {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |
| Writing a fuller / lender-ready **business plan** as its own job | `/sales-idea-validation {question}` (routes to the plan-writing tools) |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer RebeccAi-specific questions using Step 3.

## Step 3 — RebeccAi platform reference

**Read `references/platform-guide.md`** for the full reference — the evaluation/assessment/improvement
modules and the evaluation-point inputs (personality, team size, budget), the one-time business-plan
product, the free/Premium/Business-Plan pricing and the free tier's daily-idea and character caps, the
no-public-API automation reality, and how it compares to the validator cluster.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **The evaluation is an AI opinion, not demand — keep the structure, discard the verdict.** RebeccAi
  reads one text box and returns a score plus strengths/weaknesses. Keep the useful structured parts
  (the weaknesses it flags, the improvement suggestions, any competitor/positioning angle) to sharpen the
  pitch, but take the go/no-go from a real behavior test (smoke test / pre-sale), routed to
  `/sales-idea-validation`. A high evaluation is not a paying stranger.
- **Warn about the "feedback personality" toggle — it biases the result.** Choosing a feedback tone
  (e.g. "conservative & traditional") lets the founder bias scoring toward the answer they want, which
  undermines objectivity. Tell the user to pick the **most critical/skeptical** setting available, or to
  read the encouraging tones as marketing, not signal — a tool you can tune to flatter you can't
  objectively validate you.
- **A generated business plan for an unvalidated idea is a document, not a strategy.** The one-time plan
  is cheap and fast, but building a 15–25 page plan (with financial projections) around an idea nobody
  has tested is, as reviewers put it, a "fantasy" — the financials are **AI estimates with no real market
  input** and can be invented. Use the plan as a first draft/structure; replace every number, and
  validate demand *before* trusting the plan.
- **Present pricing as best-effort and plan-gated.** Note the **free tier is capped** (a small
  daily-idea limit and a short per-point character cap, no customization), that **unlimited ideas + full
  evaluation points + longer output + customizable answers are Premium-gated**, and that the **business
  plan is a separate one-time purchase** — flag all specifics as best-effort and point to
  rebecc.ai/pricing, since a small tool's tiers change (Premium is also an intro-then-higher price).
- **There's no public API — don't plan an integration around it.** If asked to export or automate, say
  plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP** — it's a UI web app;
  the only export is the business-plan document (edit/save/download) and manual copy. If you need the
  signals scripted, pull them from source (a keyword-volume API, Google Trends, Reddit) instead. The
  thing worth automating is a real demand signal, not an AI evaluation.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — RebeccAi is a small, solo-maker tool with no verified third-party
reviews (G2/Trustpilot/Capterra); verify pricing, the free-tier caps, plan contents, and evaluation
behavior at rebecc.ai.*

- **An AI evaluation is not validated demand.** The score/assessment is *opinion*, not proof anyone will
  pay — follow it with a real-behavior test (smoke test / pre-sale). The go/no-go is a stranger taking an
  action.
- **The "feedback personality" toggle biases the verdict.** You can tune the tone toward what you want to
  hear; that undermines objectivity. Pick the most skeptical setting and treat encouraging output as
  marketing.
- **The business plan is a cheap document, not a strategy.** A 15–25 page plan built on an untested idea
  is a "fantasy"; its financial projections are **AI estimates with no real market input** — replace the
  numbers and validate first.
- **Single text-box input, no structured questioning.** Unlike gap-surfacing interrogators
  (ReadySetLaunch) it's a one-shot format with no per-weakness follow-up — output quality tracks how
  concretely you frame the customer + problem.
- **Free tier is capped and plan-gated.** A small daily-idea limit + a short per-point character cap and
  no customization on free; unlimited ideas, all evaluation points, longer output, and customizable
  answers are Premium; the business plan is a separate one-time buy. Confirm current limits.
- **No verified third-party reviews.** No G2/Trustpilot/Capterra footprint — treat social-proof and
  accuracy claims as unverified.
- **No public API, no webhooks, no Zapier/Make/MCP.** UI web app — you can't script or batch-export the
  evaluations; only the business-plan document exports. Copy manually or pull signals from source.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator/business-plan landscape (use this to actually decide build-or-not; an AI evaluation is not demand)
- `/sales-ideaproof` — IdeaProof platform help (a credit-based 120s validator that also bundles a plan/brand/logo/pitch/ads — a richer sibling to RebeccAi's cheap evaluate-plus-plan)
- `/sales-informly` — Informly platform help (a per-report validator that returns a 75+ page PDF — another cheap validate-plus-report sibling)
- `/sales-readysetlaunch` — ReadySetLaunch platform help (an interrogation-style validator that surfaces gaps instead of a flattering score — the antidote to RebeccAi's tunable feedback tone)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "RebeccAi scored my idea highly — should I build it?"
**User says**: "I ran my idea through RebeccAi and it gave a strong evaluation. Good to go?"
**Skill does**: Reframes the evaluation as a **directional AI opinion, not demand** — and flags that the
**feedback-personality toggle** may have biased it toward encouragement. Keeps the structured parts (the
weaknesses it flagged, the improvement suggestions) to sharpen the pitch, then prescribes the real test:
a smoke-test landing page with a pre-committed conversion threshold, then a pre-sale to see who actually
pays — routing the build to `/sales-funnel` and the decision framework to `/sales-idea-validation`.
**Result**: The founder earns a go/no-go from stranger behavior instead of trusting a tunable score.

### Example 2: "Is RebeccAi's $14.99 business plan worth buying?"
**User says**: "Should I buy the one-time business plan from RebeccAi?"
**Skill does**: Explains it's the cheapest way to get a 15–25 page plan, but that a plan built on an
**untested idea is a document, not validation** — its **financial projections are AI estimates with no
real market input** and can be invented. Advises using it as a first-draft structure (replace every
number and edit heavily), and validating demand *before* relying on it. Presents the price as best-effort
and points to rebecc.ai/pricing.
**Result**: The user buys (or skips) the plan with clear eyes and doesn't mistake a cheap document for a strategy.

### Example 3: Can I export RebeccAi's evaluations via an API? (developer/automation)
**User says**: "I want to pull RebeccAi's evaluations into my own database via API."
**Skill does**: States plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP**
— it's a UI web app, so there's no supported way to export programmatically; only the business-plan
document exports (edit/save/download). Suggests the fallbacks: copy the evaluation you can see into your
own store (mind their terms), or pull the underlying signals from source (a keyword-volume API, Google
Trends, Reddit). Notes the thing worth automating is a real demand signal, not an AI evaluation.
**Result**: The user avoids building on a non-existent API and picks a workable path to the signal.

## Troubleshooting

### The evaluation feels flattering / it likes almost every idea
**Symptom**: RebeccAi's assessment reads encouraging and rarely says "don't build this."
**Cause**: The **feedback-personality toggle** lets you bias the tone toward what you want to hear, and
the evaluation is an AI opinion with no independent rubric — so it skews optimistic.
**Solution**: Pick the most critical/skeptical personality setting, read encouraging output as marketing,
keep only the weaknesses/improvements it surfaces, and put the go/no-go on a real demand test (smoke test
/ pre-sale) via `/sales-idea-validation`.

### The business plan's financials look made up
**Symptom**: The generated plan's revenue/cost projections don't match reality.
**Cause**: The plan is generated from a short idea description with **no real market data input** — the
financials are **AI estimates** (reviewers report hallucinated figures).
**Solution**: Treat the plan as a first-draft structure, not a forecast — replace every number with your
own research, and validate demand before trusting it. For a fuller/lender-ready plan, see the
business-plan tools via `/sales-idea-validation`.

### I want an API or a way to export/automate the evaluations
**Symptom**: Want to script RebeccAi or pull its evaluations/plans into another system.
**Cause**: RebeccAi has no documented public API, webhooks, or iPaaS connectors — it's a UI web app; only
the business-plan document exports.
**Solution**: Copy the visible evaluation into your own store (mind their terms), or pull the underlying
signals from source (a keyword-volume API, Google Trends, Reddit). Automate a real demand signal
(landing-page analytics) instead. See `/sales-idea-validation`.
