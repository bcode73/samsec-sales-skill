---
name: sales-waalaxy
description: "Waalaxy platform help — LinkedIn + email outreach automation (Chrome extension) for solopreneurs and small teams: prospect lists from LinkedIn Search/Sales Navigator, 99+ ready-made sequences with auto follow-ups, an Email Finder, enrichment, a LinkedIn Inbox. Developer surface: REST API (base `https://developers.waalaxy.com`, `Bearer` key from CRM Sync settings) to list prospect lists + campaigns and import/enroll prospects (`POST /prospects/addProspectFromIntegration`, needs a LinkedIn URL + `origin`); plus Make/Zapier/n8n and HubSpot/Pipedrive sync — API gated to Advanced/Business plans. Use when importing prospects via the API, enrolling LinkedIn leads into a campaign automatically, wiring Waalaxy to HubSpot/Pipedrive/Make, your LinkedIn account got restricted or invites stopped sending, hitting the monthly invitation cap, or choosing Waalaxy vs lemlist/La Growth Machine. Do NOT use for outbound cadence strategy across tools (use /sales-cadence) or email deliverability/warmup (use /sales-deliverability)."
argument-hint: "[describe what you need help with in Waalaxy]"
license: MIT
version: 1.0.1
tags: [sales, outbound, cadence, platform]
---

# Waalaxy Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Import/enroll prospects via the API (`POST /prospects/addProspectFromIntegration`)
   - B) Read lists/campaigns via the API (`getProspectLists`, `campaigns/getAll`)
   - C) Wire Waalaxy to HubSpot/Pipedrive/Make/Zapier/n8n (no-code)
   - D) Fix a LinkedIn restriction / invites or messages not sending
   - E) Hit the monthly invitation cap or email-finder credit limit
   - F) Build/optimize a campaign sequence, or decide Waalaxy vs lemlist/LGM

2. **API or no-code?** Code → REST API (`Bearer` key from CRM Sync settings, Advanced/Business only). No endpoint → native HubSpot/Pipedrive, Make, Zapier, or n8n.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Outbound **sequence/cadence strategy** across tools (channels, timing, copy) | `/sales-cadence {question}` |
| Email **deliverability / warmup** for the email channel | `/sales-deliverability {question}` |
| LinkedIn outreach **strategy** / social selling across tools | `/sales-cadence {question}` |
| Building/cleaning a **prospect list** across data sources | `/sales-prospect-list {question}` |
| Generic iPaaS wiring to a CRM/other app | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-cadence design a LinkedIn + email multichannel sequence`".

## Step 3 — Waalaxy platform reference

**Read `references/platform-guide.md`** for the full reference — the prospect-list/campaign/prospect model (what's API vs UI), the per-account LinkedIn safety limits, plan tiers (API on Advanced/Business; cold email on Business), the Email Finder credit model, and quick-start recipes (import a prospect; list campaigns; sync to a CRM).

**Read `references/waalaxy-api-reference.md`** for the integration surface — base `https://developers.waalaxy.com`, **`Authorization: Bearer YOUR_KEY`** auth, the operations (`GET /integrations/test`, `GET /prospectLists/getProspectLists`, `GET /campaigns/getAll`, `POST /prospects/addProspectFromIntegration`), the import body schema (`prospects[]` with `url` + `customProfile`/`customVariables`, `prospectListId`, `campaignId`, `origin`), the RFC 7807 error shape, and native integrations.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **The write path is import-into-a-list (optionally enroll).** `POST /prospects/addProspectFromIntegration` adds prospects to a `prospectListId`; pass a `campaignId` to also enroll them in a running campaign. Every prospect needs a **LinkedIn `url`** — Waalaxy is LinkedIn-identity-centric, not email-first.
- **`origin` is mandatory.** Set `origin.name` to `make`, `zapier`, or `n8n` for native flows; a custom value shows up prefixed `API-` in the app so you can trace the source.
- **Get the IDs first.** You need a real `prospectListId` (from `getProspectLists`) and, to auto-enroll, a `campaignId` (from `campaigns/getAll`, which only returns **paused/running** campaigns). Don't hardcode stale IDs.
- **API needs Advanced or Business.** The API key only exists on **Advanced (€49)** and **Business (€69)**; Pro/Free can't call it. Cold email sequences need **Business**. Confirm the tier before building.
- **Respect the LinkedIn safety caps.** Monthly invite caps (Free 80 / Pro 300 / Advanced+Business 800) and Waalaxy's daily ramp exist to protect the account — it's a Chrome-extension tool, so over-aggressive sending is the #1 cause of restrictions.
- **It's not a sending API.** There's no "send LinkedIn message" endpoint — you import + the campaign sequence executes through the connected LinkedIn account. Model your flow around import + enroll.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — API base/endpoints from the official developer docs; pricing and limits from the pricing page + 2026 review roundups. Re-verify plan gates and caps in-account.*

