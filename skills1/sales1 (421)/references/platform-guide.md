# Plaud Platform Reference

## Platform overview

Plaud is the leading hardware AI voice recorder brand with 1.5M+ global users. Unlike software-based meeting note-takers that join calls as bots, Plaud uses physical recording devices (wearable pins and credit-card recorders) to capture in-person meetings, phone calls, and ambient audio. Recordings sync to Plaud's cloud for AI-powered transcription, speaker diarization, and structured summaries. Targets professionals in sales, healthcare, consulting, legal, finance, and education who need frictionless in-person recording without phone apps or laptop dependencies.

Won Red Dot Design Award (2025) and Tom's Guide "best wearable" (2025).

## Devices

### NotePin S (newest — recommended)
- **Price**: $179
- **Form factor**: Wearable pin with clip, lanyard, and wristband options
- **Microphones**: 2 MEMS
- **Recording**: 20 hours continuous, 40-day standby
- **Storage**: 64GB internal
- **Connectivity**: Bluetooth
- **Key improvement**: Physical button — fixes unreliable touch controls on original NotePin
- **Capture range**: ~9.8 feet (3m)
- **VCS**: Yes — phone call recording via vibration conduction sensor

### NotePin (original)
- **Price**: $159 (sales/promo pricing varies)
- **Form factor**: Wearable pin
- **Microphones**: 2 MEMS
- **Recording**: Standard battery life
- **Storage**: 64GB
- **Key issue**: Touch controls are unreliable — #1 user complaint
- **VCS**: Yes

### Note
- **Price**: $159
- **Form factor**: Credit-card size, portable recorder (not truly wearable)
- **Microphones**: 2 MEMS
- **Recording**: Extended battery vs NotePin
- **Storage**: 64GB
- **Features**: Real-time highlighting (not available on NotePin)
- **VCS**: Yes

### Note Pro
- **Price**: $189
- **Form factor**: Credit-card size
- **Microphones**: 4 MEMS (doubled)
- **Recording**: Nearly double battery vs Note
- **Storage**: 64GB
- **Capture range**: 16+ feet (5m) — best for large rooms
- **Features**: Real-time highlighting
- **VCS**: Yes

### Device comparison

| Feature | NotePin | NotePin S | Note | Note Pro |
|---|---|---|---|---|
| Price | $159 | $179 | $159 | $189 |
| Wearable | Yes | Yes | No (portable) | No (portable) |
| Microphones | 2 | 2 | 2 | 4 |
| Capture range | 9.8 ft | 9.8 ft | 9.8 ft | 16+ ft |
| Physical button | No (touch) | Yes | N/A | N/A |
| Real-time highlight | No | No | Yes | Yes |
| Battery | Standard | Standard+ | Extended | Nearly 2x Note |
| VCS phone recording | Yes | Yes | Yes | Yes |

## Pricing and subscriptions

All devices include 64GB local storage. Transcription/AI features require a subscription (or free Starter tier). Verified against plaud.ai/pages/plaud-ai-plan-pricing on 2026-06-13.

| Plan | Price | Transcription minutes | First unlocks |
|---|---|---|---|
| Starter | Free | 300/month | 112-language transcription, 10,000+ AI summary templates, multidimensional summaries (Beta) |
| Pro | $99.99/yr ($17.99/mo) | 1,200/month | Everything in Starter + **Ask Plaud**, **Zapier**, **Google Calendar**, **custom vocabulary**, **auto speaker labeling** |
| Unlimited | $239.99/yr ($29.99/mo) | Unlimited (24hr/day cap) | Everything in Pro + **AutoFlow** (auto-summarize + email summaries), no minute cap |
| Team | $35/user/mo ($28 launch offer through 2026-08-31); annual $25/user/mo ($20 launch) | Unlimited (24hr/day cap) | Everything in Unlimited + centralized billing, seat/device management, workspace data residency, priority support, secure offboarding |

