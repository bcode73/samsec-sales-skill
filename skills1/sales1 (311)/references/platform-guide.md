# Linked Helper Platform Reference

<!-- Source: https://www.linkedhelper.com (homepage, pricing, support.linkedhelper.com webhook docs), research 2026-06-28 -->

## Overview

Linked Helper (Linked Helper 2) is a standalone **desktop** LinkedIn automation app (Windows/macOS/Linux) that runs inside its own bundled browser — **not** a Chrome extension and **not** cloud-hosted. It auto-executes LinkedIn actions (connect, message, InMail, endorse, follow, scrape) inside drip-style campaigns called "funnels," with a built-in mini-CRM, an email finder, native CRM connectors, and outbound webhooks. ~9 years in market, 300k+ users. Primary audience: B2B sellers, recruiters, lead-gen/solopreneurs who want a cheap, power-user LinkedIn automation tool and don't mind running a desktop app.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| Campaigns / funnels | Multi-step action chains (connect → wait → message → follow-up), spintax + variables, smart reply detection pauses on reply | UI-built; triggers webhooks via action steps |
| Connection requests | Auto-invite 2nd/3rd degree, with notes + follow-ups, invite management (accept/cancel/withdraw) | UI / campaign action |
| Messaging & InMail | Sequenced messages, InMail to out-of-network, image personalization (dynamic images) | UI / campaign action |
| Profile scraping ("Visit and extract") | Pulls full profile + company data; extracting to webhook does **not** count toward daily action limit | Webhook-accessible |
| Email finder | Up to ~95% verified email discovery, metered by **data credits** | UI; results exportable |
| Built-in CRM | Tags, notes, lists, message history, reply detection | UI; exportable to webhook/CRM/CSV |
| Native CRM sync | HubSpot, Salesforce, Pipedrive, Zoho CRM/Recruit, ActiveCampaign, Instantly, Streak, Close, Capsule, HighLevel | Native connector (in-app OAuth/token) |
| Webhooks (outbound) | "Send person to webhook", "Send replied to Webhook", "Send organization to webhook" campaign actions POST JSON to any URL | Webhook-out (no inbound API) |
| iPaaS | Zapier, Make (Integromat), Pabbly, automatic.ai via custom webhook | Webhook-out |
| Engagement | Auto like/comment, "boost post" tagging, event/group invites, skill endorsements | UI / campaign action |
| Workspace | Team collaboration / multi-account management | Paid; one license per LinkedIn account |

**Key fact:** There is **no public inbound REST API** — you do not POST leads into Linked Helper. Data flows *out* of campaigns via webhooks and native connectors. Inbound automation (importing a list) is done via CSV upload or LinkedIn search URLs inside the app.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify against the live pricing page.*

| Plan | Price (monthly / annual-effective) | Daily limits | Data credits | Webhooks |
|---|---|---|---|---|
| **Trial** | Free, 14 days | Full feature access | — | Full |
| **Standard** | $15/mo ($8.25/mo on annual) | 20 advanced actions/day, 20 messages/day, **20 webhook profiles/day** | 620/mo | Limited (20 profiles/day) |
| **Pro** | $45/mo ($24.75/mo on annual) | **Unlimited** actions/messages | 3,100/mo | **Unlimited** |

- "Advanced actions" (the capped ones on Standard) include things like profile visits/scrapes beyond core limits; core lead-gen actions are described as unlimited but real throughput is bounded by LinkedIn-safe daily caps regardless of plan.
- **One license = one LinkedIn account** running simultaneously. Multiple accounts need multiple licenses/seats.
- Data credits power email-finder/enrichment lookups; they reset monthly and don't roll over.
- Webhook delivery of *replied* profiles and *visit-and-extract* results does not consume daily **action** limits but Standard still caps **webhook profiles/day** at 20.

## Integrations

- **Data-flow direction:** Linked Helper is a **source**. It writes scraped profiles, company data, and messaging history *out* to CRMs and webhooks. It reads its prospect lists *in* from LinkedIn search/Sales Navigator URLs and CSV uploads (not from an API).
- **Native CRM connectors** (bidirectional-ish for contacts/notes; primarily push): HubSpot, Salesforce, Pipedrive, Zoho CRM & Recruit, ActiveCampaign, Instantly, Streak, Close, Capsule, HighLevel. Setup is in-app (browser redirect + approval, or pasting a CRM personal API token, e.g. Pipedrive).
- **iPaaS:** Zapier (catch-hook), Make/Integromat (custom webhook), Pabbly, automatic.ai. Use these when there's no native connector for your destination (e.g. Google Sheets, ActiveCampaign via Zapier, Salesforce via Zapier).
- **Dedupe guidance:** Always include LinkedIn IDs (member_id / profile_url) in the mapping so the destination dedupes on a stable key — name/email-only matching creates duplicates.

## Data model

Linked Helper's webhook/CSV export is a **flat record per profile** with ~100+ columns. Key fields (verbatim header names) and a representative JSON shape:

