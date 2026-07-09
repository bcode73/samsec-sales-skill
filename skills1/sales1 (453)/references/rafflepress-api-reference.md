<!-- Source: https://rafflepress.com/docs/webhooks/ and https://rafflepress.com/docs/zapier/ and https://rafflepress.com/docs-categories/developer/ (fetched 2026-06) -->
<!-- RafflePress is a self-hosted WordPress plugin. It has NO general REST API. Its programmatic surface is: outbound Webhooks, a Zapier app (REST-hook trigger), 15+ native ESP/CRM integrations, Uncanny Automator, WordPress action/filter hooks, and URL-parameter prefill. Field names and behavior below are reproduced verbatim from the official docs; any JSON example is explicitly marked as CONSTRUCTED from the documented field list (the docs publish no payload example). -->

# RafflePress Developer / Integration Reference

## Nature of the integration surface

RafflePress runs **inside WordPress** (self-hosted, WordPress.org plugin). There is **no hosted REST API** you call to create giveaways or read entrants. Instead, data flows **out** of RafflePress as entrants join:

- **Outbound Webhooks** (Pro) — POST entrant data to your endpoint
- **Zapier** (REST-hook trigger) — "New Contestant Created"
- **15+ native ESP/CRM integrations** — direct list sync
- **Uncanny Automator** — WordPress recipe automation
- **WordPress hooks** (actions/filters) + **URL-parameter prefill** — developer customization

---

## Webhooks

**Enable:** WordPress admin → **RafflePress → Settings → Webhooks**, activate the option.

**Configure a webhook:**
1. Click **"Webhook 1"** to begin setup.
2. **Request URL** — your endpoint where data is POSTed.
3. **Request Format** — **JSON** or **FORM**.
4. **Custom Headers** — add any headers required for delivery (e.g. an auth token).
5. **Add New Webhooks** — create additional webhooks (multiple endpoints supported).

**Trigger:** fires **when a user signs up for a giveaway** (a new entry/signup).

**Fields sent** (for new signup entries):

```
fullname
first_name
last_name
email
giveaway_id
giveaway_name
sign_up_date
```

**CONSTRUCTED example** (built from the documented field list above — the docs publish no payload example; verify the exact envelope against a live delivery, e.g. with webhook.site):

```json
{
  "fullname": "Jane Smith",
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@example.com",
  "giveaway_id": "123",
  "giveaway_name": "Summer Launch Giveaway",
  "sign_up_date": "2026-06-27"
}
```

> **Critical limitation (verbatim):** "User data from giveaway actions that use third-party platforms (eg. Facebook, Twitter, YouTube, Instagram, Pinterest) are **NOT** shared using this feature." So the webhook gives you the **email signup** identity, not per-social-action data.

**Auth / signature:** none documented. There is **no documented HMAC signature** on the webhook — secure the endpoint with a secret Request URL and/or a custom auth header you add in step 4, and dedupe on `email` + `giveaway_id`.

**Payload examples / rate limits:** not documented.

**Troubleshooting (from docs):** verify security policies aren't blocking the call; confirm the request format matches your endpoint; validate required headers are present.

---

## Zapier

**How it works:** connects RafflePress entrants to 500+ Zapier services.

**API key source:** the key comes from a giveaway's **"Join an Email Newsletter" action** — select **Zapier** from that action's integration dropdown and copy the generated **API key**.

**Trigger (sole trigger):** **"New Contestant Created"** — fires whenever someone enters the giveaway; sends "the names and emails of new entrants" plus the full contestant details to the destination.

**Setup steps (verbatim):**
1. Copy the API key from the **Join an Email Newsletter** action dropdown.
2. Log into Zapier and create a new zap with **RafflePress** as the trigger app.
3. Select **"New Contestant Created"** as the trigger.
4. Click **Connect Account** and enter your **website URL** plus **API key**.
5. Choose your giveaway from the dropdown.
6. Select a sample contestant for testing.
7. Specify the destination platform for data delivery.

**Limitation (verbatim):** "Only one **Join an Email Newsletter** action per giveaway when using Zapier."

---

## Native ESP / CRM integrations (direct list sync)

Add a **"Join an Email Newsletter"** entry action and connect one of (15+):

```
Mailchimp, ConvertKit (Kit), AWeber, Drip, ActiveCampaign, Constant Contact,
GetResponse, Campaign Monitor, FluentCRM, iContact, Mad Mimi, MailerLite,
Moosend, Sendy, Brevo
```

Plus **Uncanny Automator** for WordPress-side recipe automation (trigger other plugins/actions when someone enters).

---

## WordPress developer surface

From the RafflePress **Developer** docs category:

- **Access permissions** — change which WordPress user roles/capabilities can access RafflePress (filterable).
- **Prefill giveaway form fields via URL parameters** — pass values in the page URL to pre-populate the entry form (useful for pre-identifying a logged-in user or carrying UTM/identity from a landing page).
- Standard WordPress **actions/filters** apply (it's a WP plugin), so server-side PHP can hook entry events; consult the live developer docs for exact hook names.

> RafflePress is **WordPress-only / self-hosted** — there is no standalone SaaS API or MCP server. All automation runs through the WordPress site (webhooks, Zapier, native integrations, Automator, PHP hooks).

---

## Entry mechanics (relevant to integration logic)

- **30+ bonus entry actions:** email signup, social follows (Instagram, TikTok, Facebook, X/Twitter, Pinterest, LinkedIn, YouTube), referrals, shares, video watches, polls, surveys, comments, image submissions.
- **Viral "Refer a Friend":** +10 entries per referral; social-share actions +2–5 entries.
- **Fraud protection:** built-in (methods not detailed in public docs).
- **Identity:** email is the contestant identity that flows to webhooks/Zapier/ESPs.
