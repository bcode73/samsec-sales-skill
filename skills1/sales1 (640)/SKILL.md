---
name: sales-validator-ai
description: "Validator AI (validatorai.com) platform help — free AI startup-idea validation used by 300K+ founders: enter an idea and get an AI viability score, market-size estimate, competitive analysis, a simulated customer-reaction Q&A, an AI mentor chatbot, and a custom accelerator roadmap. Use when running an idea through Validator AI, interpreting its AI score and suggested next steps, deciding between the free validator, the Accelerator plan, and Pro, understanding what the score does and does not prove, or pairing an AI validation with a real demand test. Note: primarily a web tool with no documented public API. Do NOT use for the broader validate-before-building methodology or comparing validation tools across the market (use /sales-idea-validation), or for growing a pre-launch waitlist (use /sales-audience-growth)."
argument-hint: "[describe what you need help with in Validator AI]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
github: "https://github.com/ValidatorAI"
---

# Validator AI Platform Help

Validator AI (validatorai.com) is a **free, web-based AI startup-idea validator** used by 300K+
founders: you type in an idea and it returns an AI viability **score**, a market-size estimate, a
competitive analysis, a **simulated customer-reaction Q&A**, and an **AI mentor chatbot**, plus a
paid custom "accelerator" roadmap. It's a fast structured gut check for first-time founders, makers,
and vibe coders — **not proof of demand**, and **there's no documented public API** (it's a UI tool).

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from Validator AI?**
   - A) Interpret the score/report it gave you and decide what to do next
   - B) Understand the free validator vs the paid Accelerator vs Pro
   - C) Get the most useful output out of it (how to phrase the idea)
   - D) Automate/export it into your own tooling
2. **Have you run the idea yet, or are you deciding whether to?**

