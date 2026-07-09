# Talo Platform Reference

## Overview

Talo (by Palabra.AI LTD) is a real-time AI meeting translation tool that joins Zoom, Google Meet, and Microsoft Teams calls as a single bot, translating all participants' speech into 60+ languages. Positioned as an enterprise-grade alternative to budget translators, it differentiates on SOC 2/ISO 27001 compliance, single-bot architecture (one bot handles all languages), and no meeting data retention. Developers can embed translation via Palabra's speech-to-speech API.

## Capabilities & automation surface

| Capability | Description | Access |
|---|---|---|
| Real-time meeting translation | Single AI bot joins Zoom/Meet/Teams, translates all participants | UI (Talo app) |
| Voice cloning | Clone a voice from audio samples for translated output | API-accessible (Palabra API) |
| Custom glossaries | Upload domain-specific term pairs to improve translation accuracy | API-accessible (Palabra API) |
| Session management | Create/manage streaming translation sessions | API-accessible (Palabra API) |
| Managed events | Create/manage multilingual events with listener join-requests, stats, CSV export | API-accessible (`/saas/v2/event*`) |
| Channels | Create/manage broadcast channels | API-accessible (`/saas/channel*`) |
| File translation | Upload audio/video files for translation | API-accessible (Palabra API blob endpoint) |
| Streaming translation | Real-time speech-to-speech via WebSocket/WebRTC | API-accessible (Palabra API) |
| Billing/credits | Check credit balance | API-accessible (Palabra API) |
| CRM integration | Sync transcripts or meeting data to CRM | Not available — Talo has no CRM connector |
| Webhooks | Event-driven notifications | Not available — no webhook system |
| MCP server | Claude/Cursor integration | Not available |

## Pricing, limits & plan gates

### Talo meeting app

| Plan | Monthly | Annual | Minutes | Members | Extras |
|---|---|---|---|---|---|
| Starter | $33/mo | $33/mo ($396/yr) | 120/mo (1,140/yr annual) | 1 | 60 languages, voice settings |
| Pro | $100/mo | $80/mo ($960/yr) | 400/mo (4,800/yr annual) | 1 | + $0.25/extra min, custom logo (coming soon) |
| Team | $500/mo | $400/mo ($4,800/yr) | 400/mo (30,000/yr annual) | 5 | + $0.20/extra min, $100/extra seat, Slack support, SSO (coming soon) |
| Enterprise | Custom | Custom | Unlimited | Unlimited | SOC 2 compliance, dedicated support |

- 7-day free trial (no credit card required)
- Team plan is "coming soon" as of 2026-04
- Annual billing saves 20% on Pro and Team

### Palabra API / platform (separate pricing)

Palabra moved to a unified credit-subscription model. There is **no standalone "API" plan** — you buy a monthly plan (which grants a credit allowance) and spend credits across products (voice calls, events, streaming, and API). Plan tiers are now **Starter / Pro / Team / Business** (the old "Scale" tier is gone). Prices below are for the **Meetings & Presentations** product (verified 2026-06-13 at palabra.ai/pricing); the In-Person Events and Streaming products are sold as separate, higher-priced plans on the same page.

| Plan | Monthly | Annual (per mo) | Credits/mo | Key use |
|---|---|---|---|---|
| Starter | $60 | $45 | 150 | Individual creators, small teams |
| Pro (recommended) | $200 | $113 | 900 | Multi-seat workspace, SSO, audit logs |
| Team | $1,000 | $375 | 3,500 | Dedicated account manager, setup help |
| Business | Custom | Custom | Custom | SLA, priority support, regional deployment |

**Credit consumption rates (per hour, vary by tier — Starter/Pro/Team):**
- Voice calls (meetings): 30 / 25 / 20 credits/hr
- Offline (in-person) events: 150 / 130 / 100 credits/hr
- Broadcasting: 80 / 70 / 60 credits/hr
- API speech-to-speech: 30 / 25 / 20 credits/hr
- API translated captions: 10 / 7 / 5 credits/hr

Credits roll over monthly. Overage is billed per hour at tier-specific rates. No documented REST rate limits. No webhook support — streaming/event APIs only.

## Integrations

| Integration | Direction | Notes |
|---|---|---|
| Zoom | Bot joins meeting | Single bot translates all participants |
| Google Meet | Bot joins meeting | Same single-bot architecture |
| Microsoft Teams | Bot joins meeting | Requires guest access enabled in org |
| Palabra API → custom app | Embed translation | WebSocket/WebRTC streaming |
| Zapier/Make | Not available | No iPaaS connectors |
| CRM (HubSpot/Salesforce) | Not available | Pair with a dedicated note-taker |

## Data model

### Session (Palabra API)

```json
<!-- Constructed from OpenAPI spec — verify against live API -->
{
  "session_id": "sess_abc123",
  "status": "active",
  "source_lang": "EN",
  "target_langs": ["ES", "DE", "JA"],
  "created_at": "2026-04-24T10:00:00Z",
  "ttl": 3600
}
```

