# Audionotes Platform Reference

## Overview

Audionotes is a multi-format AI note-taker that converts voice recordings, text, images, video files, and YouTube links into organized, structured notes with AI-generated summaries. It targets professionals, content creators, medical/legal practitioners, and students who want to capture ideas by voice and get polished output through 100+ customizable templates. Differentiator: broadest input format coverage (voice + text + image + video + YouTube) with WhatsApp Bot for mobile-first capture.

## Capabilities & automation surface

| Capability | Description | Access |
|---|---|---|
| Voice recording | Record voice memos with auto-language detection (80+ languages) | UI (iOS/Android/Web) |
| Transcription | Convert audio to text, 95% accuracy under optimal conditions, 30+ languages | UI |
| AI summaries | Auto-generate summaries highlighting key ideas and action points | UI |
| Speaker recognition | Identify different speakers in recordings | UI |
| Custom templates | 100+ prompt options for output formatting (meeting minutes, SOAP notes, blogs, emails) | UI |
| Mind maps | Generate visual mind maps from notes | UI (Pro) |
| Image notes | Extract text and context from uploaded images | UI (Pro) |
| YouTube video notes | Paste YouTube URL → transcript + AI notes | UI (Pro) |
| File uploads | Upload audio/video files for transcription (up to 6 hours/audio recording, 500 MB/file) | UI (Pro) |
| WhatsApp Bot | Send voice/files via WhatsApp for transcription and summaries | UI (Pro) |
| Chat with notes | Query note content via AI chat | UI |
| Organization | Folders, tags, bookmarks, filters, sorting | UI |
| Zapier automation | "New Note V2" trigger → route to 8,000+ apps | **Zapier** (Pro) |
| Notion sync | Auto-sync all notes (new + existing) to Notion workspace | **Notion API** (Pro) |
| Webhook | Push new note JSON to any endpoint | **Webhook** (Pro) |
| Export/share | Share via WhatsApp, Slack, email, LinkedIn, or public pages | UI |

**No public REST API.** All programmatic access is through webhooks (push-only), Zapier, or Notion sync.

## Pricing, limits & plan gates

| Feature | Free | Pro ($129.99/yr, ~$10.83/mo) |
|---|---|---|
| Voice recording | 1 min/note | Unlimited |
| File uploads | N/A | Unlimited (up to 6 hours/audio recording, 500 MB/file) |
| YouTube video notes | N/A | Unlimited |
| Image notes | N/A | Yes |
| Mind maps | N/A | Yes |
| Zapier | N/A | Yes |
| Notion sync | N/A | Yes |
| Webhook | N/A | Yes |
| WhatsApp Bot | N/A | Yes |
| Note chatting | N/A | Yes |

**Enterprise/Custom**: Available for teams of 5+ users — contact sales.

**Key gate**: All integrations (Zapier, Notion, webhook) require Pro. The free plan is effectively a trial with the 1-minute limit.

## Integrations

### Notion (bidirectional-ish — Audionotes → Notion, auto-sync)

**Setup**: Integrations sidebar → Connect Notion → duplicate the provided template into your workspace.

**Fields synced per note**:
- Title
- Transcript
- AI Notes / AI summary (content from template output)
- Created At (recording timestamp)
- Note Type (voice/text/image/video/youtube)
- Speaker Transcript
- Action items
- Tags

**Behavior**: Per-workspace auto-sync can be toggled so every new note pushes to Notion, or notes can be sent individually with a one-tap "Send to Notion" button on each entry. One-way (Audionotes → Notion), edits in Notion don't flow back. On disconnect, already-synced notes stay in Notion as normal pages (owned by your Notion workspace).

### Zapier

**Setup**: Integrations sidebar → Connect Zapier → authenticate with API key + email.

**Available trigger**: `New Note V2` — fires when a note finishes processing.

**Trigger fields available** (Zapier maps from the same note data as the webhook):
- Full transcript
- AI-generated summary
- Action items (where present)
- Tags
- Note duration
- Source metadata / source type (voice, upload, YouTube, or WhatsApp)
- Title, note ID, created-at timestamp

```json
{
  "noteId": "abc123",
  "createdAt": "2026-04-24T10:30:00Z",
  "noteType": "voice",
  "title": "Client meeting notes",
  "transcript": "Raw transcription text...",
  "content": "AI-generated summary/notes...",
  "actionItems": ["Follow up with client", "Send proposal"],
  "tags": ["client", "meeting"],
  "duration": 312
}
```
<!-- Core fields confirmed against live Zapier/webhook docs 2026-06-13; exact JSON key casing for actionItems/tags/duration not published — verify against a live delivery -->

**Common Zap recipes**:
- Audionotes → Google Sheets (log all notes)
- Audionotes → Slack (post summaries to a channel)
- Audionotes → Notion (alternative to native sync with more control)
- Audionotes → HubSpot (create activity note on contact)

### Webhook

**Setup**: Integrations sidebar → Webhook card → Connect → paste your public webhook URL → optionally add custom headers → send a test ping to verify.

**Payload** (JSON). Core fields:

```json
{
  "noteId": "string",
  "createdAt": "string (ISO 8601)",
  "noteType": "string",
  "title": "string",
  "transcript": "string",
  "content": "string"
}
```

Per the official webhook docs, the actual payload is more comprehensive — it also carries an **action items array**, **tags**, **source type** (voice / upload / YouTube / WhatsApp), and **recording duration in seconds**, plus the ISO 8601 `created_at` timestamp.
<!-- Core fields confirmed against live webhook docs 2026-06-13; exact JSON key names for the extra fields (action items / tags / source type / duration) are not published verbatim — verify against a live delivery -->

