---
name: sales-landingi
description: "Landingi platform help — AI landing page builder (landingi.com): Lunar AI page generator, drag-and-drop Visual Builder, 400+ templates, form builder, A/B testing, EventTracker, Smart Sections, Dynamic Text Replacement (DTR), multi-language pages, programmatic landing pages, lead capture, and the Orbit MCP server. Developer surface: REST API (api.landingi.com, X-Api-Key or OAuth 2.0 Bearer) for landing pages / leads / form submissions, per-form webhooks, a WordPress plugin, and 170+ Zapier integrations. Use when your Landingi page won't publish or a custom domain is stuck, A/B testing or programmatic pages are gated to a higher plan, AI credits run out, leads aren't syncing to your CRM or email tool, setting up a form webhook or the API to pull leads, wiring DTR so the page matches your ad keyword, or choosing Landingi Build vs Optimize vs Scale. Do NOT use for cross-tool funnel/CRO strategy (use /sales-funnel) or checkout-conversion across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in Landingi]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
github: "https://github.com/landingi"
---

# Landingi Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken page — won't publish, custom domain stuck/slow, page not showing
   - B) Build/optimize a page — template, form, A/B test, EventTracker, Smart Sections, DTR
   - C) Scale — programmatic landing pages from a feed, agency sub-accounts, multi-language
   - D) Wire automation — pull leads via the API, set up a form webhook, sync leads to a CRM/ESP
   - E) Use AI — Lunar page generator, Solis insights, the Orbit MCP server, AI credits
   - F) Pick or compare a plan (Build / Optimize / Scale / Enterprise)

2. **Which plan are you on?** Build ($24/mo), Optimize ($119/mo), Scale ($229/mo+), Enterprise, or free trial. Several features below are plan-gated.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, conversion benchmarks across tools | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| A/B testing methodology, heatmaps, statistical rigor | `/sales-vwo` — Run: `/sales-vwo {user's original question}` |
| Email sequences after lead capture | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| Generic CRM/ESP iPaaS wiring (Zapier/Make) | `/sales-integration` — Run: `/sales-integration {user's original question}` |
| Checkout/cart optimization beyond Landingi's built-in payments | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |

If the question is Landingi-specific, continue to Step 3.

## Step 3 — Landingi platform reference

