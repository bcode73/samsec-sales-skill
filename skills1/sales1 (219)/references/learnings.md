# Gutenverse Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, block list, `gutenverse-core` framework hooks, the separate Gutenverse Form plugin, pricing, and the WordPress-REST-API automation surface captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-29**: Pricing sources disagree — saw both ~$55/$69 (intro/renewal, single-site) and ~$79/$99 (Professional, ~10 sites), plus an Agency tier ~$199/yr (~100 sites). Treat all Gutenverse pricing as best-effort and confirm on gutenverse.com/pricing.

**2026-06-29**: The form builder is a **separate** free plugin (`gutenverse-form`), not part of the main Gutenverse plugin. Free tier stores entries in WordPress (CSV export) + email notifications + reCAPTCHA only — no webhooks/Zapier/CRM/conditional logic/multi-step/payment (Pro). A third-party `turnstile-for-gutenverse-forms` repo exists, signaling reCAPTCHA-only anti-spam is a real pain point.

**2026-06-29**: Top WordPress.org support pattern is "the editor page won't load after a customization change; frontend still works; deactivating Gutenverse fixes it" — treat as JS conflict/corrupted block, bisect on staging. Second pattern: color/style changes apply in editor but not frontend (styling-cache/asset issue; v3.4.0+ improved the cache mechanism).

**2026-06-29**: WooCommerce blocks, custom fields, and CPT Query Loop were marketed as "coming soon" — do not assume they exist; verify against the current changelog.
