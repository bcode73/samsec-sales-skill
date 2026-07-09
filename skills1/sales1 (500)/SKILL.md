---
name: sales-salesmate
description: "Salesmate platform help — AI-powered sales CRM for SMB/mid-market teams: contacts/companies, deal pipelines, activities, built-in calling + SMS, email sequences, marketing automation, Smart Flow workflows, ticketing/team inbox, and the Sandy AI copilot; RESTful v4 API (base `https://{linkname}.salesmate.io/apis/`, header auth `accessToken` + `x-linkname`, offset pagination via `rows`+`from`, 1500 calls/hour per link) plus Zapier/Make/Pipedream. Use when a Salesmate API call returns 401 because the `accessToken`/`x-linkname` headers are wrong, syncing Salesmate contacts/deals to a warehouse or another CRM, hitting the 1500-calls/hour limit, Sandy AI or sequences are locked because you're on the Basic plan, RingCentral call logging keeps needing re-authorization, Smart Flow credits run out mid-automation, or weighing Salesmate vs Pipedrive/Close/Freshsales. Do NOT use for comparing CRMs across vendors (use /sales-crm-selection) or outbound cadence strategy across tools (use /sales-cadence)."
argument-hint: "[describe what you need help with in Salesmate]"
license: MIT
version: 1.0.0
tags: [sales, crm, platform]
github: "https://github.com/salesmate"
---

# Salesmate Platform Help

Salesmate is an AI-powered sales CRM for SMB and mid-market teams — contacts/companies, deal
pipelines, activities, built-in calling + SMS, email sequences, marketing automation, Smart Flow
workflows, a ticketing/team inbox, and the Sandy AI copilot — with a RESTful v4 API and Zapier/Make
connectors.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Figure out which of these the user needs (ask only if their prompt doesn't already say):

1. **What kind of problem is this?**
   - A) API / integration build (auth headers, pagination, syncing data in/out)
   - B) Sequences, Smart Flow automation, or marketing campaigns not behaving
   - C) Built-in calling/SMS or a telephony integration (e.g. RingCentral)
   - D) Pricing, plan gates, Sandy AI / sequence / credit limits, or which plan to buy
   - E) Choosing whether Salesmate is the right CRM at all
2. **Which plan?** Basic / Pro / Business / Enterprise — features and limits differ sharply by tier.

