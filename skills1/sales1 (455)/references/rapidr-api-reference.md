<!-- Source: https://rapidr.io , https://rapidr.io/pricing/ , https://rapidr.io/features/ , https://rapidr.io/integrations/ , https://rapidr.io/integrations/zapier , https://help.rapidr.io/article/33-what-is-single-sign-on-sso-and-how-to-implement-it , https://help.rapidr.io/article/41-slack-integration , https://rapidr.io/docs/sso/ (JS-rendered) , G2 review snippets (captured 2026-06-29) -->

# Rapidr Integration Reference

## ⚠️ No public REST / pull API

Rapidr does **not** publish a public REST API. You **cannot** `GET` ideas, votes, comments, or boards programmatically. A G2 reviewer states plainly that "Rapidr does not offer an API," and Rapidr's own docs only cover SSO, native connectors, and Zapier. The programmatic surface is:

1. **JWT SSO** — identify your users into the portal (server-side token mint)
2. **Zapier** — realtime triggers + create/update-record actions (5,000+ apps); the no-code stand-in for the missing pull API
3. **Native connectors** — Slack (two-way), Intercom, Jira (two-way), HubSpot
4. **Embeddable widget** — front-end feedback + changelog widgets, custom-domain portal
5. **Voter CSV export** — manual one-off read of voters per idea

There is **no base URL**, no auth token for data access, and no rate limit to honor — because there is no data API. Do **not** attempt `curl https://api.rapidr.io/...`; no such endpoint is documented.

---

## JWT SSO

> The primary developer integration. Configured in **Company Settings → SSO**. Lets your authenticated website users log in to the Rapidr portal seamlessly and attaches their votes/posts to a real identity (otherwise activity is anonymous).

**Flow (from the Rapidr SSO help docs):**
1. **Generate a Secret Key** for your Rapidr account in **Company Settings → SSO** (keep it server-side).
2. **Create a login redirect page** on your site that authenticates the user, then add that **Redirect URL** in SSO settings.
3. **Generate an SSO token (JWT)** on your server from the logged-in user (name + email).
4. **Redirect** the user to Rapidr's **Single Sign-On endpoint** with the valid token; a `redirect` query parameter tells Rapidr where to send the user after login.
5. **Test** the issued JWT with Rapidr's **debugger tool** (confirms Rapidr can decode it), then **enable SSO** in company settings. Enabling SSO **disables all other authentication mechanisms.**
6. Link to the portal from your app by pointing to the SSO endpoint with the user's valid token.

```python
# <!-- Constructed from the documented flow — exact claim keys, endpoint path, and signing algorithm are JS-rendered (rapidr.io/docs/sso/); verify in-account -->
import jwt  # PyJWT
from urllib.parse import quote

SECRET_KEY = "…"  # Company Settings → SSO; server-side only

def sso_url(user, return_to):
    token = jwt.encode(
        {"name": user["name"], "email": user["email"]},  # confirm exact claims in-account
        SECRET_KEY,
        algorithm="HS256",                                # confirm algorithm in-account
    )
    # Confirm the exact SSO endpoint path in your account's SSO settings:
    return f"https://<your-portal-domain>/sso?token={token}&redirect={quote(return_to)}"
```

**Plan gate:** SSO (both **SAML** and **JWT**) requires the **Business** plan ($199/mo). On Startup, identification is email-only.

---

## Zapier

> Rapidr advertises "**Realtime triggers** for events happening on Rapidr" plus actions to "create a new record or update an existing record in your app," across 5,000+ apps. This is the closest thing to an API for moving data **out** of Rapidr.

**Documented capability (verbatim-derived):**
- **Triggers:** realtime events on Rapidr start a Zap (e.g. new feedback / comment / vote — **exact trigger names are NOT published**; confirm in the live Zap editor).
- **Actions:** create or update a record in a connected app.

**⚠️ Trigger/action name gap:** Rapidr's Zapier page describes triggers/actions generically without naming them. **Do not hard-code a trigger name.** Open the Zap editor, connect Rapidr, and read the available triggers/actions live before building.

**Pattern for "no API" export:** Rapidr trigger → **Webhooks by Zapier (POST)** action → your endpoint. You receive Rapidr's event data as the Zap payload (not a Rapidr API response). Dedupe on the idea id since you can't re-read from Rapidr.

---

## Native connectors

| Connector | Direction | Behavior |
|---|---|---|
| **Slack** | bidirectional | `/rapidr` slash command opens a modal to log feedback from anywhere in Slack; Rapidr posts new-feedback/comment/vote notifications to a chosen channel. Install via **Integrations → Slack → Install Slack app** (OAuth, pick channel). Filter per channel by **board** and **event type**; authorize multiple channels. |
| **Intercom** | inbound | Track feedback & votes from Inbox and Messenger. |
| **Jira** | bidirectional | Sync feedback & status with Jira issues. Also listed on the **Atlassian Marketplace**. |
| **HubSpot** | inbound | Track feedback on behalf of contacts and deals. |
| *Coming soon* | — | **Zendesk** (tickets), **Salesforce**, **GitHub** (sync feedback & status), **Segment** (track feedback + sync status). |

**Plan gate:** basic integrations (Slack/Intercom/Jira/HubSpot/Zapier) are on **Startup**; "advanced integrations" unlock on **Business**.

---

## Embeddable widget & portal

- In-app **feedback widget** (embed boards) and **changelog widget** (surface release notes), plus a full portal hostable on a **custom domain** (Startup+) with custom branding.
- The embed is **front-end**; pair it with **JWT SSO** to attribute widget activity to real users.
- The exact embed snippet/data-attributes are configured in-account (not exposed verbatim in the public help center).

---

## Voter CSV export

- Each idea's voter list can be **exported to CSV** (name + email) from the Rapidr UI — a manual read path for outreach or reconciliation when you can't pull via an API.

---

## Pricing (best-effort, confirm in-account)

| Plan | Price | Integration-relevant inclusions |
|---|---|---|
| Startup | $49/mo | basic integrations (Slack/Intercom/Jira/HubSpot/Zapier), private boards, custom domain, widgets, roadmap, changelog. **No SSO/segmentation.** |
| Business | $199/mo | + SAML & JWT SSO, user segmentation, advanced integrations, remove branding |
| Enterprise | custom | + white-label, 99.9% SLA, invoice/PO |

No free tier; 14-day trial (no card).

---

## Gaps

These details were **not** fetchable (JS-rendered) or are **not published** and must be confirmed live/in-account before relying on them:

- **JWT SSO claim names + signing algorithm** — `rapidr.io/docs/sso/` is JS-rendered (returns only a header server-side). The flow is confirmed; exact claim keys, the SSO endpoint path, and the algorithm are not.
- **Zapier trigger/action names** — advertised as "realtime triggers" + create/update actions but not enumerated. Read them in the live Zap editor.
- **Webhook payloads** — no standalone outbound webhook product is documented (unlike FeedBear/Frill); event data flows through Zapier/native connectors, whose payload shapes must be confirmed in the Zap preview or connector.
- **Data object schemas** — no API/schema is published; the JSON shapes in `platform-guide.md` are constructed from terminology and must be verified against a live Zapier payload or CSV export.
