# GetResponse Platform Guide

## Email marketing

- **Newsletter (broadcast)**: One-time email sends to lists or segments. Drag-and-drop editor with 100+ templates. AI content generator for subject lines and body copy.
- **A/B testing**: Test subject lines, content, send time, or from field. Up to 5 variants. Auto-send winner after test period.
- **Perfect Timing**: AI-based per-subscriber send time optimization — delivers emails when each contact is most likely to engage.
- **Time Travel**: Send at a specific local time regardless of subscriber timezone.
- **RSS-to-email**: Automatically send new blog posts to subscribers.

## Autoresponders

Time-based automated email sequences triggered by subscription date:
- Day 0: Welcome email (immediate)
- Day 1: Introduction / value proposition
- Day 3: Educational content
- Day 7: Offer / CTA
- Configure per-list — each list can have its own autoresponder sequence.
- Set delivery time, day of cycle, and tracking options per message.
- Available on all plans including Starter.

## Marketing automation

Visual workflow builder (Marketer plan+ required):
- **Triggers**: Subscribe, open email, click link, purchase, visit URL, tag applied, custom event, birthday/anniversary, score change
- **Actions**: Send email, send SMS, send web push, wait, tag, score, move to list, copy to list, webhook, custom event
- **Conditions**: If/else splits based on contact data, engagement, tags, scores, consent
- **Filters**: Narrow workflow to specific segments within a running automation
- **Templates**: Pre-built workflow templates for welcome series, abandoned cart, lead nurturing, re-engagement, post-purchase
- **Starter plan limit**: 1 automation workflow. Marketer+: unlimited.

## Conversion funnels

Pre-built funnel templates that combine landing pages, emails, and (optionally) webinars into a guided conversion path:
- **Lead magnet funnel**: Landing page → opt-in form → autoresponder sequence → download delivery
- **Sales funnel**: Landing page → sales page → order form → thank you page (integrates with payment processors)
- **Webinar funnel**: Registration page → confirmation email → reminder sequence → webinar → follow-up
- **List building funnel**: Social ads → landing page → signup form → welcome email
- Visual funnel dashboard shows conversion at each stage.
- Available on Marketer plan+.

## Webinars

Built-in webinar platform (Creator plan+):
- **Live webinars**: Screen sharing, chat, polls, whiteboard, call-to-action buttons, file sharing
- **On-demand webinars**: Record live webinars and make available for replay
- **Attendee limits**: Creator plan: 100 attendees (as of 2026 pricing). Enterprise/MAX: up to 1,000.
- **Integration**: Webinars integrate with automation workflows — trigger emails based on registration, attendance, or non-attendance.
- **Webinar funnels**: Combine with conversion funnels for end-to-end webinar marketing (registration → reminders → live event → follow-up → offer).

## Course creator

Create and sell online courses (Creator plan+):
- **Course builder**: Modules, lessons, quizzes, certificates
- **Content types**: Video, text, PDF, downloadable files
- **Student management**: Track progress, completion rates
- **Payment**: Integrate with Stripe for paid courses
- **Student limits**: Creator plan: up to 500 students. Higher tiers: more.
- **Premium newsletters**: Paid newsletter subscriptions — recurring revenue from content.

## SMS marketing

SMS campaigns and automation (**Enterprise / MAX plan only** as of 2026 — no longer included on Marketer/Creator):
- Send SMS broadcasts to contact lists
- SMS as an action in automation workflows (alongside email)
- SMS credits purchased separately
- Short codes and sender IDs vary by country

## Web push notifications

Browser push notifications:
- Opt-in prompt on your website
- Send push campaigns to opted-in subscribers
- Trigger push in automation workflows
- Available on all paid plans

## Live chat

Website chat widget:
- Embed on landing pages or external websites
- Capture visitor info for contact list
- Automated greeting messages
- Available on all paid plans

## Contact management & scoring

- **Lists**: Contacts organized into lists. Each list can have its own autoresponders.
- **Tags**: Apply tags manually, via import, or via automation rules
- **Custom fields**: Unlimited custom contact fields
- **Contact scoring**: Assign points based on engagement (opens, clicks, purchases, page visits). Score thresholds trigger automation actions. Marketer plan+ required.
- **Segmentation**: Filter by demographics, behavior, engagement, tags, scores, e-commerce activity. Dynamic segments auto-update.
- **Consent fields**: GDPR-compliant consent tracking

## E-commerce

- **Shopify**: Native integration — sync products, customers, orders, abandoned carts. Automated abandoned cart emails, product recommendations, post-purchase flows.
- **WooCommerce**: WordPress plugin — same capabilities as Shopify integration.
- **Magento, BigCommerce, PrestaShop**: Additional e-commerce connectors.
- **Product recommendations**: AI-powered product recommendations in emails based on purchase/browse history.
- **Promo codes**: Generate and distribute unique promo codes in emails.
- **Revenue tracking**: Attribute revenue to specific campaigns and automations.

## Data model

