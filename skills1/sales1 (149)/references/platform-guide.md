# DimeADozen Platform Reference

<!-- Source: https://www.dimeadozen.ai + https://www.dimeadozen.ai/build-your-own (fetched 2026-07-05) -->

## Overview

DimeADozen (dimeadozen.ai) is an **AI startup-idea validation report generator** for first-time
founders, indie hackers, career-changers, and makers. You paste an idea and get a free **4-dimension
idea score**, then can buy a **keep-forever** validation report (Starter or a 200+ page Entrepreneur
report) with a named competitor set, unit-economics/retention math, a risk register, and a
build-or-don't-build verdict. Primary differentiators vs sibling validators: a **one-time purchase
model** (no subscription; credits never expire) and a marketed **800+ URL citations** across 140+
sources — though both the citation claim and the relevance of its competitor benchmarks are **disputed**
by reviewers. ~100,000+ ideas analyzed since 2023. **It is a UI web app; the report is an LLM opinion,
not evidence of demand.**

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| **Idea score (free)** | 4-dimension assessment — Market / Validation / Execution / Differentiation — in ~2 minutes, unlimited submissions, personal use | UI-only |
| **Starter report** | 7 sections (business overview, user pain points, revenue & market, monetization, kill-risks, timing, execution path) + 3 comparable companies + 3 execution recommendations | UI-only (download/copy) |
| **Entrepreneur report** | 200+ page report — full comp-set with source-linked retention benchmarks, unit-economics & cohort analysis, risk register with mitigations, investor-memo skeleton; commercial use permitted | UI-only (download/copy) |
| **Citations / sources** | Marketed 800+ URL citations across 140+ named sources ("validation with receipts") — *verifiability disputed* | UI-only |
| **Enterprise** | Bulk/discounted pricing, revenue-share, **hosted white-label**, **API access**, priority processing | **API-accessible (Enterprise/custom only)** — no public docs |

**No public API, webhooks, Zapier/Make, or MCP on any self-serve plan.** The only programmatic surface is
the **Enterprise-tier API/white-label**, which is custom and sales-gated (no published documentation).
For all self-serve tiers, the report is retrieved by downloading/copying it in the UI.

## Pricing, limits & plan gates

*Best-effort from research (2026-07) — DimeADozen's own `/build-your-own` page is the primary source; a
competitor comparison page quoted different figures. Confirm at dimeadozen.ai.*

| Tier | Price (best-effort) | Includes | Gate |
|---|---|---|---|
| **Solo** | Free (no card) | 4-dimension idea score, unlimited submissions, personal use only | — |
| **Starter** | ~$9 one-time | 7-section report, 3 comparable companies, 3 execution recommendations | one-time purchase |
| **Entrepreneur** ("Most Popular") | ~$129 one-time | 200+ page report, full comp-set + source-linked retention benchmarks, unit-economics/cohort analysis, risk register, investor-memo skeleton, commercial use | one-time purchase |
| **3-Pack** | ~$179 one-time | Three full Entrepreneur reports; **no expiration on credits** | one-time purchase |
| **Enterprise** | Custom (contact sales) | Bulk discounts, revenue share, hosted white-label, **API access**, priority processing/support | sales-gated |

- **Model:** one-time purchases, **no subscription**; report credits **never expire** ("lifetime credits").
- **Guarantee:** **14-day money-back guarantee** / satisfaction refund.
- **Commercial use:** permitted on the Entrepreneur tier (Solo is personal-use only).
- **Note on price drift:** a competitor's comparison page quoted ~$59/credit and a ~$139 3-pack; the
  platform's own page quotes the figures above. Treat every number as best-effort and re-verify.

## Integrations

- **Self-serve plans:** none. No native CRM connectors, no Zapier/Make, no webhooks, no MCP. Data flow is
  one-way and manual — you download or copy the report out of the UI.
- **Enterprise (custom):** **API access** and **hosted white-label** for organizations that want volume +
  integration (the marketing frames the buyers as VCs pre-screening deal flow, accelerators running
  portfolio diligence). No public API documentation — the shape, auth, and endpoints are arranged through
  sales. Do not assume a REST surface exists for a normal paid account.

## Data model

DimeADozen does not publish a data model or API schema for self-serve accounts. The user-facing objects
are the **idea score** and the **report**. Representative shapes below are **constructed** to illustrate
what a report contains — they are **not** a real API contract.

