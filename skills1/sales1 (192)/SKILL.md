---
name: sales-funnel
description: "Builds and optimize sales funnels — strategy, structure, conversion optimization, A/B testing, and analytics. Use when your funnel isn't converting, you need to build a funnel from scratch but don't know the right structure, upsell/downsell flow is leaving money on the table, you're not sure which funnel builder to use, or a launch needs a funnel strategy. Do NOT use for email marketing sequences (use /sales-email-marketing), checkout-specific optimization (use /sales-checkout), or webinar funnels (use /sales-webinar). For Groove-specific help, use /sales-groove. For SWAI-specific help, use /sales-swai."
argument-hint: "[describe your funnel goal — e.g., 'build a webinar registration funnel' or 'optimize my checkout conversion rate']"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, conversion]
---
# Sales Funnel Builder & Optimizer

Build, structure, and optimize sales funnels across any platform. This skill covers funnel strategy, page architecture, conversion optimization, A/B testing, and analytics — tool-agnostic with platform-specific guidance where it matters.

---
## Step 1: Lead with Structure, Then Refine


If `references/learnings.md` exists, read it first for accumulated knowledge.

**If the user's request already provides enough context to identify the funnel type, skip directly to the relevant funnel structure and start filling it in. Lead with your best-effort answer using reasonable assumptions (stated explicitly), then ask only the most critical 1-2 clarifying questions at the end.**

### Common Funnel Structures (Always Provide the Relevant Template)

When a user asks about building a funnel, immediately provide the concrete step-by-step structure for the relevant funnel type. Do not wait for answers before outlining the structure.

**Lead Magnet Funnel**:
1. **Traffic source** (ad, blog post, social media, SEO) →
2. **Opt-in / squeeze page** — Headline promising a specific outcome, 3-5 benefit bullets, email capture form, action-oriented CTA button →
3. **Thank-you / delivery page** — Deliver the asset (or confirm email delivery), set expectations for what happens next, optional tripwire offer ($7-$17) to offset ad costs →
4. **Follow-up email sequence** (3-5 emails): deliver value → build trust → introduce offer → overcome objections → CTA

**Lead magnet types** (choose based on audience and niche):
- **PDF guide / ebook**: Most common. Works when the topic needs depth. Example: "The Complete Guide to [X]."
- **Checklist / cheat sheet**: High conversion — low effort to consume. Example: "The 10-Point Launch Checklist."
- **Template / swipe file**: Extremely compelling because it's immediately usable. Example: "5 Cold Email Templates That Book Meetings."
- **Video training / mini-course**: Higher perceived value, builds more trust. Works for complex topics.
- **Quiz / assessment**: Interactive, generates personalized results. Great for segmentation. Example: "What's Your Marketing Score?"
- **Calculator / tool**: Solves a specific problem. Example: "ROI Calculator for [Your Product]."
- **Free trial / demo**: Best for SaaS — let the product sell itself.

The best lead magnets solve a specific, narrow problem quickly. "The Ultimate Guide to Marketing" converts poorly. "The 5-Minute Facebook Ad Audit Checklist" converts well. Specificity and speed-to-value beat comprehensiveness.

**Webinar Funnel**:
1. **Registration page** — Headline with specific promise, date/time, speaker credibility, registration form
2. **Confirmation + reminder sequence** — Confirmation page with calendar add, 3-4 reminder emails leading up to the event
3. **Live / replay page** — Webinar embed, chat/Q&A, CTA overlay at pitch point
4. **Follow-up sequence with offer** — Replay access, testimonials, objection handling, cart-close urgency

**Product Launch Funnel (PLF)**:
1. **Pre-launch content** — Squeeze page → PLC Video 1 (Opportunity) → Video 2 (Transformation) → Video 3 (Ownership) → Video 4 (The Offer)
2. **Cart open page** — Full long-form sales page with offer stack, testimonials, bonuses, countdown timer
3. **Sales page** — Price reveal, guarantee, FAQ, multiple CTAs
4. **Checkout** — Simplified order form, order bump offer
5. **Post-purchase upsell** — Complementary one-click upsell (1-2 OTOs max)

**Tripwire Funnel**:
1. **Opt-in page** — Free lead magnet offer
2. **Sales page** — Low-ticket offer ($7-$47) presented immediately after opt-in
3. **Order form + order bump** — Simple checkout with a complementary add-on
4. **Upsell / OTO page** — One-click upgrade to a higher-tier offer
5. **Thank-you page** — Delivery confirmation + next steps

