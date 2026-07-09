# Stackable Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, pricing, the `stackable_force_css_load` filter, and integration surface captured from live sources on this date (wpstackable.com homepage/pricing render to WebFetch; GitHub `gambitph/Stackable` README is a landing page with only build/setup steps and no hook list; docs.wpstackable.com "Customizing Blocks" is end-user only). Re-verify specifics against current docs/source before relying on them.

**2026-06-29**: Made by **Gambit Technologies / gambitph** (Benjamin Intal), **GPLv3**, open source at `github.com/gambitph/Stackable`. WordPress.org slug is `stackable-ultimate-gutenberg-blocks`. v3.19.9 (~May 2026), tested to WP 7.0, 100k+ active installs (200k+ sites claimed), 4.9★ — actively maintained.

**2026-06-29**: No hosted REST API and no native webhook — it's a WordPress plugin. Programmatic surface = WP core REST API (block markup is `stackable/`-namespaced in `post_content`) + a thin set of filters. **Only `stackable_force_css_load` is documented verbatim**; the rest is WordPress core (`render_block`). Do NOT invent `stackable_*` hooks — confirm in source.

**2026-06-29**: Blocks = **42** (free) across Essential / Special / Section groups. **Pro gates:** Dynamic Content (ACF/Metabox/JetEngine), Motion Effects/transforms, Conditional Display, Role Manager, per-block Custom CSS, advanced copy-paste, expanded Design Library (375 vs ~107) + more color schemes/presets/font pairs. **No form builder, popup builder, header/footer builder, or WooCommerce blocks** on any tier — the defining limitation vs Spectra/Kadence/aBlocks.

**2026-06-29**: Top complaints — (1) **v2→v3 migration** confusion (v3 was a rewrite; v2 blocks persist as separate blocks gated in Settings → Other Settings → Migration); (2) "blocks not showing in editor" (JS conflict / stale build / v2 loading disabled); (3) major-update regressions needing rollback; (4) styles missing when markup is injected dynamically (fix with `stackable_force_css_load`); (5) plan-gate surprises. Stackable is among the **lightest** block plugins (~10–75KB) — performance is a selling point.

**2026-06-29**: Pricing best-effort/annual with a Lifetime toggle and 1/10/Unlimited site toggle: Free (unlimited sites), **Premium ~$49/yr (1 site)**, **All Access Pass ~$89/yr (1 site)**. 30-day money-back. Multi-site/lifetime exact figures not displayed on the pricing page. Affiliate program: 1 link at wpstackable.com/affiliate/.
