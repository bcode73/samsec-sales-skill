---
name: sales-idea-validation
description: "Validating a startup or product idea before you build it — the methodology plus the AI-validator tool landscape for first-time founders, makers, and vibe coders. Covers the validate-before-you-code workflow (problem and demand research, customer interviews, market sizing, willingness-to-pay), the crucial gap between an AI \"idea score\" and real demand, and how to run a fake-door / smoke test, a pre-sale, and a waitlist to get evidence real people want it. Use when you want to validate a startup idea, decide whether an idea is worth building, get a build-or-don't-build verdict, avoid building something nobody wants, interpret an AI validation score, run a smoke test or fake-door test, pre-sell before building, or choose between AI idea-validation tools (Validator AI, DimeADozen, IdeaProof, Trend Seeker, and similar). Do NOT use for growing a pre-launch waitlist audience (use /sales-audience-growth) or building the landing page itself (use /sales-funnel)."
argument-hint: "[describe your idea and what evidence you have so far]"
license: MIT
version: 1.0.30
tags: [sales, validation, pre-launch, strategy]
---

# Idea Validation

Help the user find out whether real people want their idea **before** they spend weeks building it.
Tool-agnostic: covers the evidence ladder (problem → demand → willingness-to-pay), how to read an AI
"idea score" without being fooled by it, and how to run cheap real-world tests (smoke test, pre-sale,
waitlist). The core message: **an AI validator is a gut check, not proof — proof is a stranger taking
an action (an email, a click on "buy", a pre-order).**

## Step 1 — Gather context

Ask only what you can't infer:

1. **What's the idea, in one sentence?** Who's it for and what problem does it solve?
2. **What evidence do you already have?** (multi-select) A hunch · talked to potential users · an AI
   validation score · a landing page · a waitlist · someone offered to pay.
3. **What's the real question you're trying to answer?**
   - A) Is this problem real / painful enough? (problem validation)
   - B) Do enough people want a solution? (demand validation)
   - C) Will they pay, and how much? (willingness-to-pay)
   - D) Should I build this at all — go / no-go?
4. **How much time/money before you'd build?** (Most validation costs under a few hundred dollars and
   1–3 weeks.) And **can you build it yourself** (vibe coder) or are you paying someone?

Skip-ahead: if the user already has a landing page and just wants to test demand, jump to Step 3's
smoke-test section.

## Step 2 — The validation method (the evidence ladder)

Climb from cheapest/weakest to strongest evidence. Stop as soon as you have a clear no; keep going for a yes.

1. **Problem research (cheap, weak alone).** Confirm the problem exists and hurts: read where your
   users already complain (Reddit, niche communities, support forums, review sites), search volume,
   and existing paid alternatives. *No existing solutions* is usually a red flag (no market), not a gold mine.
2. **Customer conversations (do ~10).** Talk to real target users about their problem — **not your
   idea**. Ask about the last time they hit the problem and what they did. People are polite about
   ideas and honest about their past behavior; mine the behavior.
3. **AI idea validation (instant, directional).** Run the idea through an AI validator for a fast
   structured second opinion (score, market size, competitors, risks, GTM angle). Treat it as a
   **hypothesis generator and blind-spot check, not evidence** — the model can sound confident about
   things it invented. Use it to sharpen the pitch and find competitors, then go get real signal.
4. **Demand test / smoke test (real signal).** A fake-door / smoke-test landing page describes the
   product as if it exists and measures whether strangers take an action — join a waitlist or click
   "Get started / Buy". Drive a little traffic (a community post, a small ad budget) and read the
   conversion. A commonly cited bar is **~5%+ of targeted visitors** taking the action = active demand.
5. **Willingness-to-pay / pre-sale (strongest).** Ask for money before it's built: a pre-order, a
   "pay $X now for lifetime/50% off", a paid pilot. **Credit cards are the truth** — a pre-sale that
   converts beats any score. Refund cleanly if you decide not to build.

**How much signal is enough?** More committed = more evidence. An email < a click on "buy" < a card
entered. One pre-sale from a stranger outweighs a 9/10 AI score. Decide a go/no-go threshold *before*
you run the test so you don't rationalize a weak result.

## Step 3 — Tool landscape

Two different jobs — don't confuse them:

- **AI idea validators** (instant AI opinion on the idea): fast, broad, directional; the risk is
  confident hallucination. Good for a first-pass gut check, competitor list, and pitch sharpening.
- **Real-demand tools** (measure what strangers actually do): landing-page builders + waitlists +
  ads + pre-sale checkout. This is where truth lives.

