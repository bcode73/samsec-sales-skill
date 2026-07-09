---
name: sales-maximizer
description: "Maximizer (maximizer.com) platform help — Canadian cloud/on-premise sales + financial-services CRM. Octopus API (Maximizer.Web.Data, base api.maximizer.com/octopus) is a POST-RPC service (/Authenticate, /Read, /Create, /Update, /Delete) with Scope/Criteria/Configuration query bodies, PAT or OAuth2 auth, and a separate Webhooks API (https://api.maximizer.com/webhooks, v1 targets + subscriptions). Use when an Octopus /Read returns nothing because Configuration.Drivers names the wrong searcher, building an AbEntry/Opportunity/Lead export to a warehouse or another CRM, a webhook silently stops after the 2-second / 3-attempt delivery limit, hitting the per-edition rate limit (Core 30/min, Business/Financial 90/min), wiring base64 record Keys or UDF (Udf/$TYPEID) fields, linking Outlook email to records without endless clicks, or choosing Base vs Sales Leader vs Financial Advisor editions. Do NOT use for comparing CRMs across vendors (use /sales-crm-selection) or generic iPaaS wiring (use /sales-integration)."
argument-hint: "[describe what you need help with in Maximizer]"
license: MIT
version: 1.0.0
tags: [sales, crm, platform]
github: "https://github.com/maximizercrm"
---

# Maximizer Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Build an API integration — read/write AbEntry (companies/contacts/individuals), Opportunities, Leads, Cases, Notes, Activities
   - B) Set up a webhook to push CRM changes into a warehouse / another CRM / Slack
   - C) Fix an auth (401) or token/PAT problem
   - D) Fix a rate-limit (429) or timeout (408) problem
   - E) Work with custom fields (UDFs), favorite lists, or the Read query syntax
   - F) Pick or understand an edition — Base / Sales Leader / Financial Advisor, cloud vs on-premise

2. **Cloud (CRM Live) or on-premise?** Auth differs: cloud uses a **Personal Access Token (PAT)** or `/Authenticate` with `VendorId`+`AppKey`; on-premise calls `/Authenticate` with just `Database`/`UID`/`Password`. Base URL for cloud is `https://api.maximizer.com/octopus`.

3. **Which edition?** Base/For Sales, Sales Leader, or Financial Advisor (households, investment/insurance views). Rate limits and some features are edition-gated.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| CRM selection/comparison or migration strategy across vendors | `/sales-crm-selection {question}` |
| CRM data cleanup, dedupe, record matching | `/sales-data-hygiene {question}` |
| Contact/company enrichment for CRM records | `/sales-enrich {question}` |
| Outbound sequence / cadence design across platforms (Maximizer has thin native sequencing) | `/sales-cadence {question}` |
| Connecting Maximizer to other tools generically (iPaaS, Zapier, Make) | `/sales-integration {question}` |
| Lead scoring model design | `/sales-lead-score {question}` |

When routing, give the exact command, e.g. "This is a CRM-comparison question — run: `/sales-crm-selection should I move from Maximizer to HubSpot at 30 people`".

## Step 3 — Maximizer platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's API- vs webhook- vs UI-only), editions and pricing/rate-limit gates, the AbEntry/Opportunity/Lead data model with JSON shapes, base64 Key encoding, the Read query syntax (Scope/Criteria/GroupBy/OrderBy + Configuration.Drivers), and quick-start recipes (authenticate + read contacts; nightly opportunity export; subscribe to a webhook target).

