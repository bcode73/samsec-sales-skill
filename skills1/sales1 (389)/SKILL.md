---
name: sales-ontraport
description: "Ontraport platform help — all-in-one CRM + marketing automation + payments + dynamic CMS for small/mid-market businesses (ontraport.com): contacts, pipelines, email/SMS campaigns, automation, order forms/subscriptions, and membership pages on one database. Covers the object-based REST API (base api.ontraport.com/1, Api-Key + Api-Appid headers, every record is an object with an objectID, 180 requests/minute limit) and webhook subscriptions. Use when building an Ontraport API integration to sync contacts or transactions into a CRM or warehouse, figuring out the objectID model, hitting the 180-requests-per-minute rate limit, subscribing to a webhook for new-sale or tag events, the steep learning curve has you stuck, contact-overage charges are escalating your bill, the email editor is fighting you, or choosing a plan (Basic vs Plus vs Pro vs Enterprise). Do NOT use for choosing a CRM across vendors or comparing Ontraport vs Keap/HubSpot/GoHighLevel (use /sales-crm-selection)."
argument-hint: "[describe what you need help with in Ontraport]"
license: MIT
version: 1.0.0
tags: [sales, crm, all-in-one, platform]
github: "https://github.com/Ontraport"
---

# Ontraport Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Build a REST API integration — sync contacts/objects, read transactions, manage records
   - B) Subscribe to a webhook — react to object created, form submitted, tag added/removed, product purchased, transaction added
   - C) Configure a module inside Ontraport — CRM pipelines, Campaign Builder automation, email/SMS, order forms, dynamic CMS pages/membership
   - D) Pick a plan — Basic vs Plus vs Pro vs Enterprise (note: per-contact pricing)
   - E) Fix a problem — learning curve, cost/overage escalation, email editor, deliverability
   - F) Something else — describe it

2. **Where does data need to flow?** Stay inside Ontraport / sync to a CRM or warehouse / drive an external app — this decides API vs webhook vs Zapier.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Choosing a CRM across vendors (Ontraport vs Keap vs HubSpot…) | `/sales-crm-selection {question}` |
| Email-marketing strategy and sequences | `/sales-email-marketing {question}` |
| Email deliverability / inbox placement | `/sales-deliverability {question}` |
| SMS marketing strategy / compliance | `/sales-sms-marketing {question}` |
| Membership-site / course structure and retention | `/sales-membership {question}` |
| Checkout / order-form / upsell conversion | `/sales-checkout {question}` |
| Affiliate / partner-program design across tools | `/sales-affiliate-program {question}` |

When routing, give the exact command, e.g. "This is a CRM-selection question — run: `/sales-crm-selection {your question}`".

## Step 3 — Ontraport platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (API/webhook/UI-only), per-contact pricing and plan limits, the object/contact/transaction data model with JSON shapes, and quick-start recipes (create a contact via the objects API; subscribe to a new-sale webhook; page through objects with range/start).

**Read `references/ontraport-api-reference.md`** for the API — base `https://api.ontraport.com/1`, the `Api-Key` + `Api-Appid` auth, the object model (`objectID`, `/objects`, `/object`, `/objects/meta`), pagination (`range`/`start`/`listFields`/`sort`/`condition`), the 180-requests/minute limit, and the webhook event list.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Everything is an object.** The API is object-oriented, not one-endpoint-per-resource. Each record type has a numeric `objectID` (Contact = `0`); you operate through `/1/objects` (+ `objectID`) rather than `/contacts`. Call `GET /1/objects/meta` to discover the objectIDs in the account.
- **Auth with two headers.** Send `Api-Key` and `Api-Appid` (both from Administration → Integrations) in headers — never in the URL or body.
- **Paginate with `range` + `start`.** List calls cap at 50 per page; loop with `start` offset, and pass `listFields` to fetch only the fields you need. Complex queries use a JSON `condition`.
- **Throttle to 180 requests/minute.** It's a rolling limit — read the rate-limit response headers and back off before you hit it.
- **Use webhooks for events** (new sale, tag added, transaction added) instead of polling — subscribe via the API and check Administration → Integrations → Webhook Logs to debug.
- **Set pricing expectations early.** Ontraport is per-contact — the bill climbs with list size and overages stack. Suppress/clean inactive contacts so you don't pay for dead weight.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing, which change frequently.*

