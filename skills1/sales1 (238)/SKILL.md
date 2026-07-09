---
name: sales-ideatwister
description: "IdeaTwister (ideatwister.com) platform help — a pay-per-run AI idea validator that twists ONE rough idea into 10–25 angle-variations and ranks every pivot across five commercial dimensions (buyer urgency, market proof, solo executability, revenue speed, defensibility), returning an interactive dashboard with GTM sketches and 30-day validation plans. Use when running an idea through IdeaTwister, deciding which *version* of your idea to build, choosing the pricing tier that gets you enough alternatives, interpreting its pivot scores, understanding the one-time pay-per-run pricing (no subscription), or asking whether it has an API to export the dashboard. UI-only, NO public API/webhooks/Zapier/MCP; the pivot scores are AI estimates, not validated demand. Do NOT use for the validate-before-building method or comparing validators across the market (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in IdeaTwister]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
---

# IdeaTwister Platform Help

IdeaTwister (**ideatwister.com**) is a **pay-per-run AI idea validator with a distinctive job: it
picks the best *angle*.** You give it **one** rough business idea; it runs a fleet of specialised AI
agents in parallel, pulls live web research, **"twists" the idea into 10–25 angle-variations (pivots)**,
scores every pivot across **five commercial dimensions** — **buyer urgency, market proof, solo
executability, revenue speed, defensibility** — and returns an **interactive HTML dashboard** (your
"workspace") with the top picks fully developed: a GTM sketch, "$100K math," and a 30-day validation
plan. It's **priced per run (one-time, no subscription)** and is **UI-only — no public API**. Its niche
in the validator market: use it once you already have *an* idea and need to know **which version of it to
build**, not to discover an idea from scratch and not as proof anyone will pay.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from IdeaTwister?**
   - A) **Run/interpret a twist** — the 10–25 pivots and their five-dimension scores
   - B) Decide **which version/angle** of your idea to build (the "pick the best pivot" job)
   - C) Choose a **pricing tier** — which run gets you enough alternatives / deep validations
   - D) Understand the **Business Growth Run** (growth opportunities for an existing business)
   - E) Get the dashboard **out / automate it** (export / API reality)
2. **Do you already have one idea, or are you still hunting for an idea?** IdeaTwister is for when you
   *have* one idea and want its best angle — hunting for an idea from scratch is discovery
   (`/sales-idea-validation` routes to discovery catalogs).
3. **What's the real question — "which angle should I build?" or "is this validated?"** A ranked pivot is
   still an AI opinion, not demand; the go/no-go belongs to a real test — route in Step 2.

Skip-ahead: if the user wants the validate-before-building *method* or to rank validators across the
market, route to `/sales-idea-validation` immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| Comparing IdeaTwister against other validators (Validator AI, IdeaProof, RebeccAi, DimeADozen…) | `/sales-idea-validation {question}` |
| **Discovering** an idea from scratch (no idea yet — browse a catalog of opportunities) | `/sales-idea-validation {question}` (routes to discovery catalogs) |
| Deep **Reddit demand-signal** discovery / scoring as its own workflow | `/sales-trendseeker {question}` |
| Building the smoke-test / fake-door **landing page** to test the winning pivot | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand on the chosen angle | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer IdeaTwister-specific questions using Step 3.

## Step 3 — IdeaTwister platform reference

**Read `references/platform-guide.md`** for the full reference — the twist engine and the five scoring
dimensions, what each tier delivers (Quick Idea Check / Validate This Idea / Find My Best Direction /
Business Growth Run) and the alternatives-per-run and deep-validation counts, the one-time pay-per-run
pricing and auto-refund-on-failure, the interactive-dashboard output, the no-public-API automation
reality, and how it compares to the rest of the validator cluster.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Frame IdeaTwister as the "pick the best angle" tool, not a one-idea scorer or a discovery catalog.**
  Its distinctive job is to take ONE idea, generate 10–25 *variations/pivots*, and rank them — so it fits
  the founder who already has an idea and is unsure *which version* to build. If the user has no idea yet,
  that's discovery (a browsable opportunity catalog); if they want a single as-is score, a plain
  validator is simpler. Route cross-market comparison and the method to `/sales-idea-validation`.