**Read `references/maximizer-api-reference.md`** for the integration surface — the Octopus base URL, the `/Authenticate` → PAT/OAuth2 flow, the POST-RPC endpoint list (`/Read`, `/Create`, `/Update`, `/Delete`, `/Validate`, `/BinaryUpload`, `/WorkflowStart`…), the Scope/Criteria operator catalog (`$EQ`/`$LIKE`/`$RANGE`/`$OFFSET()`…), the `Configuration.Drivers` searcher names, pagination via `OrderBy`+`Top`, the per-edition rate limits, and the Webhooks API (`/v1/targets`, `/v1/subscriptions`, payload shape, 2-second/3-attempt delivery rule).

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Every Read needs the right `Configuration.Drivers` searcher.** A `/Read` body specifies which entity searcher to use, e.g. `"IAbEntrySearcher": "Maximizer.Model.Access.Sql.AbEntrySearcher"`. Naming the wrong searcher (or omitting it) returns empty/unexpected results, not an error — this is the #1 "my query returns nothing" cause.
- **Keys are opaque base64 composites.** Record `Key` values (e.g. `Q29tcGFueQk...`) encode the entity type and IDs. Never construct or mutate them — read a record first, then pass its `Key` back on `/Update` and `/Delete`. A wrong-type Key fails silently or hits the wrong record.
- **Auth differs by deployment.** Cloud: mint a **PAT** in account settings (sent as a Bearer token) or `/Authenticate` with `Database`/`UID`/`Password`/`VendorId`/`AppKey`. On-premise: `/Authenticate` with just `Database`/`UID`/`Password`. A `{"Code":0}` from `/TokenValid` means the token is still good.
- **Budget the rate limit by edition.** Core allows ~30 calls / 10 s, Business/Financial ~90 / 30 s; exceeding returns `429`, and a long-running call can return `408`. Pull incrementally (filter on a date UDF/field with `$OFFSET()`), page with `OrderBy`+`Top`, and back off on `429`.
- **Webhooks are fragile by design.** Your target must return `200 OK` within **2 seconds**; Maximizer retries twice (3 attempts total) then **discards** the event. There is **no documented HMAC signature** — verify authenticity another way (allowlist source IPs, a secret path/header). ACK immediately, process async, and run a periodic reconciliation pull to catch dropped events.
- **Email logging is click-heavy.** Native Outlook/M365 sync is solid, but linking individual sent emails and syncing multiple mailboxes is a known friction point — for high-volume logging, drive it through the API or a BCC-dropbox pattern rather than manual clicks.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially pricing and edition-gated features, which change.*

1. **`Configuration.Drivers` must name the correct searcher** (e.g. `IAbEntrySearcher`, `IOpportunitySearcher`). Wrong/missing driver → empty result, not an error.
2. **Record `Key`s are base64 composites** that encode entity type + IDs. Read first, reuse the `Key`; never hand-build one.
3. **`Code: 0` means success.** The JSON envelope returns a numeric `Code`; non-zero is a failure — always check it even on a `200`.
4. **Webhooks need a 2-second `200` ACK and drop after 3 attempts**, with **no HMAC signature** documented. A slow receiver or brief outage silently loses events.
5. **Rate limits are per-edition** (Core ~30/min, Business/Financial ~90/min); `429` on exceed, `408` on slow calls.
6. **UDFs (custom fields) use `Udf/$TYPEID` notation** in webhook filters and queries — not the display name.
7. **Pricing is annual-commitment "rental."** Published rates assume annual billing; monthly is ~10–20% higher, and there's no free tier (30-day trial only).
8. **Two APIs, two base URLs.** Data is `https://api.maximizer.com/octopus`; webhooks live at `https://api.maximizer.com/webhooks`. The legacy **Ferret API** is being superseded by Octopus.

## Related skills

