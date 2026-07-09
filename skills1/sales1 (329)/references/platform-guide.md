# Marketing Mary Platform Reference

<!-- Best-effort from research (2026-07). Product is waitlist/pre-release — verify every detail at marketingmary.ai. -->

## Overview

Marketing Mary (marketingmary.ai) is an **AI marketing co-pilot** for B2B marketing teams (positioned at
UK/EU companies, ~50–500 employees). Its headline module is **Interactive Buyer Personas** — synthetic
personas built from your real customer data that you **converse with** to test messaging before a
campaign. Around personas it runs a full research → strategise → create → publish → measure → maintain
loop and publishes to HubSpot/WordPress. Differentiator: personas are **grounded in live CRM/analytics
data and conversational**, not generated from a one-line prompt. Subscription; UK/EU-based, GDPR built in.

## Capabilities & automation surface

For each module, whether a developer can automate it:

| Module | What it does | Automation surface |
|---|---|---|
| **Interactive Buyer Personas** | Personas built from CRM/GA4/email/ad data; chat with them to test subject lines, probe objections, validate angles, compare personas | **UI-only** (no persona API/export endpoint) |
| **Buying-committee mapping** | Maps ~10-stakeholder B2B committees (IT/ops/finance/end-users) + interdependencies; differentiated messaging per role | **UI-only** |
| **Auto-update** | Personas refresh as new behavioral data flows from connected sources | **UI-only** (driven by the native connectors) |
| **Research** | Autonomous market/audience/competitor analysis | **UI-only** |
| **Strategise** | Topic strategy + content calendar | **UI-only** |
| **Create** | Research-backed content with brand-voice preservation | **UI-only** |
| **Publish** | Push content to HubSpot or WordPress | Via **HubSpot/WordPress** (Marketing Mary drives it; no MM API) |
| **Measure** | Search + engagement signal monitoring | **UI-only** |
| **Maintain** | Automated content refresh + technical optimization | **UI-only** |
| **Native connectors** | Bidirectional sync with HubSpot & Salesforce; reads GA4, email, ad accounts | **CRM-side API** (automate via HubSpot/Salesforce, not MM) |

**Bottom line for developers:** there is **no public Marketing Mary API, no webhooks, and no developer
MCP server.** The "Model Context Protocol (MCP) Integration Addendum" referenced in the site footer is a
**legal/data-processing document** (governing how MM may connect to MCP-enabled tools you own), *not* a
Marketing Mary MCP server you can call. Anything programmatic must go through the **CRM it syncs to** or a
direct **LLM API**.

## Pricing, limits & plan gates

Best-effort (GBP), from the live pricing surface during a **waitlist/pre-release** phase — confirm before
relying on any figure:

| Tier | Price (best-effort) | Users | Personas | Notable gates |
|---|---|---|---|---|
| **Starter** | ~£99/mo | 1 | 2 | Core integrations |
| **Growth** ("Most Popular") | ~£299/mo | 3 | 10 | Full integrations |
| **Agency** | ~£999/mo | Unlimited | Unlimited | Multi-client dashboard, **white-label**, custom integrations |

- All tiers include AI persona generation, interactive conversations, and workflow integration.
- **Waitlist:** the product was pre-release at research (500+ reportedly on the waitlist) — tiers,
  seat/persona caps, and which integrations are plan-gated may all change at GA.
- "Replaces ~£15K agency persona studies" is **marketing framing**, not a like-for-like guarantee.

## Integrations

Focus on data-flow direction:

- **HubSpot** — native, **bidirectional** (Marketing Hub / Sales Hub / CMS Hub). Reads CRM/contact data;
  writes published content. The primary publish target.
- **Salesforce** — native, **bidirectional** (Sales Cloud / Pardot).
- **Google Analytics 4** — **read** (behavioral/traffic signal that feeds personas).
- **Email platforms** (e.g. Mailchimp, ActiveCampaign) — **read** engagement signal.
- **Ad accounts** (Google Ads, Meta Ads, LinkedIn Campaign Manager) — **read** performance history.
- **WordPress** — **write** (publish target).
- **No Zapier/Make required** (native connectors) — and, correspondingly, **no documented Zapier/Make
  triggers/actions or public API** to build custom flows on. "Under 2 hours to connect a ~12-tool stack"
  is the vendor's stated onboarding time.

