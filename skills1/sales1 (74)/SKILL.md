---
name: sales-buildornot
description: "BuildOrNot (buildornot.io) platform help — a startup-idea discovery and market-research data platform plus a free, no-signup AI idea evaluator, for indie hackers, makers, and first-time founders. Browse datasets of AI tools and startups ranked by revenue and growth, Reddit startup-idea threads, startup revenue records, and trending topics to find proven demand; or paste an idea into the free evaluator for an instant AI take (USP, risks, suggestions). Use when mining BuildOrNot's data to find a niche or idea worth building, interpreting its AI evaluator verdict, understanding the free-tier preview limits and what the paid plan unlocks, asking whether it has an API to export data, or judging its credibility (anonymous founder, inconsistent user counts, unverified success claims). UI-only, NO public API/webhooks/Zapier. Do NOT use for the validate-before-building method or comparing idea validators across the market (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in BuildOrNot]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
github: "https://github.com/buildornot"
---

# BuildOrNot Platform Help

BuildOrNot (buildornot.io) is two products in one: a **startup-idea discovery / market-research
data platform** and a **free, no-signup AI idea evaluator**. The data side lets you browse datasets
of **AI tools and startups ranked by revenue and growth**, **Reddit startup-idea threads**, **startup
revenue records**, and **trending topics** to hunt for proven demand and underserved niches. The
evaluator takes a freeform idea and returns an instant AI take (USP, risk factors, suggestions) — a
**single-prompt GPT wrapper**, not a structured validator. It's a **discovery/research tool**, not
proof of demand, and it has **no public API** (a UI web app; data is preview-limited on the free tier).

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from BuildOrNot?**
   - A) Mine its **data** (AI-tool revenue rankings, Reddit ideas, revenue records, trending topics) to find a niche or idea
   - B) Run an idea through the **free AI evaluator** and interpret the verdict
   - C) Understand the **free tier's preview limits** and what the paid plan unlocks
   - D) Get the data out / automate it (export / API reality)
   - E) Judge whether the tool (and its claims) is **credible** enough to rely on
2. **What's the real question — "what should I build / is this idea worth building?" or "how do I use this tool?"**
   If it's the go/no-go decision, that's `/sales-idea-validation` (a data browse and an AI take are not
   demand) — route in Step 2.

