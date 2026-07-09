---
name: sales-sweepwidget
description: "SweepWidget (sweepwidget.com) platform help — giveaway, contest, and sweepstakes builder with 100+ entry methods across 30+ social platforms, viral refer-a-friend, leaderboards, instant rewards/coupons, and list capture. Developer surface: a read+write REST API (base sweepwidgetapi.com/sw_api/, Bearer or api_key auth, 50 rows/page via page_start) for users/entries/winners/giveaways plus create-giveaway and entry-method endpoints, and HMAC-SHA256 signed webhooks (X-SweepWidget-Signature; entry_submitted/task_completed/all_entries_completed) — both Enterprise-plan-gated. Use when pulling entries or winners into a CRM or warehouse via the API, verifying the signed webhook, syncing entrants to an ESP or Zapier, an entry is flagged by anti-spam, honor-system entries cannot be verified, the free plan hides entrant data past 10 users, or choosing a plan. Do NOT use for giveaway/audience-growth strategy across tools (use /sales-audience-growth) or deliverability of the collected list (use /sales-deliverability)."
argument-hint: "[describe what you need help with in SweepWidget]"
license: MIT
version: 1.0.0
tags: [sales, email-marketing, giveaway, platform]
github: "https://github.com/SweepWidget"
---

# SweepWidget Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Read entries / winners / users via the REST API (paging with `page_start`)
   - B) Receive entries in real time via the signed webhook (and verify `X-SweepWidget-Signature`)
   - C) Create or update a giveaway / entry method programmatically
   - D) Sync entrants to an ESP/CRM (Mailchimp etc.) or Zapier
   - E) An entry got flagged by the anti-spam system, or honor-system entries can't be verified
   - F) Decide a plan (Free vs Pro vs Business vs Premium vs Enterprise), or export entrant data

2. **Which plan are you on?** The API and server-side webhooks are **Enterprise-only** — if you're below Enterprise, code integration isn't available; use native ESP connectors, Zapier, or the client-side JavaScript callbacks instead.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Giveaway / audience-growth **strategy** across tools (which tool, viral mechanics) | `/sales-audience-growth {question}` |
| Connecting SweepWidget to a CRM/ESP generically (iPaaS) | `/sales-integration {question}` |
| Email sequences for the list you collect | `/sales-email-marketing {question}` |
| Deliverability / list quality of giveaway emails | `/sales-deliverability {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-audience-growth maximize entries on a refer-a-friend contest`".

## Step 3 — SweepWidget platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's API vs webhook vs UI-only), plan gates, the entry/giveaway data model (JSON shapes), and quick-start recipes (pull entries via the API; verify the signed webhook; sync to an ESP).

**Read `references/sweepwidget-api-reference.md`** for the integration surface — base URL `https://sweepwidgetapi.com/sw_api/`, `Authorization: Bearer` (or `api_key` param) auth, read endpoints (`/users`, `/entries`, `/winners`, `/giveaways`, `/user-entries`), write endpoints (`/new-entry`, `/create-giveaway`, `/add-manual-entries`, `/create-entry-method`), `page_start` pagination at **50 rows/page**, and the HMAC-SHA256 signed webhook (`X-SweepWidget-Signature`).

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Confirm the plan gate first.** The REST API and server-side webhooks are **Enterprise-plan-only**. If the user is on Free/Pro/Business/Premium, tell them code integration isn't available on their tier — point them to native ESP connectors, Zapier, or **client-side JavaScript callbacks** (`window.addEventListener('sweepwidget.entry_submitted', …)`) as the no-Enterprise path.
- **Authenticate correctly.** Base URL is `https://sweepwidgetapi.com/sw_api/`. Pass `Authorization: Bearer YOUR_API_KEY`, or `api_key` as a query param (GET) / form field (POST). Key comes from Integrations → API Access.
- **Page with `page_start`.** List endpoints return **50 rows per page**; increment `page_start` until a page returns fewer than 50. Always pass `competition_id` to scope reads to one giveaway.
- **Verify the webhook signature.** The `X-SweepWidget-Signature` header is `sha256=` + an **HMAC-SHA256 of the raw request body** using your signing secret. Recompute over the raw bytes and **constant-time compare**; reject on mismatch. Then **dedupe on user email + `competition_id`** because events (`entry_submitted`, `task_completed`, `all_entries_completed`) can repeat.
- **Explain anti-spam flags without over-promising.** SweepWidget uses device fingerprinting (300+ data points) and can false-positive; the fix is to contact support (they typically clear legitimate flags quickly) — you cannot self-unflag via API.
- **Set verification expectations honestly.** Some entry methods (e.g. YouTube likes/comments) are **honor-system** — SweepWidget can't verify them via those platforms' APIs, so those entries aren't "verified" even on paid plans. Verified entries themselves require Pro+.
- **Flag the free-plan data cap.** On Free, entrant personal info (name/email/location) is **truncated past 10 users** and there are no verified entries — you must upgrade to Pro+ to view/export the full entrant list.
- **Present pricing as best-effort** and confirm in-account; note the API/webhooks are Enterprise-gated when recommending an integration path.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-07) — review these, especially plan-gated API/webhook access and integration details that may be outdated.*

