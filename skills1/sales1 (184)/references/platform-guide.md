# FounderPal Platform Reference

## Overview

FounderPal (founderpal.ai, by **Dan Kulkov**) is a suite of **AI marketing tools for solopreneurs who
"hate marketing."** It grew via a well-known playbook of **free single-purpose generators** (marketing
strategy, buyer persona, value proposition, ad copy, idea validator, …) used as lead magnets, with a
paid **Marketing Strategy** product sold as a **one-time / lifetime** purchase (not a subscription).
Its differentiator over generic ChatGPT is that outputs are **personalized to a detailed profile of
your product** (customer, problem, differentiation, stage). It targets solo founders and indie hackers
who want expert-grade marketing output without a team. It is **UI-only — no documented public API.**

## Capabilities & automation surface

| Capability | What it produces | Automation surface |
|---|---|---|
| Marketing strategy generator | A tailored marketing plan for your product | UI-only |
| Buyer / user persona generator | Detailed target-customer personas | UI-only |
| Value proposition generator | Positioning / value-prop statements | UI-only |
| Business model generator | Business-model / monetization ideas | UI-only |
| Idea validator | A quick AI sanity-check of an idea | UI-only |
| Ad copy / marketing ideas | Ad and marketing copy + campaign ideas | UI-only |
| Pricing strategy | Pricing approach suggestions | UI-only |
| Action-plan generator | Step-by-step plan per generated idea | UI-only |

**Everything is UI-only.** No public API, no webhooks, no documented Zapier/Make connectors. The
generators run in the browser off the product profile you enter. (Tool lineup ~8 generators; exact set
changes — verify at founderpal.ai.)

## Pricing, limits & plan gates

*Best-effort from research (2026-07) — third-party quotes disagree; confirm at founderpal.ai.*

- **Free tools** — many single-purpose generators are free to try (the top-of-funnel lead magnets).
  Start here.
- **Paid Marketing Strategy product — one-time / lifetime, not a subscription.** Reported structures
  include a **per-strategy** purchase (~$69 for one) and an **unlimited / lifetime** deal (~$199), with
  plan names like **Idea / Founder / Agency**; more recently an **annual pass with credits**. These
  numbers are inconsistent across sources — treat all as best-effort.
- **No API rate limits** apply — there's no API. Usage limits (credits) are enforced in the product.
- Frame the buy decision as **"how many strategies/personas will I generate"** against a one-time fee,
  not a monthly cost.

## Integrations

- **Direction:** none programmatic — outputs are read/copied in the browser.
- **No native CRM / Zapier / Make connectors** are documented.
- The realistic "integration" is workflow: use FounderPal to draft the persona, positioning, and
  marketing plan, then execute in your own tools (site, email, ads) and validate demand separately.

## Data model

There is no public API and no documented response schema. A generated *result*, as shown in the UI, is
essentially structured marketing content — for example a persona:

```json
{
  "product": "A budgeting app for freelancers with irregular income",
  "persona": {
    "name": "Freelance Fiona",
    "demographics": "28–40, self-employed, variable monthly income",
    "goals": ["smooth out cash flow", "set aside taxes automatically"],
    "pains": ["feast-or-famine months", "surprise tax bills"],
    "objections": ["another subscription", "is my data safe"]
  }
}
```
<!-- ILLUSTRATIVE ONLY — FounderPal has no public API or documented schema; this represents UI output, not a real response contract. Do not code against it. -->

## Getting the most out of it (in place of quick-start API recipes)

There's no API, so "recipes" are usage patterns, not code:

1. **Fill the product profile richly before generating.** Give the specific customer, the exact
   problem, how you're different, and your stage. FounderPal's edge is personalization — thin input
   collapses it to generic ChatGPT output. Re-run variants and compare.
2. **Use it for the pitch, not the verdict.** Harvest the persona, value proposition, and objections
   to sharpen messaging; treat the generated marketing strategy as a hypothesis to test, and validate
   the persona against real customers.
3. **Chain into real validation and execution.** Take the sharpened positioning to a demand test
   (smoke-test landing page + pre-sale via `/sales-idea-validation`) and execute the plan in your own
   marketing tools. FounderPal drafts; the market decides.

## Automation reality (developer note)

- **No public API.** If a workflow needs programmatic strategy/persona generation, FounderPal is the
  wrong tool — it can't be called in a supported way.
- **Don't scrape the app.** Generators run behind the UI/credits; automating them is fragile and
  against the tool's intent.
- **Automate the demand signal instead.** Wire real behavior (landing-page conversion, waitlist growth,
  pre-sale revenue) into your dashboards — not an AI-generated strategy. See `/sales-idea-validation`.
