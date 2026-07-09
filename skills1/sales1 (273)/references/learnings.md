# Keap Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-19**: Research baseline — platform docs, API surface (REST v1/v2, OAuth 2.0 + Personal Access Tokens + Service Account Keys), REST Hooks/webhooks, rate limits, and pricing captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-19**: The official interactive REST docs (Stoplight at `developer.infusionsoft.com/docs/restv2/` and `/docs/rest/`) are JS-rendered — WebFetch returns only the nav shell, not endpoint specs. Endpoint detail in `keap-api-reference.md` is assembled from the OAuth getting-started page, the REST Hook documentation page (both fetchable), and reputable third-party guides (Rollout, AeroLeads). Re-verify exact paths/fields against the live interactive docs.

**2026-06-19**: Two products share the "Keap" name — Max Classic (legacy Infusionsoft engine) and the newer Keap (Pro/Max/Ultimate UI). Campaign Builder, reporting, and some API fields differ. Always confirm which interface the user is on before giving steps. The "Ultimate" UI rollout (2024) introduced bugs where automation action options were missing/mislabeled; the workaround is to toggle back to Max Classic.

**2026-06-19**: Deliverability enforcement is unusually aggressive — a Reddit report cited an account blocked after ~13 complaints across ~73,000 emails, and Keap counts unsubscribe-with-feedback ("too frequent") as a complaint. Suppress unengaged contacts before broadcasting.

**2026-06-19**: Pricing scales with contact count (per-contact model), which is the most common cost complaint vs flat-rate competitors like GoHighLevel. ~56% of Capterra reviewers call it "too expensive."

**2026-06-19**: Affiliate program — 20% recurring commission for one year + ~$250/qualifying sale, 90-day cookie, via the Partnerize network. Logged to `_internal/affiliates.md`.
