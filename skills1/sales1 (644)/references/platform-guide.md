# VenturusAI Platform Reference

## Overview

VenturusAI (venturusai.com) is an AI business-idea validator that turns a written idea into a
framework-structured report — **SWOT, PESTEL, Porter's Five Forces, and VRIO**, plus market sizing,
target-audience personas, financial projections, and a marketing/GTM pass. It's aimed at first-time
founders, solopreneurs, and students who want a fast, structured second opinion. Its differentiator is
**breadth of classic business frameworks in one ~30-second run**; its limitation is that it's a **pure-LLM
tool with no source citations**, so the output is reasoning, not scraped evidence, and scores skew
encouraging.

## Capabilities & automation surface

Each capability below is tagged for what a developer can automate.

- **Business analysis report (SWOT / PESTEL / Porter's Five Forces / VRIO)** — the core output; a structured
  strategic teardown of the idea. *UI-only* (Enterprise API can trigger report generation but is undocumented).
- **Target-audience identification** — named personas with user stories and demographic detail. *UI-only.*
- **Market sizing (TAM / SAM / SOM)** — top-down market estimates. Numbers are LLM-generated, not sourced.
  *UI-only.*
- **Financial projections** — startup cost breakdown, revenue projections, breakeven analysis (deeper on
  Advanced reports). *UI-only.*
- **MVP + Go-to-Market strategy** — recommended MVP scope and GTM plan; **Advanced reports** go deeper. *UI-only.*
- **Marketing & branding** — slogans, positioning, social-media post examples. *UI-only.*
- **Pitch-deck generation** — a generated deck from the analysis (paid tiers). *UI-only.*
- **Vera Search & Charts** — in-app search/visualization layer over analyses (newer feature). *UI-only.*
- **Chat with AI** — follow-up Q&A on the report. *UI-only.*
- **PDF export** — download the report (watermarked on free). *UI-only (manual download).*
- **API access** — generate reports/analyses programmatically. *Enterprise-plan feature, but no public API
  documentation is published — `api.venturusai.com` is behind auth. Treat as unusable for a DIY integration.*

**Report depth: Standard vs Advanced.** Standard reports deliver the framework analysis (SWOT/PESTEL/Porter/
VRIO + audience + basic sizing). **Advanced** reports add the deeper MVP/GTM plan, richer financial
projections, and pitch deck. Advanced reports are quota-limited per plan and unavailable on the free Starter tier.

## Pricing, limits & plan gates

*Best-effort from research (2026-07). Tiers, quotas, and character limits move and differ between sources —
confirm at **venturusai.com/plans**. Users retain commercial rights to reports they generate, even on free.*

| Tier | Reports/mo (Standard) | Advanced/mo | Idea char limit | API | Watermark | Multi-user |
|---|---|---|---|---|---|---|
| **Starter** (free) | ~2 | 0 | ~1,000 | No | Watermarked PDF | No |
| **Lite** | ~10 | ~3 | ~5,000 | No | PDF w/o watermark | No |
| **Pro** (most popular) | ~40 | ~5 | ~10,000 | No | PDF w/o watermark | No |
| **Enterprise** | ~300 | ~100 | ~20,000+ | **Yes** | Custom watermark | Yes |

- **Per-report top-ups** are available on lower tiers (a small per-report charge to exceed the monthly quota).
- **Note on source variance:** some third-party pages report different plan names/prices (e.g. an
  "Agency"/higher-price tier, or a $20 Pro). The plans page is the authoritative source; present figures as
  best-effort.
- **Will my "integration" break on free?** There is no usable API on any self-serve tier — API is
  Enterprise-only and undocumented. Automation is effectively not available regardless of plan.

## Integrations

- **Native connectors:** none documented (no CRM connectors, no Zapier, no Make, no MCP server found).
- **Data flow:** essentially one-way *out* via **manual PDF download**. There is no documented programmatic
  read/write surface for the general user.
- **API (Enterprise):** exists for "automated report generation" per marketing copy, but with no public
  reference — direction and payloads are undocumented. Contact support if on Enterprise.

## Data model

VenturusAI does not publish a public API schema, so there are no official object shapes. The report is a
document, not a queryable object model. Below is a **representative** shape of what a generated analysis
contains, constructed from the documented report sections — not an actual API response.

<!-- Constructed from documented report sections — no public API; verify against the live product. -->
```json
{
  "idea": "A subscription meal-kit for people with kidney disease (renal diet)",
  "report_type": "advanced",
  "score": 78,
  "swot": {
    "strengths": ["Underserved medical-diet niche", "Recurring subscription revenue"],
    "weaknesses": ["Cold-chain logistics cost", "Regulated nutrition claims"],
    "opportunities": ["Partner with dialysis clinics", "Insurance reimbursement angle"],
    "threats": ["Incumbent meal-kit players", "Low switching cost"]
  },
  "pestel": {"political": "...", "economic": "...", "social": "...", "technological": "...", "environmental": "...", "legal": "..."},
  "porters_five_forces": {"new_entrants": "medium", "supplier_power": "low", "buyer_power": "high", "substitutes": "high", "rivalry": "medium"},
  "vrio": {"value": true, "rarity": true, "imitability": "low", "organization": "unproven"},
  "market_sizing": {"tam_usd": 3200000000, "sam_usd": 480000000, "som_usd": 12000000},
  "target_audience": [
    {"persona": "Recently-diagnosed CKD patient", "user_story": "As a CKD patient, I want compliant meals so I don't have to calculate potassium/phosphorus.", "demographics": {"age": "45-70", "income": "mid"}}
  ],
  "financials": {"startup_cost_usd": 85000, "monthly_revenue_projection_usd": 40000, "breakeven_months": 14},
  "gtm": {"mvp": "One meal plan, one metro, clinic referral pilot", "channels": ["clinic partnerships", "renal-diet communities"]}
}
```

**Reading the shape:** every number here (score, TAM/SAM/SOM, financials) is **LLM-generated** — there is
no citation trail behind any figure. Use the qualitative structure (SWOT, Porter, personas) to sharpen
thinking; treat all numbers as illustrative placeholders to replace with real research.

## Quick-start recipes

VenturusAI has **no usable public API**, so these recipes are workflow recipes, not code integrations.
Where automation is genuinely wanted, the right move is to automate the *real* demand signal, not the report.

### Recipe 1 — Get a specific (non-generic) report

1. Write a **rich input** (~500–2,000+ chars): who the customer is, the exact problem, how they solve it
   today, the business model, and any constraints. Thin input is the #1 cause of generic output.
2. Run a **Standard** report first to sanity-check the framing.
3. If the framing is right and you want MVP/GTM/financial depth + a deck, run an **Advanced** report (paid).
4. **Keep** the SWOT, competitor list, risks, and GTM angle to sharpen your pitch; **discard** the verdict
   and every unsourced number.
5. Go earn a real go/no-go: build a smoke-test page (`/sales-funnel`) and drive a little traffic
   (`/sales-audience-growth`), with a pre-set conversion threshold.

### Recipe 2 — Cross-check the verdict (don't trust one score)

```bash
# There is no API — this is a manual cross-check workflow, not a call.
# 1. Run the same idea through a *cited* validator (Preuve) and a *demand-signal* tool (Trend Seeker).
# 2. Compare where they agree/disagree. Disagreement is the useful information.
```
Because VenturusAI has no citations and skews encouraging, pair it with `/sales-preuve` (source-linked,
conservative score) and `/sales-trendseeker` (Reddit demand signal). If VenturusAI says "great" but the
demand signal is flat, believe the demand signal.

### Recipe 3 — "Automate my validation" (the workable version)

You cannot script VenturusAI. What you *can* automate is the real test:

```python
# Pseudocode: automate the demand signal, not the AI report.
# 1. Ship a fake-door landing page (see /sales-funnel).
# 2. Capture signups + "buy" clicks via your analytics/waitlist tool's API.
# 3. Decide go/no-go on the measured conversion rate, not on VenturusAI's score.
threshold = 0.05  # e.g. >=5% of targeted visitors take the action
conversion = signups / targeted_visitors
build = conversion >= threshold
```
The report is a gut check; the conversion number is the evidence.

## Integration patterns

- **No API / webhook pattern applies** — VenturusAI exposes no documented public API, webhooks, Zapier/Make
  modules, or MCP server. Do not design a sync around it.
- **Export pattern:** manual **PDF download** is the only reliable way to get a report out. Watermarked on
  free; clean PDF on paid; custom watermark on Enterprise.
- **Enterprise API:** exists but undocumented — if you're on Enterprise and need it, request the reference
  and credentials from VenturusAI support; don't assume shape or auth.
- **The pattern worth building:** treat any AI validator (VenturusAI included) as a manual, occasional
  pitch-sharpening step, and put your engineering effort into the real demand pipeline (landing page +
  analytics + pre-sale checkout), which *does* have APIs. See `/sales-funnel` and `/sales-audience-growth`.
