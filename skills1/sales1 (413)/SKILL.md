---
name: sales-personadeck
description: "Personadeck (personadeck.io) platform help — an AI customer-persona generator that turns a short audience/product description into a professionally-styled persona: demographics, behaviors, motivations, preferred channels, and personality-trait predictions (practical-vs-emotional, introvert-vs-extrovert). Pick a persona type — User Persona or Negative Persona (for skeptics/non-buyers) — with editable card labels, multilingual generation, and PDF export; UI-only with no public API. Use when generating a buyer or user persona in Personadeck, choosing a User vs Negative persona, editing labels or exporting a persona to PDF, comparing Free vs Basic/Medium/Pro tiers, judging whether a generated persona is accurate or just repackages your input, or asking whether it has an API or how to automate it. Do NOT use for the validate-before-building method or comparing persona/idea tools across the market (use /sales-idea-validation), or content strategy across tools (use /sales-content)."
argument-hint: "[describe what you need help with in Personadeck]"
license: MIT
version: 1.0.0
tags: [sales, pre-launch, platform]
---

# Personadeck Platform Help

Personadeck (personadeck.io, app at `app.personadeck.io`) is an **AI customer-persona generator** for
marketers, marketing agencies, product managers, and founders. Describe your audience or product and it
returns a **professionally-styled persona card** — demographics, behaviors, motivations, preferred
channels, and **personality-trait predictions** (practical-vs-emotional, introvert-vs-extrovert). You
first pick a **persona type**: a **User Persona** (align a product with the people you want) or a
**Negative Persona** (map the skeptics/non-buyers you want to *avoid* or win over). Output has
**editable card labels**, a **multilingual UI** (English, French, German, Spanish) with persona
**generation in any language** on higher plans, and **PDF export**. It's a fast persona copilot, **not a
substitute for real demand validation**, and it has **no documented public API** (a UI web tool).

*Note: the homepage often 404s to the app (`app.personadeck.io`) and details below are best-effort from
third-party sources (Capterra, AppSumo, GetApp) — verify live. Pricing is in EUR.*

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from Personadeck?**
   - A) Generate a buyer/user persona for a product or audience
   - B) Decide between a **User Persona** and a **Negative Persona**
   - C) Edit labels / export a persona to PDF
   - D) Understand the Free vs Basic/Medium/Pro tiers (and the AppSumo lifetime deal)
   - E) Get more useful/accurate personas out of it (how to describe your audience)
2. **Do you have a specific product/audience description ready?** Output quality tracks the detail you give it.

