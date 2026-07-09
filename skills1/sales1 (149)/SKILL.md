---
name: sales-dimeadozen
description: "DimeADozen (dimeadozen.ai) platform help — an AI startup-idea validation report generator for first-time founders, indie hackers, and makers, sold as a one-time purchase you keep forever (no subscription, no expiring credits): a free 4-dimension idea score, then a paid multi-section or 200+ page build-or-don't-build report with a named competitor set, unit-economics/retention math, and a marketed 800+ source citations. Use when running an idea through DimeADozen, interpreting its idea score or report, deciding if the paid Entrepreneur report is worth it, sanity-checking whether its citations and competitor benchmarks fit your niche, understanding the one-time pricing vs credit/subscription rivals, or asking whether it has an API to export reports (public UI-only; API is Enterprise/custom only). Do NOT use for the validate-before-building method or comparing validators across the market (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in DimeADozen]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
---

# DimeADozen Platform Help

DimeADozen (dimeadozen.ai) is an **AI startup-idea validation report generator**. You paste an idea and
get a free **4-dimension idea score** (Market / Validation / Execution / Differentiation), then can buy a
**keep-forever report** — a **Starter** (7 sections + 3 comparable companies) or a **200+ page
Entrepreneur** report with a named competitor set, unit-economics/retention math, a risk register, and a
clear **build-or-don't-build** verdict. Its differentiators vs sibling validators are the **one-time
purchase model** (no subscription, credits never expire) and a marketed **800+ URL citations** — though
that citation claim and its competitor benchmarks are **disputed** (see Gotchas). It's a **UI web app**:
there's **no public API** — API access exists only on the custom Enterprise tier. A report is an **LLM
opinion, not demand**.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from DimeADozen?**
   - A) Run an idea through the **free idea score** and interpret the 4 dimensions
   - B) Decide whether the paid **Starter vs Entrepreneur** report is worth buying
   - C) Interpret a report you already bought (comp-set, unit economics, the verdict)
   - D) Understand the **one-time pricing** (vs credit/subscription rivals) or the refund guarantee
   - E) Export / automate reports, or wire it into your stack (API reality)
2. **What's the real question — "is THIS idea worth building (go/no-go)?" or "how do I use DimeADozen?"**
   If it's the decision itself, that's `/sales-idea-validation` (a report is not demand) — route in Step 2.

