# aicofounder Platform Reference

## Overview

aicofounder (aicofounder.com) is an **AI "co-founder"** for solo founders, indie hackers, and
first-time entrepreneurs — a structured, phased workspace that takes an idea from **discovery →
research → validation → plan → build → launch**, rather than a general-purpose chatbot. Its
differentiator is **multi-agent deep market research that scans real communities (Reddit, X)** for
pain points and demand signals, so validation is grounded in actual discussions instead of pure LLM
opinion. It's trusted by 90K+ founders. It is **UI-only — no documented public API.**

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| Structured phases | Guided idea → research → validation → plan → launch workflow | UI-only |
| Multi-agent market research | Parallel agents scan Reddit / X for pain points & demand signals | UI-only |
| Idea validation | Evaluates which problems are worth pursuing from real evidence | UI-only |
| Competitive analysis | Surveys the competitive landscape | UI-only |
| Visual product canvas | Persistent workspace to map concepts, notes, feature overview | UI-only |
| Planning agent | Identifies your biggest constraint → adaptive step-by-step tasks | UI-only |
| Website builder | Generates a landing/site | UI-only |
| Content calendar | Plans marketing content | UI-only |
| Persistent project memory | Learns the project, gives tailored auto-saved advice | UI-only |
| Privacy mode | Confidential work | UI-only |

**Everything is UI-only.** No public API, no webhooks, no documented Zapier/Make connectors. The
agents run in the product against credits.

## Pricing, limits & plan gates

*Best-effort from research (2026-07) — third-party quotes disagree; confirm at aicofounder.com/pricing.*

- **Free to start — ~15 credits per month, no credit card.** The first phases (idea discovery + market
  research) are available free.
- **Paid plan unlocks advanced features.** Reported prices **conflict across sources** — e.g. **~$25/mo**
  (a comparison site) vs **~$149** (a review). Treat all as best-effort and confirm live.
- **Credits are the limit**, not API rate limits (there's no API). Heavier research/phases consume more credits.
- Frame the buy decision as **"how many projects/phases will I run"** against the plan.

## Integrations

- **Direction:** none programmatic — work happens in the browser workspace.
- **No native CRM / Zapier / Make connectors** are documented.
- The realistic workflow "integration": use aicofounder to research demand and produce a plan, then
  execute in your own tools (site, email, ads) and validate demand with a real test.

## Data model

There is no public API and no documented response schema. A research/validation *result*, as shown in
the UI, is structured evidence — for example:

```json
{
  "idea": "A time-tracking tool for freelance designers",
  "target_customer": "Freelance / solo designers billing hourly",
  "demand_signals": [
    { "source": "reddit", "subreddit": "r/freelance", "pain": "clients dispute logged hours", "strength": "high" },
    { "source": "x", "pain": "forgetting to start the timer", "strength": "medium" }
  ],
  "competitors": ["...", "..."],
  "biggest_constraint": "distribution — how designers will discover it",
  "next_tasks": ["interview 10 freelance designers", "build a fake-door landing page"]
}
```
<!-- ILLUSTRATIVE ONLY — aicofounder has no public API or documented schema; this represents UI output, not a real response contract. Do not code against it. -->

## Getting the most out of it (in place of quick-start API recipes)

There's no API, so "recipes" are usage patterns, not code:

1. **Start every phase from a concrete idea + target customer.** Name the specific audience and the
   exact problem before running research — the Reddit/X pain-point scan sharpens dramatically with a
   precise audience, and the whole phased plan builds on it.
2. **Trust the grounded research, verify the verdict.** The Reddit/X demand signals are genuinely useful
   evidence (better than a pure-LLM score) — use them to prioritize. But an AI summary of discussions is
   still not a stranger paying you: confirm with a smoke test / pre-sale.
3. **Treat the plan as structure, not orders.** Sanity-check the "biggest constraint" against your
   reality and re-order the generated tasks; execute the plan against a real demand test, not on faith.

## Automation reality (developer note)

- **No public API.** If a workflow needs programmatic research/validation, aicofounder is the wrong
  tool — it can't be called in a supported way.
- **Don't scrape the app.** Agents run behind the UI/credits; automating them is fragile and against intent.
- **Automate the demand signal instead.** Wire real behavior (landing-page conversion, waitlist growth,
  pre-sale revenue) into your dashboards — not an AI research summary. See `/sales-idea-validation`.