- `/sales-crm-selection` — CRM comparison, selection, and migration strategy across vendors (is Maximizer the right CRM, or time to switch?)
- `/sales-data-hygiene` — CRM data quality: dedupe, record matching, enrichment automation
- `/sales-enrich` — Contact/company enrichment for Maximizer records
- `/sales-cadence` — Outbound sequence/cadence design across platforms (Maximizer has thin native sequencing)
- `/sales-integration` — Connecting Maximizer to other tools via webhooks/Zapier/Make
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: My Octopus `/Read` returns an empty list (developer/automation)
**User says**: "I POST to `/Read` with a Scope and Criteria for contacts but get back zero rows even though they exist."
**Skill does**: Checks the `Configuration.Drivers` block — a contact/company read needs `"IAbEntrySearcher": "Maximizer.Model.Access.Sql.AbEntrySearcher"` (opportunities need `IOpportunitySearcher`). Confirms the `Criteria.SearchQuery` uses the operator syntax (`{"Type": {"$EQ": "Contact"}}`) and that the Bearer PAT is valid via `/TokenValid` (expect `{"Code":0}`). Shows the working `/Read` body from the API reference.
**Result**: The correct searcher returns the expected rows.

### Example 2: Nightly export of changed opportunities into a warehouse (developer/automation)
**User says**: "I want to pull opportunities that changed recently into BigQuery without tripping the rate limit."
**Skill does**: Recommends a `/Read` against `IOpportunitySearcher` filtered with a date operator (`$OFFSET()` / `$RANGE`) on a last-modified field, paginated with `OrderBy` + `Top`, selecting only needed `Scope.Fields`. Notes Core ~30/min vs Business/Financial ~90/min, to back off on `429`, and to persist each record's base64 `Key`. Points to Recipe 2 in the platform guide.
**Result**: A bounded incremental export that stays under the edition's rate limit.

### Example 3: Is Maximizer the right CRM for us?
**User says**: "We're a 12-advisor wealth firm comparing Maximizer's Financial Advisor edition to Salesforce Financial Services Cloud."
**Skill does**: Recognizes a cross-vendor selection question and routes: "run: `/sales-crm-selection 12-advisor wealth firm, Maximizer Financial Advisor vs Salesforce FSC`." Briefly notes Maximizer's edge (advisor/household features at ~$79/user/mo vs FSC's ~$325) and weak spots (reporting, email-logging friction) but defers the comparison to the strategy skill.
**Result**: User is handed to the right strategy skill with a ready prompt.

## Troubleshooting

### `/Read` returns nothing (no error)
**Symptom**: A `/Read` with valid Scope/Criteria returns an empty result and a `200`.
**Cause**: The `Configuration.Drivers` searcher is wrong or missing for the entity, or the `Criteria.SearchQuery` operator/field name doesn't match (e.g. querying a UDF by display name instead of `Udf/$TYPEID`).
**Solution**: Set the matching driver (`IAbEntrySearcher` for AbEntry, `IOpportunitySearcher` for Opportunity, etc.), verify field names via the object's Metadata read, and use the documented operators (`$EQ`, `$LIKE`, `$RANGE`, `$IN`…). Check the response `Code` — `0` is success.

### Webhook fired for a while, then stopped
**Symptom**: A subscription delivered events, then they silently stopped arriving.
**Cause**: The target failed to return `200 OK` within **2 seconds**; Maximizer retries twice and then **discards** the event after 3 total attempts. There's no signature to confirm authenticity and no built-in delivery log.
**Solution**: Make the target ACK `200` immediately and process async; confirm the target is still enabled (`/v1/targets/{id}/enable`) and the subscription's `Entity`/`Op`/`Filter` still match; run a periodic reconciliation `/Read` on a last-modified field to backfill dropped events.

### 401 / 408 / 429 on API calls
**Symptom**: Calls fail with `401 Unauthorized`, `408 Request Timeout`, or `429 Too Many Requests`.
**Cause**: `401` — expired/invalid PAT or wrong auth flow for cloud vs on-premise; `408` — a single call ran too long; `429` — exceeded the per-edition rate window (Core ~30/10s, Business/Financial ~90/30s).
**Solution**: Re-check the token with `/TokenValid` and re-mint the PAT if needed (cloud uses Bearer PAT or `/Authenticate` with `VendorId`/`AppKey`; on-premise omits those). Split heavy `/Read`s into smaller pages (`Top` + `OrderBy`), select fewer `Scope.Fields`, and add exponential backoff on `429`.