1. **API + server-side webhooks are Enterprise-only.** Below Enterprise there is no REST API and no server-side webhook — plan around native ESP connectors, Zapier, or client-side JavaScript callbacks.
2. **The API base host is a separate domain.** It's `https://sweepwidgetapi.com/sw_api/`, NOT `sweepwidget.com`. Hitting the marketing domain won't work.
3. **Pagination is fixed at 50 rows/page via `page_start`.** There's no adjustable page size; loop `page_start` until a short page.
4. **Webhooks ARE signed — verify them.** `X-SweepWidget-Signature` = `sha256=` HMAC-SHA256(raw body, secret). Don't skip verification, and dedupe on email + `competition_id` (events repeat across the three event types).
5. **Anti-spam false positives happen.** Device-fingerprint flags occasionally block legitimate entrants ("flagged by our anti-spam system"); resolution is via support, not an API call.
6. **Honor-system entries can't be verified.** YouTube like/comment and similar actions rely on the entrant's claim; there's no API to confirm them — don't treat them as verified.
7. **Free plan truncates entrant data past 10 users** and disables verified entries — upgrade to Pro+ to see/export the full list.
8. **Giveaways attract fraud.** Disposable emails, duplicate/self-referrals — validate before rewarding, and use SweepWidget's built-in fingerprinting plus login-required entry methods.

## Related skills

- `/sales-audience-growth` — Giveaway / contest / audience-growth strategy across tools (SweepWidget is one of the contest platforms covered) — viral mechanics, tool selection
- `/sales-email-marketing` — Email sequences for the list you grow with a giveaway
- `/sales-integration` — Connecting SweepWidget to a CRM/ESP via the API / webhooks / Zapier
- `/sales-deliverability` — Inbox placement and list quality for the emails you collect
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Pull entrants into my CRM via the API (developer/automation)
**User says**: "How do I fetch all entries from my SweepWidget giveaway programmatically and load them into my warehouse?"
**Skill does**: Confirms the REST API is **Enterprise-only**, then shows `GET https://sweepwidgetapi.com/sw_api/entries?competition_id=123&page_start=1` with `Authorization: Bearer YOUR_API_KEY`, looping `page_start` while a page returns 50 rows, and parsing the `{ "data": [ … ] }` response. Recommends the signed webhook for real-time instead of repeated polling, and deduping on email + `competition_id`.
**Result**: A working, paged pull of the giveaway's entrants ready to upsert.

### Example 2: Verify the entry webhook so I can trust it
**User says**: "SweepWidget is POSTing entries to my endpoint — how do I make sure they're really from SweepWidget?"
**Skill does**: Explains `X-SweepWidget-Signature` is `sha256=` + an **HMAC-SHA256 of the raw request body** with the signing secret; the handler recomputes the HMAC over the raw bytes and **constant-time compares**, rejecting on mismatch. Adds dedupe on user email + `competition_id` (events repeat) and notes it's Enterprise-gated, with the JavaScript callback as a client-side alternative.
**Result**: Authenticated, tamper-evident webhook intake.

### Example 3: My entry was flagged for spam
**User says**: "Contestants say their SweepWidget entry was flagged by the anti-spam system — how do I fix it?"
**Skill does**: Explains SweepWidget's device-fingerprinting (300+ data points, occasional false positives) blocks suspected bots/duplicates; there's **no API to self-unflag**, so the path is contacting support (usually resolved quickly). Suggests reducing false positives with login-required entry methods and warns that some entry types are honor-system and simply can't be verified.
**Result**: A clear explanation and the correct resolution path for flagged entrants.

## Troubleshooting

### My API calls return 401 / don't work
**Symptom**: Requests to the API are rejected, or you can't find the endpoint.
**Cause**: Wrong host, missing/misplaced key, or you're below the Enterprise plan (no API access).
**Solution**: Use the base host `https://sweepwidgetapi.com/sw_api/` (not `sweepwidget.com`), send `Authorization: Bearer YOUR_API_KEY` (or `api_key` param/form field) from Integrations → API Access, and confirm the account is on **Enterprise** — the API is gated to it. Test: `curl -i -H "Authorization: Bearer $KEY" "https://sweepwidgetapi.com/sw_api/giveaways?type=live&page_start=1"`.

### My webhook signature check keeps failing
**Symptom**: The HMAC you compute doesn't match `X-SweepWidget-Signature`.
**Cause**: Signing a re-serialized/parsed body instead of the **raw** bytes, forgetting the `sha256=` prefix handling, a wrong secret, or not being on Enterprise.
**Solution**: Compute HMAC-SHA256 over the **raw request body** with your signing secret, compare against the hex after the `sha256=` prefix, and constant-time compare. Confirm server-side webhooks are enabled (Enterprise). Once verified, dedupe on email + `competition_id` since events repeat.

### Contestants' entries are flagged for spam
**Symptom**: Legitimate entrants see "This entry has been flagged by our anti-spam system."
**Cause**: SweepWidget's device fingerprinting scans 300+ data points and occasionally false-positives on real users (shared networks, VPNs, aggressive privacy tools).
**Solution**: Have the contestant contact SweepWidget support to clear the flag (usually fast). To reduce recurrence, prefer login-required/verified entry methods and set expectations that honor-system entries (e.g. YouTube likes) can't be verified. For list quality afterward, use `/sales-deliverability`.