Skip-ahead: if the user wants the validate-before-building *method* or to compare validators across the
market, that's a `/sales-idea-validation` question — route immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| Comparing BuildOrNot against other validators (Validator AI, IdeaProof, Informly, DimeADozen…) | `/sales-idea-validation {question}` |
| Deep **Reddit demand-signal** discovery / scoring as its own workflow | `/sales-trendseeker {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer BuildOrNot-specific questions using Step 3.

## Step 3 — BuildOrNot platform reference

**Read `references/platform-guide.md`** for the full reference — the two products (data platform vs
free evaluator), the datasets and their counts, the free-tier 100-item preview limit and what the paid
plan unlocks, how the evaluator is built (a single-prompt GPT wrapper) and why its verdict reads
optimistic, the no-public-API automation reality (no API/webhooks/Zapier/MCP; the GitHub org is
marketing, not an API), and the credibility caveats to weigh.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Use BuildOrNot for discovery, not for the decision.** Its real value is the *data* — AI-tool
  revenue rankings, Reddit idea threads, revenue records, and trending topics — to **find candidate
  ideas and see what's already making money**. Tell the user to treat the datasets as a **starting
  shortlist and competitor/market scan**, then take the go/no-go from a real demand test (smoke test /
  pre-sale), not from a data browse. Route the real test to `/sales-idea-validation`.
- **Treat the AI evaluator's verdict as a directional gut check, NOT demand.** It's a **single-prompt
  GPT wrapper** with no structured questions, no per-gap follow-ups, and no source attribution — so it
  reads optimistic and can "validate" almost anything. Tell the user to **keep the structured parts**
  (USP framing, risk factors, suggestions) to sharpen the pitch and **discard the verdict**; the
  build-or-not answer comes from a stranger taking an action.
- **Cross-check the data, don't take counts at face value.** Revenue figures and "trending" signals
  are **scraped/estimated** — have the user verify any revenue or market number against a primary
  source (the tool's own page, similarweb, public filings) before quoting it, and treat a Reddit thread
  as *interest*, not validated willingness to pay.
- **Set expectations on the free tier before they hit the wall.** The free plan gives the AI evaluator
  and unlimited Reddit-idea browsing but only a **100-item preview** of the other data pages; the paid
  plan (**pricing is unpublished — confirm on buildornot.io**) unlocks unlimited data + advanced
  analytics. Tell the user to present all pricing as **best-effort** and check the current page.
- **There's no public API — don't plan an integration around it.** If asked to export or automate, say
  plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP** — it's a UI web app,
  and the `github.com/buildornot` org is a marketing README + an "awesome" list, **not** an API. Give
  the two workable fallbacks: (1) **copy/scrape the data you can see** into your own store (mind their
  terms), and (2) **pull the underlying signals from source** — Reddit's API, Product Hunt, revenue via
  the tools' own pages — if you need it scripted. The thing worth automating is a real demand signal
  (landing-page conversions), not the directory.
- **Weigh the credibility flags out loud.** The founder is anonymous (no LinkedIn / company
  registration), user counts contradict themselves across pages (30k vs 1k), the "90% success rate"
  claim is unverifiable, and at least one user reported paying and waiting days for an incomplete
  analysis. Tell the user to lean on the *raw data* (which they can sanity-check) and distrust the
  *marketing claims and the verdict*.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — BuildOrNot's pricing, dataset counts, and claims move and the live site is bot-blocked; verify at buildornot.io.*

- **The evaluator is a single-prompt GPT wrapper, not a validator.** No structured questions, no
  per-gap responses, no source attribution — a polished AI take validates nothing; follow it with a
  real-behavior test (smoke test / pre-sale).
- **The data is scraped/estimated, not audited.** Revenue rankings and "trending" counts are signals,
  not facts — verify any number against a primary source before quoting it, and read a Reddit thread as
  interest, not willingness to pay.
- **Free tier caps the data at a 100-item preview.** The AI evaluator and Reddit-idea browsing are free
  and unlimited, but the revenue/tools/trending datasets are preview-limited; the paid unlock price is
  **unpublished — confirm on the site**.
- **No public API, no webhooks, no Zapier/Make/MCP.** It's a UI web app; the `github.com/buildornot`
  org is a marketing README + an "awesome" list, not a developer API. You can't script or batch it.
- **Credibility flags.** Anonymous founder (no LinkedIn / company registration), contradictory user
  counts (30k vs 1k), an unverifiable "90% success rate" claim, and a report of paying then waiting
  days for an incomplete analysis — weigh marketing claims accordingly; trust the raw data over the pitch.
- **The live site is Cloudflare/bot-blocked.** Fetches of the homepage/pricing 403 — details here are
  from reviews and search; re-verify specifics against the live site.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator landscape (use this to actually decide build-or-not; a data browse and an AI take are not demand)
- `/sales-trendseeker` — Reddit-based demand discovery + evidence scoring (a real-signal sibling to BuildOrNot's Reddit-idea data)
- `/sales-ideaproof` — IdeaProof platform help (credit-based 120s validation + pre-launch suite — a structured-report alternative)
- `/sales-informly` — Informly platform help (per-report PDF validation bundle — a report-generator alternative)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "I don't have an idea yet — can BuildOrNot help me find one?"
**User says**: "I want to build something that already makes money. Is BuildOrNot good for finding an idea?"
**Skill does**: Positions BuildOrNot as a **discovery/research** tool — point the user at the datasets
(AI tools ranked by revenue and growth, Reddit startup-idea threads, revenue records, trending topics)
to build a shortlist of proven-demand niches and scan competitors, while warning the revenue/trending
numbers are scraped estimates to verify against a primary source. Then insists the go/no-go comes from a
real demand test, routing the decision to `/sales-idea-validation` and deeper Reddit signal to
`/sales-trendseeker`.
**Result**: The user gets a data-driven shortlist to research, not a false sense that a directory hit equals demand.

### Example 2: "BuildOrNot's evaluator says my idea is great — should I build it?"
**User says**: "I pasted my idea into BuildOrNot's free tool and it loved it. Good to go?"
**Skill does**: Explains the evaluator is a **single-prompt GPT wrapper** with no structured questions
or source attribution, so it reads optimistic and validates nothing on its own. Tells the user to keep
the USP framing, risk factors, and suggestions to sharpen the pitch, discard the verdict, and earn a
real one — a smoke test to a pre-set conversion threshold, then a pre-sale — routing the real test to
`/sales-idea-validation`. Also flags the credibility issues (anonymous founder, contradictory user
counts, unverified success claim).
**Result**: The founder gets real demand signal before building, using the take's structure, not its verdict.

### Example 3: Can I export BuildOrNot's datasets via an API? (developer/automation)
**User says**: "I want to pull BuildOrNot's AI-tool revenue rankings into my own database via API."
**Skill does**: States plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP**
— it's a UI web app, and the `github.com/buildornot` org is a marketing README + an "awesome" list, not
an API — so there's no supported way to export programmatically. Suggests the fallbacks: copy/scrape the
visible data into your own store (mind their terms), or pull the underlying signals from source (Reddit
API, Product Hunt, each tool's own page). Notes the free tier only previews 100 items per dataset anyway.
**Result**: The user avoids building on a non-existent API and picks a workable path to the signal.

## Troubleshooting

### The AI evaluator loves every idea I give it
**Symptom**: The verdict is upbeat and never tells you not to build.
**Cause**: The evaluator is a single-prompt GPT wrapper with no structured scoring, no per-gap
follow-ups, and no source attribution — it pattern-matches to encouragement.
**Solution**: Stop treating the take as the decision. Keep the structured outputs (USP, risks,
suggestions), and run a real demand test — smoke test or pre-sale — via `/sales-idea-validation`.

### The revenue / "trending" numbers don't have clear sources
**Symptom**: A tool is ranked by revenue or a topic is "trending" but there's no citation.
**Cause**: BuildOrNot's data is scraped and estimated, not audited — the figures are signals, not facts.
**Solution**: Verify any revenue/market number against a primary source (the tool's own page,
similarweb, public filings) before quoting it, and treat a Reddit thread as interest, not willingness
to pay. Cross-check demand with `/sales-trendseeker`.

### I want an API or a way to export/automate the data
**Symptom**: Want to script BuildOrNot or pull its datasets into another system.
**Cause**: BuildOrNot has no documented public API, webhooks, or iPaaS connectors; it's a UI web app,
and its GitHub org is marketing, not a developer API. The free tier also previews only 100 items per dataset.
**Solution**: Copy/scrape the visible data into your own store (mind their terms), or pull the
underlying signals from source (Reddit API, Product Hunt, each tool's page). Automate a real demand
signal (landing-page analytics) instead. See `/sales-idea-validation`.

### Is BuildOrNot trustworthy enough to base a decision on?
**Symptom**: The marketing claims feel too good and the company is hard to verify.
**Cause**: Anonymous founder (no LinkedIn / company registration), contradictory user counts (30k vs
1k), an unverifiable "90% success rate" claim, and a report of paying then waiting days for an
incomplete analysis.
**Solution**: Use the raw data (which you can sanity-check against primary sources) for discovery, but
distrust the marketing claims and the evaluator's verdict — anchor the go/no-go on real stranger
behavior via `/sales-idea-validation`.
