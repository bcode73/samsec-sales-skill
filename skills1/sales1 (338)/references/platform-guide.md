# Meetily Platform Reference

## Platform overview

Meetily (Meetly AI) is an open-source, privacy-first AI meeting assistant that records, transcribes, and summarizes meetings with 100% local processing. Built by Zackriya Solutions, it positions itself as the self-hosted alternative to Otter.ai, Fireflies.ai, Granola, and Fathom. MIT licensed with 180K+ users and ~12.7K+ GitHub stars (verified 2026-06-13; latest release v0.4.0, 2026-06-05). Bot-free recording via system audio capture — no visible bot joins meetings.

**Target audience**: Privacy-conscious teams, healthcare/legal/financial/government orgs needing GDPR/HIPAA compliance, developers wanting extensibility, enterprises requiring self-hosted infrastructure.

## Key modules

### Transcription engine
- **Parakeet** (NVIDIA) — 4x faster than Whisper, English-focused; marked "Recommended" on Windows machines with NVIDIA GPUs
- **Whisper models** (OpenAI via Whisper.cpp) — tiny (~75 MB), base (~142 MB), small (~466 MB), medium (~1.5 GB), large-v3 (~3 GB). 95%+ accuracy for clear English audio. Multi-language support. (Model sizes verified 2026-06-13, meetily.ai/docs/features/pluggable-transcription)
- **Custom transcription server** — OpenAI-compatible provider can point at a self-hosted Whisper server (e.g. `http://localhost:8000` for Speaches / whisper.cpp / Faster Whisper Server / vLLM)
- Hardware acceleration: Apple Silicon Metal + CoreML on macOS, NVIDIA CUDA on Windows/Linux, AMD/Intel Vulkan
- Speaker diarization for multi-speaker meetings

### AI summarization
- **Built-in AI** — bundled local models (free); v0.4.0 added Qwen 3.5 built-in models and multi-language summaries
- **Ollama** — fully local LLM summarization (no internet required; default `http://localhost:11434`)
- **OpenAI** (GPT-4 / GPT-4o) — cloud summarization via API key
- **Claude** (Anthropic) — cloud summarization via API key
- **Groq** — fast cloud inference
- **OpenRouter** — access to multiple models
- **Custom Server (OpenAI-compatible endpoint)** — any server implementing `/v1/chat/completions` (LM Studio `:1234/v1`, Open WebUI `:3000/api/v1`, vLLM `:8000/v1`, Jan.ai `:1337/v1`, LocalAI `:8080/v1`). Endpoint URL must end in `/v1` or requests 404. **The Custom Server (OpenAI) provider requires Pro**; Ollama and Built-in AI are free. (Source: meetily.ai/docs/integrations/custom-apis, verified 2026-06-13)

### Audio capture
- Bot-free system audio recording (captures all meeting platforms)
- Simultaneous microphone + system audio with intelligent ducking
- Clipping prevention
- Works with: Zoom, Google Meet, Microsoft Teams, Discord, Slack Huddles, Webex, any audio source

### Audio/video import
- 10+ format support: MP4, WAV, MP3, FLAC, and more
- Drag-and-drop import with automatic chunked transcription
- Retranscription — re-process any meeting with a different provider, model, or language

### Summary templates
- Create, edit, duplicate, import, and export custom templates
- Customizable output structure

### Export
- Markdown, Word (DOCX), PDF, plain text
- Search and replace across transcripts and summaries

## Pricing and limits

| Plan | Price | Key features |
|---|---|---|
| Community | Free (MIT license) | Real-time transcription, audio/video import (10 formats), local AI processing, AI summaries, basic sharing (copy), community support |
| Pro | **$10/user/mo billed annually ($120/user/yr)** — **$25/user/mo billed monthly** | Enhanced-accuracy models, Custom Server (OpenAI-compatible) connector, custom summary templates (6 built-in + custom), auto-detect meetings, advanced exports (PDF/DOCX/MD), Windows GPU acceleration, hosted AI summaries, BYOK, priority email support, 1 year of access + all future updates |
| Enterprise | Custom (10+ user licenses) | Volume discounts, dedicated support, custom deployment help, all Pro features; SSO listed as roadmap |

14-day free Pro trial, no credit card required. Pro page also advertises a **30-day money-back guarantee** and "cancel anytime."

> **Pricing/feature note (verified 2026-06-13, meetily.ai/pricing + meetily.ai/pro):** The "$10/user/month" headline is the *annual* price (60% off the $25/month regular rate); month-to-month billing is **$25/user/month**. **Speaker identification, calendar integration, and "Chat with meetings" are marked "Coming Soon"/roadmap — NOT shipped Pro features** (speaker diarization was listed as planned for mid-June). Do not promise these as available today.

