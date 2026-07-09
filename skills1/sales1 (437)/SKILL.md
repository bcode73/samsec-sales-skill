---
name: sales-productlane
description: "Productlane platform help — AI-native customer support + product-feedback suite built exclusively on Linear: omnichannel support inbox, AI Agent, self-updating help center, feedback portal, public roadmap, and a changelog that auto-drafts release notes from completed Linear issues. A Canny/Cycle/Productboard alternative for teams that run engineering in Linear. Developer surface: a documented REST API (productlane.com/api/v1, Bearer) for Companies, Customers, Insights, and Portal (projects/upvotes/changelogs + a public no-auth feedback endpoint); a Zapier Create-Note action; no MCP server. Use when pushing feedback in via the API, turning feedback into Linear issues, building a roadmap/changelog from Linear, embedding the widget, picking a plan (Starter $15 / Pro $29 / Scale $79 per user), judging the hard Linear requirement, or choosing Productlane vs Canny/Cycle/Frill. Do NOT use for VoC survey strategy (use /sales-customer-feedback) or public review generation (use /sales-customer-reviews)."
argument-hint: "[describe what you need help with in Productlane]"
license: MIT
version: 1.0.0
tags: [sales, customer-feedback, product, platform]
github: "https://github.com/productlane"
---

# Productlane Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Get feedback **into** Productlane programmatically — push **Insights/Notes** (`POST /api/v1/insights`, auth) or public widget **feedback** (`POST /api/v1/feedback`, **no auth**) tied to a customer/project
   - B) **Read** data out via the REST API — Companies, Customers, Insights, or Portal **projects / upvotes / changelogs** (`productlane.com/api/v1`, `Authorization: Bearer`)
   - C) Build the **feedback portal + public roadmap + changelog** — note these are **driven by Linear** (projects = Linear projects; changelog auto-drafts from completed Linear issues)
   - D) Configure the **support inbox** (email, live chat, Slack Connect, MS Teams, Discord), the **AI Agent**, or the self-updating **help center** (Pro+)
   - E) Decide whether Productlane fits — it is **built exclusively on Linear**; if the team doesn't run engineering in Linear, this is the wrong tool
   - F) Pick a plan (Starter $15 / Pro $29 / Scale $79 per user/mo annual) or compare Productlane vs Canny/Cycle/Frill/Productboard

2. **Do you use Linear?** This is the gating question. Productlane is not a standalone board — Linear is the single source of truth for issues, roadmap, and changelog. No Linear → recommend a standalone board (`/sales-frill`, `/sales-userjot`, or Canny-class tools) instead.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Voice-of-customer / NPS/CSAT/CES survey **program** strategy across tools | `/sales-customer-feedback {question}` |
| Choosing a feedback-board tool across the whole market (incl. non-Linear) | `/sales-customer-feedback {question}` |
| Aggregating **unsolicited** feedback across reviews/social/support | `/sales-noisely {question}` |
| Public review **generation** strategy (Trustpilot/G2) | `/sales-customer-reviews {question}` |
| In-app message / onboarding survey **strategy** across tools | `/sales-in-app-messaging {question}` |
| Connecting Productlane to another tool generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-customer-feedback choose a Linear-native feedback tool`".

## Step 3 — Productlane platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (omnichannel inbox, AI Agent, help center, feedback portal, roadmap, changelog/Release Intelligence) tagged API-/webhook-/UI-only, the Linear-dependency model, pricing tiers + plan gates (Starter/Pro/Scale), the data model (Companies, Customers, Segments, Insights, Portal projects/changelogs), and quick-start recipes (push an insight via the API; submit public feedback from a widget; pull the public changelog).

**Read `references/productlane-api-reference.md`** for the developer surface — base URL `https://productlane.com/api/v1`, `Authorization: Bearer API_KEY` (key from `productlane.com/settings/api`), the full endpoint inventory (Companies, Customers, Insights, Portal, Workspaces), which endpoints need auth vs are public (`POST /feedback` is public), and a **Gaps** section noting webhook/rate-limit details to confirm in-account.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Linear is mandatory, not optional.** Productlane is *built on* Linear — feedback links to Linear issues, the roadmap mirrors Linear projects, and the changelog auto-drafts from completed Linear issues. If the team doesn't use Linear (or plans to leave it), Productlane is the wrong choice — point them to a standalone board via `/sales-customer-feedback`. This is the single biggest fit question.
- **It HAS a real, documented REST API** (unlike Rapidr/Quickhunt/FeedBear). Base `productlane.com/api/v1`, Bearer auth. You can `GET`/create Companies & Customers, create/update **Insights** (feedback notes), and read **Portal** projects/upvotes/changelogs. Build against the API, not just no-code.
- **Two different "feedback" entry points.** `POST /api/v1/feedback` is **public (no auth)** — for widgets/portals capturing raw feedback. `POST /api/v1/insights` **requires auth** — for pushing structured feedback (text + `painLevel` + customer) from your backend/Zapier. Pick the right one for the trust boundary.
- **`painLevel` is a first-class field.** Insights/feedback carry `UNKNOWN | LOW | MEDIUM | HIGH` — use it to prioritize, since Productlane's whole pitch is routing feedback to engineering. Set it deliberately rather than defaulting to `UNKNOWN`.
- **No MCP server.** Unlike UserJot/Sleekplan/Four-Four, there's no Productlane MCP server — an AI agent integrates via the REST API (or Zapier's Create-Note action), not MCP.
- **It's a support + feedback suite, not just a board.** Pro+ adds a full omnichannel **support inbox** (email/live chat/Slack Connect/Teams/Discord) and an **AI Agent** — closer to Intercom + Canny than to a pure voting board. If they only need a board, a cheaper single-purpose tool may fit; if they want support + feedback + changelog unified on Linear, that's the draw.
- **Mind the plan gates.** Public roadmap/changelog/feedback portal are **Starter**; the support inbox + AI Changelog generation are **Pro**; SSO (JWT), custom domains, white-labeling, private portals, and HubSpot/Zapier are **Scale**. Pricing is per-user — model seat count before quoting.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — modules/pricing/API captured from productlane.com, its docs, and the ReadMe-hosted API reference on this date. Re-verify plan gates, the API surface, and webhook details against current docs/in-account before relying on them.*

