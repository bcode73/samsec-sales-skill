# SeedProd Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, the Abilities API surface (8 named actions, WP 6.9 + SeedProd 6.20.0+), permission filters, shortcodes, pricing tiers (Basic $79 / Plus $199 / Pro $399 / Elite $599, annual intro-priced), and plan gates (Theme Builder = Plus+, Zapier + Dynamic Text = Pro+, WooCommerce + Domain Mapping = Elite) captured from live sources on this date. SeedProd is a closed-source WordPress plugin (free version on WordPress.org SVN; no public GitHub org). No public outbound REST API or native webhook — lead data exits via ESP/Zapier. Top user pain: coming-soon/maintenance mode locking the whole site even after deactivation. Re-verify specifics against current docs before relying on them.
