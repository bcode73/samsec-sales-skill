---
name: sales-readysetlaunch
description: "ReadySetLaunch (readysetlaunch.ai) platform help — an AI startup-idea validator built to interrogate, not flatter. Its Launch Control walks founders through 13 questions across 7 pillars (problem, customer, demand, differentiation, execution, distribution, monetisation), surfacing the gaps in weak answers instead of handing out an inflated score, grounded in a database of failed, unicorn, and acquired startups. Deliberately slow (30–45 min/idea), anti-gaslighting, credit-based, no subscription. Use when running an idea through ReadySetLaunch / Launch Control, interpreting its pillar-level gaps and launch-readiness report, comparing its interrogation model against score-in-seconds validators like IdeaProof or Validator AI, deciding whether credit packs are worth it, or asking whether it has an API to export reports. UI-only, no public API. Do NOT use for the validate-before-building method or comparing validators (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in ReadySetLaunch]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
---

# ReadySetLaunch Platform Help

ReadySetLaunch (readysetlaunch.ai) is an **AI startup-idea validator built to interrogate, not flatter**.
Its core product, **Launch Control**, walks a founder through **13 structured questions across 7 pillars**
(problem clarity, target customer, demand signal strength, differentiation, execution feasibility,
distribution readiness, monetisation viability). Each question breaks into plain-English sub-prompts that
show what a good answer looks like; on weak answers it **surfaces the specific gap** and coaches you to
close it — rather than emitting a single feel-good score. Every signal is graded against a **database of
real startup outcomes** (failed, successful, unicorn, acquired). It's **deliberately slow** (~30–45 min
per idea — "30 minutes on purpose"), explicitly **anti-gaslighting** (no engineered encouragement, no
hallucinated confidence), and **credit-based with no subscription**. It is a **UI tool — no documented
public API.** It also publishes competitor **review pages** (`/compare/{tool}/review/`) and a **startup
case database** (`/cases/`).

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from ReadySetLaunch?**
   - A) Run an idea through Launch Control and interpret the pillar-level gaps / launch-readiness report
   - B) Understand the 7-pillar / 13-question method and how the "surface the gap" scoring works
   - C) Understand the credits system — free credits, packs, no subscription — and whether it's worth it
   - D) Export or automate the report (API / integration reality)
2. **What's the real question — "is this idea worth building?" or "how do I use this tool?"** If it's the
   go/no-go decision itself, that's `/sales-idea-validation` (a validator's output is a gut check, not
   demand) — route in Step 2.

Skip-ahead: if the user wants the validate-before-building *method* or to compare validators across the
market, that's a `/sales-idea-validation` question — route immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| A full **cross-market comparison** of validators (ranking IdeaProof, Validator AI, WorthBuild, DimeADozen… to pick one) — but answer a quick ReadySetLaunch-vs-X *how-they-differ* inline first (Step 4) | `/sales-idea-validation {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer ReadySetLaunch-specific questions using Step 3.

## Step 3 — ReadySetLaunch platform reference

**Read `references/platform-guide.md`** for the full reference — the 7 pillars and 13-question structure,
how the gap-surfacing scoring differs from a single score, the failure/exit case database it grades
against, the credit-and-packs pricing (no subscription), the review/case content it publishes, and the
no-public-API automation reality.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Frame it as the anti-inflation validator — the value is the gaps, not a score.** Unlike
  score-in-seconds tools (IdeaProof, Validator AI) that hand out a high number (medians run ~78/100),
  Launch Control is built to **surface where your answers are weak** across the 7 pillars. Tell the user
  the useful output is **the specific gaps and the pillar-level signal**, not a pass/fail — its whole
  pitch is "no AI gaslighting," so read it for what it flags, not for reassurance.