1. **API is plan-gated.** The `Generate API key` button only appears on **Advanced/Business**. On Pro/Free there's no key — the API simply isn't available.
2. **Two base URLs float around.** The intro page mentions `api.waalaxy.com`, but every endpoint reference resolves to **`https://developers.waalaxy.com`** — use that.
3. **`origin` is required on import.** Omitting `origin.name` rejects the request; native values are `make`/`zapier`/`n8n`, custom ones appear as `API-…`.
4. **Every prospect needs a LinkedIn URL.** `addProspectFromIntegration` is keyed on the LinkedIn `url`; an email alone won't create a prospect.
5. **Chrome extension = account risk.** Waalaxy runs in your browser against your real LinkedIn session — exceeding the daily ramp or monthly cap is the top cause of restricted accounts. Warm up new accounts slowly.
6. **Cold email is Business-only.** Pro/Advanced get the Email Finder (credits) but **automated cold-email sequences** require the Business plan; multichannel = Business.
7. **The LinkedIn Inbox is a paid add-on.** Reply management (Inbox Waalaxy) is ~€20/user/mo on top of the base plan, not included.
8. **Annual billing is upfront.** The ~50% annual discount requires paying the full year up front — factor that into "real cost."

## Related skills

- `/sales-cadence` — Outbound sequence/cadence strategy across tools (Waalaxy is one of the LinkedIn-first platforms covered) — channel mix, timing, copy, tool selection vs lemlist/LGM/Expandi- `/sales-prospect-list` — Building/cleaning prospect lists across data sources before importing into Waalaxy
- `/sales-deliverability` — Email warmup + inbox placement for Waalaxy's email channel
- `/sales-integration` — Wiring Waalaxy into a CRM via the API / Make / Zapier / n8n
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Import a LinkedIn lead into a campaign via the API (developer/automation)
**User says**: "When a lead signs up in my app, how do I push their LinkedIn profile into a Waalaxy campaign automatically?"
**Skill does**: Walks Recipe 1 — first `GET /prospectLists/getProspectLists` and `GET /campaigns/getAll` to grab a `prospectListId` and `campaignId`, then `POST https://developers.waalaxy.com/prospects/addProspectFromIntegration` with `Authorization: Bearer YOUR_KEY`, a `prospects[]` entry containing the LinkedIn `url` (+ optional `customProfile`/`customVariables`), the `prospectListId`, the `campaignId`, and a required `origin.name`. Notes the API needs the **Advanced/Business** plan and that the campaign sequence does the actual sending.
**Result**: New app signups flow straight into the right LinkedIn sequence.

### Example 2: My LinkedIn account got restricted
**User says**: "I started a Waalaxy campaign and LinkedIn restricted my account within a day."
**Skill does**: Explains that Waalaxy is a Chrome-extension tool acting on the real LinkedIn session, so over-aggressive volume trips LinkedIn's limits. Recommends pausing campaigns, respecting the monthly invite cap (Free 80 / Pro 300 / Advanced+Business 800) and Waalaxy's daily ramp, warming a new/low-activity account slowly, and personalizing connection notes. Routes the broader strategy: "run: `/sales-cadence recover a restricted LinkedIn account and set safe daily limits`."
**Result**: A safer sending posture and a recovery plan.

### Example 3: Waalaxy vs lemlist vs La Growth Machine
**User says**: "I'm a solo founder — should I use Waalaxy, lemlist, or La Growth Machine for LinkedIn outreach?"
**Skill does**: Frames the split — **Waalaxy** is the simplest/cheapest LinkedIn-first tool (Chrome extension, ready-made sequences, Free tier, cold email only on Business), **lemlist** is email-first with a built-in lead DB and warmup, **LGM** is cloud-based multichannel with stronger safety. Recommends Waalaxy for a budget LinkedIn-led motion, then routes the decision: "run: `/sales-cadence choose a LinkedIn-first outbound tool for a solo founder`."
**Result**: A grounded tool choice based on channel emphasis and budget.

## Troubleshooting

### My API calls return 401 / there's no API key in settings
**Symptom**: Requests to `developers.waalaxy.com` are rejected, or you can't find where to generate a key.
**Cause**: The API is gated to **Advanced/Business**, or the `Authorization: Bearer` header is missing/wrong.
**Solution**: Confirm you're on Advanced or Business, open **CRM Sync settings → Generate API key** (shown once — store it securely), and send `Authorization: Bearer YOUR_KEY` on every request. Test with `GET /integrations/test` (returns `true`) before anything else.

### Imported prospects don't get worked / don't enter the campaign
**Symptom**: `addProspectFromIntegration` succeeds but no outreach happens.
**Cause**: No `campaignId` was passed (import only lands them in a list), the campaign isn't paused/running, the prospect was a duplicate, or `origin` was missing.
**Solution**: Pass a valid `campaignId` from `campaigns/getAll` (only paused/running campaigns are returned), include the required `origin.name`, and check the response `importCode`/`addToCampaignCode` per prospect (`duplicated_prospect` means it already existed). Use `addExistingProspectInCampaign` to enroll prospects already in your CRM.

### Invites/messages stopped sending mid-campaign
**Symptom**: A campaign stalls and no new actions fire.
**Cause**: You hit the monthly invitation cap, the daily ramp limit, the LinkedIn account is restricted, or the Chrome extension/computer was offline (extension-based execution needs the browser running).
**Solution**: Check remaining monthly invites for your plan, ensure the extension is installed and LinkedIn is logged in, and look for a LinkedIn restriction banner. For volume/timing strategy use `/sales-cadence`; for restriction recovery use `/sales-cadence`.
