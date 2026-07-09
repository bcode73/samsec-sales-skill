<!-- Source: https://getlaunchlist.com/help/docs/plugins/webhook, https://getlaunchlist.com/help/docs/widget/integrate-widget, https://getlaunchlist.com/help/docs/plugins/zapier, https://getlaunchlist.com/help/docs/tips/spam-protection, https://getlaunchlist.com/roadmap — captured 2026-06-06 -->

# LaunchList API Reference

> **No public REST API.** LaunchList's roadmap lists "API Access" as *planned* ("We are planning to provide LaunchList API") — as of 2026-06-06 it has not shipped. The programmatic surface today is:
>
> | Surface | Direction | Plan gate |
> |---|---|---|
> | Form POST endpoint (`/s/FORM_KEY`) | Ingress (add signups) | All plans |
> | Webhooks (`new_user`, `email_verify`) | Egress (push events) | Grow ($79 one-time)+ |
> | Zapier (New Submission, Email Verified) | Egress via iPaaS | Grow+ |
> | Slack + email notifications | Egress (human alerts) | Slack: Launch+; email: all plans |
> | CSV export | Egress (manual bulk) | All plans, UI-only |
>
> There is no endpoint to **read, update, or delete** submissions programmatically — exports are UI-only. No MCP server exists (nothing to wrap).

## Form POST endpoint (ingress)

The only way to add a signup programmatically. Two installation methods, verbatim from the widget docs:

### Embed widget (iframe)

```html
<script src="https://getlaunchlist.com/js/widget.js" defer></script>
<div class="launchlist-widget" data-key-id="FORM_KEY" data-height="180px"></div>
```

Replace `FORM_KEY` with your form key from the Integration page.

### Custom form (DIY)

```html
<form class="launchlist-form" action="https://getlaunchlist.com/s/FORM_KEY" method="POST">
    <input name="name" type="text">
    <input name="email" type="email">
    <button type="submit">Join Waitlist</button>
</form>
```

Tracking script required in the page `<head>`:

```html
<script src="https://getlaunchlist.com/js/widget-diy.js" defer></script>
```

