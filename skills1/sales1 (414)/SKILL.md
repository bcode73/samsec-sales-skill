---
name: sales-personagen
description: "PersonaGen (personagen.app) platform help — an AI user-persona generator for founders, indie makers, marketers, and UX designers: answer a few questions about your product and it generates detailed personas (demographics, goals, challenges, motivations, frustrations, preferred channels, quotes) plus content-generation prompts, organized into multi-project workspaces and feature-wise sections. UI-only with no public API. Use when generating a user or buyer persona in PersonaGen, turning a short product description into a usable persona, organizing personas by project or product feature, deciding free vs paid, judging whether a generated persona is accurate, or asking whether it has an API or how to automate it. Do NOT use for the validate-before-building method or comparing persona/idea tools across the market (use /sales-idea-validation), or content strategy across tools (use /sales-content)."
argument-hint: "[describe what you need help with in PersonaGen]"
license: MIT
version: 1.0.0
tags: [sales, pre-launch, platform]
---

# PersonaGen Platform Help

PersonaGen (personagen.app) is an **AI user-persona generator** for founders, indie makers, marketers,
product managers, and UX/UI designers. Answer a few questions about your product, project, or company
and it generates **detailed user personas** — demographics, personality traits, goals, challenges,
motivations, frustrations, preferred channels, and representative quotes — plus **customized
content-generation prompts** you can reuse for copy. Personas are organized into **multiple projects**
and sorted into **product-based / feature-wise sections** so you can analyze an audience segment by
segment. It's a fast persona copilot, **not a substitute for real demand validation**, and it has **no
documented public API** (a UI web tool).

*Note: the live site was unreachable during research — details below are best-effort from third-party
sources; verify at personagen.app. The backlog listed `personagen.io`, which does not resolve; the
canonical domain is `personagen.app` (a related `personagen.net` also exists).*

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from PersonaGen?**
   - A) Generate a user/buyer persona for a product or project
   - B) Organize personas across projects or by product feature (feature-wise sections)
   - C) Understand the free tier vs the paid plan
   - D) Get more useful/tailored personas out of it (how to describe your audience)
2. **Do you have a specific product/audience description ready?** Output quality tracks the detail you give it.

