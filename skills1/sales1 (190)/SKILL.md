---
name: sales-frill
description: "Frill (frill.co) platform help — affordable customer-feedback suite (Canny/Nolt/UserVoice alternative): feedback boards (voting/comments), public roadmaps, changelog announcements, surveys, and an embeddable widget. Developer surface: REST API (api.frill.co/v1, Bearer key, cursor pagination via after/endCursor) for ideas/comments/votes/statuses/topics/announcements; HMAC-SHA256-signed webhooks (idea/vote/comment/announcement events; triggered_at/event/data payload); a Frill-Script widget (identify users, surveys); SSO; and 15+ integrations (Slack/Jira/Linear/Intercom/Zapier). Use when reading or syncing ideas/votes via the API, verifying signed webhooks, embedding the widget or identifying users, mapping statuses/topics to your roadmap, or choosing Frill vs Canny/Nolt on price. Do NOT use for voice-of-customer / survey program strategy across tools (use /sales-customer-feedback), feedback aggregation across review/social sources (use /sales-noisely), or generic iPaaS wiring (use /sales-integration)."
argument-hint: "[describe what you need help with in Frill]"
license: MIT
version: 1.0.0
tags: [sales, customer-feedback, product, platform]
github: "https://github.com/Frill-co"
---

# Frill Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Read/sync ideas, votes, comments via the REST API (cursor pagination)
   - B) Verify a signed webhook (HMAC-SHA256) and react to idea/vote/comment events
   - C) Embed the widget / identify logged-in users / run a survey (Frill-Script)
   - D) Map Statuses + Topics to your public roadmap and changelog (Announcements)
   - E) Set up SSO or a native integration (Slack/Jira/Linear/Intercom/Zapier)
   - F) Decide Frill vs Canny/Nolt (price), or pick a plan

2. **API or no-code?** Code → REST API + signed webhooks. Front-end → Frill-Script widget. No endpoint → native integrations / Zapier.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Voice-of-customer / survey **program** strategy (NPS/CSAT) across tools | `/sales-customer-feedback {question}` |
| Aggregating feedback across **reviews/social/support** sources | `/sales-noisely {question}` |
| Connecting Frill to a CRM/PM tool generically (iPaaS) | `/sales-integration {question}` |
| Public review **generation** strategy | `/sales-customer-reviews {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-customer-feedback build a closed-loop feedback program`".

## Step 3 — Frill platform reference