**Rules (from docs):**
- The email field MUST be named `email`
- The form MUST have class `launchlist-form`
- Custom data fields are sent as additional `name`-attributed inputs
- `widget-diy.js` handles referral attribution (referral code parsing from the visitor's URL) — a bare server-to-server POST to `/s/FORM_KEY` records the signup but loses browser-side referral context
- Honeypot spam field (optional): `<input type="hidden" name="_gotcha" />` — submissions with `_gotcha` filled are rejected as bots
- AJAX form submission (submit without page reload) is a **Grow-tier** feature

## Webhooks (egress)

Setup: Plugins (sidebar) → "Create a webhook" → add URL → "Send a test request". Enable/disable or change the URL via the Edit link. **Grow tier ($79 one-time) and above.**

LaunchList sends `POST` requests with a JSON body to your URL on signup events. Two events are documented:

### `new_user` — fires when someone joins the waitlist

Payload, verbatim from the docs:

```json
{
    "event": "new_user",
    "id": "02a146c3-7b36-490c-a97f-bba76ba1c900",
    "waitlist_name": "My Website",
    "waitlist_key": "aa53Pf",
    "position": 49,
    "name": "Richard Hendricks",
    "email": "richard@piedpiper.com",
    "referral_code": "9ZK8QR",
    "users_referred": 0,
    "is_email_verified": null,
    "is_spam": 0,
    "info": {
        "browser": "Chrome",
        "browser_version": "100.0.3945.130",
        "platform": "Mac OS X",
        "platform_version": "10.13.6",
        "language": [
            "en-us",
            "en"
        ],
        "is_robot": false,
        "is_mobile": false,
        "is_tablet": false,
        "is_desktop": true,
        "is_bot": false,
        "ip": "162.223.73.159",
        "location": {
            "countryName": "United States",
            "countryCode": "US",
            "regionName": "California",
            "regionCode": "CA",
            "areaCode": "CA",
            "cityName": "Palo Alto",
            "zipCode": "94306",
            "isoCode": null,
            "postalCode": null,
            "latitude": "34.0544",
            "longitude": "-118.2441",
            "timezone": "America/Los_Angeles"
        },
        "analytics": {
            "utm_source": "Reddit",
            "utm_medium": "social",
            "utm_campaign": "launch",
            "utm_term": null,
            "utm_content": "posts",
            "http_referrer": "https://reddit.com/r/programming"
        }
    },
    "referred_by": {
        "id": "4465265f-b2bf-4cf1-8a48-46ccc59eb0c2",
        "waitlist_name": "My Website",
        "waitlist_key": "aa53Pf",
        "positon": 3,
        "name": "Gavin Belson",
        "email": "gavin@hooli.xyz",
        "referral_code": "ae4s4C",
        "users_referred": "29",
        "is_email_verified": "2022-07-17 19:14:37",
        "is_spam": 0,
        "info": {
            "browser": "Chrome",
            "browser_version": "101.0.4951.67",
            "platform": "Windows",
            "platform_version": "11.0",
            "language": [
                "en-us",
                "en"
            ],
            "is_robot": false,
            "is_mobile": false,
            "is_tablet": false,
            "is_desktop": true,
            "is_bot": false,
            "ip": "162.223.73.159",
            "location": {
                "countryName": "United States",
                "countryCode": "US",
                "regionName": "California",
                "regionCode": "CA",
                "areaCode": "CA",
                "cityName": "Palo Alto",
                "zipCode": "94306",
                "isoCode": null,
                "postalCode": null,
                "latitude": "34.0544",
                "longitude": "-118.2441",
                "timezone": "America/Los_Angeles"
            },
            "analytics": {
                "utm_source": "Twitter",
                "utm_medium": "cpc",
                "utm_campaign": "launch",
                "utm_term": null,
                "utm_content": "promoted",
                "http_referrer": "https://twitter.com"
            }
        },
        "created_at": "2022-07-17 19:14:37",
        "updated_at": "2022-07-17 19:14:37"
    },
    "created_at": "2022-07-24 19:14:37",
    "updated_at": "2022-07-24 19:14:37"
}
```

**Field notes (observed in the documented payload — verify against live events):**
- `referred_by.positon` — the position field inside `referred_by` is spelled `positon` (verbatim typo in LaunchList's docs). Top-level uses the correct `position`. Match both spellings when parsing.
- `referred_by` is `null`/absent for direct (non-referred) signups — guard before dereferencing.
- `is_email_verified` is `null` when unverified and a `"YYYY-MM-DD HH:MM:SS"` timestamp string when verified — it is NOT a boolean.
- `users_referred` appears as integer `0` at top level but string `"29"` inside `referred_by` — coerce types defensively.
- `is_spam` is `0`/`1` integer — `1` means LaunchList's fraud heuristics flagged the signup.
- `id` is a UUID — use it as the idempotency key for webhook deduplication.

### `email_verify` — fires when a signup verifies their email

Payload, verbatim from the docs:

```json
{
    "event": "email_verify",
    "id": "02a146c3-7b36-490c-a97f-bba76ba1c900",
    "waitlist_name": "My Website",
    "waitlist_key": "aa53Pf",
    "email": "richard@piedpiper.com",
    "email_verification_token": "uVMV7wKiiOno0p7seXOnU0fgimzqfZlFRb8yAf4UM5cTFaDeWw4AYWtDZm1O",
    "email_verification_token_sent_at": "2023-05-21 06:43:18",
    "email_verified_at": "2023-05-23 06:43:18"
}
```

The `id` matches the `new_user` event's `id` for the same person — join on it.

### Webhook security & delivery

- **No signing scheme documented** — no HMAC signature header, no shared-secret mechanism in the public docs. Mitigations: use an unguessable webhook URL path, validate payload shape (`event` + `waitlist_key` matching your waitlist), and treat the webhook as a trigger to act on data you already trust rather than as authoritative input.
- **No retry policy documented** — assume at-most-once delivery and reconcile against CSV exports periodically if completeness matters.
- A "Send a test request" button exists in the webhook modal for connection testing.

## Zapier (egress via iPaaS)

Setup, from the docs:
1. Plugins (sidebar) → scroll to Zapier → **Generate Access Token** (unique per project)
2. In Zapier: Create Zap → search "LaunchList" → authenticate with the access token

**Triggers:**
- **New Submission** — fires per signup; payload mirrors the `new_user` webhook (name, email, position, referral info, device, geolocation, UTM analytics, `referred_by` object)
- **Email Verified** — fires on email verification

No Zapier **actions** are documented (you cannot add signups via Zapier — use the form POST endpoint). Connects to 3,000+ apps; docs name Google Sheets, Airtable, Mailchimp, HubSpot, ConvertKit (Kit) as common destinations. Zapier is a **Grow-tier** feature.

No Make, Pabbly, or Pipedream integrations are documented.

## Spam protection surface

From the spam-protection docs — these operate at the form/ingress layer:

- **Google ReCaptcha v2**: register at google.com/recaptcha, add the secret key under Submissions settings; LaunchList verifies each new signup
- **Honeypot**: `<input type="hidden" name="_gotcha" />` in custom forms — bots that fill it are rejected
- **Cloudflare**: route your domain through Cloudflare; bot users blocked before reaching the form
- **Temporary email blocking**: built-in blocklist of 3,000+ disposable-email domains (temp-mail.org, guerrillamail.com, etc.) — enable in Blocks settings
- **Email validation + verification**: validation on all plans; verification emails from Launch tier
- **Domain/pattern blocking rules**: block specific domains or patterns in Blocks settings

## Gaps

- **No read/update/delete API** — submissions are export-only (CSV via UI). A reconciliation pipeline must rely on webhooks + periodic manual exports.
- **Webhook signing and retry behavior undocumented** — confirmed absent from public docs, not confirmed absent from the product; ask support if it matters.
- **Rate limits undocumented** — no published limits for the form POST endpoint.
- **`email_verify` payload omits referral fields** — re-join with the stored `new_user` record via `id`.
- **Roadmap "API Access" item has no ETA** — re-check https://getlaunchlist.com/roadmap before building workarounds for a long-lived integration.
