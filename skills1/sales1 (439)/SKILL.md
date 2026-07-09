---
name: sales-proposal-analytics
description: "Interprets Qwilr engagement signals and decide what to do next. Use when a prospect hasn't opened your proposal, the buyer went dark after viewing, you don't know who else on the committee saw it, you're unsure whether to follow up or wait, a prospect keeps re-reading the pricing section but won't sign, or deal momentum stalled after sending the quote. Do NOT use for writing or structuring the proposal (use /sales-proposal-page), building reusable templates (use /sales-proposal-template), or wiring Qwilr to a CRM (use /sales-qwilr-automation)."
argument-hint: "[describe the engagement signals you're seeing — e.g., 'prospect viewed 3 times but hasn't accepted']"
license: MIT
version: 1.0.0
tags: [sales, proposal, analytics, engagement, qwilr]
---
# Interpret Qwilr Proposal Analytics

Help the user read Qwilr engagement signals and turn them into concrete next steps — follow-up messages, strategy adjustments, or deal actions.

## Step 1 — Gather context


If `references/learnings.md` exists, read it first for accumulated knowledge.

Ask the user:

1. **What are the analytics showing?**
   - A) Prospect viewed the proposal (single view)
   - B) Prospect viewed multiple times
   - C) Multiple people viewed it (committee/forwarded)
   - D) Prospect hasn't viewed it at all
   - E) Prospect viewed specific sections heavily (e.g., pricing)
   - F) Prospect partially accepted (selected some items, not all)
   - G) Prospect accepted the proposal
   - H) Other — describe the signals

2. **How long since you sent it?**
   - A) Less than 24 hours
   - B) 1-3 days
   - C) 4-7 days
   - D) More than a week
   - E) More than 2 weeks

3. **Deal context**:
   - What's the deal size and product/service?
   - Who's the buyer (title, decision-making authority)?
   - Is there a competitive situation?
   - What was the last conversation like before sending?

**If the user's request already provides most of this context, skip directly to the relevant step.** Lead with your best-effort answer using reasonable assumptions (stated explicitly), then ask only the most critical 1-2 clarifying questions at the end — don't gate your response behind gathering complete context.

## Step 2 — Signal interpretation

Interpret the engagement pattern using this framework:

### View patterns and what they mean

| Signal | Likely Meaning | Urgency |
|---|---|---|
| **Viewed once, briefly** | Skimmed it, may return later — or may not be prioritizing | Medium |
| **Viewed once, spent time on pricing** | Evaluating cost, possibly comparing to alternatives | High |
| **Viewed multiple times** | Actively considering, possibly building internal case | High |
| **Multiple unique viewers** | Being circulated to buying committee — deal is progressing | High |
| **Pricing section revisited 3+ times** | Price sensitivity or building a budget justification | High |
| **Executive summary skipped, jumped to pricing** | Buyer already understands the value, focused on cost | Medium |
| **Not viewed after 24h** | Email may not have landed, or not a priority right now | Medium |
| **Not viewed after 3+ days** | Delivery issue, lost priority, or buyer is going dark | High |
| **Viewed then went silent** | May be discussing internally, or lost momentum | Medium-High |
| **Partial acceptance** | Wants some items but not others — negotiation opportunity | High |

### Multiple-viewer analysis

When multiple people view the proposal:
- **2-3 viewers**: Normal buying committee circulation. The original contact is championing internally.
- **4+ viewers**: Larger committee than expected — deal may be more complex. Ask about procurement involvement.
- **New viewer after silence**: The proposal was forwarded up — a good sign, but the new viewer may need different framing.
- **Same person, different times**: They're returning to it — likely building a case or comparing options.

## Step 3 — Action plan

Based on the signals, provide concrete next steps:

### If viewed and engaged (positive signals)
1. **Don't jump in immediately** — let them finish evaluating (unless they've viewed 3+ times with no action)
2. **Send a value-add follow-up** — share a relevant case study, ROI data, or answer a question they didn't ask yet
3. **Offer to walk through it** — "I saw you've had a chance to review — want to jump on a quick call to walk through the pricing options?"