Skip-ahead: if the user wants the validate-before-building *method* or to compare validators across the
market, that's a `/sales-idea-validation` question — route immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| Comparing DimeADozen against other validators (Preuve, Validator AI, IdeaProof, Informly…) | `/sales-idea-validation {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |
| Reddit-based **real-demand discovery** as its own workflow | `/sales-trendseeker {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer DimeADozen-specific questions using Step 3.

## Step 3 — DimeADozen platform reference

**Read `references/platform-guide.md`** for the full reference — the free idea score vs the paid report
tiers, what each tier includes, the one-time/keep-forever pricing and the 14-day guarantee, the
disputed 800+-citation and comp-set-relevance issues, the no-public-API automation reality (Enterprise
custom API/white-label only; no webhooks/Zapier/MCP), and how to get data out of a report.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Treat the report as a sharpening tool, not the decision.** The idea score and the report are an
  **LLM opinion, not demand** — DimeADozen produces a confident, structured, often *optimistic* report
  for almost any idea. Tell the user to **keep the structured parts** (competitor/comp-set, risk
  register, unit-economics framing, GTM angle, investor-memo skeleton) to sharpen the pitch and **take
  the go/no-go from a real behavior test** (smoke test / pre-sale), routing the real test to
  `/sales-idea-validation`.
- **Sanity-check the comp-set and citations for relevance — don't trust them at face value.** Reviewers
  report **niche ideas benchmarked against irrelevant giants** (e.g. a small newsletter compared to
  Etsy/Airbnb/Uber) and dispute whether the marketed **800+ citations** are actually verifiable
  source links. Tell the user to **open a sample of the cited sources and check each comparable is a
  real, relevant competitor** before quoting any market-size or retention number; verify figures
  against a primary source.
- **Frame the pricing as one-time / keep-forever and best-effort.** DimeADozen's differentiator is
  **one-time purchase, no subscription, credits never expire** (free score → Starter → Entrepreneur →
  a multi-report pack → custom Enterprise). Present all specific prices as **best-effort — confirm at
  dimeadozen.ai** — and note the **14-day money-back guarantee** if the user is deciding whether to buy.
- **On "is the big report worth it?" — anchor value on decision-usefulness, not page count.** A 200+
  page report is not more valid than a short one; steer the user to buy the tier only if they'll use the
  structured outputs to sharpen the pitch, and remind them the verdict still needs a real demand test.
- **Weigh the one-time model against how often they'll re-run.** Because each report is a separate
  purchase, a founder who re-validates the same idea across several pivots may pay repeatedly — if
  they'll iterate a lot, compare against credit-pack (IdeaProof, ReadySetLaunch) or lower-cost
  per-report/subscription rivals (Informly, Preuve) via `/sales-idea-validation`.
- **There's no public API — don't plan an integration around it.** If asked to export or automate, say
  plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP** on the self-serve
  plans; **API access and white-label exist only on the custom Enterprise tier** (contact sales). Then
  give the user **two concrete moves**: (1) the workable path today — **download/copy the report and
  parse it yourself** (there's no supported self-serve export); and (2) **redirect the automation effort
  to a real demand signal** — explicitly tell them to instrument **landing-page conversions from a smoke
  test** and wire *that* into their CRM/warehouse, because the conversion event (not the AI report) is
  what's worth automating. Route the demand-signal build to `/sales-funnel` and `/sales-idea-validation`.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — DimeADozen's pricing, report scope, and citation claims move; verify at dimeadozen.ai.*

- **The report is an LLM opinion, not demand.** A confident "build" verdict and a high idea score
  validate nothing on their own — follow with a real-behavior test (smoke test / pre-sale).
- **Reports read optimistic.** Independent reviewers note the output can feel like feel-good
  encouragement; keep the structured parts, discard the verdict.
- **Comp-set relevance is inconsistent.** Niche ideas have been benchmarked against irrelevant giants
  (Etsy/Airbnb/Uber for a small newsletter) — check each comparable is a real, relevant competitor.
- **The "800+ citations" claim is disputed.** Marketing touts source-linked claims, but critics report
  reports without verifiable clickable sources — open and check a sample before quoting any figure.
- **Pricing is one-time / keep-forever but best-effort.** Free score → Starter → Entrepreneur → multi-
  report pack → custom Enterprise; no subscription, credits never expire; **14-day money-back
  guarantee**. Confirm current numbers on the site.
- **No public API on self-serve plans.** API access and white-label are **Enterprise/custom only**; no
  webhooks, Zapier/Make, or MCP — get data out by downloading/parsing the report.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator landscape (use this to actually decide build-or-not; a report is not demand)
- `/sales-preuve` — Preuve AI platform help (source-linked validator citing every claim across 50+ live sources; lower-cost per-report + a monitoring tier — a citations-you-can-verify alternative)
- `/sales-ideaproof` — IdeaProof platform help (credit-based 120s validation + pre-launch suite — a credit-model alternative to DimeADozen's one-time report)
- `/sales-informly` — Informly platform help (per-report PDF validation bundle — a lower-cost per-report alternative)
- `/sales-validator-ai` — Validator AI platform help (free conversational validator + score — a free-first alternative)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "DimeADozen scored my idea high and said build it — should I?"
**User says**: "I ran my idea through DimeADozen, got a strong score and a 'build' verdict. Good to go?"
**Skill does**: Reframes the score and verdict as an **LLM opinion, not demand** — the report reads
optimistic and can "validate" almost anything. Tells the user to keep the structured parts (comp-set,
risk register, unit-economics, GTM angle) to sharpen the pitch and earn a real verdict with a smoke test
to a pre-set conversion threshold, then a pre-sale — routing the real test to `/sales-idea-validation`
and the landing page to `/sales-funnel`.
**Result**: The founder gets a go/no-go from stranger behavior, using the report's structure, not its verdict.

### Example 2: "Is the 200+ page Entrepreneur report worth $129, and are the citations real?"
**User says**: "Should I pay for the big DimeADozen report? It claims 800+ citations."
**Skill does**: Anchors value on **decision-usefulness, not page count**, and frames pricing as one-time
/ keep-forever, best-effort (with the 14-day money-back guarantee). Warns the **citation claim is
disputed** and that niche ideas can get **irrelevant comparables**, so the user should open a sample of
sources and confirm each competitor is real and relevant before trusting any number. Suggests comparing
the one-time model against credit/subscription rivals via `/sales-idea-validation` if they'll re-run per pivot.
**Result**: The user buys (or skips) with clear eyes and knows to audit the comp-set and sources.

### Example 3: Can I pull DimeADozen reports into my CRM via an API? (developer/automation)
**User says**: "I want to auto-export DimeADozen reports into our data warehouse via API."
**Skill does**: States plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP**
on self-serve plans — **API access and white-label are Enterprise/custom only** (contact sales), so
there's no supported self-serve way to export programmatically. Suggests the workable path: download/copy
the report and parse it yourself, and automate a real demand signal (landing-page analytics) instead.
Routes the demand pipeline thinking to `/sales-idea-validation`.
**Result**: The user avoids building on a non-existent self-serve API and picks a workable path.

## Troubleshooting

### The report is glowing but I don't trust it
**Symptom**: A confident, upbeat report with a high score and a "build" verdict that feels too easy.
**Cause**: The report is an LLM opinion that pattern-matches to plausible encouragement — reviewers note
it reads optimistic and can "validate" almost anything.
**Solution**: Keep the structured outputs (comp-set, risks, unit economics, positioning), discard the
verdict, and earn a real one — a smoke test to a pre-set conversion threshold, then a pre-sale — via
`/sales-idea-validation`.

### My niche idea was compared to Etsy/Airbnb/Uber
**Symptom**: The comp-set benchmarks a small/niche idea against giant, irrelevant companies.
**Cause**: The comparable-company selection is inconsistent for niche ideas, and the marketed "800+
citations" may not all be verifiable, relevant sources.
**Solution**: Manually vet the comp-set — open a sample of the cited sources and confirm each comparable
is a real, relevant competitor before quoting any market-size or retention figure; verify numbers against
a primary source. Cross-check demand with `/sales-trendseeker`.

### I want an API or a way to export/automate the reports
**Symptom**: Want to script DimeADozen or push reports into another system.
**Cause**: DimeADozen has **no public API, webhooks, or iPaaS connectors** on self-serve plans; API
access and white-label are **Enterprise/custom only** (contact sales).
**Solution**: Download/copy the report and parse it yourself; there's no supported self-serve export.
Automate a real demand signal (landing-page analytics) instead. See `/sales-idea-validation`.
