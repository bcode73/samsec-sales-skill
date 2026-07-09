# Transkriptor Platform Reference

## Platform overview

Transkriptor is an AI-powered transcription platform claiming 99%+ accuracy across 100+ languages with dialect detection. It offers both batch file transcription (upload audio/video) and live meeting recording via bot (Zoom, Google Meet, Microsoft Teams). Target audience ranges from individual content creators and students (50% education discount) to mid-market teams needing multilingual transcription with speaker analytics. Differentiators: broad language coverage (100+), built-in subtitle generation, AI chat for querying transcripts, knowledge base creation from multiple files, and sentiment analysis on Team plan.

**Parent company**: Also operates Speaktor (text-to-speech) and Eskritor (AI writing) as sister products under the same umbrella.

## Key modules

### Transcription engine
- **Batch upload**: Drag-and-drop audio/video files for transcription
- **Meeting bot**: Auto-joins Zoom/Google Meet/Teams via calendar sync
- **URL transcription**: Transcribe from YouTube, Google Drive, Dropbox, OneDrive URLs
- **Languages**: 100+ with dialect detection
- **Speaker diarization**: Multi-speaker identification (accuracy varies — weaker than competitors for overlapping speech)
- **Custom vocabulary**: Add domain terms, acronyms, proper nouns (paid plans, via app or API)

### AI features
- **Summaries**: AI-generated meeting summaries and action items
- **Sentiment analysis**: Conversation tone detection (Team plan only)
- **AI Chat**: Query transcribed content in natural language
- **Knowledge base**: Combine multiple transcripts into a searchable knowledge base
- **Meeting templates**: Pre-built templates for sales, marketing, education, and custom

### Subtitle/caption generation
- **Formats**: SRT, VTT
- **Languages**: Same 100+ language coverage
- **Subtitle service parameter**: Use `service: "Subtitle"` in API calls for optimized subtitle output

### Editor
- Built-in transcript editor for corrections
- Speaker label editing
- Timestamp-aligned editing

### Integrations
- **Meeting platforms**: Zoom, Google Meet, Microsoft Teams (via bot auto-join)
- **Storage**: Google Drive, Dropbox, OneDrive, SharePoint
- **Productivity**: Notion, Google Docs, OneNote, Slack, Gmail, Outlook, Trello
- **CRM**: HubSpot, Salesforce, Zoho (listed — depth of integration is disputed in reviews; verify before relying on CRM field-mapping)
- **Automation**: Zapier (8,000+ apps), Make (community integration)
- **Export**: PDF, SRT, TXT, DOCX

## Pricing and limits

| Plan | Monthly | Annual | Minutes/mo | Key gates |
|---|---|---|---|---|
| Lite | $9.99/mo | — | 300 | Basic transcription, editing, translation |
| Pro | $19.99/mo | $99.99/yr ($8.33/mo) | 2,400 | Calendar sync, meeting recording, summary templates, AI knowledge base, workspaces |
| Team | $30/seat/mo | $240/seat/yr ($20/seat/mo) | 3,000/seat | Speaker analysis, sentiment detection, advanced analytics, role-based access, custom bot branding |
| Enterprise | Custom | Custom | Custom | Individual/custom API documentation, custom development, system integration, priority support, advanced security (which exact tier first unlocks API access is not stated in official docs — unverified) |

**Bulk plans** (for high-volume transcription):
| Hours | Monthly | Annual (50% off) |
|---|---|---|
| 100 hrs | $60/mo | $30/mo |
| 250 hrs | $150/mo | $75/mo |
| 500 hrs | $300/mo | $150/mo |
| 1,000 hrs | $600/mo | $300/mo |

**Other notes**:
- **Free tier**: pricing page lists a "Free — 90 Minutes" option (surfaced when downgrading)
- **Education discount**: 50% off all plans for students
- **Unused minutes do NOT roll over** — monthly allotments reset each billing cycle
- **API**: requires a paid subscription. The official docs and pricing page do NOT state a specific tier (Enterprise-only is unverified); confirm API availability in-app for your plan

## Data model (API — paid plan)

