# GutenKit Platform Reference

## Overview

GutenKit is a **feature-rich Gutenberg block plugin and page builder** for WordPress, built by **Wpmet** (the team behind ElementsKit, ShopEngine, and MetForm; lead author Ataur R). It *extends* the native block editor with page-builder-like controls — a flexbox **Container**, draggable layouts, responsive breakpoints, motion effects — rather than replacing the editor the way Elementor/Divi do. Its angle is breadth of ready-made blocks + a deep template library at a generous free tier, with **Full Site Editing (FSE)** compatibility. ~70,000+ active installs; WP 6.1+ / PHP 7.4+, tested to WP 7.0; Block API v3, zero jQuery; current v2.4.x. Slug: `gutenkit-blocks-addon`.

## Capabilities & automation surface

| Module / feature | What it does | Automation tag |
|---|---|---|
| **65+ blocks** (Container, Nav Menu, Mega Menu, Advanced Accordion/Tab, Post Grid/Blog Posts, Post Tab, Pricing Table, Countdown Timer, Image Box/Icon Box, Image Comparison, Timeline, Testimonial, Team, Gallery, Offcanvas, Social Icons/Share, Back to Top, Progress Bar, Fun Fact, Business Hours, Dual Button) | Drag-and-drop building inside the native block editor; output is `gutenkit/`-namespaced block markup | UI-first; markup readable/writable via **WordPress core REST API** |
| **900+ templates / patterns** | Importable pre-designed pages and sections | UI-only (import in editor; library handler shared with ElementsKit) |
| **Flexbox Container** + responsive breakpoints (mobile/tablet/desktop/landscape) | Page-builder layout primitive with absolute/fixed/default positioning, inline editing | UI-only |
| **Mega Menu** (Pro) | Multi-column navigation menus built from blocks | UI-only |
| **Query Loop Builder** (Pro) | Dynamic post listing — filter by post type, taxonomy, meta query, date query, author, post status | UI-only; underlying content readable via WP REST API |
| **Dynamic Content** (Pro) | Bind block text/links/images to post fields, site title, author, user info, and custom fields (ACF-style) | UI-only |
| **Display Conditions** (Pro) | Show/hide blocks by rule (login state, role, date, etc.) | UI-only |
| **Motion / Interaction effects, Parallax, One Page Scroll, Sticky Content** (advanced ones Pro) | Scroll/transform animations, parallax, full-page scroll, sticky elements | UI-only |
| **Mailchimp block** | Opt-in form that subscribes to a Mailchimp audience | Native Mailchimp integration; **no GutenKit-side webhook/storage** |
| **Global colors / fonts, local Google Fonts, inline SVG icons** | Site-wide palette/typography; GDPR-friendly local font loading; per-icon SVG loading | UI-only (stored in theme/global styles) |

**Performance posture:** Block API v3, zero jQuery, selective CSS/JS asset loading per page, local Google Fonts, individually-loaded inline SVG icons — marketed as matching core Gutenberg performance. **No native A/B testing, heatmaps, or analytics on any tier.** No full form builder (Mailchimp opt-in block only).

## Pricing, limits & plan gates

*Best-effort from research (2026-06); sources disagree on exact numbers and on the free-vs-Pro split — confirm on wpgutenkit.com/pricing. Annual unless noted; lifetime options exist; a free version lives on WordPress.org.*

| Tier | Yearly | Lifetime | Sites | Highlights |
|---|---|---|---|---|
| **Free** | $0 (WordPress.org) | — | unlimited | Core block set, template library, flexbox Container, responsive editing, global colors/fonts, Mailchimp block |
| **Personal** | ~$39/yr | ~$89 | 1 | Pro blocks/modules: Mega Menu, Query Loop Builder, Glass Morphism, animation effects |
| **Professional** | ~$79/yr | ~$189 | 5 | Everything in Personal across more sites; full template library; One Page Scroll, Parallax, Advanced Accordion |
| **Agency** | ~$149/yr | ~$389 | unlimited | All modules incl. Dynamic Content, Sticky Content, Display Conditions, Advanced Tab, Post blocks |

