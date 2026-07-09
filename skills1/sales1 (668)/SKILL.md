---
name: sales-worthbuild
description: "WorthBuild (worthbuild.io) platform help — a cheap, fast AI startup-idea validator whose differentiator is built-in customer discovery: it scans Reddit, Hacker News, and X for real people already describing your problem and hands you ready-to-send outreach messages, alongside a full report (TAM/SAM/SOM sizing, competitor map, risk + unit-economics, a Go/Pivot/Stop verdict), a free auto-generated landing page + waitlist, a one-click pitch deck, and AI pivot suggestions. Use when running an idea through WorthBuild, interpreting its Go/Pivot/Stop verdict, using its 'Your First Customers' leads and outreach messages, understanding the one-time-per-report pricing and free monthly validation, or asking whether it has an API. UI-only, NO public API/webhooks/Zapier/MCP; the score is an AI opinion and the surfaced leads are interest, not validated demand. Do NOT use for the validate-before-building method or comparing validators (use /sales-idea-validation), or cold-emailing the surfaced leads (use /sales-cadence)."
argument-hint: "[describe what you need help with in WorthBuild]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
---

# WorthBuild Platform Help

WorthBuild (**worthbuild.io**) is a **cheap, fast AI startup-idea validator** whose distinctive job in
the validator market is **built-in customer discovery**. You describe your idea; in ~2 minutes it scans
public discussions (**Reddit, Hacker News, X/Twitter, forums**) for **real people already voicing the
problem** and returns them as **"Your First Customers"** — each with their pain point, an engagement
signal, and a **ready-to-send personalized outreach message** — alongside a **full validation report**
(TAM/SAM/SOM market sizing, a ~12-competitor map, risk assessment, unit economics, financial
projections, a week-by-week roadmap, and a **Go/Pivot/Stop** verdict). Extras: a **free auto-generated
landing page + waitlist**, a **one-click 10-slide pitch deck** (customizable, PDF export), **AI Pivot
Suggestions** if the idea scores low, and a **Discovery Hub** of problem discussions. It's priced
**one-time per report** with a **free monthly validation**, and is **UI-only — no public API**. Its niche:
of the validators, it's the one that hands you an actual **customer-conversation shortlist** — but a
surfaced lead is *interest*, not proof anyone will pay, and the verdict is still an AI opinion.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from WorthBuild?**
   - A) **Run/interpret a validation** — the Go/Pivot/Stop verdict, market sizing, competitor map, risks
   - B) Use the **"Your First Customers"** leads and the ready-to-send outreach messages
   - C) Understand the **pricing** — the free monthly validation vs the one-time per-report packs
   - D) Use a **downstream generator** — the free landing page + waitlist, the pitch deck, or pivot suggestions
   - E) Get the report **out / automate it** (export / API reality)
2. **What's the real question — "is this validated?" or "who do I talk to first?"** The verdict is an AI
   opinion; the surfaced leads are a conversation list, not confirmed demand — route the go/no-go in Step 2.
3. **If you're planning to contact the surfaced leads**, that's cold/warm outreach — not WorthBuild's job.
   Route to `/sales-cadence` (sequence) and `/sales-deliverability` (land in the inbox).

