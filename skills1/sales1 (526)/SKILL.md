---
name: sales-shortstack
description: "ShortStack (shortstack.com) platform help — campaign platform for contests, giveaways, sweepstakes, quizzes, refer-a-friend, instant-win, and hashtag/comment-to-enter promotions, with lead capture, automatic winner selection, and analytics. Developer surface: an Entries API (`entries.shortstack.com`, `Authorization: Token token=`, per_page ≤5000, `{data:[...]}` response) and real-time signed webhooks (`X-Ss-Signature` HMAC of body + secret) on each new entry, plus a Webhooks management API, native Mailchimp/HubSpot/Salesforce, and Zapier. Free-forever plan + paid tiers. Use when reading entries/leads via the API, verifying or wiring the signed webhook, syncing entrants to an ESP/CRM or Zapier, picking a campaign type, handling giveaway fraud, or exporting leads. Do NOT use for giveaway/audience-growth strategy across tools (use /sales-audience-growth), generic iPaaS wiring (use /sales-integration), or email deliverability (use /sales-deliverability)."
argument-hint: "[describe what you need help with in ShortStack]"
license: MIT
version: 1.0.0
tags: [sales, audience-growth, giveaway, platform]
---

# ShortStack Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Read entries/leads via the Entries API (paging, newest-first)
   - B) Receive entries in real time via the signed webhook (and verify `X-Ss-Signature`)
   - C) Sync entrants to an ESP/CRM (Mailchimp/HubSpot/Salesforce) or Zapier
   - D) Pick + set up a campaign type — contest, sweepstakes, quiz, refer-a-friend, instant-win, hashtag/comment-to-enter
   - E) Handle giveaway fraud / fake entries, or pick a winner fairly
   - F) Decide Free vs a paid tier, or export leads

2. **API or no-code?** Code integration → Entries API + signed webhooks. No endpoint → native ESP/CRM connectors or Zapier.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Giveaway / audience-growth **strategy** across tools (which tool, viral mechanics) | `/sales-audience-growth {question}` |
| Connecting ShortStack to a CRM/ESP generically (iPaaS) | `/sales-integration {question}` |
| Email sequences for the list you collect | `/sales-email-marketing {question}` |
| Deliverability of giveaway/notification emails | `/sales-deliverability {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-audience-growth maximize entries on a refer-a-friend contest`".

## Step 3 — ShortStack platform reference