- **Plan-gated features (Pro):** Mega Menu, Query Loop Builder, Dynamic Content, Display Conditions, One Page Scroll, Sticky Content, Glass Morphism, Advanced Tooltip, Google Map, advanced Parallax, Price Menu.
- **License lapse:** Pro-only blocks/styling stop applying when the license expires — test on staging before relying on them for a live launch.
- **Counts vary:** different reviews cite free block counts from ~33 to ~50 and Pro from ~50 to ~65; treat any specific number as best-effort and verify the live feature matrix.

## Integrations

- **Reads/writes:** Page/post content via the **WordPress core REST API** (`gutenkit/`-namespaced block markup in `post_content`). No proprietary GutenKit API.
- **Lead capture:** the **Mailchimp** block subscribes opt-ins directly to a Mailchimp audience (connect your Mailchimp API key). There is **no** native form storage, webhook, Zapier app, or CRM connector — for anything beyond a Mailchimp opt-in, pair a dedicated form plugin.
- **Dynamic data sources:** Query Loop Builder + Dynamic Content read WordPress posts, taxonomies, meta, and custom fields (ACF-style) — all WordPress-side, no external API.
- **External services used by blocks:** Mailchimp (opt-in block), Google Maps (Map block, Pro), Google Fonts (local-loaded for GDPR).
- **Companion plugins (same maker, Wpmet):** ElementsKit (Elementor addon), ShopEngine (WooCommerce), MetForm (forms) — note the **shared template-library handler with ElementsKit** can conflict on version mismatch.
- **iPaaS:** No first-party Zapier/Make app. To push leads outward, use the Mailchimp block (then route from Mailchimp), or swap in a form plugin that has native iPaaS.

## Data model

GutenKit stores everything as **WordPress block markup** inside the post/page `post_content`. There is no separate object database to query via a GutenKit API — you operate on WordPress posts.

A GutenKit block in `post_content` looks like this (shape constructed from observed Gutenberg block markup; verify attribute names against a live saved page):

```html
<!-- wp:gutenkit/button {"blockId":"gkit-AB12cd"} -->
<div class="wp-block-gutenkit-button gutenkit-element gkit-AB12cd">
  <a class="gkit-button" href="/signup">Get Started</a>
</div>
<!-- /wp:gutenkit/button -->
```
<!-- Constructed from observed Gutenberg block markup — verify the gutenkit/ namespace and attribute names (e.g. blockId) against the live editor / block.json. -->

Retrieved via the WordPress REST API, a page is a standard post object:

```json
{
  "id": 482,
  "status": "publish",
  "type": "page",
  "content": {
    "raw": "<!-- wp:gutenkit/container ... --> ... <!-- /wp:gutenkit/container -->",
    "rendered": "<div class=\"wp-block-gutenkit-container ...\">...</div>"
  }
}
```
<!-- Constructed from the WordPress core REST API page schema — content.raw requires context=edit + auth. -->

A **Query Loop Builder** block doesn't store the posts it lists — it stores query parameters (post type, taxonomy, meta, order) and renders against the WordPress posts at display time. To read what it lists, query the underlying posts via the WordPress REST API (`/wp/v2/{post_type}`).

## Quick-start recipes

> GutenKit has **no hosted API**. These recipes use the **WordPress core REST API**. Base URL = your site, e.g. `https://example.com/wp-json/wp/v2/`. Auth = **Application Passwords** (Users → Profile → Application Passwords) over HTTPS, sent as HTTP Basic.

### Recipe 1 — Read a page's GutenKit block markup
**Trigger:** you need the raw block markup to audit or transform it.

cURL:
```bash
curl -s "https://example.com/wp-json/wp/v2/pages/482?context=edit" \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['content']['raw'])"
```

