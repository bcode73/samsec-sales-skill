---
name: sales-spectra
description: "Spectra platform help — Gutenberg-native WordPress website/page builder plugin by Brainstorm Force (Astra makers; formerly Ultimate Addons for Gutenberg, 1M+ installs): 30+ blocks, flexbox Container, Starter Templates, Popup Builder, Coming Soon mode, animations, local Google Fonts, plus Pro Loop Builder, Dynamic Content, display conditions, role permissions & white label; developer hooks/filters (uagb_*, spectra_*) including a spectra_pro_rest_api_get_controllers REST filter. Use when the Spectra editor is slow or freezing on long posts, Spectra blocks or CSS won't render on inner pages (only the homepage), a Post Grid or Taxonomy block looks distorted inside a template, deciding which plan unlocks Loop Builder/Dynamic Content/Popup Builder/white label, Pro blocks drop to fallback content after deactivating, or customizing block output via hooks. Do NOT use for cross-tool builder selection or funnel/CRO strategy (use /sales-funnel) or checkout/cart across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in Spectra]"
license: MIT
version: 1.0.0
tags: [sales, funnel, landing-pages, platform]
github: "https://github.com/brainstormforce"
---

# Spectra Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken state — editor slow/freezing, blocks or CSS not rendering on inner pages, Post Grid/Taxonomy block distorted in a template, site broke after an update
   - B) Build with blocks — Container/flexbox layout, Starter Templates, Popup Builder, Coming Soon mode, animations, Global Styles, Wireframe blocks
   - C) Use Pro/dynamic features — Loop Builder, Dynamic Content, display conditions, role permissions, white label
   - D) Customize/automate — public actions & filters, `spectra_pro_rest_api_get_controllers` REST filter, design-library role gating, query-arg filters
   - E) Pick or compare a plan (Free / Pro / Essential Toolkit / Business Toolkit) or weigh Spectra vs other block builders