Skip-ahead: if the user wants the validate-before-building *method* or to compare persona/idea tools
across the market, that's a `/sales-idea-validation` question — route in Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or comparing persona/idea tools across the market | `/sales-idea-validation {question}` |
| The free front-door / paid persona sibling that adds website-perception "Insights" | `/sales-instantpersonas {question}` |
| A dedicated AI idea validator (viability score/report) rather than persona generation | `/sales-validator-ai {question}` |
| Turning persona insights into a content plan across tools | `/sales-content {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer PersonaGen-specific questions using Step 3.

## Step 3 — PersonaGen platform reference

**Read `references/platform-guide.md`** for the full reference — the persona/projects/feature-wise
modules and what each produces, the persona field set, the free-vs-paid split and best-effort pricing,
how to describe your audience for the most useful personas, and the no-public-API automation reality.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Feed it a specific audience/product description — output quality tracks input.** A generated
  persona is only as good as the context behind it. Tell the user to describe a **specific customer,
  the exact problem, the product's differentiation, and current stage** rather than a one-line topic,
  then **re-run variants and compare**; a thin prompt yields a generic, could-be-anyone persona.
- **Tell the user what PersonaGen actually produces and to reuse the content-generation prompts.** Each
  persona comes back with **demographics** (age, location, occupation, income, education, family
  status), **personality traits, goals, challenges, motivations, frustrations, preferred channels,**
  and a **representative quote** — plus **content-generation prompts** tailored to that persona. Point
  the user to those prompts as the reusable output for writing on-message copy, not just the profile.
- **Treat every generated persona as an editable hypothesis, and always prescribe validating it
  against real customers.** The persona is an AI guess that can *sound* convincing while being
  invented — so in every answer, even a "how do I get a good persona?" one, tell the user to
  **validate it against a handful of real customers before building or messaging around it: interview
  target users about the last time they hit the problem, and watch what they actually do** (observed
  behavior beats stated intent). Keep the useful scaffolding (challenges, frustrations, channels,
  quotes) as a starting draft to confirm or discard against that real behavior.
- **Don't confuse a persona with validated demand.** PersonaGen can produce a polished persona for an
  audience that won't buy — if the real question is "should I build/ship this?", route to
  `/sales-idea-validation` for real signal (smoke test / pre-sale). Use the persona to sharpen the
  pitch; take the go/no-go from real behavior.
- **Use the projects + feature-wise organization to keep segments separate.** For a multi-feature or
  multi-audience product, have the user create a persona per segment/feature rather than one blended
  persona, so messaging and content prompts stay specific to each.
- **Present pricing as best-effort and start on the free tier.** PersonaGen launched free (beta) and
  advertises affordable tiered pricing — name the free tier first and tell the user to confirm current
  plans/limits at personagen.app before upgrading, since figures move and the live site was unreachable
  at research.
- **There's no public API — don't plan an integration around it.** If asked to automate or batch
  personas, say plainly there's **no documented public API, no webhooks, and no Zapier/Make**; it's a
  UI tool. Copy outputs manually, or for programmatic persona generation call an LLM API directly with
  your own prompt (see `references/platform-guide.md`).

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — the live site was unreachable at research; the tool lineup and
pricing move, so verify at personagen.app.*

- **A generated persona is not validated demand.** It'll happily describe a buyer for an audience that
  won't pay — pair it with a real demand test (`/sales-idea-validation`).
- **AI personas sound convincing even on thin data.** The model can invent demographics, income,
  motivations, and an ICP; validate the persona against real customers before betting on it.
- **Output quality depends on input depth.** A one-line prompt → generic persona; the specificity of
  your audience/product description is what makes the output useful.
- **No documented public API / webhooks / Zapier.** It's a web tool — don't plan integrations or batch
  jobs around it; automate with a direct LLM API call instead.
- **URL confusion.** `personagen.app` is canonical; the backlog's `personagen.io` does not resolve and
  a separate `personagen.net` ("Custom User Personas in minutes") also exists — confirm you're on the
  right one.
- **Pricing is best-effort and may be stale.** It launched free/beta with tiered plans promised;
  confirm current tiers and limits live before recommending an upgrade.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full persona/validator tool landscape (use this to actually decide build-or-not)
- `/sales-instantpersonas` — InstantPersonas / User Persona platform help (a sibling prompt-only persona generator that also adds website-perception "Insights" and competitor personas)
- `/sales-personadeck` — Personadeck platform help (a sibling prompt-only persona generator with an explicit User-vs-Negative persona-type choice, personality-trait predictions, and PDF-only export)
- `/sales-founderpal` — FounderPal platform help (broader solopreneur AI marketing suite that includes a buyer-persona generator)
- `/sales-content` — Content-marketing strategy across tools (turn persona insights into a content plan)
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Generate a user persona for a project
**User says**: "I'm building a habit-tracking app for busy parents — can PersonaGen build me a persona?"
**Skill does**: Points to the persona generator, stresses describing a **specific** customer (a
working parent of two who keeps abandoning habit apps by week three, say) with the exact problem and
differentiation so the output beats a generic template, and frames the resulting persona — challenges,
frustrations, channels, quotes — as an editable hypothesis to confirm with a handful of real parent
conversations before building messaging around it. Notes the free tier is the place to start.
**Result**: A tailored persona the founder validates against reality instead of a generic profile.

### Example 2: "PersonaGen's persona looks perfect — does that mean there's demand?"
**User says**: "The persona it generated matches my idea exactly. Is my idea validated now?"
**Skill does**: Separates a generated *persona* from validated *demand* — PersonaGen can describe a
convincing buyer for an audience that won't pay — and routes the build-or-ship decision to
`/sales-idea-validation` (smoke test + pre-sale), keeping the persona's challenges and objections as
pitch-sharpening input rather than a verdict.
**Result**: The founder gets real demand signal before building, using the persona for the pitch, not the go/no-go.

### Example 3: Can I automate PersonaGen via API? (developer/automation)
**User says**: "I want to generate personas for 30 product ideas automatically — what's PersonaGen's API?"
**Skill does**: States plainly there's **no documented public API, no webhooks, and no Zapier/Make**
(it's a UI tool), so there's no supported way to batch it; suggests copying outputs manually or calling
an LLM API directly with a persona prompt (see `references/platform-guide.md` for a cURL/Python
example) for programmatic generation, and notes the thing worth automating is a real demand signal, not
a generated persona — pointing to `/sales-idea-validation`.
**Result**: The user avoids building on a non-existent API and picks a workable path.

## Troubleshooting

### Persona feels generic / like plain ChatGPT
**Symptom**: The generated persona is vague and could describe almost anyone.
**Cause**: The audience/product prompt was thin — PersonaGen needs specific context to produce a
useful, differentiated persona.
**Solution**: Re-run with a rich description — specific customer, the exact problem, how the product
differs, current stage — and compare variants; the more context, the sharper and more usable the persona.

### "Is there an API?" / can't export or batch personas
**Symptom**: Looking for API docs, an export endpoint, or a way to batch-generate personas.
**Cause**: PersonaGen has no documented public API, webhooks, or Zapier/Make modules; it's a web tool.
**Solution**: Don't build an integration around it — copy outputs manually, or call an LLM API directly
with your own persona prompt for programmatic use (see `references/platform-guide.md`). Automate the
real demand signal instead. See `/sales-idea-validation`.

### Can't reach the site / not sure which domain is real
**Symptom**: personagen.io doesn't load, or there seem to be multiple PersonaGen sites.
**Cause**: `personagen.io` (the old backlog URL) does not resolve; the canonical app is
`personagen.app`, and a separate `personagen.net` also exists.
**Solution**: Use `personagen.app`. If it's unreachable, the tool may be in a beta/waitlist state —
confirm status before relying on it, and use a sibling generator (`/sales-instantpersonas`) or a direct
LLM prompt in the meantime.
