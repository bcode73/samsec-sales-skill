# Snov.io Platform Guide

## Email Finder
- **Domain search**: Find all email addresses associated with a domain — returns prospects with names, positions, and social profiles
- **Name + domain search**: Find a specific person's email given their name and company domain
- **LinkedIn profile enrichment**: Extract email from a LinkedIn profile URL
- **Company domain lookup**: Find the domain for a company by name
- **Email count check**: Check how many emails are available for a domain before using credits
- **Chrome extension**: Find emails directly from LinkedIn profiles and company websites
- **Credits system**: Each successful find consumes credits — check email count first to estimate credit usage

## Email Verifier
- **98% accuracy**: 7-tier verification process for high-confidence results
- **Verification tiers**: Syntax check, gibberish detection, domain check, MX record check, SMTP check, catch-all detection, freemail detection
- **Bulk verification**: Verify up to 10 emails per API batch request
- **Statuses**: Valid, invalid, catch-all, unknown — act on valid only, treat catch-all with caution
- **Best practice**: Always verify emails before adding to campaigns — reduces bounces and protects sender reputation

## Multichannel campaigns
- **Email + LinkedIn sequences**: Combine email steps with LinkedIn actions in a single drip campaign
- **Drip campaigns**: Automated multi-step sequences with configurable delays between steps
- **A/B testing**: Test different subject lines and email body variants to optimize performance
- **Sentiment analysis**: AI-powered analysis of prospect replies to gauge interest level
- **AI email writer**: Automated email composition — generates personalized emails based on prospect data
- **Auto-stop on reply**: Campaign pauses sending to a prospect when they reply
- **Scheduling**: Configure send windows by day and time to optimize delivery timing

## LinkedIn Automation
- **Paid add-on**: $69/month per LinkedIn account slot on a free plan, or $59/month per slot when purchased with a paid plan (~$62 billed annually) — not included in any base plan
- **Automated actions**: Profile views, connection requests, follow-up messages
- **Multichannel integration**: LinkedIn steps woven into email campaign sequences
- **Condition-based**: Trigger LinkedIn actions based on email engagement (e.g., no open -> send connection request)
- **Requires**: Connected LinkedIn account and active add-on subscription

## Sales CRM
- **Deal tracking**: Manage deals through custom pipeline stages
- **Pipelines**: Visual pipeline view with drag-and-drop deal management
- **Google Calendar sync**: Sync meetings and calls directly from the CRM
- **Contact association**: Link prospects, emails, and deals together
- **Lightweight CRM**: Best for teams using Snov.io as their primary prospecting tool — for full CRM needs, integrate with Salesforce/HubSpot

## Email Warmup
- **Automated inbox warming**: Sends and receives emails between a large pool of real mailboxes to build sender reputation
- **Freemail support**: Works with Gmail, Outlook, and other freemail providers — not limited to custom domains
- **Large warm-up pool**: Extensive network of warmup accounts for realistic engagement patterns
- **Ramp schedule**: Gradually increases send volume over time
- **Best practice**: Run warmup for 2+ weeks before launching cold campaigns from a new mailbox
- **Slot limits**: Lower-tier plans have limited warmup slots (Starter: 3, Pro S+: unlimited)

## Email Deliverability Check
- **Inbox placement testing**: Check whether your emails land in inbox, spam, or promotions tab
- **Reputation monitoring**: Track sender reputation over time
- **Domain authentication check**: Verify SPF, DKIM, DMARC configuration
- **Best practice**: Run deliverability checks before and after campaign launches to catch issues early

## Email Tracker
- **Gmail extension**: Track email opens and link clicks directly from Gmail
- **Real-time notifications**: Get alerted when a prospect opens your email or clicks a link
- **Engagement history**: View full open/click timeline per email
- **Free tool**: Available to all Snov.io users

## AI Email Writer
- **Automated composition**: Generate personalized cold emails based on prospect data and your product/service
- **Campaign integration**: Use AI-written emails directly in drip campaigns
- **Customization**: Adjust tone, length, and call-to-action style
- **Best practice**: Always review and personalize AI-generated emails before sending — use as a starting point, not a final draft

## Prospect Management
- **Lists**: Organize prospects into targeted lists for campaigns
- **Custom fields**: Add custom data fields to prospect records for segmentation and personalization
- **Do-not-email list**: Maintain a suppression list to prevent outreach to opted-out or restricted contacts
- **Import/export**: CSV import and export for bulk prospect management
- **Deduplication**: Automatic duplicate detection across lists

## Data model

| Object | Description | Key fields |
|--------|-------------|------------|
| Prospect | Contact record | id, email, firstName, lastName, company, position, socialProfiles, lists |
| List | Prospect grouping | id, name, contactCount, created |
| Campaign | Drip email sequence | id, name, status, steps, recipientCount |
| Campaign Step | Individual step in a campaign | id, campaignId, type (email/LinkedIn), variant, delay |
| Email Verification | Verification result | email, status (valid/invalid/catch-all/unknown), result |
| Domain Search | Domain lookup result | domain, emailCount, prospects |
| Deal | CRM deal record | id, name, stage, value, contacts |
| Pipeline | CRM pipeline | id, name, stages |
| Webhook | Event subscription | id, url, events, status |

