---
name: sales-proposal-page
description: "Writes and structure a Qwilr proposal page that closes deals. Use when your proposals look generic and aren't closing, you don't know what sections to include, the pricing table confuses buyers, your proposal doesn't stand out from competitors, or you're staring at a blank Qwilr page and need a structure that sells. Do NOT use for a multi-stakeholder deal room (use /sales-deal-room), reusable team templates (use /sales-proposal-template), or interpreting engagement analytics (use /sales-proposal-analytics)."
argument-hint: "[describe what you're proposing, to whom, and any Qwilr features to use]"
license: MIT
version: 1.0.0
tags: [sales, proposal, copywriting, qwilr]
---
# Write a Qwilr Proposal Page

Help the user write and structure a Qwilr proposal page — from section planning through copy and interactive element configuration. Qwilr replaces static PDF proposals with interactive web-based pages that include quote blocks, embedded content, and real-time engagement tracking.

## Step 1 — Gather context


If `references/learnings.md` exists, read it first for accumulated knowledge.

Ask the user:

1. **What are you proposing?** (product/service, scope, price range)
2. **Who is the buyer?** (title, company, industry, company size)
3. **Where is this deal?**
   - A) Early — they're evaluating options
   - B) Mid — they've seen a demo, now need a formal proposal
   - C) Late — verbal yes, need the paperwork
   - D) Renewal or expansion of existing deal
4. **Which Qwilr features do you want to use?**
   - A) Quote block with pricing table (interactive line items, optional add-ons)
   - B) Simple text-based proposal (no interactive pricing)
   - C) Full deal room with multiple pages (for instead, hand off: `/sales-deal-room {your question}`)
   - D) Not sure — recommend what fits

**If the user's request already provides most of this context, skip directly to the relevant step.** Lead with your best-effort answer using reasonable assumptions (stated explicitly), then ask only the most critical 1-2 clarifying questions at the end — don't gate your response behind gathering complete context.

## Step 2 — Generate page blueprint

Design a section-by-section page structure mapped to Qwilr block types. A strong Qwilr proposal typically follows this flow:

| Section | Qwilr Block Type | Purpose |
|---|---|---|
| Cover / Hero | Splash block | First impression, prospect's name/logo, one-line value prop |
| Executive Summary | Text + Image block | Why this matters to *them* specifically (2-3 paragraphs max) |
| Problem & Solution | Text block or Accordion | Frame the pain, present your solution mapped to their needs |
| Scope of Work | Text block or Accordion | What's included, deliverables, timeline |
| Pricing | Quote block | Interactive pricing table with line items |
| Timeline & Milestones | Text block | Key dates, phases, dependencies |
| About Us / Team | Text + Image block | Credibility — relevant team members, case study snippets |
| Next Steps / CTA | Accept block | Clear call to action — accept the proposal, sign, or book a call |

Adapt this structure based on the deal context:
- **Early-stage deals**: Lead heavier on problem/solution, lighter on detailed scope
- **Late-stage deals**: Lead with scope and pricing, lighter on problem framing
- **Renewals/expansions**: Lead with results achieved, then expansion scope and pricing. Use Qwilr's `isOptional: true` on expansion line items (new modules, add-ons, additional seats) so the buyer can self-select what to add beyond the base renewal. This gives the CFO/budget holder control while making the upsell frictionless.
- **Technical buyers**: Add a technical architecture or integration section
- **Executive buyers**: Add an ROI/business case section

## Step 3 — Write the copy

Write actual copy for each section, not just placeholders. Follow these principles:

- **Executive Summary**: 2-3 paragraphs max. Lead with their problem, not your product. Reference specific things from their situation (company name, goals they mentioned, pain points from discovery).
- **Problem & Solution**: Mirror their language back to them. Map each pain point to a specific capability.
- **Scope**: Use clear deliverables with enough detail that both sides know what "done" looks like, but not so much that it reads like a contract.
- **Pricing copy**: Write the framing text above the quote block — this is where you anchor value before they see numbers.
- **CTA**: Be specific about what happens after they accept (kickoff call within 48 hours, implementation begins week of X, etc.).

Use `{{token}}` syntax for any fields the user might want to auto-populate via the Qwilr API later (e.g., `{{company_name}}`, `{{contact_first_name}}`, `{{deal_amount}}`).

