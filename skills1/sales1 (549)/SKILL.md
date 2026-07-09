---
name: sales-sonix
description: "Sonix platform help — AI transcription, translation, and subtitling in 53+ languages with SOC 2 / HIPAA compliance. Use when uploading audio or video files for batch transcription, translating transcripts into multiple languages, generating SRT/VTT subtitles or burning captions into video, integrating Sonix REST API into a transcript pipeline, troubleshooting speaker diarization errors, comparing Sonix vs Otter vs Trint vs Rev for media transcription, choosing between Pay-As-You-Go and the Core/Advanced/Pro subscription tiers, or debugging upload failures and slow processing. Do NOT use for live meeting recording or real-time transcription (Sonix is upload-only — use /sales-note-taker for live meeting tools)."
argument-hint: "[describe what you need help with in Sonix]"
license: MIT
version: 1.0.0
tags: [sales, transcription, translation, subtitles, platform]
---

# Sonix Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What's your primary goal?**
   - A) Transcribe audio/video files (batch transcription)
   - B) Translate existing transcripts into other languages
   - C) Generate subtitles/captions for video
   - D) Integrate Sonix API into a pipeline
   - E) Compare Sonix to alternatives for my use case
   - F) Troubleshoot a specific issue (upload, accuracy, speaker labels)

2. **What type of content are you transcribing?**
   - A) Meetings / calls
   - B) Interviews / podcasts
   - C) Legal / compliance recordings
   - D) Media production (film, TV, marketing videos)
   - E) Research / academic
   - F) Mixed / high volume

3. **What plan are you on (or considering)?**
   - A) Free trial (30 min)
   - B) Pay As You Go ($10/hr, no subscription — no API)
   - C) Core ($25/mo, 5 hrs) / Advanced ($50/mo, 20 hrs) / Pro ($80/mo, 40 hrs) — subscription tiers, API included
   - D) Enterprise (custom — SSO, audit logs, dashboard webhooks, HIPAA BAA)
   - E) Not sure yet

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Choosing a live meeting recorder or note-taker | `/sales-note-taker {user's question}` |
| Building a coaching program from call recordings | `/sales-coaching {user's question}` |
| General CRM-to-tool integration (Zapier, webhooks, iPaaS) | `/sales-integration {user's question}` |
| Email deliverability or outbound sequences | `/sales-deliverability {user's question}` |

When routing, provide the exact command: "This is a {problem domain} question — run: `/sales-{skill} {user's original question}`"

Otherwise, answer directly below.

## Step 3 — Sonix platform reference

**Read `references/platform-guide.md`** for the full platform reference — modules, pricing, integrations, data model, workflows.

If the question involves the API, also read `references/sonix-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

You no longer need the platform guide — focus on the user's specific situation.

**Plan selection framework (2026 pricing):**
- **One-off or infrequent transcription, no API** → Pay As You Go ($10/hr, no subscription)
- **Need the API or custom dictionary, low volume** → Core ($25/mo, 5 hrs included)
- **Regular volume (~20 hrs/mo)** → Advanced ($50/mo, 20 hrs included) — Most Popular
- **Heavy volume (~40 hrs/mo) or lots of AI summaries** → Pro ($80/mo, 40 hrs transcription + 100 AI-workspace hrs)
- **Team with compliance needs (SSO, audit logs, dashboard webhooks, HIPAA BAA)** → Enterprise
- **Key gates**: API access starts at Core (any paid subscription); Pay-As-You-Go has NO API. Overage on any subscription is $10/hr, so pick the tier whose included hours cover your volume.

**Accuracy optimization:**
1. Upload the highest quality audio possible (minimize background noise)
2. Use custom dictionary (any subscription tier) for domain-specific terms
3. Review and correct speaker labels immediately after transcription
4. Use the in-browser editor for corrections — edits sync with audio timestamps

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research — review these, especially items about plan-gated features and integration gotchas that may be outdated.*

- **No live/real-time transcription.** Sonix is upload-only — you must upload a recorded file. It does not join meetings or capture audio live. For live transcription, use Fathom, Fireflies, or Otter.
- **API requires a paid subscription (Core and up).** Pay-As-You-Go users cannot access the API — the 403 error says "upgrade to Core or higher." Any subscription tier (Core $25/mo, Advanced, Pro, Enterprise) unlocks it; you do NOT need a top tier.
- **Two different "webhook" mechanisms.** Per-request `callback_url` on `POST /media` (Sonix POSTs you on completion) works on ALL API plans — no polling needed. The separate dashboard Webhooks (workspace event subscriptions: Transcription/Translation finished, Label/Folder change, HMAC-SHA256 signed via `X-Webhook-Signature`) are Enterprise-only. Don't conflate them.
- **Speaker diarization is imperfect.** Multiple speakers may be split into extra labels or merged. Review speaker labels after every transcription and merge/rename in the editor.
- **Custom dictionary is on every subscription tier.** Included on Core and up; only Pay-As-You-Go lacks it.
- **AI workspace hours are metered per tier.** Summaries, chapters, and sentiment consume the included AI-workspace allowance (Core 5/mo, Advanced 25/mo, Pro 100/mo); overage is billed.
- **Upload size limit is 100 MB direct.** For larger files, use a URL upload (no size limit). Slow uploads are usually caused by file size — compress or convert to a smaller format first.
- **Hybrid pricing can be confusing.** Premium charges both a per-seat monthly fee AND a per-hour transcription fee. Calculate total cost for your volume before committing.
- **No mobile app for recording.** Sonix Recorder exists but is separate from the main transcription workflow. Sonix is primarily a post-recording processing tool.

## Related skills

- `/sales-note-taker` — Comparing AI meeting note-takers and conversation intelligence platforms (Fathom, Fireflies, Gong, etc.). Sonix is a backend transcription option, not a live meeting tool.
- `/sales-integration` — General tool integration patterns (Zapier, webhooks, iPaaS)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`

