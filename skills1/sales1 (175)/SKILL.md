---
name: sales-featureos
description: "FeatureOS (formerly Hellonext) platform help — customer-feedback suite for product teams: feedback boards (posts/feature requests with voting + comments), public roadmaps, branded changelogs, knowledge base, surveys, widget. Developer surface: REST API v3 (base api.featureos.app/api/v3, API-KEY header, keys prefixed hn_, page/per_page pagination, 100 req/min), OAuth 2.0 apps (foapp_/foot_ tokens, scopes, app/self actor modes), webhooks (post_created/post_completed/changelog_published, 3x retry then auto-disable), and the HellonextWidget embed with SSO. Use when reading or syncing feedback posts/votes via the API, building an OAuth app other workspaces install, verifying or debugging webhooks, embedding the widget or identifying users with SSO, mapping post statuses to a roadmap, or choosing FeatureOS vs Canny/Frill/Featurebase on price. Do NOT use for voice-of-customer / NPS survey program strategy across tools (use /sales-customer-feedback) or public review generation (use /sales-customer-reviews)."
argument-hint: "[describe what you need help with in FeatureOS]"
license: MIT
version: 1.0.0
tags: [sales, customer-feedback, product, platform]
github: "https://github.com/skcript"
---

# FeatureOS Platform Help

FeatureOS (formerly **Hellonext**) — feedback boards + roadmap + changelog + knowledge base. Note the rebrand left legacy names in place: API keys are prefixed `hn_`, the embed class is `HellonextWidget`, and posts are the `feature_requests` resource.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Read/sync feedback posts, votes, comments via the REST API v3 (`API-KEY` header)
   - B) Build an OAuth app that **other workspaces install** (scopes, actor modes, token refresh)
   - C) Receive/verify webhooks (post + changelog events) and react to them
   - D) Embed the widget / identify logged-in users with SSO (`ssoToken`)
   - E) Map post **statuses** to a roadmap, or wire a changelog
   - F) Pick a plan, or decide FeatureOS vs Canny/Frill/Featurebase

2. **API key or OAuth?** Scripting your own org → plain `API-KEY` (`hn_…`). An integration other orgs connect → OAuth 2.0 app (`foapp_`/`foot_`). Front-end embed → `HellonextWidget`.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Voice-of-customer / survey **program** strategy (NPS/CSAT/CES) across tools | `/sales-customer-feedback {question}` |
| Aggregating **unsolicited** feedback across reviews/social/support sources | `/sales-noisely {question}` |
| Public review **generation** strategy | `/sales-customer-reviews {question}` |
| Connecting FeatureOS to a CRM/PM tool generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-customer-feedback build a closed-loop feedback program`".

## Step 3 — FeatureOS platform reference

**Read `references/platform-guide.md`** for the full reference — the boards/roadmap/changelog/KB module map (API vs widget vs UI), pricing tiers + the API plan-gate, the post/customer data model, and quick-start recipes (export posts, handle a webhook, embed + SSO).

**Read `references/featureos-api-reference.md`** for the integration surface — base `https://api.featureos.app/api/v3`, **`API-KEY: hn_…`** auth (+ per-user `Authorization: Bearer <sso_jwt>`), **`page`/`per_page`** pagination (default 30, max 100), **100 req/min** rate limit, the full **errors** table + `ERROR_CODE_*` codes, **OAuth 2.0 apps** (token formats, `/oauth/apps` → `/oauth/authorize` → `/oauth/authorize/consent` → `/oauth/token`, scopes, actor modes, role-capping), **webhooks** (events, `postCompleted` payload, retry policy), and the **`HellonextWidget`** options.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Auth + pagination.** `API-KEY: hn_<key>` against `api.featureos.app/api/v3`; page with `?page=N&per_page=100` (default 30, max 100). Keep the key server-side; full API access is plan-gated (≈Growth tier and up — verify in-account).
- **Posts are `feature_requests`; `status.value` is the roadmap column.** Read/sync `feature_requests` (and `buckets` = boards, `votes`, `comments`); map `status.value` (`planned`/`in_progress`/`completed`) to your roadmap.
- **Webhooks: 200 or they retry then disable.** Subscribe to post/changelog events; respond **200** fast — failures retry at 5m/30m/2h then the webhook is **auto-disabled** (email sent). Dashboard webhooks aren't HMAC-signed; keep the URL secret. Dedupe on `data.id` + timestamp (unix seconds).
- **OAuth for multi-tenant apps.** Register `POST /oauth/apps`, request **minimum scopes**, pick actor mode (`app` bot vs `self` user, which is role-capped). Access tokens expire in **24h** — refresh (rotation: store the newest `foot_`/`foor_` pair).
- **Identify widget users with `ssoToken`** or board activity is anonymous. The class is `HellonextWidget` (legacy), not FeatureOSWidget.
- **It's a feedback-board tool, not VoC surveys or aggregation.** For NPS/CSAT *programs* use `/sales-customer-feedback`; for mining *unsolicited* reviews/social use `/sales-noisely`.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — API verbatim from developers.featureos.app; pricing from the live site. Confirm in-account.*

