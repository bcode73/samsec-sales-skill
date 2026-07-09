<!-- Source: https://wordpress.org/plugins/superb-blocks/ , https://superbthemes.com/superb-addons/ , https://superbthemes.com/documentation/ -->

# Superb Addons — Developer & Integration Reference

**There is no public hosted REST API for Superb Addons and no MCP server.** Superb Addons is a WordPress plugin, so the programmatic surface is (1) the form builder's **outbound webhook + native integrations**, (2) the **WordPress core REST API** over the posts/pages that contain Superb block markup, and (3) standard **WordPress hooks/filters**. This file documents that surface and flags what couldn't be confirmed from public docs.

## 1. Form webhook (outbound) — primary automation surface

Configured per form on the Superb Form block (form/integration settings). On submission, the form POSTs the captured fields to a URL you provide.

| Aspect | Detail | Confidence |
|---|---|---|
| Direction | Outbound only (Superb → your URL). No inbound/ingest API. | High |
| Trigger | Form submit | High |
| Method | HTTP POST | High (typical) — confirm in UI |
| Payload | Submission fields (+ form/page metadata) | Schema **not published** |
| Signing | No documented HMAC/signature | Treat as unauthenticated |
| Delivery logs / retries | None documented | Use a gateway/iPaaS if you need them |

**Representative payload (constructed — confirm against a live delivery):**
```json
{
  "form_id": "contact-1",
  "form_title": "Contact",
  "submitted_at": "2026-06-29T12:00:00Z",
  "page_url": "https://example.com/contact/",
  "fields": { "name": "Jane Doe", "email": "jane@example.com", "message": "Hello" }
}
```
<!-- Constructed from docs/UI — Superb does not publish the webhook payload schema. Capture one real delivery (Zapier "Catch Raw Hook", RequestBin, or a logging endpoint) and map field keys before relying on names. -->

**Receiver (defensive — schema may differ):**
```python
from flask import Flask, request
app = Flask(__name__)

@app.post("/superb-hook")
def superb_hook():
    body = request.get_json(force=True, silent=True) or request.form.to_dict()
    fields = body.get("fields", body)        # be defensive: shape isn't documented
    return "", 200
```

**Best practice:** point the webhook at a **Zapier/Make/Pabbly catch hook** or a **webhook gateway (Hookdeck/Svix)** rather than straight at production — you get delivery history, replay, and a stable mapping layer, none of which Superb provides natively.

## 2. Native form integrations (outbound, no code)

Set on the form's integration panel. Use these when the destination is one of the supported services and you don't need custom logic.

| Integration | What it does | Notes |
|---|---|---|
| **Mailchimp** | Add submitter to an audience/list | Newsletter opt-in; map email → audience |
| **Brevo** (Sendinblue) | Add contact to a list | Same pattern as Mailchimp |
| **Google Sheets** | Append submission as a row | Good for lightweight logging |
| **Slack** | Post a message on submission | Internal lead alerts |
| **Webhook** | POST to any URL (see §1) | The escape hatch for everything else |

Integrations behave as **Premium** features — confirm availability on the install.

## 3. Anti-spam (form security config)

UI-configured per form; relevant when submissions are missing or spammy:
- **Honeypot** (silent)
- **hCaptcha**
- **reCAPTCHA v2 / v3**
- **Cloudflare Turnstile**

If legitimate submissions stop arriving at a webhook/ESP, check that a newly-enabled CAPTCHA isn't blocking them, and that the integration is still connected.

## 4. WordPress core REST API (read/write Superb-built content)

Superb has no content API of its own; its blocks are stored as namespaced block markup in `post_content`, reachable through standard WordPress endpoints.

```bash
# Application Password auth (wp-admin → Users → Profile → Application Passwords)
curl -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" \
  "https://example.com/wp-json/wp/v2/pages?per_page=100&context=edit&_fields=id,slug,content"
```
- `context=edit` returns `content.raw` containing `<!-- wp:superb/... -->` block comments (confirm the exact namespace prefix in-account).
- Pagination: `page` / `per_page`, total pages in the `X-WP-TotalPages` header.
- Writing back: `POST/PUT /wp-json/wp/v2/pages/{id}` with serialized block markup — easy to corrupt; prefer editing in the block editor.

## 5. WordPress hooks/filters (developer extension)

As a standard plugin, Superb runs inside WordPress, so a developer can attach to core hooks (`render_block`, `block_categories_all`, etc.) from a child theme or companion plugin to mutate output or restrict blocks. **Superb-specific public action/filter names were not found in public docs** — confirm any branded hooks against the plugin source before relying on them.

## 6. Built-in Troubleshooter (support tooling)

Not an API, but the supported diagnostic path: **wp-admin → Superb Addons → Get Help → Start Troubleshoot Process**. It isolates plugin/theme conflicts (the typical cause of Theme Designer not loading). Use it before manual plugin-bisection.

## Gaps (could not confirm from public sources)

- **Webhook payload schema** — not published. Capture a live delivery to map fields.
- **Webhook method/headers/signing** — assumed POST, no HMAC; verify in the form UI.
- **Exact block namespace prefix** (`superb/`?) and attribute keys — confirm from a live block export; do not hard-code.
- **Branded WordPress action/filter hook names** — not documented publicly; read the plugin source.
- **Whether each integration is Free or Premium** on a given install — gating is ambiguous between the WordPress.org readme and the marketing pricing page; verify in-plugin.
