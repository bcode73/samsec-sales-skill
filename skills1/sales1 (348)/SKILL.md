---
name: sales-mention
description: "Mention platform help — real-time media monitoring, brand mention tracking, sentiment analysis, competitor benchmarking, review monitoring, REST API. Use when Mention alerts are returning too much noise and irrelevant results, mention limits are filling up before the month ends, sentiment analysis results seem inaccurate or missing, you need to pull Mention data into your CRM or dashboard via the API, Boolean search queries aren't catching the right conversations, you want to track competitor share of voice in Mention, or review monitoring isn't picking up sites you care about. Do NOT use for social listening strategy across tools (use /sales-social-listening) or choosing between social listening platforms (use /sales-social-listening)."
argument-hint: "[describe your Mention question — e.g., 'how do I reduce false positives in my alerts' or 'pull mentions into my app via API']"
license: MIT
version: 1.0.0
tags: [sales, social-listening, brand-monitoring, platform]
---

# Mention Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask the user:

1. **What do you need help with?**
   - A) Setting up monitoring alerts (keywords, Boolean queries, sources)
   - B) Reducing noise / improving mention quality
   - C) Sentiment analysis or tone filtering
   - D) Competitor benchmarking / Share of Voice
   - E) Review monitoring (Google, Trustpilot, G2, etc.)
   - F) API integration (pulling mentions into another tool)
   - G) Zapier / Slack integration
   - H) Understanding pricing / plan limits
   - I) Something else — describe it

2. **Which Mention plan are you on?**
   - A) Company ($599/mo, annual only — 5 alerts, 50K mentions, unlimited users; the ONLY plan new customers can buy as of July 2025)
   - B) Legacy Solo (2 alerts, 5K mentions, 1 user — discontinued, existing customers only)
   - C) Legacy Pro (5 alerts, 10K mentions, 10 users — discontinued)
   - D) Legacy Pro Plus (7 alerts, 20K mentions, unlimited users — discontinued)
   - E) Not sure / evaluating

   Note: legacy Solo/Pro/Pro Plus prices are no longer published by Mention and third-party trackers disagree — don't quote a hard legacy price.

**If the user's request already provides most of this context, skip directly to Step 2.** Lead with your best-effort answer using reasonable assumptions (stated explicitly), then ask only the most critical 1-2 clarifying questions at the end.

## Step 2 — Route or answer directly

If the request maps to a strategy or platform skill, route:
- Social listening strategy or tool comparison → `/sales-social-listening [question]`
- Social media scheduling/publishing → `/sales-social-media-management [question]` (Mention deprecated publishing — use Agorapulse or another tool)
- Competitor displacement strategy → `/sales-compete [question]`
- Crisis communication strategy → `/sales-social-listening [crisis detection question]`
- PR / media outreach → `/sales-media-relations [question]`

Otherwise, answer directly from the platform reference below.

## Step 3 — Mention platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities, pricing, data model, API integration recipes, code examples, and automation patterns.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

You no longer need the platform guide — focus on the user's specific situation.

1. **Alert setup** — help design Boolean queries, pick sources, set language/country filters
2. **Noise reduction** — review their query, add NOT exclusions, narrow sources
3. **API integration** — provide code snippets for their specific use case
4. **Plan optimization** — help them stay within mention limits or decide when to upgrade
5. **Competitive tracking** — set up parallel alerts for competitors, measure share of voice

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

*Best-effort from research — review these, especially items about plan-gated features and integration gotchas that may be outdated.*

- **Self-serve plans are gone — Company ($599/mo, annual only) is the only plan new customers can buy.** Solo/Pro/Pro Plus/Company Lite were discontinued in July 2025; existing customers may still be on them. The Company plan includes 5 alerts and 50K mentions/month (more are purchasable).
- **API access is a paid add-on on EVERY plan, including Company.** It is NOT bundled into the $599 Company plan. Mention's pricing for it is unpublished — you have to go through your account manager. Historical Data is also a Company add-on, not bundled.
- **On legacy plans, sentiment was Pro+ and competitive analysis / Share of Voice was Pro Plus+.** The current Company plan includes sentiment and competitive benchmarking by default.
- **Only 250 characters of mention content returned via API.** Confirmed in Mention's API Access help article — for legal/IP reasons the API returns a snippet of up to 250 chars. Follow the original source URL for full content.
- **No webhooks.** Egress is GET polling via `_links.pull` or the real-time streaming endpoint (`stream.mention.net`, one open stream per account, max 1000 mentions/alert). There is no push/HMAC callback.
- **Publishing was deprecated January 30, 2026.** Mention retired its Publish and Respond features; Agorapulse is the official replacement. Mention is now monitoring-only.
- **Common brand names generate massive noise.** If your brand name is a dictionary word, invest time in Boolean NOT exclusions before doing anything else.