**Read `references/platform-guide.md`** for the full platform reference — modules, pricing/plan gates, data model, integration recipes, code examples. For raw endpoint/auth/webhook detail, read `references/landingi-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **Publishing & domains**: Custom-domain connection is the #1 friction point — it's slow and not fully automated. Add the domain/subdomain in account settings, point DNS (A/CNAME), then wait for propagation before reporting it "broken."
- **Plan gating**: A/B testing, EventTracker, Smart Sections, and multi-language need **Optimize+**; programmatic pages, agency sub-accounts, and the **Orbit MCP server** need **Scale+**. Confirm the plan before promising a feature.
- **AI credits**: Lunar generation and AI copy/SEO consume a monthly **credit** pool — heavy AI use exhausts it; buy a credit add-on or upgrade rather than expecting unlimited generation.
- **Design ceiling**: The builder trades pixel-level freedom for speed; advanced layouts often need a little HTML/CSS. Set that expectation versus Unbounce/Instapage freeform canvases.
- **DTR for ads**: Dynamic Text Replacement swaps page keywords from the ad's URL params to keep message match (and Quality Score) high on PPC traffic.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

1. **Custom-domain setup is slow and clunky.** The single most common complaint — domain connection is not fully automated and DNS propagation adds delay. Verify DNS and wait before troubleshooting.
2. **A/B testing is gated to Optimize ($119/mo) and up.** The cheap Build plan ($24/mo) can't split-test — a real limit for CRO.
3. **AI features burn metered credits.** Lunar and AI copy/SEO draw down a monthly credit pool; running out blocks generation until you top up or upgrade.
4. **Programmatic pages and the Orbit MCP server are Scale-tier ($229/mo+).** Don't plan a bulk-page or MCP workflow on a lower plan.
5. **The visual builder is less freeform than Unbounce/Instapage.** Sections snap to structure; pixel-precise custom layouts may need HTML/CSS.
6. **Visit caps per plan.** Each tier caps monthly visits (Build 2,000; Optimize 30,000); overages can throttle or require an upgrade — size the plan to expected traffic.
7. **Webhooks are form-submission scoped and undocumented for signing.** Set per-form in the form's Integrations tab; no published HMAC signature — validate payloads yourself.

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, conversion optimization, A/B testing methodology across tools
- `/sales-vwo` — A/B testing, heatmaps, and experimentation methodology beyond Landingi's built-in tools
- `/sales-leadpages` — Leadpages platform help (landing pages, pop-ups, alert bars, Leadmeter) — a close lower-cost alternative
- `/sales-unbounce` — Unbounce platform help (Smart Traffic AI, freeform builder, DTR) — a higher-end PPC alternative
- `/sales-instapage` — Instapage platform help (AdMap, AI Experiments, Personalization/DTR, heatmaps) — the premium post-click alternative
- `/sales-audience-growth` — Growing an email list (lead magnets, cross-promotion, referral programs)
- `/sales-email-marketing` — Email sequences to run after lead capture
- `/sales-integration` — Connect Landingi to a CRM or ESP via Zapier, Make, or the API
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Pull leads into a CRM via the API
**User**: "How do I automatically get new Landingi form leads into my CRM?"
**Approach**: Two options — (1) per-form **webhook** (form Settings → Integrations → Webhook, POST to your endpoint, map fields), best for real-time; (2) **REST API** poll of `GET /forms/{formId}/submissions` with the `X-Api-Key` header (or OAuth Bearer), best for backfills/reconciliation. Show the cURL, note 429 retry, and map fields to CRM properties. Pull recipe + JSON from `references/platform-guide.md` / `references/landingi-api-reference.md`.

### Example 2: Page won't publish on a custom domain
**User**: "I connected my domain but the page still won't go live."
**Approach**: Confirm the domain/subdomain is added in account settings, DNS records (A or CNAME) point to Landingi, and propagation has completed (can take hours). Domain connection being slow/manual is a known gotcha — rule that out before assuming a bug; check SSL provisioning status too.

### Example 3: Choosing a plan for split testing + bulk pages
**User**: "I want A/B testing and to spin up 200 pages from a spreadsheet — which plan?"
**Approach**: A/B testing needs **Optimize ($119/mo)**; **programmatic landing pages** (bulk generation from a data source) need **Scale ($229/mo+)**. For 200 pages from a feed, Scale is required; explain the visit caps and credit pool so they size it correctly.

## Troubleshooting

### Custom domain connected but page not live
**Symptom**: Domain added but the published page 404s or shows no SSL.
**Cause**: DNS not propagated, wrong A/CNAME target, or SSL still provisioning. Domain connection is known to be slow and not fully automated.
**Solution**: Re-check the A/CNAME against Landingi's published target, wait for DNS + SSL to finish, and test in incognito. Contact support only after propagation completes.

### Leads not reaching my CRM/email tool
**Symptom**: Form submits on the page but leads never arrive downstream.
**Cause**: Integration disconnected, webhook field mapping wrong, or double opt-in holding the contact.
**Solution**: Reconnect the integration or re-check the form's Webhook URL + field map. Confirm the webhook fires on submit. Check the ESP's pending/unconfirmed queue for double opt-in. As a backstop, reconcile via `GET /forms/{formId}/submissions`.

### AI generation stopped working mid-month
**Symptom**: Lunar or AI copy refuses to generate.
**Cause**: The monthly AI **credit** pool is exhausted.
**Solution**: Buy a credit add-on (pay-as-you-go bundles) or upgrade the plan for a larger monthly allotment. Credits reset on the billing cycle.