**High-Ticket Application Funnel**:
1. **Landing page** — Outcome-driven headline, case studies, "Apply Now" CTA
2. **Application form** — Qualifying questions to filter serious prospects
3. **Booking page** — Calendar integration for scheduling a sales call
4. **Sales call** — Discovery + pitch (supported by a follow-up sequence)

**Sales Page Funnel**:
1. **Long-form sales page** — Full PAS or AIDA sales letter with offer stack, testimonials, and guarantee →
2. **Order / checkout page** — Simplified checkout with order bump offer →
3. **Upsell page(s)** — 1-2 one-click upsell or downsell offers →
4. **Thank-you / onboarding page** — Delivery confirmation, next steps, community invite

**Free Trial / Demo Funnel (SaaS)**:
1. **Landing page** — Problem-focused headline, product demo video or screenshots, CTA to start free trial →
2. **Sign-up / trial activation** — Minimal-friction registration (email + password, or SSO), immediate access to product →
3. **Onboarding sequence** — In-app guided tour + email sequence (5-7 emails over trial period: quick wins, key features, case studies) →
4. **Upgrade prompt sequence** — Trial-expiring reminders, ROI recap, plan comparison, limited-time upgrade incentive

### Gathering Additional Context

After providing the relevant funnel structure, refine your recommendations with these details as needed:

1. **Offer** — What are you selling, at what price point?
2. **Audience** — Who is the target buyer? Where are they in the awareness spectrum?
3. **Traffic source** — Where will traffic come from? (paid ads, organic, email list, affiliates, social media)
4. **Existing assets** — Do you already have landing pages, email sequences, lead magnets, videos, testimonials?
5. **Platform / tool** — Which funnel builder are you using or considering?
6. **Goal & timeline** — What does success look like? When do you need this live?
7. **Current metrics** — If optimizing an existing funnel, what are your current conversion rates at each step?

If the user skips details, make reasonable assumptions for a general B2B or B2C info-product funnel and state them explicitly.

---
## Step 2: Funnel Strategy

### Funnel Types & When to Use Each

| Funnel Type | Best For | Typical Price Point | Key Pages |
|---|---|---|---|
| **Lead Magnet** | List building, top-of-funnel | Free (email opt-in) | Opt-in page, thank-you page |
| **Tripwire** | Converting leads to buyers fast | $7–$47 | Opt-in, sales page, OTO, thank-you |
| **Webinar** | Courses, coaching, mid-to-high ticket | $297–$2,000 | Registration, confirmation, webinar, sales page, order |
| **Product Launch (PLF)** | Big reveals, course launches | $197–$2,000+ | Squeeze page, PLC videos (3–4), cart page, order |
| **Sales Page** | Direct product sales, info products | $47–$997 | Sales page, checkout, upsell, thank-you |
| **High-Ticket Application** | Coaching, consulting, done-for-you | $3,000–$50,000+ | Landing page, application form, booking page, sales call |
| **Free Trial / Demo (SaaS)** | SaaS, software, tools | $29–$299/mo | Landing page, sign-up, onboarding, upgrade prompts |
| **VSL (Video Sales Letter)** | Direct-response offers | $47–$497 | VSL page, order form, OTO |
| **Challenge** | Community-driven launches | $27–$497 (or free entry) | Registration, daily content pages, offer page |

### Conversion Benchmarks by Funnel Type

Use these as baselines — not guarantees. Benchmarks assume warm-to-lukewarm traffic:

| Funnel Step | Good | Great | Elite |
|---|---|---|---|
| **Opt-in page** | 25–35% | 35–50% | 50%+ |
| **Tripwire sales page** | 5–10% | 10–15% | 15%+ |
| **Webinar registration** | 20–30% | 30–45% | 45%+ |
| **Webinar show-up rate** | 25–35% | 35–50% | 50%+ |
| **Webinar pitch conversion** | 3–7% of registrants | 7–12% | 12%+ |
| **Sales page (cold traffic)** | 1–3% | 3–5% | 5%+ |
| **Sales page (warm traffic)** | 3–8% | 8–15% | 15%+ |
| **Order bump acceptance** | 15–25% | 25–40% | 40%+ |
| **Upsell/OTO acceptance** | 10–20% | 20–35% | 35%+ |
| **Application completion** | 30–50% | 50–70% | 70%+ |

