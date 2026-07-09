# ReadySetLaunch Platform Reference

<!-- Source: https://readysetlaunch.ai/ , https://readysetlaunch.ai/pricing , https://readysetlaunch.ai/compare/ideaproof/review/ (fetched 2026-07) -->

## Overview

ReadySetLaunch (readysetlaunch.ai) is an **AI startup-idea validator** whose product **Launch Control**
is built to *interrogate* a founder rather than flatter them. It walks you through 13 structured questions
across 7 product-judgement pillars, **surfaces the gaps in weak answers** instead of emitting a single
feel-good score, and grades every signal against a curated database of real startup outcomes (failed,
successful, unicorn, acquired). Target user: first-time founders, vibe coders, and solo builders who can
now ship anything and need a reality check on *what* to ship. Primary differentiator vs the field:
**anti-gaslighting** — no engineered encouragement, no hallucinated confidence, and a deliberate
~30–45-minute pace ("30 minutes on purpose").

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| **Launch Control** (core) | 13 structured questions across the 7 pillars; per-question sub-prompts show what a good answer looks like; coaches you to close gaps until "strong signal strength" | **UI-only** |
| **7-pillar scoring** | Grades each pillar against a knowledge base of real startup outcomes; surfaces specific gaps rather than one number | **UI-only** |
| **Launch-readiness report** | Output with pillar-level signals + a clear next move | **UI-only** (copy/save manually — no export API) |
| **Startup case database** (`/cases/`) | Browsable successes, failures, and acquisition case studies used as grounding data | **UI-only** (web content) |
| **Competitor reviews** (`/compare/{tool}/review/`) | Vendor-published pros/cons/pricing reviews of other validators (IdeaProof, BuildOrNot, RebeccAi, Informly…) | **UI-only** (web content) |
| **Credits / account** | 3 free credits, one-time packs, no subscription | **UI-only** |

**No public API, no webhooks, no MCP server, no Zapier/Make modules.** Everything runs in the browser.

## The 7 pillars

Launch Control scores 13 questions across these seven product-judgement pillars:

1. **Problem clarity** — is the problem specific and real?
2. **Target customer definition** — who exactly is it for?
3. **Demand signal strength** — is there evidence people want it?
4. **Differentiation** — why this vs how people solve it today?
5. **Execution feasibility** — can you actually build/ship it?
6. **Distribution readiness** — how will you reach the customer?
7. **Monetisation viability** — will they pay, and does the model work?

Each question is broken into plain-English sub-prompts that describe what a strong answer contains; weak
answers get a **per-gap response** (the tool names the gap and asks you to close it) instead of a numeric
pass. The framework clusters around **demand, distribution, and monetisation** as the make-or-break axes.

## Pricing, limits & plan gates

*Best-effort from research (2026-07) — confirm at readysetlaunch.ai/pricing. Exact per-pack credit counts
and prices are not fully published.*

- **Free trial:** **3 credits, no card required.**
- **Model:** **Credit-based, NO subscription.** You buy **one-time packs** (advertised **from ~£14.99**).
- **Credits never expire.**
- **No monthly recurring plan** — cost scales with how many ideas you run, not calendar time.
- **Rough usage:** budget one idea ≈ one Launch Control run (confirm the exact credit cost per run in-app —
  it isn't published as a fixed number).

There is no free-forever tier beyond the 3 starter credits, and no plan-gated API (there is no API at all).

## Integrations

**None documented.** No native CRM connectors, no Zapier/Make triggers or actions, no webhooks, no public
API. Data flow is **into** the tool (you type answers) and **out** only via the on-screen report you copy
or save manually. If you need validation output in another system, re-key it by hand or drive a
programmatic validator instead.

## Data model

There is **no public API**, so there are no documented object schemas. The only user-facing artifact is the
**launch-readiness report**. A representative shape of what that report contains (constructed from the
product description — not an API response):

```json
{
  "idea": "One-line description of the idea being validated",
  "pillars": {
    "problem_clarity":        { "signal": "strong|moderate|weak", "gaps": ["..."] },
    "target_customer":        { "signal": "strong|moderate|weak", "gaps": ["..."] },
    "demand_signal":          { "signal": "strong|moderate|weak", "gaps": ["..."] },
    "differentiation":        { "signal": "strong|moderate|weak", "gaps": ["..."] },
    "execution_feasibility":  { "signal": "strong|moderate|weak", "gaps": ["..."] },
    "distribution_readiness": { "signal": "strong|moderate|weak", "gaps": ["..."] },
    "monetisation_viability": { "signal": "strong|moderate|weak", "gaps": ["..."] }
  },
  "next_move": "The single clearest next action the report recommends"
}
```
<!-- Constructed from docs — verify against live product; ReadySetLaunch exposes no API. -->

## Quick-start recipes

ReadySetLaunch has no API, so "recipes" are workflow patterns, not code.

### Recipe 1 — Get the most out of a Launch Control run (workflow)
1. Write a **sharp one-line idea** first: specific customer + exact problem + why-you-vs-today. Vague input
   → vague gaps.
2. Answer each of the 13 questions as if writing to a skeptical investor — the sub-prompts tell you what a
   strong answer contains.
3. When a pillar is flagged **weak**, don't rewrite to satisfy the tool — write down the gap as a **real
   task** (e.g. "no demand evidence" → go run a smoke test).
4. Save/copy the launch-readiness report; the **weak pillars are your validation to-do list**.

### Recipe 2 — Export the report without an API (workaround)
Since there's no API/export endpoint, capture the report manually:
```bash
# There is NO ReadySetLaunch API. To archive a report, use the browser:
#   - Print to PDF (Cmd/Ctrl-P → Save as PDF), or
#   - Select-all → copy into a doc/markdown file.
# To structure it for a spreadsheet, paste the pillar signals into a CSV by hand:
printf 'pillar,signal,gap\n' > readysetlaunch_report.csv
# then append rows manually, e.g.:
printf 'demand_signal,weak,"no evidence anyone wants it"\n' >> readysetlaunch_report.csv
```

### Recipe 3 — Pair the gaps with a real demand test (the part worth automating)
The report is a gut check; the go/no-go is stranger behavior. Automate *that* instead:
```python
# Pseudocode: the demand signal, not the ReadySetLaunch report, is what you script.
# 1. Build a fake-door landing page (see /sales-funnel).
# 2. Drive a little traffic (a community post or small ad budget).
# 3. Measure the action rate; a commonly cited bar is ~5%+ of targeted visitors.
conversions = signups / targeted_visitors
go = conversions >= 0.05           # decide this threshold BEFORE the test
```

## Integration patterns

**Not applicable — no API, webhooks, or connectors.** If a user asks for a CRM-sync, webhook-listener, or
batch-pipeline pattern, the honest answer is that ReadySetLaunch supports none of them. The realistic
architecture is: (1) run ideas manually in Launch Control, (2) copy the launch-readiness report out by
hand, and (3) build any automation around the **real demand test** (landing-page analytics, waitlist
signups, pre-sale checkout) — see `/sales-funnel` and `/sales-audience-growth`. For programmatic idea
validation at volume, choose a tool that actually exposes an API.
