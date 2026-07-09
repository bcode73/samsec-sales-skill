# Letterly Platform Reference

## Platform overview

Letterly is an AI-powered speech-to-text app that transforms unstructured voice recordings into polished, formatted written content. Unlike pure transcription tools (Voicenotes) or rewriting tools (AudioPen), Letterly focuses on instant content reformatting — 25+ rewrite options turn a voice memo into a social post, formal email, to-do list, journal entry, or article outline within seconds. Available on iOS, Android, web, macOS, and Windows (Windows app released June 2026). 300,000+ users. 90+ languages with automatic detection and mid-sentence language switching. Targets content creators, entrepreneurs, journalists, and professionals who need quick, formatted output from spoken thoughts.

## Key modules

### Recording & capture
- **One-tap recording**: Widget for instant recording from home screen
- **Screen-off recording**: Continues recording with screen locked (mobile)
- **Offline recording**: Records without internet — processes when back online
- **Audio/video file upload**: Transcribe existing audio and video files from any device (added Aug 2025) — no longer record-only
- **Automatic language detection**: Recognizes 90+ languages without manual selection, including mid-sentence language switching
- **90-minute session limit**: Each recording caps at 90 minutes (raised from 15 min in May 2025) — long enough for full meetings, lectures, or deep-thinking sessions; unlimited number of recordings

### AI rewriting
- **25+ built-in rewrite options**: Structured text, X/Twitter posts, formal emails, friendly messages, to-do lists, journal entries, meeting notes, blog drafts, video scripts, and more
- **Custom rewrites**: Create your own rewrite instructions for consistent output formatting
- **One-tap rewrite**: Select any rewrite option and get reformatted output in seconds
- **Translation**: Translate output into any supported language after rewriting

### Organization
- **Tags**: Tag-based note organization (no folders — tags are the primary organization method)
- **Cross-device sync**: Notes sync across iOS, Android, web, macOS via cloud
- **Dark/light mode**: UI theme support

### AI tool connections
Letterly can send notes directly to AI tools for further processing:
- Claude
- ChatGPT
- Cursor
- Perplexity
- Gemini
- Codex

**MCP server (added April 2026)**: Letterly now exposes a Model Context Protocol (MCP) connection so AI tools — Claude, ChatGPT, Cursor, and others — can query and act on your notes directly ("ask about your notes, write and rewrite text"). This is in addition to the one-tap "send to AI tool" buttons above.

## Pricing and limits

**AppSumo Lifetime Deal (primary pricing path)** — stackable-code model (verified 2026-06-13):
- 1 code: ~~$200~~ → $89
- 2 codes: ~~$400~~ → $178
- 3 codes: ~~$800~~ → $267
- 4 codes: ~~$1,200~~ → $356
- "Stack" codes to raise feature limits; lifetime access
- All plans: unlimited recordings, rewrite options, 90+ languages, 90-min recording limit
- Refundable up to 60 days

> Note: the older LTD tiers ($69/$138/$207, framed as 1/2/4-device licenses) are no longer the live offer. AppSumo now lists $89/$178/$267/$356 stackable codes. Device-count framing may persist in older reviews; treat the code-stacking model as current.

**Regular pricing**: Mobile-app subscription. Exact official tiers are not reliably published on a public pricing page (the website pricing path returned 404 at verification); third-party aggregators report roughly ~$9/mo or ~$70–99/yr but these are UNVERIFIED against an official source — confirm in-app or on the app store before quoting.

**Key limits**:
- 90-minute max recording per session (raised from 15 min in May 2025)
- Audio/video file upload now supported (added Aug 2025) — no longer record-only
- LTD uses stackable codes (raise feature limits by stacking)
- No team/workspace features

## Integrations

### Zapier
- Connects to 8,000+ apps via Zapier
- Trigger: **"Letterly Actions"** — fires "when you select an action from the note" (it is NOT an automatic "Note Created" trigger; you must tap the action inside the note to push it)
- Use the Actions button inside any note to send via Zapier
- Exported fields per third-party Zapier docs: title, text, date, tags (text-only — audio file is not sent via Zapier/webhook); audio export is "being considered"
- Some users report intermittent trigger reliability issues

### Webhooks
- Custom webhook support available
- Send notes to Google Docs, Notion, or any webhook-accepting endpoint
- Configured via the Actions button inside each note
- Payload format and authentication not publicly documented

