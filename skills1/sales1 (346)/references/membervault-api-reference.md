<!-- Source: https://zapier.com/apps/membervault/integrations -->
<!-- Source: https://courses.vipmembervault.com/how-to-setup-webhooks -->
<!-- Source: https://integrately.com/integrations/membervault/webhook-api -->
<!-- Source: https://membervault.co (pricing/features) -->

# MemberVault Integration & API Reference

> **There is no documented public REST API for MemberVault.** MemberVault is a no-code creator platform; the supported programmatic surface is **Zapier** (triggers + actions) and **inbound/outbound webhooks**. Everything below was captured from the Zapier app listing and MemberVault's own webhook tutorial. Where exact payload fields or auth weren't documented, that is flagged — nothing is invented.

## Integration surface at a glance

| Mechanism | Direction | Use it for |
|---|---|---|
| **Inbound webhook** ("API URL") | external → MemberVault | Grant/revoke product access when a purchase happens on an external cart/ESP |
| **Outbound webhook** ("Call a web hook" product action) | MemberVault → external | Push a contact to an unsupported ESP / fire on purchase, lesson completion, quiz answer |
| **Zapier** | both | 7 triggers + 2 actions, connect to 30+ apps without code |
| **Native ESP integrations** | both | Kit (ConvertKit), MailerLite, ActiveCampaign, etc. |

No public REST API. No MCP server.

## Inbound webhook (grant access from an external purchase)

The single most important integration for developers: when someone buys on an external cart (Gumroad, SamCart, ThriveCart, a custom Stripe checkout, or via an ESP automation), POST to MemberVault's inbound webhook URL to grant that email access to a product.

**Where to get the URL:** in MemberVault, **Integrations → Advanced**, select your email service (ActiveCampaign, Zapier, ConvertKit/Kit, etc.) and copy the provided **API URL**.

**URL shape (from the tutorial):** the URL embeds your custom MemberVault domain, an `API` designation, and a **course/product ID** parameter (the docs give the example "Course ID equals 100").

```
https://<your-subdomain>.vipmembervault.com/...api...?course_id=100&email=...
```

> ⚠️ The exact query/body parameter names and the auth mechanism are **not fully documented** in public sources. Confirm the precise URL and parameters by copying it from your own **Integrations → Advanced** screen. Transport is **HTTPS** (required). Webhook activity is logged with an identifier (e.g. `webhook-AC`).

**Typical fields to send:** subscriber `email` (key identity), the target product/`course_id`, and optionally first/last name.

## Outbound webhook (notify an external system)

Configured per product under the product's **Actions** section → **"Call a web hook."** Fires on a trigger (e.g. purchase, lesson completion, quiz answer) and POSTs contact data out.

**Documented payload data:** `email address`, `first name`, `last name`.

> The full JSON envelope/field keys aren't published — capture one delivery against a request-bin (e.g. webhook.site) to confirm exact keys before parsing.

## Zapier triggers (events MemberVault emits)

1. **Completed Lesson** — "Triggers when a user completes a selected lesson in your account"
2. **Completed Module** — "Triggers when a user completes a selected module in your account"
3. **Earned X EP** — "Triggers when a user reaches the configured EP number" (EP = Engagement Points)
4. **Hot Lead** — "Triggers when a user becomes a Hot Lead"
5. **User Completes an Action** — "Triggers when a user completes an action in your account"
6. **User Added to a Product** — "Triggers when a user signs up for a specified product" *(note: manual user additions won't activate the Zap)*
7. **User Email Consent** — "Triggers when a user approves or denies email consent"

## Zapier actions (writes into MemberVault)

1. **Add User to Product** — "This action will add a user to a product and create a login for them automatically if they don't already have one"
2. **Remove User From Product** — "Removes selected user from a product"

## cURL example (inbound webhook, representative)

Confirm the exact URL/params from Integrations → Advanced; this is the documented shape, not a guaranteed contract:

```bash
curl -X POST "https://YOURSUB.vipmembervault.com/api/webhook?course_id=100" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "email=jane@example.com" \
  --data-urlencode "first_name=Jane" \
  --data-urlencode "last_name=Doe"
```

## Auth, pagination, rate limits

- **Auth:** the inbound URL itself is the credential (it embeds account-specific routing). Treat it as a secret. No documented API key/Bearer scheme.
- **Pagination:** N/A — there is no list/read API. Reading member or engagement data programmatically is not supported beyond Zapier triggers; for bulk data, use the in-app CSV export.
- **Rate limits:** none documented. Don't hammer the inbound webhook; batch external events.

## Data model (representative — confirm in-app)

```json
// Member / user (as surfaced via outbound webhook / Zapier)
{
  "email": "jane@example.com",   // primary identity across products
  "first_name": "Jane",
  "last_name": "Doe",
  "ep": 120,                      // Engagement Points (gamification)
  "lead_status": "hot"           // warm | hot — set automatically by sales-info views
}
```

```json
// Product (course / membership / download / portal / challenge / summit)
{
  "course_id": 100,              // referenced by the inbound webhook
  "name": "Signature Course",
  "type": "course"
}
```

## Notes that matter for integrations

- **Identity is email.** A member is one login per account; products are granted to that email. Match/dedupe on `email`.
- **MemberVault does not send marketing email.** Wire an ESP (Kit/MailerLite/ActiveCampaign natively, others via Zapier/webhooks) — every "send them a sequence" flow lives in the ESP, not MemberVault.
- **"Hot Lead" is the differentiator.** MemberVault tags users who repeatedly view the sales info of products they don't own. The `Hot Lead` Zapier trigger is how you route those warm leads into an outreach/nurture flow automatically.
- **Free plan caps members at 100** — a Zap that auto-adds users can silently hit that ceiling.
