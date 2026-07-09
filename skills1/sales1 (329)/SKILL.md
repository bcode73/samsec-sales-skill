---
name: sales-marketing-mary
description: "Marketing Mary (marketingmary.ai) platform help — an AI marketing co-pilot whose standout feature is interactive buyer personas you converse with, built from your real CRM, analytics, email, and ad data, not a one-line prompt: chat with a persona to pressure-test subject lines, objections, and messaging before launch, map ~10-stakeholder B2B buying committees, and auto-update personas as new data flows in. Subscription (Starter/Growth/Agency), UK/EU/GDPR-hosted, waitlist-stage; native HubSpot/Salesforce/GA4 connectors but no public developer API or MCP server. Use when building or talking to an interactive persona in Marketing Mary, grounding personas in real customer data instead of a prompt, testing messaging against a synthetic buyer, mapping a B2B buying committee, or connecting it to HubSpot or Salesforce. Do NOT use for comparing persona/idea tools across the market (use /sales-idea-validation), or prompt-only persona generators (use /sales-personadeck or /sales-instantpersonas)."
argument-hint: "[describe what you need help with in Marketing Mary]"
license: MIT
version: 1.0.0
tags: [sales, pre-launch, platform]
---

# Marketing Mary Platform Help

Marketing Mary (marketingmary.ai) is an **AI marketing co-pilot** for B2B marketing teams whose
standout module is **interactive buyer personas** — synthetic personas built from your **real customer
data** (CRM, Google Analytics 4, email platform, ad accounts) that you **converse with** to test
subject lines, probe objections, and validate messaging *before* a campaign ships. Beyond personas it
runs a research → strategise → create → publish → measure → maintain loop and can **publish to HubSpot
or WordPress**. It maps **B2B buying committees** (~10 stakeholders across IT/ops/finance/end-users) and
**auto-updates** personas as new behavioral data flows in.

Its differentiator vs the prompt-only persona generators (InstantPersonas, PersonaGen, Personadeck) is
that personas are **grounded in your live data and conversational**, not generated from a one-line
description. It's a **subscription** (Starter/Growth/Agency), **UK/EU-based with GDPR built in**, and
**currently waitlist-stage** — treat all features/pricing as best-effort and unconfirmed.

*Note: as of research the product is in waitlist/pre-release, so details below are best-effort from the
live site and third-party sources — verify at marketingmary.ai. There is **no public developer API, no
webhooks, and no developer MCP server** (the "MCP Integration Addendum" in the footer is a legal
data-processing document, not a Marketing Mary MCP server).*

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from Marketing Mary?**
   - A) Build an interactive persona from your real customer data
   - B) *Talk to* a persona to test subject lines / objections / messaging before a campaign
   - C) Map a B2B buying committee (multi-stakeholder targeting)
   - D) Connect it to HubSpot / Salesforce / GA4, or publish content
   - E) Understand the Starter/Growth/Agency tiers (or the waitlist)
   - F) Automate or export personas programmatically (API question)
2. **What data can you connect?** Personas are only as good as the CRM/analytics/email/ad data behind
   them — a thin or low-traffic account yields a thin persona.

