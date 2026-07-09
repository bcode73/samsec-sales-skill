# MemberVault — Learnings

Accumulated platform knowledge. Append new findings with the date discovered.

**2026-06-22**: Research baseline. MemberVault (membervault.co) is a "binge & buy" course/membership platform for solopreneurs, coaches, and creators. Put all paid + free offers in one marketplace; it tracks who views the sales info of products they don't own and auto-tags them warm/hot lead — engagement doubles as lead gen. Gamification via Engagement Points (EP), communities, drip content (progressive/date/timed), quizzes. Positioned vs Teachable/Kajabi/Podia/Systeme.io/Mighty Networks.

- **No public REST API.** Integration surface = Zapier (7 triggers: Completed Lesson, Completed Module, Earned X EP, Hot Lead, User Completes an Action, User Added to a Product, User Email Consent; 2 actions: Add User to Product, Remove User From Product) + inbound webhooks (grant access from external cart — "API URL" from Integrations → Advanced, embeds custom domain + `course_id`) + outbound webhooks (product Actions → "Call a web hook"; sends email/first/last name). No MCP server.
- ⚠️ Exact inbound webhook params and auth scheme are NOT publicly documented — the URL itself is the credential. Confirm by copying from Integrations → Advanced; capture an outbound delivery on webhook.site to learn the exact keys.
- **Does NOT send marketing email** — requires a connected ESP. Native: Kit (ConvertKit), MailerLite, ActiveCampaign; others via Zapier/webhooks. Top complaint: paying for Zapier to connect a non-native ESP eats into margins.
- **0% transaction fees on all plans** (direct Stripe/PayPal). Identity = email (one login, products attach to email).
- **Pricing (best-effort):** Free (≤100 members, limited); 5 Product ~$29/mo (1 community); 15 Product ~$49/mo (3 communities, "Best Deal"); Unlimited ~$109/mo. Lifetime deals ("Cash Kickstart", "Unlimited Lifetime") appear periodically. All paid plans include all features — tiers differ only by product/community counts.
- **Top review pain points:** no built-in email; limited video hosting (host elsewhere); fixed marketplace design; clunky member self-cancellation; weak search with large libraries; "essential features only."
- Affiliate program: MemberVault has historically run an affiliate/referral program — note for `_internal/affiliates.md` if tracking.
- Adjacent platforms surfaced → backlog: Graphy (all-in-one course/website/app builder), Memberstack (no-code membership/auth/payments API for Webflow sites), group.app (creator community platform). Absorb LMS seen but skipped (enterprise corporate L&D, outside creator/GTM audience).