- **A ranked pivot is an AI opinion, not validated demand — keep the structure, discard the verdict.**
  The five-dimension scores (buyer urgency, market proof, solo executability, revenue speed,
  defensibility) rank the *model's* guesses. Keep the winning pivot's structured outputs (the GTM sketch,
  the competitor/market read, the 30-day validation plan) to sharpen the pitch, but take the go/no-go from
  a real behavior test (smoke test / pre-sale) on the chosen angle, routed to `/sales-idea-validation`.
- **Whenever pricing or a tier comes up, state the business model FIRST: IdeaTwister is one-time
  pay-per-run with NO subscription — you pay per run, no recurring charge.** Then match the tier to how
  many alternatives the user needs, and treat every figure as best-effort: the cheapest run scores only
  the original idea; the mid tier adds ~10 alternatives; the top tier generates ~25 and fully validates
  the 2 strongest; the Business Growth Run is for an existing business's growth opportunities + a 90-day
  plan. Point to ideatwister.com/pricing and flag every price/count as best-effort. Note that a run which
  **fails before delivering the workspace auto-refunds** while completed runs don't — so frame the spend as
  "cost per attempt," and that iterating an idea means paying per re-run.
- **Verify every market figure — the twist pulls live web research but the numbers are AI estimates.**
  Market-size, "$100K math," and pivot scores are generated, not audited; check any figure against a
  primary source before acting on it.
- **There's no public API — don't plan an integration around it.** If asked to export or automate, say
  plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP** — it's a UI web app and
  the deliverable is an interactive dashboard you view/copy (outputs are yours to use commercially). If you
  need the signals scripted, pull them from source (a keyword-volume API, Google Trends, Reddit) instead.
  The thing worth automating is a real demand signal, not a pivot score.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — IdeaTwister is a young pay-per-run tool with thin third-party
review coverage; verify pricing, per-tier alternative/validation counts, and the refund policy at
ideatwister.com.*

- **It ranks angles — a top pivot is not validated demand.** The five-dimension score orders the model's
  own guesses; a "winning" pivot still needs a real-behavior test (smoke test / pre-sale) before you build.
- **"Pick the best angle" ≠ "find an idea."** IdeaTwister needs one seed idea to twist; it is not a
  discovery catalog (VentureVault, StartupIdeasDB, Ideagrape) for founders with no idea yet.
- **One-time pay-per-run, priced by depth — and re-runs cost again.** Cheapest tier scores only the
  original; more alternatives and deep validations cost more; iterating an idea means paying per run.
  Failed runs auto-refund, completed runs don't. Confirm current tiers/counts.
- **Market figures and "$100K math" are AI estimates.** The twist pulls live web research, but sizing and
  revenue math are generated — verify every number against a primary source.
- **Output is an interactive dashboard, not a file/API.** The deliverable is a web workspace (yours to use
  commercially); there's no structured export beyond viewing/copying it.
- **No public API, no webhooks, no Zapier/Make/MCP.** UI web app — you can't script or batch-run it; copy
  the dashboard manually or pull demand signals from source.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator/discovery landscape (use this to actually decide build-or-not; a ranked pivot is not demand)