2. **Free or Pro?** Free (WordPress.org, 30+ blocks). Pro is sold as Spectra Pro or the Essential/Business Toolkit bundles. Several blocks and features (Loop Builder, Dynamic Content, display conditions, white label, finer styling) are Pro-gated.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Funnel strategy, page structure, builder selection across tools (Elementor/Kadence/GenerateBlocks/SeedProd…) | `/sales-funnel` — Run: `/sales-funnel {user's original question}` |
| A/B testing methodology (Spectra has no native split testing) | `/sales-vwo` — Run: `/sales-vwo {user's original question}` |
| Email sequences/automation after a Spectra form opt-in | `/sales-email-marketing` — Run: `/sales-email-marketing {user's original question}` |
| Growing the list, lead-magnet strategy | `/sales-audience-growth` — Run: `/sales-audience-growth {user's original question}` |
| WooCommerce store/checkout beyond Spectra's blocks | `/sales-checkout` — Run: `/sales-checkout {user's original question}` |
| WordPress/WooCommerce funnel + upsells (by the same makers) | `/sales-cartflows` — Run: `/sales-cartflows {user's original question}` |
| On-page/technical SEO beyond Spectra's FAQ/Schema blocks | `/sales-seo` — Run: `/sales-seo {user's original question}` |

If the question is Spectra-specific, continue to Step 3.

## Step 3 — Spectra platform reference

**Read `references/platform-guide.md`** for the full platform reference — blocks/modules, pricing/plan gates, data model, integration recipes, and code examples. For the public actions/filters list, the REST-controller filter, and design-library role gating, read `references/spectra-api-reference.md`.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation.

- **Editor slowness/freezing is the #1 complaint**, especially on long posts with Spectra Pro active. Deactivating Spectra Pro confirms it's the culprit. Mitigate: update to the latest version, disable unused blocks (Spectra → Settings → Blocks), and split very long pages. If it persists, report it with a System Info dump.
- **"Blocks broken on inner pages, fine on the homepage"** is almost always Spectra's **CSS not loading sitewide.** Set Spectra → Settings → **CSS file generation** appropriately and **regenerate Spectra assets** (Settings → Regenerate / clear the `uag_*` asset cache), then clear page/CDN cache.
- **Plan gating drives most surprises.** Free is 30+ blocks; **Loop Builder, Dynamic Content, display conditions, white label, role permissions, and the richer style controls are Pro.** Confirm the tier before promising a feature, and warn that **pages built with Pro-only blocks fall back to fallback content** if Pro is deactivated/expires — test on staging first.
- **No native A/B testing, heatmaps, or analytics.** Pair with a separate tool (VWO, Microsoft Clarity) — Spectra only builds the page.
- **The real automation surface is WordPress hooks/filters**, not a hosted API: `render_block`, `uagb_post_query_args_*` (Post Grid/Masonry/Carousel queries), `spectra_slider_params`, `spectra_countdown_context`, plus `spectra_pro_rest_api_get_controllers` to register a custom REST controller. There is no outbound webhook — form leads flow out via the connected form/ESP integration.
- **Performance angle:** Spectra emits leaner DOM markup than some block plugins, but the **Pro editor's runtime can be heavy** — the page weight win and the editor sluggishness are separate issues.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

1. **Editor backend slows down / freezes**, particularly on long posts and with Spectra Pro enabled. Update first; disable unused blocks; if it persists, it's a known performance area the team is iterating on.
2. **Spectra CSS not loaded on non-homepage pages** makes blocks render unstyled/distorted on inner pages. Fix the CSS file-generation setting and regenerate Spectra assets, then clear caches.
3. **Post Grid / Taxonomy blocks can render distorted inside post/loop templates.** Check the block's query/layout settings and theme template context; the `uagb_post_query_args_*` filters can correct query args.
4. **Pro features don't deactivate gracefully** — blocks built with Pro-only features may switch to **fallback content** when Pro is off/expired. Don't build a live page solely on Pro blocks without a tested fallback.
5. **Loop Builder, Dynamic Content, display conditions, role permissions, and white label are Pro.** The free plugin is block-building only.
6. **No native A/B testing, heatmaps, or analytics.** Spectra builds pages; measurement needs a separate tool.
7. **Spectra + Astra updates have conflicted in the past** (e.g. WP Trac #62481). Update plugins on staging and keep a rollback before bulk-updating a live site.

## Related skills

- `/sales-funnel` — Funnel strategy, page structure, and builder selection across tools (Elementor, Kadence Blocks, GenerateBlocks, SeedProd, ClickFunnels, Leadpages)
- `/sales-cartflows` — WordPress/WooCommerce funnel + checkout builder by the same makers (Brainstorm Force); Spectra builds the pages, CartFlows adds the cart/upsells
- `/sales-kadence` — The closest rival: another Gutenberg-native block plugin (by StellarWP) — compare blocks, performance, plan gates, and developer hooks
- `/sales-generateblocks` — The minimalist, performance-first Gutenberg block plugin (by EDGE22/GeneratePress) — compare its few-primitives model and lean DOM against Spectra's 30+ blocks
- `/sales-stackable` — Another Gutenberg-native block plugin (by Gambit Technologies) — design-focused with 42 blocks but no form/popup builder (Spectra ships both); compare blocks, plan gates, and developer hooks
- `/sales-seedprod` — Another WordPress page/landing-page builder plugin (a non-Gutenberg alternative with Theme Builder + coming-soon pages)
- `/sales-vwo` — A/B testing and heatmap methodology Spectra lacks natively
- `/sales-audience-growth` — Growing an email list (lead magnets, opt-in strategy) behind a Spectra form
- `/sales-email-marketing` — Email sequences to run after a Spectra form captures the lead
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Register a custom REST controller and tweak Post Grid queries via hooks
**User**: "How do I extend Spectra programmatically — add my own REST endpoint and change what the Post Grid block queries?"
**Approach**: Spectra exposes WordPress-style hooks, not a hosted API. Add a custom REST controller by hooking the `spectra_pro_rest_api_get_controllers` filter (push your controller class onto the array). To change which posts the Post Grid/Masonry/Carousel blocks pull, filter `uagb_post_query_args_grid` / `uagb_post_query_args_masonry` / `uagb_post_query_args_carousel` and modify the `WP_Query` args. Pull the exact hook names, parameters, and a code snippet from `references/spectra-api-reference.md`.

### Example 2: Spectra blocks look broken on every page except the homepage
**User**: "My Spectra blocks display fine on the home page but are unstyled/broken on inner pages."
**Approach**: This is Spectra's CSS not being generated/loaded sitewide. In Spectra → Settings, set the **CSS file generation** option and **regenerate Spectra assets** (clears the cached `uag_*` CSS), then purge page cache and CDN. If a security/optimization plugin strips inline CSS or blocks the assets directory, allowlist Spectra's uploads path. See Troubleshooting.

### Example 3: Which plan do I need for Loop Builder and Dynamic Content?
**User**: "I want to build a dynamic blog/portfolio loop and pull custom-field content into blocks — what tier?"
**Approach**: **Loop Builder, Dynamic Content, and display conditions are Pro** — the free plugin can't do them. Spectra Pro (or the Essential/Business Toolkit bundles, which add Astra Pro and more) unlocks them. Warn that pages built with these Pro blocks **fall back to fallback content** if Pro lapses, so test on staging. Confirm current tiers/prices in `references/platform-guide.md` (pricing is best-effort and annual; lifetime deals exist).

## Troubleshooting

### Editor is slow or freezes
**Symptom**: The WordPress block editor becomes sluggish or freezes when editing pages/posts, especially long ones, after enabling Spectra (often Spectra Pro).
**Cause**: Spectra's editor-side runtime overhead, compounded on long documents and by many active blocks.
**Solution**: Update Spectra/Spectra Pro to the latest version; disable blocks you don't use (Spectra → Settings → Blocks); split very long pages; deactivate other heavy editor plugins to isolate the conflict. If it remains, submit System Info to support — it's an acknowledged performance area.

### Spectra blocks render broken on inner pages
**Symptom**: Blocks look correct on the homepage but unstyled or distorted on other pages.
**Cause**: Spectra's per-page CSS isn't being generated/loaded sitewide, or a cache/optimization plugin is stripping it.
**Solution**: Set the **CSS file generation** option (Spectra → Settings), **regenerate Spectra assets** to rebuild the cached `uag_*` CSS, then clear page cache + CDN. Allowlist Spectra's uploads asset path in any minify/security plugin.

### A block (Post Grid/Taxonomy) looks distorted in a template, or a Pro block disappeared
**Symptom**: Post Grid/Taxonomy blocks display distorted inside a post/loop template, or a block reverted to plain "fallback content."
**Cause**: Wrong query/layout context inside the template, or a Pro-only block losing its Pro feature because Spectra Pro is deactivated/expired.
**Solution**: For distorted post blocks, check the block's query + layout settings and the template context; correct the query with `uagb_post_query_args_*`. For fallback content, reactivate/renew Spectra Pro (the Pro-only styling/feature is gated) and avoid building critical pages solely on Pro blocks.