---
## Step 3: Platform-Specific Guidance

For platform-specific funnel building guidance (Groove.cm, ClickFunnels, GoHighLevel, Kartra, Systeme.io, WordPress, CartFlows, WPFunnels, FunnelKit, Closum, Mailchimp, GetResponse, Kit, SendPulse, VWO, Leadpages, Unbounce, Landingi, Instapage, Convertri, SeedProd, Beaver Builder, Breakdance, Spectra, Kadence Blocks, GenerateBlocks, Stackable, Nexter Blocks, Greenshift, Gutenverse, GutenKit, Superb Addons, Jotform, Typeform, Wix, etc.), see references/platforms.md.

---
## Step 4: Actionable Guidance

### Page Structure for Each Funnel Step

**Opt-in Page**
1. Headline: State the specific outcome the lead magnet delivers (not the format).
2. Subheadline: Reinforce with timeframe or ease — "in 15 minutes" or "without X."
3. Bullet points (3–5): Benefits, not features. Each bullet = one desirable outcome.
4. Opt-in form: Name + email minimum. Ask only for what you need.
5. CTA button: Action-oriented verb + outcome ("Get My Free Guide," not "Submit").
6. Social proof (optional): Subscriber count, testimonial, or trust logos.

**Sales Page (Long-Form)**
1. Pre-headline: Call out the audience ("Attention course creators...")
2. Headline: Big promise or pattern interrupt.
3. Story/problem section: Agitate the pain. Use the PAS (Problem-Agitate-Solution) or AIDA framework.
4. Solution introduction: Bridge from problem to your offer.
5. Offer stack: List everything included with perceived value for each item.
6. Testimonials/proof: Scatter throughout, not just in one section.
7. Price reveal + anchor: Show total value, then actual price.
8. Guarantee: Risk reversal — 30-day, 60-day, or conditional.
9. CTA: Repeat 2–3 times throughout the page.
10. FAQ: Handle top 5–7 objections.
11. Final CTA + urgency: Deadline, scarcity, or bonus expiration.

**Upsell / OTO Page**
1. Headline: "Wait! Your order is not complete..."
2. Short video or copy explaining the complementary offer.
3. One-click purchase button (no re-entering payment info).
4. "No thanks" decline link — always visible, never hidden.
5. Keep it short: 300–500 words max. The decision should take under 60 seconds.

**Thank-You / Confirmation Page**
1. Confirm what they just got and what happens next.
2. Set expectations for delivery (check email, access link, etc.).
3. Introduce the next step: book a call, join the community, share on social.
4. This page is underused — it's prime real estate for a soft upsell or referral ask.

### Copy Frameworks

- **PAS (Problem-Agitate-Solution)**: Name the problem, twist the knife, present the fix. Best for sales pages.
- **AIDA (Attention-Interest-Desire-Action)**: Hook, build curiosity, create want, prompt action. Best for shorter pages.
- **BAB (Before-After-Bridge)**: Show current state, paint the dream state, bridge with your offer. Best for opt-in pages and ads.
- **4 Ps (Promise-Picture-Proof-Push)**: Make a bold promise, paint the outcome, show proof it works, push to action. Best for VSLs.

### CTA Placement Rules

- First CTA: Above the fold or immediately after the headline/subheadline.
- Second CTA: After the main benefit section or proof section.
- Final CTA: At the bottom, paired with urgency or a guarantee reminder.
- Sticky CTA (mobile): Use a fixed bottom bar with the CTA button on mobile. Do not rely on in-page buttons alone.

### Mobile Optimization

- 60–80% of funnel traffic is mobile. Design mobile-first.
- Keep opt-in forms to 1–2 fields on mobile.
- Use large tap targets (min 44px height for buttons).
- Compress images to under 200KB per image. Use WebP format.
- Test page load speed: aim for under 3 seconds on 3G.
- Avoid pop-ups that block the full screen on mobile (Google penalizes these).

### A/B Testing Priorities

Test in this order (highest impact first):

1. **Headline** — The single biggest lever. Test completely different angles, not word swaps.
2. **CTA button** (text, color, placement) — Test action-oriented vs. benefit-oriented copy.
3. **Hero image or video** — Test video vs. static image, or different hero shots.
4. **Social proof placement** — Test above the fold vs. below.
5. **Price presentation** — Test payment plans vs. one-time, or different anchoring.
6. **Page length** — Test long-form vs. short-form (especially for cold vs. warm traffic).