<!-- Constructed from the product UI/marketing — NOT a documented API; verify against any Enterprise contract -->

```json
// Idea score (free) — conceptual shape
{
  "idea": "A newsletter that curates grant deadlines for indie game devs",
  "score": {
    "market": 61,
    "validation": 48,
    "execution": 72,
    "differentiation": 55
  },
  "scale": "0-100 per dimension"
}
```

```json
// Entrepreneur report — conceptual section list (not an API payload)
{
  "verdict": "build | don't build",
  "sections": [
    "business_overview",
    "user_pain_points",
    "revenue_and_market",
    "monetization",
    "kill_risks",
    "timing",
    "execution_path",
    "comparable_companies",        // named comp-set — VET each for relevance
    "unit_economics_and_cohorts",  // retention math — AI estimates, verify
    "risk_register_with_mitigations",
    "investor_memo_skeleton"
  ],
  "citations": "marketed 800+ URLs across 140+ sources — verifiability disputed"
}
```

**Key caution:** the `comparable_companies`, `revenue_and_market`, and `unit_economics_and_cohorts`
values are **AI-generated estimates**. Niche ideas have been benchmarked against irrelevant giants; open
a sample of the cited sources and confirm each comparable is real and relevant before trusting a number.

## Quick-start recipes

DimeADozen has **no self-serve API**, so these are the realistic automation patterns.

### Recipe 1 — Get the report data out of the UI (no API)

There is no export endpoint on self-serve plans. Download/copy the report, then parse it locally.

```bash
# There is NO public API. Do NOT do this — it will 404 / is unsupported:
#   curl https://api.dimeadozen.ai/v1/reports/123   # <- does not exist for self-serve
# Instead: download the report (PDF/HTML) from the dashboard, then parse it.
```

```python
# Parse a downloaded DimeADozen report PDF into structured fields for your own store.
# (Self-serve has no API; this operates on the file you exported from the UI.)
from pypdf import PdfReader

reader = PdfReader("dimeadozen_entrepreneur_report.pdf")
text = "\n".join(page.extract_text() or "" for page in reader.pages)

# Naive section split — adapt to the actual headings in your report
sections = {}
for heading in ["Business Overview", "Comparable Companies", "Unit Economics",
                "Risk Register", "Kill Risks", "Execution Path"]:
    idx = text.find(heading)
    sections[heading] = idx  # locate; then slice to the next heading

print({k: (v >= 0) for k, v in sections.items()})
# NOTE: comp-set + market/retention numbers are AI estimates — verify before ingesting as fact.
```

**Gotchas:** no stable schema; headings and page counts change between reports — don't hard-code offsets.

### Recipe 2 — Enterprise API (custom, sales-gated)

If an organization has an Enterprise contract, DimeADozen provides API access — but there are **no public
docs**, so the auth method, base URL, and endpoints come from the sales/onboarding process.

```bash
# Illustrative ONLY — confirm the real base URL, auth header, and paths with DimeADozen sales.
# curl -H "Authorization: Bearer $DIMEADOZEN_ENTERPRISE_KEY" \
#      https://<enterprise-base-url>/reports \
#      -d '{"idea": "..."}'
```

**Gotchas:** don't design a production integration against assumed endpoints — get the contract's actual
spec first. White-label/API is a bulk/enterprise offering, not something a $129 account unlocks.

### Recipe 3 — Automate the thing that actually matters (real demand)

The report isn't demand. The automation worth building is a **smoke test**: a landing page whose "Get
started / Pre-order" clicks are the signal. DimeADozen has no role here — route to `/sales-funnel` (page)
and `/sales-audience-growth` (drive + capture). Keep the DimeADozen comp-set/risks to sharpen the pitch.

## Integration patterns

- **No self-serve sync architecture exists** — there's no API/webhook to sync from. If you need report
  data in a CRM or warehouse, the pattern is **manual export → parse → load** (Recipe 1), and you own the
  brittleness (schema drift, AI-estimate data quality).
- **Enterprise integration** is bespoke: negotiate the API surface, then treat it like any undocumented
  vendor API — capture a real response first, verify auth and pagination, and don't trust marketed field
  claims (e.g. citations) without inspecting a live payload.
- **The durable pipeline is the demand test, not the report** — instrument landing-page conversions
  (analytics + a webhook from your waitlist/checkout tool) and let that, not the AI verdict, drive
  go/no-go. See `/sales-idea-validation` for the end-to-end evidence ladder.
