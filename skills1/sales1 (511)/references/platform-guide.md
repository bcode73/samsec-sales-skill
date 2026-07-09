# SeedProd Platform Reference

## Overview

SeedProd is a WordPress drag-and-drop website + landing-page builder plugin (by Awesome Motive, 1M+ installs). It builds landing pages, full themes (headers/footers/templates), and the built-in coming-soon, maintenance, 404, and login pages without touching code. Primary differentiator: it replaces the whole theme via its Theme Builder and ships an AI site builder, while staying a self-hosted WordPress plugin (your data, your host). It is *not* a hosted SaaS like Instapage/Unbounce and has no traditional outbound REST API — automation runs through the WordPress Abilities API, shortcodes, PHP hooks, and Zapier.

## Capabilities & automation surface

| Module / capability | What it does | Automation tag |
|---|---|---|
| Drag & Drop Page Builder | Visual builder, 90+ Pro blocks, Smart Sections (reusable saved sections) | UI-only (content reachable via `save-page` ability) |
| Theme Builder (Plus+) | Replaces the WordPress theme — headers, footers, page/post/archive/sidebar templates, WooCommerce templates (Elite) | UI-built; `toggle-theme` + `import-theme` abilities |
| Landing page types | Sales, opt-in/squeeze, webinar, thank-you, coming-soon, maintenance, 404, login pages | UI / `save-page` ability |
| Coming Soon & Maintenance Mode | Site-wide gated page with access control | `toggle-coming-soon` / `toggle-maintenance` abilities |
| Templates & Themes | 50–300+ page templates (tier-based), 200+ themes, 100+ section templates (Plus+) | UI-only |
| Subscriber management | Built-in email subscriber capture + management; spam protection (reCAPTCHA) | UI; export; ESP/Zapier out |
| ESP integrations | Native opt-in delivery to 13 ESPs (all tiers) | Connector (writes leads out) |
| Dynamic Text (Pro+) | Swap page copy from URL params / WP data (ad-to-page message match) | UI config |
| WooCommerce blocks (Elite) | Product grids, add-to-cart, cart/checkout, product meta/gallery/tabs via shortcodes | Shortcodes |
| Easy Digital Downloads blocks | EDD product grid, buy-now, cart, checkout, add-to-cart via shortcodes | Shortcodes |
| Zapier (Pro+) | 3000+ app automations | iPaaS |
| AI Theme Builder | Describe a business → generates a full WordPress site | UI |
| Abilities API (6.20.0+) | 8 named actions exposed to any WordPress Abilities API client / AI tool | API-accessible |
| Permission filters | PHP `add_filter` hooks gating menu/page/plugin actions by capability | Code (server-side) |

## Pricing, limits & plan gates

All paid tiers are **annual, introductory-priced, and renew at full price**; 14-day refund. A free version exists on WordPress.org (coming-soon/maintenance + basic builder).

| Plan | Intro price | Sites | Templates | Key unlocks |
|---|---|---|---|---|
| **Basic** | $79/yr | 1 | 50 | 90+ blocks, landing pages, coming-soon/maintenance, all 13 ESP integrations |
| **Plus** | $199/yr | 3 | 100 | + **Theme Builder**, 100+ section templates |
| **Pro** | $399/yr | 5 | 300+ | + **Zapier (3000+)**, + **Dynamic Text** |
| **Elite** | $599/yr | 100 | 300+ | + **WooCommerce support**, + **Domain Mapping**, priority support |

Plan-gate cheat sheet (the source of most "where is X?" tickets):
- **Theme Builder → Plus+**
- **Zapier + Dynamic Text → Pro+**
- **WooCommerce support + Domain Mapping → Elite only**
- **No native A/B testing, heatmaps, or analytics on any tier** — pair with a separate tool.

## Integrations

Data flow is **outbound from SeedProd opt-in forms to ESPs** — SeedProd captures the lead and writes it to the connected service; it does not read back from them.

- **ESPs (all tiers, native):** ActiveCampaign, AWeber, Campaign Monitor, Constant Contact, ConvertKit (Kit), Drip, GetResponse, iContact, Mad Mimi, Mailchimp, MailerLite, Sendy, Sendinblue (Brevo).
- **Zapier (Pro+):** 3000+ apps for downstream routing (CRM, Slack, sheets).
- **Commerce:** WooCommerce (Elite) and Easy Digital Downloads product/cart/checkout blocks rendered via shortcodes.
- **Spam:** Google reCAPTCHA on forms.
- **AI tools / automation:** Abilities API clients (e.g. WPVibe, Claude) auto-discover SeedProd's 8 actions on a connected site — no per-tool integration.

## Data model

SeedProd stores pages/templates as WordPress posts of its own custom post types and keeps settings in WordPress options — there is no external JSON object model exposed by a public REST API. The closest structured surface is the **Abilities API** request/response. Representative shapes (constructed from documented behavior):

