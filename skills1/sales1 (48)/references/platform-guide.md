# Bazzly Platform Reference

## Overview

Bazzly is an AI-powered Reddit lead generation tool that monitors subreddits 24/7, identifies high-intent users, drafts contextual messages, and sends outreach (DMs and replies) via a Chrome extension running through the user's own Reddit account. Designed for solo founders and small teams wanting Reddit customer acquisition without manual scanning.

## Capabilities & automation surface

| Capability | How it works | Access |
|---|---|---|
| **Reddit monitoring** | Scans configured subreddits continuously, ~4-minute discovery latency | UI-only |
| **AI intent scoring** | Scores leads 0-100% based on post context and buying signals | UI-only |
| **AI message drafting** | Generates contextual DMs and replies based on product description and thread context | UI-only |
| **Chrome extension sending** | Sends approved messages through user's own Reddit account and browser session | Chrome extension |
| **Reply Boost / Smart upvotes** | Smart upvotes to push comments higher in thread visibility ("rank your comment #1") | UI-only |
| **High-karma autopilot accounts** | Comments/DMs posted by Bazzly's aged accounts on full autopilot ("zero ban risk") | UI / API |
| **DM automation** | Sends personalized direct messages to identified leads (manual approval required when using your own account) | Chrome extension |
| **Analytics dashboard** | Tracks leads found, messages sent, responses, and conversions | UI-only |
| **Subreddit configuration** | Select/exclude subreddits, set targeting criteria | UI-only |
| **REST API** | List opportunities, generate replies, queue replies programmatically | API |
| **MCP server** | Connect Claude Desktop / Cursor to the same opportunity → reply → queue workflow | MCP |

**Bazzly NOW ships a public REST API and an MCP server** (added since the 2026-05 baseline). Base URL `https://api.bazzly.ai`; Bearer / `X-Bazzly-Api-Key` auth with `bzly_live_` keys; MCP endpoint `https://api.bazzly.ai/mcp`. See `references/bazzly-api-reference.md`. There is still **no documented webhook or Zapier integration** — egress is via the REST API / MCP, not push events.

## Pricing, limits & plan gates

*Verified against bazzly.ai 2026-06-13.*

Bazzly now sells a **single "All in One" plan** — the previous three-tier
Starter/Growth/Elite structure (with 20/200/unlimited AI credits and 4/6/unlimited
subreddits) is gone.

| Feature | All in One |
|---|---|
| Price | **$99/month** |
| Included credits | **100 / month** (refreshed monthly; top up when you need more) |
| Leads / opportunities | Unlimited |
| High-karma autopilot accounts | Yes ("zero ban risk") |
| Smart upvotes (Reply Boost) | Yes |
| Reddit → Google ranking / AI citations | Yes |
| Chrome extension (post from your own account) | Yes |
| REST API + MCP server | Yes |
| Support | Direct support |

- **"Get Started for Free"** entry path; **cancel anytime, no questions asked**.
  (A previously-documented explicit "7-day free trial" is no longer stated on the
  pricing page — treat the free-start path as the current offer.)
- Extra credits are available as **top-ups** beyond the monthly 100 (there is a
  dedicated `top-ups` API scope).
- **Affiliate program**: 30% commission.

### Credit costs

| Action | Credit cost | Notes |
|---|---|---|
| AI draft generation | 0.1 | Cheapest — use for screening |
| Upvote (Reply Boost) | 0.2 | Per vote, limited by Reply Boost count |
| Comment via high-karma account | 10 | Most expensive — reserve for highest-intent leads |

**Credit strategy**: Generate AI drafts first (0.1 credits) to evaluate lead quality before committing 10 credits to post a comment. This screening step can save 50-80% of wasted credits.

## How the Chrome extension works

1. Install the Bazzly Chrome extension from the Chrome Web Store
2. Log in with your Bazzly account
3. The extension runs through your own Reddit session — Bazzly never stores your Reddit credentials
4. When you approve a message in the dashboard, the extension posts it through your browser as if you typed it
5. Daily sending limits are configurable to avoid spam detection
6. All messages require manual approval before sending

**Safety model**: Because messages are sent through your real browser session and Reddit account, Reddit sees normal browser activity, not API bot traffic. This reduces (but does not eliminate) ban risk.

## Message optimization

