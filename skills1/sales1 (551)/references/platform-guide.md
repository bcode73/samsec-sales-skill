# Soz AI Platform Reference

## Platform overview

Soz AI is a mobile-first AI transcription and note-taking platform that converts audio and video into text in 100+ languages. It targets individual professionals — journalists, lawyers, psychologists, sales managers, consultants, doctors — who need affordable, high-volume transcription on the go. Key differentiators: YouTube URL paste transcription, a low-cost Premium plan (now **$3.99/week**; see Pricing), speaker diarization with automatic speaker labels, and mobile-native apps (iOS, Android; a Chrome extension is marked "Coming Soon" as of 2026-06-13). The about/marketing pages currently state "enterprise-grade security, GDPR compliance, and end-to-end encryption" and that data is never shared, sold, or used to train AI; the older CCPA/HIPAA/AES-256/99.9% SLA claims are not re-confirmed on the current pages (see Security and compliance).

## Key modules

### Audio-to-Text Transcription
- Upload all major audio/video formats — MP3, WAV, M4A, AAC, FLAC, OGG, MP4, MOV, AVI and more (up to 500MB)
- Live recording with real-time processing
- 100+ languages with automatic language detection
- 95-99% accuracy depending on audio quality and conditions
- Word-level timestamps for precise navigation
- 10x faster than real-time processing

### AI Note Taker
- Automatic topic segmentation with section headers
- Key point extraction and hierarchical organization
- Action item identification and formatting
- Decision tracking and highlighting
- Searchable archive across all notes

### Speaker Diarization
- Automatically identifies and labels different speakers (current pages, 2026-06-13, no longer state a specific count; an earlier capture cited "up to 10" — treat the cap as unconfirmed)
- Timestamps per speaker segment
- Best accuracy with 2-5 speakers in clear audio conditions

### YouTube Transcript
- Direct YouTube URL paste — no manual download needed
- Automatic language detection
- LeMUR-powered AI summaries included
- Free tool available at sozai.app

### Subtitle Generator
- SRT and VTT format output
- Multi-language subtitle generation
- Free SRT validator, VTT-to-SRT converter, subtitle time-shift tools

### Voice Translator
- Real-time translation across 50+ languages
- Context-aware translations maintaining meaning

### AI Writer
- Generate summaries from transcriptions
- Content creation from transcript material

### Offline Recording
- Record audio without internet connection
- Sync and transcribe when reconnected
- Audio-synchronized editing capability

## Pricing and limits

> **Re-verified 2026-06-13 against sozai.app/pricing.** The Premium card now shows **$3.99/week** (NOT the older $9.99/mo). The card labels it "Unlimited transcription," but the pricing-page FAQ contradicts that: "Premium gives you **300 minutes of transcription per month**." When the cap is hit, "Premium users can continue transcribing up to their 300-minute monthly limit." So treat Premium as a 300 min/month plan, not truly unlimited. (Some Soz AI comparison/alternatives marketing pages still cite the legacy $9.99/mo "unlimited" figure — the /pricing page is authoritative.) Billing is weekly only — no monthly/annual option is shown, and it runs through the App Store / Google Play.

| Feature | Free ($0/mo) | Premium ($3.99/week) |
|---|---|---|
| Transcription minutes | 30 min / month | 300 min / month (card says "unlimited"; FAQ caps at 300) |
| Languages | 100+ | 100+ |
| Speaker diarization (speaker labels) | Yes | Yes |
| AI summaries (LeMUR) | Yes | Yes |
| Priority processing | No | Yes |
| YouTube transcription | Yes | Yes |
| Subtitle generation (SRT/VTT) | Yes | Yes |
| File upload size | Up to 500MB | Up to 500MB |

- No credit card required for free tier
- When the limit is hit, free users wait until the next month for minutes to reset; Premium users transcribe up to the 300-min monthly cap
- No team/enterprise plans yet — FAQ: "Not yet, but we are working on team plans. Contact us on Telegram for volume pricing or custom needs." Individual-focused pricing, no per-seat fee.

## Integrations

| Integration | Method | Notes |
|---|---|---|
| YouTube | Native URL paste | Direct transcription from YouTube URLs |
| SRT/VTT export | File export | Subtitle files for video editing |
| Audio/video upload | File upload | MP3, WAV, M4A, AAC, FLAC, OGG, MP4, MOV, AVI and more, up to 500MB |
| Auto-export to cloud | Marketing-stated | The YouTube-transcription page advertises "Auto-export to Google Drive, Dropbox, or CMS" and a "batch queue system for overnight processing" — no setup docs published |

### REST API — advertised but undocumented (re-verified 2026-06-13)

As of 2026-06-13, the YouTube-transcription marketing page (sozai.app/transcribe-youtube-videos) states verbatim: **"Connect SozAI to your workflow with our REST API. Automate transcription for new uploads, scheduled content, or trending videos."** This reverses the prior "no public API" position as a *marketing claim*.

