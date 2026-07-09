# Validator AI Platform Reference

## Overview

Validator AI (validatorai.com) is a **free, web-based AI startup-idea validator** used by 300K+
founders. You enter an idea in plain language and it returns a structured AI assessment — a viability
score, market sizing, competitor scan, a simulated customer-reaction Q&A, and an AI mentor chatbot —
plus a paid guided "accelerator" program. It targets first-time founders, makers, students, and vibe
coders who want a fast structured second opinion before building. **It is an LLM opinion, not evidence
of demand**, and it exposes **no documented public API**.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| Idea validator | AI viability **score** + structured feedback (positioning, features, pricing, risks) | UI-only |
| Market-size estimate | AI-estimated market/opportunity sizing | UI-only |
| Competitive analysis | AI-generated competitor/positioning scan | UI-only |
| Customer simulation | Simulated customer reactions, objections, and questions before launch | UI-only |
| AI mentor chatbot | Conversational startup advisor (Accelerator) | UI-only |
| Idea generator | Generates startup ideas from prompts (free) | UI-only |
| Accelerator roadmap | Custom step-by-step startup roadmap (paid) | UI-only |
| Trend indices | Founder Momentum Index / Hesitation Index (aggregate ecosystem data) | UI-only (site content) |

**Everything is UI-only.** There is no public API, no webhooks, and no documented Zapier/Make
integration. The site's own `/api/free-tool.php` endpoint is an internal, unsupported implementation
detail — do not build integrations against it.

## Pricing, limits & plan gates

*Best-effort from research (2026-07) — third-party sources disagree; confirm at validatorai.com/pricing.*

- **Free** — the core idea **validator**, score, and **idea generator** are free with no account paywall.
  This tier is genuinely useful for a first gut check.
- **Accelerator** — a paid guided program (reported around a low monthly price, e.g. ~$15/mo): custom
  startup **roadmap** + **AI mentor** chatbot.
- **Pro** — a higher paid tier (reported around ~$99/mo): deeper **market analysis**, **competitor
  intelligence**, **financial forecasting**, and discounts on adjacent services (e.g. pitch decks).
- Some third-party listings quote different numbers (e.g. a "$12 Professional with API access") — these
  are inconsistent and unverified; treat all pricing as best-effort and confirm live.

**No API rate limits etc. apply** — there's no API to rate-limit. Usage limits (if any) are enforced in the UI.

## Integrations

- **Direction:** none programmatic — outputs are read in the browser. To move a result into your own
  docs/CRM, copy it manually.
- **No native CRM/Zapier/Make connectors** are documented.
- The useful "integration" is conceptual: use Validator AI's competitor list and customer-objection
  simulation to sharpen a pitch, then run the real demand test elsewhere (landing page + waitlist + ads).

## Data model

There is no public API and no documented response schema, so there is no JSON contract to rely on. A
typical validation *result*, as shown in the UI, contains fields like:

```json
{
  "idea": "A budgeting app for freelancers with irregular income",
  "score": 8,
  "category": "Fintech / SMB",
  "market_size_estimate": "AI-estimated (directional only)",
  "competitors": ["...", "..."],
  "customer_simulation": ["likely objection 1", "likely question 2"],
  "next_steps": ["sharpen ICP", "test demand", "..."]
}
```
<!-- ILLUSTRATIVE ONLY — Validator AI has no public API or documented schema; this is a representation of the UI output, not a real response contract. Do not code against it. -->

## Getting the most out of it (in place of quick-start API recipes)

Because there's no API, "recipes" here are usage patterns, not code:

1. **Write a sharp one-line idea before you submit.** Format: *"[specific customer] struggling with
   [specific problem]; we solve it by [specific mechanism] unlike [status quo]."* Vague input →
   generic score. Re-run 2–3 variants and compare which framing scores/reads best.
2. **Harvest the structured parts, discard the verdict.** Copy the competitor list, the positioning
   notes, and especially the **customer-simulation objections** — those are the reusable value. The
   headline score is the least trustworthy output.
3. **Chain into a real test.** Take the sharpened pitch to a fake-door landing page (`/sales-funnel`),
   drive a little traffic, and measure signups/clicks (`/sales-audience-growth`) — that conversion, plus
   a pre-sale, is the go/no-go. Validator AI is step 0, not the decision.

## Automation reality (developer note)

- **No public API.** If a workflow needs programmatic idea validation, Validator AI is the wrong tool —
  it can't be called reliably or supportedly.
- **Don't scrape `/api/free-tool.php`.** It's internal, undocumented, and can change or block without
  notice; building on it is fragile and against the spirit of the tool.
- **Automate the demand signal instead.** The thing worth wiring into dashboards is real behavior —
  landing-page conversion, waitlist growth, pre-sale revenue — not an AI score. See `/sales-idea-validation`.
