# La Growth Machine — Learnings

Accumulated, dated platform knowledge. Append new findings with a date stamp so staleness is auditable.

---

**2026-06-27**: Research baseline. Built from the marketing site (lagrowthmachine.com), the API settings docs, and integration listings (Composio MCP toolkit, MindCloud, Make, n8n, Pipedream) referencing the public Postman collection.

- **Category:** **multichannel B2B outbound automation** (LinkedIn + email + X/Twitter, phone steps). "Safely automating LinkedIn since 2017" — **cloud-based** with dedicated 5G proxies + data-driven safety limits. Audience: **GTM Engineers, Sales Ops, Heads of Sales, SDRs/AEs** (strong fit for this repo).
- **API:** base **`https://apiv2.lagrowthmachine.com/flow`**, auth via **`apikey` query parameter** (from app.lagrowthmachine.com/settings/api). It's a "flow"-oriented API.
- **Operations (from Postman/integration listings):** **Leads** — `POST /flow/leads` to **add/enroll a lead into an audience** (the main write); **Search Lead**. **Campaigns** — Get Campaigns (paginated). **Audiences** — List Audiences. **Identities** — List Identities. **Webhooks** — **Create Inbox Webhook** + **List Inbox Webhooks** (real-time inbox events, e.g. lead replied).
- **Mental model:** you **enroll leads into an audience**; a **campaign** running over that audience executes the **sequence** across channels. There is **no "send message" endpoint** — enroll + sequence. **Identities** are the connected accounts that do the work, each with per-day **safety limits** (don't exceed → LinkedIn risk).
- **Webhooks = "inbox webhooks"** for real-time conversation events; canonical use "**create a CRM contact when a lead replies**." Signature/secret scheme not documented publicly — treat URL as secret + dedupe.
- **MCP server** for AI agents (Composio toolkit exists; LGM markets API + webhooks + MCP as first-class; some pages say MCP "coming soon" — treat as emerging/available, verify).
- **Native integrations:** HubSpot, Clay, Make, Slack; **Zapier, n8n, Pipedream**. Postman collection (authoritative endpoints): `documenter.getpostman.com/view/2071164/TVCmSkH2`.
- **Pricing (per identity/mo):** Basic ~€50 (core sequences) → Pro ~€100 (lookalike, LinkedIn intent, inbox rotation, advanced integrations) → **Ultimate ~€150 (custom sequences, webhooks, advanced CRM sync)**. **API/webhooks effectively need Ultimate.** 14-day trial. Per-identity model → cost scales with connected accounts.
- **Features:** waterfall enrichment (verified contacts), lookalike, **LinkedIn intent signals** (auto-import ICP), shared multichannel inbox, AI Magic Messages + AI Voice, sequence builder (conditions/branches/A-B/custom variables), outcome tags (Interested/Call Booked/Negotiating/Not Interested/Won/Lost), campaign + channel analytics.
- **Positioning:** **LinkedIn-first** (vs email-first lemlist with its built-in DB + lemwarm). Alternatives: lemlist, Waalaxy, Kanbox, Expandi, Emelia, Apollo, Reply.io.

⚠️ **Fetch note for future runs:** marketing site fetches fine; **`developer.lagrowthmachine.com` does not resolve** and the **Postman documenter is JS-rendered (404 to WebFetch)** — get endpoint detail from the Postman collection in a browser, the help center, or integration listings (Composio/MindCloud enumerate the operations). Confirmed: base URL, `apikey` auth, the operation set above. Gaps: exact per-endpoint JSON, pagination, rate limits, webhook event catalog + signing.
