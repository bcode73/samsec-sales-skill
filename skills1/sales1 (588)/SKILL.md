---
name: sales-systemeio
description: "Systeme.io platform help — budget all-in-one for bootstrappers and solopreneurs (systeme.io): sales funnels + website, email marketing, online courses, community + booking, CRM pipelines + automation, affiliate management, automated webinars, and a genuinely usable free plan. Covers the REST API (base api.systeme.io, X-API-Key header, contacts/tags/funnels/orders/subscriptions/webhooks endpoints, cursor pagination, 429 rate-limit headers) and webhook events. Use when building a Systeme.io API integration to sync contacts or tags into a CRM, working around its small native-integration ecosystem with the API or Zapier, emails arriving late or going to spam, the drag-and-drop page builder feels restrictive, setting up a webhook for new-sale or tag events, hitting 429 rate limits, migrating in from another tool, or choosing a plan (Free vs Startup vs Webinar vs Unlimited). Do NOT use for funnel strategy across tools or comparing Systeme.io against other all-in-one platforms (use /sales-funnel)."
argument-hint: "[describe what you need help with in Systeme.io]"
license: MIT
version: 1.0.0
tags: [sales, funnel, all-in-one, platform]
github: "https://github.com/systemeio"
---

# Systeme.io Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Build a REST API integration — sync contacts/tags, read funnels/orders/subscriptions, manage webhooks
   - B) Set up a webhook — react to contact created, tag added/removed, new sale, or sale canceled
   - C) Configure a module inside Systeme.io — funnels/pages, email + automation, courses, community, affiliates, webinars
   - D) Pick a plan — Free vs Startup vs Webinar vs Unlimited
   - E) Fix a problem — email deliverability, page-builder limits, missing native integration, migration, rate limits
   - F) Something else — describe it

2. **Where does data need to flow?** Stay inside Systeme.io / sync to a CRM or warehouse / drive an external app — this decides API vs webhook vs Zapier.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Multi-step funnel strategy/structure across tools | `/sales-funnel {question}` |
| Email-marketing strategy and sequences | `/sales-email-marketing {question}` |
| Email deliverability / inbox placement | `/sales-deliverability {question}` |
| Course / membership / community structure and retention | `/sales-membership {question}` |
| Automated / evergreen webinar funnel strategy | `/sales-webinar {question}` |
| Affiliate-program design across tools | `/sales-affiliate-program {question}` |
| Comparing Systeme.io vs other all-in-one platforms | `/sales-funnel {question}` |

When routing, give the exact command, e.g. "This is a deliverability question — run: `/sales-deliverability {your question}`".

## Step 3 — Systeme.io platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's API-accessible vs webhook-accessible vs UI-only), the free-plan limits and plan gates, the contact/tag/order data model with JSON shapes, and quick-start recipes (create a contact + assign a tag via the API; register a new-sale webhook; paginate contacts into a warehouse).

**Read `references/systemeio-api-reference.md`** for the REST API — base `https://api.systeme.io`, the `X-API-Key` auth, the resource endpoints (contacts, tags, funnels, products, subscriptions, campaigns, orders, webhooks), cursor pagination (`startingAfter` + `limit`), the rate-limit headers, and the webhook event list.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **The API is the answer to the small integration ecosystem.** Systeme.io has fewer native connectors than GoHighLevel/ActiveCampaign — when a native integration is missing, the public REST API (or Zapier/Make/Pabbly/n8n) is the supported path. The API is available across plans, including Free.
- **Auth with `X-API-Key`.** Generate a key in profile settings → Public API keys (max 3, each with a name + expiry). Pass it in the `X-API-Key` header (Bearer also accepted).
- **Paginate with the cursor.** List endpoints use `startingAfter` (the ID of the last item you saw) + `limit` — not page numbers. Loop until a short page comes back.
- **Respect the rate limit.** Watch `X-RateLimit-Remaining`; on `429`, honor `Retry-After` and back off. Don't hammer list endpoints in tight loops.
- **Use webhooks for sales events** (new sale, sale canceled, tag added) instead of polling `/api/orders` — lower latency and cheaper on the rate limit.
- **Deliverability is on you.** Systeme.io sends are only as good as your list hygiene and authentication — warm up, authenticate your domain, and avoid cold/purchased lists to keep out of spam.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing, which change frequently.*

