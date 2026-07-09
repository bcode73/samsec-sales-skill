# ShortStack — Learnings

Accumulated, dated platform knowledge. Append new findings with a date stamp so staleness is auditable.

---

**2026-06-27**: Research baseline. Built from the marketing site (shortstack.com), apitracker.io, and indexed snippets of the (Cloudflare-protected) help center Entries-API and webhook-signing articles.

- **Category:** campaign platform for **contests / giveaways / sweepstakes / lead capture** + landing pages, pop-ups, quizzes, refer-a-friend, instant-win, and social promos (hashtag, comment-to-enter). 50,000+ businesses, 1B+ entries; customers from SMB/agency up to enterprise (UFC, Netflix, Live Nation, Ticketmaster). Has a **free-forever** plan → not enterprise-only.
- **Entries API (read):** base **`https://entries.shortstack.com/entries`**, auth header **`Authorization: Token token=YOUR_API_KEY`** (literal `Token token=` prefix). Params: `per_page` (default 100, **max 5000**), `sort` (e.g. `received`), `direction` (ascending|descending). Response **`{ "data": [ … ] }`**. Reads entries/leads; campaigns are UI-built (no create-campaign API surfaced).
- **Webhooks (real-time, SIGNED):** HTTP POST on each new entry. **`X-Ss-Signature`** header = HMAC of **request body + your secret key** — a real signed webhook (verify it server-side; constant-time compare; dedupe on entry id). This is a positive vs many giveaway tools (RafflePress/WPFunnels have no HMAC). Plus a **Webhooks management API** + **sandbox** + OpenAPI/Swagger spec (per apitracker).
- **Integrations:** native Mailchimp (direct), HubSpot, Salesforce; Zapier + "hundreds of tools" via webhooks; LeadsBridge. CSV lead export. **No MCP.**
- **Pricing:** free-forever + paid tiers (entry volume, advanced campaigns, white-label, team/agency/enterprise). Exact prices not on the landing page — verify.
- **Identity = email** (+ entry `id`). Per-entry fields depend on the campaign form.
- **Competitive set:** RafflePress (WordPress, built), Gleam, SweepWidget, Woorise, Vyper, KingSumo, Rafflecopter (defunct). ShortStack's edge: standalone SaaS, big-brand-grade, **signed** webhook + Entries API, free plan.

⚠️ **Fetch note for future runs:** the marketing site renders via WebFetch, but **help.shortstackapp.com is Cloudflare-protected** (WebFetch + curl both blocked with "Just a moment…"). Get API details from indexed search snippets or the in-account developer docs/OpenAPI spec. Confirmed: base URL, `Token token=` auth, `per_page`/`sort`/`direction`, `{data:[…]}`, `X-Ss-Signature` = body+secret HMAC. Unconfirmed: full endpoint catalog, exact entry/webhook JSON schema, HMAC hash function, pagination beyond 5000.
