# Kadence Blocks Platform Reference

## Overview

Kadence Blocks is a **Gutenberg page-builder block plugin for WordPress** (by **StellarWP / Liquid Web**; 600,000+ active installs, GPLv2, open-source at `github.com/stellarwp/kadence-blocks`). It **extends** the native WordPress block editor with 20+ custom blocks and advanced design controls rather than replacing it (the contrast with Elementor/Divi). It's the default rival to Spectra and GenerateBlocks, and pairs with the broader Kadence ecosystem (Kadence Theme, Shop Kit for WooCommerce, Kadence Cloud, Kadence Central). It builds the funnel's *pages* (opt-in, sales, landing) — it is **not** an all-in-one (no native cart beyond WooCommerce/Shop Kit, no email sequences, no A/B testing).

*Pricing, plan gates, and feature availability below are best-effort from 2026-06 research — verify against current docs.*

## Capabilities & automation surface

| Module / capability | What it does | Automation tag |
|---|---|---|
| **Free blocks (20+)** — Row Layout / Section (flexbox containers), Advanced Form, Advanced Gallery, Accordion, Tabs, Testimonials, Info Box, Icon / Icon List, Posts, Countdown, Count Up, Progress Bar, Table of Contents, Lottie Animation, Show More, Advanced Button, Advanced Text, Spacer/Divider, Off-Canvas | Build pages with native blocks; markup stored as `kadence/`-namespaced block comments in `post_content` | **API-accessible** (read/write via WP REST API on the post) |
| **Advanced Query Loop** (Pro) | Dynamic post/CPT loops with granular query control | UI-built; query modifiable via `kadence_blocks_pro_query_loop_query_vars` filter |
| **Dynamic Content** (Pro) | Bind block content to post meta, **ACF**, **MetaBox**, **WooCommerce** fields | **UI-only** binding; data source read via WP/ACF APIs |
| **Advanced Slider, Modal, Post/Product Carousel, Image Overlay** (Pro) | Premium layout/interaction blocks | UI-only |
| **Animate on Scroll, Custom Fonts, Custom Icons** (Pro) | Motion + branding controls | UI-only |
| **Design Library / Creative Kit + Kadence AI** (Pro) | Pre-built patterns/section templates + AI-generated sections | UI-only (AI generates editable blocks) |
| **Advanced Form webhooks** (Pro) | Send form submissions to an external URL | **Webhook-accessible** (outbound, per-form) |
| **Posts block** (Free) | Simple post grid/list | UI-built; query modifiable via `kadence_blocks_posts_query_args` filter |
| **Intelligent asset loading** | Only loads CSS/JS for blocks actually used on a page | UI/setting |
| **Performance tools** | Built-in one-click speed settings (CSS output mode, asset handling) | UI setting |

**There is no hosted/outbound REST API for the platform.** Everything programmatic rides on WordPress itself: the core REST API over the post that holds the blocks, PHP hooks/filters, and the Advanced Form webhook.

## Pricing, limits & plan gates

Best-effort, 2026-06 — **verify before quoting.** Kadence Blocks Pro is sold standalone and inside the unified **Kadence** bundles (sold via Liquid Web). The free plugin is on WordPress.org.

| Plan | Price (annual, best-effort) | What it adds |
|---|---|---|
| **Free** | $0 (WordPress.org) | 20+ blocks, responsive controls, 900+ Google fonts, Design Library (free patterns), configurable block defaults |
| **Kadence Blocks Pro** (standalone) | ~$89/yr (historical) | Advanced Query Loop, Dynamic Content, Advanced Slider, Modal, Image Overlay, Post/Product Carousel, Animate on Scroll, Custom Fonts/Icons, form webhooks, Kadence AI, full Design Library |
| **Essentials** | ~$99/yr | Theme + Blocks Pro + premium templates |
| **Pro** | ~$299/yr | + security suite, Shop Kit (WooCommerce), memberships/content gating |
| **Elite** | ~$499/yr | + Kadence Central multi-site management, white-label, A/B testing, daily backups |

