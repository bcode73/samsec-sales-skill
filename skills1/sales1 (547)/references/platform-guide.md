# SoloLaunch Platform Reference

## Overview

SoloLaunch (**sololaunch.app**) is an **AI startup builder / co-pilot for solo founders**: you enter a
one-line idea and it generates a **"startup foundation"** — company names, taglines, a logo and brand
identity, market analysis, an interactive timeline/roadmap, and marketing strategy playbooks — held in a
multi-project workspace with a canvas. It targets solo entrepreneurs, makers, and vibe coders who want a
fast starting kit without hiring out naming/branding/strategy. Its differentiator vs its idea-validation
siblings is **pricing model**: a low-cost **monthly subscription** (free Starter → paid Pro), not a
one-time purchase (FounderPal) or credit pack (IdeaProof, ReadySetLaunch). It is **UI-only — no documented
public API.**

> ⚠️ **Two different products share the name.** This guide covers **sololaunch.app** (the AI co-pilot). A
> separate product at **sololaunch.ai** is an AI-app **launch directory** ("Where solo builders launch AI
> apps" — free listing, community upvotes, a weekly newsletter). For submitting/listing/launching an app,
> that's `/sales-launch-directory`, not this skill.

## Capabilities & automation surface

| Capability | What it produces | Automation surface |
|---|---|---|
| Company name generator | Unique, memorable startup names | UI-only |
| Tagline generator | Compelling taglines / one-liners | UI-only |
| Logo & brand identity | Logo, color palette, brand look | UI-only (Starter tier watermarks the logo) |
| Market analysis | AI market-trend / opportunity summary | UI-only |
| Interactive timeline / roadmap | A step-by-step launch roadmap you can edit | UI-only |
| Marketing strategy / playbooks | Tailored marketing plan + growth strategy | UI-only |
| Multi-project workspace / canvas | Organizes assets across projects | UI-only |

**Everything is UI-only.** No public API, no webhooks, no documented Zapier/Make connectors. Generators run
in the browser off the idea you enter. (Module set changes — verify at sololaunch.app.)

## Pricing, limits & plan gates

*Best-effort from research (2026-07) — confirm at sololaunch.app; sources are thin.*

- **Free Starter — $0 (short trial window).** Gated: a small number of **name generations per 24h**
  (reported ~3/24h), **one tagline**, and a **watermarked logo**. Enough to try, not to ship.
- **Pro Launch — low-cost monthly subscription.** Reported ~**$4.99/month** (promo off a ~$15 list) or a
  discounted **annual** option (~$44.99/year off ~$90). Unlocks **unlimited generations**, complete asset
  packages, and all features. Treat all figures as best-effort.
- **This is a subscription, not one-time or credits.** Unlike FounderPal (one-time/lifetime) or
  IdeaProof/ReadySetLaunch (credit packs that don't expire), value here is "months of active use" — cancel
  when you've generated what you need.
- **No API rate limits** apply — there's no API. Usage caps are enforced in the product on the free tier.

## Integrations

- **Direction:** none programmatic — outputs are read/copied in the browser.
- **No native CRM / Zapier / Make connectors** are documented.
- The realistic "integration" is workflow: use SoloLaunch to draft the name, brand, timeline, and marketing
  plan, then execute in your own tools (site, email, ads) and validate demand separately.

## Data model

There is no public API and no documented response schema. A generated *result*, as shown in the UI, is
essentially structured startup content — for example a naming/branding output:

```json
{
  "idea": "A budgeting app for freelancers with irregular income",
  "names": ["FloatFund", "CashCadence", "SteadyStack"],
  "tagline": "Smooth out feast-or-famine months.",
  "brand": {
    "palette": ["#0E7C66", "#F4B400", "#1A1A2E"],
    "voice": "reassuring, practical, no-jargon"
  },
  "timeline": [
    {"phase": "Validate", "weeks": "1-2", "tasks": ["10 interviews", "smoke-test page"]},
    {"phase": "Build MVP", "weeks": "3-6", "tasks": ["core budgeting flow"]},
    {"phase": "Launch", "weeks": "7-8", "tasks": ["directory launch", "email list"]}
  ]
}
```
<!-- ILLUSTRATIVE ONLY — SoloLaunch has no public API or documented schema; this represents UI output, not a real response contract. Do not code against it. -->

## Getting the most out of it (in place of quick-start API recipes)

There's no API, so "recipes" are usage patterns, not code:

1. **Frame the idea richly before generating.** Give the specific customer, the exact problem, how you're
   different, and your stage. Thin input collapses the output to generic ChatGPT-grade names/branding.
   Re-run variants and compare.
2. **Use it for the assets, not the verdict.** Harvest the name shortlist, brand direction, positioning,
   and roadmap to move fast; treat the generated marketing strategy as a hypothesis to test, and validate
   the idea itself with real demand — not with the fact that a tool produced a polished kit.
3. **Chain into real validation and execution.** Take the sharpened positioning to a demand test
   (smoke-test landing page + pre-sale via `/sales-idea-validation`), and if you want a launch-day push,
   list on directories (`/sales-launch-directory`, including sololaunch.ai). SoloLaunch drafts; the market decides.

## Automation reality (developer note)

- **No public API.** If a workflow needs programmatic name/brand/strategy generation, SoloLaunch is the
  wrong tool — it can't be called in a supported way. Call an LLM API directly instead.
- **Don't scrape the app.** Generators run behind the UI/subscription gates; automating them is fragile and
  against the tool's intent.
- **Automate the demand signal instead.** Wire real behavior (landing-page conversion, waitlist growth,
  pre-sale revenue) into your dashboards — not an AI-generated startup foundation. See `/sales-idea-validation`.
