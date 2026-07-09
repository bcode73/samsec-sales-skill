---
name: sales-rapidr
description: "Rapidr (rapidr.io) platform help — product-feedback & feature-request suite for SaaS: public/private feedback boards (voting, proxy voting, duplicate merging, segmentation), public roadmap, changelog/release notes, embeddable widget, and custom-domain portal — a modern Canny/Productboard/Frill alternative. Developer surface: NO public REST/pull API (you can't GET ideas or votes) — automation is JWT SSO (so votes aren't anonymous), Zapier (realtime triggers + create/update actions), and native Slack/Intercom/Jira/HubSpot. Use when wiring Rapidr feedback into Slack/Jira/HubSpot, setting up JWT SSO to identify users, exporting/syncing feedback when there's no API, embedding the widget or hosting the portal on a custom domain, mapping statuses to a roadmap and shipping a changelog, or choosing a plan (Startup vs Business vs Enterprise). Do NOT use for NPS/VoC survey program strategy across tools (use /sales-customer-feedback) or public review generation (use /sales-customer-reviews)."
argument-hint: "[describe what you need help with in Rapidr]"
license: MIT
version: 1.0.0
tags: [sales, customer-feedback, product, platform]
---

# Rapidr Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Get feedback **out** of Rapidr automatically — but there's **no pull/REST API** (you can't `GET` ideas/votes). Use Zapier realtime triggers, native integrations, or the voter CSV export instead.
   - B) Set up **JWT SSO** so board votes/posts attach to your real logged-in users (not anonymous)
   - C) Wire Rapidr into **Slack / Intercom / Jira / HubSpot / Zapier** (capture feedback, sync status, notify)
   - D) Embed the **feedback/changelog widget** or host the portal on a **custom domain**
   - E) Organize boards, custom statuses, the **public roadmap**, and ship a **changelog**
   - F) Decide Rapidr vs Canny/Frill/Productboard/Featurebase, or pick a plan (Startup / Business / Enterprise)

