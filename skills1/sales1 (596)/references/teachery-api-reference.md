<!-- Source: https://help.teachery.co/en/articles/137-integration-with-zapier -->
<!-- Source: https://zapier.com/apps/teachery/integrations -->
<!-- Captured 2026-06-27. Teachery exposes NO public REST API. The "API key" is a Zapier (and Make/Pabbly)
     connection credential, not a documented REST endpoint. Trigger/action names are copied from the Zapier
     app + Teachery help center. JSON payloads are CONSTRUCTED from the documented fields and marked. -->

# Teachery API / Integration Reference

**Teachery has no public REST API.** There are no documented HTTP endpoints, no base URL, and no developer
API docs. The only programmatic surface is **iPaaS** — Teachery connects to **Zapier**, **Make**, and
**Pabbly** using an **API key** found at **Account → Integrations**. That key authenticates the Zapier
connection (you paste it once); it does **not** authorize direct REST calls. Plan around triggers and
actions (and **Webhooks/Code by Zapier** for anything the native connector can't reach).

## Authentication (for Zapier/Make/Pabbly)

- **Credential:** your Teachery **API key**, from **Account → Integrations**.
- **Setup:** paste the key into Zapier once when you connect the Teachery app — watch for trailing spaces
  on copy/paste. The account then stays linked.
- There is no public auth scheme for direct API calls because there is no public API.

## Zapier surface

Teachery is **both a trigger app and an action app**.

### Triggers (3)
| Trigger | Fires when… | Notes |
|---|---|---|
| **Completed Course** | a student completes a course | course-completion automations |
| **New Lead** | a new email lead is created (Landing Page opt-in) | export leads to an ESP |
| **New Order** | a new order is created | optional Course/Theme Name filter input |

### Actions (4)
| Action | Does… | Required fields |
|---|---|---|
| **Add User to Course** | enrolls a user in a course (grants access) | Course, Email, First Name |
| **Add User to Theme** | enrolls a user in a Theme / Course Hub (membership) | Theme, Email, First Name |
| **Revoke Course Access From User** | removes a user's course enrollment | Course, Email |
| **Revoke Theme Access From User** | removes a user's Theme/Hub enrollment | Theme, Email |

> "Theme" is Teachery's term for a **Course Hub** (a membership grouping of courses). Enroll/revoke comes
> in both a per-Course and a per-Theme flavor.

Make and Pabbly expose the same operations as cheaper Zapier alternatives. For systems none of them reach
natively, chain **Webhooks by Zapier** (Custom Request) off a Teachery trigger.

## Identity & common patterns

- **Identity is email.** Add User to Course creates/locates the student by email; match and dedupe on
  email everywhere.
- **Grant access on external purchase:** trigger on the cart/processor (PayPal, Shopify, Gumroad, Stripe
  via the cart) → **Add User to Course** (or **Add User to Theme** for a membership).
- **Run dunning/win-back:** there is no native cancellation trigger; cancellation handling lives in your
  payment processor — trigger on the processor's "subscription canceled," then **Revoke Course/Theme
  Access From User** in Teachery and add the student to a win-back sequence in your ESP.
- **Export leads:** **New Lead** → create/update subscriber in your ESP (Teachery's built-in email is only
  welcome/completion/lesson-unlock).

## Constructed example payloads

<!-- Constructed from documented Zapier fields — verify against a live Zap before relying on shapes -->

**New Order trigger (outbound to your Zap):**
```json
{
  "event": "new_order",
  "email": "buyer@example.com",
  "first_name": "Sam",
  "course_name": "Launch Your Brand",
  "amount": 149.00,
  "currency": "USD",
  "created_at": "2026-06-27T10:00:00Z"
}
```

**Add User to Course action (inbound from your Zap):**
```json
{
  "course": "Launch Your Brand",
  "email": "buyer@example.com",
  "first_name": "Sam"
}
```

**Completed Course trigger:**
```json
{ "event": "completed_course", "email": "buyer@example.com", "course_name": "Launch Your Brand", "completed_at": "2026-06-27T12:00:00Z" }
```

## Gaps / not available

- **No public REST API** — no endpoints, base URL, pagination, or rate-limit docs exist. For bulk reads,
  use the in-app **customer analytics / CSV export** rather than expecting an API.
- **No native webhooks** outside the Zapier event surface (use Webhooks by Zapier to bridge).
- **No video/file hosting** — content is embedded from YouTube/Vimeo/Google Drive; the API/Zapier surface
  does not manage media.
- **No MCP server.**
- The built-in **course affiliate** feature (creator adds affiliates → unique Payment Page links, 30-day
  last-click cookie, recurring commissions on recurring pages) is **UI-only** — no affiliate API/Zapier
  trigger; pull affiliate-attributed sales from the dashboard/export.
