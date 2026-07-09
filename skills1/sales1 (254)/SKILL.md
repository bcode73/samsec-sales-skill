---
name: sales-instantpersonas
description: "InstantPersonas (instantpersonas.com) platform help — a free-to-try AI buyer/user-persona generator for marketers, founders, and solopreneurs, and its free sibling User Persona (userpersona.dev): describe your product or audience and it generates named personas (demographics, goals, pain points), plus website-perception \"Insights\" (how a persona sees your page), competitor-persona discovery, and SEO content ideas. Also ships free no-signup micro-tools (headline analyzer, keyword/hashtag finders). UI-only with no public API. Use when generating a buyer or user persona, turning a thin description into a usable persona, using its website-perception or competitor-persona analysis, deciding free vs paid, judging whether a generated persona is accurate, or asking whether it (or userpersona.dev) has an API. Do NOT use for the validate-before-building method or comparing persona/idea tools across the market (use /sales-idea-validation), or content strategy across tools (use /sales-content)."
argument-hint: "[describe what you need help with in InstantPersonas]"
license: MIT
version: 1.1.0
tags: [sales, marketing, pre-launch, platform]
---

# InstantPersonas Platform Help

InstantPersonas (instantpersonas.com) is an **AI buyer/user-persona generator** for marketers,
founders, and solopreneurs. Describe your product or audience and it generates **named, detailed
personas** (demographics, goals, pain points, motivations), plus website-perception **"Insights"**
(how a given persona would perceive your page), **competitor-persona discovery** (which personas a
competitor targets), niche/market opportunities, and SEO content ideas built from those personas. It
also ships a set of **free no-signup micro-tools** (headline analyzer, Google keyword finder,
Instagram hashtag finder, guest-post finder, share-preview optimizer, topical authority). It's a fast
persona/marketing copilot, **not a substitute for real demand validation**, and it has **no
documented public API** (a UI tool).

The same maker also runs **User Persona (userpersona.dev)** — a **free, no-signup, single-tool front
door** that does just the core persona generation (describe a product → get one editable persona,
save-as-image only). It's the free tier of this same product family; InstantPersonas is the upgraded
version that adds Insights, competitor personas, SEO ideas, and the paid plan. Treat questions about
"User Persona" / userpersona.dev as the same tool at its free entry point — the guidance below applies
identically (userpersona.dev also has no API and no account/export beyond a screenshot).

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from InstantPersonas?**
   - A) Generate a buyer/user persona for a product or campaign
   - B) Use website-perception "Insights" or competitor-persona analysis
   - C) Understand the free micro-tools vs the paid persona plan
   - D) Get more useful/tailored personas out of it (how to describe your audience)
2. **Do you have a clear product/audience description ready?** Output quality tracks the detail you give it.

