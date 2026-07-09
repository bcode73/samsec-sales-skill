# Frill — Learnings

Accumulated, dated platform knowledge. Append new findings with a date stamp so staleness is auditable.

---

**2026-06-27**: Research baseline. Built from the marketing site (frill.co), the developer docs (developers.frill.co — GitBook, llms.txt), the webhooks help article, and Canny/Nolt comparison content.

- **Category:** affordable **customer-feedback suite** — feedback **boards** (ideas + voting + comments), **public roadmap**, **announcements/changelog**, **surveys**, embeddable **widget**. A cheaper/simpler **Canny / Nolt / UserVoice alternative**. Audience: SaaS/product teams, early-stage startups, indie makers (startup/nonprofit/OSS discounts).
- **API:** base **`https://api.frill.co/v1/`**. Auth = **API key** (from app.frill.co/settings/company), three methods — **Bearer header recommended** (`Authorization: Bearer KEY`), or query `?api_key=`, or Basic auth (key as username). **Cursor pagination:** response `pagination` object has `count`/`total`/`hasNextPage`/`startCursor`/`endCursor`; pass `endCursor` as **`after`** to get the next page.
- **Resources:** `ideas`, `comments`, `votes`, `statuses` (roadmap stage), `topics` (tags), `followers` (tracked users), `announcements`, `announcement-categories`, `notes`. An Idea has a **Status** (roadmap column) + multiple **Topics**.
- **Webhooks (HMAC-signed!):** set in Settings → Webhooks (Company Settings). Payload `{triggered_at, event, data_type, data}`. **Events:** idea created/updated/deleted/archived/status-changed/roadmap-visibility/merged; voted/unvoted; comment created/updated/deleted; notes created/updated/deleted; announcement created/published/updated/deleted. **Signature: HMAC-SHA256** of the raw JSON payload using the Webhook Secret (Company Settings → Webhooks), compared to the signature header — `hash_hmac('sha256', payloadJson, secret)`. Verify + dedupe on entity id + `triggered_at`.
- **Frill-Script (front-end):** embed the widget, run **surveys**, and **identify users** (pass logged-in user identity so votes/ideas attach to a real account). **SSO** auto-authenticates your users on the board. Without identification, board activity is anonymous.
- **Integrations (15+):** Slack, Jira, Trello, Zendesk, Intercom, Help Scout, Zapier, Linear, Asana, Airtable, Monday.com, Miro, Basecamp, Google Docs/Sheets, Azure DevOps.
- **Prioritization:** Benefit/Cost scores → "Quick Wins" / "Major Projects" matrix.
- **Pricing:** entry ~$25/mo → Enterprise ~$349/mo; 14-day trial, no card; startup/nonprofit/OSS discounts. (Canny's lowest paid ~$400/mo; Nolt ~$25/board.)
- **Competitive set:** Canny, Nolt, UserVoice, Featurebase, Hellonext, Savio, Productlift, FeatureOS, Beamer (changelog). Frill's angle: full board+roadmap+changelog+surveys at a low price with a real API + signed webhooks.

⚠️ **Fetch note for future runs:** marketing site fetches fine; **developers.frill.co is GitBook** — append `.md` to any page, full index at `llms.txt`/`llms-full.txt`, and a **dynamic query** `GET https://developers.frill.co/api/<page>.md?ask=<question>&goal=<goal>` for specifics. Confirmed: base URL `api.frill.co/v1`, Bearer auth, cursor pagination (`after`/`endCursor`), resource list, HMAC-SHA256 webhook signing + event list. Gaps: exact per-resource create/update JSON bodies + the exact webhook signature header name (confirm via the `?ask=` query or in-account).
