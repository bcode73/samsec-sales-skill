---
name: sales-ideaproof
description: "IdeaProof (ideaproof.io) platform help — an AI startup-idea validation and pre-launch suite that scores an idea in ~120s across 50+ criteria (viability score, GO/NO-GO verdict, TAM/SAM/SOM market sizing, competitor SWOT) and bundles a business-plan generator, brand strategy, logo/visual identity, pitch deck, and multi-platform ad creatives — all on a credit-based, no-subscription model (free 90 credits; €19.99–99.99 packs; credits never expire). Use when running an idea through IdeaProof, interpreting its viability score and GO/NO-GO verdict, understanding the per-feature credit costs, deciding between the free credits and paid packs, or asking whether it has an API to export or automate reports. Note: UI-only, NO documented public API. Do NOT use for the tool-agnostic validate-before-building method or comparing idea validators across the market (use /sales-idea-validation), or building the smoke-test landing page itself (use /sales-funnel)."
argument-hint: "[describe what you need help with in IdeaProof]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
---

# IdeaProof Platform Help

IdeaProof (ideaproof.io) is an **AI startup-idea validation and pre-launch suite** — "test your idea
in 120s." It scores an idea across **50+ criteria** (a 100-point **viability score** + a **GO/NO-GO**
verdict, TAM/SAM/SOM market sizing, competitor SWOT, risks) and then bundles the rest of a pre-launch
kit: an investor-ready **business plan**, **brand strategy** (12 Jungian archetypes), **logo/visual
identity**, **pitch deck**, and **multi-platform ad creatives**. It runs a **multi-model** ensemble
(Claude, GPT, Gemini, Grok) with live web scraping, on a **credit-based, no-subscription** model
(free 90 credits, then €19.99–99.99 packs; credits never expire). It's a fast idea-analysis tool and
starter-asset generator — **not a substitute for real demand validation** — and it has **no
documented public API** (a UI tool).

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from IdeaProof?**
   - A) Run an idea through it and interpret the viability score / GO-NO-GO verdict
   - B) Understand the credit system — free 90 credits, per-feature costs, which pack to buy
   - C) Use its downstream generators (business plan, brand, logo, pitch deck, ad creatives)
   - D) Automate or export the reports (API / integration reality)
2. **What's the real question — "is this idea worth building?" or "how do I use this tool?"** If it's
   the go/no-go decision, that's `/sales-idea-validation` (a score is not demand) — route in Step 2.

Skip-ahead: if the user wants the validate-before-building *method* or to compare validators across
the market, that's a `/sales-idea-validation` question — route immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| Comparing IdeaProof against other AI validators (Validator AI, WorthBuild, DimeADozen…) | `/sales-idea-validation {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |
| Turning the generated ad creatives into a real **content/ad** program | `/sales-content {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer IdeaProof-specific questions using Step 3.

## Step 3 — IdeaProof platform reference

**Read `references/platform-guide.md`** for the full reference — the module lineup and what each
produces, the credit costs per feature and the free-vs-paid pack split, how the viability score and
GO/NO-GO verdict are built (and why they run high), the multi-model + live-scrape data pipeline, and
the no-public-API automation reality.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Treat the viability score as a directional gut check, not demand — and know it runs high.** The
  score is a multi-model **LLM opinion** (independent reviews put the median around ~78/100, i.e. it
  passes most ideas). Tell the user to **keep the structured outputs** (competitor SWOT, risks,
  market-size framing, positioning) to sharpen the pitch, and take the **GO/NO-GO from real behavior**
  — a smoke test or pre-sale — not from the score. Route the real test to `/sales-idea-validation`.
- **Read the sourcing critically before trusting the numbers.** IdeaProof markets "50+ authoritative
  sources" and "89% accuracy," but its own report footer has cited only ~5 sources and the accuracy
  claim has **no published methodology**. Tell the user to treat TAM/SAM/SOM and financial projections
  as **AI estimates to verify**, and to click through whatever citations exist rather than quoting the
  numbers as fact.
- **Budget the credits against the whole journey, not one feature.** Everything is credit-priced
  (validation ~40, market analysis ~100, business plan ~100, brand ~50, logo/visual ~150, marketing
  suite ~250, pitch deck ~120). The **free 90 credits ≈ ~2 full validations**, not the "4" the
  marketing math implies. Have the user decide which downstream assets they actually need before
  buying a pack — and note packs are **one-time (no subscription)** and **credits never expire**.
  Pricing/credit costs move, so tell the user to **confirm current prices and per-feature credit
  costs on ideaproof.io** (third-party quotes disagree) rather than treating these figures as fixed.
- **Use it for starter assets, then replace them with tested ones.** The generated brand, logo, pitch
  deck, and ad creatives are fast **first drafts** — fine to launch a smoke test with, but the copy
  and positioning that survive are the ones that convert. Push real ad/landing testing to
  `/sales-content` and `/sales-funnel`; don't treat the generated marketing suite as a finished GTM.
- **There's no public API — don't plan an integration around it.** If asked to automate or export,
  say plainly there's **no documented public API, no webhooks, no Zapier/Make**; it's a UI tool (the
  advertised OpenRouter integration is IdeaProof's **internal** model routing, **not** a developer
  API to build on). Give the user the two workable fallbacks: (1) **download/copy the report
  manually** from the app, and (2) **use a tool built for programmatic validation** if they need it
  scripted. Then point out the thing actually worth automating is the real signal (landing-page
  conversions), not the generated report — route that real test to `/sales-idea-validation`
  (decision) and `/sales-funnel` (build the page).

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — IdeaProof's credit costs, packs, and feature lineup move; verify at ideaproof.io.*

- **The viability score runs high and is not demand.** Independent reviews put the median near ~78/100
  — a "feel-good" pass rate. A high score validates nothing; follow it with a real-behavior test.
- **"50+ sources / 89% accuracy" is marketing, not a verified benchmark.** The report footer has shown
  only ~5 sources and there's no published accuracy methodology — treat market sizing as AI estimates.
- **Free-tier math is misleading.** 90 free credits ≈ ~2 full validations, not the "4" implied; each
  downstream asset (plan, brand, logo, pitch deck, marketing suite) costs more credits on top.
- **"Six jobs, none deep."** Doing validation + plan + brand + logo + ads means less depth on any one;
  the validation itself is shallower than a validation-only tool. Use it for breadth, verify depth.
- **No documented public API, no webhooks, no Zapier/Make.** It's a web tool — you can't script or
  export it programmatically; copy/download outputs manually.
- **Credit-based, not a subscription.** You buy packs; credits never expire — but there's no monthly
  plan, so model cost as "how many assets will I generate," not a recurring fee.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator landscape (use this to actually decide build-or-not; a score is not demand)
- `/sales-validator-ai` — Validator AI platform help (a dedicated free AI idea validator — the score-and-report sibling)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-content` — Turn the generated ad creatives into a real content/ad program
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "IdeaProof gave my idea 82/100 — should I build it?"
**User says**: "IdeaProof scored my idea 82 and said GO. Is it validated?"
**Skill does**: Explains the score is a multi-model **LLM opinion that runs high** (median ~78/100, so
a GO is common) and validates nothing on its own. Tells the user to keep the competitor SWOT, risks,
and positioning to sharpen the pitch, then route the real go/no-go to `/sales-idea-validation` — a
smoke test or pre-sale where a stranger takes an action — rather than trusting the score.
**Result**: The founder gets real demand signal before building, using IdeaProof's structure, not its verdict.

