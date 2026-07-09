# CRM Platform Comparison Reference

Detailed comparison of CRM platforms for startups, organized by platform. Best-effort from research — pricing and features change frequently.

## Table of Contents

- [Decision Matrix](#decision-matrix)
- [Attio](#attio)
- [HubSpot](#hubspot)
- [Salesforce](#salesforce)
- [Folk](#folk)
- [Pipedrive](#pipedrive)
- [Close](#close)
- [Zoho CRM](#zoho-crm)
- [Salesflare](#salesflare)
- [Keap](#keap)
- [Ontraport](#ontraport)
- [EngageBay](#engagebay)
- [Salesmate](#salesmate)
- [Insightly](#insightly)
- [Maximizer](#maximizer)
- [Spreadsheets](#spreadsheets)

## Decision Matrix

| Criteria | Attio | HubSpot | Salesforce | Folk | Pipedrive | Close | Zoho |
|----------|-------|---------|------------|------|-----------|-------|------|
| **Best for** | Data-flexible startups | Inbound + marketing | Enterprise, complex orgs | Relationship-focused | Pipeline-focused sales | High-velocity outbound | Budget-conscious |
| **Team size sweet spot** | 3-50 | 1-500+ | 50-10,000+ | 1-20 | 3-50 | 5-50 | 3-100 |
| **Free tier** | Yes (3 users) | Yes (unlimited users) | No (14-day trial) | No (14-day trial) | No (14-day trial) | No (14-day trial) | Yes (3 users) |
| **Data model flexibility** | Excellent (custom objects) | Rigid (fixed objects) | Excellent (but complex) | Tag/list-based | Fixed pipeline | Fixed pipeline | Good (custom modules) |
| **Marketing built-in** | No | Yes (strong) | Via Pardot/MCAE | Basic outreach | No | No | Yes (basic) |
| **API quality** | Excellent (REST, MCP) | Good (REST, GraphQL) | Extensive (SOAP, REST) | Basic | Good (REST) | Good (REST) | Good (REST) |
| **Learning curve** | Medium | Low-Medium | High | Low | Low | Low | Medium |
| **Automation** | Strong (workflow builder) | Strong (paid tiers) | Very strong | Basic | Good (paid tiers) | Good | Good |

## Attio

**Positioning**: AI-native CRM with a flexible, relational data model. Built for startups that want to structure their CRM like a product.

**Strengths**:
- Custom objects and relationships — model your business the way it actually works (investors, fundraising rounds, product feedback)
- Email and calendar sync auto-populates records from inbox history
- API-first with REST API, webhooks, and MCP server
- Modern UX — feels like a productivity tool, not enterprise software
- AI features (Ask Attio) for natural language queries
- Built-in enrichment from company and contact data

**Weaknesses**:
- No native marketing automation — need third-party tools
- Smaller integration ecosystem than HubSpot
- Steeper learning curve than simpler CRMs due to data model flexibility
- Teams that don't need custom objects are overserved

**Pricing** (best-effort):
- Free: 3 users, 50K records, 3 custom objects, 250 automation credits/mo
- Plus ($29/user/mo annual): Unlimited seats, 250K records, 5 objects, 1,500 credits
- Pro ($69/user/mo annual): Advanced automation, reporting, 10 objects
- Enterprise: Custom

**Best for**: Startups that want flexibility, plan to use the API, and don't need built-in marketing. Teams between seed stage and ~$5M ARR who want a modern CRM they won't outgrow quickly.

**Existing skill**: `/sales-attio` — full platform help including custom objects, pipelines, automations, API

## HubSpot

**Positioning**: All-in-one CRM + marketing + sales + service platform. The default choice for inbound-led startups.

**Strengths**:
- Genuinely useful free tier — unlimited users, contacts, visual pipeline, email logging, live chat
- Marketing Hub integration — email campaigns, forms, landing pages, SEO tools
- Huge ecosystem — 1,500+ app integrations
- HubSpot for Startups program — up to 90% off for eligible startups
- Excellent onboarding and documentation
- Large hiring pool — many marketers and sales ops people know HubSpot

**Weaknesses**:
- Steep pricing jump from free to paid (Starter $20/seat/mo → Professional $890/mo for Marketing Hub)
- Rigid data model — fixed contacts, companies, deals, tickets objects
- Feature gating pushes you to higher tiers quickly
- Gets expensive at scale (per-contact pricing for Marketing Hub)
- Vendor lock-in risk — workflows and automation logic don't export

**Pricing** (best-effort):
- Free: Unlimited users, basic CRM features
- Starter ($20/seat/mo): Remove branding, simple automation, email sequences (Customer Platform bundles all hubs at Starter from $20/seat/mo)
- Professional ($890/mo for Marketing Hub incl. 3 seats + 2,000 contacts; $100/seat/mo for Sales Hub): Full automation, custom reporting, sequences
- Enterprise ($3,600/mo for Marketing Hub incl. 5 seats; $150/seat/mo for Sales Hub): Custom objects, advanced permissions, predictive lead scoring

**Best for**: Inbound-led startups that want marketing+sales in one platform. Teams that value ease of use and a large ecosystem over flexibility.

## Salesforce

**Positioning**: The enterprise CRM standard. Massive ecosystem, infinite customization, but significant complexity.

**Strengths**:
- Unlimited customization (custom objects, Apex code, Lightning components)
- Largest app marketplace (AppExchange — 7,000+ apps)
- Industry-specific solutions (Financial Services Cloud, Health Cloud, etc.)
- AI features (Einstein) with predictive scoring and conversation intelligence
- Most third-party tools integrate with Salesforce first
- Scales to thousands of users

**Weaknesses**:
- Requires a dedicated admin (often full-time) for meaningful customization
- Steep learning curve — training budget needed
- Expensive once you add modules ($25 → $100 → $175 → $350/user/mo)
- Slow to implement — 2-6 months for proper setup
- Rigid if you don't customize; overwhelming if you do
- Contract lock-in with annual commitments

**Pricing** (best-effort):
- Starter Suite ($25/user/mo): Basic CRM, 1 email/contact/day
- Pro Suite ($100/user/mo): Pipeline management, forecasting
- Enterprise ($175/user/mo): Advanced customization, AI
- Unlimited ($350/user/mo): Full platform access
- Agentforce 1 Sales ($550/user/mo): Bundled AI agents (Einstein/Agentforce)

(Salesforce raised Enterprise/Unlimited list prices ~6% in Aug 2025; numbers above reflect 2026 list pricing. Expect annual renewal uplifts on top.)

**Best for**: Teams past $5M ARR with 50+ employees that need complex workflows, multiple departments on one system, and have budget for a Salesforce admin. Not for early-stage startups.

## Folk

**Positioning**: Relationship-first CRM for small teams. Lightweight, fast to deploy, built around tags and lists.

**Strengths**:
- One-click LinkedIn import (Chrome extension)
- Tag-based organization — flexible, no rigid pipeline required
- Built-in AI for drafting icebreakers and follow-ups
- Native WhatsApp integration
- Mail merge with personalization variables
- Very fast onboarding (minutes, not days)
- Designed for non-salespeople (founders, BD, investors, recruiters)

**Weaknesses**:
- Limited automation compared to Attio or HubSpot
- Monthly message limits on outreach
- Not designed for large sales teams or complex deal stages
- No built-in phone/dialer
- Limited reporting and analytics
- Teams outgrow it around 20-50 people

**Pricing** (best-effort):
- No free plan — 14-day free trial only (defaults to Premium features)
- Standard ($24/user/mo annual, $30 monthly): Full CRM, 2,000 messages/member/mo, 500 enrichment credits/mo
- Premium ($48/user/mo annual, $60 monthly): 5,000 messages/member/mo, email sequences, custom objects, API access, dashboards
- Enterprise (from $80/user/mo annual): Custom limits, dedicated support, custom billing

**Best for**: Solo founders, small teams under 10, relationship-heavy businesses (VCs, agencies, consultants, recruiters). Great as a first CRM for non-technical teams who find traditional CRMs intimidating.

## Pipedrive

**Positioning**: Pipeline-first CRM built by salespeople for salespeople. Simple, visual, activity-driven.

**Strengths**:
- Drag-and-drop pipeline — easiest visual deal management
- Activity-based selling — focuses reps on next actions
- Fast setup — productive in hours, not days
- AI sales assistant suggests next steps
- Good mobile app for field sales
- Affordable entry point

**Weaknesses**:
- No marketing automation
- Limited customization compared to Attio or Salesforce
- Reporting is basic on lower tiers
- No free tier (14-day trial only)
- Can feel limiting for complex B2B sales with multiple stakeholders

**Pricing** (best-effort):

Pipedrive moved to a new 4-plan structure in 2025 (the old Essential/Advanced/Professional/Power/Enterprise names are retired). Current plans:
- Lite ($14/user/mo annual): Basic pipeline + contacts (was Essential)
- Growth ($39/user/mo annual): Email sync, automations, forecasting, lead tracking (was Advanced)
- Premium ($49/user/mo annual): Revenue forecasting, Smart Docs, LeadBooster, AI (was Professional/Power)
- Ultimate ($79/user/mo annual): Unlimited everything, advanced permissions, dedicated support (was Enterprise)

**Best for**: Outbound-heavy small teams (3-30 people) who want a simple, visual CRM focused on deal progression. SDR teams doing high-volume prospecting.

**Developer / platform-specific help**: For Pipedrive's API, webhooks, custom-field hash keys, token-based rate limits, or the v1→v2 migration (v1 shuts down 2026-07-31), use `/sales-pipedrive`. Note the API and webhooks are available on **every** plan — only the daily API token budget scales by tier.

## Close

**Positioning**: CRM built for high-velocity inside sales. Calling, emailing, and sequencing in one tool.

**Strengths**:
- Built-in power dialer and VoIP — no separate calling tool needed
- Email sequences and templates native to the CRM
- Activity tracking and sales reporting
- Fast search and bulk actions
- Smart Views for dynamic lead lists
- Good for founder-led sales with heavy phone outreach

**Weaknesses**:
- No marketing automation or inbound tools
- Smaller integration ecosystem
- Not designed for field sales or complex enterprise deals
- Limited customization of the data model
- Phone features are US/Canada focused

**Pricing** (best-effort):
- Solo ($9/user/mo annual, $19 monthly): Single-user core CRM + calling
- Essentials ($35/user/mo annual): Core CRM, sequences, calling
- Growth ($99/user/mo annual): Custom objects, advanced reporting, workflows
- Scale ($139/user/mo annual): Predictive dialer, call coaching, advanced controls

(Close renamed its plans to Solo/Essentials/Growth/Scale — the older Startup/Professional/Enterprise names are retired. Phone/dialer credits and Call Assistant are add-ons that raise effective cost.)

**Best for**: Inside sales teams doing high-volume cold calling. Startups with SDRs running call-heavy outbound sequences. Not for teams that need marketing or complex enterprise deal management.

## Zoho CRM

**Positioning**: Most features per dollar. Part of a massive suite (40+ Zoho apps). Budget-friendly with serious depth.

**Strengths**:
- Very affordable — competitive with enterprise features at mid-market pricing
- Zoho One bundle ($45/user/mo for 45+ apps including CRM, email, analytics, etc.)
- Zia AI assistant for predictions and recommendations
- Custom modules and fields
- Blueprint process management (guided selling)
- Strong for businesses also using Zoho Books, Zoho Desk, Zoho Campaigns

**Weaknesses**:
- UI feels dated compared to Attio or HubSpot
- Overwhelming breadth — too many options for small teams
- Integration ecosystem outside Zoho is smaller
- Support quality varies by tier
- Occasional performance issues on larger data sets

**Pricing** (best-effort):
- Free: 3 users, basic CRM
- Standard ($14/user/mo annual): Scoring rules, workflows, dashboards
- Professional ($23/user/mo annual): SalesSignals, Blueprint
- Enterprise ($40/user/mo annual): Zia AI, multi-user portals
- Ultimate ($52/user/mo annual): Advanced analytics, data enrichment

**Best for**: Budget-conscious startups that need breadth of features. Teams already using other Zoho products. Small businesses that want enterprise-like features without enterprise pricing.

## Bitrix24

**Positioning**: Free-forever all-in-one business suite (CRM + tasks + contact center + sites + collaboration), cloud or self-hosted on-prem. The go-to **free** option for solo founders/SMBs — a free Keap/Ontraport/Zoho/HubSpot-free alternative — that also scales to enterprise.

**Strengths**:
- **Free plan with unlimited users** (core CRM + tasks + contact center) — uniquely generous
- Very broad: CRM, projects, omnichannel contact center, website/store builder, marketing, HR
- Full method-based REST API (`crm.*`), inbound + outbound webhooks, OAuth 2.0, 740+ app Market, MCP server
- Smart Process Automation (custom CRM objects); self-hosted on-prem option for data control

**Weaknesses**:
- **Sprawling** — breadth = a real learning curve; CRM is one of many modules
- API is **method-based RPC** (`crm.deal.add`), not resource REST — a different mental model
- Rate-limited (~2 req/sec) — needs batching for bulk work
- UI/UX feels dense vs focused CRMs; paid tiers cap users per tier (not pure per-seat)

**Best for**: cost-sensitive solo founders/SMBs who want one free tool for CRM + ops + comms and don't mind the breadth/learning curve. **Platform skill**: `/sales-bitrix24`.

## Salesflare

**Positioning**: Automated CRM for small B2B teams. Minimal data entry — auto-enriches from email and calendar.

**Strengths**:
- Automatic data capture from inbox and calendar
- Auto-enrichment of company and contact data
- Built-in email tracking (opens, clicks)
- Simple pipeline management
- Good for founders who hate data entry

**Weaknesses**:
- Limited customization
- Small team focus — not designed to scale past 50 users
- Fewer integrations than major CRMs
- Basic reporting
- Less well-known — smaller community and ecosystem

**Pricing** (best-effort):
- Growth ($29/user/mo annual): Full CRM, email tracking
- Pro ($49/user/mo annual): Email sequences, custom dashboards
- Enterprise ($99/user/mo annual): Custom objects, audit log

**Best for**: Solo founders or tiny teams (1-5 people) who want automated data capture and hate manual CRM entry. B2B companies with a small number of high-value deals.

## Keap

**Positioning**: All-in-one CRM + marketing automation for small *service* businesses (formerly Infusionsoft; now owned by Thryv). CRM, drag-and-drop Campaign Builder, email/SMS, sales pipeline, invoicing, and payments in one tool. Positions as a HubSpot alternative.

**Strengths**:
- Genuine all-in-one — CRM, automation, email, SMS, invoicing, and payments without stitching tools together
- Powerful "When-Then" Campaign Builder for goal-based automation (lead follow-up, nurture, post-purchase)
- Native invoicing, quotes, recurring subscriptions, and payment processing — strong for service businesses that bill clients
- Built-in referral/affiliate partner program tracking
- Full REST API (v1/v2, OAuth 2.0 + Personal Access Tokens) with REST Hooks webhooks
- 20+ years of automation depth; long-term users describe it as "central to operations"

**Weaknesses**:
- Steep learning curve — the most-cited complaint; not plug-and-play, and many never clear it
- Per-contact pricing — the bill climbs as the list grows (vs flat-rate GoHighLevel); ~56% of Capterra reviewers call it "too expensive"
- High price floor (~$249-299/mo base) with no free tier — trial only
- Confusing dual product (Max Classic legacy engine vs the newer Keap Pro/Max/Ultimate UI); the Ultimate rollout introduced automation builder bugs
- Aggressive deliverability enforcement — accounts can be throttled/blocked after very few complaints, and unsubscribe-with-feedback counts as a complaint
- No native funnel/landing-page builder — users add Leadpages or ClickFunnels
- Smaller native-integration set than HubSpot

**Pricing** (best-effort):
- No free plan — free trial only
- Single Keap plan ~$249-299/mo (billed annually): 2 user licenses + starting contact tier (~1,500 contacts); **scales up with contact count**
- Additional users ~$39/user/mo
- Text/SMS marketing: 6-tier add-on (Tier 1 included → Tier 6 $279/mo for 25,000 messages)

**Best for**: Established small service businesses (coaches, agencies' clients, home services, consultants) that bill clients and want CRM + marketing automation + invoicing + payments in one tool, and have the patience to configure it. Not for teams wanting a cheap, simple, or flat-rate CRM, or those who need a native funnel builder.

**Existing skill**: `/sales-keap` — full platform help including Campaign Builder, deliverability, pricing/interfaces, and API/webhook integration

## Ontraport

**Positioning**: All-in-one CRM + marketing automation + payments + dynamic CMS on one unified database, for established small/mid-market businesses (ontraport.com). A direct Keap competitor; also compared to GoHighLevel and ActiveCampaign. Strong where CRM, deep automation, native payments, and membership/course pages must live in one tool.

**Strengths**:
- Genuine all-in-one — CRM, Campaign Builder automation, email/SMS, order forms/subscriptions, and a dynamic CMS (landing pages, courses, membership sites) without stitching tools together
- Deep, visual marketing automation with attribution from ad click to revenue and an embedded AI assistant
- Native payments — order forms, upsells/order bumps, subscriptions, decline recovery, customer portal
- Object-based REST API (base `https://api.ontraport.com/1`, `Api-Key` + `Api-Appid` headers) with webhooks; official SDKs on GitHub
- Built-in partner/affiliate program tracking (Pro+)

**Weaknesses**:
- Brutal learning curve — the #1 complaint; powerful but "not intuitive", weeks to ramp
- Per-contact pricing that escalates, with overages that stack unpredictably (~$600/mo reported at ~43k contacts); can cost more than it returns below ~$10k/mo revenue
- Email editor is a clunky "fake drag-and-drop" with a smaller template library than email-first tools
- Mixed deliverability reports; some overcharge/support complaints
- No free tier (14-day trial only); object-model API surprises first-time developers (no `/contacts` resource)

**Pricing** (best-effort):
- No free plan — 14-day trial only
- Basic ~$79/mo (1,000 contacts), Plus ~$147/mo, Pro ~$297/mo (adds reporting + partner programs), Enterprise ~$497/mo
- Additional users ~$46/user/mo; **per-contact pricing** scales the bill with list size

**Best for**: Established small/mid-market businesses (info-marketers, coaches, membership/service businesses) that want CRM + automation + payments + membership pages in one database and have the patience to configure it. Not for teams wanting a cheap, simple, or flat-rate CRM.

**Existing skill**: `/sales-ontraport` — full platform help including the object-based API, webhooks, pricing/plan gates, and automation

## EngageBay

**Positioning**: Affordable all-in-one CRM + marketing + sales + service suite for startups and SMBs (engagebay.com) — three modules (Marketing Bay, Sales & CRM Bay, Service Bay) on one shared contact database. Explicitly pitched as "HubSpot power at a fraction of the cost"; a budget Keap/Ontraport/HubSpot/Agile CRM alternative. Has a genuine free tier.

**Strengths**:
- Genuine all-in-one breadth — CRM, email/marketing automation, landing pages/forms, helpdesk tickets, and live chat in one cheap tool
- Free tier (250 contacts) plus low per-user plans; modules can be bought standalone (Marketing Bay / CRM Bay) for even less than the full suite
- REST API across contacts, companies, deals, tasks, tickets, products, custom fields, plus outbound webhooks and Java/.NET/JS/PHP SDKs
- High user-satisfaction scores for value; good fit for non-technical small teams

**Weaknesses**:
- API defaults to **XML** (must request JSON via header) and has no `Bearer`/OAuth flow — just a raw API-key header; rougher developer ergonomics than HubSpot/Pipedrive
- **No incoming webhooks** — you can only push data in via the REST API; outbound webhooks are also unsigned (no HMAC)
- Plan-gated monthly API-call quota and contact caps; automation-node and landing-page limits tighten on lower tiers
- Per-user *and* per-contact pricing — both seats and list growth raise the bill
- Smaller native-integration set and shallower automation depth than HubSpot/Ontraport; deliverability/support complaints at scale

**Pricing** (best-effort, All-in-One Suite, per user, captured 2026-06):
- Free $0 (250 contacts), Basic ~$14.99 (500), Growth ~$64.99 (5,000), Pro ~$119.99 (50,000 contacts, ~750k API calls/mo)
- Yearly/biennial billing discounts the monthly rate; Marketing Bay and CRM Bay sold separately at lower prices

**Best for**: Bootstrapped startups and small teams that want HubSpot-style breadth (CRM + marketing + service) on a tight budget and can live with rougher API ergonomics. Not for teams needing OAuth/signed webhooks, deep automation, or a large native-integration catalog.

**Existing skill**: `/sales-engagebay` — full platform help including the REST API (XML-vs-JSON, auth, cursor pagination), outbound-only webhooks, pricing/plan gates, and contact/deal sync recipes

## Salesmate

**Positioning**: AI-powered sales CRM for SMB and mid-market teams (salesmate.io) — contacts/companies, deal pipelines, activities, **built-in calling + SMS**, email sequences, marketing automation, Smart Flow workflows, a ticketing/team inbox, and the **Sandy AI** copilot. An affordable Pipedrive/Close/Freshsales alternative whose differentiator is native voice/SMS plus AI baked across the funnel.

**Strengths**:
- **Native calling + SMS** (power dialer, voicemail drop) rather than a bolted-on integration — calling feels first-class
- Genuine breadth at SMB pricing — CRM + sequences + marketing automation + tickets + AI copilot in one tool
- Consistently high ease-of-use and support ratings (~4.6 on G2)
- RESTful **v4 API** across contacts/companies/deals/activities/notes/custom modules, plus Zapier/Make/Pipedream

**Weaknesses**:
- **No inbound webhooks** in the public API — push events out via a Smart Flow API/Webhook action or iPaaS "Watch" triggers; write in via REST
- Header-based auth (`accessToken` + `x-linkname`) with confusing naming (Postman labels the access-key value `sessionToken`); offset (not cursor) pagination; **1500 calls/hour per link**
- **Sharp plan gates** — sequences + Sandy AI are Pro+, power dialer/custom modules/SLAs are Business+; Smart Flow automation is **credit-metered** and can stall
- Calling/SMS numbers are a paid add-on; 24/7 support is Enterprise-only (otherwise live-chat-first, weekday hours); occasional reporting/mobile/deliverability complaints

**Pricing** (best-effort, per user/mo, captured 2026-06; 15-day free trial):
- Basic $23 (CRM only, no sequences/AI), Pro $39 (sequences, Sandy AI, quotes), Business $63 (power dialer, custom modules, SLAs), Enterprise custom (onboarding from $1,999). Calling/SMS numbers from ~$1.1/mo + usage.

**Best for**: SMB/mid-market sales teams that want a built-in dialer + SMS and AI assistance without paying for HubSpot/Salesforce, and can live with header-auth ergonomics and no inbound webhooks. Not for teams needing inbound-webhook subscriptions or a deep native-integration catalog.

**Existing skill**: `/sales-salesmate` — full platform help including the v4 REST API (auth headers, offset pagination, 1500/hour limit, search bodies), Smart Flow/webhook patterns, pricing/plan gates, and contact/deal sync recipes

## Insightly

**Positioning**: Unified **CRM + project management + marketing + service** platform for SMB/mid-market (insightly.com). Its differentiator is that a **won Opportunity converts into a Project** on the same account graph — so the team that sells the work also tracks delivering it. A Pipedrive/Zoho/Copper alternative that's strongest for **agencies, consultancies, and professional-services** firms that both sell and deliver.

**Strengths**:
- Built-in **project management** linked to opportunities — rare among CRMs; avoids a separate PM tool for delivery
- Four modules (CRM, Marketing, Service, AppConnect) so the suite can grow with you; **AppConnect** is a built-in no-code iPaaS (2,000+ connectors)
- Clean **REST API v3.1** (read/write across contacts, organisations, opportunities, leads, projects, tasks) with custom fields and an official partner ecosystem
- Mid-market customization (custom fields everywhere; custom objects/products/quotes at Enterprise)

**Weaknesses**:
- **No email sequencing on any plan** — surprising at the price; outbound cadence needs a separate tool
- **Limited built-in reporting** — multi-object/cross-object reports are hard and project budgets don't roll up cleanly to opportunities; teams export to BI/warehouse
- Modules are **licensed separately** (CRM, Marketing, Service, AppConnect each priced on their own) so an "all-in-one" setup adds up
- Slow with large datasets; dense UI (many nav tabs); mixed support reputation
- **Webhooks require workflow automation (Professional+)** and retry only twice; **custom objects need Enterprise**

**Pricing** (best-effort; no permanent free tier, 14-day trial):
- **CRM**: Plus $29/user/mo (100k records), Professional $49 (adds workflow automation + AI Copilot, 250k records), Enterprise $99 (custom objects, products/quotes, sandboxes, 500k records) — billed annually
- **Marketing**: $99 / $499 / $999 per account/mo (by prospect count). **Service**: $29 / $49 / $99 per user/mo. **AppConnect**: $249–$1,899/mo by task volume. **All-in-One bundle** from $349/$899/$2,599 per month.

**Best for**: SMB/mid-market **services businesses** (agencies, consultancies, professional services) that want one tool for the deal *and* the delivery project, and that can live without native email sequencing. Not for outbound-heavy teams needing built-in cadences or teams needing deep native reporting.

**Developer / platform-specific help**: For Insightly's REST API v3.1 (pod-specific base URL, Base64 Basic auth, `top`/`skip`/`count_total` pagination, plan-gated daily quota, ETag/`If-Match`, `CUSTOMFIELDS` array) or its workflow-automation webhooks, use `/sales-insightly`.

## Maximizer

**Positioning**: Long-standing Canadian CRM (cloud "CRM Live" or **on-premise**) for SMB sales teams and, distinctively, **financial-services / wealth-advisory** firms (maximizer.com). Its differentiator is a purpose-built **Financial Advisor edition** — households, investment/insurance data views, family-connection visualization, compliance — at a fraction of Salesforce Financial Services Cloud's price. A Pipedrive/Salesforce alternative for **regulated and advisory teams** of roughly 5–50 seats, and one of the few remaining mainstream CRMs offering a self-hosted option.

**Strengths**:
- **Financial-services depth** out of the box (households, family connections, investment/insurance views) without a $325/user enterprise platform
- **Cloud or on-premise** deployment — useful for firms with data-residency or compliance constraints
- Tight **Microsoft Outlook / 365** email + calendar integration; clean leads-vs-deals separation; Dynamic Pipeline with methodologies
- Solid **Octopus API** (Maximizer.Web.Data, REST/JSON) + a separate **Webhooks API**, plus a Power BI connector for reporting

**Weaknesses**:
- **Email logging is click-heavy** — linking individual sent emails and syncing multiple mailboxes is a recurring complaint; thin native email automation
- **Reporting is cumbersome** for complex/multi-dimensional needs; teams export to Power BI/warehouse
- **Learning curve / dated UI** and reports of slow loading are the top review gripes
- Integrations beyond the Microsoft stack can be painful; **no free tier** (30-day trial), and the annual-license "rental" model raised effective cost vs. older perpetual licensing
- **Webhooks are fragile** — 2-second ACK, 3-attempt drop, no documented HMAC

**Pricing** (best-effort, annual billing; monthly ~10–20% higher; no free tier):
- **Base / For Sales** ~$65/user/mo · **Sales Leader** ~$79 · **Financial Advisor** ~$79–100 · **On-premise** quote
- API rate limits are **per-edition**: Core ~30 calls/10s, Business/Financial ~90/30s, Enterprise custom

**Best for**: Financial advisors, insurance agents, credit unions, and SMB sales teams that want advisor/household features or an on-premise option, and can accept dated UX and click-heavy email logging. Not for outbound-heavy teams needing rich sequencing, or teams wanting modern UX and deep native reporting.

**Developer / platform-specific help**: For Maximizer's Octopus API (POST-RPC `/Read` `/Create` `/Update` `/Delete`, Scope/Criteria/`Configuration.Drivers` query syntax, base64 record Keys, PAT/OAuth2 auth, per-edition rate limits) or its Webhooks API (targets + subscriptions, 2-second/3-attempt delivery), use `/sales-maximizer`.

## Spreadsheets

**Positioning**: Not a CRM, but where most startups start. Free, familiar, flexible.

**When spreadsheets work**:
- Under 50 active contacts/accounts
- Solo founder or 1-2 people managing relationships
- Simple tracking needs (name, company, status, last contacted)
- No complex pipeline stages or automation needs

**When to graduate to a CRM**:
- More than 5 people touch customer data
- Follow-ups getting dropped
- No visibility into what teammates discussed with prospects
- You're maintaining multiple sheets that reference each other
- You need reporting or forecasting
- You're copy-pasting to create pipeline views

**Migration tips**:
- Clean your spreadsheet first — deduplicate, normalize company names and job titles
- Most CRMs import CSV directly — map columns to CRM fields
- Don't try to import everything — start with active deals and recent contacts
- Keep the spreadsheet read-only for 2 weeks as a fallback