- `/sales-ideagrape` — Ideagrape platform help (a discovery+validation hybrid — browse a market-scored idea database *and* validate one; contrast IdeaTwister, which twists ONE idea into ranked pivots)
- `/sales-ideaproof` — IdeaProof platform help (a credit-based 120s validator that scores one idea and bundles a plan/brand/logo/pitch/ads — a single-idea sibling to IdeaTwister's multi-pivot ranking)
- `/sales-rebeccai` — RebeccAi platform help (the cheapest single-idea evaluate-plus-plan combo — contrast IdeaTwister's angle-ranking job)
- `/sales-funnel` — Build the smoke-test / fake-door landing page to test the winning pivot for real
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand on the chosen angle
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "I have one idea but I'm not sure which version to build"
**User says**: "I want to build a tool for freelancers but there are a dozen ways to angle it — can IdeaTwister help me pick?"
**Skill does**: Frames IdeaTwister as exactly the **"pick the best angle"** tool — it twists the one idea
into 10–25 pivots and ranks them across the five dimensions (buyer urgency, market proof, solo
executability, revenue speed, defensibility), so the founder can compare angles side by side. Recommends
the tier that generates enough alternatives (the top tier fully validates the 2 strongest), then stresses
that the winning pivot is an **AI ranking, not demand** — the next step is a smoke test / pre-sale on the
chosen angle, routed to `/sales-funnel` and `/sales-idea-validation`.
**Result**: The founder gets a ranked shortlist of angles and a concrete plan to prove the top one for real.

### Example 2: "Which IdeaTwister tier should I pay for?"
**User says**: "Is the $29 run enough or do I need the $59 one?"
**Skill does**: Explains the **one-time pay-per-run** tiers (best-effort): the cheapest scores only the
original idea, the mid tier adds ~10 alternatives, the top tier generates ~25 and **fully validates the 2
strongest**, and the Business Growth Run is for an existing business's growth opportunities + a 90-day
plan. Advises picking by how many *angles* you want ranked, notes **failed runs auto-refund** but
completed runs don't (so budget per attempt and per re-run), and points to ideatwister.com/pricing to
confirm current counts.
**Result**: The user picks the tier matched to how many alternatives they need, with clear eyes on the per-run cost.

### Example 3: Can I export IdeaTwister's dashboard via an API? (developer/automation)
**User says**: "I want to pull IdeaTwister's pivot scores into my own database via API."
**Skill does**: States plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP** —
it's a UI web app whose deliverable is an **interactive dashboard** you view/copy (outputs are yours to
use commercially), so there's no supported programmatic export. Suggests the fallbacks: copy the workspace
you can see into your own store (mind their terms), or reconstruct the signals from source (a
keyword-volume API, Google Trends, Reddit). Notes the thing worth automating is a real demand signal, not
a pivot score.
**Result**: The user avoids building on a non-existent API and picks a workable path to the signal.

## Troubleshooting

### IdeaTwister ranked a pivot highly — does that mean it's validated?
**Symptom**: A "winning" angle scored high across the five dimensions and the founder wants to start building.
**Cause**: The score ranks the **model's own guesses** about the pivots; it's an AI opinion with live web
research behind it, not evidence a stranger will pay.
**Solution**: Keep the winning pivot's structured outputs (GTM sketch, competitor/market read, 30-day
validation plan) to sharpen the pitch, then put the go/no-go on a real demand test — a smoke-test landing
page with a pre-set conversion bar, then a pre-sale — routed to `/sales-funnel` and `/sales-idea-validation`.

### I have no idea yet — can IdeaTwister find me one?
**Symptom**: The user wants to be handed an idea, not twist one they already have.
**Cause**: IdeaTwister needs a **seed idea** to generate variations from; it's a "pick the best angle"
tool, not a discovery catalog.
**Solution**: For finding an idea from scratch, use a discovery catalog (VentureVault, StartupIdeasDB,
Ideagrape) via `/sales-idea-validation`; bring the shortlisted idea back to IdeaTwister to rank its angles.

### I want an API or a way to export/automate the dashboard
**Symptom**: Want to script IdeaTwister or pull its pivot scores/dashboard into another system.
**Cause**: IdeaTwister has no documented public API, webhooks, or iPaaS connectors — it's a UI web app and
the deliverable is an interactive dashboard.
**Solution**: Copy the visible workspace into your own store (outputs are yours; mind their terms), or pull
the underlying signals from source (a keyword-volume API, Google Trends, Reddit). Automate a real demand
signal (landing-page analytics) instead. See `/sales-idea-validation`.