However, **no developer documentation exists**: there is no published base URL, no authentication scheme, no endpoint list, no rate limits, and no webhook documentation anywhere on sozai.app (the /pricing, /, /about, and /tools pages do not mention an API). Treat the REST API as *announced/advertised but not documented or independently verifiable*. For any real programmatic pipeline you still cannot wire against published Soz AI endpoints today — contact Soz AI (Telegram) for API access, or use an API-first platform via `/sales-note-taker`.

**Not supported / not documented**: Salesforce, HubSpot, Pipedrive, Zapier, Make, n8n, Slack, Notion, or any native CRM connector. No documented webhooks. The REST API is advertised but has no public docs.

## Data model

A REST API is advertised (see Integrations) but undocumented as of 2026-06-13 — no published object schema. The data model below reflects what is visible in the app UI:

- **Recording**: Audio file + metadata (date, duration, language)
- **Transcript**: Full text with word-level timestamps and speaker labels
- **Summary**: LeMUR-powered AI-generated summary
- **Action items**: Extracted tasks from conversation
- **Notes**: Hierarchical AI-organized notes with topic segmentation
- **Subtitles**: SRT/VTT formatted subtitle files

## Workflow setup

### Initial setup
1. Download Soz AI from App Store (iOS) or Google Play (Android). (A Chrome extension is advertised but marked "Coming Soon" as of 2026-06-13; the older macOS/Chrome availability is not confirmed on the current download pages.)
2. Create an account — 30 free minutes per month included
3. Grant microphone permission when prompted

### Recording a meeting
1. Open Soz AI and tap record
2. Place device centrally among speakers for best pickup
3. Recording transcribes in real-time or after completion
4. AI generates summary, action items, and topic segmentation automatically
5. Export transcript or subtitles as needed

### YouTube transcription
1. Copy the YouTube video URL
2. Paste into Soz AI's YouTube Transcript tool
3. AI processes the video and generates transcript with timestamps
4. Review, edit, and export as needed

### Subtitle generation
1. Upload audio/video file or use a recording
2. AI generates transcript with timestamps
3. Export as SRT or VTT format
4. Use free tools (SRT validator, time-shift) to adjust if needed

## Security and compliance

> Re-verified 2026-06-13: the current about/marketing pages state "enterprise-grade security, GDPR compliance, and end-to-end encryption," and that "Your data belongs to you. We never share, sell, or use your content for training." The specific AES-256 / TLS 1.3 / CCPA / HIPAA / 99.9%-SLA claims below were captured in earlier research and are NOT re-confirmed on the current public pages — verify directly before relying on them for a compliance-sensitive use case.

- **Encryption**: "end-to-end encryption" stated; earlier capture cited TLS 1.3 in transit + AES-256 at rest (unconfirmed 2026-06-13)
- **GDPR**: stated ("GDPR compliance")
- **CCPA**: earlier capture, unconfirmed on current pages
- **HIPAA**: earlier capture, unconfirmed on current pages
- **Data control**: Users can permanently delete all data at any time
- **AI training**: Content is never shared, sold, or used to train AI without explicit permission
- **Uptime**: 99.9% SLA — earlier capture, unconfirmed (current pages mention "24/7 Support")

## Deep dives

### Language support
100+ languages with automatic detection. Can transcribe multilingual conversations and translate between languages while maintaining context. Best accuracy on major world languages (English, Spanish, French, German, Mandarin, Japanese, Korean, Hindi, Arabic, Portuguese). Less common languages may have lower accuracy.

### Mobile-first design philosophy
Unlike desktop-centric tools (Otter, Fireflies, Fathom), Soz AI is built mobile-first for iOS and Android. This means:
- Optimized for phone microphone recording (in-person meetings, interviews, lectures)
- Touch-friendly interface for on-the-go use
- Offline recording capability
- Lower barrier to entry than bot-based meeting assistants

Trade-off: no meeting bot integration (Zoom/Teams/Meet), no real-time live transcription during video calls, no CRM sync.

### Comparison positioning
| Capability | Soz AI | Otter.ai | Transkriptor | Fathom |
|---|---|---|---|---|
| Paid price | $3.99/week (300 min/mo) | $17-30/mo | $9.99/mo (tiered) | $16-20/mo |
| Languages | 100+ | 18 | 100+ | 38 |
| YouTube URL paste | Yes | No | No | No |
| Mobile-first | Yes | Partial | No (web-first) | No (desktop-first) |
| Meeting bot | No | Yes | Yes | Yes |
| CRM integration | None | Thin | Shallow | Medium |
| API | Advertised, undocumented | Enterprise beta | Enterprise only | REST + webhooks |
| Speaker diarization | Yes (speaker labels) | Yes | Yes | Yes |
| Free tier | 30 min/mo | Yes (limited) | ~30 min/day | Unlimited recordings |