| Tool | Job | Notes |
|---|---|---|
| **Validator AI** (`/sales-validator-ai`) | AI validator | Free core validator + score, market size, competitor + customer-simulation; paid Accelerator/Pro. UI tool, no public API. |
| **DimeADozen** (`/sales-dimeadozen`) | AI validator | **One-time, keep-forever** report (no subscription, credits never expire): free 4-dimension idea score → a 200+ page "build or don't build" report with a named comp-set, unit-economics/retention math, and a marketed 800+ citations — but **citation verifiability and comp-set relevance are disputed** (niche ideas benchmarked against irrelevant giants). UI-only; API is Enterprise/custom only. |
| **Preuve AI** (`/sales-preuve`) | AI validator (source-linked) | 10 agents + a cross-validator search 50+ live sources and **cite every claim**; conservative viability score (median ~55), competitor map, pivots. Free Reality Check → one-time Founder Report; a **Radar** subscription re-scans over time. UI-only, no API — a citation shows the problem is *discussed*, not that anyone will *pay*. |
| **FounderPal** (`/sales-founderpal`) | AI marketing suite (+ validator) | Solopreneur marketing tools (strategy, persona, value prop) with a free idea validator; UI tool, no API — a generated *strategy* is not validated demand. |
| **InstantPersonas** (`/sales-instantpersonas`) | AI persona generator | Named buyer/user personas + website-perception "Insights" + competitor-persona discovery from a short description; UI tool, no API — a generated *persona* is not validated demand. Its free no-signup front door is **User Persona (userpersona.dev)** — same maker, core persona generation only. |
| **PersonaGen** (`/sales-personagen`) | AI persona generator | Detailed user personas (demographics, goals, challenges, motivations, frustrations, channels, quotes) + reusable content-generation prompts, organized into projects and feature-wise sections from a short product description; UI tool, no API — a generated *persona* is not validated demand. Launched free/beta (live site was unreachable at research — verify at personagen.app). |
| **Personadeck** (`/sales-personadeck`) | AI persona generator | Styled persona card from a short description with an explicit **persona-type** choice — **User Persona** vs **Negative Persona** (the skeptic/non-buyer) — plus personality-trait predictions (practical-vs-emotional, introvert-vs-extrovert), editable labels, multilingual generation, and **PDF-only** export; UI tool, no API. Reviewers fault it for *repackaging* thin input — a generated persona is not validated demand. Free/Basic/Medium/Pro (EUR) + AppSumo lifetime deal. |
| **Marketing Mary** (`/sales-marketing-mary`) | Data-grounded, interactive persona (co-pilot) | The **conversational, data-grounded** counterpart to the prompt-only generators: personas are built from your **real CRM/GA4/email/ad data** (not a one-line description) and you **chat with them** to pressure-test subject lines/objections/messaging before a campaign, plus **~10-stakeholder B2B buying-committee** mapping and auto-update as data flows in — inside a research→publish marketing co-pilot. **Subscription** (Starter/Growth/Agency, GBP), UK/EU/GDPR-hosted, **waitlist-stage**; native HubSpot/Salesforce/GA4 connectors but **no public API/webhooks/developer MCP server** (the footer "MCP addendum" is a legal doc). Needs real data volume to beat a generic persona — and talking to a synthetic persona is directional, not demand. |
| **Juma** (`/sales-juma`) | AI marketing workspace (persona is one Flow) | Formerly **Team-GPT**. A broad AI marketing workspace — 700+ **Flows**, shared **Projects** (persistent brand context), multi-model chat (Claude/GPT/Gemini) — where **buyer-persona generation** is one Flow (Prompt Builder → follow-ups → refined prompt → generate → editable page). Its real differentiator in this cluster: it's the **only tool here with a callable MCP server** (`mcp.juma.ai`, OAuth, 40+ tools) — drive persona/brand/content/SEO from Claude Code/Cursor. **Credit-metered** (full-featured Free plan; only successful runs charge; MCP *reads* are free). No REST API/webhooks/Zapier — MCP is the automation surface. A generated persona tracks input depth and is **not** validated demand. |
| **aicofounder** (`/sales-aicofounder`) | AI co-pilot (grounded validator) | Phased idea→launch workspace; multi-agent Reddit/X demand research (grounded, stronger than pure-LLM) + planning agent; UI tool, no API — a generated plan is not validated demand. |
| **IdeaProof** (`/sales-ideaproof`) | AI validator (+ pre-launch suite) | 120s viability score + GO/NO-GO, then bundles plan/brand/logo/pitch/ads; credit-based, UI-only/no API. Score runs high (~78 median) — treat as directional, not demand. |
| **Informly** (`/sales-informly`) | AI validator (+ report bundle) | One freeform idea → a 75+ page PDF: viability score + ~11 reports (MVP roadmap, landing page, marketing/sales, competitive positioning, pitch deck, fundraising, pivot). Priced **per report ($29.99 one-time, no subscription/credits)**; UI-only/no API, PDF export only. No independent scoring rubric — plans "assume Go, not No-Go." |
| **RebeccAi** (`/sales-rebeccai`) | AI validator (+ cheap business plan) | The **cheapest** validate-plus-plan combo: a single text-box idea → a quick evaluation, strengths/weaknesses, and improvement tips, plus an optional **one-time business plan** (15–25 pages). Free tier is capped (a few ideas/day, short output, no customization); Premium unlocks unlimited + longer output. Two cautions unique to it: a **"feedback personality" toggle biases the verdict** toward what you want to hear, and the plan's **financials are AI estimates** for an untested idea; UI-only, no API. (rebecc.ai — not the parked rebeccai.com.) |
| **ReadySetLaunch** (`/sales-readysetlaunch`) | AI validator (interrogation-style) | "Launch Control" walks 13 questions across 7 pillars and **surfaces gaps in weak answers instead of a feel-good score** (anti-gaslighting); deliberately slow (~30–45 min), credit-based/no subscription, UI-only/no API. The gaps are the value; still an AI gut check, not demand. |
| **SoloLaunch** (`/sales-sololaunch`) | AI startup builder (asset kit) | One-line idea → a "startup foundation": names, taglines, logo/brand, market analysis, an **interactive timeline/roadmap**, and marketing strategy. Priced as a **monthly subscription** (free Starter → paid Pro), unlike one-time/credit siblings; UI-only/no API — a generated foundation is not validated demand. (Note: sololaunch.**app**, the co-pilot; sololaunch.**ai** is a separate launch directory → `/sales-launch-directory`.) |
| **Frederick AI** (`/sales-frederick`) | AI teammate/co-founder that **executes** | Unlike report-only siblings, its agents *build and run* things: Coding Agents ship landing pages/apps/APIs, Browser Agents automate web tasks, Background Agents run scheduled work, and Market Insights delivers competitor tracking/market research/social monitoring on a schedule. **Credit-metered** (AI Credits; free tier → paid Plus/Pro). UI-only/no public API. The validation upside: it can **build the smoke-test page itself** — but its market research is *not* demand. |
| **VenturusAI** (`/sales-venturusai`) | AI validator (frameworks) | Runs an idea through **classic strategy frameworks — SWOT, PESTEL, Porter's Five Forces, VRIO** + TAM/SAM/SOM sizing, target-audience personas, financial projections, MVP/GTM, and a pitch deck. **Pure-LLM, no source citations**, and scores **skew encouraging**. Standard vs Advanced reports; free Starter (~2/mo, ~1k-char cap, watermarked) → Lite/Pro → Enterprise. **API is Enterprise-only and undocumented**; UI-only otherwise. |
| **VentureKit** (`/sales-venturekit`) | Business-plan software (funding docs) | Not a "validator" — **AI business-planning software** that turns an idea into a **full ~28-page plan + lender-ready financial forecasts (P&L, balance sheet), a pitch deck, and market research**, plus an AI business assistant, a Radar monitor, and a separate **LLC formation & compliance** service. Angle is **lender/SBA-ready funding docs**; **very generous free tier** (unlimited light plans + ~3 full/mo) → Pro → **Agency** (many plans, for consultants). Plans/financials are **AI estimates** (can read cookie-cutter/invented) and there's **no team collaboration**; **UI-only, no public API**. A fundable plan is a *document*, not demand. |
| **Plannit AI** (`/sales-plannit`) | Business-plan generator | AI business-plan generator (a **questionnaire → a 15–20 page plan** with market analysis, financial projections, and a pitch deck), now rebranded **AIGenerator.com** (AIGenerator LLC) with a marketing-asset suite bolted on and **real-time team collaboration** (unlike VentureKit). **Forecasting is its weakest module** and plans read **generic for niche industries** — replace the numbers and edit heavily. Pricing shifted from **one-time per plan** (old) to a **free tier + monthly** (new); **UI-only, no public API**. (plannit.ai now serves AIGenerator.com; plannit.io is an unrelated app.) A generated plan is a *document*, not demand. |
| **Upmetrics** (`/sales-upmetrics`) | Business-planning suite (mature/team) | Established AI business-planning *suite* (not a validator) — AI Assistant drafts sections, 400+ sample plans, **deep multi-year forecasting** (P&L, cash-flow, break-even, 3-/7-yr, scenarios), **plan-vs-actuals** tracking, **QuickBooks/Xero** import, pitch deck, strategic canvases, **real-time collaboration** (unlike VentureKit) and a **Professional/white-label** tier for consultants. Its edge over the AI-first generators is accounting sync + forecast-vs-actuals + team/advisor features; the catch: AI drafts read **generic** (rich input + hand-edit), **financials are estimates**, accounting sync is **one-way (not live)**, and it's **UI-only, no public API**. A generated plan is a *document*, not demand. (Note: upmetrics.**co** here; upmetrics.**com** is an unrelated impact-reporting tool.) |
| **PrometAI** (`/sales-prometai`) | Business-plan software (connected financials) | AI business-plan generator whose edge is a **connected financial model** — projections, a **DCF valuation**, **stress testing**, and **scenario analysis** that **recalculate together** on input change (reviewers call it the tool whose financials stay "grounded, connected end-to-end") — plus SWOT/VRIO frameworks and a **50+ tool "Entrepreneur Journey."** A **subscription** (unlike the one-time/credit siblings): free **Explore** (view-only, **no export**) → **Basic** (~$55/mo, PDF export) → **Pro** (~$145/mo, PowerPoint + **DCF/stress testing** + term-sheet templates) → Enterprise (FP&A + ERP, sales-gated). Catches: it **invents market figures** (verify every stat), the DCF is a *model* not an appraisal, exports lose formatting, collaboration is very limited, and **most lenders still want a separate financial review**; **UI-only, no public API**. A polished, investor-grade plan is a *document*, not demand. |
| **Bizplanr** (`/sales-bizplanr`) | Business-plan generator (free) | A **free** AI business-plan generator — questionnaire → a full structured plan (executive summary, market analysis, marketing strategy, operations, **basic financials**) in ~5 min, plus standalone SWOT/competitor/financial-model/one-page generators, an AI business advisor, and iOS/Android apps. Monetized by a **one-time paid workspace** (not a subscription) that adds the guided editor, advanced forecasting, and Word/Excel export (free export is typically PDF-only). Financials are **AI estimates**, plans read **generic for niche/complex** businesses, and the standalone tools' outputs **don't cross-reference** each other; **UI-only, no public API**. A generated plan is a *document*, not demand. (Namesake: bizplanr.**ai** here vs the different bizplanner.**ai** / bizplanaipro.com.) |
| **BizPlanner AI** (`/sales-bizplanner`) | Business-plan generator (paid) | A **paid** GPT-4 business-plan generator — questionnaire → a full multi-section plan (executive summary, market/competitor analysis, SWOT, financial projections, industry trends, regulations, next steps) in ~15 min, with an in-browser editor and PDF/Word export. **No free tier**: a **one-time payment (~$9.99)** generates a plan + **2 free full regenerations**, then further generation is metered as **AI-word top-ups**; runs a **30% affiliate**. Financials are **AI estimates** (invents assumptions from thin input) and plans read **generic for niches**; **UI-only, no public API**. A generated plan is a *document*, not demand. (Namesake: bizplanner.**ai** here — paid, no free tier — vs the *free* bizplanr.**ai**.) |
| **BizPlan AI Pro** (`/sales-bizplanaipro`) | Business-plan generator (credit-based) | A **credit-based, pay-per-use** AI business-plan generator (by S. Enterprise) — questionnaire → an "investor-/lender-ready" plan (executive summary, market analysis, competitive landscape, **5-year projections**) across **150+ templates**, **bundled** with a **Startup Idea Validator**, an **AI Business Coach** (metered by separate *Coach credits*), an **AI Decision Analysis** tool, and team collaboration. Sells **credit packs that never expire, no subscription** (Starter/Professional/Enterprise ~$2.99/$15/$39 — Capterra lists a ~$30 Starter, so pricing is **unsettled**); a **plan generation** and **Coach chat** burn **separate meters**, and iterating an idea re-generates several times. Advertised "**97% accuracy**"/"$8M raised" are **unverifiable marketing**; financials are **AI estimates**, plans read **generic for niches**, and the bundled Idea Validator is an AI opinion; **UI-only, no public API**. A generated plan is a *document*, not demand. (Namesake: bizplanaipro.**com** here vs the *free* bizplanr.**ai** / the paid bizplanner.**ai**.) |
| **PlanSnack** (`/sales-plansnack`) | Business-plan builder (free, manual one-page — **not** AI) | The odd one out in this cluster: **not an AI generator** — a **free**, guided **five-step one-page** template you **fill in yourself** (with pre-written example text as a starting point), then download/print/share. **No AI generation, no financial forecasting, no API/integrations** (UI-only). Good for a fast lean one-pager (own clarity, co-founder sync, quick teaser); **not** a lender/SBA/investor package (no multi-year projections). Reach for it when someone wants to *write* a quick one-pager themselves rather than have an AI draft a full plan; a one-pager is still a document, not demand. (Third-party directories overstate its features — verify on plansnack.com.) |
| **WorthBuild** (`/sales-worthbuild`) | AI validator (+ customer discovery) | The validator that **also hands you your first customers**: a fast full report (TAM/SAM/SOM, ~12-competitor map, risks, unit economics, week-by-week roadmap, **Go/Pivot/Stop** verdict) **plus "Your First Customers"** — real people voicing the problem on Reddit/HN/X with **ready-to-send outreach messages** — a free auto-generated landing page + waitlist, a one-click pitch deck, and AI pivots. **One-time per report + a free monthly validation** (no subscription); UI-only, no API. The leads are a conversation shortlist but are *interest, not demand*, and the verdict is an AI opinion — vet the leads, personalize outreach, and take the go/no-go from real behavior. |
| **BuildOrNot** (`/sales-buildornot`) | Discovery data + AI evaluator | Idea *discovery*: browsable datasets of AI tools/startups ranked by revenue & growth, Reddit ideas, revenue records, trending topics — plus a free single-prompt AI evaluator. The data is a shortlist/competitor scan (scraped, verify numbers); the AI take is directional, not demand. UI-only, no API. |
| **VentureVault** (`/sales-venturevault`) | Discovery vault (free) | A **free IdeaBrowser clone**: a browsable **vault of AI-scored, pre-researched startup ideas** (opportunity score = revenue potential / execution difficulty / GTM / community interest) to shortlist a niche worth building. **100% free, no tier**; web + iOS/Android apps, open-source maker. The scores/market analysis are AI estimates (verify numbers) and a browsable idea is not demand; UI-only, no API. (Canonical domain venturevault.**space**, not the dead .co.) |
| **Ideagrape** (`/sales-ideagrape`) | Discovery + AI validator (hybrid) | A **cheaper IdeaBrowser alternative** blending both jobs: browse a **700+ market-scored SaaS-idea database** (search volume, growth, market size) + generate custom ideas, then validate one with an **opportunity score, a WTP analyzer, an assumption validator, a build blueprint, and a growth matrix** (AI Chat on Pro). Free tier is **capped** (a daily generation limit + a limited recent-ideas window); paid **annual** Starter/Pro undercut IdeaBrowser. UI-only, no API — a browsed idea *and* an AI score are estimates, not demand; the WTP price is a hypothesis to pre-sell. |
| **IdeaTwister** (`/sales-ideatwister`) | AI validator (pivot-ranking) | The **"pick the best angle"** tool: takes ONE seed idea, **twists it into 10–25 pivots/variations**, and **ranks every pivot** across five commercial dimensions (buyer urgency, market proof, solo executability, revenue speed, defensibility), returning an interactive dashboard with GTM sketches, "$100K math," and 30-day plans. **One-time pay-per-run** (no subscription; cheapest scores the original only, top tier generates ~25 and fully validates 2); failed runs auto-refund. Reach for it when you *have* an idea and need which *version* to build — not to discover an idea, and a ranked pivot is not demand. UI-only, no API. |
| **Trend Seeker** (`/sales-trendseeker`) | Real demand signal | Reddit-based demand discovery + evidence scoring — closer to real behavior than a pure LLM opinion. |
| **A landing page + waitlist** (`/sales-funnel`, `/sales-audience-growth`) | Real demand test | The actual smoke test; where a go/no-go is earned. |