Skip-ahead: if the user wants the validate-before-building *method* or to compare persona/idea tools
across the market, that's a `/sales-idea-validation` question — route in Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or comparing persona/idea tools across the market | `/sales-idea-validation {question}` |
| A sibling prompt-only persona generator (detailed personas + content prompts, projects) | `/sales-personagen {question}` |
| A sibling generator that adds website-perception "Insights" + competitor personas | `/sales-instantpersonas {question}` |
| A broader solopreneur AI marketing suite that also generates personas | `/sales-founderpal {question}` |
| Turning persona insights into a content plan across tools | `/sales-content {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer Personadeck-specific questions using Step 3.

## Step 3 — Personadeck platform reference

**Read `references/platform-guide.md`** for the full reference — the persona-type choice (User vs
Negative), the persona field set and personality-trait predictions, the multilingual/PDF-export and
editable-label surface, the Free/Basic/Medium/Pro split and best-effort EUR pricing plus the AppSumo
lifetime deal, how to describe your audience for the most useful personas, and the no-public-API
automation reality with an LLM-API workaround.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Feed it a specific audience/product description — output quality tracks input.** A generated persona
  is only as good as the context behind it, and reviewers specifically fault Personadeck for
  *repackaging* thin input. Tell the user to describe a **specific customer, the exact problem, the
  product's differentiation, and current stage** rather than a one-line topic, then **re-run variants
  and compare**; a thin prompt yields a generic, could-be-anyone persona.
- **Pick the persona type deliberately — User vs Negative.** A **User Persona** models the audience you
  *want* (to align product and messaging); a **Negative Persona** models the skeptic/non-buyer you want
  to **screen out or convert**. For a real audience map, have the user build **both** — one to target,
  one to disqualify — rather than a single blended profile. Personality-trait predictions
  (practical-vs-emotional, introvert-vs-extrovert) are directional framing, not measured psychometrics.
- **Treat every generated persona as an editable hypothesis, and always prescribe validating it against
  real customers.** The persona is an AI guess that can *sound* convincing while being invented — so in
  every answer, even a "how do I get a good persona?" one, tell the user to **validate it against a
  handful of real customers before building or messaging around it: interview target users about the
  last time they hit the problem, and watch what they actually do** (observed behavior beats stated
  intent). Edit the card labels to keep the useful scaffolding and cut the invented parts.
- **Don't confuse a persona with validated demand.** Personadeck can produce a polished persona for an
  audience that won't buy — if the real question is "should I build/ship this?", route to
  `/sales-idea-validation` for real signal (smoke test / pre-sale). Use the persona to sharpen the
  pitch; take the go/no-go from real behavior.
- **The output is a static PDF card — plan around that.** Personadeck exports to **PDF only**; reviewers
  note the persona is static and **can't be embedded elsewhere**. Tell the user to treat the export as a
  reference doc, edit labels before exporting, and copy fields manually into a CRM/deck rather than
  expecting a live sync.
- **Present pricing as best-effort and start on the Free tier.** Personadeck has **Free (€0), Basic
  (~€4/mo), Medium (~€9.90/mo), and Pro (~€42/mo, ~45 personas/mo)** tiers plus an **AppSumo lifetime
  deal** — name the Free tier first and tell the user to confirm current plans/limits and which features
  are plan-gated (e.g. generation in any language) before upgrading, since figures move.
- **There's no public API — don't plan an integration around it.** If asked to automate or batch
  personas, say plainly there's **no documented public API, no webhooks, and no Zapier/Make/MCP**; it's a
  UI tool. Copy outputs manually, or for programmatic persona generation call an LLM API directly with
  your own prompt (see `references/platform-guide.md`).

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — assembled from third-party listings (Capterra, AppSumo, GetApp);
the tool lineup and EUR pricing move, so verify at personadeck.io.*

- **It can just repackage your input.** The top reviewer complaint is that a thin prompt yields a persona
  that echoes what you typed with no actionable insight — specificity of the audience/product
  description is what makes the output useful.
- **A generated persona is not validated demand.** It'll happily describe a buyer for an audience that
  won't pay — pair it with a real demand test (`/sales-idea-validation`).
- **AI personas sound convincing even on thin data.** The model can invent demographics, motivations,
  and personality traits; validate the persona against real customers before betting on it.
- **The persona is static and PDF-only.** No live embed, no export beyond PDF — copy fields out manually;
  don't expect a sync into a CRM or deck.
- **No documented public API / webhooks / Zapier / MCP.** It's a web tool — don't plan integrations or
  batch jobs around it; automate with a direct LLM API call instead.
- **Pricing is best-effort, EUR, and may be stale.** Free/Basic/Medium/Pro plus an AppSumo lifetime deal;
  confirm current tiers, the ~45-persona/month cap, and which features are plan-gated before upgrading.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full persona/validator tool landscape (use this to actually decide build-or-not)
- `/sales-personagen` — PersonaGen platform help (a sibling prompt-only persona generator — detailed personas + reusable content-generation prompts, organized into projects and feature-wise sections; UI-only/no API)
- `/sales-instantpersonas` — InstantPersonas / User Persona platform help (a sibling prompt-only persona generator that also adds website-perception "Insights" and competitor personas)
- `/sales-founderpal` — FounderPal platform help (broader solopreneur AI marketing suite that includes a buyer-persona generator)
- `/sales-content` — Content-marketing strategy across tools (turn persona insights into a content plan)
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Generate a buyer persona for a product
**User says**: "I'm launching a meal-prep service for shift workers — can Personadeck build me a persona?"
**Skill does**: Points to the persona generator and stresses describing a **specific** customer (a
rotating-shift nurse who skips meals on night shifts, say) with the exact problem and differentiation so
the output beats a generic template that just echoes the prompt; suggests generating a **User Persona**
to target and a **Negative Persona** for who to screen out; frames the resulting card — behaviors,
motivations, channels — as an editable hypothesis to confirm with a handful of real shift-worker
conversations before building messaging around it. Notes the Free tier is the place to start.
**Result**: A tailored, dual-persona view the founder validates against reality instead of a generic profile.

### Example 2: User Persona vs Negative Persona
**User says**: "Personadeck asks me to pick User Persona or Negative Persona — what's the difference and which do I use?"
**Skill does**: Explains a **User Persona** models the audience you want to align the product/messaging
with, while a **Negative Persona** models the skeptic or non-buyer you want to **avoid targeting or
deliberately convert**; recommends building **both** for a real audience map rather than one blended
profile, and notes the personality-trait predictions are directional framing, not measured psychometrics —
still validate against real people.
**Result**: The user builds one persona to target and one to disqualify, with the right expectations.

### Example 3: Can I automate Personadeck via API? (developer/automation)
**User says**: "I want to generate personas for 30 audience segments automatically — what's Personadeck's API?"
**Skill does**: States plainly there's **no documented public API, no webhooks, and no Zapier/Make/MCP**
(it's a UI tool with PDF-only export), so there's no supported way to batch it; suggests copying outputs
manually or calling an LLM API directly with a persona prompt (see `references/platform-guide.md` for a
cURL/Python example) for programmatic generation, and notes the thing worth automating is a real demand
signal, not a generated persona — pointing to `/sales-idea-validation`.
**Result**: The user avoids building on a non-existent API and picks a workable path.

## Troubleshooting

### Persona feels generic / just repeats what I typed
**Symptom**: The generated persona is vague, or reads like a restatement of the prompt with no insight.
**Cause**: The audience/product prompt was thin — Personadeck needs specific context, and reviewers
specifically fault it for repackaging shallow input.
**Solution**: Re-run with a rich description — specific customer, the exact problem, how the product
differs, current stage — and compare variants; also try a **Negative Persona** to force a different
angle. The more context, the sharper and more usable the persona.

### Can't export or embed the persona anywhere but PDF
**Symptom**: Looking for a way to embed the persona live, sync it to a CRM, or export beyond PDF.
**Cause**: Personadeck's persona is **static with PDF-only export** — there's no live embed and no API.
**Solution**: Edit the card labels first, export the PDF as a reference doc, and copy the fields you need
into your CRM/deck manually. Don't build a workflow expecting a live sync.

### "Is there an API?" / can't batch personas
**Symptom**: Looking for API docs, a webhook, or a way to batch-generate personas.
**Cause**: Personadeck has no documented public API, webhooks, or Zapier/Make/MCP; it's a web tool.
**Solution**: Don't build an integration around it — copy outputs manually, or call an LLM API directly
with your own persona prompt for programmatic use (see `references/platform-guide.md`). Automate the real
demand signal instead. See `/sales-idea-validation`.