1. **Steep learning curve is the #1 complaint.** Powerful but not intuitive — budget real ramp time and lean on Ontraport University. Don't promise plug-and-play.
2. **Per-contact pricing escalates.** The bill grows with contact count and overages stack unpredictably (users report ~$600/mo at ~43k contacts). Below ~$10k/mo revenue it can cost more than it returns — flag this when someone's evaluating it.
3. **The object model trips up first-time API users.** There's no `/contacts` resource — it's `/1/objects?objectID=0`. Discover objectIDs via `GET /1/objects/meta` before coding.
4. **Email editor is a "fake" drag-and-drop.** Reviewers find it clunky and the template library smaller than email-first tools. Set expectations for heavily-designed emails.
5. **180 requests/minute, rolling.** Bulk syncs need throttling + backoff; watch the rate-limit headers.
6. **Send credentials in headers only.** `Api-Key`/`Api-Appid` in GET params or POST body is a security risk Ontraport explicitly warns against.
7. **Deliverability is mixed in reviews** — authenticate the sending domain and keep complaint rates low.

## Related skills

- `/sales-crm-selection` — CRM comparison and selection (Ontraport vs Keap, HubSpot, GoHighLevel, Attio, and others)
- `/sales-email-marketing` — Email/SMS campaign and sequence strategy
- `/sales-deliverability` — Inbox placement, domain authentication, spam avoidance
- `/sales-membership` — Membership-site and course structure, pricing, retention
- `/sales-checkout` — Order-form, upsell, and payment conversion optimization
- `/sales-affiliate-program` — Designing and running an affiliate/partner program (Ontraport has native partner programs)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync new signups into Ontraport as contacts (developer/automation)
**User says**: "From my app I want to create a contact in Ontraport via the API. What's the call and how does the object thing work?"
**Skill does**: Explains the object model (Contact = `objectID 0`) and shows `POST https://api.ontraport.com/1/objects` with `Api-Key` + `Api-Appid` headers and a body of `objectID=0` plus the contact fields (Recipe 1 in `references/platform-guide.md`). Notes discovering objectIDs via `GET /1/objects/meta`, upserting to avoid duplicates, and the 180/min limit.
**Result**: User understands the objectID model and has a working create-contact call.

### Example 2: Fire fulfillment the instant someone buys (developer)
**User says**: "I want a webhook when someone purchases, not a polling job on transactions."
**Skill does**: Points to subscribing a webhook **via the API** on the product-purchased / transaction-added event, describes the JSON payload and `Api-Key`/`Api-Appid` header auth, and explains responding `2xx` fast + deduping (Recipe 2). Notes Webhook Logs (Administration → Integrations) for debugging and the 10,000-entry log cap.
**Result**: User has an event-driven webhook instead of a cron.

### Example 3: Is Ontraport going to get expensive as I grow?
**User says**: "I'm at 5k contacts now but expect 50k next year. Will Ontraport's price blow up?"
**Skill does**: Explains per-contact pricing and overage stacking (Plus/Pro tiers, +$46/user), gives the ~$600/mo-at-43k data point as a reality check, and suggests list hygiene to control cost. If they're really weighing vendors, routes: "To compare across CRMs — run: `/sales-crm-selection Ontraport vs alternatives at 50k contacts`."
**Result**: User gets a realistic cost trajectory and a path to a vendor comparison.

## Troubleshooting

### API returns 401 Unauthorized
**Symptom**: Requests fail even with valid-looking credentials.
**Cause**: Missing/misplaced `Api-Key` or `Api-Appid` header (sent in URL/body instead of headers), or the wrong App ID.
**Solution**: Send both `Api-Key` and `Api-Appid` as request headers (generate them under Administration → Integrations). Confirm you're hitting the `https://api.ontraport.com/1` base. Use the interactive Live API doc to validate the credentials before debugging your code.

### "I can't find the contacts endpoint"
**Symptom**: There's no `/contacts` route in the API.
**Cause**: Ontraport's API is object-based — contacts are objects, not their own resource.
**Solution**: Use `/1/objects` with `objectID=0` for contacts (GET to list, POST to create, PUT to update, DELETE to remove). Run `GET /1/objects/meta` to list every object type and its objectID. Use `range`/`start` to paginate and `listFields` to limit returned fields.

### Hitting the rate limit (429)
**Symptom**: Bulk operations start failing.
**Cause**: You've exceeded 180 requests per minute (rolling).
**Solution**: Read the rate-limit response headers and throttle below 180/min; on `429`, back off exponentially with jitter. Batch with `range` (up to 50 records/call), request only needed `listFields`, and queue large migrations rather than firing them in a tight loop.
