---
name: sales-aicofounder
description: "aicofounder (aicofounder.com) platform help — an AI co-founder that guides solo founders through structured phases from idea to launch: multi-agent deep market research that scans Reddit and X for real demand signals, idea validation, competitive analysis, a visual product canvas, a planning agent that turns your biggest constraint into step-by-step tasks, a website builder, and a content calendar, with persistent project memory. Use when running an idea through aicofounder's research and validation phases, interpreting its Reddit/X demand signals, deciding between the free monthly credits and the paid plan, understanding its structured workflow vs a generic AI chat, or pairing its research with a real demand test. Note: primarily a web tool with no documented public API. Do NOT use for the tool-agnostic validate-before-building method or comparing validators across the market (use /sales-idea-validation), or growing a pre-launch waitlist (use /sales-audience-growth)."
argument-hint: "[describe what you need help with in aicofounder]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
github: "https://github.com/aicofounder"
---

# aicofounder Platform Help

aicofounder (aicofounder.com) is an **AI "co-founder"** that walks solo founders through **structured
phases from idea to launch** — not a general chatbot. Its edge is **multi-agent deep market research
that scans Reddit and X for real demand signals** (grounding validation in actual discussions rather
than pure LLM opinion), plus idea validation, competitive analysis, a **visual product canvas**, a
**planning agent** (finds your biggest constraint → step-by-step tasks), a website builder, a content
calendar, and persistent project memory. Trusted by 90K+ founders. Because its research is grounded in
Reddit/X it's a **stronger gut check than a pure-LLM validator — but still not a substitute for your
own demand test**, and it has **no documented public API** (a UI tool).

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from aicofounder?**
   - A) Run the market-research / idea-validation phases and interpret the Reddit/X demand signals
   - B) Use the planning agent / visual canvas to turn research into an action plan
   - C) Understand the free monthly credits vs the paid plan
   - D) Get the most out of its structured workflow (how to frame your idea)
2. **Do you have a specific idea + target customer in mind?** The phased workflow needs a concrete starting point.