Skip-ahead: if the user wants the validate-before-building *method* or to rank validators across the
market, route to `/sales-idea-validation` immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| Comparing WorthBuild against other validators (Validator AI, IdeaProof, DimeADozen, Preuve…) | `/sales-idea-validation {question}` |
| Actually **cold-emailing / sequencing** the "First Customers" leads | `/sales-cadence {question}` |
| Making sure that outreach **lands in the inbox** (deliverability, warmup) | `/sales-deliverability {question}` |
| Deep **Reddit demand-signal** discovery / scoring as its own workflow | `/sales-trendseeker {question}` |
| Building the smoke-test / fake-door **landing page** (beyond WorthBuild's auto-generated one) | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer WorthBuild-specific questions using Step 3.

## Step 3 — WorthBuild platform reference

**Read `references/platform-guide.md`** for the full reference — how the validation engine and the
"Your First Customers" discovery work, what the full report contains, the Go/Pivot/Stop verdict, the
downstream generators (landing page + waitlist, pitch deck, pivot suggestions, Discovery Hub), the
one-time-per-report pricing and free monthly validation, the no-public-API automation reality, and how
it compares to the rest of the validator cluster.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Frame WorthBuild as "the validator that also hands you your first customers," not a proof of demand.**
  Its edge over pure-score validators is the **"Your First Customers"** list — a shortlist of real people
  already voicing the problem, with a ready-to-send message. That's genuinely useful: it's the
  customer-conversation rung of the evidence ladder handed to you. But a person complaining online is
  **interested, not committed** — the go/no-go still belongs to a real behavior test (a reply that turns
  into a call, a waitlist signup, a pre-sale), routed to `/sales-idea-validation`.
- **Treat the Go/Pivot/Stop verdict and every market number as an AI estimate, not evidence.** The
  verdict, TAM/SAM/SOM sizing, competitor map, unit economics, and financial projections are
  model-generated from a ~2-minute scan — keep the structured parts (competitor list, risks, positioning)
  to sharpen the pitch and **verify any figure against a primary source** before quoting it. If the idea
  scores low, read the **Pivot Suggestions** as hypotheses to re-test, not directives.
- **Vet the surfaced leads before you send anything, and don't blast the canned outreach.** The "First
  Customers" are AI-surfaced from public posts — **check each is a real, relevant person** (right problem,
  recent, not a bot) before contacting them, and **personalize** the ready-made message rather than
  sending it verbatim. Respect each platform's rules (Reddit/HN dislike cold DMs). Route the actual
  sequencing to `/sales-cadence` and inbox-landing to `/sales-deliverability`.
- **Whenever pricing comes up, state the model FIRST: WorthBuild is one-time per report with a free
  monthly validation — no subscription and no credits.** Then treat figures as best-effort: **one free validation per
  month** (full report, no card), a **single report** as a cheap one-time buy, and a **multi-report
  bundle** at a small discount. Point to worthbuild.io and flag every price as best-effort; note that
  re-validating a pivoted idea is another report.
- **There's no public API — don't plan an integration around it.** If asked to export or automate, say
  plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP** — it's a UI web app;
  the report, leads, landing page, and pitch deck are used/downloaded from the browser. If you need the
  demand signals scripted, pull them from source (a keyword-volume API, Google Trends, the Reddit API)
  instead — the thing worth automating is a real demand signal, not the verdict.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — WorthBuild is a young, low-cost tool with thin third-party review
coverage; verify pricing, the free-tier allowance, report depth, and the data sources at worthbuild.io.*

- **The verdict is an AI opinion, not demand.** Go/Pivot/Stop, market sizing, and financials are
  generated from a fast scan — a "Go" is a directional gut check, not proof strangers will pay.
- **"Your First Customers" are leads, not customers.** They're AI-surfaced from public posts — a
  complaint signals *interest*. Verify each person/post is real and relevant, and treat a reply or a
  waitlist signup (not the raw list) as the actual signal.
- **Don't send the canned outreach as-is.** The ready-made messages are starting drafts; personalize
  them and respect platform norms (Reddit/HN penalize spammy DMs) — route sequencing to `/sales-cadence`.
- **One-time per report + one free validation/month — and re-runs cost again.** No subscription; a
  pivoted idea is a new report. Confirm current pack pricing and the free allowance.
- **The auto-generated landing page is a starter, not the smoke test.** Use it to capture a waitlist, but
  the demand proof is what strangers *do* on it — for a purpose-built fake-door page use `/sales-funnel`.
- **No public API, no webhooks, no Zapier/Make/MCP.** UI web app — you can't script or batch-run it;
  download the report/deck manually or pull demand signals from source.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator landscape (use this to actually decide build-or-not; a surfaced lead and an AI score are not demand)
