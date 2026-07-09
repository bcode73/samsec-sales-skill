---
name: sales-venturusai
description: "VenturusAI (venturusai.com) platform help — an AI business-idea validator that runs your idea through classic strategy frameworks (SWOT, PESTEL, Porter's Five Forces, VRIO) plus TAM/SAM/SOM sizing, target-audience personas, financial projections, and an MVP/GTM plan, then generates a downloadable report and pitch deck. It's a pure-LLM tool with no source citations, and its viability scores skew encouraging. Use when running an idea through VenturusAI's free or paid reports, interpreting its SWOT/PESTEL/Porter/VRIO analysis or score, comparing Standard vs Advanced reports, understanding its Starter/Lite/Pro/Enterprise tiers and character limits, asking whether it has an API or how to automate report generation, or troubleshooting generic or too-positive output. Do NOT use for the validate-before-building method or ranking validators to pick one (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in VenturusAI]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
---

# VenturusAI Platform Help

VenturusAI (venturusai.com) is an **AI business-idea validator built on classic strategy frameworks**.
You paste an idea (or business description) and it generates a report applying **SWOT, PESTEL, Porter's
Five Forces, and VRIO**, plus **TAM/SAM/SOM** market sizing, **target-audience personas** (user stories +
demographics), **financial projections** (startup cost, revenue, breakeven), a **marketing/branding** pass
(slogans, social examples), and — on **Advanced** reports — a deeper **MVP + GTM** plan and a **pitch
deck**. It's a **pure-LLM tool** (GPT-3.5/4 class) with **no source citations** — the analysis is the
model's reasoning over frameworks, not evidence scraped from live sources, and its scores tend to **skew
encouraging**. Reports come in two depths (**Standard** vs **Advanced**), download as PDF (watermarked on
the free tier), and are gated by monthly quotas and idea character limits per plan. **API access exists on
the Enterprise plan but is undocumented publicly.**

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from VenturusAI?**
   - A) Run an idea and interpret the report — SWOT/PESTEL/Porter/VRIO, personas, sizing, or the score
   - B) Understand the tiers — free Starter vs Lite vs Pro vs Enterprise (reports/mo, char limits, API)
   - C) Compare Standard vs Advanced reports (what the Advanced upgrade actually adds)
   - D) Export or automate report generation (the API reality)
2. **What's the real question — "is this idea worth building?" or "how do I use this tool?"** If it's the
   go/no-go decision itself, that's `/sales-idea-validation` (a validator's output is a gut check, not
   demand) — route in Step 2.

Skip-ahead: if the user wants the validate-before-building *method* or to compare validators across the
whole market to pick one, that's a `/sales-idea-validation` question — route immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| A full **cross-market ranking** of validators (Preuve, IdeaProof, Validator AI, DimeADozen… to pick one) — but answer a quick VenturusAI-vs-X *how-they-differ* inline first (Step 4) | `/sales-idea-validation {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer VenturusAI-specific questions using Step 3.

## Step 3 — VenturusAI platform reference

**Read `references/platform-guide.md`** for the full reference — the framework set (SWOT/PESTEL/Porter/VRIO)
and what each section contains, Standard vs Advanced report contents, target-audience/persona and financial
outputs, the Starter/Lite/Pro/Enterprise tiers with reports-per-month and character limits, the
Enterprise-only-and-undocumented API reality, and how to feed it a rich input to avoid generic output.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Treat the report as a framework-structured AI opinion, not evidence.** VenturusAI's value is that it
  organizes an idea into SWOT/PESTEL/Porter/VRIO with sizing and personas fast — good for spotting blind
  spots and sharpening the pitch. But it's a **pure-LLM tool with no source citations**, so every "fact"
  (market size, competitor, retention) is the model's guess. Tell the user to **keep the structured outputs
  (SWOT, competitor list, risks, GTM angle) to sharpen the pitch** and put the go/no-go on a **real demand
  test** (smoke test / pre-sale) — route the decision to `/sales-idea-validation` and the build to `/sales-funnel`.
- **Warn that the score skews encouraging.** VenturusAI's output tends to be **positive/feel-good**, and it
  will "validate" almost any idea if the input sounds plausible. A high score is not demand. Say so
  explicitly and push the user to a real-behavior test rather than trusting the verdict.