### A/B Testing Methodology

Follow this framework for every test:

- **One variable at a time**: Change only one element per test. Testing headline AND CTA simultaneously gives you no idea which change caused the result.
- **Minimum sample size**: Aim for at least 100 conversions per variant (not 100 visitors — 100 conversions). For pages with 5% conversion rate, that means ~2,000 visitors per variant. Use a significance calculator (ABTestGuide, Evan Miller, or Optimizely) if unsure.
- **Statistical significance**: Wait for 95% confidence before declaring a winner. Do NOT call a test early because one variant "looks better" after a few days.
- **Run for full business cycles**: Run tests for at least 7 days to capture weekday vs. weekend variation, even if you hit sample size sooner.
- **Document and iterate**: Record every test result (variant, metric, sample size, winner, lift %). Build a testing backlog and always be running the next test.

### Analytics & Tracking

- Track these metrics at every funnel step: visitors, conversion rate, cost per conversion, revenue per visitor.
- Set up UTM parameters for every traffic source. Use consistent naming: `utm_source`, `utm_medium`, `utm_campaign`.
- Install a Facebook/Meta Pixel and Google Analytics 4 on all funnel pages. Fire standard events: `PageView`, `Lead`, `AddToCart`, `Purchase`.
- Calculate **Earnings Per Click (EPC)**: total revenue / total clicks to funnel. This is the master metric for paid traffic funnels.
- Calculate **Customer Acquisition Cost (CAC)**: total ad spend / number of customers. Compare to Customer Lifetime Value (LTV) — aim for 3:1 LTV:CAC minimum.

---
## Gotchas

1. **Do not recommend specific conversion rates as guaranteed outcomes.** Benchmarks vary wildly by niche, traffic temperature, and offer. Always frame them as baselines to test against, not promises.
2. **Do not design upsell flows with more than 2–3 OTOs.** Beyond that, buyer fatigue tanks conversions and increases refund rates. Keep it tight.
3. **Do not ignore page load speed.** A 1-second delay in load time can drop conversions by 7%. Always recommend image compression, lazy loading, and minimal scripts — especially for WordPress funnels.
4. **Do not assume the user's traffic is warm.** Cold traffic from paid ads converts very differently from an email list. Always ask about the traffic source and tailor page length, proof elements, and CTA aggression accordingly.
5. **Do not conflate funnel structure with email sequences.** The funnel is the page flow. Post-funnel email nurture and abandoned-cart recovery are separate concerns — point users to /sales-email-marketing for those.

---
- **Self-improving**: If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Before recommending a specific platform skill

This skill covers a strategy domain across many platforms. **Before pointing the user to any specific platform skill** (any `/sales-{platform}` listed in `## Related skills`, e.g., `/sales-mailshake`, `/sales-klaviyo`, `/sales-apollo`), read that platform skill's actual `SKILL.md` first. The 1-line description in `## Related skills` is enough to *identify* a candidate — it's not enough to *commit* to it or to write a prompt that invokes it well.

**How to read it:**
- If `~/.claude/skills/{skill-name}/SKILL.md` exists locally, `Read` it.
- For `sales-*` skills, `WebFetch` directly from this repo: `https://raw.githubusercontent.com/sales-skills/sales/main/skills/{skill-name}/SKILL.md` — e.g., for `sales-mailshake`: `https://raw.githubusercontent.com/sales-skills/sales/main/skills/sales-mailshake/SKILL.md`.
- For non-`sales-*` skills (third-party), look up `{org}/{repo}` in `~/.claude/skills/sales-do/references/skill-sources.md` if installed and fetch the same `skills/{skill-name}/SKILL.md` path under that repo.

**After reading,** ground your recommendation in something concrete from the SKILL.md (its scope, a sub-flow, its `argument-hint` shape, or a "Do NOT use for..." negative trigger). Align any generated invocation with the platform skill's `argument-hint`. If the platform skill turns out not to fit the user's situation, swap to another or handle the question here directly rather than recommending a poor fit.

## Related Skills

