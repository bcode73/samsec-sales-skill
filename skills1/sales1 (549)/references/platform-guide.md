# Sonix Platform Reference

## Platform overview

Sonix is an AI-powered transcription, translation, and subtitling platform. It positions itself as "the world's most accurate automated transcription software" with 99% accuracy claims across 53+ languages. Unlike live meeting note-takers (Fathom, Fireflies, Otter), Sonix is upload-only — you submit audio/video files and get back transcripts, translations, and subtitles. Target audience: media producers, legal teams, researchers, podcasters, and enterprises needing batch transcription with compliance (SOC 2 Type 2, HIPAA).

## Key modules

### AI Transcription
- 53+ languages with speaker diarization
- Custom vocabulary/dictionary (Premium+) for domain-specific terms
- Verbatim transcription by default (includes filler words)
- Word-level timing in the output

### Automated Translation
- Neural machine translation across 53+ languages
- Translate from any transcribed language to any supported target
- Batch translation via API (`POST /media/{id}/translations`)

### Subtitles & Captions
- Auto-generated SRT and VTT files from transcriptions
- Video burn-in — embed subtitles directly into video files
- Frame-perfect timing synchronized with audio
- API: `POST /media/{id}/video_burn_ins`

### AI Analysis / AI workspace
- Summaries — auto-generated from transcript content
- Chapter markers — AI-detected topic boundaries
- Sentiment analysis — positive/negative/neutral per segment
- Batch folder-level summarization via API (`POST /folders/{id}/batch_summarizations`)
- Metered as "AI workspace hours" included on every subscription tier (Core 5/mo, Advanced 25/mo, Pro 100/mo)

### Sonix Editor
- In-browser editor where you edit text and audio stays in sync
- Speaker label management (merge, rename, reassign)
- Click any word to jump to that point in the audio
- Export to TXT, DOCX, PDF, SRT, VTT, JSON

### Collaboration
- Multi-user permissions (Premium+)
- Read-only sharing links
- Team folders for organizing projects
- Comments and annotations

### Sonix Recorder
- Mobile app for field recording
- Separate from the main transcription workflow

## Pricing and limits

Pricing was restructured in 2026 from the old Standard/Premium model into included-hours subscription tiers. Current plans (from sonix.ai/pricing):

| | Pay As You Go | Core | Advanced (Most Popular) | Pro | Enterprise |
|---|---|---|---|---|---|
| Price | $10/hr, no subscription | $25/mo ($275/yr) | $50/mo ($550/yr) | $80/mo ($880/yr) | Custom |
| Included transcription | pay per hr | 5 hrs/mo (60/yr) | 20 hrs/mo (240/yr) | 40 hrs/mo (480/yr) | Custom |
| Included AI workspace | — | 5 hrs/mo (60/yr) | 25 hrs/mo (300/yr) | 100 hrs/mo (1,200/yr) | Custom |
| Overage rate | n/a | $10/hr | $10/hr | $10/hr | Custom |
| Storage | 5 GB | 25 GB | 50 GB | 100 GB | 1 TB+ |
| Seats | single user | 1 (+$25/mo per seat) | 1 (+$25/mo per seat) | 1 (+$25/mo per seat) | unlimited |
| API access | No | Yes | Yes | Yes | Yes |
| Custom dictionary | No | Yes | Yes | Yes | Yes |
| Dashboard Webhooks | No | No | No | No (per-request `callback_url` works on all API plans) | Yes |
| SSO/SAML | No | No | No | No | Yes |
| Audit logs | No | No | No | No | Full |
| Support | self-serve | Email (48h) | Email + chat (12h) | Priority email + chat (4h) | Dedicated |
| Free trial | 30 min free, no credit card | — | — | — | — |

**Effective hourly rate on included hours**: Core ~$5/hr, Advanced ~$2.50/hr, Pro ~$2.00/hr. Overage on any subscription is billed at $10/hr (same as Pay As You Go).

**Cost math**: At a given monthly volume, pick the cheapest tier whose included hours cover it; overage is $10/hr so it never beats just buying the next tier up. Example: 20 hrs/mo fits Advanced ($50, all 20 hrs included) — cheaper than Pay As You Go ($200) and far cheaper than Core ($25 + 15 overage hrs × $10 = $175).

**Plan-gated features to watch:**
- API access: any paid subscription (Core/Advanced/Pro/Enterprise). NOT available on Pay-As-You-Go. Error 403 message: "upgrade to Core or higher."
- Custom dictionary: included on all subscription tiers (Core and up).
- AI workspace (summaries/chapters/sentiment): metered hours included on each subscription tier; consumes the AI-workspace allowance.
- Per-request completion callback (`callback_url` on POST /media): works on ALL API plans — you do NOT need Enterprise to be notified on transcript completion.
- Dashboard Webhooks (workspace event subscriptions), SSO/SAML, full audit logs: Enterprise only.

