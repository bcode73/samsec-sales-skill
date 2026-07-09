# GutenKit Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, block/module list, pricing, and the WordPress-REST-API automation surface captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-29**: The backlog URL `gutenkit.com` is dead (DNS NXDOMAIN). The live site is **wpgutenkit.com** (and `wpmet.com/plugin/gutenkit/` 301-redirects there). WordPress.org slug is `gutenkit-blocks-addon`. Maker is **Wpmet** (ElementsKit/ShopEngine/MetForm); author Ataur R. No `wpmet` GitHub org found (404) — distribution is via WordPress.org.

**2026-06-29**: Pricing sources disagree. Best-effort current tiers (wpdiscounts, 2026): Yearly Personal/1-site ~$39, Professional/5-site ~$79, Agency/unlimited ~$149; Lifetime ~$89/$189/$389. An earlier early-bird read showed $59/5 · $89/10 · $179/unlimited. Free version on WordPress.org. Treat all pricing as best-effort and confirm on wpgutenkit.com/pricing.

**2026-06-29**: Free-vs-Pro split is fuzzy across reviews — free block counts cited from ~33 to ~50, Pro ~50 to ~65; modules 8–20+; templates 400–900+. Confirmed Pro gates: **Mega Menu, Query Loop Builder, Dynamic Content, Display Conditions, One Page Scroll, Sticky Content, Glass Morphism, Advanced Tooltip, Google Map, advanced Parallax, Price Menu.** Don't promise a specific free count without checking the live matrix.

**2026-06-29**: Top WordPress.org support pattern is the generic Gutenberg-block failure: "this block has encountered an error and cannot be previewed" / editor won't load after a customization change or update; frontend still renders; deactivating GutenKit fixes it — treat as JS conflict / corrupted block / stale build, bisect on staging.

**2026-06-29**: GutenKit-specific gotcha: a `gutenkit-template-library` error surfaces **inside ElementsKit Lite** (both Wpmet plugins share a template-library handler). Keep both plugins on matched current versions + clear cache; deactivate one to isolate. Saw a WordPress.org support thread "ERROR gutenkit-template-library in ElementsKit Lite."

**2026-06-29**: Lead capture is thin — GutenKit ships only a **Mailchimp opt-in block**, no full form builder, no webhooks/Zapier, no stored entries. For CRM routing / conditional / multi-step / payment fields, pair a dedicated form plugin and route via /sales-email-marketing.

**2026-06-29**: Automation surface mirrors the other Gutenberg block plugins (Gutenverse/Spectra/etc.) — no hosted API/webhook; use the WordPress core REST API on `gutenkit/`-namespaced block markup in `post_content`, and `render_block` for output tweaks. Block namespace/attributes (`gutenkit/`, `blockId`) are representative — confirm against live saved markup / block.json.
