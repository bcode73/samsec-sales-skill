---
name: sales-founderpal
description: "FounderPal (founderpal.ai) platform help — a suite of AI marketing tools for solopreneurs who hate marketing (by Dan Kulkov): free single-purpose generators (marketing strategy, buyer/user persona, value proposition, business model, idea validator, ad copy) plus a paid one-time/lifetime Marketing Strategy product that personalizes output to a detailed profile of your product. Use when generating a marketing strategy, buyer persona, or value proposition for a solo project, validating an idea with FounderPal's tools, deciding between its free tools and the paid lifetime plans, understanding what its one-time pricing gets you, or wanting more tailored output than generic ChatGPT. Note: primarily a web tool with no documented public API. Do NOT use for the tool-agnostic validate-before-building method or comparing idea validators across the market (use /sales-idea-validation), or content-marketing strategy across tools (use /sales-content)."
argument-hint: "[describe what you need help with in FounderPal]"
license: MIT
version: 1.0.0
tags: [sales, marketing, pre-launch, platform]
---

# FounderPal Platform Help

FounderPal (founderpal.ai, by **Dan Kulkov**) is a suite of **AI marketing tools for solopreneurs
who "hate marketing."** It's a dashboard of single-purpose generators — marketing strategy, buyer/
user persona, value proposition, business model, idea validator, ad copy, pricing — that produce
output **personalized to a detailed profile of your product** (its edge over generic ChatGPT). Many
generators are **free** (a famous lead-magnet playbook); the paid product is a **one-time / lifetime
Marketing Strategy** purchase, not a subscription. It's a fast marketing-copilot, **not a
substitute for real demand validation**, and it has **no documented public API** (a UI tool).

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from FounderPal?**
   - A) Generate a marketing strategy, buyer persona, or value proposition for a project
   - B) Use its idea validator to sanity-check an idea
   - C) Understand the free tools vs the paid one-time/lifetime plans
   - D) Get more useful/tailored output out of it (how to fill the product profile)
2. **Do you have a clear product description ready?** Output quality tracks the detail you give it.

