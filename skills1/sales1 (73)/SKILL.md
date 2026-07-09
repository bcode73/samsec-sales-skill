---
name: sales-builderall
description: "Builderall platform help — budget all-in-one suite for non-technical solopreneurs (builderall.com): website + funnel builders, MailingBoss email, SuperCheckout, CRM, courses/membership, webinars, chatbot, and booking. The only first-party API is MailingBoss (base member.mailingboss.com, token-in-URL auth, subscriber create/search/update/unsubscribe, per-list inbound webhooks); funnels/checkout/courses are UI-built and integrated via the API + webhooks + Zapier/Make/Pabbly. Use when wiring a MailingBoss API or webhook integration to sync contacts/tags into a CRM, a native connector is missing, emails landing in spam, deciding whether the funnel builder is on your plan tier, the platform feels overwhelming or has an outage, migrating in/out of an all-in-one, or choosing Free vs paid tiers. Do NOT use for funnel strategy across tools or Builderall-vs-alternatives comparison (use /sales-funnel), email-marketing strategy (use /sales-email-marketing), or inbox-placement deliverability (use /sales-deliverability)."
argument-hint: "[describe what you need help with in Builderall]"
license: MIT
version: 1.0.0
tags: [sales, funnel, all-in-one, platform]
---

# Builderall Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Build a MailingBoss API integration — sync contacts/tags into a CRM or warehouse
   - B) Set up an inbound webhook — push leads from a form/app into a MailingBoss list
   - C) Configure a module inside Builderall — funnels/pages, MailingBoss email, SuperCheckout, courses/membership, webinars
   - D) Pick a plan — Free vs entry vs funnel/marketer tier
   - E) Fix a problem — deliverability, outage, missing integration, overwhelm, migration
   - F) Something else — describe it

2. **Where does data need to flow?** Stay inside Builderall / sync to a CRM or warehouse / drive an external app — this decides API vs webhook vs iPaaS.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Multi-step funnel strategy/structure across tools, or Builderall vs alternatives | `/sales-funnel {question}` |
| Email-marketing strategy and sequences | `/sales-email-marketing {question}` |
| Email deliverability / inbox placement | `/sales-deliverability {question}` |
| Course / membership / community structure and retention | `/sales-membership {question}` |
| Checkout / order-bump / upsell optimization across tools | `/sales-checkout {question}` |
| Webinar funnel strategy | `/sales-webinar {question}` |

When routing, give the exact command, e.g. "This is a deliverability question — run: `/sales-deliverability {your question}`".

## Step 3 — Builderall platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's API-accessible vs UI-only), the plan gates (the funnel builder usually sits on a higher tier), the MailingBoss list/subscriber data model with JSON shapes, and quick-start recipes (upsert a contact by email + tag it; push a lead from a form/app; tag-on-purchase follow-up).

**Read `references/builderall-api-reference.md`** for the MailingBoss API — base `https://member.mailingboss.com/integration/index.php/`, token-in-URL auth, the verified subscriber endpoints (create / search-by-email / update / unsubscribe), the documented-but-confirm list/campaign routes, and the inbound webhook pattern.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **MailingBoss is the only programmatic surface.** Funnels, SuperCheckout, courses, CRM, webinars are UI-built. To move data in/out, use the MailingBoss subscriber API, the per-list inbound webhook, or Zapier/Make/Pabbly/Integrately — there is no broad REST API and no MCP server.
- **Auth is a token in the URL path.** The token is the last path segment; all other params go in the body. Treat the URL as a secret and rotate the token if it leaks.
- **Dedupe on email, not `subscriber_uid`.** Subscribers are scoped per-list, so search-by-email first, then create-or-update (Recipe 1).
- **Tags do the work.** `taginternals` drives MailingBoss automations and segmentation — tag on opt-in/purchase, then trigger sequences off the tag.
- **Set the price expectation honestly.** It's cheap at the entry tier, but the funnel builder and marquee features are usually gated to a higher (~$79.90/mo) plan — confirm the plan covers what the user needs.
- **Deliverability and uptime are real risks.** MailingBoss is weaker than specialist ESPs and reviews report periodic outages + slow support. For a launch, build/test ahead and keep a fallback; for inbox placement, route to `/sales-deliverability`.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing, which change frequently.*

