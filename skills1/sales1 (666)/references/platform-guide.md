# Woodpecker Platform Guide

## Cold email campaigns
- **Condition-based campaigns**: If/then branching based on prospect behavior (opened, clicked, replied) or data attributes — far more flexible than linear sequences
- **Up to 16 steps per campaign** — more than most competitors
- **A/B testing**: Up to 5 variants per step (subject lines, body copy, send times)
- **Auto-stop on reply**: Campaign automatically pauses sending to a prospect when a reply is detected
- **Personalization**: Custom fields and snippets for dynamic content
- **Manual tasks**: Insert non-automated action steps (e.g., call, LinkedIn visit) into campaign sequences

## Deliverability toolkit
- **Bounce Shield**: Prevents sending to risky addresses, protects sender reputation by pre-validating before each send
- **Adaptive Sending**: Automatically adjusts send volume based on provider limits and engagement signals — throttles down when signals are negative
- **ESP Matching**: Matches your sending patterns to what email providers expect, reducing spam flags
- **Domain audit**: Checks SPF, DKIM, DMARC configuration with specific fix suggestions
- **Spam checker**: Highlights spammy words, broken links, and authentication issues before sending — catch problems pre-launch
- **Deliverability monitor**: Ongoing monitoring of inbox placement and sender reputation

## Email warmup
- **Free built-in warmup** powered by Mailivery — included in all plans
- **AI-driven interactions**: Opens, replies, marks as important, removes from spam — mimics real engagement
- **Ramp schedule**: Starts with a few emails/day, gradually ramps to a max of 50/day
- **Free plan**: 4 warmup slots included at no cost
- **Additional slots**: Available as an add-on at $5/mo per email account
- **Best practice**: Run warmup for 2+ weeks before launching campaigns from a new mailbox

## Email verification
- **Free catch-all verification** powered by Bouncer
- **Real-time list cleaning** before sending — automatic validation when prospects are added to campaigns
- **Reduces bounce rate** and protects sender reputation
- No additional cost — included in all plans

## Inbox rotation
- **Automatic distribution** of sending across multiple connected email accounts
- Woodpecker rotates which account sends each email in a campaign
- **Unlimited email accounts** on all plans — no per-seat or per-mailbox charges
- Helps maintain per-account sending limits while increasing total daily volume

## Centralized inbox
- **Unified view** of all replies from all connected mailboxes in one place
- **Auto-categorization**: Interested, auto-replied, bounced, out-of-office — no manual sorting
- **Filters**: By campaign, status, or mailbox
- **Reply directly** from the centralized inbox without switching accounts

## LinkedIn automation
- **Add-on**: $29/month per LinkedIn account (verified 2026-06-13)
- **Automated actions**: Connection requests, messages, and profile visits
- **Multichannel sequences**: LinkedIn steps woven into email campaign steps
- **Condition-based**: e.g., if email not opened -> send LinkedIn connection request
- Requires a connected LinkedIn account

## Lead Finder
- **B2B database** with 1B+ leads
- **Search filters**: Company, title, industry, location
- **Data credits system**: 100 free credits included in the base plan; additional credits start at 500 credits for $10 (verified 2026-06-13 on woodpecker.co/pricing)
- **Direct export**: Export leads directly into Woodpecker campaigns — no CSV intermediary needed
- **Lead Finder API** (requires API add-on): lead search + enrichment workflow, plus enrichment of prospects already in the database — see `references/woodpecker-api-reference.md`

## Agency panel
- **Add-on**: $27/month per active client (plus optional White Label at $5/mo per active client; verified 2026-06-13)
- **Multi-client management** from a single dashboard
- **Per-client isolation**: Separate campaigns, prospects, mailboxes per client — no data bleed
- **Agency API**: HQ key + `x-company-id` header for programmatic client management
- **Per-company API keys**: Create API keys scoped to individual clients, manage mailboxes and campaigns across clients

## Data model

