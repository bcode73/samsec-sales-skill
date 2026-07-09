<!-- Source: https://referlist.co/ , https://www.producthunt.com/p/referlist/referlist , https://www.npmjs.com/package/referlist , https://docs.referlist.co/ (docs site is JS-rendered; fetched 2026-06) -->

# Referlist Platform Reference

## Overview

Referlist (referlist.co) is a **no-code pre-launch waitlist with gamified, Dropbox/Robinhood-style referrals**: a visitor joins, sees their place in line, gets a unique referral link, and moves up the queue each time someone joins through it. It's pitched as the affordable, landing-page-agnostic alternative to heavier viral-marketing suites (Viral Loops is the named comparison) — built so you bring your own landing page and just bolt on the referral waitlist. Audience: YC/Techstars/early-stage startups and indie makers. Claimed effect: ~30% more signups via gamified referrals.

> **Research caveat.** The marketing site renders enough to extract features and pricing, but **docs.referlist.co is a JS-rendered SPA** and the public SDK GitHub repo (`parthibanloganathan/referlist-sdk`) is client-side only and last updated in 2022. So the **client-side SDK is well-documented**, but the **REST API's base URL, auth, and exact paths could not be captured** — they're flagged under `## Gaps` in the api-reference, not invented. Verify them in the signed-in docs before building.

## The 5 ways to install (verified)

| # | Method | Surface | Best for |
|---|---|---|---|
| 1 | Copy-paste **embedded signup form** | UI / embed | Pure no-code sites |
| 2 | **npm SDK** (`referlist`) for React/Next.js | Client JS | React/Next.js apps |
| 3 | **JS snippet** + element IDs `referlistemail` / `referlistbutton` | Client JS | Any HTML site / no-code builder |
| 4 | JS snippet + **manual call** `window.referlist.addToWaitlist(domain, email, referralCode)` | Client JS | Custom forms / custom flows |
| 5 | **REST API** (Pro+) | Server API | Backends, server-side adds, scheduled sync |

## Capabilities & automation surface

| Capability | What it does | Automation surface | Confidence |
|---|---|---|---|
| Gamified referral waitlist | Position in line, unique referral link, queue jumping on referred joins | UI + SDK | Verified |
| No-code embed | Embedded form / JS snippet on Webflow, Squarespace, Wix, any HTML | UI / client JS | Verified |
| npm SDK | `referlist.initialize({ domain })`, auto-binds to `referlistemail`/`referlistbutton`, `addToWaitlist(...)` | Client JS | Verified (npm v1.0.9) |
| REST API | Add signup, look up an email's place in line, list all signups, attach referral code | **API-accessible (Pro+)** | Verified it exists; specifics → Gaps |
| Export | CSV, Mailchimp, Airtable | UI export | Verified |
| Waitlist seeding | Pre-fill signups so a new list isn't empty | UI (Pro+) | Verified |
| Branded email domain | Send confirmation emails from your domain | UI (Pro+) | Verified |
| Multi-language | Localized waitlist UI | UI (Pro+) | Verified |
| Page customization | Messaging, colors; remove watermark | UI (Growth+) | Verified |
| Webhooks / Zapier | Real-time push to external systems | — | *(unconfirmed — not found in docs; assume absent until verified)* |
| MCP server | — | — | None found |

## Pricing, limits & plan gates

> Best-effort (2026-06) — verify on the live pricing page. An older Product Hunt listing cited a flat "$50/mo unlimited" that no longer matches the tiers below.

| Plan | Price | Signups | Key gates |
|---|---|---|---|
| Free | $0 | 100 | Basic; Referlist watermark; export capped at 100 |
| Growth | $29/mo | 500 | Customization, **no watermark** |
| Pro | $59/mo | 3,000 | **REST API**, branded email-sending domain, waitlist seeding, multi-language |
| Enterprise | Contact | Unlimited | Usage-based ~**$0.01/signup/mo**, priority support |

**Integration impact:** the REST API is the Pro gate that matters most for developers — there is **no server-side API on Free/Growth**. Below Pro you automate via the client-side SDK plus CSV/Mailchimp/Airtable export.

## Integrations

Data flow is mostly **egress** (Referlist → elsewhere):

- **Export connectors:** CSV, **Mailchimp**, **Airtable** (UI-triggered).
- **REST API (Pro+):** read the waitlist / a single email's position; add signups (incl. referral code) — the only programmatic *read/write* path. Direction: bidirectional but Pro-gated.
- **No-code site builders:** Webflow, Squarespace, Wix (embed/snippet).
- **Frameworks:** React / Next.js via the npm SDK.
- **No confirmed Zapier/Make/webhooks.** If you need push or 1000s-of-apps routing, confirm first or pair with a tool that documents it.