**Key objects**:
- **File** (transcription result): Contains `order_id`, a `content` array of segments with `text`, `StartTime`, `EndTime`, `VoiceStart`, `VoiceEnd` (all in milliseconds), and `Speaker` (e.g., `SPK_1`)
- **Folder**: Organizational container for files
- **Meeting**: Scheduled or ad-hoc meeting recording
- **Custom vocabulary**: User-defined terms for improved recognition
- **Webhook**: Event subscription for async notifications

**Relationships**: Files belong to folders. Meetings produce files. Webhooks subscribe to file/meeting events.

## Workflow setup

### Workflow 1: Meeting recording via bot
1. Connect calendar in Settings → Calendar Sync (Google Calendar or Outlook)
2. Transkriptor bot auto-joins meetings with recognized meeting links
3. After meeting ends, transcript + AI summary appear in dashboard
4. Optionally configure meeting templates (sales, marketing, custom) for structured summaries
5. Export or push to connected apps (Notion, Slack, Google Docs)

### Workflow 2: Batch file transcription
1. Upload audio/video file(s) via drag-and-drop or URL (YouTube/GDrive/Dropbox/OneDrive)
2. Select language (or use auto-detect)
3. Wait for processing (time depends on file length)
4. Review and edit transcript in built-in editor
5. Export as PDF, SRT, TXT, or DOCX

### Workflow 3: API pipeline (paid plan; exact gating tier unverified)
1. Get API key from https://app.transkriptor.com/account
2. Get upload URL: `POST /transcription/local_file/get_upload_url` with `file_name`
3. Upload file: `PUT {returned upload_url}` with binary body
4. Start transcription: `POST /transcription/local_file/initiate_transcription` with `url` (the returned `public_url`), `language` (ISO, e.g. `en-US`, required), `service` (Standard/Subtitle, required), optional `folder_id` and `triggering_word`
5. Poll or use webhook for completion
6. Fetch result: `GET /files/{order_id}/content`
7. Export: `POST /files/{order_id}/content/export` with `export_type` (txt/srt/pdf/docx) and options

## Deep dives

### Custom vocabulary setup
Custom vocabulary improves accuracy for domain-specific terms. Available on paid plans.

**Via app**: Settings → Custom Vocabulary → Add terms one by one or in bulk
**Via API** (paid plan):
- Set: `POST /custom_vocabulary` with a `words` array (max 1,000 items, up to 6 words per phrase)
- Get: `GET /custom_vocabulary`
- Delete: `DELETE /custom_vocabulary`

Tips:
- Add company names, product names, acronyms, and technical terms
- Include proper nouns that the generic model consistently misses
- Does NOT apply retroactively — only improves future transcriptions
- Test with a sample file after adding vocabulary to verify improvement

### Speaker recognition
- Transkriptor auto-detects speakers and assigns labels (segments carry `Speaker` identifiers like `SPK_1`)
- You can rename speakers after transcription in the editor
- API: speaker recognition is managed via speaker profiles under `annotations/profiles` (create a profile from an audio sample or from an existing transcription); there is no single `recognize_speakers` re-run endpoint
- **Known limitation**: Accuracy drops significantly with overlapping speech or similar-sounding voices

### Webhook integration (API; paid plan)
- Create: `POST /integrations/webhooks` with `url` and formatting options (`export_format` Txt/Json/Csv, `include_timestamps`, `include_speaker_names`, `merge_same_speaker_segments`, `is_single_paragraph`, `paragraph_size`, `folder_id`)
- View/List: `GET /integrations/webhooks` (optional `webhookType` query param for one webhook)
- Update: `PUT /integrations/webhooks` (the `webhookType` field in the body identifies the webhook — no ID in the path)
- Delete: `DELETE /integrations/webhooks?webhookType={id}`
- Webhooks fire when a transcription completes and POST the formatted transcript to your URL. No discrete event-type names are listed and **no HMAC/signature header is documented** — verify delivery another way (IP allowlist, secret in URL).

### Affiliate program
- 30% lifetime recurring commission
- URL: https://transkriptor.com/affiliate/
- Monthly payouts via Stripe or Paddle
- Real-time tracking dashboard
- Open to anyone (bloggers, influencers, marketers)