Skip-ahead: if the user wants the validate-before-building *method* or to compare validators, that's a
`/sales-idea-validation` question — route in Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or comparing idea validators across the market | `/sales-idea-validation {question}` |
| A dedicated AI idea validator (score/report) rather than FounderPal's marketing suite | `/sales-validator-ai {question}` |
| Content-marketing **strategy** across tools (SEO content, editorial, distribution) | `/sales-content {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer FounderPal-specific questions using Step 3.

## Step 3 — FounderPal platform reference

**Read `references/platform-guide.md`** for the full reference — the generator lineup and what each
produces, the free-vs-paid split and best-effort one-time/lifetime pricing, how to fill the product
profile for the most tailored output, and the no-public-API automation reality.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Feed it a rich product profile — output quality tracks input.** FounderPal's whole edge over
  generic ChatGPT is that it personalizes to a detailed description of the product, ICP, and goals.
  Tell the user to fill the strategy/profile inputs thoroughly (specific customer, exact problem,
  differentiation, current stage) before generating, then **re-run variants and compare**; a thin
  input yields generic strategy/persona output.
- **Treat outputs as a fast first draft to edit, not final truth.** The persona, marketing strategy,
  and ad copy are AI-generated starting points — have the user validate the persona against real
  customers and treat the strategy as a hypothesis to test, not a plan to execute blindly.
- **Don't confuse a generated strategy with validated demand.** FounderPal can produce a slick
  marketing plan for an idea nobody wants — if the real question is "should I build this?", route to
  `/sales-idea-validation` and get real signal (smoke test / pre-sale), not just a generated strategy.
  **Keep** FounderPal's persona, positioning, and value-prop outputs to sharpen the pitch — just take
  the go/no-go from real behavior, not the generated plan.
- **Model the one-time / lifetime pricing, and flag it as best-effort.** The paid product is a
  **one-time purchase** (lifetime access / credits), not a monthly subscription — so frame value as
  "how many strategies will you generate" against the one-time fee, and tell the user to confirm
  current plans/prices at founderpal.ai (third-party quotes disagree). Many generators are free — start there.
- **There's no public API — don't plan an integration around it.** If asked to automate, say plainly
  there's no documented public API; it's a UI tool. For programmatic needs use a tool built for it, or
  copy the output manually. Automate real signals (landing-page conversions), not generated strategy.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — the tool lineup and pricing move; verify at founderpal.ai.*

- **A generated marketing strategy is not validated demand.** It'll happily plan the go-to-market for
  an idea no one wants — pair it with a real demand test (`/sales-idea-validation`).
- **Output quality depends on input depth.** Thin product profile → generic ChatGPT-grade output; the
  personalization is the point, so fill the inputs.
- **Pricing is one-time / lifetime, not a subscription** — and third-party quotes disagree (e.g. per-
  strategy vs unlimited-lifetime vs an annual credits pass). Confirm live; many tools are free.
- **No documented public API.** It's a web tool; don't plan integrations around it.
- **Personas/strategy are AI drafts.** Validate the persona against real customers before betting on it.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator/tool landscape (use this to actually decide build-or-not)
- `/sales-validator-ai` — Validator AI platform help (a dedicated free AI idea validator — the score-and-report sibling)
- `/sales-content` — Content-marketing strategy across tools (beyond FounderPal's generators)
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Generate a marketing strategy for a solo project
**User says**: "I built a small SaaS but I'm terrible at marketing — can FounderPal give me a plan?"
**Skill does**: Points to FounderPal's marketing-strategy + buyer-persona generators, stresses filling
the product profile in detail (specific customer, problem, differentiation) so the output beats generic
ChatGPT, and frames the result as an editable first draft — a hypothesis to test with real customers,
not a plan to execute blindly. Notes many generators are free to start.
**Result**: A tailored starting strategy the founder refines against reality instead of a generic template.

### Example 2: "Should I build this — FounderPal says my strategy looks good"
**User says**: "FounderPal generated a great marketing strategy for my idea. Does that mean it's validated?"
**Skill does**: Separates a generated *strategy* from validated *demand* — FounderPal can plan GTM for an
idea nobody wants — and routes the build-or-not decision to `/sales-idea-validation` (smoke test +
pre-sale), keeping FounderPal's persona/positioning as pitch-sharpening input.
**Result**: The founder gets real demand signal before building, using FounderPal for the pitch, not the verdict.

### Example 3: Can I automate FounderPal via API? (developer/automation)
**User says**: "I want to generate personas for 30 products automatically — what's FounderPal's API?"
**Skill does**: States plainly there's **no documented public API** (it's a UI tool), so there's no
supported way to batch it; suggests copying outputs manually or using a tool built for programmatic
persona generation, and notes the thing worth automating is a real demand signal, not generated
strategy — pointing to `/sales-idea-validation`.
**Result**: The user avoids building on a non-existent API and picks a workable path.

## Troubleshooting

### Output feels generic / like plain ChatGPT
**Symptom**: The generated strategy or persona is vague and could apply to any product.
**Cause**: The product profile/input was thin — FounderPal's personalization needs detail to beat a
generic model.
**Solution**: Re-run with a rich description — specific customer, the exact problem, how the solution
differs, current stage — and compare variants; the more context, the more tailored the output.

### "Is there an API?" / can't automate it
**Symptom**: Looking for API docs or a way to batch-generate.
**Cause**: FounderPal has no documented public API; it's a web tool.
**Solution**: Don't build an integration around it — copy outputs manually or use a tool intended for
programmatic use; automate real demand signals (landing-page analytics) instead. See `/sales-idea-validation`.

### Not sure if the paid plan is worth it
**Symptom**: Deciding between the free tools and a one-time/lifetime purchase.
**Cause**: The pricing is a one-time fee (lifetime/credits), not a subscription, and quotes vary by source.
**Solution**: Start with the free generators; if you'll generate many strategies, weigh the one-time fee
against that volume, and confirm the current plans/prices at founderpal.ai before buying.
