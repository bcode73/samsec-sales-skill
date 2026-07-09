---
name: sales-deal-room
description: "Designs a Qwilr deal room for complex multi-stakeholder B2B deals. Use when a deal has too many stakeholders to manage over email, buyers keep losing track of materials, there's no single source of truth for a complex deal, you need a mutual action plan to keep procurement on track, or an enterprise deal needs a polished hub for all parties. Do NOT use for a single-stakeholder proposal page (use /sales-proposal-page), reusable team templates (use /sales-proposal-template), or interpreting buyer engagement signals (use /sales-proposal-analytics)."
argument-hint: "[describe the deal — type, stakeholders, stage, and what materials are needed]"
license: MIT
version: 1.0.0
tags: [sales, proposal, deal-room, qwilr]
---
# Design a Qwilr Deal Room

Help the user architect a Qwilr deal room — a multi-page digital sales room for complex B2B deals with multiple stakeholders, long sales cycles, and lots of moving parts.

## When to use a deal room vs. a single proposal

| Scenario | Use |
|---|---|
| Simple deal, single decision-maker, straightforward pricing | Single proposal page (`/sales-proposal-page`) |
| Multiple stakeholders, complex evaluation, needs ongoing updates | Deal room (this skill) |
| Enterprise deal with procurement, legal, technical review | Deal room |
| Partner/channel deal with shared materials | Deal room |
| Expansion deal with existing customer needing executive buy-in | Deal room |

## Step 1 — Gather context


If `references/learnings.md` exists, read it first for accumulated knowledge.

Ask the user:

1. **What type of deal is this?**
   - A) New logo — first time selling to this company
   - B) Expansion — upselling/cross-selling existing customer
   - C) Renewal — contract renewal with potential changes
   - D) Partner/channel deal — working through a partner
   - E) Other — describe it

2. **Who are the stakeholders?** (select all that apply)
   - A) Executive sponsor (C-suite / VP)
   - B) Economic buyer (budget holder)
   - C) Technical evaluator (engineering/IT)
   - D) End users / champions
   - E) Procurement / legal
   - F) External consultant or advisor
   - G) Other — describe

3. **What materials do you already have?**
   - A) Nothing yet — starting from scratch
   - B) We have a proposal/quote
   - C) We have a pitch deck
   - D) We have case studies and technical docs
   - E) We have most things, need to organize them

4. **What's the deal timeline?**
   - A) Trying to close this month
   - B) 1-3 month sales cycle
   - C) 3-6 month enterprise cycle
   - D) 6+ months

**If the user's request already provides most of this context, skip directly to the relevant step.** Lead with your best-effort answer using reasonable assumptions (stated explicitly), then ask only the most critical 1-2 clarifying questions at the end — don't gate your response behind gathering complete context.

## Step 2 — Deal room architecture

Design the page-by-page structure. A deal room is a collection of Qwilr pages organized as a hub with linked sub-pages. The hub page is the "front door" that each stakeholder visits.

### Recommended structure

**Hub Page** (the main deal room page — everyone starts here)

| Section | Block Type | Content |
|---|---|---|
| Welcome header | Splash | Personalized greeting, company logos, deal room title |
| Navigation | Text + buttons | Links to each sub-page, organized by topic |
| Key contacts | Text + Image | Your team's contacts with photos and roles |
| Timeline snapshot | Text | High-level mutual action plan with key dates |
| Latest updates | Text | What's new since last visit (keep this updated) |

**Sub-pages** (linked from the hub — create based on what the deal needs):

| Page | Who it's for | Content |
|---|---|---|
| Executive Summary | Executive sponsor | Business case, ROI, strategic alignment |
| Technical Overview | Technical evaluator | Architecture, integrations, security, compliance |
| Proposal & Pricing | Economic buyer | Interactive quote block, pricing options, terms |
| Case Studies | All stakeholders | Relevant customer stories, metrics, testimonials |
| Implementation Plan | Technical + Ops | Timeline, phases, resource requirements, dependencies |
| Security & Compliance | IT / Legal / Procurement | Certifications, data handling, SLAs, DPA |
| Mutual Action Plan | All stakeholders | Shared timeline with milestones, owners, and status |
| FAQ & Objection Handling | Champions | Answers to common questions champions get asked internally |

### Adapting for deal type

- **New logo**: Heavier on Executive Summary, Case Studies, and Security. Include a "Why Us" page if competitive.
- **Expansion**: Lead with "Results So Far" page showing value delivered, then expansion scope.
- **Renewal**: Lead with partnership recap, then changes/additions for the new term.
- **Partner deal**: Include a partner-facing page with co-selling materials and margin details.

