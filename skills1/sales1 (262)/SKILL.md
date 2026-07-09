---
name: sales-jamy
description: "Jamy.ai platform help — AI meeting assistant with real-time transcription, 100+ language translation, and cross-language search. Use when setting up Jamy for multilingual meetings, configuring auto-join for Zoom/Meet/Teams, connecting Jamy to HubSpot CRM, building API integrations with Jamy's Create Report endpoint, troubleshooting Jamy bot not joining meetings, comparing Jamy pricing tiers (Starter/Pro/Global Business), or syncing meeting notes to Slack/Notion/Trello. Do NOT use for picking between note-takers (use /sales-note-taker) or reviewing a call for coaching (use /sales-call-review)."
argument-hint: "[describe what you need help with in Jamy]"
license: MIT
version: 1.0.0
tags: [sales, note-taker, platform]
---

# Jamy.ai Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What's your goal?**
   - A) Set up Jamy for my team (onboarding, calendar, auto-join)
   - B) Configure integrations (CRM, Slack, Notion, PM tools)
   - C) Use the API to build custom integrations
   - D) Troubleshoot a problem (bot not joining, missing transcripts, etc.)
   - E) Understand pricing and plan differences

2. **Which plan are you on?**
   - A) Starter (free)
   - B) Pro ($14.99/mo)
   - C) Global Business ($29.99/mo)

3. **Primary use case?**
   - A) Multilingual team meetings (translation is key)
   - B) Sales calls with CRM sync
   - C) General meeting notes and action items
   - D) Phone call transcription

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Choosing between Jamy and other note-takers | `/sales-note-taker {user's question}` |
| Reviewing a specific call for coaching | `/sales-call-review {user's question}` |
| Building a coaching program | `/sales-coaching {user's question}` |
| General CRM/tool integration patterns | `/sales-integration {user's question}` |
| HubSpot-specific questions beyond Jamy sync | `/sales-hubspot {user's question}` |

Otherwise, answer directly below.

## Step 3 — Jamy platform reference

**Read `references/platform-guide.md`** for the full platform reference — modules, pricing, integrations, data model, workflows.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

You no longer need the platform guide — focus on the user's specific situation.

**Setup priority order:**
1. Connect calendar (Google Calendar or Outlook) for auto-join
2. Test with a short meeting to verify transcription quality
3. Configure custom report templates for your meeting types
4. Set up integrations (HubSpot, Slack, Notion) based on workflow
5. Explore translation if team is multilingual

**When evaluating Jamy vs competitors:**
- Jamy's unique advantage is real-time translation in 100+ languages + cross-language search — no other note-taker at this price point matches it
- Weaknesses: immature CRM ecosystem (HubSpot only, Salesforce/Pipedrive "coming soon"), limited G2/Capterra social proof, reliability concerns from AppSumo reviews
- If translation isn't important, Fathom (free tier) or Fireflies (conversation search) are stronger choices

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research — review these, especially items about plan-gated features and integration gotchas that may be outdated.*

- **Bot-not-joining is the #1 reported issue.** Multiple AppSumo users report calendar integration breaking — bot stops recognizing meetings. If this happens, try disconnecting and reconnecting your calendar. AppSumo-onboarded users have reported worse reliability than direct signups.
- **"Premium feature" paywalls appear unexpectedly.** Some features that appear accessible (like custom templates) may trigger upgrade prompts. Check your plan's feature list before relying on a capability.
- **Salesforce/Pipedrive/Close CRM integrations are "coming soon"** — only HubSpot works natively today.
- **Free tier limits are strict.** 300 min/mo transcription, 60 min/mo translation, 60-min max meeting length, plus structural caps (1 workspace folder, 1 team member, 1 custom template, 1 Space). For a team doing 5+ meetings/day, you'll hit limits fast.
- **API Keys and Webhooks are Global Business only (verified 2026-06-13).** Both are listed as $29.99/mo Global-Business features on the live pricing page — Starter and Pro cannot use the API or webhooks. Any programmatic/CRM-sync pipeline forces the Global Business tier. White Label and Custom Words are also Global-Business-only.
- **Paid-tier transcription is NOT unlimited.** As of 2026-06-13 the pricing page lists capped monthly bundles: Pro = 300 + 500 min/mo, Global Business = 800 + 500 min/mo. Earlier "unlimited" copy is gone.
- **Webhooks run on Svix.** Configure at Settings → Webhooks → Configure Webhooks (redirects to Svix). The only event is `meeting.processed`, which sends the report object (fields include `tasks`, `summary`, `url`, `duration`). Verify deliveries with the Svix `svix-id`/`svix-timestamp`/`svix-signature` headers (HMAC-SHA256, `whsec_` secret, 5-min replay window) — use the `svix` SDK.
- **API docs are a JS-rendered SPA at docs.jamy.ai** — can't be scraped, so exact endpoint paths/methods/auth headers aren't publicly documented. The help center has prose docs for Create Report (recording must be at a publicly accessible URL) and Answer Question.
- **Phone call recording** is listed as a feature but plan availability is unclear.