## Examples

### Example 1: Choosing Sonix vs Otter for podcast transcription
**User says**: "I produce a weekly podcast and need accurate transcripts in English and Spanish. Should I use Sonix or Otter?"
**Skill does**:
1. Notes Sonix handles file uploads with translation to 53+ languages — upload the recording, get English transcript, then translate to Spanish
2. Compares: Otter is better for live recording but weaker on translation; Sonix is better for post-production with multi-language needs
3. Recommends Pay-As-You-Go ($10/hr) for occasional use, or a subscription tier (Core/Advanced/Pro) if the user needs API automation or regular volume
**Result**: Clear recommendation based on the podcast workflow with translation needs.

### Example 2: Building a Sonix API pipeline
**User says**: "I want to auto-transcribe every sales call recording from our S3 bucket using the Sonix API."
**Skill does**:
1. Reads the API reference for endpoint details
2. Sketches the pipeline: S3 event → Lambda → `POST /media` with S3 presigned URL + `callback_url` → Sonix POSTs the Lambda on completion → `GET /media/{id}/transcript.json` → write to warehouse
3. Notes API needs any paid subscription (Core+; Pay-As-You-Go has none), Bearer token auth, 100 MB direct upload limit (use `file_url` for larger files)
4. Recommends the per-request `callback_url` parameter for completion notification (works on all API plans) instead of polling `GET /media/{id}`
**Result**: Working pipeline architecture with Sonix-specific constraints.

### Example 3: Speaker labels wrong after transcription
**User says**: "Sonix keeps labeling my speakers wrong — it shows 7 speakers when there were only 3 in the meeting."
**Skill does**:
1. Explains this is the most common Sonix complaint — the AI over-segments speakers, especially with similar voices or audio quality issues
2. Recommends: merge duplicate speakers in the editor, rename to real names, upload higher quality audio next time
3. Notes custom dictionary (Premium) can help with names but won't fix diarization directly
**Result**: Practical fix for the immediate issue plus prevention tips.

## Troubleshooting

### Speaker diarization creates too many speakers
**Symptom**: Sonix labels 5-7 speakers when the recording only had 2-3
**Cause**: Similar voices, cross-talk, or poor audio quality cause the AI to split one speaker into multiple labels
**Solution**: After transcription, use the editor to merge duplicate speaker labels. Upload the highest quality audio possible. If recording via conference call, ensure each participant has a separate audio channel if possible.

### Upload fails or takes hours
**Symptom**: File upload hangs, times out, or takes 2+ hours for a 30-minute recording
**Cause**: Large file size (>100 MB) or slow connection
**Solution**: Compress the file (convert video to audio-only MP3/M4A, reduce bitrate). For files over 100 MB, use URL upload instead of direct upload — host on S3/Google Drive and provide the URL. Check the Sonix status page for service issues.

### Transcript has excessive filler words and wrong punctuation
**Symptom**: "Um", "uh", "like" appear everywhere; sentences run together or break in wrong places
**Cause**: Sonix transcribes verbatim by default, including hesitations; punctuation AI struggles with conversational speech
**Solution**: Use the Sonix editor's clean-up tools to remove filler words. For future transcriptions, consider whether verbatim mode is necessary — some workflows only need clean transcripts. Custom dictionary (Premium) can help with domain terms but won't fix filler word over-capture.