### AI tool integrations
- Direct send to Claude, ChatGPT, Cursor, Perplexity, Gemini, Codex
- Useful for further processing, summarization, or expansion of voice-captured content

### No public REST API — but an MCP server exists
- No public REST API endpoints or SDKs
- **MCP server available (added April 2026)**: connect Letterly to Claude, ChatGPT, Cursor, and other AI tools via Model Context Protocol — query notes and write/rewrite text programmatically through the AI client
- Zapier + webhooks + MCP are the integration paths (no traditional REST API for custom backend development)

## Workflow setup

### Basic voice-to-content workflow
1. Open Letterly → tap record (or use widget for one-tap)
2. Speak your thoughts — unstructured is fine
3. Tap stop — AI transcribes automatically
4. Select a rewrite option (email, social post, to-do, etc.)
5. Copy the rewritten text or share directly

### Automated content pipeline
1. Record voice memo in Letterly
2. Inside the note, tap Actions → Zapier or Webhook
3. Zapier routes to: Buffer/Hootsuite (social), Google Docs (long-form), Notion (knowledge base), Slack (team updates)
4. For multi-destination fan-out, create multiple Zaps from the same trigger

### Multilingual content creation
1. Record in any of 90+ languages — auto-detected
2. Select rewrite option for formatting
3. Use translation feature to convert to target language
4. Copy or share the translated, formatted output

## Comparison with voice note competitors

| Feature | Letterly | AudioPen | TalkNotes | Voicenotes |
|---|---|---|---|---|
| Rewrite options | 25+ built-in | AI rewriting (custom styles) | 100+ templates | Summaries, to-dos, emails |
| Custom rewrites | Yes | Yes (writing samples) | Yes (custom styles) | No |
| Recording limit | 90 min | 15 min (Prime) | 20 min (Plus) / 2 hr (Pro) | Unlimited (paid) |
| Audio upload | Yes (added Aug 2025) | Yes (Prime) | Yes | Yes |
| Search | No | No | AI Chat (v1.6.0+) | Ask AI (semantic) |
| Languages | 90+ | 58 input / 64 output | 50+ | 100+ |
| Pricing model | LTD $89+ (stackable codes) or subscription | One-time $33-159 | Subscription ~$10-49/mo | Freemium $0-14.99/mo |
| Free tier | Yes (limited) | Yes (10 notes, 3 min) | No (7-day trial) | Yes |
| Zapier | Yes | Yes (Prime, 1 trigger) | Yes (1 trigger) | Yes (9 triggers) |
| Webhooks | Yes | Yes (Prime) | Yes | Yes |
| Native sync | None | None | None | Obsidian, Notion, Readwise |
| Platforms | iOS, Android, web, macOS | iOS, Android, Mac, Chrome, web | iOS, Android, web | iOS, Android, web, Apple Watch, WearOS |
| CRM integration | None | None | None | None |
| Speaker diarization | No | No | No | No |

### When to pick Letterly over alternatives
- **Over AudioPen**: When you want more built-in rewrite options (25+ vs style-based rewriting), need 90+ language support vs 58, or prefer the lifetime deal pricing model
- **Over TalkNotes**: When you want a permanent free tier (TalkNotes has 7-day trial only), need offline recording, or prefer built-in rewrite options over template-driven output
- **Over Voicenotes**: When you prioritize content reformatting (social posts, emails) over thought capture and search, or need offline recording

### When to avoid Letterly
- **Need search across notes** → Voicenotes (Ask AI semantic search). (Letterly's MCP server lets an AI client query notes, but there's no built-in search UI.)
- **Need recordings longer than 90 min in one file** → TalkNotes Pro (2 hours), Voicenotes (unlimited). (Letterly now supports up to 90 min per recording.)
- **Need native Obsidian/Notion sync** → Voicenotes
- **Need a public REST API** → Fathom, Fireflies, Wave (Letterly offers MCP + Zapier + webhooks but no REST API)
- **Need CRM integration** → Fathom Business, Sybill, tl;dv
- **Need speaker diarization** → Fireflies, Otter, Fathom

(Note: audio/video file upload IS now supported in Letterly as of Aug 2025, so it's no longer a reason to avoid it.)