Skip-ahead: if the user really wants the validate-before-building *method* or a tool comparison, this
is a `/sales-idea-validation` question — route in Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, the evidence ladder, or comparing validators across the market | `/sales-idea-validation {question}` |
| Reddit-based real-demand discovery/scoring (a different, behavior-based validator) | `/sales-trendseeker {question}` |
| Growing a pre-launch **waitlist** / capturing signups | `/sales-audience-growth {question}` |
| Building the **landing page** / smoke test to test real demand | `/sales-funnel {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer Validator-AI-specific questions using Step 3.

## Step 3 — Validator AI platform reference

**Read `references/platform-guide.md`** for the full reference — what each output means (score,
market size, competitor list, customer simulation, mentor), the free vs Accelerator vs Pro plan
gates and best-effort pricing, how to phrase an idea for the most useful output, and the
no-public-API automation reality.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Treat the score as a directional gut check, never proof.** Tell the user plainly that Validator
  AI's output is an LLM's opinion that can be confidently wrong (it can invent market sizes and
  "validate" almost anything) — a high score is not demand. Keep the useful structured parts
  (competitor list, positioning, GTM angle, the customer-simulation objections) and then get real
  signal. Route the actual go/no-go to `/sales-idea-validation`.
- **Use it to sharpen the pitch and surface blind spots, then go test.** Its best value is a fast
  second opinion, a competitor scan, and a rehearsal of customer objections — use those to tighten the
  idea, then validate demand with a smoke test / pre-sale (`/sales-funnel` + `/sales-audience-growth`).
- **Feed it a sharp idea statement.** Output quality tracks input: give it the specific customer, the
  problem, and how the solution is different — a vague idea yields generic feedback. Re-run variants to
  compare.
- **Choose the plan by what you actually need, and flag pricing as best-effort.** The core validator +
  idea generator are free; the **Accelerator** adds a guided roadmap + AI mentor and **Pro** adds
  deeper market/competitor intel and financial forecasting. Sources disagree on exact prices — tell the
  user to confirm current tiers at validatorai.com and not to pay for depth they won't act on.
- **Don't plan an integration around it — there's no public API.** If asked to automate, say clearly
  there's no documented public API (the site's own `/api/free-tool.php` endpoint is internal and
  unsupported — **it can change or block without notice**, so don't build on it); for programmatic
  validation, use a tool built for it or capture the output manually. See `/sales-idea-validation` for the tool landscape.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — pricing and features move; verify at validatorai.com.*

- **The score is an LLM opinion, not evidence.** It can hallucinate market sizes and encourage almost
  any idea — don't let it substitute for a real demand test.
- **No documented public API.** It's a web tool; the internal `/api/free-tool.php` endpoint is
  unsupported — don't build integrations on it. Review sites that claim "API access" are echoing marketing copy.
- **Pricing is inconsistent across sources.** Free core; paid Accelerator and Pro tiers are quoted
  differently by third parties — confirm live before deciding.
- **Free tier is genuinely useful** — the core validator, score, and idea generator don't require payment.
- **It validates the pitch, not the market.** Two runs (or two tools) can disagree; the customer
  simulation is a rehearsal, not real customers.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method and the full validator landscape (start here for the decision)
- `/sales-trendseeker` — Trend Seeker platform help (Reddit-based real-demand discovery + evidence scoring)
- `/sales-audience-growth` — Grow a pre-launch waitlist to capture real demand
- `/sales-funnel` — Build the smoke-test / fake-door landing page for a real demand test
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "It scored my idea 8/10 — what now?"
**User says**: "Validator AI gave my idea 8/10 and a big market size. Should I build?"
**Skill does**: Explains the score is a directional AI opinion that can be confidently wrong, keeps the
competitor list and customer-simulation objections to sharpen the pitch, and prescribes a real demand
test (smoke-test page + pre-sale with a pre-set threshold), routing the method to `/sales-idea-validation`.
**Result**: The founder uses the report to improve the pitch and earns a go/no-go from real behavior.

### Example 2: Free vs paid
**User says**: "Do I need Validator AI's paid plan or is the free one enough?"
**Skill does**: Notes the core validator, score, and idea generator are free; the Accelerator adds a
roadmap + AI mentor and Pro adds deeper market/competitor/financial detail — recommends staying free for
a first gut check and only paying for depth they'll act on, flagging pricing as best-effort to confirm
on-site.
**Result**: The user avoids paying for a tier they don't need.

### Example 3: Can I automate it via API? (developer/automation)
**User says**: "I want to run 50 ideas through Validator AI automatically from a script — what's the API?"
**Skill does**: States plainly there's **no documented public API** and that the site's internal
`/api/free-tool.php` endpoint is unsupported and not to be built on; suggests either capturing outputs
manually or using a validator designed for programmatic use, and points to `/sales-idea-validation` for
options and to a real demand test as the thing worth automating (landing-page conversions).
**Result**: The user avoids building on an unsupported endpoint and picks a workable path.

## Troubleshooting

### The score feels too generous / too vague
**Symptom**: Validator AI is encouraging or gives generic feedback.
**Cause**: LLM validators skew positive, and vague inputs yield vague outputs.
**Solution**: Re-run with a sharper idea statement (specific customer + problem + differentiation),
compare variants, and treat the verdict as directional — get real signal via a smoke test / pre-sale.

### "Is there an API?" / automation isn't working
**Symptom**: Can't find API docs or an integration keeps breaking.
**Cause**: There's no documented public API; the internal `/api/free-tool.php` endpoint isn't a supported interface.
**Solution**: Don't build on the internal endpoint. Capture outputs manually, or use a tool intended for
programmatic validation; automate the *demand test* (landing-page analytics) instead. See `/sales-idea-validation`.

### Should I trust it for a go/no-go?
**Symptom**: Tempted to decide to build (or not) purely on the score.
**Cause**: Confusing an AI opinion with market evidence.
**Solution**: Use Validator AI to sharpen the idea and list competitors, then decide on real behavior —
a smoke test to a pre-set conversion bar and a pre-sale. Route the method to `/sales-idea-validation`.
