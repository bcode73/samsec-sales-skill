---
name: sales-clickfunnels
description: "ClickFunnels platform help — the category-defining all-in-one funnel builder, now ClickFunnels 2.0 (clickfunnels.com): multi-step funnels + page builder, e-commerce, email/automation (Workflows), CRM, courses, checkout with one-click upsells and order bumps, A/B testing, and Backpack affiliate management. Covers the V2 REST API (base {workspace}.myclickfunnels.com/api/v2, Bearer token + required User-Agent header or OAuth 2.0, cursor+offset pagination, signed webhooks) — the V1/Classic API is deprecated. Use when building a ClickFunnels 2.0 API or webhook integration, your API token 401s or you can't find where to generate it, the workspace-subdomain base URL is confusing, syncing contacts or orders into a CRM, the platform feels buggy or page previews won't load, per-send email costs climb as your list grows, migrating from Classic to 2.0, or choosing a plan (Startup vs Pro). Do NOT use for funnel strategy across tools or comparing ClickFunnels against other funnel builders (use /sales-funnel)."
argument-hint: "[describe what you need help with in ClickFunnels]"
license: MIT
version: 1.0.0
tags: [sales, funnel, all-in-one, platform]
github: "https://github.com/clickfunnels"
---

# ClickFunnels Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **Are you on ClickFunnels 2.0 or Classic (1.0)?** 2.0 is the current platform with the V2 REST API; Classic is legacy and its V1 API is deprecated. This changes every API answer.

2. **What are you trying to do?**
   - A) Build a V2 API integration — sync contacts/products/orders/subscriptions, manage funnels/pages
   - B) Set up webhooks — react to contact/order/subscription/funnel events with signature verification
   - C) Configure a module inside ClickFunnels — funnels/pages, Workflows automation, checkout/upsells, courses, CRM/opportunities, Backpack affiliates
   - D) Pick a plan — Startup vs Pro (note: API access is plan-gated)
   - E) Fix a problem — bugs/page previews, email cost escalation, Classic→2.0 migration, deliverability
   - F) Something else — describe it

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Multi-step funnel strategy/structure across tools | `/sales-funnel {question}` |
| Comparing ClickFunnels vs other funnel builders | `/sales-funnel {question}` |
| Email-marketing strategy and sequences | `/sales-email-marketing {question}` |
| Email deliverability / inbox placement | `/sales-deliverability {question}` |
| Checkout / order-bump / upsell conversion optimization | `/sales-checkout {question}` |
| Course / membership structure and retention | `/sales-membership {question}` |
| Affiliate-program design across tools | `/sales-affiliate-program {question}` |

When routing, give the exact command, e.g. "This is a funnel-strategy question — run: `/sales-funnel {your question}`".

## Step 3 — ClickFunnels platform reference

**Read `references/platform-guide.md`** for the full reference — the 2.0-vs-Classic split, the module map (API/webhook/UI-only), per-plan limits and the per-send email cost model, the contact/product/order data model with JSON shapes, and quick-start recipes (create/upsert a contact via the V2 API; register a signed webhook for new orders; paginate contacts into a warehouse).

**Read `references/clickfunnels-api-reference.md`** for the V2 API — the two base URLs (`accounts.myclickfunnels.com/api/v2` for team-level, `{workspace}.myclickfunnels.com/api/v2` for workspace data), the `Bearer` token + required `User-Agent` auth, the team→workspace bootstrap flow, the full resource list, cursor/offset pagination + `expand[]`, and the webhook endpoints/events.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Confirm 2.0 vs Classic first.** They're different products with different APIs. Build on the **V2 API** (`developers.myclickfunnels.com`); the Classic V1 API (`apidocs.clickfunnels.com`) is deprecated.
- **Two base URLs.** Team-level calls (`/teams`, `/workspaces`) go to `accounts.myclickfunnels.com/api/v2`; workspace data (contacts, orders, funnels) goes to `{workspace}.myclickfunnels.com/api/v2`. Bootstrap with `GET /api/v2/teams` → `GET /api/v2/teams/{id}/workspaces`.
- **A `User-Agent` header is required** alongside `Authorization: Bearer {token}` — omit it and calls fail. Tokens are generated per team in Team Settings → Developer Portal.
- **Use `id`, not `public_id`.** URLs surface a `public_id`, but POST/PATCH payloads expect the internal `id` — a common 422 cause.
- **Watch the per-send email cost.** ClickFunnels charges per email send; a big list makes the bill climb. Run the math before migrating a large list in, and lean on tags/segments to send less.
- **Use signed webhooks instead of polling** for order/contact/subscription events — register a `webhook_endpoint` and verify the signature.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing, which change frequently.*