Skip-ahead: if the user wants the validate-before-building *method* or to compare persona/idea tools,
that's a `/sales-idea-validation` question — route in Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or comparing persona/idea tools across the market | `/sales-idea-validation {question}` |
| A dedicated AI idea validator (viability score/report) rather than persona generation | `/sales-validator-ai {question}` |
| The broader solopreneur AI marketing suite (strategy, value prop, business model) | `/sales-founderpal {question}` |
| Content-marketing **strategy** across tools (SEO content, editorial, distribution) | `/sales-content {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer InstantPersonas-specific questions using Step 3.

## Step 3 — InstantPersonas platform reference

**Read `references/platform-guide.md`** for the full reference — the persona/insights/competitor
modules and what each produces, the free micro-tools inventory, the free-vs-paid split and best-effort
pricing, how to describe your audience for the most useful personas, and the no-public-API automation
reality.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Feed it a specific audience/product description — output quality tracks input.** A named persona
  is only as good as the context behind it. Tell the user to describe a **specific customer, the exact
  problem, the product's differentiation, and current stage** rather than a one-line topic, then
  **re-run variants and compare**; a thin prompt yields a generic, could-be-anyone persona.
- **Treat every generated persona as an editable hypothesis, not a finding.** The persona is an AI
  guess that can *sound* convincing while being invented — have the user **validate it against real
  customers** (interviews, observed behavior) before designing or messaging around it. Keep the
  useful scaffolding (pain points, objections, channels) as a starting draft to confirm or discard.
- **Don't confuse a persona (or "Insights") with validated demand.** InstantPersonas can produce a
  polished persona for an audience that won't buy — if the real question is "should I build/ship
  this?", route to `/sales-idea-validation` for real signal (smoke test / pre-sale). Use the persona
  to sharpen the pitch; take the go/no-go from real behavior.
- **Use website-perception "Insights" and competitor-persona output as directional prompts, not proof.**
  "How persona X sees your page" is an AI simulation — treat it as a checklist of things to test with
  real users (a quick hallway test or session recording), not a verdict on your copy.
- **Present pricing as best-effort and start with the free tools.** The paid persona plan is a
  low-cost monthly/annual subscription (best-effort — confirm at instantpersonas.com; there's a short
  trial and a money-back guarantee), while a limited persona run and the **free no-signup micro-tools
  (headline analyzer, Google keyword finder, Instagram hashtag finder, guest-post finder, share-preview
  optimizer)** are free — name a couple of those free tools and tell the user to start free, only
  upgrading for unlimited personas/insights.
- **There's no public API — don't plan an integration around it.** If asked to automate or batch
  personas, say plainly there's **no documented public API**; it's a UI tool. Copy outputs manually,
  or for programmatic persona generation call an LLM API directly with your own prompt.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — the tool lineup and pricing move; verify at instantpersonas.com.*

- **A generated persona is not validated demand.** It'll happily describe a buyer for an audience that
  won't pay — pair it with a real demand test (`/sales-idea-validation`).
- **AI personas sound convincing even on thin data.** The model can invent demographics, motivations,
  and an ICP; validate the persona against real customers before betting on it.
- **Output quality depends on input depth.** A one-line prompt → generic persona; the specificity of
  your audience/product description is what makes the output useful.
- **"Insights" / competitor personas are simulations.** How a persona "perceives" your page or what a
  competitor "targets" is an AI guess — confirm with real user testing, don't treat it as measured.
- **No documented public API.** It's a web tool; don't plan integrations or batch jobs around it —
  the same holds for the free **userpersona.dev** front door.
- **userpersona.dev is the free tier of the same product, not a different tool.** Same maker; it does
  only the core persona generation, no account, save-as-image only. Don't treat it as a separate
  vendor — the persona-is-a-hypothesis / no-API / feed-rich-input guidance is identical.
- **Pricing is best-effort.** Confirm current plans/trial/guarantee live; start with the free tools.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full persona/validator tool landscape (use this to actually decide build-or-not)
- `/sales-personagen` — PersonaGen platform help (a sibling prompt-only AI persona generator — detailed personas + content prompts organized into projects/feature-wise sections; UI-only/no API)
- `/sales-personadeck` — Personadeck platform help (a sibling prompt-only AI persona generator with an explicit User-vs-Negative persona-type choice, personality-trait predictions, and PDF-only export; UI-only/no API)
- `/sales-founderpal` — FounderPal platform help (broader solopreneur AI marketing suite — strategy, persona, value prop, idea validator)
- `/sales-validator-ai` — Validator AI platform help (a dedicated free AI idea validator — the score-and-report sibling)
- `/sales-content` — Content-marketing strategy across tools (turn persona insights into a content plan)
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Generate a buyer persona for a project
**User says**: "I'm launching a budgeting app for freelancers — can InstantPersonas build me a buyer persona?"
**Skill does**: Points to the persona generator, stresses describing a **specific** customer (freelance
designers who miss quarterly taxes, say) with the exact problem and differentiation so the output beats
a generic template, and frames the resulting persona as an editable hypothesis to confirm with a handful
of real freelancer conversations before building messaging around it. Notes a limited run is free.
**Result**: A tailored persona the founder validates against reality instead of a generic profile.

### Example 2: "InstantPersonas says my audience loves this — is it validated?"
**User says**: "The persona and Insights look great for my idea. Does that mean there's demand?"
**Skill does**: Separates a generated *persona* from validated *demand* — InstantPersonas can describe a
buyer for an audience that won't pay, and "Insights" is an AI simulation — and routes the build-or-ship
decision to `/sales-idea-validation` (smoke test + pre-sale), keeping the persona/objections as
pitch-sharpening input.
**Result**: The founder gets real demand signal before building, using the persona for the pitch, not the verdict.

### Example 3: Can I automate InstantPersonas via API? (developer/automation)
**User says**: "I want to generate personas for 40 product ideas automatically — what's InstantPersonas's API?"
**Skill does**: States plainly there's **no documented public API** (it's a UI tool), so there's no
supported way to batch it; suggests copying outputs manually or calling an LLM API directly with a
persona prompt for programmatic generation, and notes the thing worth automating is a real demand
signal, not a generated persona — pointing to `/sales-idea-validation`.
**Result**: The user avoids building on a non-existent API and picks a workable path.

## Troubleshooting

### Persona feels generic / like plain ChatGPT
**Symptom**: The generated persona is vague and could describe almost anyone.
**Cause**: The audience/product prompt was thin — InstantPersonas needs specific context to produce a
useful, differentiated persona.
**Solution**: Re-run with a rich description — specific customer, the exact problem, how the product
differs, current stage — and compare variants; the more context, the sharper and more usable the persona.

### "Is there an API?" / can't export or batch personas
**Symptom**: Looking for API docs, an export endpoint, or a way to batch-generate personas.
**Cause**: InstantPersonas has no documented public API; it's a web tool.
**Solution**: Don't build an integration around it — copy outputs manually, or call an LLM API directly
with your own persona prompt for programmatic use. Automate real demand signals (landing-page
analytics) instead. See `/sales-idea-validation`.

### Not sure if the paid plan is worth it
**Symptom**: Deciding between the free micro-tools/limited run and the paid persona subscription.
**Cause**: The persona plan is a low-cost subscription; quotes and trial terms vary by source and change.
**Solution**: Start with the free tools and a limited persona run; upgrade only if you need unlimited
personas/insights, and confirm the current price, trial, and money-back terms at instantpersonas.com first.