Skip-ahead: if the user wants the validate-before-building *method* or to compare persona/idea tools
across the market, that's a `/sales-idea-validation` question — route in Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or comparing persona/idea tools across the market | `/sales-idea-validation {question}` |
| A prompt-only persona generator (persona from a short description, no live data) | `/sales-personadeck` or `/sales-instantpersonas` or `/sales-personagen` `{question}` |
| Turning persona insights into a content plan across tools | `/sales-content {question}` |
| Deeper HubSpot-side setup (the CMS/CRM it publishes to) | `/sales-hubspot {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer Marketing Mary-specific questions using Step 3.

## Step 3 — Marketing Mary platform reference

**Read `references/platform-guide.md`** for the full reference — the persona-creation phases and required
data sources, how the interactive/conversational persona works, buying-committee mapping, the
research→publish co-pilot modules with their API/webhook/UI-only tags, the Starter/Growth/Agency tiers
and best-effort GBP pricing, the integration/connector surface (HubSpot/Salesforce/GA4 — bidirectional
vs read-only), and the no-public-API automation reality with an LLM-API + HubSpot-API workaround.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **A persona you converse with is a model of your DATA, not a real customer — say so every time.**
  Whatever the user asks, make clear that "talking to" a Marketing Mary persona (testing a subject
  line, probing objections) is a **synthetic simulation of your existing data**, so it's **directional
  input, not validated demand**. It can sound convincing and still be wrong. **Keep the objections and
  angles the conversation surfaces — that's its real value** — but prescribe confirming the go/no-go with
  **real behavior** — a smoke-test click, a reply, an A/B send, a pre-sale — and route the real test to
  `/sales-idea-validation` / `/sales-audience-growth`.
- **Ground the persona in real data — output tracks the data you connect.** Its edge over prompt-only
  generators is that personas are built from CRM/GA4/email/ad data, so tell the user a **thin or
  low-traffic account yields a thin persona**; connect real sources first, and note personas
  **auto-update** as new data flows in (they're not a one-time doc).
- **For a B2B buying committee, build the whole committee, not one persona.** Marketing Mary maps ~10
  stakeholders (IT, ops, finance, end-users) with interdependencies — advise mapping each role and
  **differentiating the message per stakeholder** rather than targeting a single blended buyer.
- **Present pricing as best-effort and waitlist-stage; point to the live pricing page.** Name the tiers
  — **Starter (~£99/mo, 1 user, 2 personas), Growth (~£299/mo, 3 users, 10 personas), Agency (~£999/mo,
  unlimited users/personas, multi-client + white-label)** — but say the product is **pre-release**, so
  confirm current tiers, seat/persona caps, and which integrations are plan-gated at marketingmary.ai
  before relying on any figure.
- **There is no public developer API or MCP server — don't plan an integration around one.** If asked to
  automate, export, or batch personas, state plainly there's **no documented public API, no webhooks,
  and no developer MCP server** (the footer's "MCP Integration Addendum" is a **legal/data-processing
  doc**, not an MCP server you can call), and note it's **pre-release/waitlist-stage so there's no
  supported export endpoint today**. It's a UI tool with **native connectors** (HubSpot, Salesforce,
  GA4, email, ads). Workarounds: read/write the synced data through the **HubSpot/Salesforce API**, or
  generate personas programmatically by calling an **LLM API** directly (see `references/platform-guide.md`).
- **It's a co-pilot, not just personas — but publishing to HubSpot/WordPress isn't demand either.** The
  research/create/publish/measure loop speeds execution; a *published* campaign informed by a persona is
  still not evidence anyone will buy. Keep the go/no-go on real behavior.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — the product is in waitlist/pre-release, so features, tiers, GBP
pricing, and the connector list are unconfirmed and move; verify at marketingmary.ai.*

- **"Talking to a persona" feels like validation but isn't.** The persona is a synthetic model of your
  existing data — pressure-testing a subject line against it is a directional gut check, not a stranger
  taking an action. Confirm with a real demand test.
- **Persona quality tracks the data you connect.** A low-traffic or sparse CRM/GA4 account produces a
  generic persona (competitors like Delve AI effectively need thousands of monthly sessions). Connect
  real, rich sources first.
- **It's waitlist-stage.** Pricing, seat/persona caps, and which integrations exist may differ from any
  marketing copy — confirm live before committing.
- **No public API / webhooks / developer MCP server.** Don't build a pipeline around it; the "MCP
  Integration Addendum" is a legal document, not a callable server. Automate via the HubSpot/Salesforce
  API on the synced data, or an LLM API for persona text.
- **Personas auto-update.** Unlike a static PDF persona, these change as data flows in — a message you
  validated last quarter may map to a shifted persona; re-check before reusing.
- **B2B committee ≠ single buyer.** Targeting one persona in a ~10-stakeholder committee misses the
  approvers/blockers — map and message the whole committee.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full persona/validator tool landscape (use this to actually decide build-or-not; a persona you talk to is not demand)
- `/sales-personadeck` — Personadeck platform help (a prompt-only persona generator — a styled persona card from a short description, User vs Negative type, PDF-only; UI-only/no API)
- `/sales-instantpersonas` — InstantPersonas / User Persona platform help (a prompt-only buyer/user-persona generator + website-perception "Insights" + competitor personas; UI-only/no API)
- `/sales-personagen` — PersonaGen platform help (a prompt-only persona generator — detailed personas + content-generation prompts, organized into projects; UI-only/no API)
- `/sales-hubspot` — HubSpot platform help (the CRM/CMS Marketing Mary syncs to and publishes into; use for HubSpot-side API/automation)
- `/sales-content` — Content-marketing strategy across tools (turn persona insights into a content plan)
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "Can I test my cold-email subject lines by talking to a persona?"
**User says**: "Marketing Mary lets me chat with a buyer persona — if it likes my subject line, is that a green light to send?"
**Skill does**: Explains that the persona is a **synthetic model built from your CRM/GA4/email data**, so
its reaction is a **directional gut check, not demand** — it can approve a line real recipients would
ignore. Recommends using the conversation to **surface objections and angles** (its real value), then
validating the winner with **real behavior** — an A/B send, reply rate, or a smoke-test click — and
points the real test to `/sales-idea-validation` and `/sales-audience-growth`. Notes personas
auto-update, so re-check before reusing an old winner.
**Result**: The founder mines the persona for angles but takes the go decision from real recipients.

### Example 2: Grounding personas in real data + mapping a committee
**User says**: "We sell to a buying committee. How do I get Marketing Mary to build something useful, not a generic persona?"
**Skill does**: Says persona quality **tracks the data connected** — wire up the real CRM, GA4, email,
and ad accounts first (a low-traffic account yields a thin persona), and let personas auto-update.
Explains Marketing Mary maps **~10-stakeholder B2B buying committees** (IT/ops/finance/end-users) and
advises **building the whole committee and differentiating the message per role** rather than one blended
buyer. Frames each persona as a hypothesis to confirm against real stakeholder conversations.
**Result**: A committee map with role-specific messaging, grounded in live data instead of a one-liner.

### Example 3: Automating persona export via API (developer/automation)
**User says**: "I want to pull our Marketing Mary personas into our data warehouse automatically — what's the API?"
**Skill does**: States plainly there's **no documented public API, no webhooks, and no developer MCP
server** (the footer's "MCP Integration Addendum" is a **legal data-processing doc**, not a callable
server), and that the product is **waitlist-stage** — so there's no supported export endpoint today.
Offers the real path: since personas are **bidirectionally synced with HubSpot/Salesforce**, read the
persona/contact data through the **HubSpot or Salesforce API** into the warehouse; and for programmatic
persona *generation*, call an **LLM API** directly (see `references/platform-guide.md` for a cURL/Python
sketch). Notes the thing worth automating is a real demand signal, not a synthetic persona.
**Result**: The user avoids building on a non-existent API and pipelines via the connected CRM instead.

## Troubleshooting

### "The persona agreed with my messaging — does that mean it'll work?"
**Symptom**: A Marketing Mary persona reacts positively to a subject line / pitch and the user reads it as validation.
**Cause**: The persona is a **synthetic simulation of your existing data**, not a real prospect — it
pattern-matches to plausible agreement and can be confidently wrong.
**Solution**: Keep the useful parts (objections surfaced, angles to try), discard the "verdict," and earn
a real one — an A/B send, reply/click data, or a pre-sale. Cross-check with a real demand test via
`/sales-idea-validation`.

### Persona feels generic despite connecting my data
**Symptom**: The generated persona is vague or could describe anyone, even after linking accounts.
**Cause**: The connected sources are **thin or low-traffic** — data-grounded personas need real volume
(analytics-connected tools broadly need thousands of monthly sessions to differentiate).
**Solution**: Connect richer, higher-volume sources (full CRM history, GA4 with real traffic, email
engagement, ad data), and let personas auto-update as data accumulates. Add more first-party signal
before trusting the profile.

### "Where's the API / how do I automate or export personas?"
**Symptom**: Looking for API docs, a webhook, or an MCP server to export or batch personas.
**Cause**: Marketing Mary has **no public API, no webhooks, and no developer MCP server** (the footer
"MCP Integration Addendum" is a legal doc), and it's pre-release.
**Solution**: Don't build a pipeline around it. Read the persona/contact data via the **HubSpot or
Salesforce API** it syncs to, or call an **LLM API** directly for programmatic persona generation (see
`references/platform-guide.md`). Automate the real demand signal instead — see `/sales-idea-validation`.
