# Superb Addons Platform Reference

## Overview

Superb Addons (WordPress.org slug `superb-blocks`) is a Gutenberg-native block-addon plugin by **SuperbThemes / Suplugins** that turns the native WordPress block editor into a website builder — blocks, design patterns, pre-built pages, a form builder, popups, animations, and a Theme Designer, without a separate page-builder canvas. It **extends** the block editor rather than replacing it (the contrast with Elementor/Divi). ~80,000+ active installs, freemium. The backlog/marketing domain `superbaddons.com` does not resolve as of research; the live product lives at `superbthemes.com/superb-addons/` and `wordpress.org/plugins/superb-blocks/`.

## Capabilities & automation surface

For each module: what it does, then how (if at all) it's automatable.

- **20 blocks** — Superb Form, Popup, Carousel Slider (+ Carousel Slide), Countdown, Progress Bar, Google Maps, Rating, Add to Cart, About the Author, Table of Contents, Recent Posts, Animated Heading, Toggle, Reveal Button(s), Cover Image, Multi-Step Form (+ Form Step, Form Field). **UI-only to build**; the resulting markup is **readable via the WordPress core REST API** (namespaced block markup in `post_content`).
- **Form builder** — contact / newsletter / feedback / support / RSVP / booking / quote / multi-step forms; field types include email, textarea, number, calculated, slider, dropdown, radio, checkbox, rating, file upload, date/time/color pickers, signature, phone, URL. Conditional logic, submission storage, admin + user email notifications, post-submit redirect, role-based access, GDPR auto-deletion. **Outbound automation: webhook-accessible** (+ native Mailchimp/Brevo/Google Sheets/Slack). **No inbound API.**
- **Anti-spam** — honeypot, hCaptcha, reCAPTCHA v2/v3, Cloudflare Turnstile. **UI-config.**
- **Popups & modals** — newsletter/offer/announcement popups with smart triggers. **UI-only.**
- **200+ patterns, 50+ pre-built pages, 20+ header/footer templates** — design library inserted into posts/pages. **UI-only.**
- **Theme Designer** — customize theme-wide elements/layouts (100+ layouts). **UI-only.** (Most-reported failure point — see Troubleshooting in SKILL.md.)
- **70+ animations** — scroll/hover/typing/counting/click triggers on any block. **UI-only.**
- **Responsive visibility + design controls** — show/hide per device; per-device padding/margin/font/alignment/flex/order. **UI-only.**
- **Dynamic content / conditional display** — including ACF support for dynamic content. **UI-config.**

> There is **no public hosted REST API** for Superb Addons and **no MCP server**. The programmatic surface is: (1) the form's **webhook + native integrations** (outbound), (2) the **WordPress core REST API** for reading/writing the underlying posts/pages, and (3) standard **WordPress hooks/filters** a developer can attach in a child theme/plugin. See `references/superb-addons-api-reference.md`.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify current pricing on superbthemes.com.*

| Plan | Price (best-effort) | Notes |
|---|---|---|
| Free | $0 | WordPress.org. Core blocks + library. The readme markets a free form builder. |
| Premium — yearly | $29 (1 site) / $39 (3) / $49 (50) | Intro discounts shown on site. |
| Premium — lifetime | $59 (1 site) / $79 (3) / $99 (50) | One-time. |
| SuperbThemes Premium | bundle | All SuperbThemes themes + plugins (yearly/lifetime). |

**Premium-gated (per the pricing page — note the conflict with the free-form-builder readme):** Forms & multi-step forms, Popups with smart triggers, 70+ animation effects, sliders/carousels, Theme Designer (100+ layouts), visibility conditions, advanced custom CSS, responsive controls, extended social icons, premium blocks.

**Plan-gating ambiguity is the #1 gotcha:** the WordPress.org readme says forms/popups/animations are free; the marketing page lists them as Premium. The likely reality is a basic free tier with advanced capabilities (multi-step, integrations, smart triggers, full animation set, Theme Designer layouts) gated to Premium. **Verify on the live install** before promising a feature.

No API rate limits apply (no hosted API). Form throughput is bounded by the host/WordPress, not a vendor quota.

## Integrations

Direction of data flow matters more than logos.

- **Form → external (outbound):**
  - **Webhook** — POSTs a form submission to a URL you control (or a Zapier/Make/Pabbly "Catch Hook"). The reliable, tool-agnostic path to any CRM/endpoint.
  - **Mailchimp / Brevo** — push subscribers to a list/audience (newsletter opt-in). Native, no middleware.
  - **Google Sheets** — append each submission as a row.
  - **Slack** — post a message on submission.