## Step 3 — Content briefs and hub page copy

### Hub page draft copy

Write the actual content for the hub/navigation page:

**Welcome section**: "Welcome to the [Company] + [Your Company] Deal Room. This is your central hub for everything related to our partnership. Below you'll find the key materials organized by topic — click into any section to dive deeper."

**Navigation section**: Create a card-style layout linking to each sub-page with a one-line description:

- **Executive Summary** — The business case for [solution]: ROI, strategic fit, and expected outcomes
- **Technical Overview** — Architecture, integrations, security posture, and compliance details
- **Proposal & Pricing** — Interactive pricing with options to customize your package
- **Case Studies** — How companies like yours achieved [specific outcome]
- **Implementation Plan** — Timeline, phases, and what we need from each team
- **Mutual Action Plan** — Our shared roadmap to getting this live by [target date]

**Key contacts section**: List 2-3 people from your team with name, title, photo placeholder, email, and one line about their role in this deal.

### Content briefs for sub-pages

For each sub-page, provide:
- **Audience**: Who this page is for and what they care about
- **Key message**: The one thing this page should communicate
- **Structure**: Section-by-section outline with recommended block types
- **Tone**: How formal/technical/executive the language should be
- **CTA**: What action the reader should take after this page

## Step 4 — Mutual action plan

Design the timeline page with milestones and owners:

| Milestone | Owner | Target Date | Status |
|---|---|---|---|
| Discovery & scoping complete | Both | [date] | Done |
| Technical evaluation | Buyer's IT team | [date] | In progress |
| Security review | Buyer's security | [date] | Not started |
| Proposal & pricing review | Economic buyer | [date] | Not started |
| Legal / contract review | Both legal teams | [date] | Not started |
| Executive sign-off | Executive sponsor | [date] | Not started |
| Contract signed | Both | [date] | Not started |
| Kickoff & implementation begins | Both | [date] | Not started |

Customize milestones based on the deal type and timeline. For faster deals, collapse steps. For enterprise deals, add procurement and compliance milestones.

## Step 5 — Analytics strategy

Set up engagement tracking per stakeholder by configuring webhooks for the deal room pages:

### Which events to watch per stakeholder

| Stakeholder | Watch for | What it means |
|---|---|---|
| Executive sponsor | Views Executive Summary page | They're engaged — or their EA is screening |
| Technical evaluator | Views Technical Overview, time on security page | Doing due diligence — prepare for technical questions |
| Economic buyer | Views Pricing page repeatedly | Evaluating cost — may need ROI reinforcement |
| Procurement/Legal | Views Security & Compliance page | Deal is in procurement — prepare for contract negotiation |
| New/unknown viewer | Views any page | Champion is sharing internally — the deal is expanding |

### Webhook setup for deal room

```bash
curl -X POST https://api.qwilr.com/v1/webhooks \
  -H "Authorization: Bearer $QWILR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-endpoint.com/qwilr-deal-room",
    "events": ["pageFirstViewed", "pageViewed", "pageAccepted", "pagePartiallyAccepted"]
  }'
```

Use view data to:
1. Identify which stakeholders are engaged and which aren't
2. Spot new stakeholders entering the evaluation
3. Time your follow-ups to when people are actively reviewing
4. Update your champion on who's looked at what

For full webhook and CRM automation setup, use `/sales-qwilr-automation`.

### In Seismic

- **Digital Sales Rooms (DSR)**: Create buyer-facing microsites for complex deals. Curate content by stakeholder role — executive summaries for C-suite, technical specs for evaluators, ROI calculators for finance.
- **Per-stakeholder tracking**: See which stakeholder viewed which content, how long they spent, and what they downloaded. Identify champions (high engagement) and blockers (no activity).
- **Content recommendations**: Seismic's AI (Aura) suggests relevant content for the deal based on CRM data, deal stage, and buyer persona.
- **CRM integration**: DSR activity syncs to Salesforce/HubSpot — engagement data appears on the opportunity record for deal reviews.
- **Best practice**: Create a DSR template per deal type (new business, expansion, renewal) with pre-loaded content for each stage. Customize per deal rather than building from scratch.

## Gotchas