- **When asked how it compares to a fast-score validator, give the model-level contrast inline first, then offer the cross-market route.** If the user asks ReadySetLaunch vs IdeaProof / Validator AI (or "is it worth it over X"), answer the *how-they-differ* directly: ReadySetLaunch **interrogates across 7 pillars over ~30–45 min and surfaces gaps**, whereas a fast-score tool like IdeaProof **produces a score in seconds and bundles a broader pre-launch toolkit** (plan/brand/logo/deck/ads). Tell the user to pick by **rigor-vs-speed**, not by free-credit count — then offer `/sales-idea-validation` for a full validator-market comparison. Don't just route the question away.
- **It's still an AI opinion — the go/no-go is a real demand test.** Even a rigorous, database-grounded
  interrogation is a **structured gut check, not proof of demand**. A "strong signal" across pillars does
  not mean strangers will pay. Tell the user to take the pillar gaps as a **sharpening tool** and put the
  actual go/no-go on a **smoke test or pre-sale** — route the decision to `/sales-idea-validation` and the
  build to `/sales-funnel`.
- **Set expectations on the time cost — that's the point.** It deliberately takes **~30–45 minutes per
  idea** and makes you write real answers; it's not a 120-second score. If the user wants a fast
  throwaway number, this is the wrong tool; if they want to be forced to think, it's the right one.
- **Present pricing as best-effort and credit-based with no subscription.** Best-effort: **3 free credits
  (no card)**, then **one-time packs (from ~£14.99)**, and **credits never expire** — there is **no
  monthly plan**. Prices move and packs/credit counts aren't fully published, so tell the user to
  **confirm current packs and per-idea credit cost at readysetlaunch.ai/pricing** rather than treating
  these figures as fixed. Model cost as "how many ideas will I run," not a recurring fee.
- **There's no public API — don't plan an integration around it.** If asked to export or automate, say
  plainly there's **no documented public API, no webhooks, no Zapier/Make** — it's a UI tool. The
  workable fallbacks: **copy/save the launch-readiness report manually** from the app, and if they need
  validation scripted, use a tool built for programmatic use. The thing actually worth automating is the
  real signal (landing-page conversions), not the report — route that to `/sales-funnel`.
- **Distinguish the product from its review/case content.** ReadySetLaunch also publishes competitor
  *reviews* (`/compare/…`) and a *startup case database* (`/cases/`). If the user is reading one of those
  pages, note it's the vendor's own comparison content (it positions Launch Control favourably) — useful
  context, not a neutral benchmark.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — ReadySetLaunch's pillars, credit packs, and pricing move; verify at readysetlaunch.ai.*

- **It surfaces gaps, it doesn't validate.** By design there's no single confidence score to celebrate —
  the output is *where your thinking is weak* across the 7 pillars. A "strong signal" is still an AI
  judgement, not demand; follow it with a real-behavior test.
- **It's slow on purpose (~30–45 min/idea).** This is a feature, not a bug — if a user expects a
  120-second score they'll bounce. Set the expectation up front.
- **Credit-based, no subscription.** You buy one-time packs (best-effort from ~£14.99); credits never
  expire and there's **no** monthly plan. Model cost as ideas-run, not a recurring fee. Confirm packs at
  readysetlaunch.ai/pricing — exact credit-per-idea counts aren't fully published.
- **No documented public API, no webhooks, no Zapier/Make.** It's a web tool — you can't script or export
  it programmatically; copy/save outputs manually.
- **`/compare/` and `/cases/` pages are the vendor's own content.** The competitor reviews and case
  database live on ReadySetLaunch's site and position Launch Control favourably — treat as vendor
  comparison, not a neutral source.