## Integrations

### Video conferencing (11)
Zoom, Microsoft Teams, Google Meet, Cisco Webex, GoToMeeting, Skype, RingCentral, UberConference, Join.me, BlueJeans, Loom — these are file import integrations, not live join. You import recordings from these platforms into Sonix.

### Cloud storage (4)
Dropbox, Google Drive, OneDrive, Box — upload files directly from cloud storage

### CRM
Salesforce — native integration

### Automation
Zapier — triggers on transcript completion, actions to submit media. Connects to 5,000+ apps.

### Media production (4)
Adobe Premiere Pro, Final Cut Pro X, Adobe Audition, Avid Media Composer — export transcripts in compatible formats

### Research / QDA (3)
Atlas.ti, NVivo, MaxQDA — qualitative data analysis tools

### Legal (2)
Clio, Relativity — legal practice management and eDiscovery

## Data model (API)

Key objects in the Sonix API:

- **Media** — the core object. Represents an uploaded audio/video file with its transcript.
  - `id` (string) — unique identifier
  - `name` (string) — file name
  - `status` (string) — processing status
  - `language` (string) — transcript language code
  - `duration` (float) — media duration in seconds
  - `created_at` (datetime) — upload timestamp

- **Transcript** — retrieved via `GET /media/{id}/transcript` in multiple formats (text, SRT, VTT, JSON, Avid DS)

- **Translation** — a translated version of a transcript
  - `language` (string) — target language code
  - `status` (string) — translation processing status

- **Summarization** — AI-generated summary, chapters, or sentiment
  - `type` (string) — summary, chapters, or sentiment

- **Folder** — organizational container for media files

- **User** — workspace member with permissions

- **Share** — sharing configuration for a media file

## Workflow setup

### Basic transcription workflow
1. Upload file via web UI or `POST /media` API endpoint
2. Wait for processing (typically minutes for audio, longer for video)
3. Review transcript in the Sonix editor
4. Fix speaker labels (merge duplicates, rename)
5. Export in desired format (TXT, DOCX, SRT, VTT, JSON)

### Translation workflow
1. Complete transcription first
2. Select target language(s)
3. Request translation via UI or `POST /media/{id}/translations`
4. Review translated transcript
5. Export translated version

### Subtitle burn-in workflow
1. Upload video file and transcribe
2. Review and correct transcript (corrections carry into subtitles)
3. Generate SRT/VTT or request video burn-in
4. For burn-in: `POST /media/{id}/video_burn_ins` — Sonix embeds subtitles into the video file
5. Download the subtitled video

### API pipeline workflow
1. Obtain API key from `https://my.sonix.ai/api` (any paid subscription works — Core and up; Pay-As-You-Go and trials cannot use the API, trial users must email support)
2. Submit media: `POST /media` with file upload (100 MB max) or `file_url`. Pass `callback_url` so Sonix POSTs you on completion instead of polling
3. If not using `callback_url`, poll `GET /media/{id}` for processing status (`preparing` → `transcribing` → `completed`)
4. Retrieve transcript: `GET /media/{id}/transcript.json` (or `.srt`/`.vtt`/`?format=avid_ds`)
5. Optionally request translation: `POST /media/{id}/translations`
6. Optionally request summarization: `POST /media/{id}/summarizations`

### MCP (LLM client) access
Sonix runs an MCP server at `https://api.sonix.ai/mcp` (OAuth 2.1, separate auth from REST keys) exposing read-only tools `list_media`, `read_transcript`, `export_transcript`, `get_account_info` — let Claude/Cursor/Codex read your media library and transcripts without building a pipeline.

## Deep dives

### Accuracy optimization
- **Audio quality is #1 factor.** Clean audio with minimal background noise produces dramatically better results.
- **Custom dictionary** (Premium+): Add company names, product terms, acronyms, and domain jargon. This improves recognition of specialized vocabulary.
- **Language selection**: Explicitly set the correct language — don't rely on auto-detect for best results.
- **Speaker count**: Sonix handles 2-4 speakers well. Beyond 5-6 speakers, diarization accuracy drops.

### Security & compliance
- SOC 2 Type 2 certified
- HIPAA compliant (Enterprise with BAA)
- Encrypted storage (at rest and in transit)
- Audit logs (Enterprise only)
- Data retention configurable
- PHI detection capabilities

### Sonix vs live meeting tools
Sonix is **not** a meeting note-taker. It does not:
- Join meetings live
- Provide real-time transcription
- Integrate with calendar for auto-recording
- Offer coaching or conversation intelligence features

For live meeting recording, use Fathom, Fireflies, Otter, or other tools covered in `/sales-note-taker`. Sonix is best as a post-recording transcription engine for media files, interviews, legal recordings, and content production.