**Read the AI score critically.** Two validators will disagree on the same idea, and an LLM will
happily rationalize a bad idea. Use AI for structure and blind spots; use a smoke test / pre-sale for
the decision.

## Step 4 — Actionable guidance

- **Lay out the evidence ladder cheapest-first.** Give the user the ordered sequence — problem
  research → ~10 behavior-focused customer conversations → an AI validation (directional) → a
  fake-door / smoke-test landing page → a pre-sale (willingness-to-pay) — and tell them to stop at the
  first clear *no* and keep climbing on a *yes*. Cheaper/weaker signal first, strongest (money) last.
- **Sort every tool into "AI opinion" vs "measures real behavior," and keep the validator's structured
  outputs.** When the user names a tool, classify it: AI idea validators (Validator AI, DimeADozen,
  IdeaProof, …) give an instant opinion that can be confidently wrong; real-demand tests (a landing
  page + waitlist, or Reddit-signal tools like Trend Seeker) measure what strangers actually do — the
  decision belongs to the latter. From any AI validator, **keep the structured parts (competitor list,
  risks, positioning, customer-objection simulation) to sharpen the pitch and discard the verdict.** A
  gap-surfacing *interrogator* (ReadySetLaunch, which flags weak pillars instead of a feel-good score) is
  still AI opinion — its gaps are a sharpening tool, not demand; the go/no-go stays with real behavior.