**Plan-gate notes** (corrected 2026-06-13): Ask Plaud, Zapier, Google Calendar, custom vocabulary, and auto speaker labeling are **NOT** in the free Starter tier — they start at **Pro**. AutoFlow starts at **Unlimited**. Starter is essentially capped GPT-class transcription + summary templates only.

**Note**: Device purchase does not include bundled transcription minutes — subscription is separate.

Multiple devices can pair to a single subscription account.

## Compliance and security

- ISO 27001 / ISO 27701 certified
- GDPR compliant
- SOC 2 Type II
- HIPAA compliant
- EN 18031 compliant
- Cloud-based processing (recordings stored locally until synced)

## Vibration Conduction Sensor (VCS)

Plaud's key hardware differentiator. The VCS detects mechanical vibrations from the phone's earpiece voice coil, capturing both sides of a phone call without speakerphone and without any software or carrier bypass. This works by:

1. Place Plaud device on the phone's earpiece area (top edge near speaker)
2. VCS captures the caller's voice through vibrations
3. Ambient mic captures your voice simultaneously
4. Both are combined into a single recording with speaker diarization

**Tips for best VCS quality**:
- Remove thick phone cases during recording
- Place device directly on the earpiece speaker area
- Ensure VCS side faces the phone
- Speakerphone is a fallback if VCS quality is insufficient

## AI features

- **Transcription**: 112 languages, speaker diarization (auto speaker labeling is Pro+)
- **Summaries**: 10,000+ professional templates (meeting notes, action items, key decisions, etc.) — available on Starter
- **Ask Plaud**: Chatbot to query your recording history — **Pro plan+**
- **AutoFlow**: Automatically summarize recordings and email summaries to specified recipients — **Unlimited plan+**
- **Mind maps**: Visual summary generation
- **Custom vocabulary**: Add industry-specific terms for better accuracy — **Pro plan+**

## Integrations

- **Zapier**: Native Plaud Zapier app (Pro plan+). Trigger fires when a transcript & summary are ready; route to Google Calendar, CRMs, Slack, etc. (triggers — actions limited).
- **Google Calendar**: Native integration (Pro plan+).
- **MCP server**: `https://mcp.plaud.ai/mcp` — exposes files/transcripts/summaries to Claude, Cursor, ChatGPT, etc.
- **Cloud sync**: Recordings accessible across devices after upload
- **Email**: AutoFlow sends summaries via email (Unlimited plan+)
- **Export**: Transcript and summary export/sharing

No documented native Make or n8n connectors (use Zapier or the MCP server). The official Embedded REST API (see Developer API section) is the path for direct CRM/data-warehouse pipelines.

## Developer API (public docs, Beta v1.0.0 — launched 2026-05-12)

The Plaud Developer Platform is publicly documented at docs.plaud.ai/documentation. The Embedded SDK + REST API launched as Developer Platform Beta v1.0.0 on 2026-05-12; core SDK and transcription services are described as GA. Credential access is **gated**: request access via the contact form in the developer console at **dev.plaud.ai**, then create an app to get a Client ID + Secret Key. See `references/plaud-api-reference.md` for the full endpoint/auth reference.

- **Base URL**: `https://platform-<region>.plaud.ai/developer/api` (US and Japan live; EU and Singapore coming soon)
- **Auth**: two-step OAuth — Basic Auth `client_id:secret_key` → partner token (`POST /oauth/partner/access-token`); then `POST /open/partner/users/access-token` → per-user JWT. Transcription calls use `X-Client-Id` + `X-Client-Api-Key` headers.
- **Endpoints**: `POST /open/partner/ai/transcriptions/` (submit `file_url` + diarization/language params) and `GET /open/partner/ai/transcriptions/{id}` (poll status, returns transcript/summary JSON). No documented webhooks — detect completion by polling.
- **Capabilities**: transcription (112 languages, diarization), AI summary, file management, device management (start/stop/monitor recordings, BLE/WiFi transfer)
- **SDKs**: official iOS (Swift, SPM, iOS 13+) and Android (Kotlin, Maven, API 21+); Swift SDK public at github.com/Plaud-AI/plaud-sdk-public. No official Python SDK.
- **MCP + CLI** (Plaud App account data, separate from Embedded API): remote MCP at `https://mcp.plaud.ai/mcp`, local install `npx -y @plaud-ai/mcp@latest install`, plus official CLI `@plaud-ai/cli` (`npm i -g`, Node ≥20, OAuth).

