---
name: sales-feedbear
description: "FeedBear (feedbear.com) platform help — budget customer-feedback suite (Canny/Nolt/Frill alternative): feedback boards (upvoting, comments, duplicate-merge), public roadmap, changelog, AI-generated replies, embeddable widget. Notable: NO public pull/REST API — automation is outbound webhooks (new idea / upvote / comment events, JSON POST, no documented HMAC), JWT SSO (private key + /sso/auth?payload= redirect), Zapier, and native Intercom/Slack/Trello/Jira. Use when wiring FeedBear webhooks into your app or Slack/Trello, setting up JWT SSO so board votes attach to real users, exporting or syncing feedback with no REST API, embedding the widget, or choosing FeedBear vs Canny/Frill on price (paid-only, no free tier). Do NOT use for NPS/CSAT survey-program strategy across tools (use /sales-customer-feedback), aggregating unsolicited feedback across reviews/social (use /sales-noisely), or public review generation (use /sales-customer-reviews)."
argument-hint: "[describe what you need help with in FeedBear]"
license: MIT
version: 1.0.1
tags: [sales, customer-feedback, product, platform]
---

# FeedBear Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) React to feedback in your own app via **outbound webhooks** (new idea / upvote / comment)
   - B) Set up **JWT SSO** so board votes/ideas attach to your real logged-in users
   - C) **Export or sync** feedback out of FeedBear when there's no pull/REST API
   - D) Wire FeedBear to other tools via **Zapier** or native **Intercom/Slack/Trello/Jira**
   - E) Embed the **website widget** / customize branding (CSS/HTML/JS)
   - F) Map idea **statuses → roadmap** and ship a **changelog**
   - G) Decide **FeedBear vs Canny/Frill/Nolt** (price) or pick a plan

2. **Code or no-code?** Code → outbound webhooks + JWT SSO (server-side). No endpoint → Zapier / native integrations. There is **no REST pull API** — plan accordingly.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Voice-of-customer / survey **program** strategy (NPS/CSAT/CES) across tools | `/sales-customer-feedback {question}` |
| Aggregating feedback across **reviews/social/support** sources | `/sales-noisely {question}` |
| Public review **generation** strategy | `/sales-customer-reviews {question}` |
| Connecting FeedBear to a CRM/PM tool generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-customer-feedback choose a product-feedback board tool`".

## Step 3 — FeedBear platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (boards / roadmap / changelog / widget, each tagged API-accessible / webhook-accessible / UI-only), plan tiers and what gates where, the data model (Project → Boards → Ideas → Votes/Comments), and quick-start recipes (catch a new-idea webhook; generate a JWT SSO token; mirror feedback into a sheet via Zapier).

**Read `references/feedbear-api-reference.md`** for the integration surface — the **no-REST-API** reality, the **outbound webhook** setup (events, JSON-over-HTTPS POST, unsigned → verify by URL secrecy/IP allowlist + a representative payload to capture live), the **JWT SSO** flow (`{BOARD}/sso/auth?payload={JWT}`, private key from Project Settings → SSO), and the **Zapier** triggers + native integrations.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **There is no pull API — design around webhooks.** FeedBear pushes events out; it does not let you `GET` your ideas. For ongoing sync, catch the **webhook** (new idea / upvote / comment) and persist locally; for one-off export, use **Zapier** or the in-app export. Don't architect a poller against a REST endpoint that doesn't exist.
- **Webhooks aren't documented as signed — secure them another way.** No published HMAC. Use a **secret, hard-to-guess webhook URL** (and/or IP allowlist), validate the payload shape, and dedupe on the idea id. Capture one live delivery to lock down the exact field names before coding.
- **JWT SSO ties board activity to real users.** Generate a JWT from the user's name + email with the **private key** (Project Settings → SSO), then redirect to `{{BOARD_URL}}/sso/auth?payload={{JWT}}`. Without it, widget votes/ideas are anonymous. SSO is **Business-tier** ($99).
- **Mind the plan gates.** Integrations + webhooks unlock at **Startup ($49)**; **SSO, private projects, and remove-branding** unlock at **Business ($99)**. Lite ($19) is boards + roadmap + changelog + widget + AI replies only.
- **It's boards, not surveys.** FeedBear collects *solicited* board feedback + roadmap + changelog — no NPS/CSAT surveys (unlike Frill/Sleekplan). For survey *programs* use `/sales-customer-feedback`; for mining *unsolicited* feedback use `/sales-noisely`.
- **Price is the pitch.** Cheapest entry in the category ($19/mo) but **no free tier** (14-day trial, no card) — vs Sleekplan's free Indie tier and Frill's ~$25.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — webhook/SSO behavior and pricing from FeedBear's site + help center and third-party reviews. The exact webhook payload schema is JS-rendered and was not fetchable; capture a live delivery and confirm in-account.*

1. **No public REST/pull API.** You cannot `GET` ideas/votes — the only programmatic surface is outbound webhooks + JWT SSO + Zapier + native integrations. Reviewers explicitly flag the missing API; plan integrations around push, not pull.
2. **Webhooks are not documented as HMAC-signed.** Unlike Frill (HMAC-SHA256), FeedBear publishes no signature scheme. Protect the endpoint with a secret URL / IP allowlist and validate payloads yourself.
3. **Exact webhook payload schema is undocumented online.** The help article references payloads "at the bottom of the page" but they're JS-rendered. Capture a real delivery to confirm field names before relying on them.
4. **Integrations + webhooks gate at Startup ($49); SSO at Business ($99).** On the $19 Lite plan you get boards/roadmap/changelog/widget/AI replies but **no integrations, no webhooks, no SSO, no custom domain**. Size the plan to your integration needs.
5. **No free tier.** 14-day trial (no card), then paid. Sleekplan has a free Indie tier and Frill a free trial too — factor this into a budget comparison.
6. **Boards only — no surveys/NPS.** It doesn't run NPS/CSAT programs (→ `/sales-customer-feedback`) and doesn't mine reviews/social (→ `/sales-noisely`).
7. **Limited design customization.** Effective branding is accent color + logo (plus CSS/HTML/JS on paid tiers); reviewers note dark-theme/embedding blends are hard. English-only UI (multi-language is on their roadmap).

## Related skills

- `/sales-customer-feedback` — Voice-of-customer / survey program strategy across tools (FeedBear is one feedback-board option) — program design, tool selection. Install: `npx skills add sales-skills/sales --skill sales-customer-feedback -a claude-code`
- `/sales-frill` — Frill platform help — the closest like-for-like budget competitor that *does* ship a REST API (`api.frill.co/v1`, Bearer + cursor) and **HMAC-signed** webhooks + surveys; the right pick when you need to pull data. Install: `npx skills add sales-skills/sales --skill sales-frill -a claude-code`
- `/sales-sleekplan` — Sleekplan platform help — AI feedback suite with a REST API, MCP server, and a **free** tier; compare when you want AI auto-categorization or programmatic reads. Install: `npx skills add sales-skills/sales --skill sales-sleekplan -a claude-code`
- `/sales-featureos` — FeatureOS (formerly Hellonext) — feedback boards + roadmap + changelog + knowledge base with REST API v3 + OAuth apps. Install: `npx skills add sales-skills/sales --skill sales-featureos -a claude-code`
- `/sales-noisely` — AI feedback aggregation across reviews/social/support (complement: FeedBear = solicited boards, Noisely = unsolicited mining). Install: `npx skills add sales-skills/sales --skill sales-noisely -a claude-code`
- `/sales-customer-reviews` — Public review generation strategy. Install: `npx skills add sales-skills/sales --skill sales-customer-reviews -a claude-code`
- `/sales-integration` — Connecting FeedBear to a CRM/PM tool via webhooks/Zapier. Install: `npx skills add sales-skills/sales --skill sales-integration -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Catch a new-idea event in my app when there's no REST API (developer/automation)
**User says**: "FeedBear doesn't have a pull API — how do I get new feedback ideas into my system automatically?"
**Skill does**: Explains FeedBear has **no REST/pull API**, so you wire an **outbound webhook**: in **Project Settings → Webhooks** set a **secret HTTPS URL**, enable events, and process the JSON POST for **new idea / upvote / comment**. Since there's no documented HMAC, secure with a hard-to-guess URL + payload validation and **dedupe on the idea id**; advises capturing one live delivery to confirm field names, and notes webhooks require the **Startup ($49)** plan.
**Result**: A push-based intake that survives the missing pull API.

