---
name: sales-quickhunt
description: "Quickhunt (quickhunt.app) platform help — affordable all-in-one customer-feedback suite for SaaS: feedback boards (ideas + upvoting/comments), public roadmap, changelog, in-app messages, knowledge base, AI assistant, and live chat — a Canny/Frill/Featurebase/Upvoty alternative with a genuinely free lifetime tier. Developer surface: the REST API is gated to the top Premium plan and undocumented, integrations (Slack/Zapier/viaSocket/GitHub/HubSpot/Jira) are Growth-tier, and there's no MCP server — so it's mostly a no-code intake tool. Use when getting feedback out of Quickhunt without an API, wiring it into Slack/Jira/GitHub/HubSpot via Zapier or viaSocket, embedding the widget, mapping statuses to a roadmap and shipping a changelog, picking a plan (Free/Starter/Growth/Premium), or choosing Quickhunt vs Frill/UserJot/Canny. Do NOT use for VoC survey-program strategy (use /sales-customer-feedback) or public review generation (use /sales-customer-reviews)."
argument-hint: "[describe what you need help with in Quickhunt]"
license: MIT
version: 1.0.1
tags: [sales, customer-feedback, product, platform]
github: "https://github.com/QuickHUnt"
---

# Quickhunt Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Get feedback **out** of Quickhunt automatically — note the **REST API is gated to the top Premium plan ($99/mo) and undocumented publicly**. On lower plans, use Zapier/viaSocket or native connectors instead.
   - B) Wire Quickhunt into **Slack / Jira / GitHub / HubSpot / ClickUp / Zapier / viaSocket** (these are **Growth-tier, $49/mo**; Free and Starter have **no integrations** at all)
   - C) Embed the **feedback/changelog/docs widget** (embed, modal, sidebar, popover, banner) or host the portal on a **custom domain** (Starter+)
   - D) Organize **feedback boards**, an idea's **status**, the **public roadmap**, and ship a **changelog** (scheduled changelog is Starter+)
   - E) Run **in-app messages** — surveys, checklists, banners, posts — or set up the **knowledge base / AI assistant / live chat**
   - F) Decide Quickhunt vs Canny/Frill/UserJot/Featurebase, or pick a plan (Free / Starter $29 / Growth $49 / Premium $99)