- **Grounding data is a curated database, not live scraping.** Signals are graded against a knowledge base
  of past startup outcomes — strong for pattern-matching to known failures/exits, but it's not real-time
  market demand.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator landscape (use this to actually decide build-or-not; a validator's output is a gut check, not demand)
- `/sales-ideaproof` — IdeaProof platform help (the score-in-120s + pre-launch-suite contrast to ReadySetLaunch's interrogation model)
- `/sales-validator-ai` — Validator AI platform help (a free score-and-report validator — the fast-score sibling)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "ReadySetLaunch flagged gaps in my demand and distribution pillars — is my idea dead?"
**User says**: "Launch Control said my demand-signal and distribution answers were weak. Should I drop the idea?"
**Skill does**: Explains the flagged gaps are the *point* — the tool surfaces where the thinking is thin
(here: no evidence anyone wants it, no plan to reach them), not a verdict. Tells the user to treat the two
weak pillars as a to-do list (go get demand evidence, name a distribution channel) and to settle the
actual go/no-go with a real test — a smoke-test landing page or pre-sale — via `/sales-idea-validation`,
not by re-running the questionnaire until the gaps disappear.
**Result**: The founder uses the gaps to sharpen the plan and gets a real go/no-go from stranger behavior.

### Example 2: How do the credits work, and is it worth it vs IdeaProof? (pricing / comparison)
**User says**: "ReadySetLaunch gives 3 free credits with no subscription. How does that compare to IdeaProof's credits, and which should I use?"
**Skill does**: Lays out ReadySetLaunch as credit-based with **no subscription** (best-effort: 3 free
credits no card, one-time packs from ~£14.99, credits never expire) and contrasts the *model*, not just
price — ReadySetLaunch **interrogates across 7 pillars in ~30–45 min** and surfaces gaps, whereas IdeaProof
scores in ~120s and bundles brand/logo/deck assets. Recommends ReadySetLaunch when the goal is to pressure-
test thinking and IdeaProof when the goal is fast breadth, and tells the user to confirm current packs at
readysetlaunch.ai/pricing.
**Result**: The user picks by what they actually need (rigor vs speed/assets), not by the free-credit count.

### Example 3: Can I export or automate ReadySetLaunch reports? (developer/automation)
**User says**: "I want to run 20 ideas through ReadySetLaunch and pull the launch-readiness reports into a spreadsheet via API."
**Skill does**: States plainly there's **no documented public API, no webhooks, no Zapier/Make** — it's a
UI tool, so there's no supported way to batch or export programmatically. Suggests copying/saving each
report manually, or using a tool built for programmatic validation if scripting is essential, and notes the
thing worth automating is a real demand signal (landing-page conversions), not a generated report —
pointing to `/sales-idea-validation` and `/sales-funnel`.
**Result**: The user avoids building on a non-existent API and picks a workable path.

## Troubleshooting

### "It didn't give me a score — just a list of gaps"
**Symptom**: The user expected a single viability number and got pillar-level gap feedback instead.
**Cause**: By design, Launch Control **surfaces gaps rather than emitting a feel-good score** — that's the
anti-gaslighting positioning.
**Solution**: Read the gaps as the deliverable. Close the weak pillars one at a time, then take the go/no-go
to a real demand test (smoke test / pre-sale) via `/sales-idea-validation` — don't re-answer until the
gaps vanish, which just games the tool.

### "This took 40 minutes — I wanted a quick check"
**Symptom**: The process felt slow compared to a 120-second validator.
**Cause**: ReadySetLaunch is **deliberately slow** (~30–45 min/idea) — the friction is the feature.
**Solution**: If the user wants a fast throwaway number, a score-in-seconds tool (IdeaProof, Validator AI)
fits better — route via `/sales-idea-validation`. If they want to be forced to think through the 7 pillars,
ReadySetLaunch is the right tool; budget the time.

### "I want an API / to export the report automatically"
**Symptom**: Wants to script ReadySetLaunch or pull reports into another system.
**Cause**: ReadySetLaunch has **no documented public API, webhooks, or iPaaS connectors** — it's a web tool.
**Solution**: Copy/save the launch-readiness report manually, or use a tool intended for programmatic use;
automate a real demand signal (landing-page analytics) instead. See `/sales-idea-validation`.