**Hardware requirements**:
- Minimum: 8GB RAM, 4-core CPU, 10GB storage, Node.js 18+, Python 3.10+, FFmpeg
- Recommended: 16GB RAM, 8-core CPU, 50GB storage, GPU acceleration, SSD

## Integrations

### Current
- LLM providers: Built-in AI, Ollama, OpenAI, Claude, Groq, OpenRouter, any OpenAI-compatible endpoint
- Export: Markdown, PDF, DOCX, plain text

### Planned / "Coming Soon" (not shipped yet)
- Speaker identification / diarization (marked "Coming Soon"; was listed as planned for mid-June)
- Calendar integration ("Coming Soon")
- Chat with meetings — AI-powered meeting insights/queries ("Coming Soon")
- SSO (Enterprise roadmap)
- Knowledge management: Obsidian, Notion, Confluence
- Communication: Slack, Teams, Discord
- CRM: Salesforce, HubSpot
- Project management: Jira, Asana, Monday.com
- RESTful API and webhook support for custom integrations

> Note (verified 2026-06-13): No CRM/iPaaS/webhook integrations are shipped. There is **no supported external REST API** (see Local API section below).

## Local API — DEPRECATED standalone FastAPI backend

> **IMPORTANT (verified 2026-06-13):** The standalone FastAPI backend is **deprecated/archived**. Per the repo's own `backend/API_DOCUMENTATION.md`: *"Meetily no longer supports the standalone FastAPI backend as the active application API."* The supported application is now the **Tauri desktop app**, where the Next.js UI talks to the **Rust core via Tauri commands and events** — there is no exposed HTTP API server for the current app. The archived FastAPI API was *"unauthenticated and had development-oriented CORS behavior. It must not be treated as a supported production API."*

**Legacy details (older 0.0.x builds only — do not rely on for current versions):**
- Legacy backend ran on `http://localhost:5167` (`APP_PORT`), with the Whisper server on port `8178` (`WHISPER_PORT`). Legacy endpoints included `POST /upload-transcript` (multipart) and `GET /get-summary`. Swagger was at `/docs`.
- **No cloud API and no supported external integration surface today.** All processing is on-device. For automation, the only practical path is reading the local SQLite store / exported files, not an HTTP API.

**What IS at a local URL today:** the *summarization* call goes OUT to a user-configured OpenAI-compatible endpoint (e.g. Ollama `http://localhost:11434`, vLLM `http://localhost:8000/v1`); and *pluggable transcription* can point at a custom server (e.g. `http://localhost:8000`). Those are servers **you** run, not Meetily's own API. (Source: meetily.ai/docs/integrations/custom-apis, meetily.ai/docs/features/pluggable-transcription)

## Tech stack

| Component | Technology |
|---|---|
| Framework | Tauri (desktop app) |
| Backend | Rust (45.4%) |
| Frontend | Next.js / TypeScript (29.7%) |
| AI processing | Python / FastAPI |
| Transcription | Whisper.cpp / NVIDIA Parakeet |
| Platforms | Windows (.exe), macOS (.dmg), Linux (Docker / source) |

## Deployment options

### Desktop (standard)
- Windows: Download x64-setup.exe from GitHub releases
- macOS: Install .dmg to Applications
- Linux: Build from source or Docker

### Self-hosted enterprise
- Docker containerization
- Deploy on Azure, AWS, GCP, or on-premises
- Admin dashboard for user management (Enterprise plan)
- European data residency available

### Build from source
- Requires Rust compiler, Node.js runtime, platform-specific build tools
- See `docs/BUILDING.md` in the repository

## Compliance

- GDPR compliant by architecture (data never leaves device)
- HIPAA ready (no cloud transmission)
- SOC 2 support available (Enterprise)
- ISO 27001 alignment (Enterprise)

## Workflow setup

### First meeting recording
1. Install Meetily from GitHub releases or meetily.ai
2. Wait for Parakeet Lightning model to download (required, ~500MB)
3. Select audio input device in Settings → Recordings → Default Audio Devices
4. Join your meeting on any platform (Zoom, Meet, Teams, etc.)
5. Click Record in Meetily — it captures system audio without joining as a bot
6. Click Stop when done — transcription processes locally
7. Configure summarization provider (Settings → Provider Configuration)
8. View AI summary, transcript, and preferences in the meeting details tabs

### Fully offline setup
1. Install Meetily
2. Download Whisper model of choice (for non-English or if Parakeet isn't sufficient)
3. Install Ollama and download a local LLM (e.g., llama3, mistral)
4. Set Ollama as the summarization provider in Meetily settings
5. Disconnect from internet — Meetily works fully offline after model downloads

### Batch transcription of existing recordings
1. Open Meetily
2. Drag and drop audio/video files (MP4, WAV, MP3, FLAC, etc.)
3. Files are automatically chunked and transcribed
4. Use Retranscription to re-process with a different model or language
