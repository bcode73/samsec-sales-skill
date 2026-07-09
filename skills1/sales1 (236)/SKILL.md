---
name: sales-ideagrape
description: "Ideagrape (ideagrape.com) platform help — a free-tier + paid IdeaBrowser alternative blending startup-idea discovery with AI validation: browse a database of 700+ market-scored SaaS ideas, generate custom ideas from your skills, then analyze one with an opportunity score, a willingness-to-pay analyzer, an assumption validator, a build blueprint, and a growth matrix. Use when browsing Ideagrape's idea database to find a niche to build, generating or validating a SaaS idea, interpreting its opportunity score or WTP analysis, comparing it to the pricier IdeaBrowser, understanding the free tier's daily generation limit or the annual Starter/Pro plans, or asking whether it has an API to export ideas. UI-only, NO public API/webhooks/Zapier/MCP; scores are AI estimates and an AI-scored idea is not validated demand. Do NOT use for the validate-before-building method or comparing idea validators across the market (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in Ideagrape]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
---

# Ideagrape Platform Help

Ideagrape (**ideagrape.com**) is a **free-tier + paid IdeaBrowser alternative** that blends two jobs in
one tool: **idea discovery** (browse a database of 700+ AI-validated SaaS ideas with market data —
plus Idea of the Day, Trending Keywords, and a Market Analytics dashboard) **and idea validation**
(generate a custom idea from your skills, then run it through an opportunity score, a **Willingness-to-Pay
Analyzer**, an **Assumption Validator**, a **Build Blueprint**, and a **Startup Growth Matrix**, with an
AI Chat & Strategize helper on Pro). Its pitch is **speed + price**: "conviction in minutes" at a
fraction of IdeaBrowser's cost. It's a **UI web app** — **no public API** — and both the browsable
scores and the AI validation are **directional estimates, not proof anyone will pay**.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from Ideagrape?**
   - A) **Browse/generate** to find a niche or idea worth building (discovery side)
   - B) **Validate one idea** — opportunity score, WTP analyzer, assumption validator, build blueprint
   - C) Interpret an **opportunity score / market number / WTP** it produced
   - D) Compare it to the **paid IdeaBrowser** (or other validators/discovery tools)
   - E) Understand **pricing** — the free tier's daily generation limit, or the Starter/Pro annual plans
   - F) Get the ideas out / automate them (export / API reality)
2. **What's the real question — "what should I build / is this idea worth building?" or "how do I use
   this tool?"** If it's the go/no-go decision or a cross-market validator comparison, that's
   `/sales-idea-validation` (a browsable idea and an AI score are not demand) — route in Step 2.