## Data model

> ⚠️ The REST API's response shapes are **not in the public docs index**. The JSON below is **representative**, constructed from the documented capabilities ("add signups, query info on a particular email, list all emails… place in line… referral code"). **Verify field names against the live docs / a real response before mapping.**

```json
<!-- Constructed/representative — NOT copied from Referlist docs. Verify against the live API. -->
{
  "email": "founder@example.com",
  "domain": "my-startup",
  "position": 42,
  "referral_code": "a1b2c3",
  "referral_link": "https://my-startup.com/?ref=a1b2c3",
  "referrals": 3,
  "joined_at": "2026-06-19T12:00:00Z"
}
```

Handling, regardless of exact shape: dedupe on `email` (+ `domain`); treat `position`/`referrals` as server-owned (don't compute locally); guard `referral_code`/`referral_link` for direct signups.

## Quick-start recipes

### Recipe 1 — Next.js SDK install with the SSR fix (the #1 gotcha)
```jsx
// The SDK touches `window`, so it must load client-side only.
import dynamic from "next/dynamic";
import { useEffect } from "react";

// Option A: dynamic import with ssr disabled
const useReferlist = () => {
  useEffect(() => {
    let mounted = true;
    import("referlist").then((referlist) => {
      if (mounted) referlist.initialize({ domain: "YOUR_DOMAIN" });
    });
    return () => { mounted = false; };
  }, []);
};

export default function WaitlistForm() {
  useReferlist();
  return (
    <form>
      <input id="referlistemail" type="email" placeholder="you@example.com" />
      <button id="referlistbutton" type="button">Join the waitlist</button>
    </form>
  );
}
```
**Gotchas:** never import `referlist` at module top level in a server component; the element IDs `referlistemail` / `referlistbutton` are what the SDK binds to.

### Recipe 2 — Custom form: manual add with referral attribution
```html
<!-- Capture the inbound ?ref code and forward it, or the referrer never moves up. -->
<input id="email" type="email" />
<button onclick="join()">Join</button>
<script src="https://referlist.co/referlist.js"></script> <!-- verify exact snippet URL in your dashboard -->
<script>
  function getRef() {
    return new URLSearchParams(window.location.search).get("ref") || "";
  }
  function join() {
    const email = document.getElementById("email").value;
    // 3rd arg = referral code of whoever referred this visitor
    window.referlist.addToWaitlist("YOUR_DOMAIN", email, getRef());
  }
</script>
```
**Gotchas:** omitting the 3rd arg records the signup but credits no referrer; `addToWaitlist` runs in the browser (it's not a server endpoint).

### Recipe 3 — Pull the waitlist into Mailchimp (Pro)
1. One-shot / manual: **Export → Mailchimp** (or CSV/Airtable) from the dashboard.
2. Ongoing: on **Pro**, use the REST API to **list signups** on a schedule and upsert into Mailchimp (verify the base URL + auth header in the live docs first — see api-reference `## Gaps`).
3. Send the actual launch broadcast from Mailchimp, not Referlist — hand off to `/sales-email-marketing`.

```bash
# Placeholder — confirm the real base URL, path, and auth in docs.referlist.co before running.
# curl -H "Authorization: Bearer $REFERLIST_API_KEY" \
#   "https://<VERIFY-BASE-URL>/waitlist?domain=YOUR_DOMAIN"
```

## Integration patterns

- **Client-side first:** for most installs the integration is the SDK/snippet binding to your form — no server needed. Keep the referral-code capture (`?ref`) in your page logic.
- **Pro API sync:** treat Referlist as source-of-truth for position/referrals; pull on a schedule (no confirmed webhooks) and upsert into your ESP/CRM, deduping on email.
- **No push/webhook assumption:** design for polling + export, not real-time callbacks, unless you confirm webhooks exist in the live docs.

## Fit vs. other indie waitlist tools

| Need | Better fit |
|---|---|
| Cheap, landing-page-agnostic viral referral waitlist with an npm SDK | **Referlist** |
| Built-in email broadcasts + documented REST API + HMAC-signed webhooks | `/sales-waitlister` |
| Developer widget with an unauthenticated signup API + censored public leaderboard | `/sales-getwaitlist` |
| One-time lifetime pricing instead of subscription | `/sales-launchlist` |
| Waitlists **plus** giveaways/contests with fraud webhooks | `/sales-kickofflabs` |
| Fastest no-frills validation page, custom domain, free to start | `/sales-waitlistly` |
| The growth *strategy* (referral design, lead magnets, cross-promotion) — tool-agnostic | `/sales-audience-growth` |