## Related skills

- `/sales-note-taker` — Choosing between AI note-takers (Fathom, Fireflies, Avoma, Gong, Otter, and 10+ others) or building transcript API pipelines
- `/sales-hubspot` — HubSpot platform help for CRM-side configuration
- `/sales-integration` — General CRM/tool integration patterns (Zapier, Make, webhooks)
- `/sales-call-review` — Review a specific call for coaching
- `/sales-coaching` — Build coaching programs that consume call data
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`

## Examples

### Example 1: Setting up Jamy for a multilingual sales team
**User says**: "My team does sales calls in English, Spanish, and German. We need meeting notes and translations — is Jamy right for us?"
**Skill does**:
1. Confirms Jamy is the strongest option for multilingual — 100+ languages with real-time translation
2. Recommends Global Business plan ($29.99/mo) for unlimited translation
3. Walks through setup: connect calendar, enable auto-join, configure language preferences
4. Notes HubSpot CRM sync works today; Salesforce is "coming soon"

### Example 2: Building an API integration
**User says**: "I want to send Jamy meeting reports to our internal dashboard via API"
**Skill does**:
1. Points to API docs at docs.jamy.ai, help center article for Create Report endpoint
2. Flags that API Keys are a Global Business ($29.99/mo) feature — Starter/Pro can't use the API
3. Explains API key generation (Settings → API Keys, OWNER role required)
4. Suggests the `meeting.processed` webhook (delivered via Svix; verify `svix-signature`) or Zapier/Make as an event-driven alternative if polling the API is insufficient
5. Warns about JS-rendered docs — exact endpoint paths/methods aren't published, so explore manually or rely on the help center

### Example 3: Bot stopped joining meetings
**User says**: "Jamy's bot hasn't joined my last 3 Google Meet calls"
**Skill does**:
1. Identifies this as the #1 reported issue (calendar integration breaking)
2. Recommends: disconnect calendar → reconnect → test with a short meeting
3. If AppSumo user: notes known issue where AppSumo onboarding flow causes auto-join failures — try signing up directly from jamy.ai
4. Suggests checking Settings → Calendar to verify connection status

## Troubleshooting

### Bot not joining meetings
**Symptom**: Jamy stops auto-joining scheduled meetings after previously working
**Cause**: Calendar integration silently disconnects — more common with AppSumo-onboarded accounts
**Solution**: Go to Settings → Calendar, disconnect and reconnect your Google Calendar or Outlook. Test with a short meeting. If using an AppSumo account and the problem persists, contact support — some users report resolution after account migration.

### Missing or incomplete transcripts
**Symptom**: Meeting was recorded but transcript is partial or blank
**Cause**: Free tier has 300 min/mo cap and 60-min max meeting length — exceeding either silently truncates
**Solution**: Check your usage in Settings. If you're on Starter and hitting limits, upgrade to Pro ($14.99/mo) for a larger monthly transcription bundle (300 + 500 min/mo as of 2026-06-13, not unlimited) and unlimited meeting length.

### Translation not working
**Symptom**: Translation feature prompts for upgrade or doesn't appear
**Cause**: Starter plan has only 60 min/mo translation; Pro has 300 min/mo
**Solution**: If multilingual meetings are your primary use case, Global Business ($29.99/mo) provides unlimited translation up to 4-hour meetings. Check your translation minute usage in the dashboard.
