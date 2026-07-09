<!-- Source: https://www.npmjs.com/package/referlist , https://registry.npmjs.org/referlist , https://github.com/parthibanloganathan/referlist-sdk , https://docs.referlist.co/ (REST docs JS-rendered; fetched 2026-06) -->

# Referlist — Programmatic Surface

Referlist exposes two programmatic layers: a **client-side JavaScript SDK** (well-documented, captured verbatim below) and a **Pro-gated REST API** (capabilities known; base URL/auth/paths are behind a JS-rendered docs site — see `## Gaps`).

## Client-side SDK (`referlist`, npm v1.0.9)

Install:
```bash
npm install referlist --save
```

Initialize on mount (the library reads `window`, so it must run client-side):
```javascript
// React hooks
useEffect(() => {
  referlist.initialize({ domain: 'NAME_OF_YOUR_DOMAIN' });
}, []);
```
- **Class components:** call `referlist.initialize({ domain })` in `componentDidMount`.
- **Next.js:** import dynamically with `{ ssr: false }` (or import inside `useEffect`) because the library accesses `window`.

Auto-binding: add these IDs to your form and the SDK wires them up automatically:
- `id="referlistemail"` on the email `<input>`
- `id="referlistbutton"` on the submit `<button>`

Manual add (custom forms / custom flows):
```javascript
window.referlist.addToWaitlist('NAME_OF_YOUR_DOMAIN', 'EMAIL_TO_ADD_TO_WAITLIST', 'REFERRAL_CODE');
```
- 1st arg: your Referlist domain/identifier.
- 2nd arg: the email to add.
- 3rd arg: the **referral code** of whoever referred this visitor (capture it from the inbound `?ref` URL param). Omitting it records the signup but credits no referrer, so positions don't move.

Repo: `github.com/parthibanloganathan/referlist-sdk` (client-side only; default branch `master`; last updated 2022). Full docs: `docs.referlist.co`.

## REST API (Pro plan and above)

**Documented capabilities** (from the marketing site / docs index; gated to Pro $59/mo):

| Capability | Method (assumed) | Notes |
|---|---|---|
| Add an email signup | POST | Accepts an email; optional referral code to attribute the referrer |
| Get info for a particular email | GET | Returns that email's details incl. **place in line** |
| List all emails in the waitlist | GET | Returns the full waitlist (verify pagination) |

Five integration methods exist overall: embedded form, npm SDK, JS snippet + element IDs, JS snippet + manual `addToWaitlist`, and this REST API.

### Auth quick-start (template — verify before use)
```bash
# ⚠️ Base URL, auth scheme, and paths are NOT in the public docs index. Confirm in
#    the signed-in docs at docs.referlist.co, then replace the placeholders.
curl -H "Authorization: Bearer $REFERLIST_API_KEY" \
  "https://<VERIFY-BASE-URL>/<VERIFY-PATH>?domain=YOUR_DOMAIN"
```

### Representative response (constructed — verify field names)
```json
<!-- Constructed from documented capabilities — NOT copied from Referlist docs. Verify against a live response. -->
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

## Export (no-code egress)

- **CSV**, **Mailchimp**, **Airtable** export from the dashboard (Free export capped at 100 signups; higher caps on paid tiers).

## Gaps (could not be verified — confirm in the live docs)

- **REST base URL** (e.g. `api.referlist.co` vs a path under `referlist.co`) — unknown.
- **Auth method** (API key header? Bearer token? where issued — likely a Pro account setting) — unknown.
- **Exact endpoint paths, HTTP methods, request bodies, and response schemas.**
- **Pagination** for the list endpoint (cursor/offset/page) — unknown.
- **Rate limits / error format.**
- **Webhooks / Zapier / Make** — not found in any source; assume **absent** until verified.
- **The exact client-side snippet `src` URL** (Recipe 2 uses a placeholder) — copy it from your dashboard's install instructions.