Python:
```python
import requests
from requests.auth import HTTPBasicAuth

site = "https://example.com"
auth = HTTPBasicAuth("admin", "xxxx xxxx xxxx xxxx xxxx xxxx")  # Application Password

r = requests.get(f"{site}/wp-json/wp/v2/pages/482",
                 params={"context": "edit"}, auth=auth)
r.raise_for_status()
raw = r.json()["content"]["raw"]
print(raw[:500])  # gutenkit/-namespaced block markup
```
**Gotcha:** `context=edit` (needed for `content.raw`) requires an authenticated user who can edit the post; without it you only get `content.rendered` HTML.

### Recipe 2 — Bulk-update CTA text inside GutenKit blocks
**Trigger:** swap a string across many pages.

Python:
```python
import requests
from requests.auth import HTTPBasicAuth

site = "https://example.com"
auth = HTTPBasicAuth("admin", "xxxx xxxx xxxx xxxx xxxx xxxx")
page_ids = [482, 483, 484]

for pid in page_ids:
    r = requests.get(f"{site}/wp-json/wp/v2/pages/{pid}",
                     params={"context": "edit"}, auth=auth)
    raw = r.json()["content"]["raw"]
    updated = raw.replace("Get Started", "Start Free Trial")
    # POST the transformed markup back; WordPress re-parses the blocks
    requests.post(f"{site}/wp-json/wp/v2/pages/{pid}",
                  json={"content": updated}, auth=auth).raise_for_status()
    print(f"updated {pid}")
```
**Gotcha:** edit the block *markup* string, not the rendered HTML — POSTing rendered HTML strips the `<!-- wp:gutenkit/... -->` block delimiters and the page stops being editable as blocks. Test on staging; back up first.

### Recipe 3 — List the posts a Query Loop Builder block renders
**Trigger:** you have a GutenKit Query Loop on a page and need the actual posts it shows (for an export or a sync) — the block stores the *query*, not the posts.

Python:
```python
import requests
from requests.auth import HTTPBasicAuth

site = "https://example.com"
auth = HTTPBasicAuth("admin", "xxxx xxxx xxxx xxxx xxxx xxxx")

# Mirror the Query Loop's filters (post type 'post', category 12, newest first)
posts, page = [], 1
while True:
    r = requests.get(f"{site}/wp-json/wp/v2/posts",
                     params={"categories": 12, "orderby": "date", "order": "desc",
                             "per_page": 100, "page": page}, auth=auth)
    if r.status_code == 400:        # past the last page
        break
    posts += r.json()
    if page >= int(r.headers.get("X-WP-TotalPages", 1)):
        break
    page += 1
print(len(posts), "posts the loop would render")
```
**Gotcha:** the GutenKit block's stored query params (post type, taxonomy, meta) are inside the block markup attributes — read them from `content.raw` (Recipe 1) and reproduce them in the REST query so the export matches what the page renders.

## Integration patterns

- **Lead sync:** GutenKit's only native capture is the **Mailchimp** block — opt-ins land in a Mailchimp audience, and you route onward from Mailchimp (tags/automation). For CRM routing, conditional logic, multi-step, or payment fields, swap in a form plugin with native webhooks/iPaaS and run the sequence via `/sales-email-marketing`. Don't expect GutenKit-side webhook delivery or stored entries.
- **Programmatic page management:** treat GutenKit pages as ordinary WordPress posts. Use the core REST API with Application Passwords; operate on `content.raw` block markup (`context=edit`). Paginate list endpoints with `?page=` + `per_page=` and read the `X-WP-Total` / `X-WP-TotalPages` headers.
- **Performance/asset handling:** GutenKit loads styling per page (selective CSS/JS). When markup is injected dynamically or served from cache, clear page/object/CDN cache and exclude GutenKit's CSS/JS from aggressive minify/combine so the frontend matches the editor.
- **ElementsKit coexistence:** if you also run ElementsKit (same maker), keep both Wpmet plugins on matched current versions — the shared template-library handler is the documented conflict point. Isolate by deactivating one when the template library errors.
- **Extending blocks:** there's no GutenKit SDK — extend via standard WordPress hooks/filters against the rendered block output (e.g. `render_block`) and the WordPress REST API for content. See `references/gutenkit-api-reference.md`.