**Skip-ahead rule:** if the user's prompt already has enough context, skip to Step 2 or Step 3.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Comparing Salesmate vs Pipedrive/Close/Freshsales/HubSpot or picking a CRM | `/sales-crm-selection {user's question}` |
| Outbound sequence/cadence strategy across platforms | `/sales-cadence {user's question}` |
| Email-marketing strategy (segmentation, deliverability) across tools | `/sales-email-marketing {user's question}` |
| SMS-marketing strategy / compliance across tools | `/sales-sms-marketing {user's question}` |
| Connecting Salesmate to other tools (Zapier/Make/native) | `/sales-integration {user's question}` |
| Contact enrichment for CRM records | `/sales-enrich {user's question}` |

When routing, give the exact command, e.g. "This is a CRM-comparison question — run: `/sales-crm-selection should I move from Salesmate to Pipedrive`".

## Step 3 — Salesmate platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface,
pricing/plan gates, data model (JSON shapes), integration recipes (cURL + Python), and integration
patterns. For raw API detail (endpoints, auth headers, search/pagination, error codes), read
`references/salesmate-api-reference.md`.

Answer using only the relevant section. Don't dump the whole reference.

## Step 4 — Actionable guidance

You no longer need the guide — focus on the user's situation.

- **Getting a 401?** Auth is header-based: `accessToken` = your Access Key (My Account → Access Key)
  and `x-linkname` = your account host (e.g. `demo.salesmate.io`). A 401 is almost always one of
  those two headers; a 403 means the user lacks access or the feature isn't enabled.
- **Base URL is per-account:** `https://{link_name}.salesmate.io/apis/{module}/v4/...`. Use **v4**.
- **Listing/searching is a POST** to `/apis/{module}/v4/search?rows=250&from=0` with a
  `displayingFields` + `filterQuery` + `sort` body; pagination is **offset-based** (`rows`+`from`),
  with `totalRows`/`totalPages` in `Data`.
- **Hitting limits?** The cap is **1500 API calls/hour per link** — batch reads with large `rows`,
  cache, and space out pages. Smart Flow automation is **credit-metered**; heavy flows stall when the
  monthly credit pool runs out.
- **Feature locked?** Sequences + Sandy AI = **Pro+**; power dialer/custom modules/SLAs = **Business+**.
- **No inbound webhooks** — push events OUT via a Smart Flow "API Call/Webhook" action or Make/Zapier
  "Watch …" triggers; write INTO Salesmate via the REST API.

If you discover a gotcha or workaround not in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing which change frequently.*

1. **Auth header naming is confusing.** The header key is `accessToken` and its value is your Access
   Key — but the official Postman collection stores that value in a variable labeled `sessionToken`,
   and Make surfaces three fields (API Key, API Token, Session Token). You also must send `x-linkname`
   (your account host). Mismatched headers = `401`.
2. **v1/v3 are deprecated** (slated May 1, 2023) — build on `v4`. A few resources (Products, Lookup
   Fields) still expose v1/v3 paths.
3. **Pagination is offset-based, not cursor.** Drive it with `rows` (≤250) + `from`, and stop on
   `totalRows`. Search/list endpoints are POSTs with a query body, not GETs.
4. **1500 API calls/hour per link**, account-wide, with no rate-limit response header — track usage
   yourself or you'll silently start failing.
5. **No inbound webhooks.** You can't subscribe to events via the API; use a Smart Flow API/Webhook
   action or an iPaaS "Watch" trigger to push out, and the REST API to write in.
6. **Sharp plan gates.** Sequences and Sandy AI need Pro ($39); power dialer/custom modules/SLAs need
   Business ($63). Smart Flow credits (5K/10K/15K by tier) can run out mid-automation. Calling/SMS
   numbers are a paid add-on. 24/7 support is Enterprise-only.

## Related skills

- `/sales-crm-selection` — CRM comparison & selection — is Salesmate right vs Pipedrive, Close, Freshsales, HubSpot, Zoho?
- `/sales-pipedrive` — Pipedrive platform help — the pipeline-first SMB CRM most often compared to Salesmate
- `/sales-cadence` — Outbound sequence/cadence strategy across platforms
- `/sales-email-marketing` — Email-marketing strategy across tools
- `/sales-sms-marketing` — SMS-marketing strategy and compliance across tools
- `/sales-integration` — Connecting Salesmate to other tools — webhooks, Zapier, Make, custom API
- `/sales-enrich` — Contact enrichment for CRM records
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: API returns 401 / how to authenticate (automation)
**User says**: "My Salesmate API calls keep returning 401 — I'm sending an Authorization Bearer token."
**Skill does**: Explains Salesmate doesn't use Bearer — auth is header-based API Key: send
`accessToken` (your Access Key from My Account → Access Key) and `x-linkname` (your account host, e.g.
`demo.salesmate.io`) plus `Content-Type: application/json`. Notes the base URL is
`https://{link_name}.salesmate.io/apis/contact/v4`, and that the Postman collection confusingly labels
the access-key value `sessionToken`. Points to the cURL quick-start in the API reference.
**Result**: User fixes the headers and the call succeeds.

### Example 2: Sync Salesmate contacts to a warehouse (automation)
**User says**: "I want to pull all my Salesmate contacts into BigQuery nightly. What's the cleanest way?"
**Skill does**: Shows the `POST /apis/contact/v4/search?rows=250&from=0` pattern with a
`displayingFields`/`filterQuery`/`sort` body, explains offset pagination via `from` + `rows` and
stopping on `Data.totalRows`, and warns to stay under the **1500 calls/hour per link** cap by using a
large page size and spacing requests. References the Python pagination recipe in the platform guide.
**Result**: User has a paginated, rate-aware export loop.

### Example 3: Is Salesmate the right CRM / why is Sandy AI missing?
**User says**: "We're a 7-person team on the Basic plan and Sandy AI and sequences are greyed out — is Salesmate worth upgrading or should we look elsewhere?"
**Skill does**: Explains sequences and Sandy AI are **Pro ($39)+** (Basic is CRM-only), frames
Salesmate's value as native calling/SMS + AI at SMB pricing, notes the trade-offs (credit-metered
automation, no inbound webhooks, weekday-only support below Enterprise), and routes the cross-vendor
decision to `/sales-crm-selection` for a structured Salesmate-vs-Pipedrive/Close/Freshsales call.
**Result**: User understands the upgrade and gets pointed to the comparison skill for the final call.

## Troubleshooting

### "Every Salesmate API call returns 401 Authentication Failure"
**Symptom**: 401 on every request.
**Cause**: Wrong/missing auth headers — Salesmate uses an API Key in the `accessToken` header plus the
`x-linkname` account host, not a Bearer token.
**Solution**: Send `accessToken: <Access Key>` (My Account → Access Key), `x-linkname:
{link_name}.salesmate.io`, and `Content-Type: application/json`. Confirm the base URL is your own
subdomain and you're calling `v4`. A 403 (not 401) means the user lacks access or the feature is off.

### "RingCentral call logging keeps breaking / I have to re-authorize"
**Symptom**: Calls and recordings stop syncing; you re-authorize and it works for a while.
**Cause**: The RingCentral integration's auth token expires/disconnects and must be re-linked.
**Solution**: Re-authorize the RingCentral connection in Salesmate settings; for reliability consider
Salesmate's **built-in** calling/SMS (numbers add-on) instead of a third-party telephony bridge, which
avoids the re-auth loop. Log a support ticket if it recurs frequently.

### "My Smart Flow automation stopped running partway through the month"
**Symptom**: Workflows that worked early in the month silently stop firing.
**Cause**: Smart Flow runs are **credit-metered** (5K/10K/15K per user/month by tier) and the pool ran
out.
**Solution**: Check remaining credits, trim noisy/looping flows, move bulk work to off-credit paths
(direct API), or upgrade the tier for a larger credit pool. Credits reset on the monthly cycle.