### Unofficial Python client

The `plaud-api` package (pip install plaud-api) is a reverse-engineered, unofficial client. **Not affiliated with Plaud Inc. — use at your own risk.**

```bash
pip install plaud-api  # Requires Python 3.10+
```

**Auth**: Get token from web.plaud.ai DevTools → Network → any api.plaud.ai request → Authorization header. Then `plaud auth setup`.

**Key methods**:
- `client.recordings.list(limit=50)` — list recordings
- `client.recordings.get(file_id)` — get single recording
- `client.recordings.get_audio_url(file_id)` — S3 download URL
- `client.recordings.upload(path, name=...)` — upload MP3/OPUS
- `client.transcriptions.start(file_id, language="en")` — begin transcription
- `client.transcriptions.wait(file_id, timeout=600)` — block until done
- `client.transcriptions.get(file_id)` — get transcript segments
- `client.transcriptions.get_summary(file_id)` — get AI summary
- `client.speakers.list()` — list speakers
- `client.speakers.rename(file_id, old, new)` — rename speaker
- `client.tags.list()` — list tags

**CLI**: `plaud recordings list`, `plaud transcription start <id>`, `plaud transcription summary <id>`, `plaud speakers list`, `plaud auth setup`

## Affiliate and partner programs

- **Affiliate**: 5-10% commission via Impact. Apply at affiliate@plaud.ai. Monthly payouts, real-time tracking, dedicated affiliate manager.
- **Referral**: 10% discount codes for hardware, phased rollout to selected users
- **Reseller**: Partner program with early access to product updates. Contact via plaud.ai/pages/become-a-reseller.

## Workflow setup

### Setting up for in-person meetings
1. Charge device via proprietary dock
2. Download Plaud app (iOS/Android), pair via Bluetooth
3. Choose subscription plan (Starter free to start)
4. Before meeting: press button (NotePin S) or tap (NotePin) to start recording
5. Place device on table (Note/Pro) or wear it (NotePin/S)
6. After meeting: open app to sync — transcription begins automatically
7. Review transcript, edit speaker names, apply summary template
8. Export or share via AutoFlow email

### Setting up for phone calls (VCS)
1. Start recording on Plaud device
2. Place device on phone's earpiece area (top edge, speaker side)
3. Make or answer the call normally (earpiece, not speakerphone)
4. VCS captures both sides of the conversation
5. After call: sync via app for transcription

### Building a transcript pipeline
**Preferred — official Embedded REST API** (request access at dev.plaud.ai):
1. Create an app in the dev.plaud.ai console → get Client ID + Secret Key
2. Mint a partner token (`POST /oauth/partner/access-token`, Basic Auth) and a per-user JWT (`POST /open/partner/users/access-token`)
3. Submit audio: `POST /open/partner/ai/transcriptions/` with `file_url` + diarization params (`X-Client-Id`/`X-Client-Api-Key` headers)
4. Poll `GET /open/partner/ai/transcriptions/{id}` until `status: SUCCESS` → normalize JSON → push to CRM/warehouse
5. No webhooks documented — use polling.

**No-code alternative**: Zapier (Pro+) trigger "transcript & summary ready" → CRM/Slack, or the MCP server (`https://mcp.plaud.ai/mcp`) for agent access.

**Interim / unofficial (consumer backend)**:
1. Install: `pip install plaud-api`
2. Get auth token from web.plaud.ai DevTools → `plaud auth setup`
3. Poll `client.recordings.list()` on a schedule, then `client.transcriptions.get(file_id)` → push to CRM/warehouse. Reverse-engineered and unsupported.