- `/sales-cadence` — Sequence and personalize outreach to the "First Customers" leads (WorthBuild finds them; cadence contacts them without spamming)
- `/sales-deliverability` — Make that outreach land in the inbox (warmup, SPF/DKIM/DMARC) rather than spam
- `/sales-trendseeker` — Reddit-based real-demand discovery + evidence scoring as its own workflow (contrast WorthBuild's leads-plus-report)
- `/sales-ideaproof` — IdeaProof platform help (a credit-based 120s validator that scores one idea and bundles plan/brand/logo/pitch/ads — a pure-score sibling without customer discovery)
- `/sales-preuve` — Preuve AI platform help (a source-linked validator that cites every claim across 50+ live sources — contrast WorthBuild's leads-first, cited-lightly report)
- `/sales-funnel` — Build the purpose-built smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "WorthBuild found 20 people with my problem — am I validated?"
**User says**: "WorthBuild gave me a 'Go' and a list of 20 people on Reddit who have this exact problem. Should I start building?"
**Skill does**: Credits the **"Your First Customers"** list as WorthBuild's real edge — a customer-conversation
shortlist handed to you — but reframes both the **Go verdict** (an AI opinion from a ~2-min scan) and the
leads (people who are *interested*, not committed) as directional, not demand. Prescribes the real test:
verify a handful of the leads are real/relevant, reach out *personally* (routed to `/sales-cadence` +
`/sales-deliverability`) to book conversations, and turn a waitlist signup or pre-sale into the go/no-go —
routed to `/sales-idea-validation` and `/sales-funnel`.
**Result**: The founder uses the leads as a head start on real conversations instead of treating the list as proof.

### Example 2: "Is the WorthBuild free validation enough, or do I pay?"
**User says**: "Do I need to pay WorthBuild or is the free one fine?"
**Skill does**: States the model first — **one-time per report with a free monthly validation, no
subscription** — and (best-effort) that the **free tier gives one full validation per month, no card**, so
a single idea is free to validate; the cheap **one-time single report** and the small-discount **bundle**
are for validating *more* ideas or pivots in the same month. Notes re-validating a pivoted idea is another
report, and points to worthbuild.io to confirm current pricing and the free allowance.
**Result**: The user validates their first idea free and only pays when they need to run several.

### Example 3: Can I pull WorthBuild's report into my CRM via an API? (developer/automation)
**User says**: "I want to auto-export WorthBuild's leads and report into my own database via API."
**Skill does**: States plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP** —
WorthBuild is a UI web app whose report, leads, landing page, and pitch deck are used/downloaded from the
browser, so there's no supported programmatic export. Suggests fallbacks: copy the report/leads manually,
or reconstruct the demand signals from source (the Reddit API, a keyword-volume API, Google Trends) and
automate a **real** demand signal instead of the verdict.
**Result**: The user avoids building on a non-existent API and picks a workable path to the underlying signal.

## Troubleshooting

### WorthBuild said "Go" and found me customers — does that mean it's validated?
**Symptom**: A "Go" verdict plus a list of real people with the problem, and the founder wants to start building.
**Cause**: The verdict is an **LLM opinion** from a fast scan, and the leads are **AI-surfaced from public
posts** — a complaint is interest, not willingness to pay.
**Solution**: Keep the structured outputs (competitor map, risks, positioning) to sharpen the pitch, verify
a sample of the leads are real/relevant, then earn a real verdict: contact them *personally* to book
conversations (`/sales-cadence`, `/sales-deliverability`), and put the go/no-go on a waitlist signup or
pre-sale (`/sales-funnel`, `/sales-idea-validation`).

### The "First Customers" leads look thin or off-target
**Symptom**: The surfaced people aren't quite the right audience, or some posts look old/irrelevant.
**Cause**: The discovery matches keywords in public discussions, so precision varies with how specific the
idea description is and how much the problem is discussed online.
**Solution**: Give WorthBuild a **more specific problem statement** (audience + concrete pain), re-run, and
**hand-filter** the list before outreach — discard bots, off-topic threads, and stale posts. Cross-check
demand with `/sales-trendseeker` (Reddit signal) and don't outreach anyone you haven't vetted.

### I want an API or a way to export/automate the report and leads
**Symptom**: Want to script WorthBuild or pull its report/leads into another system.
**Cause**: WorthBuild has no documented public API, webhooks, or iPaaS connectors — it's a UI web app.
**Solution**: Copy the report/leads and download the pitch deck (PDF) manually, or pull the underlying
signals from source (the Reddit API, a keyword-volume API, Google Trends) and automate a real demand
signal (landing-page analytics) instead. See `/sales-idea-validation`.