### Voice (Palabra API)

```json
<!-- Constructed from OpenAPI spec — verify against live API -->
{
  "voice_id": "voice_xyz789",
  "name": "My Cloned Voice",
  "status": "ready",
  "created_at": "2026-04-24T09:00:00Z"
}
```

### Glossary (Palabra API)

```json
<!-- Constructed from OpenAPI spec — verify against live API -->
{
  "glossary_id": "gloss_def456",
  "name": "Sales Terms",
  "type": "translation",
  "language_pair": {"source": "EN", "target": "ES"},
  "entry_count": 150,
  "created_at": "2026-04-24T08:00:00Z"
}
```

### Standard response envelope

```json
{
  "ok": true,
  "data": { ... }
}
```

Error response:
```json
{
  "ok": false,
  "errors": [
    {"error_code": 401, "detail": "Invalid credentials"}
  ]
}
```

## Quick-start recipes

### Recipe 1: Real-time microphone translation (Python SDK)

**Use case**: Translate your speech from English to Spanish in real-time during a call.

```bash
pip install palabra-ai
export PALABRA_CLIENT_ID=your_client_id
export PALABRA_CLIENT_SECRET=your_client_secret
```

```python
from palabra_ai import PalabraAI, Config, SourceLang, TargetLang, EN, ES, DeviceManager

palabra = PalabraAI()
dm = DeviceManager()
mic, speaker = dm.select_devices_interactive()
cfg = Config(SourceLang(EN, mic), [TargetLang(ES, speaker)])
palabra.run(cfg)
```

**Gotcha**: On macOS, you may need to run `pip install pip-system-certs` if you get SSL errors.

### Recipe 2: Translate an audio file to multiple languages

**Use case**: Take a recorded sales pitch and generate Spanish, French, and German versions.

```python
from palabra_ai import PalabraAI, Config, SourceLang, TargetLang, FileReader, FileWriter, EN, ES, FR, DE

palabra = PalabraAI()
config = Config(
    source=SourceLang(EN, FileReader("sales_pitch.mp3")),
    targets=[
        TargetLang(ES, FileWriter("pitch_spanish.wav")),
        TargetLang(FR, FileWriter("pitch_french.wav")),
        TargetLang(DE, FileWriter("pitch_german.wav")),
    ]
)
result = palabra.run(config)
print(f"Success: {result.ok}")
```

**Gotcha**: Input file must be 0.1-10 MB. Supported formats: MP3, AAC, WAV, WebM, MP4.

### Recipe 3: Create a custom glossary for industry terms (cURL)

**Use case**: Ensure "ARR" is translated as "Annual Recurring Revenue" not "arrangement" in Spanish.

```bash
# Step 1: Create glossary
curl -X POST https://api.palabra.ai/saas/glossary \
  -H "ClientID: $PALABRA_CLIENT_ID" \
  -H "ClientSecret: $PALABRA_CLIENT_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SaaS Sales Terms",
    "type": "translation",
    "source_lang": "EN",
    "target_lang": "ES"
  }'

# Step 2: Upload CSV with term pairs
# CSV format: source_term,target_term
# ARR,Ingresos Recurrentes Anuales
# MRR,Ingresos Mensuales Recurrentes
curl -X POST "https://api.palabra.ai/saas/glossary/{glossary_id}/upload" \
  -H "ClientID: $PALABRA_CLIENT_ID" \
  -H "ClientSecret: $PALABRA_CLIENT_SECRET" \
  -F "file=@saas_terms.csv"
```

**Gotcha**: Glossary types matter — `translation` overrides translation output, `asr` improves speech recognition, `asr_hot` boosts recognition for rare terms. Use `asr_hot` for product names.

## Integration patterns

### Pairing Talo with a note-taker for CRM sync

Talo translates but doesn't transcribe to CRM. Common architecture:

1. **Talo bot** joins the meeting for real-time translation
2. **Fathom/Fireflies/Sybill** also records for transcription + CRM sync
3. Both bots can coexist in the same Zoom/Meet/Teams call
4. Note-taker captures the translated audio (participants hear translated speech)

### Embedding Palabra API in a custom app

1. **Auth**: Set `PALABRA_CLIENT_ID` and `PALABRA_CLIENT_SECRET` environment variables
2. **Session**: Create via `POST /session-storage/session` — returns session config for WebRTC/WebSocket
3. **Connect**: Use WebRTC (browser/mobile) or WebSocket (server-side) to stream audio
4. **Translate**: Set source and target languages, publish audio, receive translated audio + text
5. **Voice clone** (optional): Clone a voice via `POST /saas/voice/clone`, use in translation for natural-sounding output

**Audio formats:**
- Input: Opus, PCM_S16LE, WAV
- Output: PCM_S16LE, ZLIB_PCM_S16LE

### Monitoring API usage

No webhooks available. Poll `GET /payments/v2/balance` to monitor credit consumption. Build a daily cron job to alert when credits drop below a threshold.
