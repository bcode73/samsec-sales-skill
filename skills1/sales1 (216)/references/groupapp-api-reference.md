<!-- Source: https://help.group.app/en/articles/31-zapier-integration -->
<!-- Source: https://help.group.app/en/articles/117-how-to-generate-api-token -->
<!-- Source: https://help.group.app/en/articles/135-how-to-set-up-webhooks -->
<!-- Source: https://www.group.app/integrations/ -->

# GroupApp (group.app) Integration & API Reference

> **Accuracy note (research baseline 2026-06-22).** GroupApp's marketing and pricing pages are JavaScript-rendered and did not return content to WebFetch; the details below were captured from the GroupApp help center and integration listings. GroupApp exposes an **API token** and **webhooks**, but a comprehensive public REST endpoint reference was not found — **confirm exact endpoints/payloads in the GroupApp help center or your in-account API docs.** The richest *documented* surface is **Zapier** (triggers + actions, captured verbatim below). Nothing here is invented; gaps are flagged.

## Integration surface at a glance

| Mechanism | Direction | Use it for |
|---|---|---|
| **API token** | both | Secure programmatic access; connect external integrations (generated in-app) |
| **Webhooks** | GroupApp → external | Real-time push when community/course/payment events happen |
| **OAuth** | both | Custom integrations + login/SSO ("enterprise-grade authentication flows") |
| **Zapier / Pabbly / Integrately** | both | No-code automation; 11 triggers + 10 actions on Zapier |
| **Native** | — | Stripe (payments, 0% GroupApp fee), Zoom, email |

No MCP server.

## Authentication (API token)

Generate a token in-app: **Admin Panel → Settings & Data → Integrations → API Token tab → "Generate New Token."** Use it to authenticate external integrations. Treat it as a secret (server-side only).

> The exact header name and base URL for direct REST calls were not published in the captured sources — confirm in the in-account API docs / help center before building direct calls. For most automations, the Zapier/webhook paths below are the supported route.

## Webhooks

Set up under **Settings → Integrations (Webhooks)** — "automatically send data when important events happen." Point a webhook at your endpoint to receive events in real time. Exact payload schemas/signature were not published in captured sources — capture one delivery against a request bin (e.g. webhook.site) to confirm field keys before parsing.

## Zapier — Triggers (events GroupApp emits, verbatim)

1. **New community member** — fires when a member joins
2. **Members' Profile updated** — fires on profile information changes
3. **Course enrollment** — fires when a member enrolls
4. **Course lessons completed** — fires when a member marks a course complete
5. **New Payment** — fires on payment transactions
6. **Event RSVP** — fires when a member RSVPs
7. **Course completed** — fires on course completion
8. **Subscription canceled** — fires on cancellation
9. **New Post** — fires when a community post is created
10. **Payment Failed** — fires on failed payment attempts
11. **Membership Questionnaire** — fires when a pending member responds to questions

## Zapier — Actions (writes into GroupApp, verbatim)

1. **Invite new members** — sends email notification to join the community
2. **Create a member by email** — creates a community member on the free plan
3. **Add a member to a channel** — adds an existing member to a channel
4. **Remove Channel Member** — removes a member from a channel
5. **Remove community members** — removes a member from the community
6. **Enroll a member in a course** — enrolls a user in a course
7. **Remove Enrollment** — removes a course enrollment
8. **Add a member to a segment** — adds a member to a segment
9. **Remove a member from a segment** — removes a member from a segment
10. **Add a user to your community** — adds a GroupApp account holder to a community

**Setup:** accept the Zapier invitation; GroupApp's app is added to your account for building Zaps.

## Data model (representative — confirm in-app)

```json
// Member
{ "email": "jane@example.com", "name": "Jane Doe", "segments": ["vip"], "channels": ["general"] }

// Course enrollment (Zapier "Course enrollment" / "Enroll a member in a course")
{ "member_email": "jane@example.com", "course": "Signature Program", "status": "enrolled" }

// Payment (Zapier "New Payment" / "Payment Failed")
{ "member_email": "jane@example.com", "amount": 4900, "currency": "USD", "status": "succeeded" }
```

- **Identity is email.** Members, enrollments, and payments key on the member's email — match/dedupe on it.
- **Segments** are GroupApp's tagging/grouping primitive — use Add/Remove segment actions to drive automations.

## Notes that matter for integrations

- **No published full REST reference** — for code beyond Zapier/webhooks, generate an API token and confirm endpoints in the in-account API docs/help center; don't assume paths.
- **Grant access on a paid event, not enrollment intent** — use **New Payment** (success) to fulfill, and handle **Payment Failed** for dunning.
- **0% GroupApp transaction fee** on every plan (you connect your own Stripe) — Stripe's own fees still apply.
- **B2B group subscriptions** (one manager buys for a team) are a GroupApp differentiator — relevant when modeling seats/access.