- **Content read/write:** **WordPress core REST API** (`/wp-json/wp/v2/posts|pages`) with application-password auth — Superb blocks are namespaced block markup inside `post_content`.
- **iPaaS:** the webhook makes Zapier/Make/Pabbly/Integrately reachable as catch-hook targets; there are no first-party Zapier triggers/actions for Superb itself (it isn't a hosted app).
- **No native CRM connector, no inbound API, no MCP.**

## Data model

Superb Addons does not expose object IDs through a hosted API. Two shapes matter:

**1. A Superb block as stored in `post_content` (read via WordPress core REST API).** Block names are namespaced (e.g. a form block serializes as Gutenberg block-comment markup). Confirm the exact namespace prefix in-account before parsing.

```html
<!-- wp:superb/form {"formId":"contact-1"} -->
  <!-- wp:superb/form-field {"type":"email","name":"email","required":true} /-->
  <!-- wp:superb/form-field {"type":"text","name":"name"} /-->
<!-- /wp:superb/form -->
```
<!-- Constructed from docs/UI — verify the exact block namespace and attribute keys against a live export. -->

**2. A form submission as delivered to a webhook (representative — the exact schema is not published; capture one live delivery to confirm keys).**

```json
{
  "form_id": "contact-1",
  "form_title": "Contact",
  "submitted_at": "2026-06-29T12:00:00Z",
  "page_url": "https://example.com/contact/",
  "fields": {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "message": "Hello"
  }
}
```
<!-- Constructed representative payload — Superb does not publish the webhook schema. Capture a real delivery (Zapier Catch Raw Hook / RequestBin) and map field keys before relying on names. -->

## Quick-start recipes

### Recipe 1 — Capture a Superb form submission and forward to your CRM (webhook)
**Trigger:** form submitted on the page.
**Steps:** On the Superb Form block, open the **Webhook** integration → add your endpoint URL → save. Stand up a tiny receiver, capture one real submission to learn the field keys, then map into your CRM.

```python
# Minimal Flask receiver — capture the real payload shape first, then map.
from flask import Flask, request
app = Flask(__name__)

@app.post("/superb-hook")
def superb_hook():
    payload = request.get_json(force=True, silent=True) or request.form.to_dict()
    fields = payload.get("fields", payload)          # schema not published — be defensive
    email = fields.get("email")
    name = fields.get("name")
    # push to your CRM here (e.g. requests.post(CRM_URL, json={...}))
    print("Superb submission:", name, email)
    return "", 200
```

```bash
# Simulate a delivery while wiring the mapping (replace with your real captured body):
curl -X POST https://your-app.example.com/superb-hook \
  -H 'Content-Type: application/json' \
  -d '{"form_id":"contact-1","fields":{"name":"Jane","email":"jane@example.com","message":"hi"}}'
```
**Gotchas:** The payload schema isn't documented — never hard-code field names without capturing a live delivery. Superb webhooks aren't documented as HMAC-signed; treat the endpoint as unauthenticated and validate/whitelist server-side. For zero-code, point the webhook at a Zapier/Make Catch Hook instead.

### Recipe 2 — Read pages built with Superb blocks via the WordPress REST API
**Trigger:** you need to export or audit Superb-built content programmatically.
```bash
# Application Password auth (Users → Profile → Application Passwords)
curl -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" \
  "https://example.com/wp-json/wp/v2/pages?per_page=100&context=edit&_fields=id,slug,content"
```
```python
import requests
auth = ("admin", "xxxx xxxx xxxx xxxx xxxx xxxx")
r = requests.get("https://example.com/wp-json/wp/v2/pages",
                 params={"per_page": 100, "context": "edit", "_fields": "id,slug,content"},
                 auth=auth)
for page in r.json():
    html = page["content"]["raw"]        # contains <!-- wp:superb/... --> markup
    # parse block comments to find Superb blocks
```
**Gotchas:** Use `context=edit` to get `content.raw` (the block markup). Pagination via `page`/`per_page` and the `X-WP-TotalPages` header. There is no Superb-specific endpoint — you're reading core WordPress content.

### Recipe 3 — Newsletter opt-in straight into Mailchimp/Brevo (no middleware)
**Trigger:** newsletter signup form submit.
**Steps:** Build a Superb newsletter form (use a pre-built newsletter pattern), enable anti-spam (honeypot + Turnstile/reCAPTCHA), open the form's **Mailchimp** (or **Brevo**) integration, connect the account, and map email → audience/list. No code, no Zapier. Use this instead of a webhook when the only destination is your ESP.
**Gotchas:** Integrations and multi-step forms behave as Premium — confirm they're available on the install. Always pair an ESP integration with an admin email notification as a backup in case a sync silently fails.

## Integration patterns

- **CRM sync:** form → webhook → your endpoint/iPaaS → CRM upsert keyed on email. Because there's no inbound API, treat the form submission as the source event; dedupe by email + submission timestamp. Keep submission storage on in wp-admin as the system of record.
- **Reliability:** no delivery logs or retry dashboard are documented for the webhook. For anything revenue-critical, send to a webhook gateway (Hookdeck/Svix) or a Zapier/Make catch hook that gives you a delivery history and replay, rather than POSTing straight to production.
- **Content pipeline:** read/write Superb-built pages through the WordPress core REST API (application passwords); parse the `superb/`-namespaced block comments out of `content.raw`. There's no structured field API — the block attributes live in the JSON inside each block comment.
- **Conflict isolation:** when the editor or Theme Designer breaks, the fastest diagnosis is the built-in Troubleshooter plus deactivating other block plugins (a documented Gutenverse interaction exists). Always do this on staging before touching a live site.
