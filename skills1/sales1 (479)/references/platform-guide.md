# ReplyDaddy Platform Reference

## Overview

ReplyDaddy (replydaddy.com) is a Reddit marketing co-pilot that uses AI (Claude Sonnet 4) to discover relevant Reddit posts and generate authentic responses. Differentiated by manual-control-first design — it never requests Reddit credentials or posts on your behalf. Available as both a monthly/annual subscription (AI costs included) and a lifetime deal with a BYOK (Bring Your Own Key) Anthropic API model. Re-verified against live official docs 2026-06-13.

## Capabilities & automation surface

| Capability | Access |
|---|---|
| AI post discovery (keyword + brand matching) | UI-only |
| Multi-factor relevance scoring (70% relevance weight) | UI-only |
| Response generation (Claude Sonnet 4) | UI-only |
| Subreddit rule compliance checking | UI-only |
| Post eligibility verification | UI-only |
| Persona-based reply customization | UI-only |
| Two-prompt system (Analysis prompt + Reply prompt) | UI-only |
| 0-100 relevancy scoring | UI-only |
| Post Generator (Beta) with eligibility checking | UI-only |
| Subreddit Intelligence dashboard | UI-only |
| 90-day marketing plan generator | UI-only |
| Daily engagement habit builder | UI-only |
| Marketing Momentum Tracker | UI-only |
| Multi-project support (multiple brands per account) | UI-only |
| Scheduled scans | Coming soon (manual scans only today) |

**No public API.** No webhooks. No Zapier/Make/MCP integration. No programmatic access. All interaction happens through the web dashboard.

**Workaround for automation:** None documented. If you need CRM integration or automated workflows, consider alternatives with API access (Redreach webhooks, CatchIntent CRM push, Buska API/MCP, ForumScout API Direct).

## Pricing, limits & plan gates

### Subscription Plans (verified live 2026-06-13 — AI costs included, no BYOK needed)

| Plan | Monthly | Annual | Notes |
|---|---|---|---|
| Free | $0 | $0 | 5 subreddits, 10 keywords, 30 scans/mo, up to 60 posts/mo |
| Solopreneur | $49/mo | $490/yr (save $98) | Entry paid tier |
| Growing Business | $199/mo | $1,990/yr (save $398) | Marked "most popular" |
| Marketing Teams & Agencies | $799/mo | $7,990/yr (save $1,598) | Multi-project / team |
| Enterprise | Custom (book a call) | Custom | Custom limits + dedicated support |

<!-- Source: replydaddy.com (rendered) re-verified 2026-06-13. Subscription tiers were previously documented as Starter $99 / Growth $299 / Scale $799 — those names/prices are no longer current. Subscription plans include AI generation costs (no API key required); the LTD is the only BYOK path. -->

### Lifetime Deal (BYOK — Anthropic key)

Sold via RocketHub in three one-time tiers (all marked SOLD OUT on RocketHub as of 2026-06-13 — availability may rotate):

| LTD tier | One-time | Projects | Subreddits/project | Keywords/project | Posts/day/project | Scans/day/project | Replies/day |
|---|---|---|---|---|---|---|---|
| Solopreneur | $59 | 1 | 10 | 10 | 2 | 1 | Unlimited |
| Growing Business | $159 | 5 | 15 | 15 | 10 | 2 | Unlimited |
| Agency | $259 | 10 | 30 | 30 | 30 | 10 | Unlimited |

- **BYOK model:** User provides own **Anthropic** API key (console.anthropic.com). OpenAI is NOT referenced in current official docs — Anthropic only.
- **Default key caveat:** ReplyDaddy's default API key works only for onboarding/project setup. For day-to-day usage (scanning, generating replies, creating posts) you must add your own Anthropic key.
- **Per-action cost (official):** $0.003-$0.015 per AI-generated response; $10-20 in Anthropic credits covers ~1,000-3,000 responses.
- **30-day money-back guarantee** on the LTD.

**Cost comparison at typical usage (30 replies + 10 scans/day):**

At the official rate of $0.003-$0.015 per response, ~30 replies/day ≈ 900/mo ≈ $3-14/mo in Anthropic credits (scanning adds some on top). Heavy multi-keyword scanning across hot/rising/new pushes this higher.

| Pricing path | Month 1 | Month 3 | Month 6 |
|---|---|---|---|
| LTD + BYOK (~$15-30/mo Anthropic) | $74-89 | $104-149 | $149-239 |
| Solopreneur subscription ($49/mo, AI included) | $49 | $147 | $294 |
| Growing Business subscription ($199/mo, AI included) | $199 | $597 | $1,194 |
| Reppit AI (flat rate) | $29 | $87 | $174 |
| Subtle AI (cheapest tier) | $20 | $60 | $120 |

The LTD ($59 + Anthropic credits) is the cheapest long-run path for most solo users, since subscriptions bundle AI cost into a recurring fee. Subscriptions only win if you want zero key management or need team/agency seats.

### Key limits to watch

- **BYOK costs are proportional to usage.** More keywords, more scans, more reply drafts = higher API bills. There's no usage cap — but there's no cost cap either.
- **No free trial mentioned for subscription plans.** The LTD is effectively a trial path.
- **Solo developer risk.** LTD products from solo developers carry abandonment risk — evaluate accordingly.

## Integrations

**None.** ReplyDaddy has no native CRM connectors, no Zapier/Make triggers, no API, no export functionality.