- **The single biggest lever is input richness — coach it.** The #1 complaint is *generic output*, and it's
  almost always caused by a thin one-line input. Tell the user to feed a **detailed** description (target
  customer, the specific problem, how it's solved today, business model) and to use the **higher character
  limits on paid tiers** (Starter caps ideas at ~1,000 chars; Pro allows ~10,000). Richer input in →
  specific analysis out. Present any tier/character-limit figures as **best-effort and point the user to
  venturusai.com/plans** to confirm current numbers before they pick a plan.
- **When asked how it compares to a cited/evidence validator, give the contrast inline, then offer the route.**
  If the user asks VenturusAI vs Preuve / IdeaProof / DimeADozen, answer *how they differ* directly:
  VenturusAI runs **classic frameworks (SWOT/PESTEL/Porter/VRIO) with no source-linking and encouraging
  scores**, whereas Preuve **cites every claim to 50+ live sources and scores conservatively**, and
  DimeADozen is a **one-time citation-backed report you buy and keep**. Tell the user to pick by **framework
  breadth/speed vs evidence rigor**, then offer `/sales-idea-validation` for a full ranking. Don't just route away.
- **Present all pricing/tiers as best-effort and point to the plans page.** VenturusAI's tiers, quotas, and
  character limits **move and differ between sources** — present any figure as best-effort and point the
  user to **venturusai.com/plans** to confirm. Frame the tiers around what breaks: the free Starter is
  ~2 reports/mo with a tight character cap and a watermarked PDF; **Advanced reports** (MVP/GTM/financial
  depth) and higher quotas need a paid plan; **API + multi-user + custom watermark** are Enterprise-only.
- **There's no usable public API — don't plan an integration around it.** If asked to export or automate,
  say plainly that **API access is an Enterprise-plan feature but there is no public API documentation**
  (`api.venturusai.com` sits behind auth and redirects), and no webhooks/Zapier/MCP are documented. The only
  reliable export is the **downloadable PDF**. If programmatic batch validation matters, choose a tool built
  for it; and remember the thing worth automating is the real demand signal (landing-page analytics), not the
  report — route that to `/sales-funnel`.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — VenturusAI's tiers, quotas, character limits, and features move; verify at venturusai.com/plans.*

- **No source citations — it's a pure-LLM opinion.** Unlike cited validators (Preuve, DimeADozen), every
  claim (market size, competitors, retention) is the model's guess, not scraped evidence. Follow any score
  with a real-behavior test (smoke test / pre-sale).
- **Scores skew encouraging.** Output tends to be positive/feel-good and will "validate" most ideas — a high
  score is not demand. Read it as directional and settle the go/no-go with real behavior.
- **Generic output = thin input.** The most common complaint; a one-line idea produces vague analysis. Feed a
  detailed description and use the paid tiers' higher character limits to get specific output.
- **Standard vs Advanced is the real gate.** Standard reports give the framework analysis; **Advanced**
  reports (limited per plan) add the deeper MVP/GTM plan, richer financials, and pitch deck. Free Starter
  gives Standard only.
- **Free tier is tight.** ~2 Standard reports/month, a ~1,000-character idea cap, and a **watermarked** PDF;
  no Advanced reports, no API, no custom watermark.
- **API is Enterprise-only and undocumented.** API access is a paid Enterprise feature, but there's **no
  public API reference**, no documented webhooks, and no Zapier/MCP — treat it as unusable for a DIY
  integration and contact VenturusAI support if you're on Enterprise.
- **Text-only.** It analyzes a written description; it can't ingest images, mockups, videos, or prototypes,
  and it misses nuance in highly specialized/regulated industries.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator landscape (use this to actually decide build-or-not; a validator's output is a gut check, not demand)
- `/sales-preuve` — Preuve AI platform help (the cite-every-claim, conservative-score contrast to VenturusAI's framework-driven, no-citation, encouraging-score model)
- `/sales-ideaproof` — IdeaProof platform help (fast 120s score + broad pre-launch suite — the speed/breadth sibling)
- `/sales-dimeadozen` — DimeADozen platform help (one-time, keep-forever citation-backed report — the evidence-with-receipts sibling)
- `/sales-validator-ai` — Validator AI platform help (a free score-and-report validator — the fast-score sibling)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "VenturusAI gave my idea a strong SWOT and a good score — should I build it?"
**User says**: "I ran my idea through VenturusAI, the SWOT looks great and it gave me a positive score. Good to go?"
**Skill does**: Credits the framework structure (SWOT/PESTEL/Porter/VRIO) as useful for spotting blind spots
and sharpening the pitch, but reframes the verdict: VenturusAI is a **pure-LLM tool with no source citations**
and its scores **skew encouraging**, so the positive read reflects the model, not the market. Tells the user
to keep the structured outputs (SWOT, competitors, risks, GTM angle) and earn a real go/no-go with a
smoke-test landing page (pre-set ≥5% join threshold) or a pre-sale — routing the decision to
`/sales-idea-validation` and the build to `/sales-funnel`.
**Result**: The founder uses the analysis to sharpen, and decides on stranger behavior, not the score.

### Example 2: "Can I batch 20 ideas through VenturusAI and pull the reports via the API?" (developer/automation)
**User says**: "I want to script VenturusAI to run 20 ideas and pull each report into a database via the API or a webhook."
**Skill does**: States plainly that **API access is an Enterprise-plan feature but there is no public API
documentation** (`api.venturusai.com` is behind auth and redirects to the homepage), and no webhooks,
Zapier, or MCP server are documented — so there's no supported DIY way to batch or export programmatically.
Notes the only reliable export is the **downloadable PDF**, and suggests that if programmatic validation is
essential, use a tool built for it. Adds that the thing actually worth automating is a real demand signal
(landing-page analytics), not a generated report — pointing to `/sales-idea-validation` and `/sales-funnel`.
**Result**: The user avoids planning an integration around an undocumented API and picks a workable path.

### Example 3: "Why is my VenturusAI report so generic, and is the paid plan worth it?" (output quality / tiers)
**User says**: "My VenturusAI report is vague and could apply to any startup. Will paying fix it?"
**Skill does**: Explains that generic output almost always traces to a **thin input** — a one-line idea — and
that the fix is a **detailed** description (target customer, specific problem, how it's solved today,
business model) plus the **higher character limits on paid tiers** (Starter caps ideas at ~1,000 chars; Pro
allows ~10,000). Notes the real paid upgrade is **Advanced reports** (deeper MVP/GTM/financials + pitch
deck) and more reports/month, and presents all tier figures as best-effort, pointing to venturusai.com/plans.
**Result**: The user gets specific output by enriching the input, and understands what a paid plan actually adds.

## Troubleshooting

### "My VenturusAI report reads generic — it could describe any startup"
**Symptom**: The analysis is vague and not specific to the idea.
**Cause**: A thin, one-line input — VenturusAI reasons over whatever you give it, so a short description
yields a short, generic report. The free tier's ~1,000-character cap makes this worse.
**Solution**: Feed a **detailed** description — target customer, the exact problem, how people solve it today,
the business model — and use a paid tier's higher character limit (Pro ~10,000). Then keep the structured
sections (SWOT, competitors, risks) and still settle the go/no-go with a real demand test via `/sales-idea-validation`.

### "The score seems too positive to trust"
**Symptom**: A glowing, encouraging report the founder senses is too easy.
**Cause**: VenturusAI is a **pure-LLM validator with no source citations** and its scores **skew
encouraging** — it pattern-matches to plausible-sounding optimism and can invent supporting "facts" (market
size, demand).
**Solution**: Discard the verdict, keep the framework outputs to sharpen the pitch, and earn a real one — run
a smoke test to a pre-set conversion threshold and attempt a pre-sale. Cross-check with a cited validator
(`/sales-preuve`) or a real-demand signal (`/sales-trendseeker`); disagreement is the useful information.

### "I'm on Enterprise and want to use the API — where are the docs?"
**Symptom**: Paid for API access but can't find developer documentation.
**Cause**: VenturusAI gates API access to the **Enterprise plan** but publishes **no public API reference**;
`api.venturusai.com` sits behind auth and redirects, and no webhooks/Zapier/MCP are documented.
**Solution**: Contact VenturusAI support/Help Centre directly for API credentials and endpoint docs — there's
no self-serve reference to build against. For anything you'd script today, export the **PDF** manually, and
if programmatic batch validation is core to your workflow, pick a validator built for it.
