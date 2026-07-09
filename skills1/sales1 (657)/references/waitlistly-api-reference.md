<!-- Source: https://waitlistly.live/help , https://waitlistly.live/sitemap.xml (fetched 2026-06). Homepage and /growth are JS-rendered SPAs; no /api or /docs page exists. -->

# Waitlistly — Programmatic Surface

> **No public REST API.** Waitlistly does not publish API documentation, and its sitemap contains no `/api` or `/docs` path (only `/`, `/growth`, `/help`, `/contact`, `/login`, `/signup`, `/privacy`, `/terms`). There is **no documented way to list, read, update, or delete signups in code.** The only documented programmatic surface is the **on-signup webhook** and its iPaaS connectors. Do not design an integration around endpoints that don't exist.

## What exists (verified from Help → Webhooks/Integrations)

> "Send real-time lead data to Zapier, Make, Slack, or your own API when someone joins your waitlist." — Waitlistly Help

| Surface | Direction | Trigger | Destination |
|---|---|---|---|
| Webhook (custom endpoint) | Egress (out of Waitlistly) | A person joins the waitlist | Your own HTTPS endpoint |
| Zapier | Egress → iPaaS | New waitlist signup | 1000s of Zapier apps |
| Make | Egress → iPaaS | New waitlist signup | Make scenarios |
| Slack | Egress | New waitlist signup | A Slack channel |

There are **no documented inbound endpoints** (no signup-create API, no read/list API, no admin API).

## Webhook payload

**The payload schema is NOT published.** Treat it as opaque and discover it empirically:

1. Stand up a receiver (see `platform-guide.md` Recipe 2) or use a request-inspector URL.
2. Paste that URL into Waitlistly's webhook setting (Help → Webhooks/Integrations).
3. Submit a real test signup on your waitlist page.
4. Read the logged body — that is the source of truth for field names. Map from it.

```json
<!-- Constructed/representative ONLY — NOT from Waitlistly docs. Replace with the real delivery. -->
{
  "event": "signup.created",
  "email": "founder@example.com",
  "waitlist": "my-idea",
  "referrer": null,
  "created_at": "2026-06-19T12:00:00Z"
}
```

## Auth & security

- **No documented signature/HMAC** on the webhook and **no documented retry policy.**
- Mitigations: use an **unguessable endpoint path** (or a shared-secret query parameter you check server-side), **validate the payload shape**, make the handler **idempotent** on the most stable id the payload carries, and run a periodic **dashboard export** as reconciliation (since you can't re-pull via an API).

## Custom domains (verified from Help → Custom Domains)

- Point your own domain/subdomain at the Waitlistly landing page via the DNS record Waitlistly specifies in the dashboard.
- Allow time for DNS propagation and SSL certificate issuance (commonly up to 24–48h).
- This is a UI + DNS feature, not an API.

## Gaps (could not be verified — confirm in-app)

- **Pricing / tiers / subscriber caps** — no public `/pricing`; "free to start" is the only confirmed claim.
- **Whether webhooks/custom domains are free or plan-gated.**
- **Referral / viral mechanics** — a `/growth` page exists but rendered blank; leaderboard/position-jumping unconfirmed.
- **Analytics** — assumed present (category norm) but not documented.
- **In-app email sending** — no evidence; assume Waitlistly is capture-only and send launch/nurture mail from your ESP.
- **Exact webhook payload fields, event types, and delivery semantics** (retries, ordering, timeouts).