1. **2.0 ≠ Classic.** Two separate platforms, logins, and APIs. The V1 (Classic) API is deprecated — don't build new integrations on it.
2. **API access is plan-gated** to the higher tier (Pro, ~$297/mo; some plan generations call it Scale/Optimize/Dominate). An integration can't start on the entry plan — verify the account's plan first.
3. **Per-send email pricing escalates.** Unlike flat-rate competitors, ClickFunnels bills per email send, so cost grows with list size and frequency. Account for this before importing a large list.
4. **No bulk contact import** has been a long-standing gap — large list onboarding may need the API or a workaround.
5. **2.0 has real stability complaints** — page previews that don't load, features that ship under-tested. Expect occasional bugs; keep a Classic/backup plan during launches.
6. **`User-Agent` header is mandatory** on V2 calls, and payloads use `id` (not the URL's `public_id`).
7. **Migration is risky.** Classic→2.0 (or importing big lists) mid-launch can break revenue flows — migrate in a staging workspace and test before cutover.

## Related skills

- `/sales-funnel` — Funnel strategy across tools (ClickFunnels is the category-defining builder covered) and ClickFunnels-vs-alternatives comparisons
- `/sales-email-marketing` — Email sequence and broadcast strategy
- `/sales-deliverability` — Inbox placement, domain authentication, spam avoidance
- `/sales-checkout` — Checkout, order-bump, and one-click-upsell conversion optimization
- `/sales-membership` — Course and membership structure, pricing, and retention
- `/sales-affiliate-program` — Designing and running an affiliate program (ClickFunnels has native Backpack)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync new signups into ClickFunnels and tag them (developer/automation)
**User says**: "From my app I want to create or update a contact in ClickFunnels 2.0 and tag them. What's the API call?"
**Skill does**: Walks the bootstrap (`GET /api/v2/teams` → workspaces), then shows `POST /api/v2/contacts/{id}/upsert` (upsert by email) on the workspace base URL with `Authorization: Bearer` + `User-Agent`, followed by `POST /api/v2/contacts/{id}/applied_tags` to tag (Recipe 1 in `references/platform-guide.md`). Notes the `id`-vs-`public_id` gotcha and that API access needs the Pro tier.
**Result**: User has a working upsert-and-tag flow on the correct base URL.

### Example 2: Fire fulfillment the instant an order is placed (developer)
**User says**: "I want a webhook when someone buys in ClickFunnels, not a polling job on orders."
**Skill does**: Shows registering a `POST /api/v2/workspaces/{id}/webhook_endpoints` subscribed to the order-created event, explains verifying the webhook **signature**, and responding `2xx` fast + deduping on the event id (Recipe 2). Contrasts with polling `/orders`, which burns rate limit.
**Result**: User has a signed, event-driven webhook.

### Example 3: My ClickFunnels bill is climbing as my list grows
**User says**: "Why does ClickFunnels keep getting more expensive every month?"
**Skill does**: Explains the per-send email pricing model (cost scales with sends, not a flat rate) and the plan ladder (Startup ~$97 → Pro ~$297 + API/Backpack). Recommends segmenting to send less and pruning unengaged contacts. If they're weighing vendors, routes: "To compare builders — run: `/sales-funnel ClickFunnels vs alternatives for a large list`."
**Result**: User understands the cost driver and has levers to control it.

## Troubleshooting

### API returns 401 / "I can't find where to get a token"
**Symptom**: Requests fail to authenticate, or there's no obvious API-key screen.
**Cause**: Token not generated, missing `User-Agent` header, wrong base URL, or the account's plan doesn't include API access.
**Solution**: Generate a token under Team Settings → Developer Portal → Add new platform application (per-team). Send both `Authorization: Bearer {token}` and a `User-Agent` header. Use `accounts.myclickfunnels.com/api/v2` for team/workspace lookups and `{workspace}.myclickfunnels.com/api/v2` for workspace data. Confirm the plan includes API (Pro/Scale+).

### A create/update call returns 422
**Symptom**: POST/PATCH rejects the payload.
**Cause**: Using the `public_id` from a URL where the API expects the internal `id`, invalid PML on a page (returns 400), or a workspace-scoped resource hit on the wrong base URL.
**Solution**: Use `id` (not `public_id`) in payload bodies; validate PML markup for page calls; ensure workspace resources go to the `{workspace}` subdomain. Use `expand[]` to confirm related-resource ids.

### Classic → 2.0 migration broke something
**Symptom**: Funnels/automations behave differently or break after moving to 2.0.
**Cause**: 2.0 is a rebuilt platform — funnels, email, and automations don't transfer 1:1, and per-send email pricing differs from Classic.
**Solution**: Rebuild and test in a staging workspace before cutover; recreate automations as Workflows; recalculate email cost under the per-send model; keep Classic live until 2.0 is verified. Never cut over mid-launch.