### Example 2: How do the credits and free tier actually work?
**User says**: "IdeaProof says 90 free credits = 4 validations, but I ran out fast. What's going on and which pack should I buy?"
**Skill does**: Breaks down the per-feature credit costs (validation ~40, market ~100, plan ~100,
brand ~50, logo ~150, marketing suite ~250, pitch deck ~120), so 90 credits ≈ ~2 full validations, not
4. Advises deciding which downstream assets are actually needed before buying, and notes packs are
one-time (no subscription) with credits that never expire — confirm current prices on ideaproof.io.
**Result**: The user picks a pack sized to what they'll generate instead of overbuying.

### Example 3: Can I export or automate IdeaProof reports? (developer/automation)
**User says**: "I want to run 25 ideas through IdeaProof and pull the reports into a spreadsheet via API."
**Skill does**: States plainly there's **no documented public API, no webhooks, no Zapier/Make** — it's
a UI tool, so there's no supported way to batch or export programmatically. Suggests downloading/copying
reports manually or using a tool built for programmatic validation, and notes the thing worth automating
is a real demand signal (landing-page conversions), not a generated report — pointing to `/sales-idea-validation`.
**Result**: The user avoids building on a non-existent API and picks a workable path.

## Troubleshooting

### The viability score seems inflated / everything I test passes
**Symptom**: Multiple ideas all score in the high 70s–80s with a GO verdict.
**Cause**: The score is a multi-model LLM opinion that trends optimistic (independent reviews put the
median near ~78/100); it's a directional gut check, not evidence of demand.
**Solution**: Stop treating the score as the decision. Keep the structured outputs (competitors, risks,
positioning) and run a real demand test — smoke test or pre-sale — via `/sales-idea-validation`.

### The market-size / financial numbers don't have sources
**Symptom**: TAM/SAM/SOM and projections are stated with few or no clickable citations.
**Cause**: IdeaProof markets "50+ sources" but reports have cited only ~5, and figures are largely
AI-generated estimates.
**Solution**: Treat the numbers as hypotheses to verify against primary sources (Statista, Crunchbase,
your own bottom-up math) before quoting them in a plan or pitch.

### Ran out of free credits faster than expected
**Symptom**: The 90 free credits disappeared after ~2 runs despite "4 validations" marketing.
**Cause**: Each feature is credit-priced and a full journey (validation + market + plan + assets) costs
far more than one validation; 90 credits ≈ ~2 full validations.
**Solution**: Decide which downstream assets you actually need before spending, and size any paid pack
to that. Packs are one-time and credits never expire — confirm current pricing on ideaproof.io.

### Looking for an API or export/automation
**Symptom**: Want to script IdeaProof or pull reports into another system.
**Cause**: IdeaProof has no documented public API, webhooks, or iPaaS connectors; it's a web tool.
**Solution**: Download/copy outputs manually or use a tool intended for programmatic use; automate a
real demand signal (landing-page analytics) instead. See `/sales-idea-validation`.