## Related skills

- `/sales-social-listening` — Social listening strategy — tool comparison, monitoring setup, sentiment analysis, crisis detection, competitive intelligence
- `/sales-brand24` — Brand24 platform help — affordable Brand24 alternative with MCP server and Storm Alerts
- `/sales-brandwatch` — Brandwatch platform help — enterprise-grade social listening with deep consumer intelligence
- `/sales-meltwater` — Meltwater platform help — enterprise media intelligence with journalist database
- `/sales-social-media-management` — Social media management strategy — publishing, scheduling (since Mention no longer publishes)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`

## Examples

### Example 1: Reduce noise in brand monitoring
**User says**: "My Mention alerts are full of irrelevant results — my brand name is 'Atlas' and I get mentions of Atlas mountains, Atlas rockets, etc."
**Skill does**:
1. Reads platform guide for Boolean query best practices
2. Designs a refined query: `"Atlas" AND ("software" OR "app" OR "saas") NOT "mountains" NOT "rocket" NOT "mythology" NOT "atlas shrugged"`
3. Suggests narrowing sources to exclude travel/science blogs
4. Recommends reviewing first 50 results and iterating exclusions
**Result**: Targeted monitoring query that filters out common word noise

### Example 2: Pull mentions into a dashboard via API
**User says**: "I want to automatically pull new brand mentions from Mention into our internal analytics dashboard"
**Skill does**:
1. Reads API reference for authentication and mention endpoints
2. Provides working cURL and Python code to list mentions with cursor pagination
3. Explains the 250-char content limit and how to follow `original_url` for full text
4. Suggests polling `_links.pull` for new mentions or using streaming API for real-time
**Result**: Working integration code with pagination and rate limit handling

### Example 3: Set up competitor share of voice tracking
**User says**: "I want to compare our brand mentions vs two competitors in Mention"
**Skill does**:
1. Notes that competitive analysis / Share of Voice is included on the current Company plan ($599/mo); on legacy plans it required Pro Plus or higher (Solo/Pro had no competitive benchmarking)
2. Designs three parallel alerts with identical source/language settings
3. Explains how to use Mention's built-in competitive report
4. Suggests tracking mention volume, sentiment split, and top sources weekly
**Result**: Competitive monitoring setup with apples-to-apples comparison

## Troubleshooting

### Mention limits filling up too fast
**Symptom**: You hit your monthly mention cap within the first week
**Cause**: Queries too broad, monitoring common words without enough exclusions, or tracking too many sources
**Solution**: Audit each alert's query — add NOT exclusions for the top false positive patterns. Narrow source types (e.g., drop forums if they're mostly spam). Consider splitting one broad alert into two focused ones so you can better control each. If you consistently need more, note that the current Company plan ($599/mo) includes 50K mentions/month with additional quota purchasable; legacy Solo/Pro/Pro Plus are no longer sold to new customers.

### Boolean queries not matching expected mentions
**Symptom**: You know a mention exists online but Mention didn't capture it
**Cause**: Query syntax issues, source not crawled by Mention, or mention published before alert was created
**Solution**: Test your Boolean logic — Mention uses AND/OR/NOT (no NEAR/n proximity). Check that the source type is included in your alert settings. Mention only tracks mentions from the moment an alert is created — no retroactive capture unless you have historical data access (Company plan).

### Sentiment analysis seems wrong
**Symptom**: Positive reviews show as negative, or sarcastic posts show as positive
**Cause**: Automated sentiment accuracy tops out around 70-85%, especially with sarcasm, slang, or non-English text
**Solution**: Use the API's `tone` parameter to manually override sentiment on high-impact mentions. Focus on sentiment trends over time rather than individual mention accuracy. If you need higher accuracy, consider Brand24's sarcasm detection or Brandwatch's custom sentiment models.
