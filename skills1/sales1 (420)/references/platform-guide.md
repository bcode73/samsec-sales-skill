# PlanSnack Platform Reference

<!-- Best-effort from research (2026-07). PlanSnack has a thin public footprint (no user reviews on major
directories, JS-light homepage). Pricing, export formats, account requirement, and any future "premium
services" can change — verify at plansnack.com. -->

## Overview

PlanSnack (**plansnack.com**) is a **free, guided one-page business-plan builder** for first-time founders,
solopreneurs, and small-business owners. You complete a **five-step** process and fill in a **one-page
("lean") plan** yourself, with **pre-written example text** per section as a starting point, then
**download / print / share** the result. Its differentiator is **speed + zero learning curve** ("a plan in
minutes, not hours") and being **genuinely free** — **not** AI generation. It is **UI-only** with **no public
API and no integrations**.

## What it is — and what it is NOT

| PlanSnack IS | PlanSnack is NOT |
|---|---|
| A **manual, guided template** with example text you edit | An **AI generator** (no questionnaire→plan, no AI advisor) |
| A **one-page** / lean summary format | A **full multi-section narrative plan** (~15–30 pages) |
| A **free** tool (no paywall at research) | A **forecasting engine** (no P&L, cash-flow, multi-year projections) |
| Download / print / share of the one-pager | A **lender/SBA/investor funding package** |
| Standalone (nothing to connect) | An **API / integration / automation** surface |

This table is the core of the skill: most PlanSnack confusion is someone expecting an AI generator or a
fundable full plan and getting a free one-page template instead.

## Capabilities & automation surface

- **Five-step guided process** — *UI-only.* Walks you through the sections of a one-page plan.
- **Pre-written examples per section** — *UI-only.* Industry-flavored example text ("pre-written text and
  inspiration") you can start from and rewrite. Marketed as covering many business types (startup, restaurant,
  food truck, coffee shop, online store, small business, mobile app).
- **One-page plan output** — *UI-only.* The finished plan is a single page in the "one page business plan" format.
- **Download / print / share** — *UI-only.* The only export path. Exact file format (PDF vs Word) was **not
  confirmed** at research; "download, print, and share" is the stated capability.
- **No AI generation, no AI advisor/chat** — the plan is written by the user.
- **No financial modeling** — no P&L, cash-flow, break-even, or multi-year projections.
- **No API, webhooks, Zapier/Make, or MCP** — nothing to automate against.
- **No native integrations** — the platform itself states "No Integrations at this time" on third-party listings.

## Pricing, limits & plan gates

*Best-effort at research (2026-07) — confirm on plansnack.com.*

- **Completely free.** The homepage states **"no upgrades, no pro version and no credit card required"**, and
  that **download and sharing are included at no cost**. There were **no paid tiers** at research.
- **Future "premium services"** are **promised but not live** — the company reserves the right to add paid
  services later. Treat any "paid plan" claim as unconfirmed until it appears on the live site.
- **Account requirement: unconfirmed.** Whether you must sign up to build/save/export was not established at
  research — verify on the site.
- **Aggregator-listing discrepancy (important).** Third-party directories (Slashdot, GoodFirms) auto-populate
  feature tags — e.g. **"financial projections," "collaboration," "investor management," "pitch presentation,"
  "dashboard"** — that PlanSnack's **own homepage does not claim**. These are **unverified aggregator tags**;
  do not represent them as real features. GoodFirms/Slashdot also showed **"No User Reviews"** and support
  limited to **business hours**, training **not offered**.

## Integrations

**None.** PlanSnack has **no native connectors, no Zapier/Make, no API, and no webhooks**. Data flow is a
**one-way manual export** (download/print/share) of the one-pager out of the tool. There is no way to read
plans into a CRM/warehouse or to write data in programmatically.

## Data model

There is **no public API and no documented data model** — PlanSnack does not expose plan objects
programmatically. Conceptually a plan is a single **one-page document** composed of the guided sections
(a lean/one-page business plan typically covers: the problem/opportunity, the solution/offer, the target
customer/market, the revenue/business model, and the go-to-market / key next steps). The exact section set is
defined in the UI's five steps and is **UI-only** — capture it by using the tool, not by querying it.

<!-- Constructed from the "one page business plan" positioning — verify the exact five sections in the live UI. -->
```json
// Illustrative only — PlanSnack exposes no API/JSON. This is how a one-page plan maps conceptually.
{
  "plan_type": "one_page",
  "sections": {
    "opportunity_problem": "the problem / market opportunity",
    "solution_offer": "the product or service",
    "target_customer": "who it's for",
    "business_model": "how it makes money (high level, no forecast)",
    "go_to_market_next_steps": "how you'll reach customers / what's next"
  },
  "export": "manual download / print / share (format unconfirmed: PDF vs Word)"
}
```

## Quick-start recipes

PlanSnack has no API, so there are no code recipes. The realistic "recipes" are decisions and workflows:

### Recipe 1 — Use PlanSnack for a fast one-page plan, then decide if you need more
1. Open plansnack.com and start the **five-step** flow.
2. For each section, **start from the example text** and rewrite it for your specific business (exact customer,
   the real problem, how it's solved today, your offer, how you make money).
3. **Download / print / share** the one-pager.
4. **Decide the format fit:** if it's just for your own clarity, a co-founder sync, or a quick teaser — done.
   If a **bank/SBA or investor** needs financials, treat the one-pager as the *summary* and build the full plan
   + projections elsewhere (route via `/sales-idea-validation`).

### Recipe 2 — Programmatic plan text (since PlanSnack can't do it)
PlanSnack is UI-only and manual, so to generate plan text at scale, **call an LLM API directly** instead:
```bash
# Illustrative — generate one-page-plan text with an LLM (PlanSnack has NO API of its own)
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 1200,
    "messages": [{"role":"user","content":"Write a one-page lean business plan for: <describe the business>. Sections: opportunity, solution, target customer, business model, go-to-market/next steps. Keep it to one page."}]
  }'
```
Then have the founder paste/adapt it — and remember a generated plan is a **document, not validated demand**.

### Recipe 3 — Pair the one-pager with a real demand test
A plan (one-page or full) doesn't prove anyone wants the thing. Use PlanSnack to get the idea straight, then
run the actual go/no-go on stranger behavior: a **smoke-test landing page** (`/sales-funnel`) + a
**waitlist/pre-sale** (`/sales-audience-growth`), with a pre-committed conversion threshold. See
`/sales-idea-validation` for the full evidence ladder.

## Integration patterns

**Not applicable — there is no integration surface.** PlanSnack cannot participate in CRM sync, webhook
listeners, or batch pipelines. If a workflow needs plan data to move automatically, PlanSnack is the wrong
tool; use an LLM API for generation and a full-plan tool (Upmetrics/VentureKit/Bizplanr) if structured output
or richer plans are needed — none of which offer public APIs either, so the automation ceiling for this whole
category is "call an LLM directly."

## One-page vs full plan — the fit decision

| Situation | Use a one-pager (PlanSnack) | Use a full plan |
|---|---|---|
| Get your own thinking straight | ✅ | overkill |
| Co-founder / early-team alignment | ✅ | optional |
| Quick investor teaser / "napkin" pitch | ✅ | later |
| **Bank / SBA loan application** | ❌ (summary only) | ✅ (needs projections, P&L, use-of-funds) |
| **Equity investors doing diligence** | teaser only | ✅ (needs financial model, market sizing) |
| Complex/multi-product or regulated business | ❌ | ✅ |

When the right column applies, route to `/sales-idea-validation` (which maps the full-plan/forecasting tools),
and replace any AI-estimated numbers with real unit economics and cited market size before a funder sees them.