2. **Code or no-code?** Rapidr has no REST API, so "code" means JWT SSO (server-side token mint) + webhook receivers fed by Zapier; "no-code" means Zapier + native connectors.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Voice-of-customer / NPS/CSAT/CES survey **program** strategy across tools | `/sales-customer-feedback {question}` |
| Aggregating **unsolicited** feedback across reviews/social/support | `/sales-noisely {question}` |
| Public review **generation** strategy (Trustpilot/G2) | `/sales-customer-reviews {question}` |
| Connecting Rapidr to a CRM/PM tool generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-customer-feedback choose a product-feedback board tool`".

## Step 3 — Rapidr platform reference

**Read `references/platform-guide.md`** for the full reference — the Boards/Roadmap/Changelog/Widget module map (what's Zapier-automatable vs SSO vs UI-only), the integration surface (Slack `/rapidr`, Intercom, Jira, HubSpot, Zapier triggers/actions), pricing tiers + the SSO/segmentation plan gate, the data model, and quick-start recipes (push new ideas out via Zapier; identify a user with JWT SSO; embed the widget; export voters to CSV).

**Read `references/rapidr-api-reference.md`** for the integration surface — the **"no public REST/pull API"** reality and the four programmatic substitutes (**JWT SSO**, **Zapier**, **native connectors**, **embeddable widget**), the JWT SSO flow + a server-side token example, the Zapier trigger/action inventory, and a **Gaps** section noting which details (exact JWT claims, Zapier trigger names, webhook payloads) are JS-rendered and must be confirmed live/in-account.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **There is no REST API — design around it.** You cannot `GET` ideas, votes, or comments from Rapidr. To move feedback into your own system, use **Zapier realtime triggers** (new feedback/comment/vote → your app/CRM/Slack), the native **Jira/HubSpot/Intercom** syncs, or the manual **voter CSV export**. Don't promise an API pull — confirm any Zapier trigger names in the live Zap editor.
- **Identify users with JWT SSO or feedback stays anonymous.** Generate a Secret Key in **Company Settings → SSO**, mint a JWT server-side from the authenticated user, and redirect them to Rapidr's SSO endpoint with the token (a `redirect` query param returns them afterward). Use Rapidr's JWT debugger before going live. Keep the secret key server-side.
- **Mind the SSO/segmentation plan cliff.** SSO (SAML & JWT), user segmentation, and advanced integrations are **Business ($199/mo)** features — there's a steep jump from **Startup ($49/mo)**. If you only need boards + roadmap + changelog + Slack/Zapier, Startup is enough; you pay the cliff specifically for SSO + segmentation.
- **Slack is two-way.** The `/rapidr` slash command captures feedback from inside Slack, and Rapidr pushes new-feedback/comment/vote notifications to a channel (filterable by board and event type). It's the fastest no-code intake + alerting path.
- **Proxy voting beats lost feedback.** When customers report feedback over support/sales, log it and vote **on their behalf** so demand is captured against the right idea — then merge duplicates to keep the signal clean.
- **It's a feedback-board tool, not a VoC survey suite.** Rapidr collects *solicited* board feedback + roadmap + changelog. For survey *program* strategy use `/sales-customer-feedback`; for mining *unsolicited* feedback across reviews/social use `/sales-noisely`.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — modules/pricing captured from rapidr.io (homepage, /pricing, /features, /integrations) and third-party reviews on this date; the detailed SSO/JWT docs page is JS-rendered. Re-verify plan gates and SSO claim names in-account before relying on them.*

1. **No public REST/pull API.** A G2 reviewer states plainly that Rapidr doesn't offer an API, and the docs only cover SSO + native connectors + Zapier. You **cannot** `GET` ideas/votes/comments. Treat Zapier triggers + the CSV voter export as your only read paths.
2. **SSO is plan-gated to Business ($199/mo).** Both SAML and JWT SSO sit on Business+ — on Startup, board activity is anonymous unless users self-identify by email. Don't architect an SSO flow for a Startup-plan customer without flagging the upgrade.
3. **No free tier.** Only a 14-day trial (no card). Budget the $49 Startup minimum from day one — unlike Frill/Upvoty/UserJot which have free or sub-$25 entry.
4. **Several headline features are "Coming Soon."** MRR/priority filters, roadmap prioritization scoring, the embeddable roadmap widget, changelog reactions, and the email digest were marked Coming Soon at research time. Verify availability before promising them.
5. **Zapier trigger/action names are unconfirmed.** Rapidr advertises "realtime triggers" + create/update-record actions but doesn't publish the exact trigger names. Confirm them in the live Zap editor; don't hard-code a trigger that may not exist.
6. **JWT SSO claim names + algorithm are JS-rendered.** The `rapidr.io/docs/sso/` page didn't render server-side. The flow (secret key → mint JWT from name/email → redirect with token → debugger) is confirmed, but exact claim keys and the signing algorithm must be read from the in-account developer docs.

## Related skills

- `/sales-customer-feedback` — Voice-of-customer / survey program strategy across tools (Rapidr is one feedback-board option) — program design, metric choice, tool selection. Install: `npx skills add sales-skills/sales --skill sales-customer-feedback -a claude-code`
- `/sales-feedbear` — The closest like-for-like: a **no-pull-API** budget feedback board (webhooks/JWT SSO/Zapier only) — useful contrast since FeedBear has outbound webhooks where Rapidr leans on Zapier. Install: `npx skills add sales-skills/sales --skill sales-feedbear -a claude-code`
- `/sales-frill` — Affordable feedback-board competitor that **does** ship a REST API + HMAC-SHA256-signed webhooks — the pick when programmatic reads are the deciding factor. Install: `npx skills add sales-skills/sales --skill sales-frill -a claude-code`
- `/sales-userjot` — AI-first feedback board with a REST API + MCP server + no-per-seat pricing and a free tier — contrast on price and API access. Install: `npx skills add sales-skills/sales --skill sales-userjot -a claude-code`
- `/sales-sleekplan` — AI feedback suite (auto-categorization + MCP server) with a REST API + JWT SSO — contrast when you want AI triage plus an API. Install: `npx skills add sales-skills/sales --skill sales-sleekplan -a claude-code`
- `/sales-featureos` — FeatureOS (formerly Hellonext) feedback boards + roadmap + changelog + knowledge base; REST API v3, OAuth apps, auto-disabling webhooks. Install: `npx skills add sales-skills/sales --skill sales-featureos -a claude-code`
- `/sales-noisely` — AI aggregation of **unsolicited** feedback across reviews/social/support (complement: Rapidr = solicited boards, Noisely = unsolicited mining). Install: `npx skills add sales-skills/sales --skill sales-noisely -a claude-code`
- `/sales-integration` — Connecting Rapidr to a CRM/PM tool via Zapier/native connectors. Install: `npx skills add sales-skills/sales --skill sales-integration -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "Rapidr has no API — how do I get new feedback into our own system?" (developer/automation)
**User says**: "I want every new feature request in Rapidr to land in our internal tool automatically, but I can't find an API."
**Skill does**: Confirms **Rapidr has no public REST/pull API** — you cannot `GET` ideas/votes. Lays out the substitutes: a **Zapier** Zap on Rapidr's realtime "new feedback" trigger → an action into your tool (confirm the exact trigger name in the live Zap editor), the native **Jira/HubSpot** syncs if you live there, **Slack** notifications via the `/rapidr` integration, or the manual **voter CSV export** for a one-off pull. Flags that ongoing sync must be push-based (Zapier), not a polled API read.
**Result**: A working push-based intake plan with the no-API constraint made explicit.