**Read `references/platform-guide.md`** for the full reference — the campaign-type + module map (what's API vs webhook vs UI-only), the entry/lead data model, plan tiers, and quick-start recipes (pull entries via the API; verify the signed webhook; sync to an ESP).

**Read `references/shortstack-api-reference.md`** for the integration surface — the **Entries API** (base `https://entries.shortstack.com/entries`, **`Authorization: Token token=`** header, `per_page` ≤5000, `sort`/`direction`, `{data:[...]}` response) and the **signed webhook** (`X-Ss-Signature` = HMAC of request body + your secret key) that fires on each new entry, plus the Webhooks management API + sandbox.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Read entries with the token header.** `GET https://entries.shortstack.com/entries` with `Authorization: Token token=YOUR_API_KEY`; page newest-first with `sort=received&direction=descending&per_page=…` (max **5000**). Response is `{ "data": [ … ] }`.
- **Verify the webhook signature.** ShortStack signs each webhook with **`X-Ss-Signature`** = HMAC(request body + secret). Recompute and constant-time compare before trusting the payload — this is a real signed webhook, so use it (don't skip verification). Still dedupe on the entry id.
- **Prefer a native ESP/CRM connector when you can.** Mailchimp/HubSpot/Salesforce sync directly; use Zapier or the webhook only when you need custom routing.
- **Pick the campaign type to the goal.** Contests/sweepstakes for reach, quizzes for segmentation, refer-a-friend for virality, instant-win for engagement, hashtag/comment-to-enter for social. Winner selection is automatic.
- **Plan for fraud.** Viral contests attract fake/disposable entries and multi-entry abuse — validate emails before counting/rewarding and review entries before drawing a winner.
- **Mind the plan.** Free-forever plan exists; advanced features, entry volume, and white-labeling scale with paid tiers (best-effort — verify current pricing). ShortStack also serves big brands/agencies, so tiers run up to enterprise.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — the help center is Cloudflare-protected, so some API/pricing specifics are from indexed sources; verify in-account.*

1. **Entries API auth is a token header.** `Authorization: Token token=YOUR_API_KEY` (note the `token=` prefix) — not a bare bearer; a wrong format 401s.
2. **`per_page` max is 5000 (default 100).** For large accounts, page with `sort=received&direction=descending` and confirm the cursor/offset for beyond 5000 in the live docs.
3. **The webhook IS signed — verify it.** `X-Ss-Signature` is an HMAC of the body + your secret. Unlike many giveaway tools (no HMAC), you can and should verify authenticity; failing to is the main security gap.
4. **Campaigns are UI-built.** The API reads entries and manages webhooks; you don't create campaigns via API. Build them in the app.
5. **Help center is bot-protected.** Exact endpoint catalog + entry/webhook payload schema need confirming in-account (Cloudflare blocks automated fetches).
6. **Contests attract fraud.** Disposable emails, same-person multi-entry — validate before counting and review before awarding.
7. **Tiers scale to enterprise.** A free plan exists, but advanced/volume/white-label features are paid; ShortStack's bigger customers are enterprise/agencies, so confirm what your tier includes.

## Related skills

- `/sales-audience-growth` — Giveaway / contest / audience-growth strategy across tools (ShortStack is one of the contest platforms covered) — viral mechanics, tool selection
- `/sales-email-marketing` — Email sequences for the list you grow with a contest
- `/sales-integration` — Connecting ShortStack to a CRM/ESP via the Entries API / webhooks / Zapier
- `/sales-deliverability` — Inbox placement and list quality for the emails you collect
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Pull new entries into my system via the API (developer/automation)
**User says**: "How do I fetch the latest entries from my ShortStack campaign programmatically?"
**Skill does**: Shows `GET https://entries.shortstack.com/entries` with the **`Authorization: Token token=YOUR_API_KEY`** header, using `sort=received&direction=descending&per_page=50` to get newest-first (max **5000**), and parsing the `{ "data": [ … ] }` response. Notes the API **reads** entries (campaigns are UI-built) and recommends the **signed webhook** for real-time instead of polling.
**Result**: A working, paged pull of the campaign's entries.

### Example 2: Verify the entry webhook so I can trust it
**User says**: "ShortStack is POSTing entries to my endpoint — how do I make sure they're really from ShortStack?"
**Skill does**: Explains the **`X-Ss-Signature`** header is an **HMAC of the request body + your secret key**; the handler should recompute the HMAC over the raw body and **constant-time compare** to the header, rejecting on mismatch. Adds dedupe on the entry id (retries) and treating the endpoint as secret. Notes Zapier as a no-code alternative if they don't want to host an endpoint.
**Result**: Authenticated, tamper-evident webhook intake.

### Example 3: Which campaign type — and how do entries flow to my ESP?
**User says**: "I want a refer-a-friend giveaway that adds entrants to Mailchimp. What do I pick?"
**Skill does**: Recommends the **refer-a-friend** campaign type for virality and the **native Mailchimp** connection (direct) so entrants sync automatically — or Zapier/the webhook for custom routing. Flags double-opt-in + fraud filtering before nurture, automatic winner selection at the end, and routes deeper viral-mechanics strategy: "run: `/sales-audience-growth maximize referrals on a giveaway`."
**Result**: The right campaign type wired to the user's ESP.

## Troubleshooting

### My Entries API calls return 401
**Symptom**: Requests to `entries.shortstack.com/entries` are rejected as unauthorized.
**Cause**: The auth header is malformed — ShortStack expects `Authorization: Token token=YOUR_API_KEY` (the literal `Token token=` prefix), not `Bearer ...` or a bare key.
**Solution**: Send exactly `Authorization: Token token=YOUR_API_KEY` (key from account settings), over HTTPS, to `https://entries.shortstack.com/entries`. Test with `curl -i -H "Authorization: Token token=$API_KEY" "https://entries.shortstack.com/entries?per_page=25"`.

### My webhook signature check keeps failing
**Symptom**: The HMAC you compute doesn't match `X-Ss-Signature`.
**Cause**: Signing over a re-serialized/parsed body instead of the **raw** bytes, a wrong secret, or the wrong HMAC encoding.
**Solution**: Compute the HMAC over the **raw request body** (before any JSON parsing) using your shared **secret key**, match the encoding ShortStack uses, and constant-time compare to `X-Ss-Signature`. Capture a live delivery to confirm the exact scheme (the help center is bot-protected). Once verified, dedupe on the entry id.

### My contest is full of fake entries
**Symptom**: A spike of disposable-email or duplicate entries.
**Cause**: Viral contests attract fraud — disposable emails, multi-entry, bots.
**Solution**: Validate/verify emails before counting, watch for same-person multi-entry, add friction (double opt-in), and review entries before the automatic winner draw. For list quality/deliverability afterward, use `/sales-deliverability`.
