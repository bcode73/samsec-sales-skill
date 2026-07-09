<!-- Source: https://preshiplist.co/ , https://preshiplist.co/features , https://preshiplist.co/sitemap.xml (fetched 2026-07). No /api, /docs, or /integrations path exists in the sitemap. -->

# Preshiplist — Programmatic Surface

> **No public API. No webhooks. No Zapier/Make. No MCP.** Preshiplist publishes no developer documentation, and its sitemap contains only marketing pages — `/`, `/features`, `/pricing`, `/blog`, `/founder-letter`, `/use-cases/early-stage-startups`, `/use-cases/scale-ups`, `/use-cases/solo-founders`, `/legal`. There is **no `/api`, `/docs`, or `/integrations` path.** The homepage explicitly markets "no third-party integrations needed." **The only way data leaves Preshiplist is a manual CSV export from the dashboard.** Do not design an integration around endpoints, webhooks, or Zapier steps that do not exist.

## Egress surface (the only one)

| Surface | Direction | Trigger | Destination |
|---|---|---|---|
| CSV export | Egress (out of Preshiplist) | Manual click in dashboard | A `.csv` file you download |

There are **no inbound endpoints** (no signup-create API, no read/list API, no admin API) and **no real-time egress** (no webhook, no Zapier trigger, no Slack notification to an external channel).

## What Preshiplist does instead of integrations

Preshiplist is deliberately self-contained: it **captures** signups (hosted/custom-domain page) and **sends** the emails (built-in, auto-branded drip sequences — confirmation, launch-day, updates). That's why it advertises needing no third-party tools — the launch email you'd normally wire an ESP for is handled in-app. The trade-off is zero programmatic access: to move contacts into your own CRM/ESP you export the CSV.

## Exported CSV shape

**The column set is NOT published.** Treat it as opaque until you open a real export:

```csv
<!-- Representative ONLY — NOT from Preshiplist docs. Confirm columns against a real export. -->
email,created_at,source,country,device
founder@example.com,2026-07-07T12:00:00Z,twitter,US,mobile
```

Practical handling:
- **Dedupe on `email`** — no documented stable id.
- **Guard optional columns** (source/country/device/UTM/custom fields may be blank).
- **Track a high-water mark** on `created_at` so a scheduled job only upserts new rows (see `platform-guide.md` Recipe 2).

## If you need real-time / event-driven integration

Preshiplist cannot do it. Use a waitlist tool with a documented programmatic surface:
- **`/sales-getwaitlist`** — REST API (`api.getwaitlist.com/api/v1`), unauthenticated `POST /signup`, `new_signup`/`offboarded_signup` webhooks.
- **`/sales-waitlister`** — REST API + five HMAC-signed webhook events + built-in broadcasts.
- **`/sales-waitlistly`** — on-signup webhooks → Zapier/Make/Slack/your own endpoint.

## Gaps (could not be verified — confirm in-app)

- **Exact CSV columns / export format / field names.**
- **Exact paid prices** — pricing page names tiers (Chill Builder / Serious Builder / Lifetime Partner) but shows no figures ("limited-time launch pricing").
- **Whether any referral/viral mechanic exists** — only social-proof signup counts/notifications are advertised; no leaderboard/position-jumping documented.
- **Email drip specifics** — exact trigger events, scheduling granularity, sending-domain/DKIM setup, and deliverability-monitoring details.
- **Custom-domain DNS record details and SSL issuance time.**
