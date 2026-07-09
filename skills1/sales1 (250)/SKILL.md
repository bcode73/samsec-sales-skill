---
name: sales-informly
description: "Informly (informly.ai) platform help — an AI startup-idea validation and pre-launch report generator that turns one idea description into a single 75+ page PDF: a viability score plus ~11 reports (idea validation, MVP roadmap, landing-page blueprint, marketing and sales strategy, competitive positioning, pitch deck, fundraising navigator, pivot playbook) built with real-time Google Search data, plus an AI business-advisor chat. Priced per report — a one-time purchase, no subscription, no credits — so each new idea is a fresh purchase. Use when running an idea through Informly, interpreting its viability score, understanding the per-report pricing, getting the reports out (PDF-only), or asking whether it has an API to export or automate reports. Note: UI-only, NO documented public API, no webhooks, no Zapier. Do NOT use for the tool-agnostic validate-before-building method or comparing idea validators across the market (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in Informly]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
---

# Informly Platform Help

Informly (informly.ai; the product runs at validator.informly.ai) is an **AI startup-idea validation
and pre-launch report generator**. You paste one freeform description of your idea and it returns a
single **75+ page PDF** — a **viability score** plus a suite of **~11 reports** (idea validation, MVP
roadmap, landing-page blueprint, marketing/sales strategy, competitive positioning, pitch deck,
fundraising navigator, pivot playbook, customer discovery), organized as **Ideate → Validate → Plan**
and grounded with **real-time Google Search** data. It also offers an **AI business-advisor chat**
(marketing, finance, sales, tech, fundraising, ops). Pricing is **per report — $29.99 one-time, no
subscription, no credits** — so each new idea is a fresh purchase. It's a fast idea-analysis tool and
document generator — **not a substitute for real demand validation** — and it has **no documented
public API** (a UI tool; PDF export only).

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from Informly?**
   - A) Run an idea through it and interpret the viability score / the report
   - B) Understand the pricing — $29.99 per report, one-time, and what a report includes
   - C) Use its downstream reports (MVP roadmap, landing page, marketing/sales, pitch deck, fundraising)
   - D) Get the report out or automate it (export / API reality)
2. **What's the real question — "is this idea worth building?" or "how do I use this tool?"** If it's
   the go/no-go decision, that's `/sales-idea-validation` (a report is not demand) — route in Step 2.

Skip-ahead: if the user wants the validate-before-building *method* or to compare validators across
the market, that's a `/sales-idea-validation` question — route immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| Comparing Informly against other AI validators (Validator AI, IdeaProof, DimeADozen…) | `/sales-idea-validation {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |
| Turning the report's marketing/sales sections into a real **content** program | `/sales-content {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer Informly-specific questions using Step 3.

## Step 3 — Informly platform reference

**Read `references/platform-guide.md`** for the full reference — the report lineup and what each
section produces, the per-report $29.99 pricing and what a purchase includes, how the viability score
is built (and why an AI report reads optimistic), the real-time Google Search data pipeline, the AI
business-advisor chat, and the no-public-API automation reality (PDF export only).

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Treat the viability score and report as a directional gut check, not demand.** The report is an
  **LLM opinion** from a single freeform prompt, grounded with live web search but still generated;
  independent reviewers note Informly gives no independent scoring rubric and its action plans
  **assume the idea should proceed ("assumes Go, not No-Go")**. Tell the user to **keep the structured
  outputs** (competitor/positioning sections, risks, the MVP-roadmap and customer-discovery prompts) to
  sharpen the pitch, and take the **go/no-go from real behavior** — a smoke test or pre-sale — not from
  the report. Route the real test to `/sales-idea-validation`.
- **Read the sourcing and the page count critically.** Reports lean on real-time Google Search, but the
  market-size and financial numbers are still **AI estimates** — tell the user to verify them against
  primary sources before quoting them, and note the "45+ vs 75+ pages" claim is marketed
  inconsistently, so **judge it by usefulness, not length**. A longer PDF is not more validation.
- **Budget per idea, not per month.** Pricing is **$29.99 per report, one-time — no subscription, no
  credits** — so **every new idea (and every re-run after a pivot) is a fresh $29.99 purchase**. Have
  the user finalize the idea framing before buying so they don't pay again to fix a thin input, and note
  the 7-day satisfaction guarantee allows a refund + re-generation (capped, ~2 uses). Prices move —
  tell the user to **confirm the current price on informly.ai**.
- **Use it for starter drafts, then replace them with tested ones.** The MVP roadmap, landing-page
  blueprint, marketing/sales strategy, and pitch deck are fast **first drafts** — fine to launch a smoke
  test with, but the copy and positioning that survive are the ones that convert. Push real
  ad/landing testing to `/sales-content` and `/sales-funnel`; don't treat the generated plan as a
  finished GTM. The AI business-advisor chat is a brainstorming aid, not an accountable advisor.
- **There's no public API — don't plan an integration around it.** If asked to automate or export, say
  plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP** — it's a UI tool
  that outputs a **PDF only**. Give the user the two workable fallbacks: (1) **download the PDF and
  parse/extract it** yourself if you need the text elsewhere, and (2) **use a tool built for
  programmatic validation** if you need it scripted. Then point out the thing actually worth automating
  is the real signal (landing-page conversions), not the generated report — route that real test to
  `/sales-idea-validation` (decision) and `/sales-funnel` (build the page).

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — Informly's pricing, report lineup, and page counts move; verify at informly.ai.*

