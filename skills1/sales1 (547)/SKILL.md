---
name: sales-sololaunch
description: "SoloLaunch (sololaunch.app) platform help — an AI startup builder / co-pilot that turns a one-line idea into a complete \"startup foundation\": generated company names and taglines, a logo and brand identity, market analysis, an interactive timeline/roadmap, and marketing strategy playbooks. Priced as a low-cost monthly subscription (not one-time or credits); a free Starter tier caps name generations, allows one tagline, and watermarks the logo. UI-only, no public API. Use when generating a startup name, tagline, logo, or brand identity, building a launch roadmap or interactive timeline, getting an AI marketing strategy for a solo project, deciding between its free Starter and paid Pro plan, or asking whether it has an API. Note: its AI-generated branding and strategy are a fast first draft, not validated demand. Do NOT use for the validate-before-building method or comparing idea-validation tools (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in SoloLaunch]"
license: MIT
version: 1.0.0
tags: [sales, pre-launch, platform]
---

# SoloLaunch Platform Help

SoloLaunch (**sololaunch.app**) is an **AI startup builder / co-pilot for solo founders**. You give it a
one-line idea and it generates a **"startup foundation"** — company names and taglines, a logo and brand
identity, market analysis, an **interactive timeline/roadmap**, and **marketing strategy playbooks** —
organized in a multi-project workspace. Its differentiator vs its idea-validation siblings is **pricing:
a low-cost monthly subscription** (free Starter → paid Pro), not one-time or credit-pack. It is a fast
asset generator, **not a substitute for real demand validation**, and it has **no documented public API**
(a UI tool).

> ⚠️ **Domain disambiguation.** The co-pilot is at **sololaunch.app**. A separate, unrelated product at
> **sololaunch.ai** is an AI-app *launch directory* ("Where solo builders launch AI apps"). If the user
> means the directory (submitting/listing an app, upvotes, weekly newsletter), that's a launch-directory
> question — route to `/sales-launch-directory`, not here.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from SoloLaunch?**
   - A) Generate a startup name, tagline, logo, or brand identity
   - B) Build a launch roadmap / interactive timeline, or get a marketing strategy
   - C) Understand the free Starter tier vs the paid Pro subscription (what's gated)
   - D) Get more useful/tailored output out of it (how to frame the idea input)
2. **Do you have a clear idea description ready?** Output quality tracks the detail you give it.
3. **Do you mean sololaunch.app (the co-pilot) or sololaunch.ai (the launch directory)?** If the latter,
   route to `/sales-launch-directory`.