2. **Code or no-code?** Below Premium there's no API, so "code" mostly means webhook receivers fed by Zapier/viaSocket; "no-code" means Zapier + viaSocket + native connectors (Growth+).

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Voice-of-customer / NPS/CSAT/CES survey **program** strategy across tools | `/sales-customer-feedback {question}` |
| Aggregating **unsolicited** feedback across reviews/social/support | `/sales-noisely {question}` |
| Public review **generation** strategy (Trustpilot/G2) | `/sales-customer-reviews {question}` |
| In-app message / onboarding survey **strategy** across tools | `/sales-in-app-messaging {question}` |
| Connecting Quickhunt to a CRM/PM tool generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-customer-feedback choose a product-feedback board tool`".

## Step 3 — Quickhunt platform reference

**Read `references/platform-guide.md`** for the full reference — the Feedback/Roadmap/Changelog/In-App-Messages/Docs/AI/Live-Chat module map (what's Zapier-automatable vs API-only vs UI-only), the integration surface (Slack, Zapier, viaSocket, ClickUp, GitHub, HubSpot, Jira), pricing tiers + the integration ($49 Growth) and API ($99 Premium) plan gates, the data model, and quick-start recipes (push new ideas out via Zapier; turn feedback into a GitHub issue; embed the widget).

**Read `references/quickhunt-api-reference.md`** for the developer surface — the **"API is Premium-only and undocumented publicly"** reality and the no-code substitutes (**Zapier**, **viaSocket**, **native connectors**, **webhooks**, **embeddable widget**), plus a **Gaps** section noting which details (REST endpoints, auth scheme, webhook payloads) are gated/JS-rendered and must be confirmed in-account.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **The API is Premium-only and undocumented — design around it.** Quickhunt's REST API is listed only on the **Premium ($99/mo)** plan, and no public API docs were found. Below Premium, move feedback with **Zapier** or **viaSocket** (both bridge to thousands of apps), the native **GitHub/Jira/HubSpot/ClickUp/Slack** connectors, or **webhooks** — don't promise an API pull unless the account is on Premium, and confirm endpoints/auth in-account.
- **Integrations start at Growth ($49/mo).** Free and Starter have **no integrations** — so a customer on Free/Starter cannot use Zapier, Slack, GitHub, etc. at all. If their plan is Free/Starter and they need automation, the answer is "upgrade to Growth" before any wiring.
- **The free tier is the real differentiator.** Unlike FeedBear/Rapidr (no free tier) and cheaper to start than Frill, Quickhunt's **lifetime Free** plan (1 board, 1 roadmap, AI assistant, unlimited posts + changelog) makes it a strong "just start collecting feedback" pick — at the cost of branding, custom domain, and integrations.
- **It bundles more than a feedback board.** On top of boards/roadmap/changelog it adds **in-app messages** (surveys/checklists/banners), a **knowledge base**, an **AI assistant**, and **live chat** — closer to a lightweight Intercom + feedback combo. If they only need a board, a cheaper single-purpose tool may fit better; if they want one tool for feedback + announcements + help docs, the bundle is the draw.
- **Mind the per-feature plan gates.** Custom domain + remove branding + scheduled changelog + analytics + conditional logic are **Starter+**; integrations are **Growth+**; API + dedicated account manager are **Premium**. Extra team members are **+$10/mo each** on every plan.
- **It's a feedback-board tool, not a VoC survey suite.** Quickhunt collects *solicited* board feedback + roadmap + changelog (+ in-app messages). For survey *program* strategy use `/sales-customer-feedback`; for mining *unsolicited* feedback across reviews/social use `/sales-noisely`.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — modules/pricing captured from quickhunt.app (homepage, /pricing, /integrations) and third-party roundups on this date; no public API/developer docs page exists (`/docs` 404s). Re-verify plan gates, the API surface, and webhook details in-account before relying on them.*

1. **The REST API is Premium-only ($99/mo) and undocumented publicly.** API access is listed only on the top Premium tier, and no developer/API docs page was found (the `/docs` path 404s). Treat the API as unavailable below Premium, and confirm its endpoints/auth in-account — don't reconstruct or assume them.
2. **No integrations on Free or Starter.** All integrations (Slack/Zapier/ClickUp/GitHub/HubSpot/Jira/viaSocket) require **Growth ($49/mo)**. A Free or Starter customer literally cannot connect anything — the fix is an upgrade, not a config change.
3. **Webhooks have no published schema or documented HMAC.** Webhooks are mentioned as a feature but no payload schema or signing scheme is documented. If you wire them, **capture a live delivery** to learn the shape, and secure the endpoint by secret URL / IP allowlist rather than assuming HMAC.
4. **Intercom is "coming soon."** The Intercom integration was marked coming-soon at research time — don't promise it. Verify availability in-account.
5. **Per-feature gates are easy to miss.** Custom domain, remove branding, scheduled changelog, analytics, and conditional logic are **Starter+**; the AI assistant is on Free but live chat is a newer add. Check the exact tier before promising a feature.
6. **Extra seats cost $10/mo each.** Team members are billed per-seat on top of every plan (Growth includes 5). Factor this into any "what will this cost" answer.

## Related skills

- `/sales-customer-feedback` — Voice-of-customer / survey program strategy across tools (Quickhunt is one feedback-board option) — program design, metric choice, tool selection. Install: `npx skills add sales-skills/sales --skill sales-customer-feedback -a claude-code`
- `/sales-frill` — Affordable feedback-board competitor that ships a **documented REST API + HMAC-SHA256-signed webhooks** at ~$25/mo — the pick when programmatic reads matter and you don't want to pay $99 for an API. Install: `npx skills add sales-skills/sales --skill sales-frill -a claude-code`
- `/sales-userjot` — AI-first feedback board with a REST API + MCP server + no-per-seat pricing and a free tier — the closest contrast (free tier + real API). Install: `npx skills add sales-skills/sales --skill sales-userjot -a claude-code`
- `/sales-sleekplan` — AI feedback suite (auto-categorization + MCP server) with a REST API + JWT SSO and a free Indie tier — contrast when you want AI triage plus an API. Install: `npx skills add sales-skills/sales --skill sales-sleekplan -a claude-code`
- `/sales-featureos` — FeatureOS (formerly Hellonext) feedback boards + roadmap + changelog + knowledge base; REST API v3, OAuth apps, auto-disabling webhooks. Install: `npx skills add sales-skills/sales --skill sales-featureos -a claude-code`
- `/sales-feedbear` — Budget no-pull-API feedback board (webhooks/JWT SSO/Zapier only) — a useful contrast since both lean on no-code intake. Install: `npx skills add sales-skills/sales --skill sales-feedbear -a claude-code`
- `/sales-rapidr` — Polished Canny alternative with **no public API** (Zapier/SSO/native only) — the closest peer on the "no-code intake, no API" axis. Install: `npx skills add sales-skills/sales --skill sales-rapidr -a claude-code`
- `/sales-in-app-messaging` — In-app message / onboarding survey strategy across tools (Quickhunt ships in-app surveys/checklists/banners). Install: `npx skills add sales-skills/sales --skill sales-in-app-messaging -a claude-code`
- `/sales-noisely` — AI aggregation of **unsolicited** feedback across reviews/social/support (complement: Quickhunt = solicited boards, Noisely = unsolicited mining). Install: `npx skills add sales-skills/sales --skill sales-noisely -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "Quickhunt's API is locked to the top plan — how do I get new feedback into our own system?" (developer/automation)
**User says**: "Every new feature request in Quickhunt should land in our internal tool automatically, but the API is on the $99 plan and we're on Growth."
**Skill does**: Confirms the **REST API is Premium-only ($99/mo) and undocumented**, so on Growth you can't `GET` ideas. Lays out the substitutes available on **Growth ($49)**: a **Zapier** or **viaSocket** automation on a Quickhunt "new feedback" trigger → an action into your tool (confirm exact trigger names in the live editor), the native **GitHub/Jira/HubSpot/ClickUp** connectors if you live there, **Slack** notifications, or **webhooks** (capture a live payload to learn the shape). Flags that sync must be push-based, not a polled API read, and that Free/Starter have no integrations at all.
**Result**: A working push-based intake plan with the API/plan constraints made explicit.

