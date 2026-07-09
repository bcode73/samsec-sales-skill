<!-- Source: https://preshiplist.co/ , https://preshiplist.co/features , https://preshiplist.co/pricing , https://preshiplist.co/sitemap.xml (fetched 2026-07). Marketing pages only; no /api, /docs, or /integrations path exists. -->

# Preshiplist Platform Reference

## Overview

Preshiplist (preshiplist.co) is a no-code **pre-launch waitlist builder** for SaaS and app makers — "the fastest way to create waitlists for SaaS and Apps," with zero database setup. You pick from design/marketing-validated templates, publish a hosted (or custom-domain) waitlist page, and collect emails before you build. Its distinguishing feature within the indie waitlist family is that it also **sends the emails itself** via built-in drip sequences, so it doubles as a lightweight ESP for launch/nurture. Target users: solo founders, early-stage startups, and scale-ups. Differentiator: capture + send in one closed, self-contained tool that markets "no third-party integrations needed."

> **Research caveat.** The pricing page names tiers but does not publish exact figures ("limited-time launch pricing"), and there is no public `/api`, `/docs`, or `/integrations`. Verified facts come from the homepage, `/features`, `/pricing`, and the sitemap. Anything tagged *(unconfirmed)* below needs checking against the live app before you rely on it.

## Capabilities & automation surface

| Capability | What it does | Automation surface | Confidence |
|---|---|---|---|
| Hosted waitlist landing page | Publish a waitlist page from 7+ validated templates; customizable multi-field forms | UI-only | Verified (core pitch) |
| Custom domains + SSL | Point your own domain/subdomain at the page | UI + DNS | Verified (`/features`) |
| Built-in email drip sequences | Auto-branded confirmation, launch-day, and update emails; add/remove/reschedule steps; deliverability monitoring | UI-only (Preshiplist sends) | Verified (`/features`) |
| AI content generation | AI-written headlines, subheadlines, product highlights, conversion copy | UI-only | Verified (`/features`) |
| Signup dashboard | CRM-like list of signups | UI-only | Verified |
| Analytics | Signups by country, source, device, time; portfolio-wide metrics | UI-only | Verified (`/features`) |
| Short links + click tracking | Trackable short links for the waitlist | UI-only | Verified (`/features`) |
| OG social images | Auto social share images | UI-only | Verified (`/features`) |
| Multi-product portfolio | Run several products/waitlists; consolidated metrics + global signup notifications | UI-only | Verified (Serious Builder tier) |
| CSV export | One-click export of the signup list | **UI export only (the sole egress)** | Verified (`/features`, `/pricing`) |
| Referral / viral loop | A referral leaderboard or position-jumping mechanic | — | *(unconfirmed — only social-proof counts/notifications are advertised)* |
| Public REST API | Programmatic read/write of signups | — | **Verified absent** (no `/api`/`/docs`; site markets "no integrations needed") |
| Webhooks | Real-time push on signup | — | **Verified absent** |
| Zapier / Make | No-code routing | — | **Verified absent** |
| MCP server | — | — | None found |

**Rule of thumb:** there is **no programmatic hook at all**. Data comes out only via a manual CSV export. Design any downstream flow around that file, not around endpoints or events that don't exist.

## The email-drip model (the differentiator)

Most indie waitlist tools are capture-only — they collect emails and you send the launch broadcast from a separate ESP. Preshiplist is different: it **sends the emails itself**.

- Drip sequences are **auto-branded** to match the product's waitlist ("without touching templates").
- Typical steps: **signup confirmation**, **launch-day announcement**, and **product updates**.
- Sequences are editable — add, remove, or reschedule emails anytime.
- Built-in **deliverability monitoring** is advertised.
- **Implication:** you don't need an ESP for the launch send. But the flip side is lock-in — to run those contacts through your own ESP's automations (or a CRM), you must **export the CSV first**; there's no live sync.
- **Timing matters:** ensure the confirmation email fires immediately on signup. The window between signup and the first share/engagement is short (~60s), so a delayed or missing first email costs you momentum.

## Pricing, limits & plan gates

*Best-effort — exact figures are not published (launch/quarterly pricing). Confirm at `preshiplist.co/pricing`.*

| Tier | Publish live? | Products | Notes |
|---|---|---|---|
| **Free** | **No — draft/preview only** | 1 | Build, customize, and preview but **cannot publish or collect signups**. $0 forever. |
| **Chill Builder** | Yes | 1 | Unlimited draft + published waitlists, unlimited signups, unlimited drip sequences, custom domains, signup validation + CSV export, AI copy, short-link tracking, OG images. |
| **Serious Builder** | Yes | **Unlimited** | Everything in Chill + global signup notifications across the portfolio + consolidated metrics across products. |
| **Lifetime Partner** | Yes | Unlimited | One-time payment; all Serious Builder features + future features, priority announcements. |

- **No per-signup charges; no caps on signups on paid tiers.** "The price you see is the price you pay."
- **Payment:** major cards + PayPal. **Refunds:** 30-day (monthly) / 60-day (quarterly) / 90-day (yearly). Quarterly billing is nudged as the default.
- **Integration impact:** because there's no API on *any* tier, the free-vs-paid question that matters is simply **publish + collect** (paid) vs **draft-only** (free), and **1 product** (Chill) vs **many** (Serious/Lifetime).

