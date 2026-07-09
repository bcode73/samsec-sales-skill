# Superb Addons Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, the WordPress.org listing, pricing, and the form integration/webhook surface captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-29**: The backlog/marketing domain `superbaddons.com` does NOT resolve (DNS ENOTFOUND). The live product is at `superbthemes.com/superb-addons/` and `wordpress.org/plugins/superb-blocks/` (slug `superb-blocks`, developer Suplugins/SuperbThemes). Use those URLs for future research.

**2026-06-29**: Plan-gating is genuinely ambiguous — the WordPress.org readme markets a free form builder ("no license/account needed"), but the SuperbThemes pricing page lists Forms, multi-step forms, Popups (smart triggers), 70+ animations, sliders, Theme Designer, visibility conditions, and advanced custom CSS as Premium. Don't assert free/Premium without checking the live install.

**2026-06-29**: No public hosted REST API and no MCP server. Outbound automation = form webhook + native Mailchimp/Brevo/Google Sheets/Slack. The webhook payload schema is NOT published — capture a live delivery before mapping field keys; no documented HMAC signing.

**2026-06-29**: Top support issue is the **Theme Designer not loading/responding when clicked**. v4.0.5 changelog fixed Theme Designer previews not rendering when **Gutenverse** is active, and fixed saved form submissions not displaying in wp-admin for some permalink configs. First remediation is always: update plugin → run built-in Troubleshooter (Superb Addons → Get Help → Start Troubleshoot Process) → clear caches → deactivate other block plugins to isolate.

**2026-06-29**: No GitHub org found for `suplugins`/`superbthemes` (both 404) — `github:` field intentionally omitted from frontmatter.

**2026-06-29**: SuperbThemes runs an affiliate/partner program (noted to `_internal/affiliates.md`).
