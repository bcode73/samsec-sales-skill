# Kadence Blocks Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, hooks/filters, the Advanced Form webhook flow, and pricing captured from live sources on this date (kadencewp.com now 301-redirects to liquidweb.com; plugin is open-source at github.com/stellarwp/kadence-blocks, GPLv2, 600k+ installs). No hosted REST API exists — the automation surface is the WordPress core REST API over block content, PHP hooks/filters (`kadence_blocks_posts_query_args`, `kadence_blocks_pro_query_loop_query_vars`, `kadence_element_display`, `kadence_blocks_table_data_scope_attributes`), and the Pro Advanced Form webhook. Re-verify specifics (especially pricing tiers and filter signatures) against current docs before relying on them.