| Object | Key fields | Notes |
|---|---|---|
| **Contact** | `email`, `name`, `customFieldValues`, `tags`, `scoring`, `campaign` (list) | Contacts belong to campaigns (lists) |
| **Campaign** (list) | `campaignId`, `name`, `description`, `optinTypes` | "Campaign" = mailing list in GetResponse terminology |
| **Newsletter** | `newsletterId`, `name`, `subject`, `sendOn`, `campaign` | One-time email sends |
| **Autoresponder** | `autoresponderId`, `name`, `subject`, `triggerSettings` | Day-based automated emails |
| **Automation** | `workflowId`, `name`, `status` | Visual automation workflows |
| **Landing page** | `landingPageId`, `name`, `url` | Hosted landing pages |
| **Webinar** | `webinarId`, `name`, `startsOn`, `status` | Live or on-demand webinars |
| **Tag** | `tagId`, `name` | Applied to contacts for segmentation |
| **Custom field** | `customFieldId`, `name`, `type`, `values` | Contact custom attributes |

**Important terminology**: In GetResponse, a "campaign" means a **mailing list**, not an email send. An email send is called a "newsletter." This is a common source of confusion.

## API quick reference

| Action | Method & endpoint |
|---|---|
| Get contacts | `GET /v3/contacts` |
| Create contact | `POST /v3/contacts` |
| Update contact | `POST /v3/contacts/{contactId}` |
| Delete contact | `DELETE /v3/contacts/{contactId}` |
| Get campaigns (lists) | `GET /v3/campaigns` |
| Create campaign (list) | `POST /v3/campaigns` |
| Get newsletters | `GET /v3/newsletters` |
| Create newsletter | `POST /v3/newsletters` |
| Get autoresponders | `GET /v3/autoresponders` |
| Get tags | `GET /v3/tags` |
| Create tag | `POST /v3/tags` |
| Get custom fields | `GET /v3/custom-fields` |
| Get landing pages | `GET /v3/landing-pages` |
| Get webinars | `GET /v3/webinars` |

- **Base URL**: `https://api.getresponse.com/v3` (retail), `https://api3.getresponse360.com/v3` (MAX)
- **Auth**: `X-Auth-Token: api-key {your-api-key}` header. OAuth 2.0 also supported.
- **Rate limits**: 30,000 calls/10 min, 80 calls/sec, max 10 simultaneous requests. API keys expire after 90 days of inactivity.
- **MAX users**: Must include `X-Domain` header with client domain.

## Integrations

- **E-commerce**: Shopify, WooCommerce, Magento, BigCommerce, PrestaShop
- **CRM**: Salesforce (bidirectional sync), HubSpot, Zoho CRM
- **CMS**: WordPress, Squarespace, Wix
- **Webinar platforms**: Zoom, GoToWebinar (in addition to built-in webinars)
- **Payment**: Stripe, PayPal, Square (for courses and funnels)
- **Social/Ads**: Facebook Custom Audiences, Google Ads
- **Analytics**: Google Analytics
- **Zapier**: 150+ app connections
- **Callbacks** (legacy, query-string payloads, managed via `/v3/accounts/callbacks`): subscribe, open, click, goal reached, survey answer, unsubscribe
- **Webhooks** (current, JSON payloads, UI-configured): 13 event types incl. `contact_added`, `contact_opened_message`, `contact_clicked_message_link`, `contact_clicked_sms_link`, `contact_moved`, `contact_removed_link`, `contact_custom_field_changed`, `contacts_import_finished`. No HMAC signing — verify with a secret query-string parameter.
- **API**: Full REST API with OAuth 2.0 and API key auth

## Pricing

Re-verified 2026-06-13 against getresponse.com/pricing (1,000-contact tier, monthly; prices scale with contact count):
- **Free**: $0, 500 contacts, basic email + landing page + signup forms. (Free also gives a 14-day trial of premium features: 1 automation workflow, limited AI uses.)
- **Starter** (~$19/mo, 1K contacts): Unlimited monthly email sends, autoresponders, **1 automation workflow**, AI content generators, landing pages, signup forms/popups. 3 users.
- **Marketer** (~$59/mo, 1K contacts): Everything in Starter + **unlimited automation workflows**, contact scoring & tagging, advanced segmentation, abandoned-cart recovery, sales/conversion funnels, promo codes & revenue reports, e-commerce tracking, unlimited web push. 5 users.
- **Creator** (~$69/mo, 1K contacts): Everything in Marketer + website builder, course creator (up to 500 students), **webinars (up to 100 attendees)**, premium (paid) newsletter subscriptions. 5 users.
- **Enterprise / MAX** (custom, demo required): Everything + **SMS marketing**, mobile push, **transactional email** (MAX² add-on), dedicated IP, SSO, unlimited users, priority support, webinars up to 1,000 attendees.
- ~18% discount for annual billing. **Billing is based on peak contact count**; exceeding your tier auto-bumps you to the next bracket (1K → 2.5K → 5K → 10K → 25K → 50K → 100K).
- NOTE: SMS is now **Enterprise-only** (previously bundled lower); webinars moved to **Creator** at a **100-attendee** cap. Verify live before quoting.
