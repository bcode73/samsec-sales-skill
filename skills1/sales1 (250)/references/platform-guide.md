# Informly Platform Guide

Full reference for Informly (informly.ai; product at validator.informly.ai). Best-effort from research
(2026-07) — pricing, the report lineup, and page counts move; confirm live at informly.ai. Informly is
**UI-only with no documented public API**.

## What Informly is

An AI **startup-idea validation and pre-launch report generator** — "validate your business idea
instantly with the help of AI." You submit one **freeform description** of your idea and it returns a
single **75+ page PDF** report (page count is marketed inconsistently as 45+ and 75+). Trusted-by
claim: "4,290+ entrepreneurs." Founders: **Prageeth and Edisa Silva** (Melbourne-based; the company is
registered in Anguilla). Target audience: first-time founders, indie hackers, and makers who want an
affordable alternative to weeks of manual market research.

## Framework — Ideate → Validate → Plan

Informly frames its output in three phases (some marketing pages label them Validate / Launch / Grow;
the underlying deliverable is the same PDF):

1. **Ideate** — "receive new insights, ideas and inspiration to refine your business idea."
2. **Validate** — "get a viability score and assessment on your business venture's chance of success."
3. **Plan** — "explore all aspects and considerations of starting a business."

It advertises **23 topics** covered across these sections (business viability, target audience, ideal
team, business model, financials, etc.).

## Report lineup — what the PDF includes (~11 reports/guides)

| Report | Produces |
|---|---|
| **Idea Validation** | Viability score + assessment of the idea's chance of success, strengths/weaknesses |
| **MVP Roadmap** | What to build first; a phased path to a minimum viable product |
| **Landing Page Blueprint** | Copy/structure guidance for a validation landing page |
| **Marketing Strategy** | Channels, positioning, and a go-to-market marketing plan |
| **Sales Blueprint** | Sales approach and conversion guidance |
| **Competitive Positioning** | Competitor landscape and how to position against it |
| **Fundraising Navigator** | Funding options and investor-readiness guidance |
| **Pivot Playbook** | Alternative directions if the core idea is weak |
| **Customer Discovery** | Who to talk to and what to ask |
| **Pitch Deck** | Investor pitch scaffold |
| **Growth Hacking / Launch Plan** | Early-growth tactics and a launch checklist |

> The exact set and labels move — Informly markets "11 comprehensive reports and guides." The
> **Idea Validation** report (viability score) is the core deliverable; the rest are downstream
> planning assets bundled into the same PDF.

## AI Business Advisors (chat)

In the dashboard, Informly offers **AI-powered business advisors** you can chat with for real-time
guidance, specialized across **marketing, finance, sales, technology, fundraising, and operations**.
Treat this as a brainstorming aid grounded in your report — not an accountable human advisor.

## How the viability score & report are built (and why they read optimistic)

- Generated from a **single freeform idea description** — there is **no structured questionnaire or
  pillar-level interrogation** (a noted contrast with gap-surfacing validators like ReadySetLaunch).
- **Grounded with real-time Google Search** so the market context is "not stale" — but the analysis and
  the numbers are still **LLM-generated**.
- **Reality check:** independent reviewers note there is **no independent scoring rubric** and the
  action plans **"assume Go, not No-Go"** — i.e. the report is oriented toward proceeding. The score is
  fundamentally an **AI opinion**, not measured demand. Keep the structured parts (competitors,
  positioning, risks, customer-discovery prompts) and treat the verdict as directional.
- **Sourcing caveat:** verify TAM/market-size and financial figures against primary sources before
  quoting them; real-time search grounds the prose, not necessarily every number.

## Pricing — per report, one-time (no subscription, no credits)

- **$29.99 per report** — a **one-time purchase**. There is **no subscription and no credits system**.
- **Each idea is a separate purchase**, and re-running after a pivot is another $29.99 (the satisfaction
  guarantee below covers a capped re-generation, not unlimited re-runs).
- **Free tier:** **sample reports only** — the full report requires payment (some marketing mentions a
  "7-day trial" framing, but full access is pay-per-report).
- **100% Satisfaction Guarantee:** 7-day refund with a re-generation option (capped, ~2 uses).
- **100% Confidentiality:** inputs are stated to not be shared or used for model training.
- **Payments:** Stripe. **Export:** **PDF only**.
- Prices move — confirm current pricing on informly.ai.

## Data pipeline

- **Model:** LLM-generated analysis (specific model not publicly documented), grounded with **real-time
  Google Search** for current market context.
- **Input:** one freeform text description of the idea, audience, and industry.
- **Output:** a single multi-report **PDF** (viability score + the report lineup above), plus the
  in-dashboard AI business-advisor chat.

## Automation & integration reality — no public API

- **No documented public API, no webhooks, no Zapier/Make, no MCP server, no native CRM connectors.**
  Informly is a browser tool.
- **To get data out:** download the **PDF** from the app and parse/extract it yourself if you need the
  text in another system. There's no supported batch, export-to-JSON, or scripted path.
- **If you need programmatic validation:** use a tool built for it, or — better — automate the thing
  that actually matters (a smoke-test landing page's conversion rate), not a generated report. See
  `/sales-idea-validation` and `/sales-funnel`.

## Affiliate program

- Informly advertises an **affiliate program with ~30% commission** ("limited time"). Relevant if the
  user is a creator/marketer wanting to recommend it — not a developer integration surface.

## Quick-start recipes (no API — manual workflows)

Because there's no API, the "recipes" are efficient manual workflows, not code.

1. **Fast first-pass gut check.** Buy one report (**$29.99**) for a *finalized* idea framing. Ignore the
   headline verdict; extract the **competitor/positioning section + top risks + customer-discovery
   prompts**. Feed those into your real test.
2. **Pitch-sharpening pass before a smoke test.** Take the **Landing Page Blueprint** and **Marketing
   Strategy** sections into a one-page landing headline and channel plan; discard the score. Then build
   the page in `/sales-funnel` and drive a little traffic to measure real demand.
3. **Get the text out of the PDF.** Download the report and run it through a PDF-to-text/extraction step
   locally if you need the sections in a doc, spreadsheet, or notes app — there is no export API.

## When Informly is / isn't the right tool

- **Good for:** a fast, broad first-pass structure on an idea (competitors, positioning, risks, MVP
  roadmap, customer-discovery prompts) and a polished PDF to share with an advisor — cheap relative to
  weeks of manual research.
- **Not for:** the go/no-go decision (that needs real behavior — smoke test / pre-sale), gap-surfacing
  interrogation of weak answers (a structured-questionnaire validator does that), deep single-domain
  analysis (a validation-only or research-only tool goes deeper), or any programmatic workflow (no API).