## Integrations

Data flow is **egress-only and manual**: Preshiplist → CSV → wherever you take it.

- **No native CRM connectors, no inbound API, no webhooks, no Zapier/Make, no MCP.** The site explicitly frames "no third-party integrations needed" as a selling point (self-contained: capture + email in one).
- The only bridge to other systems is the **CSV export**. Everything downstream (CRM import, feeding your own ESP, analytics) starts from that file.

## Data model

There is no API and no documented webhook payload, so the only concrete data artifact is the **exported CSV**. Its exact columns aren't published; expect at least an email and a signup timestamp, plus whatever custom form fields you added.

```csv
# Representative ONLY — column names/order are not published. Confirm against a real export.
email,created_at,source,country,device,<your_custom_fields...>
founder@example.com,2026-07-07T12:00:00Z,twitter,US,mobile,...
```

Practical handling of the export:
- **Dedupe on `email`** (there's no documented stable id) when re-importing after successive exports.
- **Guard optional columns** — source/country/device/UTM and custom fields may be blank for direct signups.
- **Track a high-water mark** (max `created_at` you've already imported) so a scheduled job only upserts new rows instead of re-processing the whole file.

## Quick-start recipes

Because there's no API/webhook, "automation" here means automating over the **exported CSV**. These are the realistic patterns.

### Recipe 1 — One-off: get the list into your CRM/ESP
1. Dashboard → export signups as **CSV**.
2. Import into your CRM/ESP (HubSpot import, Mailchimp/Kit audience import, Google Sheets, etc.), mapping `email` (+ created-at/source if present).
3. Dedupe on `email` so re-imports don't duplicate contacts.
4. Remember the launch email can send from Preshiplist itself — only export if you specifically want the contacts in *your* stack.

### Recipe 2 — Scheduled CSV → CRM upsert (over an exported file)
```python
# Batch, NOT real-time. Point this at the most recent CSV export you downloaded
# (Preshiplist has no API to pull from, so a human/cron drops the file here).
import csv, os
from datetime import datetime

STATE = "preshiplist_highwater.txt"   # last created_at already imported
CSV_PATH = "preshiplist_export.csv"    # the file you exported from the dashboard

def load_highwater():
    return open(STATE).read().strip() if os.path.exists(STATE) else ""

def save_highwater(ts):
    open(STATE, "w").write(ts)

def run():
    hw = load_highwater()
    newest = hw
    with open(CSV_PATH, newline="") as f:
        for row in csv.DictReader(f):
            email = (row.get("email") or "").strip().lower()
            created = row.get("created_at", "")
            if not email:
                continue
            if hw and created <= hw:      # already imported in a prior run
                continue
            # upsert_contact_to_crm(email=email, source="preshiplist", joined=created)
            if created > newest:
                newest = created
    if newest:
        save_highwater(newest)

if __name__ == "__main__":
    run()
```
**Gotchas:** it can only be as fresh as your last export — there's no push. Dedupe on `email`. Normalize case/whitespace. Confirm the real column names against an actual export before trusting `email`/`created_at`.

### Recipe 3 — Configure the launch-day drip (no external ESP)
1. In Preshiplist email/drip settings, confirm a **confirmation email fires immediately** on signup.
2. Add a **launch-day** step and schedule it for your go-live date; keep the confirmation → nurture → launch order sensible.
3. Send yourself a real test signup and verify the confirmation arrives instantly and renders with your branding.
4. Watch the deliverability indicator; if a critical launch and deliverability looks shaky, export the list and broadcast from a dedicated ESP instead (`/sales-email-marketing`).

## Integration patterns

- **Treat Preshiplist as a terminal capture+send node, not a data source you can sync.** Ingress is the hosted/custom-domain form; the launch/nurture emails send from Preshiplist; egress is a manual CSV. There is no write-back, no read API, no event stream.
- **No backfill problem, but a freshness problem.** Unlike webhook-based tools you never "miss" a signup (they're all in the dashboard), but any external copy is only as current as your last export — schedule exports if you need a semi-fresh mirror.
- **If the requirement is real-time or event-driven** (fire a Slack ping on signup, sync to CRM instantly, trigger a downstream automation), Preshiplist cannot do it — pick a tool with a documented API/webhooks.

## Fit vs. other indie waitlist tools

| Need | Better fit |
|---|---|
| Waitlist page **plus** built-in launch/nurture emails, no separate ESP, closed & simple | **Preshiplist** |
| Fastest idea-validation page with on-signup webhooks → Zapier/Make/Slack | `/sales-waitlistly` |
| Documented REST API + HMAC-signed webhooks + built-in broadcasts | `/sales-waitlister` |
| Developer widget, unauthenticated signup API, censored public leaderboard | `/sales-getwaitlist` |
| One-time lifetime pricing instead of subscription | `/sales-launchlist` |
| Waitlists **plus** giveaways/contests with fraud webhooks + REST API | `/sales-kickofflabs` |
| The growth *strategy* (lead magnets, referral design, driving traffic) — tool-agnostic | `/sales-audience-growth` |