### Improving AI draft quality

1. **Product context**: Provide detailed, specific product description. Include: what problem you solve, who you solve it for, key differentiators, and proof points (numbers, testimonials)
2. **Tone guidance**: Specify whether replies should be casual, technical, founder-story, or resource-sharing
3. **Edit every draft**: Treat AI output as a starting point. Add personal context, remove generic phrases, and ensure the reply genuinely answers the thread's question
4. **Vary styles**: Don't use the same reply format everywhere. Mix:
   - Direct answer + subtle mention
   - Personal experience story
   - Resource/tool recommendation (your product among others)
   - Question that shows expertise + follow-up with solution

### Avoiding spam signals

- Never post the same message template in multiple threads
- Lead with value — answer the question before mentioning your product
- Don't mention your product in every reply — some threads deserve pure value
- Vary reply length (2 sentences to 2 paragraphs)
- Engage in follow-up comments when people respond — don't just drop a link and leave
- Limit to 3-5 posts per day from a single account

## Account safety

### Ban risk factors

| Risk level | Action | Mitigation |
|---|---|---|
| **Low** | AI draft generation, manual posting via Chrome extension | Review every message, vary content |
| **Medium** | DM automation with manual approval | Limit daily DMs, personalize each one |
| **High** | Reply Boost (smart upvotes) | Vote manipulation violates Reddit TOS — use very sparingly |
| **High** | High-volume posting (10+/day from one account) | Keep under 5 genuine replies per day |

### If your account gets warned

1. **Stop all automated activity immediately** — pause Bazzly
2. Wait 2-4 weeks before any engagement from the warned account
3. Resume with manual-only posting, no DMs, no Reply Boost
4. Consider creating a separate Reddit account for Bazzly outreach (keep your main account clean)
5. Reduce daily volume and increase personalization

## Integrations

**REST API + MCP server (added since 2026-05).** Bazzly now exposes a public REST
API and an MCP server, so opportunity/lead data and reply queueing CAN be driven
programmatically. See `references/bazzly-api-reference.md` for endpoints and auth.

- **REST API** — base `https://api.bazzly.ai`, Bearer `bzly_live_...` (or
  `X-Bazzly-Api-Key`) auth, scopes `read` / `write` / `top-ups`. Public Postman
  docs: https://documenter.getpostman.com/view/3358302/2sBXqKof1B
- **MCP server** — `https://api.bazzly.ai/mcp` (streamable-HTTP); wire it into
  Claude Desktop or Cursor. Tools: `list_opportunities`,
  `generate_opportunity_reply`, `queue_reply`, `list_reply_queue`.
- **Affiliate program** — 30% commission.
- **Still NOT available**: documented webhooks, Zapier, or Make. Egress is
  pull-based via the REST API / MCP, not push events.

**CRM tracking**: pull opportunities via `GET /public/v1/opportunities` (or the
`list_opportunities` MCP tool) and push them into your CRM. No webhook means you
poll rather than receive pushes. A spreadsheet bridge (Reddit username, thread URL,
message sent, response status, conversion) still works for non-developers.

## Comparison with similar tools

| Feature | Bazzly | KeyMentions | RedShip | ReplyGuy |
|---|---|---|---|---|
| **Platforms** | Reddit only | Reddit only | Reddit only | Twitter, Reddit, LinkedIn |
| **Intent scoring** | Yes (0-100%) | No | Yes (0-100) | No |
| **AI reply drafts** | Yes | Yes | Yes | Yes |
| **Auto-publish** | No (manual approval via Chrome) | Yes (auto-publish to Reddit) | No (manual, + auto DMs) | Yes (Twitter auto, Reddit/LinkedIn manual) |
| **Upvote boost** | Yes (Reply Boost) | No | No | No |
| **DM automation** | Yes (manual approval) | No | Yes (auto DMs) | No |
| **API/webhooks** | REST API + MCP (no webhooks) | No | Yes (REST + webhooks) | No |
| **Starting price** | $99/mo (single plan) | Free (3 keywords) | $19/mo | $49/mo |
| **Best for** | Founders wanting intent-scored leads, high-karma autopilot, and an API/MCP workflow | Founders wanting auto-publish to Reddit | Developers wanting API access + SEO post discovery | Teams wanting multi-platform reply generation |