## Step 4 — Configure interactive elements

If the proposal includes a quote block, design the pricing structure:

### Quote block configuration

- **Sections**: Group line items logically (e.g., "Platform License", "Implementation", "Add-Ons")
- **Line items**: Each item needs a name, description, and price
  - Use `fixedCost` type for most items
  - Mark add-ons as `isOptional: true` so the buyer can select/deselect
  - Set `quantity` ranges where buyers should choose volume (seats, units)
  - Apply discounts where appropriate (percentage or fixed amount)
- **Billing**: Specify `oneOff` or `recurring` (monthly/quarterly/annual) per item
- **Tax**: Include tax configuration if applicable

### Interactive features to consider

- **Optional line items**: Let buyers self-select add-ons — this increases deal size while giving them control
- **Quantity selectors**: For per-seat or per-unit pricing, let buyers adjust quantity
- **Discount display**: Show the discount visibly to reinforce the deal they're getting
- **Section subtotals**: Help buyers understand cost breakdown by category
- **Features lists**: Add feature descriptions to line items for context

## Step 5 — Generate API payload (optional)

If the user wants to create the page programmatically via the Qwilr API, generate a `POST /pages` JSON payload with blocks, tokens, and quote sections. See `references/qwilr-api-proposals.md` for the full payload structure, field reference, and endpoint list.

Key points:
- Run `GET /blocks/saved` first to discover available block IDs
- Set `isPublished: false` to review before sending
- Use `tokens` to substitute CRM data into `{{token}}` placeholders
- Configure quote sections with line items, optional add-ons, and billing frequency

## Gotchas

- **Don't generate walls of text.** Qwilr is a visual, web-based platform — not a Word doc. Use Qwilr block types (Splash, Accordion, Quote blocks) to break up content. If a section runs longer than 3 paragraphs, restructure it into an Accordion or split it into sub-sections.
- **Don't forget the interactive pricing/quote block.** Claude defaults to writing pricing as plain text. Qwilr's quote block is the product's key differentiator — use it for any proposal that includes pricing. Configure line items, optional add-ons, and quantity selectors.
- **Don't skip the CTA.** Every proposal needs a clear call to action using Qwilr's Accept block. Don't end with "let us know your thoughts" — end with "Accept this proposal" or "Book your kickoff call."
- **Don't make the proposal too long.** Web proposals are not PDFs. Buyers skim. A strong Qwilr proposal is 5-8 sections. If it's longer, consider moving detailed content to a deal room (`/sales-deal-room`) instead.
- **Don't forget `{{token}}` placeholders.** If the proposal might be auto-generated via API later, use `{{company_name}}`, `{{contact_first_name}}`, etc. throughout — not hardcoded values.

- **Self-improving**: If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Examples

### Example 1: Late-stage SaaS proposal with interactive pricing

**User says**: "I need a Qwilr proposal for Acme Corp — verbal yes already, $48k/yr for our analytics platform plus an optional onboarding package. Mid-size fintech, buyer is their VP of Data."

**Skill does**:
1. Recognizes a Late-stage deal — leads with scope and pricing, keeps problem framing light.
2. Builds a page blueprint: Splash cover with Acme's name, a short Executive Summary tied to their data goals, a concise Scope of Work, then a Quote block.
3. Writes the section copy, including the value-anchoring framing text above the quote block.
4. Configures the quote block: a "Platform License" section at $48k/yr billed `recurring` annual, plus an "Onboarding" line item marked `isOptional: true` so the VP can self-select it.
5. Closes with an Accept block CTA naming the kickoff timeline.

**Result**: A 5-section Qwilr page with an interactive, buyer-selectable pricing table and a clear accept-to-sign CTA — ready to paste into Qwilr or push via the API.

### Example 2: Early-stage deal, blank page

**User says**: "I'm staring at a blank Qwilr page. Marketing agency pitching a brand refresh to an e-commerce startup that's still comparing vendors. Around $20k."

**Skill does**:
1. Identifies an Early-stage deal — weights the structure toward problem/solution, lighter on detailed scope.
2. Proposes a blueprint that opens with the buyer's pain, maps each pain point to a capability, and uses an Accordion to keep the solution scannable.
3. Drafts the Executive Summary and Problem & Solution copy mirroring the prospect's language.
4. Adds a simple Quote block with the $20k engagement and one optional add-on, then an Accept block CTA.