- **The report reads optimistic and is not demand.** A single freeform prompt with no independent
  scoring rubric, and action plans that assume the idea proceeds — a polished report validates nothing;
  follow it with a real-behavior test (smoke test / pre-sale).
- **Page count is marketed inconsistently (45+ vs 75+).** Judge the report by usefulness, not length —
  a longer PDF is padding, not more evidence.
- **Priced per report, not per month.** $29.99 one-time buys one idea's report; **no subscription and no
  credits**, so every new idea and every post-pivot re-run is another $29.99.
- **Market-size / financial numbers are AI estimates.** Real-time Google Search grounds the text, but
  the figures still need verifying against primary sources before you quote them.
- **No documented public API, no webhooks, no Zapier/Make/MCP.** It's a web tool that exports a **PDF
  only** — you can't script or batch it; download and parse the PDF if you need the data elsewhere.
- **Thin independent review presence.** Few third-party reviews (Reddit/Trustpilot/G2) and the company
  is registered in Anguilla while operated from Melbourne — weigh marketing claims accordingly.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator landscape (use this to actually decide build-or-not; a report is not demand)
- `/sales-ideaproof` — IdeaProof platform help (the credit-based 120s validation + pre-launch suite — a close sibling; both bundle many downstream assets)
- `/sales-validator-ai` — Validator AI platform help (a dedicated free AI idea validator — the score-and-report sibling)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-content` — Turn the report's marketing/sales sections into a real content/ad program
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "Informly scored my idea well and gave me a 75-page report — should I build it?"
**User says**: "Informly gave my idea a good viability score and a huge report. Is it validated?"
**Skill does**: Explains the report is an **LLM opinion** from one freeform prompt with no independent
scoring rubric — and that its plans assume the idea proceeds, so it reads optimistic and validates
nothing on its own. Tells the user to keep the competitor/positioning, risks, and customer-discovery
prompts to sharpen the pitch, then route the real go/no-go to `/sales-idea-validation` — a smoke test or
pre-sale where a stranger takes an action — rather than trusting the report or its length.
**Result**: The founder gets real demand signal before building, using Informly's structure, not its verdict.

### Example 2: How does Informly's pricing actually work?
**User says**: "Is Informly a subscription? I want to validate a few different ideas."
**Skill does**: Explains pricing is **$29.99 per report, one-time — no subscription and no credits** — so
each of several ideas is a separate $29.99 purchase, and every post-pivot re-run costs again. Advises
finalizing each idea's framing before buying so a thin input isn't paid for twice, notes the 7-day
satisfaction guarantee allows a refund + re-generation (capped), and to confirm the current price on
informly.ai since pricing moves.
**Result**: The user budgets per idea and avoids re-buying to fix a rushed input.

### Example 3: Can I export or automate Informly reports? (developer/automation)
**User says**: "I want to run 20 ideas through Informly and pull the reports into a database via API."
**Skill does**: States plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP**
— it's a UI tool that outputs a **PDF only**, so there's no supported way to batch or export
programmatically. Suggests downloading and parsing the PDF, or using a tool built for programmatic
validation, and notes the thing worth automating is a real demand signal (landing-page conversions),
not a generated report — pointing to `/sales-idea-validation` and `/sales-funnel`.
**Result**: The user avoids building on a non-existent API and picks a workable path.

## Troubleshooting

### The report seems glowing / it never tells me not to build
**Symptom**: The viability score is high and every section assumes the idea should proceed.
**Cause**: The report is a single-prompt LLM opinion with no independent scoring rubric; reviewers note
it "assumes Go, not No-Go" — it pattern-matches to encouragement.
**Solution**: Stop treating the report as the decision. Keep the structured outputs (competitors, risks,
positioning, customer-discovery prompts) and run a real demand test — smoke test or pre-sale — via
`/sales-idea-validation`.

### The market-size / financial numbers don't have clear sources
**Symptom**: TAM/market and projections are stated with few clickable citations.
**Cause**: Reports use real-time Google Search for context, but the figures are largely AI-generated
estimates.
**Solution**: Treat the numbers as hypotheses to verify against primary sources (Statista, Crunchbase,
your own bottom-up math) before quoting them in a plan or pitch.

### I want an API or a way to export/automate
**Symptom**: Want to script Informly or pull reports into another system.
**Cause**: Informly has no documented public API, webhooks, or iPaaS connectors; it's a web tool that
outputs a PDF only.
**Solution**: Download and parse the PDF, or use a tool intended for programmatic use; automate a real
demand signal (landing-page analytics) instead. See `/sales-idea-validation`.

### I paid $29.99 but want to validate a different idea now
**Symptom**: Expected ongoing access after paying; a second idea asks for payment again.
**Cause**: Informly is priced **per report** — one-time, no subscription, no credits — so each idea is a
separate purchase.
**Solution**: Finalize each idea's framing before buying, use the 7-day satisfaction guarantee
(refund + re-generation, capped) if a report is off, and confirm the current per-report price on
informly.ai.