### If not viewed
1. **Check delivery** — confirm the email landed (check spam, verify address)
2. **Re-send with a different subject line** — the original email may not have cut through
3. **Try a different channel** — phone call (most direct), LinkedIn message (visible even if email is buried), text/SMS (if you have the number and the relationship supports it). Don't keep using the same channel that isn't working.
4. **Reduce friction** — "Here's the one-page summary" with a link back to the full proposal

### If pricing section is getting heavy attention
1. **Proactively address value** — send an ROI breakdown or case study showing cost justification
2. **Offer flexibility** — "I noticed you're reviewing the pricing — happy to discuss options that fit your budget"
3. **Don't discount preemptively** — let them raise the concern first

### If multiple stakeholders are viewing
1. **Ask your champion** — "It looks like a few people on your team are reviewing — should I put together a summary for the broader group?"
2. **Create stakeholder-specific content** — technical details for engineering, ROI for finance, timeline for ops
3. **Offer a group walkthrough** — bring all stakeholders into one call

### If buyer went dark
1. **Day 3-5**: Light touch — share something useful (article, case study), don't ask "did you see my proposal?"
2. **Day 7-10**: Direct but empathetic — "I know things get busy. Is this still a priority for Q2, or should we revisit later?"
3. **Day 14+**: Break-up email — "I don't want to keep following up if the timing isn't right. Should I close this out for now?"

## Step 4 — Draft follow-up messages

Write 1-2 follow-up messages tailored to the specific engagement pattern. Messages should:

- Reference the engagement signal *indirectly* (don't say "I see you viewed it 5 times" — that's creepy)
- Add value, not just ask for status
- Include a specific, low-friction CTA
- Match the tone of the deal stage (casual for early, professional for enterprise)

## Step 5 — Webhook setup guidance

Help the user set up real-time alerts for future proposals using Qwilr webhooks:

### Recommended webhook subscriptions

```bash
curl -X POST https://api.qwilr.com/v1/webhooks \
  -H "Authorization: Bearer $QWILR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-endpoint.com/qwilr-events",
    "events": ["pageFirstViewed", "pageViewed", "pageAccepted", "pagePartiallyAccepted"]
  }'
```

### Event-to-action mapping

| Webhook Event | Recommended Action |
|---|---|
| `pageFirstViewed` | Alert rep in Slack/email — prospect opened the proposal |
| `pageViewed` (repeat) | Log in CRM — track view count and timing |
| `pageAccepted` | Update CRM deal stage, notify rep, trigger onboarding |
| `pagePartiallyAccepted` | Alert rep — buyer selected some items, follow up on the rest |
| `pagePreviewAccepted` | Internal preview was accepted — ready for client review |

For full automation setup (CRM sync, Slack notifications, etc.), use `/sales-qwilr-automation`.

## Gotchas

- **Don't over-interpret a single page view.** One view could be the prospect, their EA, or an automated CRM preview. A single brief view doesn't mean "they're interested" — it means "someone opened the link." Wait for patterns (repeat views, time spent, multiple viewers) before drawing conclusions.
- **Don't treat all engagement signals equally.** Pricing section views are much higher signal than a quick skim of the cover page. Weight your interpretation toward the sections that indicate evaluation behavior (pricing, scope, case studies).
- **Don't recommend aggressive follow-up on automated CRM views.** Some CRMs and email tools auto-preview links, generating false "viewed" signals. If a view happens within seconds of sending with zero time on page, it's likely automated.
- **Don't tell the prospect you can see their views.** Saying "I noticed you looked at the pricing 3 times" is creepy and breaks trust. Reference engagement signals *indirectly* — "I wanted to see if you had questions about the pricing options."
- **Don't ignore time-of-day context.** A prospect reviewing a proposal at 10pm on a Sunday suggests they're doing personal due diligence, possibly building a case. A 30-second view during business hours is likely a quick skim between meetings.