### Example 2: "Votes on our board are all anonymous — tie them to real users" (developer/automation)
**User says**: "Feedback on our Rapidr portal shows up without names. How do I attach it to our logged-in accounts?"
**Skill does**: Walks the **JWT SSO** flow — generate a **Secret Key** in **Company Settings → SSO**, mint a JWT **server-side** from the authenticated user (name + email) on a login redirect page, redirect the user to Rapidr's **SSO endpoint** with the token (honoring the `redirect` query param), and validate with Rapidr's **JWT debugger** before enabling. Notes the secret stays server-side, that enabling SSO disables other login methods, and that **SSO is a Business-plan ($199/mo) feature** — on Startup, identification is email-only.
**Result**: A correct SSO setup with the plan-gate caveat surfaced.

### Example 3: Rapidr vs Frill vs Canny — which board, and what do the plans cost?
**User says**: "Small SaaS picking a feedback + roadmap + changelog tool — Rapidr, Frill, or Canny? And is there an API?"
**Skill does**: Frames the tradeoff — **Rapidr** ($49 Startup / $199 Business, no free tier) is a polished Canny alternative with boards + roadmap + changelog + segmentation but **no REST API** (Zapier/SSO/native only); **Frill** (~$25) is cheaper and ships a **REST API + signed webhooks**; **Canny** (~$400) is the pricier enterprise option. Recommends by whether **programmatic reads** matter (→ Frill/UserJot) vs no-code intake being enough (→ Rapidr), flags Rapidr's **SSO/segmentation cliff at $199**, and routes broader selection: "run: `/sales-customer-feedback choose a product-feedback board tool`".
**Result**: A price-, API-, and plan-gate-grounded board-tool choice.

## Troubleshooting

### I can't find Rapidr's API to pull our feedback
**Symptom**: You want to read ideas/votes programmatically but there's no API reference.
**Cause**: **Rapidr does not publish a public REST/pull API** — third-party reviews confirm "no API." The programmatic surface is push/identify only.
**Solution**: Use **Zapier** realtime triggers (new feedback/comment/vote → your app — confirm trigger names live), the native **Jira/HubSpot/Intercom** syncs, **Slack** notifications, or the **voter CSV export** for one-off pulls. If a true API is a hard requirement, evaluate `/sales-frill` or `/sales-userjot` instead.

### My SSO/JWT login isn't available or board activity is still anonymous
**Symptom**: You can't set up SSO, or votes/posts stay anonymous after building a JWT flow.
**Cause**: **SSO (SAML & JWT) is gated to the Business plan ($199/mo)** — it isn't available on Startup. Or the JWT redirect/secret key isn't configured correctly.
**Solution**: Confirm the account is on **Business+**, generate the **Secret Key** in **Company Settings → SSO**, mint the JWT server-side, and redirect to the SSO endpoint with the token; validate with the **JWT debugger** first. Note enabling SSO disables other auth methods. Confirm exact claim names/algorithm in the in-account developer docs (the public docs page is JS-rendered).

### Pricing feels steep for what we get
**Symptom**: "$49 is fine but jumping to $199 just for SSO/segmentation hurts," or "pricey for a non-multi-tenant product" (a real G2 complaint).
**Cause**: Rapidr's value-unlocking features (SSO, user segmentation, advanced integrations, remove branding) all live on **Business ($199/mo)** with no middle tier, and there's **no free plan**.
**Solution**: Stay on **Startup ($49/mo)** if you only need boards + roadmap + changelog + Slack/Zapier; only move to Business when you genuinely need SSO or segmentation. If budget is the deciding factor, compare cheaper boards (`/sales-frill` ~$25, `/sales-userjot` free tier) via `/sales-customer-feedback`.