Skip-ahead: if the user wants the validate-before-building *method* or to compare validators, that's a
`/sales-idea-validation` question — route in Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or comparing idea validators/co-pilots across the market | `/sales-idea-validation {question}` |
| A dedicated AI idea validator (instant score/report) rather than a phased co-pilot | `/sales-validator-ai {question}` |
| Reddit-based real-demand discovery as a standalone signal | `/sales-trendseeker {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer aicofounder-specific questions using Step 3.

## Step 3 — aicofounder platform reference

**Read `references/platform-guide.md`** for the full reference — the phase/feature lineup (research,
validation, canvas, planning agent, website builder, content calendar), the free-credits vs paid
split and best-effort pricing, how to frame an idea for the most useful research, and the
no-public-API automation reality.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Lean on the Reddit/X demand research — it's the strongest part — but still confirm with your own
  test.** aicofounder's edge over a pure-LLM validator is that it grounds validation in real Reddit/X
  discussions, so treat those demand signals as genuinely useful evidence. Still tell the user that an
  AI-synthesized research summary is not the same as a stranger taking an action — confirm the go/no-go
  with a smoke test / pre-sale (route the method to `/sales-idea-validation`).
- **Frame a concrete idea + target customer before running the phases.** The structured workflow and
  research quality depend on a specific starting point (who it's for, the exact problem, and current
  stage) — a vague idea yields a vague plan. Have the user fill the context richly, then let the phases build on it.
- **Use the planning agent's output as an editable plan, not gospel.** The "biggest constraint → tasks"
  output and the generated plan are AI drafts — have the user sanity-check the identified constraint
  against their own reality and re-order tasks to fit; the value is the structure, not blind execution.
- **Budget around the free monthly credits, and flag pricing as best-effort.** It's **free to start
  with ~15 credits/month, no credit card**, and the first phases (idea discovery + market research) are
  free; a paid plan unlocks advanced features — **frame the buy decision around how many
  projects/phases they'll run**, not a monthly cost. Third-party quotes for the paid tier **disagree**
  (~$25/mo vs ~$149) — tell the user to confirm current pricing at aicofounder.com and start on the
  free credits.
- **There's no public API — don't plan an integration around it.** If asked to automate, say plainly
  there's no documented public API; it's a UI tool. For programmatic needs use a tool built for it, or
  export/copy manually. Automate real signals (landing-page conversions), not an AI research summary.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — features/pricing move; verify at aicofounder.com.*

- **Grounded, but still AI-synthesized.** Reddit/X demand research is stronger than a pure-LLM score,
  but it's an AI summary of discussions — not a stranger paying you. Confirm with a real demand test.
- **Pricing quotes disagree** (free ~15 credits/mo; paid quoted ~$25/mo vs ~$149). Confirm live; start free.
- **Output quality tracks input.** A vague idea/target → a generic plan; frame a concrete customer + problem.
- **No documented public API.** It's a web tool; don't plan integrations around it.
- **A generated plan is not validated demand** — the planning agent will happily plan a launch for an
  idea no one wants; the Reddit research is the check, and your own pre-sale is the proof.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator/co-pilot landscape (use this to actually decide build-or-not)
- `/sales-validator-ai` — Validator AI platform help (a dedicated instant AI idea validator — the score-and-report sibling)
- `/sales-founderpal` — FounderPal platform help (solopreneur AI marketing generators — persona/strategy sibling)
- `/sales-trendseeker` — Trend Seeker platform help (Reddit-based demand discovery as a standalone real signal)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Run market research on an idea
**User says**: "I have an idea for a tool for freelance designers — can aicofounder tell me if there's demand?"
**Skill does**: Points to aicofounder's multi-agent research phase that scans Reddit/X for real
pain-point discussions among the target audience, frames a concrete customer + problem first for better
signal, and reads the output as genuine (grounded) evidence — while stressing the go/no-go still needs a
real demand test (smoke test / pre-sale via `/sales-idea-validation`), because a research summary isn't
a stranger paying.
**Result**: The founder gets grounded demand signal from aicofounder and a plan to confirm it for real.

### Example 2: "It planned my whole launch — am I validated?"
**User says**: "aicofounder gave me a full plan from idea to launch. Does that mean it's validated?"
**Skill does**: Separates a generated *plan* from validated *demand* — the planning agent will map a
launch for an idea nobody wants — keeps the Reddit research + constraint analysis as useful input, and
routes the build-or-not decision to a real demand test via `/sales-idea-validation`.
**Result**: The founder executes the plan only after real demand signal, not because an agent produced steps.

### Example 3: Can I automate aicofounder via API? (developer/automation)
**User says**: "I want to run 20 ideas through aicofounder's research automatically — what's the API?"
**Skill does**: States plainly there's **no documented public API** (it's a UI tool), so there's no
supported way to batch it; suggests running ideas manually or using a tool built for programmatic
research, and notes the thing worth automating is a real demand signal, not an AI research summary —
pointing to `/sales-idea-validation`.
**Result**: The user avoids building on a non-existent API and picks a workable path.

## Troubleshooting

### The plan/research feels generic
**Symptom**: aicofounder's output could apply to almost any product.
**Cause**: The idea/target was too vague — the phased workflow and research need a concrete starting point.
**Solution**: Re-run with a specific customer, the exact problem, and current stage; the research
(especially the Reddit/X pain-point scan) sharpens a lot with a precise audience.

### Is the paid plan worth it over the free credits?
**Symptom**: Deciding whether to pay after the free credits.
**Cause**: Free tier is ~15 credits/month (first phases free); paid unlocks advanced features, and quotes vary.
**Solution**: Start on the free credits to see if the workflow fits; if you'll run many projects/phases,
weigh the paid plan — and confirm the current price at aicofounder.com (third-party quotes disagree).

### "Is there an API?" / can't automate it
**Symptom**: Looking for API docs or a way to batch runs.
**Cause**: aicofounder has no documented public API; it's a web tool.
**Solution**: Don't build an integration around it — run ideas manually or use a tool intended for
programmatic use; automate real demand signals (landing-page analytics) instead. See `/sales-idea-validation`.