**Result**: A persuasive, skimmable proposal structure with real copy that frames the problem before the price.

### Example 3: Renewal with expansion upsell via the API

**User says**: "Generate the Qwilr API payload for a renewal — base $30k, plus three optional expansion modules at $5k each. I'll auto-fill the company name from HubSpot."

**Skill does**:
1. Treats it as a Renewal/expansion — leads with results achieved, then expansion scope.
2. Uses `{{company_name}}` and `{{contact_first_name}}` token placeholders throughout the copy.
3. Notes that `GET /blocks/saved` should run first to discover block IDs, then builds a `POST /pages` payload with `isPublished: false`.
4. Configures quote sections: a base renewal line item plus three expansion modules each set `isOptional: true`.
5. Maps `tokens` so HubSpot data substitutes into the `{{...}}` placeholders.

**Result**: A ready-to-send JSON payload (per `references/qwilr-api-proposals.md`) that creates an unpublished, token-driven renewal page with self-select expansion upsells.

## Troubleshooting

### The generated proposal reads like a wall of text or a Word doc

**Cause**: Copy was written as long prose instead of being mapped to Qwilr block types, so it ignores the platform's visual, web-based format.

**Solution**: Restructure any section longer than 3 paragraphs into an Accordion or split it into sub-sections, and map content to Splash, Text+Image, and Quote blocks. Aim for 5-8 sections total; move overflow detail to a deal room (`/sales-deal-room`).

### Pricing rendered as plain text instead of an interactive quote

**Cause**: Claude defaults to writing pricing as a text table, skipping Qwilr's quote block — its key differentiator.

**Solution**: Move any priced proposal into a Quote block. Group line items into sections, mark add-ons `isOptional: true`, set `quantity` ranges for per-seat pricing, and specify `oneOff` vs `recurring` billing per item.

### API call to create the page fails or references unknown block IDs

**Cause**: The `POST /pages` payload was built without first discovering the available saved block IDs, or it published immediately with no review step.

**Solution**: Run `GET /blocks/saved` to retrieve valid block IDs before composing the payload, set `isPublished: false` so the page can be reviewed before sending, and confirm `tokens` match the `{{token}}` placeholders in the copy. See `references/qwilr-api-proposals.md` for the full field reference.

## Before recommending a specific platform skill

This skill covers a strategy domain across many platforms. **Before pointing the user to any specific platform skill** (any `/sales-{platform}` listed in `## Related skills`, e.g., `/sales-mailshake`, `/sales-klaviyo`, `/sales-apollo`), read that platform skill's actual `SKILL.md` first. The 1-line description in `## Related skills` is enough to *identify* a candidate — it's not enough to *commit* to it or to write a prompt that invokes it well.

**How to read it:**
- If `~/.claude/skills/{skill-name}/SKILL.md` exists locally, `Read` it.
- For `sales-*` skills, `WebFetch` directly from this repo: `https://raw.githubusercontent.com/sales-skills/sales/main/skills/{skill-name}/SKILL.md` — e.g., for `sales-mailshake`: `https://raw.githubusercontent.com/sales-skills/sales/main/skills/sales-mailshake/SKILL.md`.
- For non-`sales-*` skills (third-party), look up `{org}/{repo}` in `~/.claude/skills/sales-do/references/skill-sources.md` if installed and fetch the same `skills/{skill-name}/SKILL.md` path under that repo.

**After reading,** ground your recommendation in something concrete from the SKILL.md (its scope, a sub-flow, its `argument-hint` shape, or a "Do NOT use for..." negative trigger). Align any generated invocation with the platform skill's `argument-hint`. If the platform skill turns out not to fit the user's situation, swap to another or handle the question here directly rather than recommending a poor fit.

## Related skills

- `/sales-proposal-analytics` — Track engagement after sending (who viewed, which sections, when to follow up)
- `/sales-qwilr-automation` — Automate proposal creation from CRM data via the Qwilr API
- `/sales-deal-room` — For complex multi-stakeholder deals that need multiple pages
- `/sales-proposal-template` — Design reusable templates for your whole team
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`