Skip-ahead: if the user wants the validate-before-building *method* or to rank validators across the
market, route to `/sales-idea-validation` immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| Comparing Ideagrape against other validators/discovery tools (IdeaBrowser, VentureVault, BuildOrNot, DimeADozen…) | `/sales-idea-validation {question}` |
| Deep **Reddit demand-signal** discovery / scoring as its own workflow | `/sales-trendseeker {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer Ideagrape-specific questions using Step 3.

## Step 3 — Ideagrape platform reference

**Read `references/platform-guide.md`** for the full reference — the discovery modules (idea database,
Idea of the Day, Trending Keywords, Market Analytics) and the validation modules (Idea Generator,
opportunity score, WTP Analyzer, Assumption Validator, Build Blueprint, Growth Matrix, AI Chat), the
free/Starter/Pro pricing and the free tier's daily generation limit, the no-public-API automation
reality, and the IdeaBrowser comparison.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Separate its two jobs, and don't let either stand in for demand.** The **discovery** side (browsing
  700+ scored ideas, Idea of the Day, trending keywords) hands you a *shortlist*; the **validation** side
  (generate → opportunity score, WTP, assumptions, blueprint) hands you a *structured AI opinion*. Keep
  the useful structured parts (competitor list, market angle, assumptions to test) to sharpen the pitch,
  but take the go/no-go from a real behavior test (smoke test / pre-sale), routed to
  `/sales-idea-validation`. Neither a browsable idea nor an AI score is a paying stranger.
- **Treat every number as an AI/data estimate — verify it.** Opportunity scores, "market size," search
  volume, growth trends, and the WTP analyzer's price are model-/data-derived, not audited. Tell the user
  to **cross-check any market-size or search-volume figure against a primary source** (a keyword tool,
  Google Trends, real competitor pricing) before quoting it. The WTP number is a hypothesis to test with
  a real pre-sale, not a price to set.
- **Frame it against IdeaBrowser honestly.** Ideagrape positions as the **cheaper IdeaBrowser
  alternative** — same browse-scored-ideas + validate shape, undercutting IdeaBrowser on price
  (annual Starter/Pro vs IdeaBrowser's pricier tiers). Present that as a **best-effort** tradeoff: it's a
  smaller, solo-maker tool, so don't promise parity on idea depth, freshness, or catalog size — point the
  user to the live site to confirm.
- **Present pricing as best-effort and plan-gated.** Note the **free tier is capped** (a daily
  generation limit and a limited window of recent ideas), that **AI Chat & Strategize is Pro-gated**, and
  that generation counts differ by plan (Starter vs Pro) — flag all specifics as best-effort and point to
  ideagrape.com/pricing, since a small tool's tiers change.
- **There's no public API — don't plan an integration around it.** If asked to export or automate, say
  plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP** — it's a UI web app.
  Give the workable fallbacks: copy the ideas/analysis you can see into your own store (mind their terms),
  or pull the underlying signals from source (a keyword-volume API, Google Trends, Reddit, Product Hunt)
  if you need it scripted. The thing worth automating is a real demand signal, not a directory.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — Ideagrape is a small, solo-maker tool with a JS-rendered site and
little review coverage; verify pricing, the free-tier limits, catalog size, and scoring specifics at
ideagrape.com.*

- **A browsable or AI-scored idea is not validated demand.** Both the vault entry and the opportunity
  score are *research/opinion*, not proof anyone will pay — follow with a real-behavior test (smoke test
  / pre-sale). The go/no-go is a stranger taking an action.
- **Opportunity scores, market size, and search/growth numbers are estimates.** Model-/data-derived and
  not audited — verify any figure against a primary source before acting on it.
- **The WTP Analyzer's price is a hypothesis, not a validated price.** "Willingness to pay" from an AI
  tool is a starting guess; only a real pre-sale confirms what people actually pay.
- **Free tier is capped and plan-gated.** A daily generation limit and a limited window of recent ideas
  on free; more generations on Starter, AI Chat + the most generations on Pro. Confirm current counts.
- **Cheaper IdeaBrowser alternative — parity is unproven.** It undercuts IdeaBrowser on price, but idea
  depth/freshness/catalog size are best-effort; don't promise it matches the paid original.
- **No public API, no webhooks, no Zapier/Make/MCP.** UI web app — you can't script or batch-export the
  ideas or reports. Copy manually or pull signals from source.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator/discovery landscape (use this to actually decide build-or-not; a browsable idea + AI score is not demand)
- `/sales-venturevault` — VentureVault platform help (the closest analog — a *free* IdeaBrowser-clone idea vault; Ideagrape adds active validation tools and a paid tier)
- `/sales-buildornot` — BuildOrNot platform help (another discovery-data + AI-evaluator sibling — datasets of revenue-ranked tools, Reddit ideas, trending topics)
- `/sales-trendseeker` — Reddit-based demand discovery + evidence scoring (a real-signal sibling to a curated idea database)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "I don't have an idea yet — can Ideagrape find me one?"
**User says**: "I want to build a SaaS but have no idea what. Is Ideagrape good for finding one?"
**Skill does**: Points the user at the **discovery** side — the database of 700+ market-scored ideas,
Idea of the Day, and Trending Keywords — to build a shortlist of candidate niches, while explaining the
opportunity scores and market numbers are AI/data estimates to sanity-check, not facts. Then it can
**generate** a custom idea from their skills, but insists the go/no-go comes from a real demand test —
routing the decision to `/sales-idea-validation` and deeper Reddit signal to `/sales-trendseeker`.
**Result**: The user gets a curated + generated shortlist to research, not a false sense that a scored idea equals demand.

### Example 2: "Ideagrape scored my idea high and gave me a WTP price — build it?"
**User says**: "The opportunity score is strong and the WTP Analyzer says I can charge $49/mo. Good to go?"
**Skill does**: Reframes both as **directional AI outputs, not demand** — keeps the structured parts
(competitors, market angle, the assumptions the Assumption Validator surfaced) to sharpen the pitch, but
tells the user to verify the market/search numbers against a primary source and treat $49 as a hypothesis.
Prescribes the real test: a smoke-test landing page with a pre-committed conversion threshold, then a
**pre-sale at that price** to see who actually pays — routing the build to `/sales-funnel`.
**Result**: The founder earns a go/no-go and a real price from stranger behavior instead of trusting a score.

### Example 3: Can I export Ideagrape's ideas via an API? (developer/automation)
**User says**: "I want to pull Ideagrape's scored ideas into my own database via API."
**Skill does**: States plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP**
— it's a UI web app, so there's no supported way to export programmatically. Suggests the fallbacks: copy
the ideas/analysis you can see into your own store (mind their terms), or pull the underlying signals
from source (a keyword-volume API, Google Trends, Reddit, Product Hunt). Notes the thing worth automating
is a real demand signal (landing-page conversions), not a directory.
**Result**: The user avoids building on a non-existent API and picks a workable path to the signal.

## Troubleshooting

### The opportunity scores feel optimistic / every idea looks buildable
**Symptom**: The database and the analyzer make most ideas look promising.
**Cause**: The opportunity scores, market size, and search/growth numbers are **AI-/data-generated
estimates**, not audited — they read directional and can skew encouraging.
**Solution**: Use the scores to *rank and shortlist*, not to decide. Verify any market/search figure
against a primary source, then run a real demand test (smoke test / pre-sale) via `/sales-idea-validation`.

### I hit a generation limit / ran out of ideas on the free plan
**Symptom**: The generator stops or the recent-ideas list is capped.
**Cause**: The **free tier is capped** — a daily AI-generation limit and a limited window of recent
ideas; more generations require Starter, and AI Chat + the highest generation count require Pro.
**Solution**: Confirm current limits at ideagrape.com/pricing; decide whether an annual Starter/Pro plan
is worth it for how much you'll iterate. Because you'll re-validate the same idea across pivots, budget
for re-runs rather than assuming one generation is enough.

### I want an API or a way to export/automate the ideas and reports
**Symptom**: Want to script Ideagrape or pull its scored ideas/analysis into another system.
**Cause**: Ideagrape has no documented public API, webhooks, or iPaaS connectors — it's a UI web app.
**Solution**: Copy the visible ideas/analysis into your own store (mind their terms), or pull the
underlying signals from source (a keyword-volume API, Google Trends, Reddit, Product Hunt). Automate a
real demand signal (landing-page analytics) instead. See `/sales-idea-validation`.