1. **Hard Linear dependency.** Productlane is built exclusively on Linear — there's no standalone mode. If the user doesn't run engineering in Linear, this tool does not fit, full stop. Don't recommend it as a generic Canny replacement without confirming Linear usage.
2. **Per-user pricing, and the entry price is high for tiny teams.** Starter is ~$15/user/mo (annual) / ~$19 monthly — a reviewer noted the lowest tier is steep for small product teams, and there is **no permanent free plan** (7-day trial only). Multiply by seats before quoting.
3. **Portal Google/SSO auth is plan-gated.** A reviewer reported the low tier didn't include Google auth on the portal; **SSO (JWT)** and private portals are **Scale-tier**. Confirm which auth the customer's plan unlocks before promising gated portal access.
4. **`POST /api/v1/feedback` takes no auth — protect it.** The public feedback endpoint accepts `workspaceId` + `text` + `painLevel` + `email` with no API key, so a leaked `workspaceId` invites spam. Put a CAPTCHA / rate limit / origin check in front of any widget that calls it.
5. **Webhooks aren't clearly documented publicly.** Productlane's own outbound-webhook surface isn't in the public docs (Linear's webhooks are separate). If you need event push, confirm what Productlane emits in-account — don't assume HMAC-signed webhooks exist; consider Zapier or polling the API as a fallback.
6. **No MCP server.** There's no Productlane MCP server — agent integrations go through the REST API or Zapier, not MCP. Don't promise an MCP setup.
7. **AI features are newer.** The AI Agent / AI Changelog generation are recent and reviewers note limited track record — verify behavior on the actual account rather than assuming maturity.

## Related skills

