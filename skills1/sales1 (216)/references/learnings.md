# GroupApp — Learnings

Accumulated platform knowledge. Append new findings with the date discovered.

**2026-06-22**: Research baseline. GroupApp (group.app) is a **learning-focused community platform** for creators, coaches, and learning businesses — communities/channels + a deep LMS (drag-and-drop curriculum builder, modules/lessons, enforced completion, native or embedded video Wistia/YouTube/Vimeo), auto-issued branded certificates, progress tracking, events (RSVP), memberships, and **B2B group subscriptions** (one manager buys seats for a team). 0% transaction fees on every plan. Positioned vs Circle/Skool/Mighty Networks; its edge is LMS depth + certificates + group subscriptions; weaker on white-label/branding (vs Circle) and gamification (vs Skool).

- ⚠️ Marketing/pricing pages are **JS-rendered** — WebFetch returned empty. Research assembled from the GroupApp help center + integration listings + comparison roundups. Re-verify pricing/features live.
- **Integration surface:** API token (Admin Panel → Settings & Data → Integrations → API Token → Generate New Token); webhooks (Settings → Integrations); OAuth (custom integrations + login/SSO); native Stripe/Zoom/email; Zapier + Pabbly + Integrately. **No MCP server.** A comprehensive public REST endpoint reference was NOT found — confirm endpoints in-account; for most flows use Zapier/webhooks.
- **Zapier triggers (11):** New community member, Members' Profile updated, Course enrollment, Course lessons completed, New Payment, Event RSVP, Course completed, Subscription canceled, New Post, Payment Failed, Membership Questionnaire.
- **Zapier actions (10):** Invite new members, Create a member by email, Add a member to a channel, Remove Channel Member, Remove community members, Enroll a member in a course, Remove Enrollment, Add a member to a segment, Remove a member from a segment, Add a user to your community.
- **Identity = email**; **segments** are the tag/grouping primitive driving automations. Fulfill on **New Payment** (success), use **Payment Failed** for dunning, **Subscription canceled** for win-back.
- **Pricing (best-effort + conflicting):** one source "from $24/mo, 0% fees"; a third-party roundup lists $49–$259/mo across tiers. 0% GroupApp fee on all plans (connect own Stripe; Stripe fees still apply). Verify live.
- Does NOT send marketing email — connect an ESP and trigger off events.
- Adjacent platforms surfaced → backlog: Heartbeat, Swarm, BuddyBoss, AccessAlly, LearnDash, Patreon. Skipped: Bettermode/Khoros/Hivebrite/Disciple/Disco (enterprise community), Discord/Slack/Reddit/Facebook Groups (social, no ownership/monetization), Circle/Mighty Networks/Kajabi/Skool/MemberPress/LearnWorlds/Thinkific (already cataloged/backlog).