- **Will my integration break on free?** Yes if it depends on **form webhooks, Dynamic Content, or Advanced Query Loop** — all Pro. The WP REST API on block content works on any tier (it's WordPress core).
- **License lapse:** Pro-gated block features degrade / stop rendering their Pro behavior when the license expires. Test on staging before relying on Pro blocks for a live page.
- **No rate limits of its own** — you're bound by your WordPress host and (for webhooks) the receiving endpoint.

## Integrations

- **Dynamic data (reads from):** ACF, MetaBox, WooCommerce product/order fields, post meta — surfaced through Dynamic Content and the Query Loop.
- **Form submissions (writes to):** native ESP/CRM integrations on the Advanced Form, plus the **outbound webhook** (Pro) → any URL, commonly **Zapier** ("Catch Hook" / "Webhooks by Zapier") or **Make**. Third-party automators (WP Webhooks, FlowMattic, Bit Integrations) also expose a `kdbl_submit` trigger.
- **Design assets (bidirectional):** Kadence Cloud stores reusable sections/patterns synced into the Design Library.
- **No first-party Zapier/Make app** — automation rides on the form webhook or on WordPress hooks.

## Data model

Kadence blocks are **not** rows in a database table — they're **block markup inside `post_content`**. You read/write them via the WordPress REST API on the post.

A Kadence block in `post_content` looks like (Row Layout wrapping an Advanced Button):

```html
<!-- wp:kadence/rowlayout {"uniqueID":"123_abc","columns":1} -->
<div class="wp-block-kadence-rowlayout">
  <!-- wp:kadence/advancedbtn {"uniqueID":"456_def"} -->
  <div class="wp-block-kadence-advancedbtn">…</div>
  <!-- /wp:kadence/advancedbtn -->
</div>
<!-- /wp:kadence/rowlayout -->
```

<!-- Constructed from docs — verify against live block markup -->

Reading the post via the REST API returns the markup in `content.raw`:

```json
{
  "id": 42,
  "status": "publish",
  "content": {
    "raw": "<!-- wp:kadence/rowlayout {\"uniqueID\":\"123_abc\"} -->…<!-- /wp:kadence/rowlayout -->",
    "rendered": "<div class=\"wp-block-kadence-rowlayout\">…</div>"
  }
}
```

An **Advanced Form webhook** payload is a flat map of your **mapped field names → submitted values** (you control the keys via **Map Fields**):

```json
{
  "email": "jane@example.com",
  "name": "Jane Doe",
  "message": "Interested in a demo"
}
```

<!-- Constructed from documented behavior — verify against a live test submission -->

## Quick-start recipes

### Recipe 1 — Capture an Advanced Form submission in a CRM (no code on the WP side)

**Trigger:** form submitted → **Kadence pushes a webhook** → your endpoint / Zapier / Make creates the CRM record.

Setup (requires **Kadence Blocks Pro**):
1. Edit the form block. For **Kadence Form**: *Actions After Submit* → check **WebHook**. For **Kadence Form (Adv)**: *Submit Actions* → add **WebHook**.
2. In **Webhook Settings**, paste your **Webhook URL** and use **Map Fields** to set the payload keys.
3. Receive it. A minimal listener:

```python
# Flask receiver for a Kadence Advanced Form webhook
from flask import Flask, request
import requests

app = Flask(__name__)

@app.post("/kadence-hook")
def kadence_hook():
    data = request.get_json(silent=True) or request.form.to_dict()
    # data keys are whatever you set under "Map Fields"
    requests.post(
        "https://api.your-crm.example/v1/contacts",
        headers={"Authorization": "Bearer YOUR_CRM_TOKEN"},
        json={"email": data.get("email"), "name": data.get("name")},
        timeout=10,
    )
    return "", 200
```

Test with a temporary URL first:
```bash
# grab a throwaway URL from webhook-test.com, paste it as the Webhook URL, submit the form
curl -s https://webhook-test.com/<your-token> | jq .
```

**Gotchas:** webhook is **Pro-only**; the form id used in markup is `kadence-form-{id}` (inspect the frontend to find it); there is no documented signature/HMAC — make the handler **idempotent** and validate fields server-side.

### Recipe 2 — Read/update a page's Kadence blocks via the WordPress REST API

**Trigger:** you want to programmatically read or edit the block content (e.g. swap a CTA across pages).

```bash
# Read raw block markup (needs context=edit + auth via Application Password)
curl -s "https://example.com/wp-json/wp/v2/pages/42?context=edit" \
  -u "admin:APPLICATION_PASSWORD" | jq -r '.content.raw'
```

```python
import requests
from requests.auth import HTTPBasicAuth

base = "https://example.com/wp-json/wp/v2"
auth = HTTPBasicAuth("admin", "APPLICATION_PASSWORD")

page = requests.get(f"{base}/pages/42", params={"context": "edit"}, auth=auth).json()
new_markup = page["content"]["raw"].replace("Get the guide", "Start free trial")
requests.post(f"{base}/pages/42", auth=auth, json={"content": new_markup})
```

**Gotchas:** you're editing **raw block markup** — keep the `<!-- wp:kadence/... -->` delimiters and `uniqueID` attributes intact or the block breaks in the editor. This is core WordPress, not a Kadence API.

### Recipe 3 — Change what the Posts / Query Loop block pulls (PHP filter)

**Trigger:** you need a custom query the block UI can't express.

```php
// Free Posts block — modify WP_Query args
add_filter( 'kadence_blocks_posts_query_args', function ( $query_args, $attributes ) {
    $query_args['meta_key']   = 'featured';
    $query_args['meta_value'] = '1';
    return $query_args;
}, 10, 2 );

// Pro Advanced Query Loop — customize query vars (post_type, meta_key, meta_value, comment_count, …)
add_filter( 'kadence_blocks_pro_query_loop_query_vars', function ( $query_vars, $attributes ) {
    $query_vars['post_type'] = 'product';
    return $query_vars;
}, 10, 2 );
```

<!-- Filter names verified from Kadence docs/changelog; exact callback arg count may vary — verify on a staging site. -->

**Gotchas:** these are **developer hooks** — run on staging, and note the Advanced Query Loop filter requires **Kadence Blocks Pro**.

## Integration patterns

- **Form-lead pipeline:** Advanced Form → webhook → automation layer (Zapier/Make/your service) → CRM/ESP. There's no platform-side delivery log or retry guarantee on the webhook, so **make consumers idempotent** (dedupe on email + timestamp) and validate every field.
- **Content automation:** treat pages as WordPress posts. Read `content.raw` (Application-Password auth, `context=edit`), transform the block markup as text while preserving delimiters/`uniqueID`s, write back via `POST /wp/v2/pages/{id}`. Regenerate Kadence's cached CSS after bulk edits.
- **Performance posture:** set CSS output to **External File**, enable the Performance tools, and serve generated CSS/JS from a page cache; exclude Kadence's handles from any minify/combine/defer step in your optimization plugin.
- **Dynamic listings:** prefer the Pro **Advanced Query Loop** + Dynamic Content for ACF/Meta Box/WooCommerce data; drop to the `kadence_blocks_pro_query_loop_query_vars` filter only when the UI can't express the query.