### Example 2: "Turn Quickhunt feedback into GitHub issues automatically" (developer/automation)
**User says**: "When a feature request hits a certain status, I want a GitHub issue created for engineering."
**Skill does**: Confirms the **GitHub integration is native** (and requires **Growth $49+** — no integrations on Free/Starter). Walks the no-code path: connect GitHub in **Integrations**, map the Quickhunt board/status to a target repo, and have new/updated feedback create an actionable GitHub issue. Offers the **Zapier/viaSocket** alternative for more control (status-change trigger → "Create Issue" action with templated title/body), and notes that two-way status sync should be verified in-account since webhook payloads are unpublished.
**Result**: A feedback→GitHub pipeline grounded in the real plan gate and connector behavior.

### Example 3: Quickhunt vs Frill vs Canny — which board, and what do the plans cost?
**User says**: "Small SaaS picking a feedback + roadmap + changelog tool — Quickhunt, Frill, or Canny? And is there an API?"
**Skill does**: Frames the tradeoff — **Quickhunt** has a genuinely **free lifetime tier** and an affordable all-in-one bundle (boards + roadmap + changelog + in-app messages + docs + AI assistant + live chat), but its **API is Premium-only ($99/mo) and undocumented** and integrations need **Growth ($49)**; **Frill** (~$25) is cheaper for paid and ships a **documented REST API + signed webhooks**; **Canny** (~$400) is the pricier enterprise option. Recommends by whether **programmatic reads** matter (→ Frill/UserJot) vs a free start + no-code intake being enough (→ Quickhunt), and routes broader selection: "run: `/sales-customer-feedback choose a product-feedback board tool`".
**Result**: A price-, API-, and free-tier-grounded board-tool choice.

## Troubleshooting

### I can't find Quickhunt's API to pull our feedback
**Symptom**: You want to read ideas/votes programmatically but there's no API reference.
**Cause**: **API access is gated to the top Premium plan ($99/mo)** and no public API/developer docs exist (the `/docs` path 404s). Below Premium there is effectively no programmatic read path.
**Solution**: If you're below Premium, use **Zapier** or **viaSocket** triggers (new feedback/comment/vote → your app), the native **GitHub/Jira/HubSpot/ClickUp/Slack** connectors, or **webhooks** (capture a live payload). If a true documented API at a lower price is a hard requirement, evaluate `/sales-frill` or `/sales-userjot` instead. If you're on Premium, request the API docs from your dedicated account manager and confirm endpoints/auth in-account.

### My integration (Slack/GitHub/Zapier) isn't available
**Symptom**: There's no way to connect Quickhunt to your other tools.
**Cause**: **All integrations require Growth ($49/mo)** — Free and Starter have no integrations.
**Solution**: Upgrade to **Growth** (or higher) to unlock Slack/Zapier/ClickUp/GitHub/HubSpot/Jira/viaSocket. Note **Intercom** was "coming soon" at research time — verify before relying on it. On Growth, all listed integrations are included (unlike Canny's one-integration limit).

### Pricing or feature gates feel confusing
**Symptom**: "I'm on Starter but can't add an integration," or "custom domain isn't available."
**Cause**: Quickhunt gates features by tier — **custom domain / remove branding / scheduled changelog / analytics / conditional logic are Starter+**, **integrations are Growth+**, and **API + dedicated account manager are Premium**. Extra seats are **+$10/mo each**.
**Solution**: Match the needed feature to its tier: start **Free** to validate, move to **Starter ($29)** for custom domain + branding removal, **Growth ($49)** for integrations + more boards, and **Premium ($99)** only if you genuinely need the API. Budget +$10/mo per extra team member. Treat all pricing as best-effort and confirm in-account.
