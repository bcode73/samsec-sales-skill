<!-- Source: https://support.linkedhelper.com/hc/en-us/sections/4407233782546-Integrations and webhook articles (360016687659 Send person to webhook, 9057995150482 Send replied to Webhook, 16685333860882 Send organization to webhook, 16713677664274 Data fields exported), plus the public "Linked Helper 2 Webhook column headers" Google Sheet. Captured 2026-06-28. The Zendesk support pages 403 to automated fetch; field lists below are reconstructed verbatim from the public column-header sheet and search-indexed snippets. -->

# Linked Helper 2 — Integration / Webhook Reference

## API status

**There is no public inbound REST API.** Per apitracker.io, Linked Helper publishes no developer docs, API reference, base endpoint, GraphQL endpoint, or documented auth method. You cannot POST leads or trigger campaigns over HTTP. The programmatic surface is:

1. **Outbound webhooks** fired by campaign action steps (this document's focus).
2. **Native CRM connectors** configured in-app.
3. **iPaaS** (Zapier, Make/Integromat, Pabbly, automatic.ai) consuming the outbound webhooks.

If you need an inbound API, Linked Helper is the wrong tool — it's a desktop automation app, not an API-first platform.

## Webhook actions (campaign steps)

You add a webhook step to a campaign ("funnel") and paste a destination URL in the **Webhook URL** field. Linked Helper then **HTTP POSTs** a JSON array/object of profile data to that URL when the step runs.

| Action step | Fires when | Payload |
|---|---|---|
| **Send person to webhook** | The profile reaches this step in the funnel | Full person record (fields below) |
| **Send replied to Webhook** (plug-in) | The lead **replies** to a message | Person record + emails + last message / last reply / messaging history |
| **Send organization to webhook** | Company record reaches this step | Company-shaped record |

Notes from the docs:
- "Linked Helper 2 sends an array of information to the URL inserted in the 'Webhook URL' field."
- Sending a contact to a webhook **after the "Visit and extract" action does not count toward daily limits** (the action itself does; the webhook delivery does not).
- The number of **Educations, Messengers, Positions, Phone numbers, Websites, Languages, and messaging-history** columns is adjustable in the "Send person to webhook" action.
- **Since application version 1.11.1**, the webhook can also send the **last message** and **last reply** from a specific profile, or the **full / campaign messaging history**.
- Successfully processed profiles are auto-tagged so you can filter/group them.
- There is **no documented HMAC signature, no delivery log, and no retry** — treat deliveries as untrusted and fire-and-forget. Validate with a secret token embedded in the Webhook URL path/query.

## Auth quick-start (testing your receiver)

Linked Helper authenticates to *your* endpoint only by the URL you paste (optionally with a token in the query string). To build and test a receiver, simulate the POST it sends:

```bash
curl -X POST "https://your-endpoint.example.com/lh-hook?token=YOUR_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_url": "https://www.linkedin.com/in/jane-doe-1234/",
    "member_id": "<linkedin-member-id>",
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "full_name": "Jane Doe",
    "headline": "VP Engineering at Acme",
    "current_company": "Acme",
    "current_company_position": "VP Engineering"
  }'
```

A minimal Flask receiver that returns 200 quickly and dedupes on the LinkedIn member id:

```python
from flask import Flask, request, abort
app = Flask(__name__)
SECRET = "YOUR_SECRET"

@app.post("/lh-hook")
def hook():
    if request.args.get("token") != SECRET:
        abort(401)
    p = request.get_json(force=True)
    # Linked Helper may send a single object or an array of objects
    rows = p if isinstance(p, list) else [p]
    for r in rows:
        key = r.get("member_id") or r.get("profile_url")  # stable dedupe key
        upsert_contact(external_id=key, **r)
    return "", 200   # return fast — no retry on your side
```

## Webhook / CSV field reference (verbatim column headers)

These are the column headers Linked Helper exports to a webhook, CRM, or CSV (from the public "Linked Helper 2 Webhook column headers" sheet). Organizations repeat as numbered groups (`organization_1` … `organization_N`); each org group has the same sub-fields.

### Identity / dedupe keys
```
id, public_id, hash_id, member_id, sn_member_id, sn_hash_id, r_member_id, t_hash_id, lh_id
```
- `member_id` — LinkedIn member id; the recommended stable key for CRM dedupe.
- `sn_member_id` / `sn_hash_id` — Sales Navigator identifiers.
- `lh_id` — Linked Helper's internal id.

### Core profile
```
profile_url, email, full_name, first_name, last_name,
original_first_name, original_last_name, custom_first_name, custom_last_name,
avatar, headline, location_name, industry, summary, address, birthday
```
- `custom_first_name` / `custom_last_name` — values you edit inside the LH CRM; they override the scraped `original_*` values for personalization tokens.

### Badges
```
badges_premium, badges_influencer, badges_job_seeker, badges_open_link
```

### Current company
```
current_company, current_company_custom,
current_company_position, current_company_custom_position
```

### Organizations (repeating group, `_1` … `_N`)
For each numbered organization (e.g. `organization_1`):
```
organization_1, organization_id_1, organization_url_1, organization_title_1,
organization_start_1, organization_end_1, organization_description_1,
organization_location_1, organization_website_1, organization_domain_1
```
The sheet documents at least organizations 1–7 with identical sub-field structure; the count of org/education/position/phone/website/language/messaging columns is configurable per action.

## Representative "person" webhook payload (constructed)

<!-- Constructed from the documented column headers — verify against a live delivery. -->
```json
{
  "id": "987654",
  "lh_id": "lh_ab12cd34",
  "member_id": "<linkedin-member-id>",
  "public_id": "jane-doe-1234",
  "profile_url": "https://www.linkedin.com/in/jane-doe-1234/",
  "email": "jane@example.com",
  "full_name": "Jane Doe",
  "first_name": "Jane",
  "last_name": "Doe",
  "custom_first_name": "Jane",
  "headline": "VP Engineering at Acme",
  "location_name": "San Francisco Bay Area",
  "industry": "Computer Software",
  "badges_premium": "true",
  "badges_open_link": "false",
  "current_company": "Acme",
  "current_company_position": "VP Engineering",
  "organization_1": "Acme",
  "organization_id_1": "1234567",
  "organization_url_1": "https://www.linkedin.com/company/acme/",
  "organization_title_1": "VP Engineering",
  "organization_start_1": "2021-03",
  "organization_end_1": "",
  "organization_domain_1": "acme.com",
  "last_message": "Hi Jane, would a quick chat make sense next week?",
  "last_reply": "Sure, send me a couple of times."
}
```

## Native CRM connector notes (verbatim-sourced)

- Native integrations: **HubSpot, Salesforce, Pipedrive, Zoho CRM & Recruit, ActiveCampaign, Instantly, Streak, Close, Capsule, HighLevel.**
- Setup: "synchronize two applications directly in the browser through redirect and approval of Linked Helper access." For **Pipedrive**, get the **Personal API token** from Pipedrive → *Personal Preferences* and paste it into Linked Helper.
- "Linked Helper automatically sends scraped profile data, company details, and full messaging history. You can choose whether to transfer message history" (per-account or per-company); the conversation appears in **recent communications** on the org profile in HubSpot.
- "It's recommended to **include LinkedIn IDs to avoid duplicate contacts** in the CRM."
- "In the settings, you can create additional **custom fields** to transfer data for which there are no sections in the CRM, for example, skills from the LinkedIn profile."

## Zapier / Make recipe (verbatim-sourced)

To send profiles to apps without a native connector (Google Sheets, ActiveCampaign, Salesforce, HubSpot, Pipedrive):
1. In Zapier create a **"Catch Hook"** trigger → copy the webhook URL.
2. In Linked Helper, add **"Send the person to webhook"** to the campaign workflow and paste that URL into the **Webhook URL** field.
3. Run one profile so Zapier captures a sample payload, then map the LH columns to your destination fields.
4. For **Make/Integromat**, use a **Custom webhook** module the same way.

## Pagination / rate limits / errors

- **Pagination:** N/A — there is no read API. Bulk reads are done by exporting the LH CRM list to **CSV** in-app, or by collecting webhook deliveries.
- **Rate limits:** governed by **LinkedIn-safe daily action limits** (configurable, plan-gated: Standard 20 advanced actions/day + 20 webhook profiles/day; Pro unlimited), **not** by an HTTP rate-limit header.
- **Errors / retries:** Linked Helper does not expose webhook delivery status, error codes, or retries. If your endpoint is down or returns non-2xx, the delivery is lost. Mitigate by placing a durable queue or iPaaS (Zapier/Make) in front of your own service.

## Gaps

- Exact JSON envelope (single object vs array) and content-type are not published; build your receiver to accept both `application/json` object and array bodies.
- Full education/position/phone/website/language/messaging sub-field names beyond the organization group were not individually enumerated in public sources — capture them from a live delivery.
- No webhook signing/secret mechanism is documented; rely on a secret token in the URL.