**Behavior**:
- Fires on every new note created after connection
- Historical notes are NOT retransmitted ("only notes created after connecting to webhooks will be sent")
- No HMAC / signature header. **Instead, each webhook can carry custom headers you specify** (e.g. an API key or bearer token) so your receiving server can verify the request came from Audionotes — set these in the Webhook card during setup.
- No retry/delivery guarantee documented

### WhatsApp Bot (Pro only)

Send voice messages, audio files, or text to the Audionotes WhatsApp Bot. It transcribes and creates notes in your account. Useful for mobile-first capture when the app isn't convenient.

## Data model

Audionotes has a simple, flat data model. Notes are the primary object:

```json
{
  "noteId": "unique-note-identifier",
  "createdAt": "2026-04-24T10:30:00Z (ISO 8601)",
  "noteType": "voice | text | image | video | youtube",
  "sourceType": "voice | upload | youtube | whatsapp",
  "title": "Auto-generated or user-set title",
  "transcript": "Raw transcription from audio/video, or extracted text from image",
  "content": "AI-generated output based on selected template",
  "actionItems": ["array of extracted action items"],
  "tags": ["array of tags"],
  "duration": "recording duration in seconds"
}
```
<!-- Core fields confirmed against live webhook docs 2026-06-13; extra-field key names (sourceType / actionItems / tags / duration) are documented as present but not published verbatim — verify against a live delivery -->

**Organization objects** (UI-only, not available via webhook/Zapier):
- **Folders**: Group notes by project or topic
- **Tags**: Label notes for filtering
- **Bookmarks**: Pin important notes

## Quick-start recipes

### Recipe 1: Voice notes → Notion knowledge base

**Trigger**: Record a voice note in Audionotes (any platform)
**Steps**:
1. Go to Integrations → Notion → Connect
2. Authorize Audionotes to access your Notion workspace
3. Duplicate the Audionotes template page into your target workspace
4. Record a voice note — it appears in Notion within seconds

**Gotcha**: All existing notes sync on first connection, which may flood your Notion workspace. Create a dedicated database first.

### Recipe 2: Voice notes → Slack channel via Zapier

**Trigger**: New Note V2 in Audionotes
**Steps**:
1. Create a Zap: Audionotes (trigger) → Slack (action)
2. Trigger: "New Note V2"
3. Action: "Send Channel Message" in Slack
4. Map fields: Title → message header, Content → message body
5. Test with a new voice recording

**Python equivalent using webhook**:

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
SLACK_WEBHOOK = "https://hooks.slack.com/services/T.../B.../xxx"

@app.route("/audionotes-webhook", methods=["POST"])
def handle_note():
    note = request.json
    slack_msg = {
        "text": f"*{note['title']}*\n{note['content']}"
    }
    requests.post(SLACK_WEBHOOK, json=slack_msg)
    return jsonify({"ok": True}), 200
```

**Gotcha**: No HMAC signature verification available, but you CAN attach a custom auth header (e.g. `Authorization: Bearer xxx`) in the Webhook config and validate it server-side — that's the recommended way to confirm the request came from Audionotes. IP allowlisting or a shared secret in a query parameter work as fallbacks.

### Recipe 3: Voice notes → HubSpot contact activity via webhook

**Trigger**: Webhook fires on new Audionotes note
**Steps**:
1. Set up webhook endpoint
2. Parse incoming JSON for `title`, `content`, `createdAt`
3. Match note to HubSpot contact (by keyword in title or a naming convention)
4. Create engagement/note via HubSpot API

```python
import requests

HUBSPOT_TOKEN = "pat-xxx"

def create_hubspot_note(contact_id: str, note_title: str, note_body: str):
    url = "https://api.hubapi.com/crm/v3/objects/notes"
    payload = {
        "properties": {
            "hs_note_body": f"<strong>{note_title}</strong><br>{note_body}",
            "hs_timestamp": "2026-04-24T10:30:00.000Z"
        },
        "associations": [{
            "to": {"id": contact_id},
            "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 202}]
        }]
    }
    resp = requests.post(url, json=payload, headers={
        "Authorization": f"Bearer {HUBSPOT_TOKEN}",
        "Content-Type": "application/json"
    })
    resp.raise_for_status()
    return resp.json()
```

**Gotcha**: Audionotes doesn't include contact identifiers in the payload — you must build your own matching logic (e.g., include client name in the note title and parse it).

## Integration patterns

### Webhook listener pattern

```
Audionotes (new note) → POST JSON → Your endpoint → Parse → Route to destination
```

**No HMAC signature** — but custom headers ARE supported: Unlike Fathom (Svix HMAC), Fireflies (`x-hub-signature`), or Circleback (HMAC-SHA256), Audionotes webhooks have no cryptographic signature. However, the Webhook card lets you attach **custom headers** (e.g. `Authorization: Bearer xxx` or an `X-Api-Key`), so the recommended way to verify the request came from Audionotes is to check for a known header value. Additionally protect your endpoint with:
- Require HTTPS
- Set a custom auth header in the Webhook config and validate it server-side (preferred)
- Add a shared secret as a query parameter (`?token=xxx`) as a fallback
- IP allowlisting if Audionotes publishes origin IPs
- Rate limiting to prevent abuse

### Zapier-first pattern (recommended for non-developers)

```
Audionotes → Zapier "New Note V2" → Filter (by noteType) → Action (CRM/Slack/Sheets)
```

Use Zapier's built-in Filter step to route different note types to different destinations (e.g., voice notes → Slack, meeting notes → CRM).

## Affiliate program

- **Commission**: 30% on upgrades
- **Network**: Lemon Squeezy
- **Signup**: https://audionotes.lemonsqueezy.com/affiliates (or https://affiliates.lemonsqueezy.com/programs/audionotes)
- **Cookie duration**: Not documented