Skip-ahead: if the user wants the validate-before-building *method* or to compare validators, that's a
`/sales-idea-validation` question — route in Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or comparing idea/startup-builder tools across the market | `/sales-idea-validation {question}` |
| Submitting/listing an app on **sololaunch.ai** (the launch directory), upvotes, launch-day exposure | `/sales-launch-directory {question}` |
| Building the actual **landing page / smoke test** the demand test runs on | `/sales-funnel {question}` |
| Content-marketing **strategy** across tools (SEO content, editorial, distribution) | `/sales-content {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer SoloLaunch-specific questions using Step 3.

## Step 3 — SoloLaunch platform reference

**Read `references/platform-guide.md`** for the full reference — the generator lineup (names, taglines,
logo/brand, market analysis, timeline, marketing strategy) and what each produces, the free-Starter-vs-
paid-Pro **subscription** split and best-effort pricing, how to frame the idea input for tailored output,
and the no-public-API automation reality.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Frame a rich idea input — output quality tracks input depth.** A one-line prompt yields generic
  names/branding/strategy; feed it a specific customer, the exact problem, and how it's different, then
  **re-run variants and compare**. Tell the user to treat every generated asset as an editable first draft.
- **Keep the assets, not the verdict — a generated "startup foundation" is NOT validated demand.**
  SoloLaunch will happily produce a name, logo, timeline, and marketing plan for an idea nobody wants. If
  the real question is "should I build this?", route to `/sales-idea-validation` and get real signal (a
  smoke test / pre-sale). Harvest its branding/positioning to sharpen the pitch; take the go/no-go from
  real behavior.
- **Model the pricing as a monthly subscription with two named tiers, and flag it as best-effort.**
  Whenever pricing or "is it worth it" comes up, **name both tiers explicitly**: a **free Starter** tier
  (gated — caps generations to e.g. a few names/24h, one tagline, and a **watermarked logo**) and a **paid
  Pro** tier (unlocks unlimited generations and full, unwatermarked asset packages). Contrast the model
  with siblings — unlike FounderPal (one-time/lifetime) or IdeaProof/ReadySetLaunch (credit packs),
  SoloLaunch is a **recurring monthly subscription** — so frame value as "how many months will I actively
  use it" against the monthly fee, and tell the user to confirm current tiers/prices at sololaunch.app.
- **There's no public API — don't plan an integration around it.** If asked to automate/export, say
  plainly there's no documented public API; it's a UI tool. Copy outputs manually or use a tool built for
  programmatic generation, and automate real signals (landing-page conversions), not generated assets.
- **Disambiguate the domain before answering.** If the user's task is submitting/listing an app or a
  launch-day directory push, they mean **sololaunch.ai** (the directory) — route to
  `/sales-launch-directory`, not this skill.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — the tool lineup and pricing move; verify at sololaunch.app.*

- **A generated "startup foundation" is not validated demand.** Names, logos, timelines, and marketing
  plans are AI assets — pair them with a real demand test (`/sales-idea-validation`).
- **Two SoloLaunches.** sololaunch.app = the AI co-pilot (this skill); sololaunch.ai = a separate AI-app
  launch directory (`/sales-launch-directory`). Don't conflate them.
- **Output quality depends on input depth.** A thin idea input → generic names/branding; the tailoring is
  the point, so frame a specific customer + problem + differentiation.
- **Pricing is a monthly subscription, not one-time or credits** — the free Starter tier gates generations
  (name-per-24h caps, one tagline, watermarked logo). Confirm live at sololaunch.app; treat prices as best-effort.
- **No documented public API.** It's a web tool; don't plan integrations around it.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator/builder landscape (use this to actually decide build-or-not)
- `/sales-founderpal` — FounderPal — a sibling solopreneur AI marketing/asset suite (one-time/lifetime pricing, not subscription)
- `/sales-ideaproof` — IdeaProof — a sibling that bundles validation + brand/logo/pitch/ads generators (credit-based)
- `/sales-launch-directory` — Launching on directories (incl. sololaunch.ai, the AI-app launch directory)
- `/sales-funnel` — Build the smoke-test / landing page the demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Generate a name, logo, and brand for a new idea
**User says**: "I have a budgeting app for freelancers — can SoloLaunch give me a name, logo, and branding?"
**Skill does**: Points to SoloLaunch's name/tagline/logo/brand-identity generators, stresses framing the
idea richly (specific customer, exact problem, differentiation) so the output beats a generic prompt, and
frames every asset as an editable first draft. Notes the free Starter tier caps generations and watermarks
the logo, so unlimited output needs paid Pro.
**Result**: A tailored starting brand kit the founder refines, with clear expectations on the free-tier limits.

### Example 2: "SoloLaunch built my whole startup foundation — am I validated?"
**User says**: "SoloLaunch generated a name, timeline, and marketing strategy for my idea. Does that mean it's validated?"
**Skill does**: Separates a generated *foundation* from validated *demand* — SoloLaunch can produce a full
kit for an idea nobody wants — and routes the build-or-not decision to `/sales-idea-validation` (smoke test
+ pre-sale), keeping SoloLaunch's branding/positioning as pitch-sharpening input.
**Result**: The founder gets real demand signal before building, using SoloLaunch for the assets, not the verdict.

### Example 3: Can I automate SoloLaunch via API? (developer/automation)
**User says**: "I want to generate names and brand kits for 20 ideas from a script — what's SoloLaunch's API?"
**Skill does**: States plainly there's **no documented public API** (it's a UI tool), so there's no
supported way to batch it; suggests copying outputs manually or using a tool built for programmatic
generation (or calling an LLM API directly), and notes the thing worth automating is a real demand signal,
not generated assets — pointing to `/sales-idea-validation`.
**Result**: The user avoids building on a non-existent API and picks a workable path.

## Troubleshooting

### Output feels generic / like plain ChatGPT
**Symptom**: The generated names, branding, or marketing strategy are vague and could fit any product.
**Cause**: The idea input was thin — SoloLaunch's tailoring needs detail to beat a generic model.
**Solution**: Re-run with a rich description — specific customer, the exact problem, how the solution
differs, current stage — and compare variants; the more context, the more tailored the output.

### Hit a limit / logo is watermarked
**Symptom**: Ran out of name generations, only got one tagline, or the logo has a watermark.
**Cause**: Those are **free Starter tier** gates — SoloLaunch bills a monthly subscription and reserves
unlimited generations and clean assets for paid Pro.
**Solution**: If you'll use it actively, weigh the low monthly Pro fee against how many months you'll use
it (it's a subscription, not one-time/credits); confirm the current tiers/limits at sololaunch.app.

### "Is there an API?" / wrong SoloLaunch
**Symptom**: Looking for API docs, or confused between sololaunch.app and sololaunch.ai.
**Cause**: The co-pilot (sololaunch.app) has no documented public API; sololaunch.ai is a *different*
product — an AI-app launch directory.
**Solution**: Don't build an integration around the co-pilot — copy outputs manually. If the task is
listing/launching an app on the directory, that's `/sales-launch-directory`. Automate real demand signals
(landing-page analytics) instead. See `/sales-idea-validation`.