<!-- Constructed from docs — verify against live API -->
```json
// get-status ability response (fields per documented behavior)
{
  "coming_soon": true,
  "maintenance": false,
  "theme_enabled": true,
  "license": { "active": true, "tier": "Pro" }
}
```

```json
// list-pages ability response
{
  "pages": [
    { "id": 412, "title": "Spring Launch", "type": "landing", "status": "publish" },
    { "id": 87,  "title": "Coming Soon",   "type": "coming_soon", "status": "active" }
  ]
}
```

```json
// save-page ability request (create or update)
{
  "id": null,
  "title": "Webinar Opt-in",
  "type": "optin",
  "content": "<!-- SeedProd builder blocks -->"
}
```

## Quick-start recipes

### Recipe 1 — Toggle coming-soon mode for a launch via the Abilities API
WordPress 6.9+ ships the **Abilities API**; SeedProd 6.20.0+ registers 8 abilities. Any Abilities-API client (or AI tool like WPVibe/Claude on a connected site) can discover and run them. Auth is standard WordPress REST authentication — an **application password** for the user, sent over HTTPS.

<!-- Constructed from docs — verify exact route against your WP/SeedProd version -->
```bash
# Read SeedProd's current state, then turn coming-soon mode OFF for go-live.
# Abilities are invoked through the WordPress Abilities REST surface; route/version may vary.
curl -s https://example.com/wp-json/wp/v2/abilities/seedprod/get-status \
  -u "wpuser:APPLICATION_PASSWORD"

curl -s -X POST https://example.com/wp-json/wp/v2/abilities/seedprod/toggle-coming-soon \
  -u "wpuser:APPLICATION_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'
```
```python
import requests
from requests.auth import HTTPBasicAuth

base = "https://example.com/wp-json/wp/v2/abilities/seedprod"
auth = HTTPBasicAuth("wpuser", "APPLICATION_PASSWORD")  # WP application password

status = requests.get(f"{base}/get-status", auth=auth).json()
if status.get("coming_soon"):
    requests.post(f"{base}/toggle-coming-soon", auth=auth, json={"enabled": False})
```
**Gotchas:** Requires WordPress **6.9+** and SeedProd **6.20.0+** or the abilities aren't registered. The exact REST route/namespace can differ by version — discover it via the Abilities API index rather than hard-coding. `import-theme` takes a ZIP URL; `activate-license` takes a Pro key.

### Recipe 2 — Restrict the SeedProd builder to administrators (permission filter)
SeedProd menu/page/plugin actions are gated by WordPress capabilities via `add_filter`. Drop this in a site-specific plugin or `functions.php`:
```php
// Only administrators (manage_options) can open the SeedProd builder.
add_filter( 'seedprod_builder_menu_capability', function () {
    return 'manage_options';
} );

// Lock the whole SeedProd menu the same way.
add_filter( 'seedprod_main_menu_capability', function () {
    return 'manage_options';
} );
```
**Gotchas:** Menu/interface filters default to `edit_others_posts`; page-management filters (archive/trash) default to `list_users`; plugin-management filters default to the matching WP cap (`install_plugins`, etc.). Return any valid WP capability string.

### Recipe 3 — Capture opt-in leads into an ESP, then route onward
On any tier, add an Optin block, connect the form to one of the 13 native ESPs (Mailchimp/ConvertKit/etc.), and map fields. To fan out to a CRM/Slack/sheet, send the ESP's "new subscriber" event into **Zapier (Pro+)** or use the ESP's own automation. SeedProd holds the subscriber list and writes outbound; it does not poll the ESP back.
```bash
# There is no SeedProd lead-pull endpoint. Read leads from the ESP instead, e.g. Mailchimp:
curl -s https://us1.api.mailchimp.com/3.0/lists/LIST_ID/members \
  -u "anystring:MAILCHIMP_API_KEY"
```
**Gotchas:** No SeedProd webhook/REST exists to pull submissions — reconcile from the ESP side. Enable reCAPTCHA to keep bot signups out of the list.

## Integration patterns

- **Automation architecture:** SeedProd is a WordPress plugin, so server-side automation is **PHP hooks/filters + shortcodes**, and remote automation is the **Abilities API** (AI-tool/REST) plus **Zapier (Pro+)**. There is no hosted REST API and no native outbound webhook — design lead flows around the ESP/Zapier, not around SeedProd.
- **Coming-soon as a deploy gate:** Use `get-status` → `toggle-maintenance`/`toggle-coming-soon` to wrap deploys; always clear the page/CDN cache after toggling or visitors keep seeing the cached gated page.
- **Theme lifecycle:** `import-theme` (ZIP URL) → `toggle-theme` to roll a templated theme onto a fresh site; the `seedprod_disable_theme_load` filter is the escape hatch to keep the underlying theme on specific URLs.
- **Capability hardening:** In multi-author sites, tighten `seedprod_*_capability` filters so editors can't change site-wide theme/coming-soon state.
