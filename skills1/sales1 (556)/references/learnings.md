# Spectra Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, public hooks/filters, pricing, and integration surface captured from live sources on this date (wpspectra.com homepage/pricing are JS-rendered/truncated to WebFetch; research assembled from WordPress.org plugin page, GitHub `brainstormforce/wp-spectra`, the official docs hooks page, and review/comparison articles). Re-verify specifics against current docs before relying on them.

**2026-06-29**: Spectra was formerly **Ultimate Addons for Gutenberg (UAG)** — its WordPress.org slug is still `ultimate-addons-for-gutenberg`, hooks/CSS classes use the `uagb_`/`wp-block-uagb-` prefix, and the `UAGB_*` PHP classes persist. Newer hooks use `spectra_`.
**2026-06-29**: No hosted REST API and no native webhook — it's a WordPress plugin. Programmatic surface = WP core REST API + Spectra's PHP actions/filters. The `spectra_pro_rest_api_get_controllers` filter (Spectra Pro v2 only) is the way to add a custom REST controller.
**2026-06-29**: Top user complaints — (1) editor backend slowness/freezing on long posts with Spectra Pro; (2) Spectra CSS not loading on non-homepage pages (regenerate assets + CSS file-generation setting); (3) Post Grid/Taxonomy blocks distorted in templates; (4) Pro blocks fall back to fallback content when Pro is deactivated/expired; (5) Spectra+Astra update conflict (WP Trac #62481).
**2026-06-29**: Pricing is annual + intro-priced and varies by source; lifetime deals exist (~$199/$399/$599). Toolkit bundles (Essential/Business) add Astra Pro and other Brainstorm Force products — flag this when a user thinks they're only buying Spectra. Affiliate program: 50% commission, 60-day cookie, wpspectra.com/affiliate/.