| Object | Description | Key fields |
|--------|-------------|------------|
| Campaign | Cold email sequence with steps | id, name, status, steps, prospects |
| Prospect | Contact record | id, email, firstName, lastName, company, status, tags |
| Mailbox | Connected email account | id, email, provider, warmupEnabled, dailyLimit |
| Campaign Step | Individual step in a campaign | id, campaignId, type (email/LinkedIn/task), variant, delay |
| Webhook | Event subscription | id, url, events, status |
| Blacklist | Blocked domains/emails | id, type (domain/email), value |
| LinkedIn Account | Connected LinkedIn profile | id, name, status |
| Manual Task | Non-automated action in campaign | id, type, prospectId, description |

## API quick reference
- **Base URL**: `https://api.woodpecker.co/rest`
- **Auth**: `x-api-key` header
- **Versions**: v1 (legacy, still active) and v2 (current); both coexist — no v1 deprecation announced (API roadmap, verified 2026-06-13)
- **Key endpoints**: Campaigns, Prospects, Mailboxes, LinkedIn accounts, Inbox, Reports, Lead Finder, Users, Manual tasks, Blacklist, Webhooks
- **Reports API (v2)**: `POST /v2/reports/{report-name}` returns a hash, then `GET /v2/reports/{hash}` retrieves results
- **Agency API**: HQ key + `x-company-id` header for multi-client access
- **Rate limits**: 1 concurrent request, queue of 6 (15-second timeout), unlimited monthly calls, HTTP 429 on overflow
- **Add-on required**: the "API, webhooks, MCP Server, CLI & integrations" add-on ($20/mo) or active trial — this single add-on now also unlocks the MCP Server and CLI
- **MCP Server**: official Model Context Protocol server (`Woodpeckerco/woodpecker-mcp-server` on GitHub, Docker image, `WOODPECKER_API_KEY` env var) — connect Claude Desktop / Continue.dev / Cursor for conversational campaign management; requires the API & Integration add-on
- **CLI**: official command-line tool — npm `@woodpecker.co/cli`, command `woodpecker`, Node.js 22 LTS; inspect/manage campaigns, prospects, inbox, mailboxes, reports, webhooks, blacklists, agency resources, plus raw API requests; requires API access
- **Full reference**: See `references/woodpecker-api-reference.md`
- **Developer contact**: developers@woodpecker.co

## Pricing (verified 2026-06-13 at woodpecker.co/pricing — verify current pricing before quoting)

Woodpecker now prices with an interactive **calculator** keyed to "Contacted prospects," not fixed named tiers:

- **Base rate**: **$4.8 per 100 contacted prospects / month** (USD). Annual billing saves up to 33% (a "Save 25%" toggle is also shown).
- **Included in the base plan**: 16,000 emails/mo, 4,000 stored prospects, 4 warm-ups, 100 Lead Finder credits, unlimited catch-all email verification, unlimited team members, unlimited email accounts.
- **Trial**: 14-day free trial, no credit card required.

> Older fixed EUR tiers (Free, Tier 1 €35, Tier 2 €67, Tier 3 €99) are no longer published on the pricing page. Third-party sites quote per-plan USD figures (e.g. ~$29 / ~$84 / ~$188) but these are not on Woodpecker's own pricing page and should be treated as estimates.

**Add-ons** (USD, per woodpecker.co/pricing 2026-06-13):

| Add-on | Price |
|--------|-------|
| LinkedIn outreach automation | $29/mo per LinkedIn account |
| Lead Finder credits | starts at 500 credits for $10 |
| Additional warm-ups | $5/mo per email account |
| Email addresses (Google/Microsoft) | $6/mo per email address |
| Email addresses (Maildoso/Mailforge) | $4/mo per email address |
| New domains / connect your domain | ~$1/mo per domain |
| Dedicated servers (Infraforge) | $59/mo per server |
| API, webhooks, MCP Server, CLI & integrations | $20/mo |
| Agency panel | $27/mo per active client |
| White Label | $5/mo per active client |

## Integrations
- **HubSpot**: Native integration (requires API & integrations add-on)
- **Pipedrive**: Native integration
- **Salesforce**: Via Zapier
- **Zapier**: Full integration — triggers and actions
- **Clay, Persana AI**: Native connectors
- **Calendly**: Meeting booking integration
- **Google Sheets**: Prospect import/export