**Read `references/platform-guide.md`** for the full reference — the Ideas/Roadmap/Announcements/Surveys module map (what's API vs widget vs UI), the prioritization matrix, plan tiers, the data model, and quick-start recipes (pull ideas via the API; verify a webhook; embed + identify a user).

**Read `references/frill-api-reference.md`** for the integration surface — base `https://api.frill.co/v1`, **Bearer** API-key auth (from app.frill.co/settings/company), **cursor pagination** (`after` ← `pagination.endCursor`), the resources (ideas/comments/votes/statuses/topics/followers/announcements/notes), **HMAC-SHA256 signed webhooks** (events + `triggered_at`/`event`/`data`/`data_type`), Frill-Script (widget/surveys/identify), and SSO.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Bearer auth + cursor pagination.** `Authorization: Bearer <key>` against `api.frill.co/v1`; page lists by passing `pagination.endCursor` as the next request's **`after`** param until `hasNextPage` is false. Keep the key server-side.
- **Webhooks are HMAC-SHA256 signed — verify them.** Compute `HMAC-SHA256(rawBody, webhookSecret)` (secret from Company Settings → Webhooks) and constant-time compare to the signature header. Payload is `{triggered_at, event, data_type, data}`; dedupe on the entity id + `triggered_at`.
- **Statuses + Topics drive the roadmap.** An Idea's **Status** is its roadmap column (suggestion → in progress → done) and **Topics** are tags; read/set them via the API to keep an external roadmap in sync.
- **Identify users in the widget.** Use **Frill-Script** to pass your logged-in user's identity so their votes/ideas attach to a real account (and SSO so they're auto-authenticated) — otherwise feedback is anonymous.
- **It's a feedback-board tool, not VoC surveys or aggregation.** Frill collects *solicited* board feedback + roadmap + changelog. For NPS/CSAT *programs* use `/sales-customer-feedback`; for mining *unsolicited* feedback across reviews/social use `/sales-noisely`.
- **Price is the pitch.** Frill positions as a cheap Canny/Nolt alternative (~$25/mo vs Canny's $400) — size the plan to seats/boards; startup/nonprofit discounts exist.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — API verbatim from developers.frill.co; pricing from reviews. Confirm in-account.*

1. **Cursor pagination, not page numbers.** Pass `endCursor` as **`after`**; loop until `hasNextPage` is false. Don't assume offset/page params.
2. **Webhooks are HMAC-SHA256 signed — don't skip verification.** Secret from Company Settings → Webhooks; compute over the **raw** JSON body and constant-time compare to the header.
3. **Bearer header is the recommended auth** (query-string `?api_key=` leaks via logs; Basic auth uses the key as the username). Keep the key server-side.
4. **Anonymous unless you identify users.** Without Frill-Script user identification (or SSO), board votes/ideas aren't tied to a real account — wire identification if you need per-user data.
5. **Feedback-board ≠ VoC survey ≠ aggregation.** Frill is solicited board feedback + roadmap + changelog; it doesn't run NPS/CSAT programs (→ `/sales-customer-feedback`) or mine reviews/social (→ `/sales-noisely`).
6. **Plan gates.** Higher tiers unlock more boards/admins/white-label/integrations; the headline ~$25/mo is the entry point (Enterprise ~$349). Verify what your tier includes.
7. **Some create/update fields aren't on the overview docs.** The GitBook docs support `.md` + a `?ask=` dynamic query — use them to confirm exact request bodies per resource.

## Related skills

- `/sales-customer-feedback` — Voice-of-customer / survey program strategy across tools (Frill is a feedback-board option) — program design, tool selection
- `/sales-featureos` — FeatureOS (formerly Hellonext) platform help — the closest like-for-like feedback-board competitor (boards + roadmap + changelog + knowledge base); differs on API auth (`API-KEY` header + `page`/`per_page` vs Frill's Bearer + cursor) and unsigned dashboard webhooks. Install: `npx skills add sales-skills/sales --skill sales-featureos`
- `/sales-sleekplan` — AI feedback board (auto-categorization/duplicate merging) with an MCP server; the AI-forward affordable alternative to Frill. Install: `npx skills add sales-skills/sales --skill sales-sleekplan`
- `/sales-userjot` — UserJot platform help — AI-first feedback board + MCP server, no per-seat pricing (Canny/Productboard alternative); contrast with Frill on webhook signing (Frill is **HMAC-SHA256-signed** + cursor pagination vs UserJot's unpublished scheme) and the `/requests` post resource. Install: `npx skills add sales-skills/sales --skill sales-userjot`
- `/sales-noisely` — AI feedback aggregation across reviews/social/support (complement: Frill = solicited boards, Noisely = unsolicited mining)
- `/sales-customer-reviews` — Public review generation strategy
- `/sales-integration` — Connecting Frill to a CRM/PM tool via API/webhooks/Zapier
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Pull ideas + votes into my system via the API (developer/automation)
**User says**: "How do I sync all the feedback ideas and their vote counts out of Frill?"
**Skill does**: Shows `GET https://api.frill.co/v1/ideas` with **`Authorization: Bearer <key>`**, paging via **`after=`** ← `pagination.endCursor` until `hasNextPage` is false, and reading each idea's status/topics/vote count (with `/v1/votes` / `/v1/comments` for detail). Notes keeping the key server-side, and that the **webhook** (idea/vote events) is better than polling for ongoing sync.
**Result**: A complete, paginated export of ideas + engagement.

### Example 2: Verify a Frill webhook so I can trust it
**User says**: "Frill is POSTing events to my endpoint — how do I verify them?"
**Skill does**: Explains the **HMAC-SHA256** signature: get the **Webhook Secret** (Company Settings → Webhooks), compute `hash_hmac('sha256', rawBody, secret)`, and **constant-time compare** to the signature header (reject on mismatch). Notes the payload shape `{triggered_at, event, data_type, data}`, deduping on entity id + `triggered_at`, and which events exist (idea/vote/comment/announcement).
**Result**: Authenticated, tamper-evident webhook intake.

### Example 3: Frill vs Canny — which feedback tool?
**User says**: "We're a small SaaS — Frill or Canny for a feedback board + roadmap?"
**Skill does**: Frames the tradeoff — **Frill** is the affordable pick (~$25/mo, boards + roadmap + changelog + surveys, REST API + signed webhooks), while **Canny** is pricier (~$400/mo lowest paid) with deeper enterprise features; **Nolt** is even simpler/per-board. Recommends Frill for cost-sensitive indie/SMB SaaS and routes broader tool selection: "run: `/sales-customer-feedback choose a product-feedback board tool`."
**Result**: A price-grounded board-tool choice.

## Troubleshooting

### My API only returns the first page of ideas
**Symptom**: You get ~25 ideas and can't reach the rest.
**Cause**: Frill uses **cursor pagination** — there are no `page`/`offset` params; you must follow the cursor.
**Solution**: Read `pagination.endCursor` and `pagination.hasNextPage` from the response, then repeat the request with **`?after=<endCursor>`** until `hasNextPage` is false. Accumulate results across pages.

### My webhook signature check fails
**Symptom**: The HMAC you compute doesn't match Frill's signature header.
**Cause**: Hashing a re-serialized body (not the raw bytes), the wrong **Webhook Secret**, or a wrong algorithm.
**Solution**: Compute **HMAC-SHA256 over the raw request body** with the **Webhook Secret** from **Company Settings → Webhooks**, then constant-time compare to the signature header. Match the docs' `hash_hmac('sha256', payloadJson, secret)` exactly; once verified, dedupe on the entity id + `triggered_at`.

### Votes/ideas in the widget are all anonymous
**Symptom**: Board activity isn't attributed to your actual users.
**Cause**: The Frill-Script widget isn't identifying users (no SSO / no identity passed).
**Solution**: Use **Frill-Script user identification** to pass your logged-in user's id/email/name (and/or set up **SSO**) so votes/ideas attach to real accounts. See `developers.frill.co/frill-script/identifying-users`. For VoC program strategy beyond boards, use `/sales-customer-feedback`.