- **Anchor the decision on real behavior, not an AI score.** Whatever tool the user ran, tell them an
  AI validator is a directional gut check that can hallucinate — the go/no-go must rest on a stranger
  taking an action (waitlist email, "buy" click, or a pre-order). Route the real test to
  `/sales-funnel` (build the page) and `/sales-audience-growth` (drive & capture signups).
- **Push toward willingness-to-pay early.** The strongest cheap signal is money: propose a pre-sale or
  paid pilot ("pay now to lock in lifetime/50% off"), and refund if they don't ship. A single paying
  stranger outweighs a 9/10 score.
- **Set the go/no-go threshold before testing.** Have the user commit to a number first (e.g. "≥5% of
  targeted visitors join, or ≥N pre-orders") so a weak result can't be rationalized after the fact.
- **Validate the problem by past behavior, not the idea.** In interviews, ask about the last time they
  hit the problem and what they did — people flatter ideas but reveal truth in behavior. Aim for ~10 conversations.
- **Cross-check any AI validator with a second source.** Run a second validator or a real demand signal
  (e.g. `/sales-trendseeker` for Reddit demand); disagreement between them is the useful information.
- **Treat "no competitors" as a warning, not a win** — usually it means no market or bad search, not a
  clear field. Have them look harder for how people solve it today (including spreadsheets and duct tape).

## Gotchas

*Best-effort from research (2026-07) — the AI-validator tool set churns fast; verify current tiers.*

- **AI validators hallucinate with confidence.** A high score is not demand; the model can invent
  market sizes and "validate" almost anything. Always follow with a real-behavior test.
- **Two tools, two verdicts.** Idea validators disagree on the same input — no single score is truth.
- **Vanity signups aren't willingness-to-pay.** Free waitlist emails are weak; a card/pre-order is strong.
  Weight your evidence by how much it costs the person to give.
- **Surveys lie, behavior doesn't.** "Would you use this?" over-reports; a click on "buy" or money down
  under-reports honestly. Prefer observed actions to stated intentions.
- **"No competition" usually = no market.** Reframe the absence of alternatives as a demand red flag.
- **Don't outsource the decision to a bot.** The tools inform; the go/no-go is a threshold the founder
  sets and a test the market answers.

## Related skills

- `/sales-validator-ai` — Validator AI platform help (free AI idea validator: score, market size, customer simulation)
- `/sales-preuve` — Preuve AI platform help (source-linked validator — 10 agents cite every claim across 50+ live sources, conservative viability score, plus a Radar monitoring tier; UI-only, no API)
- `/sales-dimeadozen` — DimeADozen platform help (one-time, keep-forever validation report — free 4-dimension score → a 200+ page build-or-don't-build report with a named comp-set + unit-economics math and a marketed 800+ citations; citation verifiability and comp-set relevance disputed; UI-only, API is Enterprise/custom only)
- `/sales-ideaproof` — IdeaProof platform help (120s AI validation + pre-launch suite — viability score/GO-NO-GO, then plan/brand/logo/pitch/ads; credit-based, UI-only)
- `/sales-informly` — Informly platform help (AI idea validation + a 75+ page report bundle — MVP roadmap, landing page, marketing/sales, pitch deck, fundraising; priced per report, UI-only/no API)
- `/sales-readysetlaunch` — ReadySetLaunch platform help (interrogation-style validator — 13 questions across 7 pillars that surfaces gaps instead of an inflated score; credit-based/no subscription, UI-only)
- `/sales-rebeccai` — RebeccAi platform help (the cheapest validate-plus-plan combo — a single-text-box evaluation + strengths/weaknesses + improvement tips, plus a one-time ~15–25 page business plan; a **"feedback personality" toggle biases the verdict** and the plan's financials are AI estimates for an untested idea; UI-only/no API; rebecc.ai, not the parked rebeccai.com)
- `/sales-founderpal` — FounderPal platform help (solopreneur AI marketing suite with a free idea validator; a generated strategy is not validated demand)
- `/sales-instantpersonas` — InstantPersonas platform help (AI buyer/user-persona generator + website-perception insights; a generated persona is not validated demand)
- `/sales-personagen` — PersonaGen platform help (AI user-persona generator — detailed personas + content-generation prompts, organized into projects and feature-wise sections; UI-only/no API; a generated persona is not validated demand)
- `/sales-personadeck` — Personadeck platform help (AI customer-persona generator with an explicit User-vs-Negative persona-type choice, personality-trait predictions, editable labels, multilingual generation, and PDF-only export; UI-only/no API; reviewers fault it for repackaging thin input; a generated persona is not validated demand)
- `/sales-marketing-mary` — Marketing Mary platform help (the data-grounded, **interactive** persona tool — personas built from your real CRM/GA4/email/ad data that you **converse with** to test messaging pre-launch, plus ~10-stakeholder B2B buying-committee mapping and auto-update; a marketing co-pilot, subscription/waitlist-stage, UK/EU/GDPR, native HubSpot/Salesforce connectors but no public API/MCP server; talking to a synthetic persona is directional, not validated demand)
- `/sales-juma` — Juma platform help (formerly Team-GPT — a broad **AI marketing workspace**: 700+ Flows, shared Projects, multi-model chat, where persona generation is one Flow; the **only tool in this cluster with a real MCP server** [`mcp.juma.ai`, OAuth, 40+ tools] to drive persona/brand/content/SEO from Claude Code/Cursor; credit-metered with a full-featured Free plan, no REST API/webhooks; a generated persona tracks input depth and is not validated demand)
- `/sales-venturusai` — VenturusAI platform help (framework-driven validator — SWOT/PESTEL/Porter's Five Forces/VRIO + TAM/SAM/SOM, personas, financials, MVP/GTM, pitch deck; pure-LLM with no source citations, scores skew encouraging; API is Enterprise-only and undocumented)
- `/sales-venturekit` — VentureKit platform help (AI business-planning software — full plan + lender-ready financial forecasts, pitch deck, market research, AI assistant, Radar, and a built-in LLC formation service; generous free tier + an Agency tier for consultants; plans/financials are AI estimates and it's UI-only/no API — a fundable plan is a document, not validated demand)
- `/sales-plannit` — Plannit AI platform help (AI business-plan generator, now rebranded AIGenerator.com — questionnaire → a 15–20 page plan with market analysis, financial projections, a pitch deck, and marketing assets, plus real-time team collaboration; forecasting is weak and plans read generic for niche industries; UI-only/no public API — a generated plan is a document, not validated demand)
- `/sales-upmetrics` — Upmetrics platform help (mature, team-oriented AI business-planning *suite* — deep multi-year forecasting, plan-vs-actuals tracking, QuickBooks/Xero import, pitch deck, strategic canvases, real-time collaboration, and a Professional/white-label tier for consultants; AI drafts read generic and financials are estimates; UI-only/no public API — a generated plan is a document, not validated demand)
- `/sales-prometai` — PrometAI platform help (AI business-plan generator whose edge is a **connected financial model** — projections + **DCF valuation** + stress testing + scenario analysis that recalculate together — plus SWOT/VRIO and a 50+ tool "Entrepreneur Journey"; a **subscription** unlike the one-time/credit siblings; it invents market figures and the DCF is a model not an appraisal; UI-only/no public API — a polished plan is a document, not validated demand)
- `/sales-bizplanr` — Bizplanr platform help (a **free** AI business-plan generator — questionnaire → a full plan with basic financials in ~5 min, plus standalone SWOT/competitor/financial/one-page tools and mobile apps; monetized by a **one-time** paid workspace, not a subscription; UI-only/no public API — a generated plan is a document, not validated demand)
- `/sales-bizplanner` — BizPlanner AI platform help (the near-namesake **paid** GPT-4 business-plan generator — questionnaire → a full multi-section plan in ~15 min, PDF/Word export; **no free tier**, a one-time payment + AI-word top-ups, 30% affiliate; UI-only/no public API — a generated plan is a document, not validated demand; don't confuse bizplanner.ai with the free bizplanr.ai)
- `/sales-bizplanaipro` — BizPlan AI Pro platform help (the third near-namesake — a **credit-based, pay-per-use** business-plan generator bundling a Startup Idea Validator, an AI Business Coach [separate Coach credits], and AI Decision Analysis; credit packs never expire, "97% accuracy" is unverifiable marketing; UI-only/no public API — a generated plan is a document, not validated demand; bizplanaipro.com vs the free bizplanr.ai / the paid bizplanner.ai)
- `/sales-plansnack` — PlanSnack platform help (the cluster's odd one out — a **free, manual one-page** business-plan builder you fill in yourself from a guided five-step template, **not** an AI generator; no financial forecasting, no API/integrations; good for a fast lean one-pager but not a lender/SBA plan — and a written plan is a document, not validated demand)
- `/sales-aicofounder` — aicofounder platform help (AI co-founder with phased idea→launch workflow + grounded Reddit/X demand research; a generated plan is not validated demand)
- `/sales-buildornot` — BuildOrNot platform help (startup-idea discovery data platform + free single-prompt AI evaluator — datasets of revenue-ranked tools, Reddit ideas, and trending topics; the data is a shortlist, the AI take is not demand)
- `/sales-venturevault` — VentureVault platform help (a **free IdeaBrowser clone** — a browsable vault of AI-scored, pre-researched startup ideas with opportunity scores + market analysis; 100% free/no tier, web + iOS/Android, open-source; the scores are AI estimates and a browsable idea is not demand; UI-only/no API; venturevault.space, not the dead .co)
- `/sales-ideatwister` — IdeaTwister platform help (the **"pick the best angle"** validator — twists ONE seed idea into 10–25 ranked pivots across five commercial dimensions [buyer urgency, market proof, solo executability, revenue speed, defensibility] and returns an interactive dashboard with GTM sketches and 30-day plans; **one-time pay-per-run**, failed runs auto-refund; UI-only/no API — a ranked pivot is not validated demand, and it needs a seed idea so it's not a discovery catalog)
- `/sales-ideagrape` — Ideagrape platform help (a **cheaper IdeaBrowser alternative** blending discovery + validation — browse a 700+ market-scored idea database + generate custom ideas, then run an opportunity score, WTP analyzer, assumption validator, build blueprint, and growth matrix; free tier capped by a daily generation limit, paid annual Starter/Pro with AI Chat on Pro; UI-only/no API — a browsed idea and an AI score are estimates, not demand)
- `/sales-worthbuild` — WorthBuild platform help (the validator that **also hands you your first customers** — a fast full report [TAM/SAM/SOM, ~12-competitor map, risks, unit economics, roadmap, **Go/Pivot/Stop** verdict] **plus "Your First Customers"**: real people voicing the problem on Reddit/HN/X with ready-to-send outreach, a free landing page + waitlist, a one-click pitch deck, and AI pivots; **one-time per report + a free monthly validation**, UI-only/no API; the surfaced leads are *interest, not demand* and the verdict is an AI opinion — vet the leads, personalize outreach, decide on real behavior)
- `/sales-sololaunch` — SoloLaunch platform help (AI startup builder/co-pilot — one-line idea → names, logo/brand, market analysis, an interactive timeline, and marketing strategy; monthly subscription, UI-only/no API; a generated startup foundation is not validated demand)
- `/sales-frederick` — Frederick AI platform help (AI teammate/co-founder that *executes* — Coding/Browser/Background Agents build & ship apps/landing pages and run scheduled Market Insights research; credit-metered, UI-only/no public API; it can build the smoke-test page but its market research is not validated demand)
- `/sales-trendseeker` — Trend Seeker platform help (Reddit-based demand discovery + evidence scoring — a real-signal validator)
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture demand once you're testing
- `/sales-funnel` — Build the smoke-test / fake-door landing page the demand test runs on
- `/sales-customer-feedback` — Collect and prioritize feedback once you have early users
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "My AI validator gave it 8/10 — should I build?"
**User says**: "Validator AI scored my idea 8 out of 10 with a big market size. Good to go?"
**Skill does**: Reframes the score as a directional gut check that can be confidently wrong, not proof
of demand; keeps the useful parts (competitor list, GTM angle, pitch sharpening) and prescribes the
real test — a smoke-test landing page with a defined ≥5%-join threshold, then a pre-sale for
willingness-to-pay — routing the build to `/sales-funnel` and signups to `/sales-audience-growth`.
**Result**: The founder gets a go/no-go from stranger behavior instead of betting weeks on a number.

### Example 2: Cheapest way to know if anyone wants it (developer/automation-minded maker)
**User says**: "I can vibe-code the MVP in a weekend, but how do I know it's worth it first?"
**Skill does**: Lays out the evidence ladder cheapest-first — problem research + ~10 behavior-focused
interviews, a fast AI validation for structure/competitors, then a fake-door landing page measuring
"Get started" clicks, and finally a pre-sale — with a pre-committed go/no-go threshold, so a weekend
of building is spent only after a stranger signals real demand.
**Result**: A concrete, under-$100 validation plan that gates the build on evidence, not enthusiasm.

### Example 3: Which validation tool for a go/no-go?
**User says**: "Is there one tool that just tells me build-or-don't-build?"
**Skill does**: Separates AI validators (Validator AI free gut check; DimeADozen's one-time,
keep-forever report — with the caveat its citations and comp-set need vetting) from real-demand tools
(Trend Seeker's Reddit signal; a landing page + waitlist),
recommends using an AI validator to sharpen the pitch and a demand test to decide, and warns that any
single AI verdict can be confidently wrong — cross-check with a second source.
**Result**: The user picks a two-step stack (AI sharpen → real-demand decide) instead of trusting one score.

## Troubleshooting

### "The AI said my idea is great but I'm not sure I believe it"
**Symptom**: A glowing AI validation the founder senses is too easy.
**Cause**: LLM validators pattern-match to plausible-sounding encouragement and can invent supporting
"facts" (market size, demand) — a high score reflects the model, not the market.
**Solution**: Keep the structured outputs (competitors, risks, positioning), discard the verdict, and
earn a real one: run a smoke test to a pre-set conversion threshold and attempt a pre-sale. Cross-check
with a second validator or `/sales-trendseeker`.

### Lots of waitlist signups but unsure it means anything
**Symptom**: The fake-door page collected emails but the founder doesn't trust the signal.
**Cause**: A free email is low-commitment; it shows curiosity, not willingness to pay.
**Solution**: Escalate commitment — add a "reserve your spot for $X" or pre-order step, or ask a subset
to hop on a paid pilot. Weight the decision on the paid conversions, not the raw email count.

### Can't tell if the problem is real
**Symptom**: Interviews are friendly but inconclusive.
**Cause**: The questions asked about the *idea* ("would you use this?") instead of *behavior*.
**Solution**: Re-run ~10 conversations asking about the last time they hit the problem and what they
actually did/spent to solve it. Existing paid workarounds = real problem; shrugs = no pain, no market.
