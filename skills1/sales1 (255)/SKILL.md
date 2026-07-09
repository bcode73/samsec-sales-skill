---
name: sales-instapage
description: "Instapage platform help — AI landing page + post-click conversion platform (instapage.com): drag-and-drop builder, AI Content Generator, AdMap ad-to-page mapping, A/B testing and AI Experiments, Personalization / Dynamic Text Replacement (DTR), heatmaps, AMP, Global Blocks, Collections, and form lead capture. Developer surface: REST API (api.instapage.com/v1, Bearer personal token) for pages / collections / form submissions / analytics, a per-form submit webhook for piping leads to a CRM, and 120+ native + Zapier integrations. Use when an Instapage page won't publish or a custom domain is stuck, A/B testing or heatmaps are gated to a higher plan, leads aren't reaching your CRM, setting up a form-submit webhook or the API to pull submissions, wiring DTR so the page matches your ad keyword, hitting the 200-req/min or daily API quota, or choosing Create vs Optimize vs Convert. Do NOT use for cross-tool funnel/CRO strategy (use /sales-funnel) or checkout-conversion across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in Instapage]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
github: "https://github.com/Instapage"
---

# Instapage Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken page — won't publish, custom domain stuck/slow, page not live
   - B) Build/optimize a page — template, Global Blocks, A/B test, AI Experiments, heatmaps, DTR/Personalization
   - C) Scale ad campaigns — AdMap, Collections, programmatic ad-to-page mapping
   - D) Wire automation — pull form submissions via the API, set up a form-submit webhook, sync leads to a CRM
   - E) Pick or compare a plan (Create / Optimize / Convert)

2. **Which plan are you on?** Create ($99/mo), Optimize ($199/mo), Convert (custom/enterprise), or free trial. Several features below are plan-gated.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, conversion benchmarks across tools | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| A/B testing methodology, heatmap interpretation, statistical rigor | `/sales-vwo` — Run: `/sales-vwo {user's original question}` |
| Email sequences after lead capture | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| Generic CRM/ESP iPaaS wiring (Zapier/Make) | `/sales-integration` — Run: `/sales-integration {user's original question}` |
| Checkout/cart beyond Instapage forms | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |

If the question is Instapage-specific, continue to Step 3.

## Step 3 — Instapage platform reference

