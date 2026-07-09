# Bitrix24 — Learnings

Accumulated, dated platform knowledge. Append new findings with a date stamp so staleness is auditable.

---

**2026-06-27**: Research baseline. Built from the marketing site (bitrix24.com/features) and the official API docs (apidocs.bitrix24.com — local-webhooks + crm.deal.add).

- **Category:** **free-forever all-in-one business suite** — CRM (leads/deals/pipelines/contacts/companies/SPA), tasks & projects, omnichannel contact center, sites/store builder, marketing, collaboration, HR/automation. Cloud **or self-hosted on-prem**. Hook = **unlimited users on the free plan** → popular free **Keap/Ontraport/Zoho/HubSpot-free alternative** for solo founders + SMB (also scales to enterprise). 740+ app Market; **MCP server** for AI tools.
- **API is method-based RPC over REST** (not resource paths). URL: **`https://{portal}.bitrix24.com/rest/{user_id}/{webhook_code}/{method}.json?params`** (inbound webhook) or via **OAuth 2.0** (apps/Market/multi-tenant). Webhooks have **no expiry**; OAuth tokens expire (refresh).
- **Auth choice:** inbound **webhook** for automating *your own* portal (static URL + secret code, scoped permissions, created at Applications → Developer resources → Incoming webhook); **OAuth 2.0** for apps others install or anything needing UI (Local application / Market). Some methods (telephony, certain app-only ops, some chatbot events) are **unavailable to webhooks**.
- **CRM methods:** consistent verb set per entity — `crm.lead.*`, `crm.deal.*`, `crm.contact.*`, `crm.company.*`, `crm.activity.*`, `crm.status.*` (stages), `crm.dealcategory.*` (pipelines/funnels), `crm.currency.*`, and `crm.item.*` for **Smart Process Automation** custom objects. Verbs: `.add/.update/.get/.list/.delete/.fields`.
- **Deal fields:** `TITLE`, **`CATEGORY_ID`** (pipeline id, 0=default), **`STAGE_ID`** (crm_status within that funnel), `CURRENCY_ID`, `OPPORTUNITY` (amount), `CONTACT_IDS[]`, `COMPANY_ID`, `ASSIGNED_BY_ID`, `CLOSEDATE`, `SOURCE_ID`, `PROBABILITY`, `IS_RECURRING`; `PARAMS.REGISTER_SONET_EVENT`. **Add response:** `{"result": <id>, "time": {...}}`. Errors: `{"error","error_description"}`.
- **Pipelines/stages are IDs, not labels.** Read `crm.dealcategory.list` + `crm.status.list` before writing; a `STAGE_ID` from the wrong funnel misroutes.
- **Outbound webhooks (events):** `ONCRMDEALADD/UPDATE`, `ONCRMLEADADD`, etc. POST `{event, data:{FIELDS:{ID}}}` + an **application token** (verify it). **Payload carries only the ID** → re-fetch via `*.get`; dedupe. On-prem outbound webhooks need an active license.
- **Rate limits:** throttled (~2 req/sec sustained + per-method "operating time"/leaky-bucket). Use **`batch`** (up to **50 commands/request**, chain with `$result[...]`), page `*.list` via `start` (50/page, `next`+`total`), and back off.
- **Pricing/hosting:** Free (unlimited users, caps) → cloud Basic/Standard/Professional/Enterprise (fixed user cap per tier, not pure per-seat) → On-Premise license. Changes often — verify.

⚠️ **Fetch note for future runs:** `apidocs.bitrix24.com` is fully fetchable and excellent (per-method pages). The marketing `/features` page renders; `/prices` is JS-heavy (verify tiers/limits in-account). Exact rate-limit numbers + full event list: confirm in the live docs.