## Data model

Marketing Mary does not publish an API schema. The following is a **representative** shape of an
interactive persona, constructed from the product description — use it to reason about what the persona
captures, not as a real API contract.

<!-- Constructed from product descriptions — NOT a real API. Verify against the product before relying on it. -->

```json
{
  "persona_id": "per_0KZ...",
  "name": "Operations Olivia",
  "type": "synthetic",
  "grounded_in": ["hubspot_crm", "ga4", "email_engagement", "ads"],
  "journey_stage": "evaluation",
  "committee_role": "economic_buyer",
  "attributes": {
    "goals": ["cut manual reporting time", "prove ROI to finance"],
    "objections": ["switching cost", "unclear onboarding effort"],
    "channels": ["LinkedIn", "peer communities", "vendor case studies"],
    "messaging_that_lands": ["time-to-value", "committee-level ROI"]
  },
  "buying_committee": [
    {"role": "champion", "function": "operations"},
    {"role": "economic_buyer", "function": "finance"},
    {"role": "technical_gatekeeper", "function": "IT"},
    {"role": "end_user", "function": "operations"}
  ],
  "last_updated": "auto"
}
```

A **conversation** with a persona (test a subject line, probe an objection) is a chat turn against this
synthetic model — its output is *simulated buyer reaction*, not a real response from a person.

## Quick-start recipes

Because there is **no Marketing Mary API**, the "automation" recipes route through the CRM it syncs to or
a direct LLM call.

### Recipe 1 — Pull persona-adjacent contact data into a warehouse (via HubSpot, not MM)

Marketing Mary personas are bidirectionally synced with HubSpot. To get the underlying data
programmatically, read it from HubSpot:

```bash
curl -s https://api.hubapi.com/crm/v3/objects/contacts?limit=100 \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json"
```

```python
import requests, os

def hubspot_contacts(after=None):
    params = {"limit": 100, "properties": "email,lifecyclestage,hs_persona"}
    if after:
        params["after"] = after
    r = requests.get(
        "https://api.hubapi.com/crm/v3/objects/contacts",
        headers={"Authorization": f"Bearer {os.environ['HUBSPOT_TOKEN']}"},
        params=params, timeout=30,
    )
    r.raise_for_status()
    return r.json()
```

Gotcha: this reads the **CRM data behind the persona**, not the Marketing Mary persona object itself
(which has no export endpoint). Map HubSpot's `hs_persona` / lifecycle fields to your schema.

### Recipe 2 — Generate a persona programmatically (LLM API, since MM has none)

If you need batch/automated persona *generation* and can't use the UI, call an LLM directly with your
first-party data:

```python
import anthropic, json

client = anthropic.Anthropic()
crm_summary = json.dumps({"top_segments": ["ops leaders, 50-500 emp"], "objections": ["switching cost"]})

msg = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1200,
    messages=[{
        "role": "user",
        "content": (
            "Build a B2B buying-committee persona set (champion, economic buyer, "
            "technical gatekeeper, end user) grounded ONLY in this real data. "
            "For each role: goals, objections, channels, messaging that lands. "
            f"Data: {crm_summary}"
        ),
    }],
)
print(msg.content[0].text)
```

Gotcha: an LLM-generated persona (or a Marketing Mary one) is a **hypothesis**, not demand — validate
against real customers.

### Recipe 3 — Test messaging, then validate for real

1. In Marketing Mary, chat with the persona to pressure-test 3–4 subject-line/objection variants → keep
   the angles it surfaces.
2. Run the winning variant as a **real** A/B send (via HubSpot/your ESP) or a smoke-test click.
3. Decide go/no-go on the **real** open/reply/click numbers, not the persona's reaction.

## Integration patterns

- **CRM sync architecture:** MM ↔ HubSpot/Salesforce is bidirectional — reads contact/behavioral data to
  build personas, writes published content back. To integrate elsewhere, treat **HubSpot/Salesforce as
  the system of record** and use their APIs; MM is not an integration hub you can call.
- **No webhook listeners:** MM emits no webhooks. If you need event-driven flows (e.g. "persona changed"),
  poll the CRM side or watch HubSpot workflow triggers instead — MM has no equivalent.
- **Waitlist caveat:** because the product is pre-release, any connector, tier, or field named here may
  change at GA — re-verify the live integration list before building.