**Read `references/platform-guide.md`** for the full platform reference — modules, pricing/plan gates, data model, integration recipes, code examples. For raw endpoint/auth/webhook detail, read `references/instapage-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **Plan gating is the headline issue.** A/B testing, AI Experiments, Personalization/DTR need **Optimize ($199/mo)+**; **heatmaps**, ad-to-page personalization, root-domain publishing, Global Elements, SSO, and direct lead bypass are **Convert (enterprise) only**. Confirm the plan before promising a feature.
- **Leads → CRM** has two paths: the per-form **Form Submit webhook** (real-time POST to your endpoint) and the **REST API** `GET /submissions` poll (backfill/reconcile). The webhook sends internal **field IDs** (`field_1`…), not labels — map them carefully.
- **Webhook 20-second rule.** Your endpoint must respond within ~20s or the form's thank-you message/redirect breaks. Return 200 fast, process async.
- **API quotas are double-gated.** 200 requests/minute per token+IP **and** a daily call quota by plan (Create 5,000 / Optimize 10,000–15,000 / Convert 30,000+), reset 00:00 UTC. Both return 429 with `Retry-After`.
- **Visitor caps.** Each tier caps unique monthly visitors (Create 15,000; Optimize 30,000–50,000); scaling traffic forces an upgrade.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

1. **Pricing is steep and front-loads gating.** Entry **Create is $99/mo** with no A/B testing; the most-cited complaint is that real CRO features sit behind Optimize/Convert and cost climbs fast as traffic grows.
2. **Heatmaps are Convert (enterprise) only.** Not on Create or Optimize — don't promise heatmaps below the custom-priced tier.
3. **A/B testing + AI Experiments need Optimize ($199/mo).** The $99 Create plan can't split-test.
4. **Form-submit webhook sends field IDs, not labels.** Payload keys look like `field_1` — map to your CRM properties or leads land in the wrong fields.
5. **Webhook endpoint must reply in ~20s** or the page's thank-you/redirect fails for the visitor. Ack fast, process in the background.
6. **API has a daily quota on top of 200 req/min.** Plan-based daily cap resets at 00:00 UTC; both limits emit 429 + `Retry-After`. Check the Subscription section for your daily cap.
7. **Personal API tokens inherit the issuer's permissions** and can read every workspace that user can access — treat tokens like passwords and scope team-member access deliberately.

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, conversion optimization, A/B testing methodology across tools
- `/sales-vwo` — A/B testing, heatmaps, and experimentation methodology beyond Instapage's built-in tools
- `/sales-unbounce` — Unbounce platform help (Smart Traffic AI, freeform builder, DTR) — the closest direct competitor
- `/sales-landingi` — Landingi platform help (Lunar AI, programmatic pages) — a lower-cost alternative
- `/sales-leadpages` — Leadpages platform help — a budget landing-page alternative
- `/sales-audience-growth` — Growing an email list (lead magnets, cross-promotion, referral programs)
- `/sales-email-marketing` — Email sequences to run after lead capture
- `/sales-integration` — Connect Instapage to a CRM or ESP via Zapier, Make, or the API
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Pipe new form leads into a CRM via the API
**User**: "How do I automatically get new Instapage form submissions into my CRM?"
**Approach**: Two options — (1) per-form **Form Submit webhook** (page editor → form → integrations → Webhook, POST to your endpoint, real-time, but it sends `field_1`-style IDs so map fields and reply within 20s); (2) **REST API** poll of `GET /v1/workspaces/{workspaceId}/submissions` with the `Authorization: Bearer` header, best for backfill/reconcile. Show the cURL, note pagination via `page`, and handle 429 with `Retry-After`. Pull the recipe + JSON from `references/platform-guide.md` / `references/instapage-api-reference.md`.

### Example 2: Page won't publish on a custom domain
**User**: "I connected my domain but the page still isn't live."
**Approach**: Confirm the subdomain is added in account settings and DNS (A/CNAME) points to Instapage, then wait for propagation + SSL. Note **root-domain publishing is Convert-only** — on Create/Optimize you publish to a subdomain. Rule out propagation before assuming a bug.

### Example 3: Choosing a plan for split testing + heatmaps
**User**: "I want A/B testing and heatmaps — which plan?"
**Approach**: **A/B testing + AI Experiments require Optimize ($199/mo)**; **heatmaps require Convert (custom/enterprise)** — they are not on Optimize. If heatmaps are essential, budget for Convert or use a separate tool (e.g. Microsoft Clarity) on Optimize. Explain visitor caps and daily API quota so they size it correctly.

## Troubleshooting

### Form leads not reaching my CRM
**Symptom**: The form submits and shows thank-you, but leads never arrive downstream.
**Cause**: Webhook field mapping wrong (payload uses internal `field_1` IDs, not labels), the receiving endpoint timed out (>20s), or the integration disconnected.
**Solution**: Re-map each `field_N` to the correct CRM property, make the endpoint return 200 within ~20s (queue the work), and confirm HTTPS. As a backstop, reconcile with `GET /v1/workspaces/{workspaceId}/submissions`.

### API calls suddenly return 429
**Symptom**: Requests start failing with HTTP 429.
**Cause**: You hit the 200 requests/minute limit (per token + IP) or exhausted the plan's **daily** API quota (resets 00:00 UTC).
**Solution**: Honor the `Retry-After` header with exponential backoff; spread bulk jobs across the day; check the daily cap in the app's Subscription section and upgrade if the integration needs more headroom.

### A feature I expected is missing
**Symptom**: A/B testing, Personalization/DTR, or heatmaps aren't available.
**Cause**: Plan gating — A/B testing/AI Experiments/Personalization need Optimize; heatmaps + ad-to-page personalization + root-domain publishing need Convert.
**Solution**: Verify the current plan in billing before troubleshooting. Upgrade to the tier that unlocks the feature, or substitute a separate tool (e.g. Clarity for heatmaps) where cost-prohibitive.