- **Self-improving**: If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Examples

### Example 1: Repeat pricing views but no signature

**User says**: "I sent a $40k Qwilr proposal 4 days ago. The buyer has opened it 5 times and keeps landing on the pricing section, but hasn't accepted."

**Skill does**:
1. Maps the signal to "Pricing section revisited 3+ times" — High urgency, price sensitivity or budget-justification behavior.
2. Notes 5 views over 4 days means active consideration, not a stalled deal — the buyer is building an internal case.
3. Recommends proactively addressing value (ROI breakdown / cost-justification case study) rather than discounting preemptively, and offering budget-fit flexibility without conceding first.
4. Drafts a follow-up that references the pricing interest indirectly ("happy to walk through the options that fit your budget") rather than "I saw you viewed pricing 5 times."

**Result**: The user sends a value-anchored follow-up with a low-friction CTA, addressing the cost concern before it becomes an objection — and avoids the trust-breaking "I can see your views" mistake.

### Example 2: New viewer appears after the deal went quiet

**User says**: "My contact viewed the proposal once, then nothing for a week. Now suddenly two new people I've never talked to have opened it."

**Skill does**:
1. Reads this as "New viewer after silence" plus multiple-viewer circulation — the proposal was forwarded up to a buying committee, a positive sign.
2. Flags that the new viewers may need different framing (the original value pitch was built for the first contact).
3. Recommends asking the champion whether to prepare a summary for the broader group and creating stakeholder-specific content (ROI for finance, technical detail for engineering).
4. Suggests offering a single group walkthrough to align all stakeholders.

**Result**: The user re-engages through the champion, supplies committee-ready material, and converts forwarding momentum into a scheduled group call instead of waiting passively.

### Example 3: Proposal never opened after 3 days

**User says**: "It's been 3 days and the analytics show zero views. The prospect was warm on our last call."

**Skill does**:
1. Maps to "Not viewed after 3+ days" — High urgency, likely a delivery issue or lost priority rather than disinterest.
2. Has the user verify delivery first (spam folder, correct address) before assuming the buyer is dodging.
3. Recommends switching channels — phone, LinkedIn, or SMS if the relationship supports it — rather than re-sending the same dead email thread.
4. Suggests reducing friction with a one-page summary and a fresh subject line.

**Result**: The user discovers the email was buried, reaches the prospect on a more visible channel, and gets the proposal opened without an awkward "did you see it?" nudge.

## Troubleshooting

### A "view" registered within seconds of sending, with no time on page

**Cause**: Many CRMs, email security gateways, and link-preview tools auto-fetch links, generating a false "viewed" signal before any human opens it.

**Solution**: Treat sub-minute, zero-dwell views as automated, not human engagement. Wait for a pattern (repeat views, real time-on-page, or a distinct second viewer) before alerting the rep or starting follow-up.

### Analytics show many viewers but the deal still feels stuck

**Cause**: A large viewer count (4+) can signal a bigger or more complex committee than expected — often procurement or legal entering the process — not necessarily buying intent.

**Solution**: Ask the champion who is now involved and whether procurement is engaged. Provide stakeholder-specific framing and a group walkthrough rather than assuming volume of views equals momentum.

### Unsure whether to follow up or wait after a single view

**Cause**: One brief view is low-signal — it could be the prospect, an assistant, or an automated preview, and it doesn't indicate evaluation behavior.

**Solution**: Don't jump in on a single skim. Hold for a pattern; if you must touch base, send a value-add (case study, useful article) rather than a status-check, and never reference the view directly.

## Related skills

- `/sales-proposal-page` — Write or restructure the proposal itself
- `/sales-qwilr-automation` — Set up automated CRM sync and webhook workflows
- `/sales-cadence` — General follow-up strategies (non-Qwilr-specific)
- `/sales-deal-room` — For complex deals that need a multi-page deal room
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`