- `/sales-customer-feedback` — Voice-of-customer / survey-program strategy across tools (Productlane is one Linear-native feedback option) — program design, metric choice, board-tool selection. Install: `npx skills add sales-skills/sales --skill sales-customer-feedback -a claude-code`
- `/sales-frill` — Affordable **standalone** feedback board with a documented REST API + HMAC-SHA256-signed webhooks (~$25/mo) — the pick when the team is **not** on Linear and wants a self-contained board + API. Install: `npx skills add sales-skills/sales --skill sales-frill -a claude-code`
- `/sales-userjot` — AI-first feedback board with a REST API **+ MCP server** and no per-seat pricing — the contrast when you want an MCP-driven agent loop and don't want per-user billing. Install: `npx skills add sales-skills/sales --skill sales-userjot -a claude-code`
- `/sales-sleekplan` — AI feedback suite (auto-categorization + **MCP server**) with a REST API + JWT SSO and a free Indie tier — contrast for AI triage plus an API without the Linear requirement. Install: `npx skills add sales-skills/sales --skill sales-sleekplan -a claude-code`
- `/sales-featureos` — FeatureOS (formerly Hellonext) feedback boards + roadmap + changelog + knowledge base; REST API v3, OAuth apps, webhooks — a standalone suite when Linear isn't the hub. Install: `npx skills add sales-skills/sales --skill sales-featureos -a claude-code`
- `/sales-quickhunt` — Affordable all-in-one board with a free lifetime tier (API Premium-only) — the budget/free-start contrast to Productlane's per-seat support+feedback suite. Install: `npx skills add sales-skills/sales --skill sales-quickhunt -a claude-code`
- `/sales-fourfour` — AI voice-of-customer copilot (OData API + MCP server) that mines existing conversations rather than soliciting board feedback — pair when you have rich call/ticket data. Install: `npx skills add sales-skills/sales --skill sales-fourfour -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "Push feedback from our app into Productlane via the API" (developer/automation)
**User says**: "When a user submits feedback in our product I want it to land in Productlane, tagged to their email and prioritized. We have a backend service."
**Skill does**: Confirms Productlane ships a **documented REST API** (`productlane.com/api/v1`, `Authorization: Bearer API_KEY` from `productlane.com/settings/api`). Recommends `POST /api/v1/insights` from the backend (auth'd) with `text`, `painLevel` (`UNKNOWN|LOW|MEDIUM|HIGH`), `customerEmail` (+ optional `customerName`, `projectId`) so each item is a structured, prioritized note tied to the customer — and contrasts the **public, no-auth** `POST /api/v1/feedback` (workspaceId+text+painLevel+email) for an in-browser widget where you don't want to expose the key. Notes the insight links through to Linear, and to protect the public endpoint with a CAPTCHA/rate limit.
**Result**: A working, auth-correct intake path with the right endpoint for the trust boundary.

### Example 2: "Is Productlane the right feedback tool for us?" (fit / selection)
**User says**: "We're a small SaaS picking a feedback + roadmap + changelog tool. Considering Productlane, Canny, and Frill."
**Skill does**: Leads with the gating question — **do you use Linear?** Productlane is built *exclusively* on Linear (roadmap = Linear projects, changelog auto-drafts from completed Linear issues), so it's only a fit if engineering runs in Linear; otherwise Canny/Frill/UserJot are better. Frames the rest: Productlane bundles a full **support inbox + AI Agent** (Intercom-ish) and has a **real REST API** but **no MCP server** and **no free tier** (Starter ~$15/user, Pro ~$29, Scale ~$79, per-user); Frill is a cheaper standalone board (~$25/mo) with a documented API + signed webhooks; Canny is the pricier incumbent. Routes broader selection: "run: `/sales-customer-feedback choose a feedback board for a Linear team`".
**Result**: A Linear-gated, price- and API-grounded recommendation.

### Example 3: "Build our public changelog and roadmap from Linear" (workflow)
**User says**: "We ship in Linear and want a public roadmap and a changelog without writing release notes by hand."
**Skill does**: Explains Productlane's **Release Intelligence** auto-drafts changelog entries from **completed Linear issues/projects** — it pulls the relevant issues, categorizes them by label, and writes a draft you edit and publish (AI Changelog generation is **Pro+**). The **public roadmap** mirrors Linear projects, and customers can submit + upvote requests in the **feedback portal** that stay in sync with Linear. For programmatic reads, points to `GET /api/v1/portal` endpoints (`getprojects`, `getprojectupvotes`, `listchangelogs`). Flags that custom domain + white-label + private portal are **Scale-tier**.
**Result**: A Linear-driven roadmap/changelog plan with the right plan gates and API reads called out.

## Troubleshooting

### We don't use Linear — can we still use Productlane?
**Symptom**: You want Productlane's portal/changelog but your team isn't on Linear.
**Cause**: Productlane is **built exclusively on Linear** — issues, roadmap, and changelog all derive from Linear. There is no standalone mode.
**Solution**: If adopting Linear isn't on the table, pick a standalone board instead — `/sales-frill` or `/sales-userjot` (both ship documented APIs), `/sales-featureos`, or `/sales-quickhunt` (free tier). Use `/sales-customer-feedback` to choose. Only stay with Productlane if engineering will run in Linear.

### I can't authenticate to the API / which endpoints need a key?
**Symptom**: Calls return 401, or you're unsure whether an endpoint needs auth.
**Cause**: Most endpoints require `Authorization: Bearer API_KEY` (key generated at `productlane.com/settings/api`), but `POST /api/v1/feedback` is **public (no auth)** by design for widgets.
**Solution**: For server-side reads/writes (Companies, Customers, Insights, Portal) send the Bearer key. For in-browser public feedback capture, use `POST /api/v1/feedback` with `workspaceId`+`text`+`painLevel`+`email` and **don't** ship your API key to the client — protect that endpoint with a CAPTCHA/rate limit instead. Re-verify the base URL and any rate limits in-account.

### Pricing feels high / there's no free plan
**Symptom**: "Starter looks expensive for our small team," or "where's the free tier?"
**Cause**: Productlane is **per-user** (~$15 Starter / $29 Pro / $79 Scale per user/mo annual; higher monthly) with **no permanent free plan** — only a 7-day trial. Portal SSO/private portals and HubSpot/Zapier are Scale-tier.
**Solution**: Model the real seat count and the tier that unlocks the features you need (support inbox + AI changelog = Pro; SSO/custom domain/white-label = Scale). Ask about **startup discounts** (offered to early-stage companies). If budget or a free start is the priority, contrast `/sales-quickhunt` (free lifetime tier) or `/sales-frill` (~$25/mo). Treat all pricing as best-effort and confirm on productlane.com/pricing.