1. **Small native-integration ecosystem.** Far fewer one-click connectors than competitors — plan to use the public API, Zapier/Make/Pabbly/n8n, or webhooks for anything non-native. This is the most common structural complaint.
2. **Page builder is intentionally simple.** The drag-and-drop editor trades design flexibility for ease — users coming from Leadpages/Unbounce find it restrictive and occasionally buggy. Set expectations; don't promise pixel-perfect control.
3. **Email templates are basic.** Great for plain, deliverable text emails; weak for heavily designed HTML. If a brand needs rich templates, flag the limitation early.
4. **Deliverability can be inconsistent** — delayed or filtered sends show up in reviews. Authenticate the sending domain, warm up, and keep complaint rates low.
5. **Cursor pagination, not pages.** Use `startingAfter` + `limit`; assuming `?page=2` will silently miss records.
6. **Migration takes longer than expected.** Free migration is offered on the Unlimited plan, but timelines run long — budget extra time when switching in.
7. **API keys expire.** Keys are created with an expiry date — a silently-expired key looks like an auth bug. Rotate before expiry.

## Related skills

- `/sales-funnel` — Funnel strategy across tools (Systeme.io is one of the budget all-in-one funnel builders covered) and Systeme.io-vs-alternatives comparisons
- `/sales-email-marketing` — Email sequence and broadcast strategy
- `/sales-deliverability` — Inbox placement, domain authentication, and spam avoidance
- `/sales-membership` — Course, community, and membership structure, pricing, and retention
- `/sales-webinar` — Automated/evergreen webinar funnel strategy
- `/sales-affiliate-program` — Designing and running an affiliate program
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync new signups into Systeme.io and tag them (developer/automation)
**User says**: "When someone signs up in my app I want to create the contact in Systeme.io and tag them 'app-trial'. What API calls?"
**Skill does**: Shows `POST https://api.systeme.io/api/contacts` with the `X-API-Key` header and `{"email": "..."}` to create (upsert by email), then assigns the tag via the tags endpoint (Recipe 1 in `references/platform-guide.md`). Notes the tag must exist (create it once with `POST /api/tags`), and to watch `X-RateLimit-Remaining`.
**Result**: User has a create-contact-then-tag flow and understands the key + rate-limit handling.

### Example 2: Fire fulfillment the instant someone buys (developer)
**User says**: "I want a webhook when someone makes a purchase in Systeme.io, not a polling job."
**Skill does**: Points to registering a webhook (via `POST /api/webhooks` or the dashboard) on the **new sale** event, describes the payload, and explains responding `2xx` fast + deduping since deliveries can repeat (Recipe 2). Contrasts with polling `/api/orders`, which burns the rate limit.
**Result**: User sets up an event-driven webhook instead of a cron.

### Example 3: My emails are landing in spam
**User says**: "Half my Systeme.io broadcasts go to promotions or spam. How do I fix it?"
**Skill does**: Explains Systeme.io deliverability depends on domain authentication and list hygiene, then routes: "This is a deliverability problem — run: `/sales-deliverability my Systeme.io emails are going to spam`." Adds Systeme.io-specific first steps: authenticate the sending domain, send plain-text-leaning emails (the editor favors them), and suppress unengaged contacts.
**Result**: User gets platform context plus the right strategy skill.

## Troubleshooting

### API returns 401 Unauthorized
**Symptom**: Requests fail even with a key that worked before.
**Cause**: The `X-API-Key` header is missing/misspelled, the key has hit its **expiry date**, or it was deleted (max 3 keys per account).
**Solution**: Confirm the `X-API-Key` header is set; regenerate the key in profile settings → Public API keys with a fresh expiry; update the integration. Bearer-token auth is also accepted if you prefer the `Authorization` header.

### Hitting 429 Too Many Requests
**Symptom**: Bulk syncs start returning 429s.
**Cause**: You've exceeded the request budget shown in the `X-RateLimit-*` headers.
**Solution**: Read `X-RateLimit-Remaining` and slow down before you hit zero; on `429`, honor the `Retry-After` header and back off exponentially. Batch work, cache lookups, and paginate with `startingAfter` rather than re-fetching whole lists.

### A native integration I need doesn't exist
**Symptom**: The tool you want to connect isn't in Systeme.io's integrations list.
**Cause**: Systeme.io's native ecosystem is small by design.
**Solution**: Use the public REST API directly, or bridge through Zapier/Make/Pabbly/n8n, or set up a webhook (new sale, tag added) to push events to your own endpoint. For CRM sync, the `/api/contacts` + `/api/tags` endpoints plus webhooks cover most flows.