## API quick reference
- **Base URL**: `https://api.snov.io`
- **Versions**: V1 (legacy/auth, balance, webhooks) and V2 (the current surface — domain search, finder, verifier, sender accounts, warmup, campaigns, prospects, CRM)
- **Auth**: OAuth 2.0 Bearer token — exchange `client_id` + `client_secret` for an `access_token` (1-hour lifespan, must refresh)
- **Rate limit**: 60 requests per minute
- **Endpoint categories** (current API page):
  - **Domain Search** (v2): Company info, prospect profiles, prospect email lookup, domain emails, generic contacts
  - **Email Finder** (v2): Name+domain lookup, company domain lookup, LinkedIn profile enrichment; plus v1 `get-domain-emails-count`, `get-profile-by-email`
  - **Email Verifier** (v2): Batch (up to 10) verification, SMTP checks
  - **Email Accounts / Sender Accounts** (v2): `/v2/sender-accounts/emails` CRUD + `check-sender-status`
  - **Email Warmup** (v2): `/v2/warm-up` CRUD + `/v2/warm-up/{id}/statistics`
  - **Campaign Management** (v2): `/v2/campaigns` CRUD, `change-state`, schedules, email-step-content, recipient-status, finished-prospects, do-not-email-list; analytics/progress/replies/opens/clicks/sent under `/v2/campaigns/{id}/...`
  - **Prospect Management** (v2): `/v2/prospects`, find-by-email, custom-fields, `/v2/lists`
  - **CRM** (v2): `/v2/pipelines`, `/v2/pipelines/{id}/stages`
  - **Webhooks** (v1): list/add/update-status/delete + per-request callback URLs on async endpoints
  - **Account** (v1): `POST /v1/user/balance` — check credit balance
- **Async endpoints**: Most v2 finder/verifier endpoints are async (POST `/start` -> `task_hash` -> GET `/result`) — supply a `webhook_url` to receive results without polling
- **Full reference**: See Snov.io API docs at `https://snov.io/api` and `https://snov.io/knowledgebase/how-to-use-snov-io-api/`

## Integrations
- **Native CRM**: HubSpot, Pipedrive, Salesforce, Zoho CRM, Close CRM, Freshsales, Nutshell
- **Automation**: Zapier (5,000+ app connections), Make (formerly Integromat)
- **Productivity**: Gmail, Google Calendar, Slack, Calendly
- **Marketing**: Mailchimp, Airtable
- **Other**: Trello, Intercom
- **Best practices**: Use native integrations where available for real-time sync; fall back to Zapier/Make for non-native connections

## Pricing (verified 2026-06-13 against snov.io/pricing — re-verify before quoting)

| Plan | Price (monthly) | Credits | Recipients | Warmups |
|------|-------|---------|------------|---------|
| Trial | $0 | 50 | 100 | 1 slot (450 free warm-up emails, non-renewable) |
| Starter | $39/mo | 1,000 | 5,000 | 3 slots |
| Pro S | $99/mo | 5,000 | 25,000 | Unlimited |
| Pro M | $189/mo | 20,000 | 50,000 | Unlimited |
| Pro L | $369/mo | 50,000 | 100,000 | Unlimited |
| Ultra | $738/mo | 100,000 | 200,000 | Unlimited |
| Custom | Custom | from 200,000 | from 400,000 | Unlimited |

**Add-ons**: LinkedIn Automation $69/mo per slot on a free plan, or $59/mo per slot when bought with a paid plan (~$62 billed annually). Annual billing saves 25% (e.g. Starter ~$29.25/mo, Pro S ~$74.25/mo, Pro M ~$141.75/mo annual-equivalent).

**Key stats**: 400K+ users, 300K+ companies, 180+ countries, 4.5/5 G2, 4.8/5 Trustpilot.

## Campaign setup workflow
1. Build your prospect list (Email Finder, CSV import, or Chrome extension)
2. Verify all emails (bulk verification — only send to "valid" status)
3. Connect your sending mailbox(es)
4. Enable email warmup on all mailboxes — wait 2+ weeks before launching
5. Create a new drip campaign with email steps (and LinkedIn steps if add-on is active)
6. Configure A/B test variants for subject lines and body copy
7. Set delays between steps (2-3 days for follow-ups is typical)
8. Add verified prospects to the campaign
9. Run a deliverability check before launch
10. Launch and monitor campaign analytics

## Email finder workflow
1. Check email count for the target domain first (saves credits if count is low)
2. Use domain search for broad prospecting at a company
3. Use name + domain search when you know the specific person
4. Use LinkedIn enrichment when you have the prospect's LinkedIn URL
5. Always verify found emails before adding to campaigns

## Verification workflow
1. Collect emails from any source (finder, CSV, manual)
2. Run bulk verification (up to 10 per API batch)
3. Filter results: only use "valid" emails in campaigns
4. Treat "catch-all" with caution — these domains accept all emails, so verification cannot confirm the specific address exists
5. Remove "invalid" and "unknown" from your lists
6. Re-verify lists older than 3 months — email validity degrades over time

## Warmup setup
1. Connect your sending mailbox to Snov.io
2. Enable warmup — the system will start with low volume and ramp up
3. Monitor warmup progress in the dashboard
4. Wait at least 2 weeks before launching cold campaigns
5. Keep warmup running even after campaigns start — it maintains reputation

## LinkedIn automation setup
1. Purchase the LinkedIn Automation add-on ($69/mo per slot)
2. Connect your LinkedIn account
3. Create or edit a campaign to add LinkedIn steps
4. Configure LinkedIn actions: profile views, connection requests, follow-up messages
5. Set conditions: e.g., send LinkedIn connection request if email not opened after 3 days
6. Monitor LinkedIn activity to stay within LinkedIn's daily limits