### Example 2: Make board votes attach to my logged-in users (JWT SSO)
**User says**: "Everyone's feedback shows up anonymous — how do I tie it to our real accounts?"
**Skill does**: Walks the **JWT SSO** flow — grab the **private key** (Project Settings → SSO), generate a JWT from the user's **name + email** after they authenticate on your site, then redirect to **`{{BOARD_URL}}/sso/auth?payload={{JWT}}`**. Notes SSO is **Business-tier ($99)** and that without it widget activity stays anonymous.
**Result**: Authenticated, attributed board activity.

### Example 3: FeedBear vs Frill vs Canny — which feedback tool?
**User says**: "We're a small SaaS — FeedBear, Frill, or Canny for a feedback board + roadmap?"
**Skill does**: Frames the tradeoff — **FeedBear** is the cheapest entry (**$19/mo**, boards + roadmap + changelog + AI replies) but has **no pull API**, no surveys, and no free tier; **Frill** (~$25) adds a **REST API + signed webhooks + surveys**; **Canny** (~$400) is the pricier enterprise option. Recommends FeedBear for cost-sensitive teams that only need push/Zapier, Frill when you must read data programmatically, and routes broader selection: "run: `/sales-customer-feedback choose a product-feedback board tool`."
**Result**: A price- and API-grounded board-tool choice.

## Troubleshooting

### I can't find FeedBear's API to pull my ideas
**Symptom**: You're looking for a `GET /ideas` endpoint and there isn't one.
**Cause**: FeedBear publishes **no public REST/pull API** — only outbound webhooks, JWT SSO, Zapier, and native integrations.
**Solution**: For ongoing sync, register an **outbound webhook** (Project Settings → Webhooks) and persist events as they arrive. For a one-time pull, use **Zapier** (triggers for ideas/feedback/comments) or the in-app export. If a true pull API is a hard requirement, consider `/sales-frill` (REST API) or `/sales-featureos` instead.

### My webhook endpoint receives events but I can't verify they're really from FeedBear
**Symptom**: No signature header to validate against.
**Cause**: FeedBear's webhooks are **not documented as HMAC-signed** (unlike Frill's HMAC-SHA256).
**Solution**: Use a **secret, unguessable webhook URL** (and/or restrict by source IP), validate the JSON shape and required fields, and dedupe on the idea id. Capture a live delivery first to confirm the exact payload field names since the schema isn't published.

### Board votes and ideas are all anonymous
**Symptom**: Feedback isn't attributed to your actual users.
**Cause**: No SSO configured, so the widget can't identify logged-in users.
**Solution**: Set up **JWT SSO** — generate a JWT from name + email with the **private key** (Project Settings → SSO) and redirect to **`{{BOARD_URL}}/sso/auth?payload={{JWT}}`**. Note SSO requires the **Business** plan. For VoC program strategy beyond boards, use `/sales-customer-feedback`.