**Data flow:** One-directional — Reddit posts flow into ReplyDaddy's dashboard for review. You manually copy responses and post them on Reddit yourself.

## Data model

No API means no programmatic data model. The conceptual objects:

```json
// Persona (UI object)
{
  "name": "SaaS Founder",
  "background": "Built 3 SaaS products, 10 years in B2B",
  "expertise": ["project management", "remote work", "productivity"],
  "tone": "helpful, conversational, no hard sells"
}
```
<!-- Constructed from UI descriptions — no API exists to verify -->

```json
// Discovered Post (UI object)
{
  "title": "Looking for a simpler project management tool",
  "subreddit": "r/SaaS",
  "url": "https://reddit.com/r/SaaS/...",
  "category": "hot",
  "relevance_score": 0.85,
  "matched_keywords": ["project management tool"],
  "eligible_to_reply": true,
  "rule_compliance": "passes",
  "ai_response_draft": "I switched from Asana to [Product] last year because..."
}
```
<!-- Constructed from UI descriptions — no API exists to verify -->

```json
// Project (UI object)
{
  "name": "My SaaS Product",
  "website_url": "https://myproduct.com",
  "brand_knowledge": "Auto-discovered from website scan",
  "keywords": ["project management alternative", "Asana competitor"],
  "target_subreddits": ["r/SaaS", "r/startups", "r/Entrepreneur"]
}
```
<!-- Constructed from UI descriptions — no API exists to verify -->

## Quick-start recipes

### Recipe 1: First project setup

**Goal:** Start discovering Reddit leads for your product.

**Steps:**
1. Sign up at replydaddy.com (or activate LTD via RocketHub)
2. If BYOK (LTD): add your own Anthropic API key in Settings → Configuration (create it at console.anthropic.com and add credits). The built-in default key only covers onboarding/setup — day-to-day scanning and reply generation require your own key. Subscription plans include AI cost, so no key is needed.
3. Create a project — enter your website URL. ReplyDaddy's AI scans it to build brand knowledge automatically
4. Configure a persona — define background, expertise, and tone for reply generation
5. Set up keywords:
   - Competitor names: "Asana alternative", "better than Monday"
   - Problem phrases: "looking for project management", "need help organizing"
   - Pain language: "frustrated with [competitor]", "switching from [competitor]"
6. Select target subreddits where your ICP posts (niche communities, not megasubs)
7. Wait for AI to scan hot, rising, and new posts
8. Review discovered posts — check relevance score, read the AI response draft
9. Edit the response to add genuine value, then manually post on Reddit

**Gotchas:**
- Start with 3-5 keywords and expand based on quality of discovered posts
- The AI auto-discovers brand knowledge from your website — review it for accuracy
- Higher relevance scores don't mean buying intent — you still need to filter manually

### Recipe 2: Optimizing persona for authentic responses

**Goal:** Get AI responses that sound like a real person, not a marketer.

**Steps:**
1. Open your persona settings
2. Write background as if describing a real community member: "Full-stack developer who's tried 6 project management tools over 5 years"
3. Set expertise to specific domains, not broad categories: "remote team coordination" not "business"
4. Configure tone: "casual but knowledgeable, shares personal experience, never uses marketing language"
5. Generate a test response and compare against your own writing style
6. Iterate — the persona directly controls response quality

**Gotchas:**
- A well-configured persona is the single biggest lever for response quality
- Don't describe your persona as a marketer — the AI will generate marketing copy
- Review and edit every draft before posting — AI responses need human polish

### Recipe 3: Manual CRM logging workflow (no integration exists)

**Goal:** Track Reddit leads in your CRM despite no export or API.

**Steps:**
1. After posting a ReplyDaddy-suggested response on Reddit, copy the thread URL
2. Create a new contact/lead in your CRM:
   - Source: "Reddit - ReplyDaddy"
   - Notes: subreddit, thread title, your response summary, their original question
3. Add UTM parameters to any product links you share: `?utm_source=reddit&utm_medium=comment&utm_campaign=replydaddy`
4. Set a follow-up reminder (3-7 days) to check:
   - Did they reply to your comment?
   - Did they DM you?
   - Did they visit your product (check UTM in analytics)?
5. Update CRM status: engaged / interested / converted / no response

**Gotchas:**
- This is manual and doesn't scale beyond ~10-15 leads/day
- If CRM integration is critical for your workflow, consider tools with API access: Redreach (webhooks), CatchIntent (CRM push), Buska (REST API + MCP)
- Use a spreadsheet as a lightweight alternative if you don't have a CRM

## Integration patterns

### No native integration exists

ReplyDaddy is fully isolated — no data flows out programmatically. The only integration pattern is manual:

1. **Discover** leads in ReplyDaddy dashboard
2. **Review** relevance score and AI response draft
3. **Edit** response to add genuine value and thread-specific context
4. **Post** manually on Reddit (copy-paste)
5. **Log** the engagement in your CRM manually
6. **Track** results via UTM parameters in your product links

### When to switch tools for integration

If your workflow requires any of these, ReplyDaddy is not the right tool:
- Automated lead export to CRM
- Webhook notifications for new leads
- Programmatic access to discovered posts
- Pipeline integration with outbound sequences
- MCP server for AI agent workflows

Consider: Buska (REST API + MCP), Redreach (webhooks), CatchIntent (CRM push + MCP), ForumScout (API Direct)