1. **Rebrand leftovers.** Hellonext → FeatureOS, but API keys are still prefixed **`hn_`**, the embed class is still **`window.HellonextWidget`**, and feedback posts are the **`feature_requests`** resource. Don't expect "featureos"-named identifiers.
2. **Pagination is `page`/`per_page`, not cursors.** Default 30, max 100. Loop `page` until a short/empty page.
3. **Webhooks auto-disable after 3 failures** (retries at 5m/30m/2h) and aren't replayable — always return **200**, and reconcile by polling `feature_requests`. Dashboard webhooks have **no HMAC signature** (unlike Frill); secure by URL secrecy / IP allowlist.
4. **API access is plan-gated** and the docs disagree on the tier (live pricing: "complete API access" from ~Growth $120/mo; Help Center: top "Fly High" plan). Treat full API as a higher-paid feature; verify before building.
5. **OAuth access tokens expire in 24h.** Refresh is a rotation — the old access **and** refresh token stop working; persist the newest pair or you'll lock yourself out.
6. **`self`-actor OAuth tokens are role-capped per request.** If the authorizing user is downgraded/removed, `:write`/`:manage` scopes silently drop to read — don't assume a token's permissions are static.
7. **No SSO `ssoToken` → anonymous feedback.** Pass a JWT signed with your org SSO key so votes/posts attach to real accounts.
8. **Rate limit 100 req/min/key** → `429`/`ERROR_CODE_RATE_LIMITED`. Batch with `per_page=100` and back off.

## Related skills

- `/sales-customer-feedback` — Voice-of-customer / survey program strategy across tools (FeatureOS is a feedback-board option) — program design, tool selection
- `/sales-frill` — Frill platform help (the closest like-for-like feedback-board competitor: boards + roadmap + changelog; cursor pagination + HMAC-signed webhooks)
- `/sales-noisely` — AI feedback aggregation across reviews/social/support (complement: FeatureOS = solicited boards, Noisely = unsolicited mining)
- `/sales-customer-reviews` — Public review generation strategy
- `/sales-integration` — Connecting FeatureOS to a CRM/PM tool via API/webhooks/Zapier
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Export all feedback posts and their vote counts via the API (developer/automation)
**User says**: "How do I pull every feature request and its upvotes out of FeatureOS?"
**Skill does**: Shows `GET https://api.featureos.app/api/v3/feature_requests` with **`API-KEY: hn_<key>`**, paging via **`?page=N&per_page=100`** (default 30, max 100) until a short page, reading each post's `status.value`, `upvotes_count`, `bucket`, and `submitter`. Notes the **100 req/min** limit (back off on `429`), keeping the key server-side, and that **webhooks** (`post_created`/`post_updated`) beat polling for ongoing sync.
**Result**: A complete, paginated export of posts + engagement.

### Example 2: Build a webhook that won't get disabled
**User says**: "FeatureOS keeps disabling my webhook — how do I receive post events reliably?"
**Skill does**: Explains the endpoint must use HTTPS, be public, and **return 200**; on non-200 it retries at **5m/30m/2h** then **auto-disables** (email sent). Recommends responding 200 immediately and processing async, deduping on `data.id` + `created`/`updated_at` (unix seconds), reading `type`/`event` (dashboard `postCompleted` vs OAuth-app `post_completed`), and reconciling missed events by polling `feature_requests`. Flags that dashboard webhooks aren't HMAC-signed.
**Result**: A durable webhook intake that stays enabled.

### Example 3: FeatureOS vs Frill vs Canny — which feedback board?
**User says**: "Small SaaS — should I use FeatureOS, Frill, or Canny for a public feedback board + roadmap?"
**Skill does**: Frames the tradeoff — **FeatureOS** bundles boards + roadmap + changelog + **knowledge base** + AI copilot (~$60 Starter / ~$120 Growth, API gated to Growth+), **Frill** is the cheapest (~$25/mo) with cursor pagination + HMAC-signed webhooks, **Canny** is pricier (~$400/mo) with deeper enterprise features. Recommends by budget/feature-need and routes broader selection: "run: `/sales-customer-feedback choose a product-feedback board tool`."
**Result**: A price- and feature-grounded board choice.

## Troubleshooting

### My API key returns 401 / "API key is invalid"
**Symptom**: Every request fails with `401`.
**Cause**: Wrong header, a key without the `hn_` prefix, or a plan without API access.
**Solution**: Send the key in the **`API-KEY`** header (not `Authorization`) — `-H 'API-KEY: hn_…'`; regenerate from **Dashboard → Organization Settings → Advanced**. Full API access is **plan-gated** (≈Growth and up) — confirm your tier includes it. Use HTTPS only.

### My webhook stopped firing
**Symptom**: Events arrived, then silence.
**Cause**: Your endpoint returned non-200; after 3 retries (5m/30m/2h) FeatureOS **disabled** the webhook.
**Solution**: Check your inbox for the disable notice, fix the endpoint to always return **200** quickly, then re-enable under **Organization Settings → Webhooks**. Backfill the gap by polling `feature_requests`. Inspect per-delivery logs in the webhook's view.

### Widget feedback is all anonymous
**Symptom**: Board votes/posts aren't tied to your real users.
**Cause**: The `HellonextWidget` isn't passing an `ssoToken`.
**Solution**: Generate a JWT from `{ "email": "...", "name": "..." }` signed with your org **SSO key** and pass it as **`ssoToken`** (the old `jwtToken` is deprecated). For VoC program strategy beyond boards, use `/sales-customer-feedback`.