```json
{
  "id": "12345",
  "lh_id": "abc123",
  "member_id": "<linkedin-member-id>",          // LinkedIn member id — use for CRM dedupe
  "public_id": "jane-doe-1234",
  "profile_url": "https://www.linkedin.com/in/jane-doe-1234/",
  "email": "jane@example.com",
  "full_name": "Jane Doe",
  "first_name": "Jane",
  "last_name": "Doe",
  "custom_first_name": "Jane",       // editable in LH CRM, overrides scraped value
  "headline": "VP Engineering at Acme",
  "location_name": "San Francisco Bay Area",
  "industry": "Software",
  "summary": "...",
  "current_company": "Acme",
  "current_company_position": "VP Engineering",
  "organization_1": "Acme",
  "organization_url_1": "https://www.linkedin.com/company/acme/",
  "organization_title_1": "VP Engineering",
  "organization_start_1": "2021-03",
  "organization_end_1": "",
  "badges_premium": "true",
  "badges_open_link": "false"
}
```
<!-- Constructed from documented webhook column headers — verify against live export. Full header list (id, public_id, hash_id, member_id, sn_member_id, sn_hash_id, r_member_id, t_hash_id, lh_id, profile_url, email, full_name, first_name, last_name, original_first_name, original_last_name, custom_first_name, custom_last_name, avatar, headline, location_name, industry, summary, address, birthday, badges_*, current_company*, organization_1..N with id/url/title/start/end/description/location/website/domain) is in linkedhelper-api-reference.md. -->

- The number of **Educations, Messengers, Positions, Phone numbers, Websites, Languages, and messaging-history** columns is configurable in the "Send person to webhook" action.
- Since app version **1.11.1**, the webhook can also send the **last message**, **last reply**, and **full/campaign messaging history** for a profile.
- "Send organization to webhook" sends a company-shaped record; "Send replied to Webhook" fires when a lead replies and includes emails + messaging history.

## Quick-start recipes

### Recipe 1 — Push replied leads (with email + history) to a CRM
**Trigger:** a lead replies inside a Linked Helper campaign.
**Steps:** Add a **"Send replied to Webhook"** step to the funnel → paste a Zapier/Make catch-hook URL → map fields → create/update CRM contact.

cURL (simulate what Linked Helper POSTs to your endpoint, to test your receiver):
```bash
curl -X POST "https://hooks.zapier.com/hooks/catch/XXXXX/yyyyy/" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_url": "https://www.linkedin.com/in/jane-doe-1234/",
    "member_id": "<linkedin-member-id>",
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "headline": "VP Engineering at Acme",
    "last_reply": "Sure, send me details.",
    "last_message": "Hi Jane, would a quick chat make sense?"
  }'
```

Python receiver (Flask) that dedupes on the LinkedIn member id:
```python
from flask import Flask, request
app = Flask(__name__)

@app.post("/lh-webhook")
def lh_webhook():
    p = request.get_json(force=True)
    key = p.get("member_id") or p.get("profile_url")   # stable dedupe key
    upsert_crm_contact(
        external_id=key,
        email=p.get("email"),
        first_name=p.get("first_name"),
        last_name=p.get("last_name"),
        linkedin_url=p.get("profile_url"),
        last_reply=p.get("last_reply"),
    )
    return "", 200
```
**Gotcha:** Linked Helper webhooks are **fire-and-forget POSTs with no HMAC signature** — validate with a secret path/query token and treat every delivery as untrusted. Standard plan caps webhook profiles at 20/day.

### Recipe 2 — Scrape a Sales Navigator search into Google Sheets
**Trigger:** you have a Sales Navigator search URL.
**Steps:** In Linked Helper, create a campaign from the search URL → add **"Visit and extract"** → add **"Send person to webhook"** pointing at a Zapier catch-hook → Zapier "Create Spreadsheet Row" in Google Sheets. Extracting to webhook after "Visit and extract" does **not** consume daily action limits.

### Recipe 3 — Native HubSpot sync with dedupe
**Trigger:** you want scraped + replied contacts in HubSpot without Zapier.
**Steps:** Settings → Integrations → HubSpot → authorize via browser redirect → enable "include LinkedIn IDs" and map `member_id`/`profile_url` to a HubSpot custom property → choose whether to transfer message history (visible in HubSpot's recent communications). Create custom fields in HubSpot for data with no native slot (e.g. LinkedIn skills).

## Integration patterns

- **CRM sync architecture:** Push model. Map `member_id`/`profile_url` to a unique CRM key for dedupe; create custom CRM properties for un-mapped LinkedIn fields (skills, organizations 2..N). Decide up front whether to transfer messaging history (heavier payload, but useful context).
- **Webhook listener pattern:** Linked Helper POSTs JSON; there's **no signature and no delivery log/retry dashboard** in the app. Put a queue or iPaaS (Zapier/Make) in front, return 200 fast, validate via a secret token in the URL, and de-dup on `member_id`. If your endpoint is down, the delivery is lost — Linked Helper won't retry.
- **Batch/export pattern:** For one-off pulls, export the LH CRM list to CSV instead of webhooks (no per-day webhook-profile cap, but still bounded by data credits for enrichment).
- **Scale/safety pattern:** One license per LinkedIn account, one geo-matched proxy per account, conservative daily limits, slow ramp on new accounts. To remove the "computer must stay on" constraint, run the desktop app on an always-on VPS / dedicated cloud machine.