1. **The funnel builder is often NOT on the cheapest plan.** "Builderall is cheap" is true for the entry tier, but funnel building and heavier features have historically required a higher (~$79.90/mo) tier. Confirm the plan before promising funnels on the budget plan.
2. **Only MailingBoss has an API.** Don't promise API access to funnels/checkout/courses — there isn't any. Plan integrations around MailingBoss subscribers + webhooks + iPaaS.
3. **The token lives in the URL.** Anyone with the endpoint URL can write to your lists. Keep it out of client-side code and logs; rotate on leak.
4. **Periodic outages.** Reviews report site, SuperCheckout, and email-send outages. Don't cut over mid-launch; keep a checkout/email fallback for time-sensitive events.
5. **Support is slow and has no phone line.** Expect multi-day email/ticket turnaround — don't depend on support to unblock a launch.
6. **Deliverability is inconsistent.** MailingBoss is frequently rated below dedicated ESPs. Authenticate your domain (SPF/DKIM/DMARC), warm up, and keep lists clean — or send through a specialist ESP and use Builderall for pages.
7. **Steep learning curve.** Most users report 1–2 weeks to get comfortable; the breadth (50+ tools) overwhelms beginners. Start with one funnel + one list, not the whole suite.
8. **Subscribers are per-list.** The same person on two lists has two `subscriber_uid`s — dedupe on email or you'll double-count.

## Related skills

- `/sales-funnel` — Funnel strategy across tools (Builderall is one of the budget all-in-one funnel builders covered) and Builderall-vs-alternatives comparisons
- `/sales-email-marketing` — Email sequence and broadcast strategy (MailingBoss campaigns)
- `/sales-checkout` — Checkout, order-bump, and upsell optimization (SuperCheckout)
- `/sales-membership` — Course, community, and membership structure, pricing, and retention
- `/sales-deliverability` — Inbox placement, domain authentication, and spam avoidance
- `/sales-webinar` — Live and automated/evergreen webinar funnel strategy
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync app signups into MailingBoss and tag them (developer/automation)
**User says**: "When someone signs up in my app I want to add them to a MailingBoss list and tag them 'app-trial'. What calls?"
**Skill does**: Shows the upsert-by-email pattern (Recipe 1 in `references/platform-guide.md`): `POST .../lists/subscribers/search-by-email/<TOKEN>` to find an existing `subscriber_uid`, then create or update with `email`, `list_uid`, and `taginternals=app-trial`. Notes the token sits in the URL path, params go in the body, and to dedupe on email since subscribers are per-list.
**Result**: User has a create-or-tag flow and understands token-in-URL auth + per-list dedupe.

### Example 2: A native integration I need doesn't exist
**User says**: "Builderall doesn't have a connector for my tool. How do I get leads into MailingBoss?"
**Skill does**: Explains MailingBoss is the integration surface and gives two no-/low-code paths — the per-list **inbound webhook URL** (point your form/app webhook at it) or an iPaaS "Create MailingBoss contact" action (Zapier/Make/Pabbly/Integrately), plus the direct create endpoint for code (Recipe 2/3). Sets expectation that funnels/checkout themselves have no API.
**Result**: User wires the missing integration via webhook or iPaaS.

### Example 3: My Builderall emails go to spam
**User says**: "Half my MailingBoss broadcasts land in spam or promotions. Fix?"
**Skill does**: Explains MailingBoss inbox placement depends on the user's domain authentication and list hygiene, gives Builderall-specific first steps (authenticate the sending domain, warm up, suppress unengaged contacts, consider a specialist ESP for critical sends), then routes: "This is a deliverability problem — run: `/sales-deliverability my Builderall emails are going to spam`."
**Result**: User gets platform context plus the right strategy skill.

## Troubleshooting

### API write returns an error or the subscriber isn't created
**Symptom**: A `create`/`update` call fails or silently doesn't add the contact.
**Cause**: The token isn't the last URL path segment, params were put in the URL instead of the body, `list_uid` is wrong/missing, or a custom field tag (`FNAME`, etc.) doesn't exist on the list yet.
**Solution**: Put the token as the final path segment and send `email` + `list_uid` (+ field tags) in the request **body**. Create custom fields in the list settings before passing them. Log the raw response once to confirm the envelope, then map `subscriber_uid` from it.

### Duplicate contacts piling up
**Symptom**: The same person appears multiple times.
**Cause**: Subscribers are scoped per-list, so blind `create` calls (or pushing the same lead to several lists) create separate records.
**Solution**: Search-by-email first and update if found (Recipe 1). Dedupe on `email` across lists in your own system; don't rely on `subscriber_uid` as a global id.

### Funnel features aren't available on my plan
**Symptom**: The funnel builder or a marquee tool is locked.
**Cause**: That feature is gated to a higher tier (the funnel builder has historically required ~$79.90/mo, not the entry/free plan).
**Solution**: Check builderall.com/pricing for the current tier that includes the funnel builder and the specific tools you need before committing — the entry price doesn't include everything.

### A send or the checkout suddenly stopped working
**Symptom**: Emails not going out, or SuperCheckout/page won't load.
**Cause**: Reviews report periodic platform outages.
**Solution**: Check Builderall status/community, retry, and open a ticket (expect multi-day turnaround). For launches, build/test ahead and keep an email/checkout fallback so an outage doesn't sink a time-sensitive event.
