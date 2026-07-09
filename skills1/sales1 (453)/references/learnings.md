# RafflePress — Learnings

Accumulated, dated platform knowledge. Append new findings with a date stamp so staleness is auditable.

---

**2026-06-27**: Research baseline. Built from the marketing site, the official docs (webhooks, Zapier, developer), and giveaway-tool comparison/review articles.

- **It's a WordPress plugin, not a SaaS.** No hosted REST API and no MCP. The programmatic surface is **outbound webhooks**, a **Zapier** app, **15+ native ESP/CRM integrations**, **Uncanny Automator**, and **WordPress action/filter hooks + URL-parameter prefill**. Anyone expecting a "RafflePress API" to create giveaways will be disappointed — creation is UI-only.
- **Webhook payload is small and email-centric:** `fullname`, `first_name`, `last_name`, `email`, `giveaway_id`, `giveaway_name`, `sign_up_date`. Format **JSON or FORM**, custom headers supported, multiple webhooks supported. Fires on **signup**.
- **Big webhook caveat (verbatim from docs):** third-party social-action data (Facebook/X/YouTube/Instagram/Pinterest) is **NOT** shared via webhook. So you get the email identity, not per-action analytics. This is the #1 thing to set expectations on.
- **No documented webhook HMAC** and no payload example in the docs (they suggest you inspect deliveries). Secure via secret URL + a custom auth header; dedupe on `email`+`giveaway_id`.
- **Zapier key is per-action.** It comes from the giveaway's **Join an Email Newsletter** action (pick Zapier in its dropdown). Sole trigger: **New Contestant Created**. Limit: **one** Join-an-Email-Newsletter action per giveaway when using Zapier.
- **Native ESPs (15+):** Mailchimp, ConvertKit/Kit, AWeber, Drip, ActiveCampaign, Constant Contact, GetResponse, Campaign Monitor, FluentCRM, iContact, Mad Mimi, MailerLite, Moosend, Sendy, Brevo. Prefer native sync over webhook when you just need the list.
- **Entry mechanics:** 30+ bonus actions; **refer-a-friend = +10 entries**, social shares +2–5. Refer-a-friend is a *giveaway entry mechanic*, **not** affiliate/commission tracking.
- **Pricing:** free **Lite** on WordPress.org; **Pro** as one-time/lifetime (~$299 single / ~$349 unlimited, best-effort — historically also annual Plus/Pro/Growth/Ultimate tiers). Confirm on the pricing page. Requires a self-hosted WordPress site.
- **By Awesome Motive** (WPForms/OptinMonster/MonsterInsights family) — mature, well-supported, lots of docs.
- **Competitive set:** Gleam (no WP plugin, pricier), SweepWidget (cheap, 90+ entry options, strong social), Woorise (landing pages + quizzes, features gated to paid), Rafflecopter (classic, blogger-focused), KingSumo/ShortStack/Vyper. RafflePress is the go-to **for WordPress** sites specifically.

⚠️ **Fetch note for future runs:** the marketing homepage renders fine via WebFetch, and the docs pages (`/docs/webhooks/`, `/docs/zapier/`, `/docs-categories/developer/`) are readable. No anti-bot issues observed.