- `/sales-framer` — Framer platform help (design-first AI site builder; Server API for agent-driven CMS/publishing; no-code-export lock-in and SEO-gap trade-offs)
- `/sales-clickfunnels` — ClickFunnels platform help (the category-defining all-in-one funnel builder, ClickFunnels 2.0 — funnels, checkout/upsells, email/Workflows, courses, Backpack affiliates; V2 REST API + signed webhooks)
- `/sales-cartflows` — CartFlows platform help (lean checkout-first WordPress/WooCommerce funnel builder by Brainstorm Force — modern checkout layouts, dynamic order bumps, one-click upsells/downsells, A/B testing; no built-in CRM/email; no hosted REST API — WP-CLI, personalization + offer-JS shortcodes, WP hooks, OttoKit/Zapier, Cart Abandonment Recovery webhooks; funnel revenue read via WooCommerce orders; free + Pro/Suite/lifetime)
- `/sales-wpfunnels` — WPFunnels platform help (WordPress funnel builder for WooCommerce — funnel canvas, order bumps, one-click upsells, A/B testing, bundled Mail Mint email; no REST API, per-funnel webhooks + WooCommerce order hooks; CartFlows/FunnelKit competitor, free Lite + Pro)
- `/sales-funnelkit` — FunnelKit platform help (WooCommerce funnel builder + built-in CRM/automation suite, formerly WooFunnels/Autonami — checkout, order bumps, one-click upsells, A/B testing + email/SMS automations & cart recovery; Automations REST API `/wp-json/funnelkit-automations/` with api_key query param + in/outgoing webhooks; funnel revenue via WooCommerce; free + bundles)
- `/sales-gohighlevel` — GoHighLevel platform help (all-in-one CRM + funnels + messaging + white-label SaaS resale, v2 API, webhooks)
- `/sales-kartra` — Kartra platform help (all-in-one for coaches/course creators — funnels, checkout, memberships, webinars, affiliates; inbound API + IPN webhooks)
- `/sales-groove` — Groove.cm-specific page building, checkout, and membership setup
- `/sales-checkout` — Checkout page optimization, order bumps, payment processing
- `/sales-email-marketing` — Post-funnel email sequences, abandoned cart, nurture campaigns
- `/sales-webinar` — Webinar funnel strategy, registration, replay sequences
- `/sales-membership` — Membership site setup and retention funnels
- `/sales-getresponse` — GetResponse platform help (conversion funnels, landing pages, webinar funnels)
- `/sales-closum` — Closum platform help (landing pages, forms, omnichannel automation)
- `/sales-mailchimp` — Mailchimp platform help (landing pages, signup forms, email sequences)
- `/sales-kit` — Kit platform help (landing pages, forms, Creator Profile, Commerce)
- `/sales-systemeio` — Systeme.io platform help (budget all-in-one — funnels, email, courses, webinars, affiliates, free plan; REST API + webhooks)
- `/sales-builderall` — Builderall platform help (budget all-in-one — website/funnel builders, MailingBoss email, SuperCheckout, courses, webinars; MailingBoss API + webhooks; funnel builder gated to a higher tier)
- `/sales-swai` — SWAI platform help (AI-driven funnel creation, landing pages, chat widget)
- `/sales-leadpages` — Leadpages platform help (landing pages, pop-ups, alert bars, A/B testing, Leadmeter)
- `/sales-unbounce` — Unbounce platform help (landing pages, Smart Traffic AI, A/B testing, popups, sticky bars, DTR)
- `/sales-landingi` — Landingi platform help (AI landing page builder — Lunar AI generator, 400+ templates, A/B testing, EventTracker, Smart Sections, DTR, programmatic pages, Orbit MCP; REST API + per-form webhooks; lower-cost Unbounce/Leadpages alternative)
- `/sales-instapage` — Instapage platform help (premium AI landing + post-click platform — AdMap, A/B testing, AI Experiments, Personalization/DTR, heatmaps; REST API + per-form submit webhook; the high-end Unbounce alternative)
- `/sales-seedprod` — SeedProd platform help (self-hosted WordPress page + Theme Builder plugin — coming-soon/maintenance pages, 13 ESP integrations, Dynamic Text, WordPress Abilities API; the WordPress-native Leadpages/Unbounce alternative, no native cart or A/B testing)
- `/sales-beaver-builder` — Beaver Builder platform help (stable, developer-friendly standalone WordPress drag-and-drop page builder by FastLine Media — live front-end editor with Modules/Rows/Columns, reusable Templates/Saved Rows, the Beaver Builder Theme, and Beaver Themer for dynamic headers/footers/archives via Field Connections (WordPress/ACF/WooCommerce data); flat per-plan licensing (1/3/50/unlimited sites), white labeling (Unlimited), and a real PHP developer API — custom modules extending FLBuilderModule + a large `fl_builder_*` hooks/filters surface. No hosted REST API or webhook — automate via the WordPress REST API (`_fl_builder_data` layout meta) + module/hooks API; clean semantic markup and low lock-in (text survives deactivation), no native A/B testing)
- `/sales-breakdance` — Breakdance platform help (standalone visual WordPress website/page builder by Soflyy, the Oxygen makers — a themeless front-end editor like Beaver Builder/Elementor, NOT a Gutenberg block plugin; Elements/Templates/Design Library, WooCommerce Builder, built-in Form Builder + Popup Builder, Dynamic Data, Element Studio custom-element IDE, Breakdance AI (provider-swappable via `breakdance_ai_api_endpoint`/`breakdance_ai_model`). Real PHP developer API — Form Actions API, Dynamic Data Field API, Conditions API, `breakdance_*` hooks/filters — but no hosted REST API/outbound webhook; the form **Webhook action** POSTs to Zapier/Make and page layout is opaque post meta. Free + Pro ~$199.99/yr unlimited sites, no lifetime plan; key gotcha: spam plugins can't intercept the form Email action)
- `/sales-spectra` — Spectra platform help (Gutenberg-native WordPress website/page builder plugin by Brainstorm Force, formerly Ultimate Addons for Gutenberg — 30+ blocks, flexbox Container, Starter Templates, Popup Builder, Coming Soon mode; Pro Loop Builder/Dynamic Content/display conditions/white label. No hosted REST API — extend via WP hooks/filters (`uagb_post_query_args_*`, `spectra_pro_rest_api_get_controllers`); extends rather than replaces Gutenberg, lean DOM, no native cart or A/B testing)
- `/sales-kadence` — Kadence Blocks platform help (Gutenberg page-builder block plugin by StellarWP — 20+ free blocks incl. Row Layout/Section containers + Advanced Form; Pro Advanced Query Loop, Dynamic Content (ACF/MetaBox/WooCommerce), Design Library + Kadence AI. No hosted REST API — extend via WP hooks/filters (`kadence_blocks_posts_query_args`, `kadence_blocks_pro_query_loop_query_vars`, `kadence_element_display`) and Advanced Form webhooks (Pro). The closest Spectra/GenerateBlocks rival; dynamic-CSS performance tuning, no native cart or A/B testing)
- `/sales-generateblocks` — GenerateBlocks platform help (minimalist, high-performance Gutenberg block plugin by EDGE22/GeneratePress — a few composable primitives (Container, Grid, Headline, Button, Image, Query Loop) for the leanest DOM/CSS; Pro Dynamic Data/Global Styles/templates. No hosted REST API — extend via WP hooks/filters (`generateblocks_dynamic_tag_output`, `generateblocks_do_content`) and the `GenerateBlocks_Register_Dynamic_Tag` class (2.0+). The performance/dev pick vs Kadence/Spectra; no native cart, form block, or A/B testing)
- `/sales-stackable` — Stackable platform help (design-focused, Gutenberg-native block plugin by Gambit Technologies/gambitph — 42 free blocks (Columns, Hero, Card, Carousel, Pricing, Blog Posts), Global Design System, 375+ Design Library, theme.json support; Pro Dynamic Content (ACF/Metabox/JetEngine), Motion Effects, Conditional Display, Role Manager, per-block Custom CSS. No hosted REST API — extend via the `stackable_force_css_load` filter + WordPress `render_block`; GPLv3 source. Lean footprint but **no form/popup/header-footer builder or WooCommerce blocks**; v2→v3 migration is the key gotcha)
- `/sales-nexter` — Nexter platform help (all-in-one Gutenberg-native WordPress ecosystem by POSIMYTH Innovations; slug the-plus-addons-for-block-editor, GPLv3 — Nexter Blocks 90+ blocks + in-editor AI (ChatGPT/Gemini), Nexter Extension 50+ tools + Theme Builder, Nexter Theme; ships a Form Builder, Popup Builder, Mega Menu, and Header/Theme Builder. The standout: **Nexter Abilities**, a native MCP server exposing 115 AI tools to Claude/Cursor/VS Code to compose `tpgb/` blocks from a prompt. Pro Dynamic Content (ACF/Toolset/Pods)/WooCommerce blocks/animations/White Label. No hosted REST API — extend via the MCP server + WordPress REST API (`tpgb/` markup) + asset flags (`tpgb_defer_css_js`). The feature-breadth opposite of Stackable/GenerateBlocks; v4.7.0 ApiVersion-3 conversion is the key update boundary; no native cart or A/B testing)
- `/sales-gutenverse` — Gutenverse platform help (free, Gutenberg-native FSE block plugin + ecosystem by Jegstudio — 57 blocks, 600+ starter templates, built-in Popup Builder, global colors/fonts, companion Unibiz FSE theme, plus a **separate free Gutenverse Form** plugin (entries stored in WordPress, CSV export, email notifications, reCAPTCHA). Pro adds dynamic data, display conditions, custom fonts, premium templates/blocks, mega menu, advanced form features. No hosted REST API/webhook — automate via the WordPress core REST API (`gutenverse/` block markup) + the `gutenverse-core` framework hooks (`gutenverse_after_init_framework`/`gutenverse_include_block`/`gutenverse_block_config`); no native cart or A/B testing; key gotcha: the editor page failing to load after a customization change)
- `/sales-gutenkit` — GutenKit platform help (feature-rich Gutenberg-native block plugin + page builder by Wpmet, the ElementsKit makers; slug `gutenkit-blocks-addon`, 70k+ installs, Block API v3, zero jQuery — 65+ blocks on a flexbox Container, 900+ templates, FSE-compatible; Pro Mega Menu, Query Loop Builder, Dynamic Content (post meta/ACF), Display Conditions, One Page Scroll/Sticky/Glass Morphism/Parallax. Lead capture is a Mailchimp opt-in block only — no full form builder. No hosted REST API/webhook — automate via the WordPress core REST API (`gutenkit/` block markup) + `render_block`; no native cart or A/B testing. Key gotchas: a block "encountered an error and cannot be previewed" / editor won't load after a change, and the Template Library erroring inside ElementsKit Lite)
- `/sales-superb-addons` — Superb Addons platform help (Gutenberg-native block-addon plugin by SuperbThemes/Suplugins; slug `superb-blocks`, 80k+ installs — 20 blocks, 200+ patterns, 50+ pre-built pages, a real **form builder** (multi-step, calculated fields, anti-spam, **webhook + Mailchimp/Brevo/Google Sheets/Slack** integrations), a **Popup block** with smart triggers, 70+ animations, and a **Theme Designer**. Form + popup make it closest to Spectra/Nexter among block plugins. No hosted REST API/MCP — automate via the form webhook + native integrations + the WordPress core REST API (`superb/` block markup); no native cart or A/B testing. Plan-gating is ambiguous (readme says free forms, pricing page lists them Premium); the **Theme Designer not loading** is the #1 gotcha)
- `/sales-greenshift` — Greenshift platform help (performance-focused, animation-rich Gutenberg block plugin by Wpsoul — 50+ blocks, GSAP scroll/hover animations, Interaction Layers, 3D/Lottie/Rive, dynamic data + Query addon; the standout is an **API Connector** that binds external REST APIs, Google Sheets/CSV, and LLM APIs (OpenAI chat/streaming) into blocks, plus AI Helpers (bring-your-own key), a Figma/HTML/webpage→blocks converter, and a VS Code extension. No hosted REST API or webhook — extend via the WordPress REST API (`greenshift-blocks/` markup), the API Connector, and the `GSPB_API_RESPONSE` JS event. Free + Design/Woo/GreenLight PRO/All-in-One packs; no native cart or A/B testing)
- `/sales-convertri` — Convertri platform help (speed-focused funnel + landing-page builder with a free-form editor, built-in cart/upsells, and membership delivery; no public REST API — Zapier API key + custom webhooks with `cverify` SHA-1 signing; impression-metered pricing)
- `/sales-wix` — Wix platform help (no-code website builder with native commerce — landing pages + Wix Stores + custom checkout in one; Stores v3 + eCommerce Orders REST APIs, API-key/OAuth auth, signed-JWT webhooks, Wix Headless; eCommerce gated to Core+; JS-heavy SEO/perf + template lock-in caveats)
- `/sales-sendpulse` — SendPulse platform help (landing pages, email, SMS, chatbots, Automation 360)
- `/sales-audience-growth` — Growing an email list (lead magnets, cross-promotion, referral programs)
- `/sales-digital-products` — Selling digital products (platform selection, pricing, launch)
- `/sales-vwo` — VWO platform help (A/B testing, heatmaps, session recordings, personalization, feature flags)
- `/sales-jotform` — Jotform platform help (forms, payment collection, approval workflows — for the data capture step of funnels)
- `/sales-typeform` — Typeform platform help (conversational forms, quizzes, surveys — high-completion lead capture for funnels)
- `/sales-do` — Route to any sales skill by describing what you need

---
## Examples

### Example 1: Build a Lead Magnet Funnel

**User**: "I want to build a lead magnet funnel for my free PDF guide on meal planning."

**Approach**:
1. Clarify the audience (busy parents? fitness enthusiasts?) and traffic source.
2. Recommend a 2-page funnel: opt-in page + thank-you page.
3. Opt-in page structure: headline focused on outcome ("Plan a Week of Healthy Meals in 10 Minutes"), 3–4 bullet points on what's inside, simple name + email form, CTA button ("Send Me the Free Guide").
4. Thank-you page: confirm delivery vian email, introduce a tripwire offer ($7–$17 recipe bundle) to offset ad costs.
5. Platform: recommend based on user's existing tools. For beginners, Systeme.io (free tier) or Groove.cm.

### Example 2: Optimize a Low-Converting Sales Page

**User**: "My sales page converts at 1.2% — how do I improve it?"

**Approach**:
1. Ask for current metrics: traffic source, page length, offer, price, audience awareness level.
2. Compare 1.2% against benchmarks (cold traffic: 1–3% is normal; warm traffic: this is low).
3. Diagnose the most likely bottleneck: if traffic is warm and conversion is 1.2%, the page is underperforming — start with the headline and offer stack.
4. Recommend the testing priority order: headline first, then CTA, then social proof, then price presentation.
5. Provide specific headline formulas to test and suggest adding a video if there isn't one.
6. Check for mobile issues — ask if they've tested on phone.

### Example 3: Product Launch Funnel with Video Series

**User**: "Design a product launch funnel with a 4-video series leading to a cart open."

**Approach**:
1. Map the Jeff Walker PLF structure: squeeze page > PLC Video 1 > PLC Video 2 > PLC Video 3 > PLC Video 4 > Cart Open page > Cart Close page.
2. Each PLC (Pre-Launch Content) video page: video embed, key takeaway bullets below, comment section (optional), CTA to next video or to join the waitlist.
3. Video content arc: Video 1 = Opportunity (why now), Video 2 = Transformation (case studies), Video 3 = Ownership (how it works), Video 4 = The Offer (full pitch).
4. Cart open page: full long-form sales page with offer stack, testimonials, bonuses, countdown timer to cart close.
5. Email sequence: daily emails during PLC phase pointing to each video, then daily during cart-open with different angles (story, FAQ, objection handling, last chance).
6. Recommend platform based on needs — Groove.cm or ClickFunnels for the page flow, paired with their native or external email tool.

---
## Troubleshooting

### "My opt-in rate is below 20%"

- **Check the headline**: Is it promising a specific, desirable outcome? Vague headlines ("Get Our Free Guide") underperform specific ones ("The 5-Minute Morning Routine That Doubled My Energy").
- **Reduce form fields**: Every additional field beyond email drops conversion. Remove "phone" and "company" unless essential.
- **Match the ad to the page**: If running paid traffic, the opt-in page headline must mirror the ad copy. Disconnect = bounce.
- **Test the lead magnet name**: Sometimes the offer is good but the packaging is weak. Test different titles for the same asset.

### "People are adding to cart but not completing purchase"

- **Simplify the checkout**: Remove distractions, navigation, and unnecessary form fields. One-column layout, minimal steps.
- **Add trust signals**: SSL badge, money-back guarantee badge, payment logos (Visa, Mastercard, PayPal) near the payment fields.
- **Implement abandoned cart recovery**: Redirect to /sales-email-marketing for email and SMS follow-up sequences.
- **Test the price**: If cart abandonment is high, consider adding a payment plan option to reduce friction.

### "My upsell take rate is under 10%"

- **Check relevance**: The upsell must be a natural complement to what they just bought, not a random additional product.
- **Reduce price friction**: Price the upsell at 30–60% of the core offer. A $497 upsell after a $47 purchase feels jarring.
- **Simplify the decision**: One offer, one CTA, one clear benefit. Do not present multiple upsell options on the same page.
- **Add urgency**: "This offer is only available right now" — and mean it. Do not show the same "exclusive" upsell later in an email.