- **Don't create too many pages for simple deals.** A deal room with 8 sub-pages for a $15k deal is overkill. Match complexity to deal size — small deals need 2-3 pages max (proposal + case study). Reserve the full structure for enterprise deals with multiple stakeholders.
- **Don't use the same content for every stakeholder.** The whole point of a deal room is tailored content per role. An executive summary page full of technical specs fails the executive; a pricing page with no ROI context fails the CFO. Write for each audience.
- **Don't skip the mutual action plan.** Claude often builds deal rooms with great content but no shared timeline. The MAP is what turns a deal room from a content dump into a collaboration tool. Always include one.
- **Don't forget the executive summary page.** Even in a deal room with detailed sub-pages, the hub page needs a concise "why this matters" section. Executives won't click into sub-pages — they'll read the hub and decide if this is worth their time.
- **Don't treat the deal room as "set and forget."** A good deal room is updated throughout the sales cycle — latest updates section, MAP status changes, new materials added. Mention this to the user.

- **Self-improving**: If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Examples

### Example 1: New-logo enterprise deal with procurement and security review

**User says**: "We're 4 months into a new-logo deal with a 2,000-person fintech. There's a VP sponsor, a head of engineering, a security/IT team, and procurement just got pulled in. The thread is a mess and people keep asking for the same docs. Help me build a Qwilr deal room."

**Skill does**:
1. Classifies this as a New logo deal with a 3-6 month cycle and four stakeholder groups (exec sponsor, technical evaluator, IT/security, procurement).
2. Designs a hub page with welcome splash, card-style navigation, key contacts, and a timeline snapshot, then weights sub-pages toward the new-logo pattern — Executive Summary, Technical Overview, Security & Compliance (certifications, DPA, SLAs), Case Studies, Proposal & Pricing, and a Mutual Action Plan.
3. Writes hub navigation copy with a one-line description per sub-page and content briefs (audience, key message, structure, tone, CTA) for each page.
4. Builds the Mutual Action Plan table with milestones for security review, legal/contract review, and executive sign-off, with owners and target dates.
5. Sets up per-stakeholder webhook tracking so a Security & Compliance view flags "deal is in procurement" and a pricing-page revisit flags "reinforce ROI."

**Result**: A page-by-page deal room blueprint plus ready-to-paste hub copy, a procurement-aware action plan, and an engagement-tracking plan — the buyer gets one source of truth instead of a tangled email thread.

### Example 2: Expansion deal that needs executive buy-in

**User says**: "Existing customer, want to upsell a second product line, but I need a VP we haven't worked with to sponsor it. Closing target is this quarter."

**Skill does**:
1. Classifies this as an Expansion deal on a compressed timeline.
2. Leads the structure with a "Results So Far" page quantifying value already delivered, then an expansion-scope page and a tightened Proposal & Pricing page.
3. Collapses the Mutual Action Plan to the essential milestones (scoping, exec sign-off, contract, kickoff) to fit the quarter-end close.
4. Recommends watching for the new VP's first view of the Executive Summary as the signal that the champion has successfully shared internally.

**Result**: A lean expansion deal room that opens with proof of value and routes a new executive to a concise business case, with a timeline matched to the close date.

## Troubleshooting

### The deal room feels bloated and the buyer isn't engaging

**Cause**: Too many sub-pages for the deal size — an 8-page structure built for a small or simple deal buries the few things that matter.

**Solution**: Match page count to complexity. For small deals use 2-3 pages max (proposal + case study) and reserve the full hub-and-sub-page structure for enterprise deals with multiple stakeholders. Make sure the hub page itself carries a concise "why this matters" summary, since executives decide from the hub without clicking in.

### Content lands flat with one role even though other stakeholders are engaged

**Cause**: The same generic content is reused across pages, so an executive hits technical specs and a CFO hits pricing with no ROI context — the per-role tailoring that justifies a deal room is missing.

**Solution**: Write each sub-page for its specific audience using the content-brief fields (audience, key message, tone, CTA). Keep the Executive Summary strategic and outcome-focused, give the Technical Overview the depth evaluators want, and pair pricing with ROI framing for the economic buyer.

### Webhook events aren't arriving for the deal room pages

**Cause**: The webhook subscription is missing the relevant events, the endpoint isn't reachable, or the auth token is wrong.

**Solution**: Confirm the subscription includes `pageFirstViewed`, `pageViewed`, `pageAccepted`, and `pagePartiallyAccepted`, that the `Authorization: Bearer $QWILR_TOKEN` header is valid, and that your endpoint returns 2xx. For full webhook delivery and CRM-sync setup and debugging, use `/sales-qwilr-automation`.

## Related skills

- `/sales-proposal-page` — Write a single proposal page (for simpler deals)
- `/sales-proposal-analytics` — Interpret engagement signals from deal room pages
- `/sales-qwilr-automation` — Automate deal room creation and CRM sync
- `/sales-proposal-template` — Create reusable deal room templates
- `/sales-seismic` — Seismic platform help including Digital Sales Rooms and content management
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`
