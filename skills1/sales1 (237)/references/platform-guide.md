# IdeaProof Platform Guide

Full reference for IdeaProof (ideaproof.io). Best-effort from research (2026-07) — credit costs,
packs, and the feature lineup move; confirm live at ideaproof.io. IdeaProof is **UI-only with no
documented public API**.

## What IdeaProof is

An AI **startup-idea validation + pre-launch suite** positioned as "test your idea in 120s." It scores
an idea across 50+ criteria and then generates the rest of a pre-launch kit (plan, brand, logo, pitch
deck, ad creatives). Trusted-by claim: "10,000+ verified entrepreneurs." Target audience: first-time
founders, indie hackers, and makers who want an affordable alternative to agencies/consultants.

## Module lineup — what each produces

| Module | Produces | Credit cost (approx) |
|---|---|---|
| **Idea Validation** | 100-pt viability score + GO/NO-GO verdict, strengths/weaknesses, risk assessment, across 50+ criteria | ~40 |
| **Market & Competitor Analysis** | TAM/SAM/SOM sizing, competitor SWOT, audience demographics, pricing recommendations | ~100 |
| **Business Plan Generator** | Investor-ready plan — executive summary, financial projections, GTM, funding requirements | ~100 |
| **Brand Strategy** | Brand archetype (12 Jungian options), mission/vision, UVP, voice/tone guidelines | ~50 |
| **Logo & Visual Identity** | AI logos, color palette (hex), typography pairings, landing-page mockups | ~150 |
| **Marketing & Ad Creatives Suite** | Platform-optimized ads (Meta, Google, LinkedIn, TikTok, YouTube, Instagram), email sequences, UGC scripts | ~250 |
| **Pitch Deck** | Investor pitch deck slides | ~120 |
| **Investor Pack** | Bundle: market analysis + business plan + pitch deck | (sum of components) |

> Credit costs are best-effort from research and may change — always read the live cost shown in the
> app before spending. "Validation Report" is the core deliverable (viability score + GO/NO-GO).

## How the viability score & GO/NO-GO are built (and why they run high)

- A **multi-model ensemble** — Claude, GPT, Gemini, and Grok — each handling the stage it's best at,
  combined into one 100-point **viability score** and a GO/NO-GO verdict.
- Grounded partly by **live web scraping** across Reddit, X, Product Hunt, G2, App Store, Upwork,
  YouTube, and LinkedIn, plus static sources (Statista, Crunchbase, TechCrunch, HBR, etc.).
- **Reality check:** independent reviews put the **median score near ~78/100** — the tool passes most
  ideas. The score is fundamentally an **LLM opinion**, not measured demand. Keep the structured parts
  (competitor SWOT, risks, positioning) and treat the number as directional.
- **Sourcing caveat:** marketing claims "50+ authoritative sources" and "89% accuracy," but report
  footers have cited only **~5 sources** and there is **no published accuracy methodology**. Verify
  market-size and financial figures against primary sources before quoting them.

## Pricing — credit-based, no subscription

- **Free:** 90 credits, no card required. Marketed as "4 validations" but ≈ **~2 full validations**
  once you account for downstream modules.
- **Paid packs (one-time, best-effort — sources disagree; some list an Explorer €9.99/150 pack):**

  | Pack | Price (VAT incl.) | Credits |
  |---|---|---|
  | Starter | €19.99 | 150 |
  | Builder | €49.99 | 700 |
  | Founder | €99.99 | 1,500 |

- **Credits never expire.** There is **no monthly subscription** — you buy packs as needed.
- **Referral credits** exist (promotional; ~90-day validity per research). No documented public
  affiliate program as of research — confirm on site.

## Data pipeline

- **Models:** multi-model ensemble (Claude, GPT, Gemini, Grok), orchestrated via OpenRouter internally
  (this is IdeaProof's internal plumbing, **not** a customer-facing API).
- **Live data:** real-time web search / scraping across social + review + freelance platforms for
  demand and competitor signal.
- **Custom NLP** for sentiment and feasibility scoring; brand-archetype engine (12 Jungian archetypes);
  logo/palette/typography generator; multi-platform ad-creative generator.

## Automation & integration reality — no public API

- **No documented public API, no webhooks, no Zapier/Make/native CRM connectors.** IdeaProof is a
  browser tool; the OpenRouter integration it advertises is internal model routing, not a developer API.
- **To get data out:** download or copy the report/assets manually from the app. There's no supported
  batch, export-to-JSON, or scripted path.
- **If you need programmatic validation:** use a tool built for it, or — better — automate the thing
  that actually matters (a smoke-test landing page's conversion rate), not a generated report. See
  `/sales-idea-validation` and `/sales-funnel`.

## Quick-start recipes (no API — manual workflows)

Because there's no API, the "recipes" are efficient manual workflows, not code.

1. **Fast first-pass gut check (free tier).** Run one **Idea Validation** (~40 cr). Ignore the headline
   score; extract the **competitor SWOT + top 3 risks + positioning line**. Feed those into your real
   test. Cost: within free 90 credits.
2. **Pitch-sharpening pass before a smoke test.** Run **Idea Validation** + **Brand Strategy** (~90 cr
   total). Take the UVP and archetype voice into a one-page landing headline; discard the score. Then
   build the page in `/sales-funnel` and drive a little traffic to measure real demand.
3. **Investor-pack starter (paid).** For a warm investor conversation, run the **Investor Pack**
   (market analysis + business plan + pitch deck). Treat every number as a hypothesis to verify against
   primary sources before the meeting; use the deck as a scaffold you rewrite, not a final artifact.

## When IdeaProof is / isn't the right tool

- **Good for:** a fast, broad first-pass structure on an idea (competitors, risks, positioning) and
  cheap starter assets (brand, logo, deck, ad drafts) to launch a smoke test with.
- **Not for:** the go/no-go decision (that needs real behavior — smoke test / pre-sale), deep
  single-domain analysis (a validation-only or research-only tool goes deeper), or any programmatic
  workflow (no API).
