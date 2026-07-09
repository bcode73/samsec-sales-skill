# Platform-Specific Funnel Building Guide

Detailed per-platform funnel setup — page builders, checkout integration, A/B testing, automation, and best practices.

## Table of contents

- [In Groove.cm](#in-groovecm-detailed)
- [In ClickFunnels](#in-clickfunnels)
- [In GoHighLevel](#in-gohighlevel)
- [In Kartra](#in-kartra)
- [In Systeme.io](#in-systemeio)
- [In Builderall](#in-builderall)
- [In WordPress (+ Elementor or Thrive)](#in-wordpress--elementor-or-thrive)
- [In CartFlows](#in-cartflows)
- [In WPFunnels](#in-wpfunnels)
- [In FunnelKit](#in-funnelkit)
- [In Closum](#in-closum)
- [In Mailchimp](#in-mailchimp)
- [In GetResponse](#in-getresponse)
- [In Kit](#in-kit)
- [In SendPulse](#in-sendpulse)
- [In VWO](#in-vwo)
- [In Unbounce](#in-unbounce)
- [In Landingi](#in-landingi)
- [In Instapage](#in-instapage)
- [In Convertri](#in-convertri)
- [In SeedProd](#in-seedprod)
- [In Beaver Builder](#in-beaver-builder)
- [In Breakdance](#in-breakdance)
- [In Spectra](#in-spectra)
- [In Kadence Blocks](#in-kadence-blocks)
- [In GenerateBlocks](#in-generateblocks)
- [In Stackable](#in-stackable)
- [In Nexter Blocks](#in-nexter-blocks)
- [In Greenshift](#in-greenshift)
- [In Gutenverse](#in-gutenverse)
- [In GutenKit](#in-gutenkit)
- [In Superb Addons](#in-superb-addons)
- [In Jotform](#in-jotform)
- [In Wix](#in-wix)
- [In Framer](#in-framer)
- [In Other Tools](#in-other-tools)

## In Groove.cm (Detailed)

Groove.cm bundles funnel building, email, membership, and checkout into one ecosystem. Key components for funnels:

- **GroovePages** — Drag-and-drop page builder. Use "Funnel" mode (not "Site" mode) to create multi-step funnels with built-in page sequencing.
  - Create a new funnel project, then add pages as steps (opt-in, sales page, upsell, thank-you).
  - Use Groove's global blocks for consistent headers/footers across funnel steps.
  - Enable the built-in countdown timer element for urgency — it syncs across pages.
  - For split testing, duplicate a page within the funnel and use Groove's A/B test toggle. Traffic splits evenly by default.
- **GrooveSell** — Native checkout. Create products, then attach order forms directly to funnel pages. Set up order bumps and one-click upsells within GrooveSell (not GroovePages).
  - Upsell/downsell sequences are configured in GrooveSell under "Funnels" > "Upsell Flows."
  - Use GrooveSell's built-in affiliate program (GrooveAffiliate) for launch funnels.
- **GrooveMail** — Trigger post-funnel email sequences based on purchase or opt-in tags. Connect tags between GrooveSell and GrooveMail for segmentation.
- **GrooveMember** — If your funnel delivers a course or membership, GrooveMember handles access. Link product purchases in GrooveSell to membership levels.
- **Tips**: Groove's page load speed depends on image optimization — compress all images before uploading. Use Groove's built-in analytics (GroovePages > Stats) for page-level metrics, but supplement with Google Analytics or a pixel for traffic-source attribution.

## In ClickFunnels

ClickFunnels is the category-defining all-in-one funnel builder — now **ClickFunnels 2.0** (Classic/1.0 is legacy with a deprecated API). For full platform help (V2 API, webhooks, plan gates, migration, troubleshooting), use `/sales-clickfunnels`.

- **2.0 vs Classic**: 2.0 is a full rebuild (funnels, e-commerce, email/Workflows, CRM, courses, community) with the V2 REST API; Classic is the original funnel builder. They're separate products/logins — confirm which one before configuring.
- Use the funnel template library as a starting point — filter by funnel type (opt-in, sales, webinar, etc.). Each funnel step maps to a page; drag to reorder in the flow view.
- **A/B split tests**: "Create Variation" on any funnel step, then set traffic split percentages (split-test steps are also API-accessible in 2.0).
- **One-click upsells/order bumps**: configure in the funnel/step settings; requires a connected payment gateway (Stripe, etc.) with OTO enabled.
- **Stats** tab gives per-step conversion tracking; add Meta Pixel / GA via tracking-code settings.
- **Cost caveats**: ClickFunnels is among the highest-priced funnel builders and bills **email per-send**, so cost climbs with list size — segment to send less and run the math before migrating a large list in. Plans (best-effort): Startup ~$97 (20 funnels, 10k contacts), Pro ~$297 (unlimited + API access + Backpack affiliates).
- **Stability**: 2.0 still draws complaints about page previews not loading and under-tested features — build/test in a staging workspace before a launch, and don't cut over from Classic mid-launch.

## In GoHighLevel

> For full GoHighLevel platform help (v2 API, webhooks, sub-accounts/snapshots, SaaS-mode rebilling, plan gates), use `/sales-gohighlevel`.

- Build funnels under "Sites" > "Funnels." Add steps, assign templates or build from scratch.
- GoHighLevel excels at combining funnels with CRM pipelines — trigger automations when a contact hits a funnel step.
- Use "Workflows" (automations) to move contacts through pipeline stages based on funnel actions (opt-in, purchase, application submitted).
- Split testing is available per funnel step. Forms and surveys are native — useful for application funnels.
- Integrate with Stripe for payments. Upsell flows are configured via the order form settings.

## In Kartra

Kartra is an all-in-one for coaches/course creators (pages, email/SMS, checkout, memberships, video, webinars, affiliates) — a GoHighLevel/Kajabi peer without the agency layer. For full platform help (API, IPN webhooks, plan gates, troubleshooting), use `/sales-kartra`.

- Kartra's visual **funnel mapper & simulator** lets you map the entire funnel flow, including conditional branching, before building pages.
- **Behavioral adaptive marketing**: Kartra can show different page content based on tags, purchase history, or lead score.
- Helpdesk, memberships/courses, video hosting, and email/SMS are all native — strong for all-in-one setups.
- Use **Kartra Checkouts** for order bumps and 1-click upsells/downsells. Configure "Upsell/Downsell" under the product settings.
- **Analytics**: Kartra tracks end-to-end funnel metrics natively with revenue attribution — but real-time funnel analytics is gated to the Professional plan.
- **Plan gates that affect funnels**: automations, webinars, surveys/quizzes, and affiliate management require **Growth+**; the **API** (for syncing leads/tags to a CRM) and custom-code pages appear gated to **Professional**. Essentials caps you at 5 pages/1 product with a 5% transaction fee.
- **Speed caveat**: custom-domain pages route through a redirect that can slow load — compress assets and expect the extra hop.

## In Systeme.io

Systeme.io is a budget all-in-one for bootstrappers/solopreneurs — funnels, email, courses, community, affiliates, and webinars with a genuinely usable free plan. For full platform help (REST API, webhooks, plan limits, troubleshooting), use `/sales-systemeio`.

- **Funnel builder**: drag-and-drop funnel + website builder with templates. Trades design flexibility for speed/ease — fast to launch, but less polished than dedicated builders (Leadpages/Unbounce). Set expectations on pixel-level control.
- **Free plan is the hook**: 3 funnels, 1 course, 2,000 contacts, unlimited emails, and **0% transaction fees** at $0/mo — strong fit for makers validating a first offer before paying for anything.
- **Native checkout with 0% fees** on all plans (Stripe/PayPal) — order bumps and upsells built into the funnel. Good for low-ticket and tripwire funnels where fees matter.
- **Email + automation + CRM pipelines** are native — tag-based automations move contacts through the funnel. Workflow editor is simpler than GoHighLevel/ActiveCampaign.
- **Automated webinars** (Webinar plan $47+) enable evergreen webinar funnels end-to-end inside one tool.
- **Small native-integration ecosystem** is the main limitation — when a connector is missing, use the public REST API (`api.systeme.io`, `X-API-Key`), Zapier/Make/Pabbly/n8n, or webhooks (new sale, tag added) to wire the funnel into external tools.
- **Deliverability caveat**: sends can be inconsistent — authenticate the sending domain and keep lists clean so funnel follow-up emails land.

## In Builderall

Builderall is a budget all-in-one suite (website/funnel builders, MailingBoss email, SuperCheckout, courses, webinars, chatbot) aimed at non-technical solopreneurs who want everything in one bill. For full platform help (MailingBoss API, webhooks, plan gates, troubleshooting), use `/sales-builderall`.

- **Three page builders**: responsive, "pixel-perfect," and mobile-first. Build funnel steps as pages; the pixel-perfect builder gives the most control but is heavier to learn.
- **Plan gate to flag first**: the **funnel builder is usually on a higher tier (~$79.90/mo)**, not the free/entry (~$14.90–17/mo) plan. Don't pitch Builderall as a "cheap funnel builder" without checking the tier covers funnels. *(Pricing best-effort — verify.)*
- **Checkout via SuperCheckout**: native carts, order bumps, and upsells live in SuperCheckout (UI-built, no API) — attach to funnel pages and drive follow-up with MailingBoss tags on purchase.
- **Email is MailingBoss**: opt-ins flow into MailingBoss lists; tag-based automations move contacts through the funnel. MailingBoss is the *only* module with an API.
- **Breadth over depth**: templates skew dated and the builder is less refined than Leadpages/Unbounce or even ClickFunnels — fine for getting a working funnel live cheaply, not for pixel-level brand control.
- **Reliability caveat**: reviews report periodic outages (pages/checkout/email) and slow support — build/test ahead of a launch and keep a fallback for checkout/email.
- **Integration**: no broad REST API — wire funnels to external tools via the MailingBoss subscriber API, per-list inbound webhooks, or Zapier/Make/Pabbly/Integrately.

## In WordPress (+ Elementor or Thrive)

- Use a dedicated funnel plugin: CartFlows, WooFunnels (FunnelKit), or Thrive Suite.
- **CartFlows / FunnelKit**: Create funnel flows (opt-in > sales > upsell > thank-you), assign page builder templates, connect to WooCommerce for checkout.
- **Thrive Architect + Thrive Optimize**: Build pages in Thrive, use Thrive Optimize for A/B testing. Pair with Thrive Leads for opt-in forms.
- **Elementor + third-party**: Build pages in Elementor, use a separate checkout (ThriveCart, SamCart) embedded via iframe or redirect.
- WordPress funnels require more setup but offer full control over hosting, speed, and SEO.

## In CartFlows

- **WordPress/WooCommerce sales-funnel & checkout builder** (cartflows.com, by Brainstorm Force — Astra/Spectra makers; 200k+ installs): modern checkout layouts (one/two-column, multi-step, instant), custom checkout-field editor, **dynamic rule-based order bumps**, **one-click upsells/downsells** (post-purchase, charged to the original WooCommerce order), A/B split testing, opt-in/thank-you steps, funnel analytics, and prebuilt templates designed in **Elementor/Divi/Beaver Builder/Bricks/Spectra/Gutenberg**. The **checkout-first, lean** option — its defining contrast with FunnelKit is that it has **no built-in email/CRM** (connect a third-party ESP).
- **Automation surface**: **self-hosted WordPress only — no hosted REST API, no MCP**. Programmatic surface = **WP-CLI** (Pro; currently `wp cartflows license activate <key>`), **personalization shortcodes** (`[cartflows_order_fields field="first_name"]`, `[cartflows_url_fields]`), **Offer JS triggers/variables** on Upsell/Downsell steps (`{{order_id}}`/`{{txn_id}}`/`{{order_total}}` free; `{{offer_product_name/qty/price}}` Pro; Offer Accepted/Rejected scripts), **WordPress action/filter hooks**, **OttoKit (SureTriggers)/Zapier/Make** (1,000+ apps), and **Cart Abandonment Recovery** plugin **webhooks** (no published payload schema/HMAC — capture a live sample). **Funnel revenue = WooCommerce orders** (bumps + upsells) — read via the **WooCommerce REST API** (`/wp-json/wc/v3/orders`), filtering on the CartFlows flow order-meta; there is **no CartFlows read API**.
- **Watch-outs**: WordPress + WooCommerce required; order bumps, one-click upsells/downsells, A/B testing, the Pro offer-JS vars, and WP-CLI are **Pro**; the #1 support issue is the **checkout 404 / "Page Not Found"** (WooCommerce checkout page not created/assigned, or a deleted flow) and the funnel **falling back to the default WooCommerce checkout**; CartFlows has its own checkout-field editor that **conflicts with third-party field plugins**. Pricing best-effort (peers: FunnelKit ~$99.50–$399/yr, WPFunnels Pro): plugin tiers ~$99–$299/yr by site count, a **Suite** bundle (~$199/yr: CartFlows Pro + Modern Cart + Cart Abandonment Recovery + Power Coupons + OttoKit), and **lifetime** deals (~$699/$999).
- **Best for**: WooCommerce store owners who want a **lean, checkout-first WordPress funnel builder** with post-purchase upsells/order bumps and don't need a built-in CRM/email engine. **Platform skill**: `/sales-cartflows`.

## In Closum

Closum offers landing pages and forms as part of its omnichannel marketing automation platform:

- **Drag-and-drop builder**: Visual page builder — no coding required. Build landing pages with forms, CTAs, and lead capture elements
- **Pop-ups**: Timed, exit-intent, or scroll-triggered pop-ups for lead capture
- **Forms**: Embedded or pop-up forms for newsletter signups, lead magnets, event registrations
- **Dynamic segmentation**: Auto-tag and segment contacts based on which form or landing page they convert on
- **Automation integration**: Connect landing page form submissions directly to Closum automation workflows — trigger welcome emails, SMS confirmations, or WhatsApp messages automatically
- **Cross-channel follow-up**: Unlike most funnel builders, Closum natively follows up across email, SMS, WhatsApp, Telegram, and Web Push — no external tools needed
- **Plan limits**: Landing pages require the Advanced plan (EUR 35/mo, 15 pages included) or the add-on (EUR 15/mo for 4 pages). Not available on Zero or Growth plans.
- **Best for**: Lead capture funnels where the follow-up sequence needs to span multiple channels (email + SMS + WhatsApp). Not ideal for complex multi-step sales funnels with upsells/downsells — use ClickFunnels or Groove.cm for those.

## In Mailchimp

Mailchimp offers landing pages and basic funnel capabilities as part of its email marketing platform:

- **Landing pages**: Drag-and-drop builder with templates. Free on all plans (including Free tier). Good for opt-in pages, lead magnets, and event registrations.
- **Signup forms**: Embedded forms, pop-up forms, and hosted signup pages. Auto-connect to audience lists and trigger automations.
- **Website builder**: Basic website builder included — suitable for simple sites but not a full funnel builder.
- **Customer Journey integration**: Landing page signups feed directly into Customer Journey automations — trigger welcome sequences, tag-based segmentation, and nurture flows automatically.
- **Limitations**: Mailchimp is NOT a full funnel builder. No multi-step funnel flows, no upsell/downsell pages, no checkout/order forms, no A/B testing on landing pages (only on emails). For multi-step funnels with checkout, use ClickFunnels, Groove.cm, or GoHighLevel and connect to Mailchimp for email follow-up.
- **Best for**: Simple lead capture funnels (landing page → email sequence) where Mailchimp is already the email tool. For anything beyond opt-in capture, use a dedicated funnel builder and integrate.
- **Retargeting**: Mailchimp can create Facebook, Instagram, and Google retargeting audiences from your contacts — useful for funnel retargeting without a separate ad tool.

## In GetResponse

GetResponse offers Conversion Funnels — pre-built funnel templates that combine landing pages, emails, and webinars into a guided conversion path (Marketer plan+ required):

- **Funnel templates**: Lead magnet funnel, sales funnel, webinar funnel, list building funnel. Each template includes the necessary pages and email sequences pre-configured.
- **Landing pages**: Drag-and-drop builder with templates, forms, popups, and custom domains. Available on all paid plans.
- **Visual funnel dashboard**: See conversion rates at each stage — traffic → registration → email engagement → sale. Identify drop-off points visually.
- **Integrated checkout**: Connect Stripe, PayPal, or Square for payment collection within sales funnels. Order forms embedded in funnel pages.
- **Email follow-up**: Autoresponders and automation workflows trigger based on funnel stage — welcome emails for opt-ins, reminder sequences for webinar registrations, post-purchase follow-up.
- **Webinar funnels**: Unique to GetResponse — combine the built-in webinar platform (Creator plan+) with funnel pages for end-to-end webinar marketing. Registration → reminders → live event → replay → offer.
- **E-commerce funnels**: Shopify/WooCommerce integration enables abandoned cart funnels with product data.
- **Plan limits**: Conversion funnels require Marketer plan ($59/mo) or higher. Landing pages alone are available on all paid plans.
- **Best for**: Marketers who want funnel functionality integrated with email marketing, webinars, and courses in one platform. Not as flexible as ClickFunnels or Groove.cm for complex multi-step funnels with custom upsell flows, but simpler to set up for standard funnel types.

## In Kit

Kit offers landing pages and forms as growth tools for building email lists and selling digital products. For full platform help, use `/sales-kit`.

- **Landing pages**: Unlimited on all plans (including free). Hosted on Kit or custom domain. Template-based — optimized for email capture and digital product sales.
- **Opt-in forms**: Inline, modal, slide-in, sticky bar. Embed on any website. Each form can trigger different Visual Automations.
- **Creator Profile**: Free micro-website / bio link page — consolidate social media CTAs into one link.
- **Commerce pages**: Sell digital products and subscriptions with built-in checkout (Stripe required, 0.6% Kit fee).
- **A/B testing**: Not available on landing pages (only on email subject lines and content).
- **Automation integration**: Form submissions trigger Visual Automations — welcome sequences, tagging, conditional branching.
- **Best for**: Lead magnet funnels (landing page → email sequence) and digital product sales pages for creators. Not a full multi-step funnel builder — no upsell/downsell page flows, no order bumps. For complex multi-step funnels, use ClickFunnels or Groove.cm and connect to Kit for email follow-up.

## In SendPulse

SendPulse includes a drag-and-drop website and landing page builder as part of its marketing platform. For full platform help, use `/sales-sendpulse`.

- **Landing pages & websites**: Drag-and-drop builder with pre-built templates for lead capture, sales pages, and webinar registration. Free plan includes 1 website with up to 5 pages.
- **Subscription forms & pop-ups**: Built-in opt-in forms and pop-ups for lead capture — embed on SendPulse-hosted pages or external sites.
- **Custom domains**: Connect your own domain to SendPulse-hosted pages for a branded experience.
- **Platform integration**: Pages connect natively to SendPulse mailing lists, Automation 360 workflows, and CRM — form submissions flow directly into email sequences and deal pipelines.
- **Limitations**: SendPulse's website builder is simpler than dedicated funnel builders (ClickFunnels, Groove.cm). No multi-step funnel flows, no upsell/downsell pages, no order bumps or built-in checkout. For complex funnels, use a dedicated funnel builder and connect to SendPulse for email/SMS/push follow-up.
- **Best for**: Landing pages and simple sales pages where SendPulse is already the email/automation tool. Strong choice for lead magnet funnels (landing page → email sequence) that leverage SendPulse's multi-channel follow-up (email, SMS, web push, chatbots).

## In SWAI

SWAI.ai is an AI-Native Revenue OS that autonomously builds and optimizes funnels. For full platform help, use `/sales-swai`.

- **Goal-driven funnel creation**: Set a goal in plain English ("I need more qualified leads") and SWAI builds the entire funnel — landing page, email sequence, chat widget, and ads — automatically.
- **Landing pages**: Recently rebuilt native builder with full customization, AI-powered forms, script injection, and brand-tailored design. No third-party builder dependency.
- **AI forms**: Forms powered by AI agents that qualify and route leads intelligently based on responses.
- **Continuous optimization**: SWAI auto-tests and optimizes funnel elements — page design, email content, chat responses — without manual A/B test setup.
- **Integrated channels**: Funnels span email, landing pages, AI chat widget, and ad campaigns as a unified system rather than separate tools.
- **Limitations**: Less granular control than dedicated funnel builders (ClickFunnels, Groove.cm). No manual multi-step funnel flow editor — the AI decides the funnel structure based on your goal. No native checkout/upsell/downsell pages for e-commerce funnels.
- **Best for**: Agencies and small businesses that want AI to handle funnel creation and optimization end-to-end. Not ideal for teams that want manual control over every funnel step or complex e-commerce checkout flows.

## In MailerLite

MailerLite offers landing pages and basic funnel capabilities as part of its email marketing platform. For full platform help, use `/sales-mailerlite`.

- **Landing pages**: Drag-and-drop builder with templates, custom domains, SEO settings. 10 on Free, unlimited on paid plans. Good for opt-in pages, lead magnets, and product sales pages.
- **Signup forms**: Pop-up, embedded, and promotion (Advanced+). Exit-intent, scroll, and time-delay triggers. Auto-connect to groups and trigger automations.
- **Website builder**: Basic website and blog builder — suitable for simple sites but not a full funnel builder.
- **Automation integration**: Form and landing page signups feed directly into automation workflows — trigger welcome sequences, group assignments, and follow-up emails.
- **Digital products**: Sell ebooks and downloads directly via MailerLite with Stripe integration. 1 product on Free, 3 on Growing Business, unlimited on Advanced.
- **Paid newsletters**: Recurring subscription payments via Stripe — a funnel for content monetization.
- **E-commerce integration**: Shopify/WooCommerce connection enables abandoned cart and post-purchase funnel automation.
- **Limitations**: MailerLite is NOT a full funnel builder. No multi-step funnel flows, no upsell/downsell pages, no order bumps, no A/B testing on landing pages (only on emails). For multi-step funnels with checkout, use ClickFunnels, Groove.cm, or GoHighLevel and connect to MailerLite for email follow-up.
- **Best for**: Simple lead capture funnels (landing page → email sequence) and digital product sales where MailerLite is already the email tool. For anything beyond opt-in capture and basic product sales, use a dedicated funnel builder and integrate.

## In VWO

VWO (Visual Website Optimizer) is primarily an A/B testing and experimentation platform — it doesn't build funnels, but it tests and optimizes every step of them. For full platform help, use `/sales-vwo`.

- **A/B testing on funnel pages**: Use VWO Testing to run A/B, multivariate, or split URL tests on any funnel page. Visual editor for simple text/image changes, code editor for complex modifications.
- **What to test**: Follow the funnel A/B testing priority order (headline → CTA → hero image → social proof → price presentation → page length). VWO's visual editor makes headline and CTA tests fast to set up.
- **Heatmaps + session recordings**: Use VWO Insights to understand where visitors drop off. Click maps show engagement hotspots, scroll maps reveal if visitors reach the CTA, session recordings show individual user journeys through the funnel.
- **Personalization**: VWO Personalize can show different funnel content to different visitor segments (returning vs new, geo-location, traffic source, device type). Test personalized vs default with built-in A/B testing.
- **Feature flags for checkout**: Use VWO Feature Experimentation to gradually roll out new checkout flows or pricing page redesigns to a percentage of users before going site-wide.
- **Statistical guidance**: VWO uses Bayesian statistics. Wait for 95%+ probability to be best and at least 100 conversions per variation. Run for a minimum of 7 days to capture weekday/weekend variation.
- **SmartCode placement**: VWO's JavaScript snippet must be in `<head>` loaded synchronously to avoid flash of original content (FOOC). This applies to every funnel page being tested.
- **Pricing note**: A/B testing starts on the Growth plan (~$198-$314/mo). Personalization and advanced features require Pro or Enterprise. MTU quota exhaustion stops all tests mid-month.
- **Best for**: Optimizing existing funnel pages through systematic testing. Pair VWO with a funnel builder (ClickFunnels, Groove, GoHighLevel) — VWO tests what you've built, it doesn't build the funnel.

## In Leadpages

Leadpages is a landing page builder focused on lead capture and simple sales pages — not a full multi-step funnel builder. For full platform help, use `/sales-leadpages`.

- **Landing pages**: Drag-and-drop builder with 250+ templates. Grid-based layout (elements snap to positions, not freeform). Templates filterable by conversion rate — start with proven performers.
- **Leadmeter**: Real-time conversion scoring — analyzes your page and suggests specific improvements before publishing. Always run this before going live.
- **Pop-ups & alert bars**: Exit-intent, timed, scroll-triggered, click-triggered pop-ups. Alert bars for site-wide promotions. Deploy on any website via JavaScript embed code — not limited to Leadpages-hosted pages.
- **A/B testing**: Split test landing page variants with traffic distribution control. **Pro plan only ($99/mo)** — not available on Standard ($49/mo). This is the biggest plan-gated feature.
- **Payments**: Stripe checkout embedded in landing pages for one-time or recurring payments. Not a full checkout system — no order bumps, upsells, or cart. For those, use ThriveCart or SamCart and redirect from Leadpages.
- **AI features**: AI headline and copy generation, AI image creation, Leadmeter AI conversion recommendations.
- **Integrations**: 90+ native integrations (Mailchimp, ActiveCampaign, Klaviyo, HubSpot, Stripe, Zapier). WordPress plugin publishes Leadpages pages to your WordPress domain.
- **Plan limits**: Standard plan ($49/mo) caps at 5 landing pages and 1 custom domain. Pro ($99/mo) removes page limits and adds A/B testing and 3 domains.
- **Best for**: Simple lead capture funnels (landing page → email sequence) and standalone sales pages for solopreneurs and small businesses. Not ideal for multi-step funnels with upsells/downsells — use ClickFunnels, Groove.cm, or GoHighLevel for those. Stronger than Mailchimp/Kit for landing page design, but less flexible than Unbounce or Instapage for custom layouts.

## In Unbounce

Unbounce is a dedicated landing page builder and CRO platform focused on conversion optimization. For full platform help, use `/sales-unbounce`.

- **Landing pages**: Drag-and-drop Smart Builder with 100+ industry-specific templates. AI-suggested layouts based on industry and goal. Classic Builder available for pixel-level control. Custom CSS/JS injection for advanced customization.
- **Smart Traffic (AI optimization)**: Automatically routes each visitor to the page variant most likely to convert them. Analyzes location, device, browser, timezone, OS. Average 30% conversion lift. Starts optimizing after ~50 visits. **Requires Optimize plan ($249+/mo)**.
- **A/B testing**: Create page variants and split traffic between them. Statistical conversion reporting. **Requires Experiment plan ($149+/mo)**.
- **Dynamic Text Replacement (DTR)**: Swap landing page text based on URL parameters — match PPC ad copy to landing page headlines automatically. **Requires Experiment plan**.
- **Popups & sticky bars**: 50+ templates, trigger by exit-intent, scroll, click, or delay. Deploy on any website via JS embed. Available on all plans.
- **AMP pages**: Mobile-optimized pages that load in ~0.5 seconds (85% faster). Ideal for speed-critical PPC campaigns.
- **Smart Copy**: AI copywriting for headlines, CTAs, descriptions. 45+ templates. Built into builder + standalone Chrome extension. Available on all plans.
- **Page speed caveat**: Average 2.8-second load time — slower than competitors. Compress images to WebP, defer scripts, use AMP for speed-critical campaigns.
- **Plan limits**: Build ($99/mo) — unlimited pages, no A/B testing or DTR. Experiment ($149/mo) — adds A/B testing, DTR, 30K visitors. Optimize ($249/mo) — adds Smart Traffic, 50K visitors. Visitor caps with 30% overage penalties.
- **Integrations**: Native (Salesforce, HubSpot, Mailchimp, Marketo), 60+ Zapier in-app, 900+ via Zapier, webhooks, REST API.
- **Limitations**: NOT a full funnel builder — no multi-step funnel flows, no upsell/downsell pages, no checkout/order forms, no order bumps. For multi-step funnels, use ClickFunnels, Groove.cm, or GoHighLevel and send traffic to Unbounce landing pages for specific conversion steps.
- **Best for**: PPC marketers and agencies running Google/Meta ads who want the highest conversion rates on standalone landing pages. Smart Traffic is the standout feature for high-traffic campaigns. More powerful than Leadpages (AI optimization, freeform layout) but significantly more expensive ($99 vs $49 starting). Connect to a separate email tool and checkout tool.

## In Landingi

Landingi is an AI landing page builder ("landing page operation system") — single pages, pop-ups, and lead capture, not a multi-step funnel/checkout builder. For full platform help, use `/sales-landingi`.

- **Landing pages**: Drag-and-drop Visual Builder + 400+ templates; **Lunar** AI page generator (brief → page) and AI copy/SEO. Trades pixel-level freedom for speed — advanced layouts often need HTML/CSS (less freeform than Unbounce/Instapage).
- **Optimization**: **A/B testing**, **EventTracker** (click/engagement), **Smart Sections** (reusable sections synced across pages), and **Dynamic Text Replacement (DTR)** for ad-to-page message match — all **gated to Optimize ($119/mo) and up**.
- **Scale**: **Programmatic landing pages** (bulk-generate from a data source), agency sub-accounts/white-label, and the **Orbit MCP server** (connects Lunar + Solis to your LLM) — **gated to Scale ($229/mo+)**.
- **Lead capture & payments**: Form builder with lead export; sell products/services via PayPal/Stripe/PayU. Not a full cart — no order bumps/upsells; redirect to ThriveCart/SamCart for those.
- **Automation**: REST API (`api.landingi.com`, `X-Api-Key` or OAuth 2.0 Bearer) for landing pages / leads / `forms/{id}/submissions`; **per-form webhooks** (fire on submit, GET/POST, field mapping, no published HMAC); WordPress plugin; 170+ native integrations + Zapier. AI features consume a monthly **credit** pool.
- **Plan limits**: Build $24/mo (10 pages, 2,000 visits, 1 domain), Optimize $119/mo (100 pages, 30k visits, A/B testing), Scale $229/mo+ (unlimited pages, 100k–500k visits, programmatic + Orbit), Enterprise. Each tier caps monthly visits.
- **Best for**: solopreneurs, creators, and small marketing teams who want AI-assisted, A/B-tested landing pages at a lower price than Unbounce/Instapage — and bulk programmatic pages on Scale. Pair with a separate email/CRM tool. Note: custom-domain connection is slow and not fully automated (the #1 complaint).

## In Instapage

Instapage is a premium AI landing page + **post-click conversion** platform (owned by airSlate) for PPC/performance marketers and agencies — single landing pages and ad-matched variants, not a multi-step checkout funnel. For full platform help, use `/sales-instapage`.

- **Landing pages**: Pixel-precise drag-and-drop builder, AI Content Generator, **Instablocks®/Global Blocks** (reusable blocks updated across many pages), **AMP + Thor Render Engine** for ~0.5s mobile pages.
- **Ad alignment**: **AdMap®** visualizes ad-campaign structure and maps each ad → landing page; **Collections** group page variants per audience/campaign. Built for ad-to-page message match at scale.
- **Optimization**: **A/B testing + AI Experiments** (AI auto-allocates traffic to winners) and **Personalization / Dynamic Text Replacement (DTR)** are **Optimize ($199/mo)+**; **heatmaps**, ad-to-page personalization, root-domain publishing, Global Elements, SSO, and Direct Lead Bypass are **Convert (custom/enterprise) only**.
- **Lead capture**: forms with autoresponder/email; leads flow out via the per-form **Form Submit webhook** (POST, but internal `field_N` IDs not labels, 20s endpoint timeout, no documented HMAC) or the REST API.
- **Automation**: REST API (`api.instapage.com/v1`, **Bearer personal token**) for workspaces / pages / collections / `submissions` / analytics; **200 req/min per token+IP plus a per-plan daily quota** (Create 5,000 / Optimize 10–15k / Convert 30k+, reset 00:00 UTC, both → 429 + `Retry-After`); 120+ native integrations + Zapier "New Form Submission" trigger; WordPress plugin.
- **Plan limits**: Create $99/mo (15k visitors, no A/B testing/heatmaps), Optimize $199/mo (30–50k visitors, A/B testing + AI Experiments + DTR), Convert custom (heatmaps, ad-to-page personalization, root-domain publishing). 14-day trial on Create/Optimize only (2,500-visitor cap, CC required); no trial on Convert.
- **Limitations**: NOT a full funnel/checkout builder — no multi-step funnel flows, upsell/downsell pages, order bumps, or cart. Send Instapage landing pages into a checkout (ThriveCart/SamCart) or use ClickFunnels/Groove.cm/GoHighLevel for multi-step flows.
- **Best for**: PPC marketers and agencies running Google/Meta ads who want the deepest post-click testing/personalization and ad-to-page mapping — the **high-end** alternative to Unbounce, and pricier than Landingi/Leadpages. Pair with a separate email/CRM and checkout tool.

## In Convertri

Convertri is a speed-focused funnel + landing-page builder ("world's fastest") with a free-form drag-anywhere editor AND a built-in cart, upsells, and membership delivery — so it spans landing pages through checkout, unlike Landingi/Instapage. For full platform help, use `/sales-convertri`.

- **Pages & funnels**: Free-form "Photoshop-for-browser" editor (no rows/columns), ready blocks, mobile-specific design, CDN hosting + free SSL for sub-3s pages, **page importer** (clone pages from other builders, Maximize), split testing, and **Dynamic Text Replacement (DTR)** for ad-to-page message match.
- **Sell**: Integrated **shopping cart** with **one-click upsells** and **bump sells** (Stripe/PayPal), **membership delivery** (Scale+), and **interactive video** (buy buttons at video points, pixel firing on progress) — a fuller commerce stack than pure landing-page tools.
- **Automation**: **No public REST API** — you cannot create/read pages or funnels programmatically. Data-out is the **Zapier API key** (Account → Integrations → Zapier; 8 triggers incl. New Product Sale, Product Refund, Subscription Cancelled) + **custom webhooks** (Sale/Rebill/Rebill Cancellation/Refund/Lead Capture). Webhooks carry `cverify` (SHA-1, first 8 chars uppercased) for verification; amounts are in pennies. Up to 5 webhooks/form, unlimited/product.
- **Plan limits**: Convert $99/mo (100 pages, 5 domains, 250k impressions/mo), Scale ~$199/mo (unlimited pages, 10 domains, 500k impressions, membership + video hosting + A/B testing + DTR), Maximize $299/mo (unlimited everything, client sub-accounts, page importer, custom HTML). **Impression overage $30/250k**; video bandwidth 100GB/mo then $10/100GB; 14-day trial.
- **Gotchas**: Zapier times out if a funnel has too many pages (keep **≤20 pages/funnel**); impression-metered pricing surprises high-traffic users; $99/mo entry is steep vs LanderLab/Carrd.
- **Best for**: marketers/sellers who want fast pages **plus** a built-in cart + members area in one tool without a REST API. If you need programmatic page creation, choose Landingi/Instapage (REST API) or a WordPress builder (CartFlows/FunnelKit/WPFunnels) instead.

## In SeedProd

SeedProd is a self-hosted **WordPress** drag-and-drop website + landing-page builder plugin (by Awesome Motive) — the WordPress-native alternative to hosted builders like Leadpages/Unbounce/Instapage. It builds the funnel's *pages* (opt-in, sales, webinar, thank-you, coming-soon, 404) and can replace the whole theme; it is **not** an all-in-one (no native cart, no email sequences, no A/B testing). For full platform help, use `/sales-seedprod`.

- **Pages & theme**: Drag-and-drop builder (90+ Pro blocks), 300+ templates, **Theme Builder** (headers/footers/templates — Plus+), Smart Sections (reusable blocks), built-in **Coming Soon / Maintenance / 404 / Login** pages, and **Dynamic Text** (Pro+) for ad-to-page message match.
- **Lead capture**: Opt-in blocks write subscribers to **13 native ESPs** (Mailchimp, ConvertKit/Kit, ActiveCampaign, Brevo, AWeber, Drip, GetResponse, MailerLite…) on all tiers, with reCAPTCHA spam protection — pair with `/sales-email-marketing` for the sequence.
- **Checkout**: No native cart — renders **WooCommerce** (Elite only) and **Easy Digital Downloads** product/cart/checkout blocks via shortcodes, or embed/redirect to ThriveCart/SamCart. For commerce strategy use `/sales-checkout`.
- **Automation**: No public outbound REST API or webhook. Surface = the **WordPress Abilities API** (WP 6.9 + SeedProd 6.20.0+) exposing 8 named actions (`get-status`, `toggle-coming-soon`/`-maintenance`, `list-pages`, `save-page`, `toggle-theme`, `import-theme`, `activate-license`) to AI tools/REST clients; **permission filters** (`add_filter`) for capability gating; **shortcodes**; and **Zapier** (3000+, Pro+). Lead data exits via the ESP/Zapier.
- **Plan limits**: Basic $79/yr (1 site, 50 templates), Plus $199 (3 sites, +Theme Builder), Pro $399 (5 sites, 300+ templates, +Zapier, +Dynamic Text), Elite $599 (100 sites, +WooCommerce, +Domain Mapping). Annual, **intro-priced — renews at full rate**; free version on WordPress.org.
- **Gotchas**: Coming-soon/maintenance mode can lock the whole site (and you) out even after deactivating — toggle off + clear cache *before* deactivating; **no native A/B testing/heatmaps/analytics** (add VWO/Clarity); WooCommerce + Domain Mapping are **Elite-only**; nested-div output can hurt Core Web Vitals on heavy pages.
- **Best for**: WordPress owners who want pages + a full theme under their own hosting/SEO control without a hosted SaaS, and who'll bolt on a cart + ESP. If you need a built-in cart or programmatic page creation via REST, choose an all-in-one (ClickFunnels/Kartra) or a hosted builder with an API (Landingi/Instapage) instead.

## In Beaver Builder

Beaver Builder is a **standalone, drag-and-drop WordPress page builder** (by **FastLine Media**) — unlike SeedProd it's a mature builder known for **stability, clean/semantic markup, and low lock-in**; unlike Spectra/Kadence it's **not** Gutenberg-native (it builds pages as **Rows → Columns → Modules** in its own live front-end editor over any theme). It builds the funnel's *pages*; it is **not** an all-in-one (no native cart, no email sequences, no A/B testing). For full platform help, use `/sales-beaver-builder`.

- **Pages & modules**: Live front-end editor with **Rows/Columns** layout + **Modules** (Heading, Photo, Button, Gallery, Slider, Tabs, HTML, **Subscribe Form**, Posts…), reusable **Templates** and **Saved Rows/Modules** (optionally **global**), and the lightweight **Beaver Builder Theme**. **Beaver Themer** (on all paid tiers) adds dynamic **headers/footers/archives/singular/404** templates with **Field Connections** (WordPress/custom-field/**ACF**/EDD/The Events Calendar/**WooCommerce** data) and a **Loop Builder** for dynamic listings.
- **Lead capture**: the built-in **Subscribe Form** module writes to a connected ESP (Mailchimp etc.; extend services via `fl_builder_subscribe_form_services`); for arbitrary destinations use a third-party form plugin + Zapier. Pair with `/sales-email-marketing` for the sequence.
- **Checkout**: no native cart — build/customize **WooCommerce** templates with Themer (WooCommerce is the cart), or pair with a WooCommerce funnel plugin (CartFlows officially supports Beaver Builder for step design / FunnelKit) for order bumps + upsells. For strategy use `/sales-checkout`.
- **Automation**: **no hosted REST API or outbound webhook** (it's a WP plugin). The real developer surface is a **PHP API** — **custom modules** (extend `FLBuilderModule`, register with `FLBuilder::register_module()`) + a large **`fl_builder_*` hooks/filters** surface (searchable Hooks Reference at hooks.wpbeaverbuilder.com) — plus the **WordPress core REST API/WP-CLI** (a page's layout is `post_content` + the serialized **`_fl_builder_data`** post meta — best-effort, undocumented; parse server-side). For event-driven flows hook `save_post`/`publish` and POST yourself.
- **Plan limits**: Starter ~$89/yr (1 site), Plus ~$179 (3), Professional ~$299 (50, +Multisite), Unlimited ~$546 (∞, +White Labeling); **Themer + Loop Builder + WooCommerce ship on all paid tiers**; free **Lite** (WordPress.org) = reduced modules, no Themer/templates. *(Pricing best-effort — verify.)*
- **Gotchas**: after a migration the builder can be **deactivated on all pages except the home page** → run a **serialized-data-safe search-replace** (WP-CLI `search-replace --all-tables`) + clear cache + re-save; **"not working after upgrading"** = cache/stale-CSS or plugin/theme conflict (update BB+Themer+Theme together, clear caches, re-save); clean markup ≠ auto-fast — **big pages still load/edit slowly** (optimize images, cache, split pages); **multisite = Professional+**, **white label = Unlimited-only**; no native A/B testing/heatmaps (add VWO/Clarity). **Upside: deactivating BB leaves text cleanly in the default editor** (low lock-in vs block plugins).
- **Best for**: freelancers/agencies who want a **stable, clean-markup** builder with predictable client handoffs and low lock-in, building pages under their own hosting/SEO and bolting on a cart (WooCommerce/CartFlows) + ESP. If you want the leanest Gutenberg-native output choose Spectra/GenerateBlocks; if you need a built-in cart, hosted REST API, or split testing, choose an all-in-one (ClickFunnels/Kartra), a WooCommerce funnel plugin (CartFlows/FunnelKit), or a hosted builder with an API (Landingi/Instapage) instead.

## In Breakdance

Breakdance is a **standalone visual website/page builder** for WordPress (by **Soflyy**, the **Oxygen** makers) — like Beaver Builder it is **not** a Gutenberg block plugin: it builds funnel *pages* in its own front-end editor and is **themeless by default** (it can replace the theme entirely), closer to Elementor/Oxygen. **Oxygen 6 runs on the Breakdance engine.** It is **not** an all-in-one (no native cart beyond WooCommerce, no email sequences, no A/B testing). For full platform help, use `/sales-breakdance`.

- **Pages & elements**: front-end editor building **Sections/Elements** (~80 free / ~145 Pro), **Templates** + a **Design Library**, **Global Blocks**, headers/footers, **Dynamic Data** (post loops, repeaters, conditional display), a **WooCommerce Builder** (product/shop/cart/checkout templates), and **Element Studio** (built-in IDE for custom elements + code). Markets clean markup, conditional asset loading (~45 KB blank page), and jQuery-independence.
- **Lead capture**: the built-in **Form Builder** (Pro — multi-step, conditional fields, honeypot + reCAPTCHA v3) runs **Actions After Submit**: Store Submission, Email, native ESP/CRM integrations (e.g. Mailchimp/ActiveCampaign), or a **Webhook action** that POSTs mapped fields to any URL (Zapier/Make). For server-side delivery, write a **custom Form Action** (PHP, `Breakdance\Forms\Actions\Action`). Pair with `/sales-email-marketing` for the sequence.
- **Checkout**: no native cart — build/customize **WooCommerce** product/cart/checkout templates with the WooCommerce Builder (WooCommerce is the cart), or pair with a WooCommerce funnel plugin (CartFlows supports Breakdance for step design / FunnelKit) for order bumps + upsells. For strategy use `/sales-checkout`.
- **Automation**: **no hosted REST API or platform outbound webhook** (it's a WP plugin). The real developer surface is a **PHP API** — **Form Actions API**, **Dynamic Data Field API**, **Conditions API** (element display), `breakdance_*` hooks/filters, and **AI endpoint filters** (`breakdance_ai_api_endpoint`/`breakdance_ai_model` route Breakdance AI to OpenRouter/Claude) — plus the **WordPress core REST API** (the page *layout* is opaque post meta, not portable block markup; REST manages the post + scrapes rendered HTML). The form **Webhook action** is the no-code outbound path. Register extensions on `init` with `function_exists`/`class_exists` guards.
- **Plan limits**: free **Breakdance Free** (WordPress.org, ~80 elements, core builder); **Pro ~$199.99/yr** for unlimited sites + unlimited domain activations (full ~145 elements, WooCommerce Builder, Form/Popup Builder, Global Blocks, Client Mode); Pro + AI bundle ~$249.99. **No lifetime plan** (annual only) but a **price-lock guarantee** at renewal; 60-day refund. *(Pricing best-effort — verify.)*
- **Gotchas**: **spam plugins can't stop the Email action** — even when a spam filter blocks storage, the Email notification can still send (order the spam-check action above Store/Email, or remove Email and notify via the Webhook action + Make/Zapier); honeypot is off by default and **reCAPTCHA is v3-only**; the **AI settings UI doesn't reflect the endpoint/model filters** (verify via console + provider usage); **no lifetime plan**; **themeless by default** means your theme's templates may not apply; **Oxygen Classic** migration uses a third-party JSON converter (e.g. TransferForge), not a native importer; slow pages are usually **misuse** (nesting, Dynamic Data loops, images, caching), not the builder; no native A/B testing/heatmaps (add VWO/Clarity).
- **Best for**: freelancers/agencies/makers who want a **clean-markup, themeless standalone builder** with a real PHP extension API (custom form actions, dynamic data, conditions) and provider-swappable AI, building pages under their own hosting/SEO and bolting on a cart (WooCommerce/CartFlows) + ESP. If you want a Gutenberg-native block plugin choose Spectra/Kadence/GenerateBlocks; if you need a built-in cart, hosted REST API, or split testing, choose an all-in-one (ClickFunnels/Kartra), a WooCommerce funnel plugin (CartFlows/FunnelKit), or a hosted builder with an API (Landingi/Instapage) instead.

## In Spectra

Spectra is a **Gutenberg-native** WordPress website/page builder plugin (by **Brainstorm Force** — Astra/CartFlows makers; formerly Ultimate Addons for Gutenberg, 1M+ installs). It **extends** the native block editor rather than replacing it (the contrast with Elementor/Divi and even SeedProd), so funnel *pages* are built as standard WordPress blocks. It is **not** an all-in-one — no native cart, no email sequences, no A/B testing. For full platform help, use `/sales-spectra`.

- **Pages & blocks**: 30+ blocks (free) — flexbox **Container**, Post Grid/Carousel, Sliders, Forms, FAQ/Schema, Countdown, Testimonials — plus **Starter Templates**, **Popup Builder**, **Coming Soon mode**, animations, local Google Fonts (GDPR), Global Styles, and Spectra AI. **Pro** adds **Loop Builder**, **Dynamic Content** (bind to post meta/ACF), **display conditions**, role permissions, and white label.
- **Lead capture**: Form/Newsletter blocks with reCAPTCHA write to email/ESP via the configured integration; **no native webhook** — for arbitrary destinations route through a connected form plugin (Gravity Forms/FluentForms) or the ESP. Pair with `/sales-email-marketing` for the sequence.
- **Checkout**: no native cart — it builds the pages; add commerce via WooCommerce/SureCart blocks or pair with **CartFlows** (same makers) for funnel checkout + upsells. For strategy use `/sales-checkout`.
- **Automation**: no hosted REST API or outbound webhook (it's a WP plugin). Surface = the **WordPress REST API** (block markup is `uagb/`-namespaced in `post_content`) + Spectra's **public actions/filters** — `render_block`, `uagb_post_query_args_grid/masonry/carousel` (Post block queries), `spectra_slider_params`, `spectra_countdown_context`, `spectra_pro_gs_theme_colors`, and `spectra_pro_rest_api_get_controllers` (register a custom REST controller, Pro v2); design-library role gating via `ast_block_template_capability_additional_roles`.
- **Plan limits**: Free (WordPress.org, 30+ blocks), **Spectra Pro** (~$49–69/yr, lifetime ~$199), **Essential Toolkit** (~$79–119/yr, +Astra Pro), **Business Toolkit** (~$149–159/yr, +SureFeedback/CartFlows/etc.). Annual + intro-priced; 14-day refund. *(Pricing best-effort — verify.)*
- **Gotchas**: editor can be **slow/freezing on long posts** (esp. Spectra Pro); **Spectra CSS may not load on inner pages** (regenerate assets + set CSS file generation, clear cache); Post Grid/Taxonomy blocks can render distorted in templates; **Pro-only blocks fall back to fallback content** if Pro is deactivated/expires; no native A/B testing/heatmaps (add VWO/Clarity).
- **Best for**: WordPress owners who want to build funnel pages **on native Gutenberg** with lean DOM output and their own hosting/SEO control, bolting on a cart (CartFlows/WooCommerce) and ESP. If you need a built-in cart, programmatic page creation via REST, or split testing, choose an all-in-one (ClickFunnels/Kartra), a WooCommerce funnel plugin (CartFlows/FunnelKit), or a hosted builder with an API (Landingi/Instapage) instead.

## In Kadence Blocks

Kadence Blocks is a **Gutenberg page-builder block plugin** for WordPress (by **StellarWP / Liquid Web**; 600k+ installs, GPLv2, open source). Like Spectra it **extends** the native block editor rather than replacing it, so funnel *pages* are built as standard WordPress blocks — it's the closest Spectra/GenerateBlocks rival. It is **not** an all-in-one — no native cart (beyond WooCommerce/Shop Kit), no email sequences, no A/B testing. For full platform help, use `/sales-kadence`.

- **Pages & blocks**: 20+ blocks (free) — **Row Layout/Section** flexbox containers, **Advanced Form**, Advanced Gallery, Tabs, Accordion, Posts, Testimonials, Info Box, Icon List, Countdown, Count Up, Table of Contents, Lottie — plus the **Design Library** of pre-built patterns. **Pro** adds **Advanced Query Loop**, **Dynamic Content** (bind to post meta/ACF/MetaBox/WooCommerce), Advanced Slider, Modal, Post/Product Carousel, Animate on Scroll, Custom Fonts, and **Kadence AI** section generation.
- **Lead capture**: the **Advanced Form** block sends to native ESP/CRM integrations, or — on **Pro** — pushes an **outbound webhook** (Actions After Submit / Submit Actions → **WebHook** → Webhook URL + Map Fields) to any URL, commonly Zapier/Make. No HMAC/retry on the webhook; make the consumer idempotent. Pair with `/sales-email-marketing` for the sequence.
- **Checkout**: no native cart — it builds the pages; add commerce via WooCommerce (Kadence **Shop Kit** enhances it) or pair with a WooCommerce funnel plugin (CartFlows/FunnelKit) for checkout + upsells. For strategy use `/sales-checkout`.
- **Automation**: no hosted REST API or outbound platform webhook (it's a WP plugin). Surface = the **WordPress core REST API** (block markup is `kadence/`-namespaced in `post_content`, Application-Password auth) + public hooks/filters — `kadence_blocks_posts_query_args` (Posts block query), `kadence_blocks_pro_query_loop_query_vars` (Advanced Query Loop, Pro), `kadence_element_display` (Hooked Elements), `kadence_blocks_table_data_scope_attributes`.
- **Plan limits**: Free (WordPress.org, 20+ blocks); **Kadence Blocks Pro** (standalone, ~$89/yr historical) or the unified Kadence bundles **Essentials ~$99 / Pro ~$299 / Elite ~$499** per year. *(Pricing best-effort — verify.)* Advanced Query Loop, Dynamic Content, form webhooks, Design Library, and Kadence AI are **Pro**.
- **Gotchas**: **dynamic block CSS can regenerate per request** and slow TTFB (set CSS output to External File + enable Performance tools + cache); editor can **load blank** (JS conflict/stale build — update + clear cache); **child-theme/custom CSS won't show in the editor** (enqueue via `add_editor_style()`); **caching/optimization plugins can break styles** (exclude Kadence handles); some blocks still need jQuery; no native A/B testing/heatmaps (add VWO/Clarity).
- **Best for**: WordPress owners who want to build funnel pages **on native Gutenberg** with rich design controls and their own hosting/SEO control, bolting on a cart (WooCommerce/CartFlows) and ESP. If you need a built-in cart, programmatic page creation via a hosted REST API, or split testing, choose an all-in-one (ClickFunnels/Kartra), a WooCommerce funnel plugin (CartFlows/FunnelKit), or a hosted builder with an API (Landingi/Instapage) instead.

## In GenerateBlocks

GenerateBlocks is a **minimalist, high-performance Gutenberg block plugin** for WordPress (by **EDGE22 Studios** — the GeneratePress makers; 200k+ installs). Like Spectra/Kadence it **extends** the native block editor, but its philosophy is the opposite of feature-breadth: a **few composable primitives** (Container, Grid) you build everything from, for the **leanest DOM/CSS** of the block plugins. It is **not** an all-in-one — no native cart, no email, no A/B testing, no form block. For full platform help, use `/sales-generateblocks`.

- **Pages & blocks**: ~9 blocks (free) — **Container** (flexbox) and **Grid** layout primitives, Headline, Button, Image, and **Query Loop**. There are no one-off widget blocks (pricing table/testimonial) — you compose them. **Pro** adds **Dynamic Data** (bind to post title/excerpt/meta/ACF/terms/author/featured image), **Global Styles**, 150+ templates/asset library, device visibility, shape dividers, gradients, scroll effects, and custom attributes.
- **Lead capture**: **no form block and no webhook** — pair a third-party form plugin and use its ESP/webhook delivery. Pair with `/sales-email-marketing` for the sequence.
- **Checkout**: no native cart — it builds the pages; add commerce via WooCommerce or a WooCommerce funnel plugin (CartFlows/FunnelKit). For strategy use `/sales-checkout`.
- **Automation**: no hosted REST API or outbound webhook (it's a WP plugin). Surface = the **WordPress core REST API** (block markup is `generateblocks/`-namespaced in `post_content`, Application-Password auth) + public filters — `generateblocks_dynamic_tag_output` (2.0+), `generateblocks_dynamic_content_output` (1.x), `generateblocks_image_url`, `generateblocks_dynamic_image_fallback`, `generateblocks_do_content` — plus the **`GenerateBlocks_Register_Dynamic_Tag`** class (2.0+) to register your own dynamic data source.
- **Plan limits**: Free (WordPress.org, core blocks + Query Loop); **Pro Personal ~$59/yr (1 site)**, **Pro Professional ~$99/yr (up to 500 sites)**, **GeneratePress One ~$149/yr** bundle (GP Premium + GB Pro + GenerateCloud). *(Pricing best-effort — verify.)* Dynamic Data, Global Styles, the template/asset library, device visibility, and the advanced design controls are **Pro**; Pro features can degrade if the license lapses.
- **Gotchas**: the **few-blocks model is the learning curve** (Container + Grid compose everything — no ready-made widgets, unlike Kadence/Stackable); **GenerateBlocks 2.0 was a rewrite** (dynamic tags, unified Query Loop, new Styles engine — pre-2.0 tutorials mislead); block CSS is generated per page so **regenerate assets + clear cache** after a migration/major update or inner pages render unstyled; no native A/B testing/heatmaps (add VWO/Clarity).
- **Best for**: performance-conscious WordPress owners/developers who want the **leanest possible** funnel pages and full design control from primitives, on their own hosting/SEO, pairing a form plugin + cart + ESP. If you want dozens of ready-made widget blocks choose Kadence/Stackable; if you need a built-in cart, hosted REST API, or split testing, choose an all-in-one (ClickFunnels/Kartra), a WooCommerce funnel plugin (CartFlows/FunnelKit), or a hosted builder with an API (Landingi/Instapage) instead.

## In Stackable

Stackable is a **design-focused, Gutenberg-native block plugin** for WordPress (by **Gambit Technologies / gambitph**; GPLv3, 200k+ installs, 4.9★, among the lightest block plugins). Like Spectra/Kadence/GenerateBlocks it **extends** the native block editor, so funnel *pages* are built as standard WordPress blocks — its angle is rich design controls + a Global Design System with a lean footprint. It is **not** an all-in-one and, notably, has **no form block, popup builder, header/footer builder, or WooCommerce blocks.** For full platform help, use `/sales-stackable`.

- **Pages & blocks**: **42 blocks (free)** across Essential (Columns, Heading, Text, Image, Button, Icon), Special (Carousel, Tabs, Accordion, Timeline, Map, Pricing, Testimonial, Count Up, Progress), and Section (Hero, Call to Action, Feature/Feature Grid, Card, Team, Blog Posts) — plus the **Design Library** (375+ patterns; ~107 free), **Global Design System** (Global Colors/Typography, block defaults), theme.json/block-theme support, and responsive editing. **Pro** adds **Dynamic Content** (bind to ACF/Metabox/JetEngine), **Motion Effects**, **Conditional Display**, **Role Manager**, and per-block **Custom CSS**.
- **Lead capture**: **no form block** — pair a third-party form plugin and use its ESP/webhook delivery. Pair with `/sales-email-marketing` for the sequence.
- **Checkout**: no native cart and **no WooCommerce blocks** — add commerce via WooCommerce or a WooCommerce funnel plugin (CartFlows/FunnelKit). For strategy use `/sales-checkout`.
- **Automation**: no hosted REST API or outbound webhook (it's a WP plugin). Surface = the **WordPress core REST API** (block markup is `stackable/`-namespaced in `post_content`, Application-Password auth) + the documented **`stackable_force_css_load`** filter (force-load Stackable's frontend CSS) and the WordPress `render_block` filter. GPLv3 source on GitHub for deeper extension; no Zapier/Make app.
- **Plan limits**: Free (WordPress.org, all 42 blocks + Global Design System); **Premium ~$49/yr** and **All Access Pass ~$89/yr**, both starting at **1 site** with 10/Unlimited and Lifetime toggles; 30-day money-back. *(Pricing best-effort — verify.)* Dynamic Content, Motion Effects, Conditional Display, Role Manager, per-block Custom CSS, and the expanded Design Library are **Pro**; Pro features can degrade if the license lapses.
- **Gotchas**: the **v2→v3 migration** is the #1 footgun (v3 was a rewrite; v2 blocks persist as separate blocks gated in Settings → Migration — test on staging); **blocks not showing in editor** (JS conflict/stale build/v2 loading off); **styles missing on dynamically-injected markup** (use `stackable_force_css_load`); major-update regressions can need a rollback; no native A/B testing/heatmaps (add VWO/Clarity).
- **Best for**: WordPress owners/designers who want **rich design control on native Gutenberg** with a lean footprint and their own hosting/SEO, bolting on a form plugin + cart + ESP. If you need built-in forms/popups choose Spectra/Kadence/aBlocks; if you want a built-in cart, hosted REST API, or split testing, choose an all-in-one (ClickFunnels/Kartra), a WooCommerce funnel plugin (CartFlows/FunnelKit), or a hosted builder with an API (Landingi/Instapage) instead.

## In Nexter Blocks

Nexter Blocks is an **all-in-one, Gutenberg-native WordPress ecosystem** (by **POSIMYTH Innovations**; WordPress.org slug `the-plus-addons-for-block-editor`, GPLv3, ~10k+ installs). Like Spectra/Kadence/GenerateBlocks/Stackable it **extends** the native block editor, so funnel *pages* are built as standard WordPress blocks — but its angle is **feature breadth**: it bundles a form builder, popup builder, mega menu, and header/theme builder that lean plugins lack, plus a native **MCP server** for AI page building. It is **not** an all-in-one *business* suite — no native cart/checkout engine, no email sequences, no A/B testing. For full platform help, use `/sales-nexter`.

- **Pages & blocks**: **90+ blocks** (~45 free) across layout/containers, typography, pricing tables, countdowns, tabs/accordions, post grids/carousels, testimonials, social feeds, maps, animated SVGs — plus 1000+ templates, in-editor **AI (ChatGPT + Gemini)**, a **Popup Builder** (6 types, 10+ triggers), **Mega Menu**, and **Header/Theme Builder**. **Pro** adds **Dynamic Content** (ACF/Toolset/Pods), WooCommerce blocks, Lottie/Spline/scroll animations, GA4/Pixel blocks, and **White Label**.
- **Lead capture**: the built-in **Form Builder** (9 field types; login/registration/password-reset) sends to its configured integration (e.g. **Mailchimp**, Pro); **no native webhook** — for arbitrary destinations pair a form plugin or route via the ESP. Pair with `/sales-email-marketing` for the sequence.
- **Checkout**: no native cart — WooCommerce blocks (Pro) display products; add commerce via WooCommerce + a funnel plugin (CartFlows/FunnelKit) for checkout + upsells. For strategy use `/sales-checkout`.
- **Automation**: no hosted REST API or outbound webhook (it's a WP plugin). Surface = **Nexter Abilities**, a native **MCP server** exposing **115 tools** (68 free/47 Pro + workflow/CRUD/inspection) to Claude/Cursor/VS Code — token-auth scoped to post types + abilities — plus the **WordPress core REST API** (block markup is **`tpgb/`-namespaced**, best-effort, in `post_content`, Application-Password auth) and performance flags (`tpgb_defer_css_js`, `tpgb_delay_css_js`).
- **Plan limits**: Free (WordPress.org, ~45 blocks + Form Builder + AI + 68 MCP abilities); **Starter ~$39/yr (1 site)**, **Professional ~$89/yr (5 sites, +Theme Builder +White Label)**, **Studio ~$129/yr (unlimited)**; Lifetime $139/$249/$349; Agency Bundle ~$399/yr. *(Pricing best-effort — verify.)* Theme Builder/White Label are Professional+; Dynamic Content/WooCommerce blocks/advanced animations are Pro.
- **Gotchas**: "blocks not showing" = not in the Gutenberg Block Editor / plugin-JS conflict / stale cache; **v4.7.0 converted all blocks to ApiVersion 3** (major-update boundary — back up + staging); performance claims (1 CSS+1 JS/page) are real but third-party tests still show ~0.2–0.35s overhead (use the defer/delay flags + cache); Pro blocks fall back if the license lapses; the `tpgb/` namespace is best-effort (copy real markup); no native A/B testing/heatmaps (add VWO/Clarity).
- **Best for**: WordPress owners who want **one Gutenberg ecosystem** (blocks + forms + popups + theme builder) on native blocks with their own hosting/SEO, and who want **AI page building via MCP**. If you want the leanest possible footprint choose GenerateBlocks/Stackable; if you need a built-in cart, hosted REST API, or split testing, choose an all-in-one (ClickFunnels/Kartra), a WooCommerce funnel plugin (CartFlows/FunnelKit), or a hosted builder with an API (Landingi/Instapage) instead.

## In Greenshift

Greenshift is a **performance-focused, animation-rich Gutenberg block plugin** for WordPress (by **Wpsoul**; slug `greenshift-animation-and-page-builder-blocks`, ~4.8★). Like Spectra/Kadence/GenerateBlocks/Stackable/Nexter it **extends** the native block editor, so funnel *pages* are built as standard WordPress blocks — its angle is **GSAP animations + an API Connector**: it can bind external REST APIs, Google Sheets/CSV, and even **LLM APIs (OpenAI chat/streaming)** into blocks with no glue code, plus AI Helpers, a Figma/HTML/webpage→blocks converter, and a VS Code extension. It is **not** an all-in-one — no native cart engine, no email sequences, no A/B testing. For full platform help, use `/sales-greenshift`.

- **Pages & blocks**: **50+ blocks** (free) — layout/Container, animated headlines, counters, countdown, tabs/togglers, table of contents, progress bars, sliders/carousels, shape dividers, 3D flip boxes, popups/panels — plus a **GSAP animation framework** (scroll/hover/parallax, pin/smooth scroll, mouse-follow), **Interaction Layers** (trigger→action on any block), and **3D/AR-VR/Lottie/Rive**. Full Site Editing support; markets ~2 KB base styles, conditional assets, no jQuery. **Paid packs** add advanced GSAP animations + dynamic fields (Design), the **Query addon** (dynamic FAQ/chart/filter/search, repeaters), WooCommerce blocks (Woo), and the API Connector/AI/Figma converter (GreenLight PRO).
- **Lead capture**: **no core form block** — pair a third-party form plugin and use its ESP/webhook delivery, or POST from the API Connector to your endpoint. Pair with `/sales-email-marketing` for the sequence.
- **Checkout**: no native cart — the **Woo Pack** adds WooCommerce *display/merchandising* blocks (product templates, loop builder, swatches, galleries, bundles), but add the actual cart via WooCommerce or a WooCommerce funnel plugin (CartFlows/FunnelKit). For strategy use `/sales-checkout`.
- **Automation**: no hosted REST API or outbound webhook (it's a WP plugin). Surface = the **API Connector** (server-side: runs on the WP server, response stored in the block, Application-Password Basic auth, placeholders `{{FORM}}`/`{{INCREMENT}}`/`{{USER_META}}`; client-side: browser `fetch`, placeholders `{{VALUE}}`/`{{COOKIE}}`/`{{STORAGE}}`, **AI chat + streaming**) — **client-side keys are public, so proxy secrets server-side** — plus the WordPress core REST API (block markup is **`greenshift-blocks/`-namespaced**, `GSPB` classes, in `post_content`, Application-Password auth) and the **`GSPB_API_RESPONSE`** client-side JS event. Dynamic data via the **Query addon** (post types/users/taxonomies/comments/options/ACF/ACPT/external repeaters).
- **Plan limits**: Free (WordPress.org, 50+ blocks + basic animations); paid **Design Pack ~$39.99–$79.99/yr**, **Woo Pack ~$49.99–$99.99/yr**, **GreenLight PRO ~$51.99–$109.99/yr** (API Connector, AI Helpers, Figma converter, VS Code ext), **All-in-One ~$59.99–$129.99/yr** (everything + SEO/schema + charts + AI agents); each at 1/5/Unlimited sites, with lifetime tiers (payable in crypto). *(Pricing best-effort — verify.)* Paid features can degrade if the license lapses.
- **Gotchas**: **"no styles on frontend"** = inline-CSS save truncated by host/DB field limits on huge pages (set CSS management to save inline within blocks + re-save); **animations blank in the editor** are often expected (render on the front end — judge from the live page); **backend "too many requests"/editor freeze** on heavy pages or many editor API calls (split pages, raise host limits, 4–5s+ loop intervals); **HTTP→HTTPS breaks fonts/icons** (re-upload static files, confirm HTTPS URL); **duplicate synced patterns share style IDs** (duplicate the ungrouped copy, delete the original); stay updated (historical CVE-2023-6636); no native A/B testing/heatmaps (add VWO/Clarity).
- **Best for**: WordPress owners/makers who want **rich GSAP animations and to bind external or AI APIs into pages** on native Gutenberg, on their own hosting/SEO, pairing a form plugin + cart + ESP. If you want the leanest footprint choose GenerateBlocks/Stackable; if you need a built-in cart, hosted REST API, or split testing, choose an all-in-one (ClickFunnels/Kartra), a WooCommerce funnel plugin (CartFlows/FunnelKit), or a hosted builder with an API (Landingi/Instapage) instead.

## In Gutenverse

Gutenverse is a **free, Gutenberg-native FSE block plugin + ecosystem** for WordPress (by **Jegstudio**; 20k–34k+ installs, 4.9★, WP 5.9+/PHP 7.0+). Like Spectra/Kadence/GenerateBlocks/Stackable it **extends** the native block editor, so funnel *pages* are built as standard WordPress blocks — its angle is **breadth at a generous free tier**: 57 blocks, a 600+ starter-template library, a built-in **popup builder**, and a **companion FSE theme (Unibiz)**. Unlike Stackable/GenerateBlocks it ships **popups built in** and a **separate free form plugin**. It is **not** an all-in-one — no native cart engine, no email sequences, no A/B testing. For full platform help, use `/sales-gutenverse`.

- **Pages & blocks**: **57 blocks (free)** across Layout (Container/Section/Flexible Wrapper, Popup Builder), Content (Heading, Button, Image/Gallery, Icon Box, Feature List), Interactive (Tabs, Accordion, Testimonials, Team, Countdown, Progress Bar, Chart, Animated Text, Logo Slider), Post/Query (Post List/Block, Post Title/Content/Meta, Breadcrumb, Taxonomy List), Social, and Google Maps — plus a **600+ starter-template library**, global colors/fonts, and responsive editing. **Pro** adds dynamic data, **display/visibility conditions**, custom fonts, premium templates/blocks, the **mega menu**, and sticky/cursor/Lottie effects. *(WooCommerce blocks, custom fields, and CPT Query Loop were marketed "coming soon" — verify.)*
- **Lead capture**: a **separate free Gutenverse Form plugin** — form-field blocks with **entries stored in WordPress (CSV export)**, **admin + user email notifications**, and a **reCAPTCHA** block. The free tier has **no webhook/Zapier/Mailchimp/CRM, no conditional logic, no multi-step, no payment fields** (Pro). For routing into a CRM/sequence, pair a dedicated form plugin and use `/sales-email-marketing`.
- **Checkout**: no native cart (WooCommerce blocks are "coming soon") — add commerce via WooCommerce or a WooCommerce funnel plugin (CartFlows/FunnelKit). For strategy use `/sales-checkout`.
- **Automation**: no hosted REST API or outbound webhook (it's a WP plugin). Surface = the **WordPress core REST API** (block markup is **`gutenverse/`-namespaced** in `post_content`, Application-Password auth, `context=edit` for `content.raw`) + the **`gutenverse-core`** framework hooks (`gutenverse_after_init_framework`, `gutenverse_include_block`, `gutenverse_block_config`) and the `gutenverseCore.*` ES6/window packages. Open source under `github.com/Jegstudio`; no Zapier/Make app.
- **Plan limits**: Free (WordPress.org — all 57 blocks + template library + popup builder + global colors/fonts). **Pro** annual, ~$55–69/yr single-site, ~$79–99/yr Professional (~10 sites), ~$199/yr Agency (~100 sites); LemonSqueezy checkout, money-back guarantee. *(Pricing best-effort/conflicting across sources — verify.)* Dynamic data, display conditions, custom fonts, premium templates, mega menu, and advanced form features are **Pro** and degrade if the license lapses.
- **Gotchas**: the **editor page failing to load after a customization change** (frontend still renders; deactivating fixes it — a JS conflict/corrupted block, bisect on staging) is the #1 reported issue; **color/style changes applying in the editor but not the frontend** (styling-cache/asset issue — regenerate cache, exclude assets from minify, stay on v3.4.0+); **form spam** (reCAPTCHA-only — a third-party Cloudflare Turnstile add-on exists); no native A/B testing/heatmaps (add VWO/Clarity).
- **Best for**: WordPress owners/makers who want **lots of ready-made blocks + templates + a built-in popup builder on native Gutenberg at a generous free tier**, on their own hosting/SEO, bolting on a form plugin (or Gutenverse Form) + cart + ESP. If you want the leanest footprint choose GenerateBlocks/Stackable; if you need a built-in cart, hosted REST API, or split testing, choose an all-in-one (ClickFunnels/Kartra), a WooCommerce funnel plugin (CartFlows/FunnelKit), or a hosted builder with an API (Landingi/Instapage) instead.

## In GutenKit

GutenKit is a **feature-rich Gutenberg block plugin + page builder** for WordPress (by **Wpmet**, the ElementsKit makers; slug `gutenkit-blocks-addon`, 70k+ installs, WP 6.1+/PHP 7.4+, Block API v3, zero jQuery). Like Spectra/Kadence/Gutenverse it **extends** the native block editor, so funnel *pages* are built as standard WordPress blocks — its angle is **breadth of blocks + a deep template library** with FSE compatibility. It is **not** an all-in-one — no native cart, no email sequences, no A/B testing, and only a thin Mailchimp opt-in (no full form builder). For full platform help, use `/sales-gutenkit`.

- **Pages & blocks**: **65+ blocks** built on a flexbox **Container** — Nav Menu, **Mega Menu** (Pro), **Query Loop Builder** (Pro), Advanced Accordion/Tab, Post Grid/Blog Posts/Post Tab, Pricing Table, Countdown, Image/Icon Box, Image Comparison, Timeline, Testimonial, Team, Gallery, Offcanvas, Social Icons/Share, Progress Bar, Back to Top — plus a **900+ template library**, global colors/fonts, local Google Fonts, inline SVG icons, and responsive breakpoints. **Pro** adds the Mega Menu, Query Loop Builder, **Dynamic Content** (bind to post meta/ACF/user/site fields), **Display Conditions**, One Page Scroll, Sticky Content, Glass Morphism, Advanced Tooltip, Google Map, and advanced Parallax.
- **Lead capture**: a built-in **Mailchimp** opt-in block only — **no full form builder, no stored entries, no webhooks/Zapier, no conditional/multi-step/payment fields.** For anything beyond a Mailchimp opt-in, pair a dedicated form plugin and route via `/sales-email-marketing`.
- **Checkout**: no native cart — add commerce via WooCommerce or a WooCommerce funnel plugin (CartFlows/FunnelKit). For strategy use `/sales-checkout`.
- **Automation**: no hosted REST API or outbound webhook (it's a WP plugin). Surface = the **WordPress core REST API** (block markup is **`gutenkit/`-namespaced** in `post_content`, Application-Password auth, `context=edit` for `content.raw`) + WordPress core hooks/filters (`render_block` for output tweaks). No published GutenKit action/filter SDK, no Zapier/Make app; no `wpmet` GitHub org found — distribution via WordPress.org.
- **Plan limits**: Free (WordPress.org — core blocks + template library + flexbox Container + responsive editing + Mailchimp block). **Pro** (best-effort/annual): Personal/1-site ~$39/yr, Professional/5-site ~$79/yr, Agency/unlimited ~$149/yr, with lifetime options (~$89/$189/$389). The marquee features (Mega Menu, Query Loop Builder, Dynamic Content, Display Conditions, sticky/one-page-scroll/parallax) are **Pro** and degrade if the license lapses. *(Pricing + free-vs-Pro counts conflict across sources — verify.)*
- **Gotchas**: a block showing **"this block has encountered an error and cannot be previewed" / the editor failing to load after a customization change** (frontend still renders; deactivating fixes it — JS conflict/corrupted block, bisect on staging) is the #1 reported issue; the **GutenKit Template Library erroring inside ElementsKit Lite** (both Wpmet plugins share a template-library handler — keep both on matched current versions); **styles applying in the editor but not the frontend** (per-page asset/cache mismatch — clear cache, exclude GutenKit assets from minify); no native A/B testing/heatmaps (add VWO/Clarity).
- **Best for**: WordPress owners/makers who want **a lot of ready-made blocks + a big template library on native Gutenberg at a generous free tier**, on their own hosting/SEO, bolting on a form plugin + cart + ESP. If you want the leanest footprint choose GenerateBlocks/Stackable; if you need a built-in form builder choose Kadence/Nexter/Gutenverse Form; if you need a built-in cart, hosted REST API, or split testing, choose an all-in-one (ClickFunnels/Kartra), a WooCommerce funnel plugin (CartFlows/FunnelKit), or a hosted builder with an API (Landingi/Instapage) instead.

## In Superb Addons

Superb Addons is a **Gutenberg-native block-addon plugin** for WordPress (by **SuperbThemes / Suplugins**; WordPress.org slug `superb-blocks`, 80k+ installs, 4.9★). Like Spectra/Kadence/GutenKit it **extends** the native block editor, so funnel *pages* are built as standard WordPress blocks — its angle is **breadth bundled into one plugin**: 20 blocks, 200+ patterns, 50+ pre-built pages, a **form builder**, a **Popup block** with smart triggers, 70+ animations, and a **Theme Designer**. It is **not** an all-in-one — no native cart engine, no email sequences, no A/B testing. For full platform help, use `/sales-superb-addons`.

- **Pages & blocks**: 20 blocks (Carousel Slider, Countdown, Progress Bar, Google Maps, Rating, Add to Cart, Animated Heading, Table of Contents, Recent Posts, Cover Image, Toggle, Reveal Buttons) + **200+ patterns**, **50+ pre-built pages**, **20+ header/footer templates**, a **Theme Designer**, **70+ animations**, responsive visibility controls, and ACF-backed dynamic content.
- **Lead capture**: a real **form builder** — contact/newsletter/feedback/RSVP/booking/quote/**multi-step** forms, calculated fields, conditional logic, anti-spam (**honeypot, hCaptcha, reCAPTCHA v2/v3, Cloudflare Turnstile**), submission storage + admin/user email notifications + GDPR auto-deletion, and **outbound integrations: webhook + Mailchimp + Brevo + Google Sheets + Slack**. This is its edge over form-less block plugins (Stackable/GenerateBlocks) — closest to Spectra (form + popup) and Nexter.
- **Checkout**: no native cart (just an Add to Cart block) — add commerce via WooCommerce or a WooCommerce funnel plugin (CartFlows/FunnelKit). For strategy use `/sales-checkout`.
- **Automation**: **no hosted REST API and no MCP** (it's a WP plugin). Surface = the **form's outbound webhook + native Mailchimp/Brevo/Sheets/Slack** (the way leads leave the site; payload schema **not published** — capture a live delivery, no documented HMAC) + the **WordPress core REST API** (namespaced block markup in `post_content`, Application-Password auth, `context=edit` for `content.raw`) + WordPress core hooks/filters. No first-party Zapier app.
- **Plan limits**: Free (WordPress.org). **Premium** best-effort: yearly ~$29/$39/$49 (1/3/50 sites), lifetime ~$59/$79/$99. ⚠️ **Plan-gating is genuinely ambiguous** — the WordPress.org readme markets a free form builder, but the pricing page lists Forms, multi-step forms, Popups (smart triggers), 70+ animations, sliders, Theme Designer, visibility conditions, and advanced custom CSS as **Premium**. Verify each capability on the live install.
- **Gotchas**: the **Theme Designer not loading/responding when clicked** is the #1 reported issue (update plugin → run the built-in Troubleshooter → clear caches → deactivate other block plugins to isolate; a documented conflict with **Gutenverse** broke Theme Designer previews); **saved form submissions sometimes not showing in wp-admin** under some permalink configs (update + re-save permalinks); standard block-plugin **unstyled-on-inner-pages** asset/cache issue; no native A/B testing/heatmaps (add VWO/Clarity).
- **Best for**: WordPress owners/makers who want **one plugin that bundles blocks + patterns + a real form builder + popups + a Theme Designer** on native Gutenberg, on their own hosting/SEO, bolting on a cart + ESP. If you want the leanest footprint choose GenerateBlocks/Stackable; if you need a built-in cart, hosted REST API, or split testing, choose an all-in-one (ClickFunnels/Kartra), a WooCommerce funnel plugin (CartFlows/FunnelKit), or a hosted builder with an API (Landingi/Instapage) instead.

## In Jotform

Jotform is primarily a form builder, not a full funnel builder — but it's commonly used for the lead capture and payment collection steps of a funnel. For full platform help, use `/sales-jotform`.

- **Landing page forms**: Embed Jotform forms on any landing page via iframe, lightbox, or popup. Use conditional logic to show/hide fields based on user selections — creates a guided, conversational experience.
- **Multi-page forms**: Create multi-step forms with a progress bar — useful for application funnels, qualification funnels, and event registration flows. Each page can have its own conditional logic.
- **Payment collection**: Add Stripe, PayPal, or Square directly to forms for registration fees, product orders, or donations. One gateway per form.
- **Lead capture → email**: Connect form submissions to Mailchimp, ActiveCampaign, HubSpot, or other ESPs via native integrations or Zapier. Form submissions auto-add contacts to email lists and trigger nurture sequences.
- **Approval funnels**: For application-style funnels (job applications, vendor onboarding, scholarship requests), use Jotform Workflows to add approval chains with conditional routing.
- **PDF generation**: Auto-generate confirmation documents, receipts, or agreements from form submissions using Jotform PDF Editor.
- **Kiosk mode**: Jotform Apps supports kiosk mode for in-person funnels — event check-in, on-site registration, trade show lead capture.
- **Limitations**: No multi-step funnel page builder (no sales page → checkout → upsell → thank-you flow), no A/B testing on forms, no upsell/downsell pages, no countdown timers or urgency elements. For full funnel flows, use ClickFunnels, Groove.cm, or GoHighLevel and embed Jotform for the form/payment step.
- **Best for**: Lead capture forms embedded in existing funnels, event registration with payment, application/qualification funnels with approval workflows, and donation collection. Pair with a dedicated funnel builder for the page flow and use Jotform for the data collection step.

## In Typeform

Typeform is a conversational form and survey builder — not a full funnel builder, but its one-question-at-a-time UX makes it effective for the lead capture and qualification steps of funnels. For full platform help, use `/sales-typeform`.

- **Lead magnet funnels**: Embed a Typeform on your landing page using the Embed SDK (`@typeform/embed`). The conversational format drives higher completion rates than traditional multi-field forms. Pass UTM parameters via hidden fields to track which campaign each lead came from.
- **Quiz funnels**: Typeform's quiz builder with score-based outcomes is ideal for "What type of X are you?" lead magnets. Gate the results behind email capture, then segment subscribers by quiz outcome. Connect to Mailchimp, Klaviyo, or ActiveCampaign to trigger different nurture sequences per segment.
- **Application funnels**: Use logic jumps to create branching qualification flows — route high-value prospects to a booking page and disqualify poor fits early. Embed as a popup or slider to keep users on your landing page.
- **Payment collection**: Stripe integration collects payments directly in the form — useful for registration fees, event tickets, or simple product purchases. Supports fixed and calculated amounts.
- **Lead capture → CRM**: Native integrations with HubSpot, Salesforce, Pipedrive, or webhook to any CRM. Hidden fields carry tracking data (UTM, referrer) into CRM records automatically.
- **Response piping**: Insert previous answers into later questions for a personalized, conversational feel — "Thanks, {name}! Based on your interest in {topic}, here's one more question..."
- **Limitations**: No multi-step funnel page builder (no sales page → checkout → upsell → thank-you flow), no A/B testing on forms natively (use VWO or Unbounce for page-level testing), response limits shared across all forms (100/mo on Basic plan — burns fast with multiple funnels), no countdown timers or urgency elements. For full funnel flows, use ClickFunnels, Groove.cm, or GoHighLevel and embed Typeform for the form step.
- **Best for**: High-converting lead capture forms, quiz funnels for segmentation, application/qualification flows with branching logic, and any form where completion rate matters more than volume.

## In WPFunnels

- **WordPress funnel builder for WooCommerce** (CartFlows/FunnelKit competitor): visual funnel canvas, landing/checkout/thank-you steps, **order bumps**, **one-click upsells/downsells**, A/B split testing, abandoned-cart recovery, conditional steps, lead capture, analytics — plus bundled **Mail Mint** email automation. Designed in Elementor/Gutenberg/Divi/Bricks/Oxygen.
- **Automation surface**: **no hosted REST API** (it's a WP plugin). Per-funnel **outbound webhooks** (funnel canvas → three-dot → Webhook → Add Webhook; fields Name/Request URL/Method/Format/Event; body **All Fields** or **Select Fields**; **no documented event names, payload schema, or HMAC**), **Mail Mint** event triggers, and **WooCommerce** order hooks/REST for the underlying orders (order bumps + upsells are WooCommerce orders — the reliable way to read funnel revenue). Plus WordPress action/filter hooks.
- **Watch-outs**: WordPress + WooCommerce required; webhook payload is undocumented (use Select Fields + capture a live delivery); webhooks, one-click upsells, A/B testing and order bumps are **Pro** (free plugin is basic); pricing best-effort (peers: FunnelKit ~$99.50–$399/yr, CartFlows ~$79–$449/yr).
- **Best for**: WooCommerce store owners who want a **WordPress-native** funnel builder with post-purchase upsells and bundled email, lower learning curve than FunnelKit. **Platform skill**: `/sales-wpfunnels`.

## In FunnelKit

- **WordPress/WooCommerce funnel builder + built-in CRM/automation suite** (formerly WooFunnels; automation plugin formerly Autonami) — the leading CartFlows/WPFunnels rival and a WP ClickFunnels alternative. Two plugins: **Funnel Builder** (checkout, rule-based order bumps, one-click upsells/downsells, A/B testing, sliding cart, opt-in/sales/thank-you pages) + **Automations** (CRM, email/SMS, segments, broadcasts, cart-abandonment recovery, workflows).
- **Automation surface**: the differentiator is the **REST API + webhooks on the Automations side** — base `/wp-json/funnelkit-automations/`, **`?api_key=` query-param** auth (Settings → REST API), with **Tags/Lists/Fields/Contacts CRUD** (contact = email-keyed, tag/list-driven, status subscribed|bounced|unsubscribed|verified), plus **incoming webhooks** (a Webhook URL → triggers an automation, with Conditions) and **outgoing** (HTTP Request action). **Funnel revenue is WooCommerce orders** (order bumps + upsells) — read via the WooCommerce REST API; **no funnel-read API**.
- **Watch-outs**: WordPress + WooCommerce required; the REST API is the **Automations** (contacts) side only; `api_key` is a query param (leak risk); webhook payload schemas aren't fully published; sold as two plugins (each Free + Pro) combined in **bundles** (Plus/Professional/Elite, ~$99.50–$399/yr — best-effort).
- **Vs WPFunnels/CartFlows**: FunnelKit's edge is the **built-in CRM/email-SMS automation engine** (vs checkout-only CartFlows, or WPFunnels' bundled Mail Mint).
- **Best for**: WooCommerce sellers who want a funnel builder **and** a native CRM/automation + cart-recovery stack in one, with a real contacts API. **Platform skill**: `/sales-funnelkit`.

## In Wix

- **No-code website builder with native commerce, not a pure funnel tool**: Wix builds full sites, landing pages, and an online store (Wix Stores) on one drag-and-drop platform. Use it for a funnel when you want the landing pages, store, and site under one roof; reach for a dedicated funnel builder (ClickFunnels/Systeme.io) when you want step-by-step funnels with native upsell/downsell flows.
- **Commerce is plan-gated**: selling needs the **Core plan (~$29/mo)+** — the cheapest **Light (~$17/mo)** plan can't run a store; advanced shipping/tax are **Business+**.
- **Automation**: REST APIs (**Stores Products v3**, **eCommerce Orders**) at `www.wixapis.com`, **API-key or OAuth** auth, and **signed-JWT webhooks** (verify with the app public key, respond 200 within 1250 ms). **Wix Headless** lets you build a custom front end on the same APIs.
- **Watch for**: a **JS-heavy** front end (Core Web Vitals / SEO risk), **template lock-in** after publishing, and no clean store export. **Platform skill**: `/sales-wix`. For checkout-conversion strategy across tools use `/sales-checkout`.

## In Framer

- **Design-first AI site builder** — Figma-like canvas, AI design agents (Wireframer), CMS Collections, built-in A/B testing; the fastest design-to-published-landing-page path and a favorite for startup marketing sites/portfolios. Commerce is embed-only (Snipcart/Foxy/payment links).
- **The two structural trades**: **no code export** (leaving = rebuilding — keep CMS mirrored externally and design sources in Figma) and **SEO ceilings** (no JSON-LD authoring, no hreflang; robots.txt Pro-gated) — if rich results or multilingual SEO drive revenue, weigh Webflow/WordPress instead.
- **Plan gates**: CMS ~100 items on Basic / ~1,000 per collection on Pro; per-seat editors (~$20/mo) and per-language localization (~$20–40/mo each) stack on plan fees (Basic ~$10 / Pro ~$30 / Scale ~$100+, best-effort — 2026 repriced repeatedly).
- **Automation**: **Server API** (open beta — `framer-api` npm, API key in site settings, WebSocket; sync CMS from Notion/Airtable, publish programmatically, drive from Claude Code/Cursor) + Plugin API + Fetch. For setup/integration, use `/sales-framer`.

## In Other Tools

- **Systeme.io**: see the dedicated [In Systeme.io](#in-systemeio) section above, or use `/sales-systemeio`.
