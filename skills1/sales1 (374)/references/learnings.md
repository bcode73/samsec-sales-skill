# Noisely — Learnings

Accumulated, dated platform knowledge. Append new findings with a date stamp so staleness is auditable.

---

**2026-06-27**: Research baseline. Built from the marketing site (noise.ly) and the vendor's comparison pages (vs Frill/Brand24/ParseStream/Inari/Cycle/Chattermill/ChatPRD/Nolt).

- **Category:** AI feedback-tracking / product-intelligence. **Aggregates unsolicited feedback** from 23+ sources and AI-clusters it — it is **not** a survey/NPS tool (don't confuse with `/sales-customer-feedback` survey programs).
- **No public REST API.** `noise.ly/docs/webhooks` 404s; no api docs found. Programmatic surface = **outbound webhooks**, **native integrations**, **CSV** import/export. Custom plan mentions "custom integrations." Don't assume an `api.noise.ly`.
- **Incoming sources (22–23+):** Trustpilot, G2, Google Reviews, Apple App Store, Google Play, BBB, ConsumerAffairs, Yelp, Reddit, Hacker News, Quora, Bluesky, GitHub, DEV, Stack Overflow, YouTube, Google News, Zendesk, Freshdesk, Intercom, Canny, CSV.
- **AI pipeline:** 12-category classification (+ auto-dedupe), mention-level sentiment, urgency/impact scoring, **pattern clustering → "action items"** (ranked by frequency × impact), **spike detection** (real-time alerts).
- **Outbound channels (10):** Slack, Microsoft Teams, Discord, Linear, Jira, Notion, Asana, Google Sheets, Email, **Webhooks**. Native Linear/Jira/Asana turn an action item into a ticket/task; Sheets for BI; webhook for custom routing.
- **Webhook caveat:** payload schema + event names **not published**; no documented HMAC/retry/rate-limit. Capture a live delivery, secure the URL, dedupe on the **action-item id**.
- **Credit model:** "**AI analyses**" are a monthly credit limit (**~2,000/mo on Pro**) — this, not seats, is the binding constraint. Noisy sources burn credits; brand-ambiguity filters help.
- **Pricing:** **Try** $29 one-time (≤500 mentions, 1-hr report, $29 Pro credit) → **Pro** $49/mo (23+ sources, 10 channels, 2,000 analyses/mo, unlimited seats) → **Custom** (higher limits, custom integrations, SLA). No per-seat fees. Positioned as the cheap alternative ($49 vs Brand24 $149, vs enterprise Enterpret/unitQ/Chattermill).
- **Competitive set:** Enterpret, unitQ, Chattermill (enterprise VoC), Frill/Nolt/Canny (feedback boards), Brand24 (social listening, has a skill), ParseStream (has a skill). **Cycle** (acq. Atlassian, shut down Oct 2025) and **Inari** (acq. Amplitude, July 2025) are **discontinued** — don't add.

⚠️ **Fetch note for future runs:** the marketing homepage renders fine via WebFetch; there are no API/webhook docs to fetch (404). The webhook payload shape and exact source list are the known gaps — verify in-account.
