<!-- Source: https://www.feedbear.com/integrations , https://help.feedbear.com/article/30-webhooks , https://help.feedbear.com/article/25-sso , https://www.feedbear.com/pricing (captured 2026-06-29) -->

# FeedBear Integration Reference

## ⚠️ No public REST / pull API

FeedBear does **not** publish a public REST API. You **cannot** `GET` ideas, votes, or comments programmatically. Multiple third-party comparisons explicitly list "no API access" as a FeedBear limitation, and FeedBear's own integrations page documents only webhooks + native connectors. The programmatic surface is:

1. **Outbound webhooks** (event push)
2. **JWT SSO** (authenticate your users into the board)
3. **Zapier** (5,000+ apps; triggers for feedback/ideas/comments)
4. **Native integrations** (Intercom, Slack, Trello, Jira)

All of the above (except viewing) require a **paid plan**: webhooks/integrations/Zapier at **Startup ($49/mo)**, **SSO** at **Business ($99/mo)**, custom integrations at **Enterprise ($299/mo)**.

---

## Webhooks

> Configured in **Project Settings → Webhooks**. Three steps: (1) configure the webhook **URL** that notifications are sent to, (2) **listen** for the JSON payload over HTTPS, (3) **enable** webhooks.

**Documented behavior (verbatim from help center):**
- "You can use Webhooks to integrate your boards with third-party tools (using tools like Make, Syncspider, Pabbly, KonnectzIT) or your own web application."
- "On the URL provided, you will need to process the JSON payload received via HTTPS requests."
- "Each event triggered will have a different payload."

**Documented events / use cases:**
- **New idea submitted** → e.g. create a card in Trello
- **Upvote submitted** → e.g. increment a count in a Google Spreadsheet
- **Comment submitted** → e.g. send a message in a Slack channel

**Security:** No HMAC signature or secret-token scheme is documented (contrast with Frill's HMAC-SHA256-signed webhooks). Protect the endpoint with:
- a **secret, hard-to-guess URL path**
- optional **source-IP allowlisting**
- **payload shape validation** + **idempotency** (dedupe on the idea id)

**HTTP method:** delivered as JSON over HTTPS (treat as `POST`; confirm with a live delivery).

### ⚠️ Payload schema gap

The help article states the per-event payload details are "at the bottom of the page," but that section is **JS-rendered and was not fetchable** during research. Do **not** assume field names. **Capture one live webhook delivery** and lock the schema before coding. A representative (constructed) shape to start from:

```jsonc
// <!-- Constructed from documented concepts — verify against a live delivery -->
{
  "event": "idea.created",          // also: upvote / comment events (exact strings unconfirmed)
  "idea": {
    "id": "idea_123",
    "title": "Dark mode",
    "description": "Please add a dark theme",
    "board": "Feature Requests",
    "status": "open",
    "votes": 1,
    "author": { "name": "Jane", "email": "jane@example.com" },
    "created_at": "2026-06-29T10:00:00Z"
  }
}
```

---

## JWT SSO

> Configured in **Project Settings → SSO**. Lets your website users log in to your FeedBear board with your existing credentials and stay logged in when redirected.

**Flow (verbatim-derived from help center):**
1. **Provide a login URL** — where users are redirected when they click "Login" on the board; your page shows a login form and authenticates the user.
2. **Get the private key** — from **Project Settings → SSO** (core of the secure auth handshake; keep server-side).
3. **Generate a JWT token** — after authenticating the user, build the JWT using the user's **name** and **email**.
4. **Test & enable** — provide your login URL, test the generated JWT, then enable SSO on the project.
5. **Redirect** — send the user to:

```
{{ YOUR_FEEDBEAR_BOARD_URL }}/sso/auth?payload={{ GENERATED_JWT_TOKEN }}
```

FeedBear logs the user in using the data in the JWT.

```python
import jwt  # PyJWT
token = jwt.encode(
    {"name": user["name"], "email": user["email"]},
    PRIVATE_KEY,            # from Project Settings → SSO; server-side only
    algorithm="HS256",      # confirm exact algorithm in-account
)
redirect_url = f"{BOARD_URL}/sso/auth?payload={token}"
```

**Notes:** SSO requires the **Business** plan. Without SSO (or another identification path), board votes/ideas are **anonymous**.

---

## Zapier

Connects FeedBear to **5,000+ apps**. Documented **triggers** cover **feedback / ideas / comments**, with the ability to store data across third-party apps. Use as a no-code bridge or a stand-in for the missing pull API (e.g., new idea → append row to Google Sheets / Airtable). Requires the **Startup** plan. Polling latency applies vs a direct webhook.

---

## Native integrations

| Integration | What it does |
|---|---|
| **Intercom** | Gather feedback inside the Intercom Messenger (widget); (coming) add ideas to boards from Intercom messages. |
| **Slack** | Instant notifications about new feedback and comments. |
| **Trello** | Convert a customer idea into a Trello task (one click) for backlog management. |
| **Jira** | Add a validated idea as a Jira issue after it gathers votes/comments. |
| **Webhooks** | Custom flexibility for Make / Syncspider / Pabbly / KonnectzIT or your own app. |

All native integrations + Zapier + webhooks require **Startup ($49/mo)** or higher.

---

## Gaps

- **No public REST/pull API** — confirmed by FeedBear's integrations page and third-party reviews. No documented base URL, auth scheme, pagination, or rate limits because no query API exists.
- **Webhook payload schema** — undocumented online (JS-rendered). Capture a live delivery.
- **Webhook signing/retry/auto-disable** — no HMAC or retry policy documented. Verify behavior empirically.
- **Exact JWT algorithm/claims** — name + email confirmed as required; algorithm and any extra claims should be verified in-account.
