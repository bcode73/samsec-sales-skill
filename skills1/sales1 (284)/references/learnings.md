# Landingi Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-28**: Research baseline — platform docs, API surface, pricing, and webhooks captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-28**: Official endpoint-level API docs are partly behind the in-account developer area (API tokens + API Reference, Postman/Insomnia collections, OpenAPI spec per apitracker.io). Public/community sources show conflicting details: base URL is `https://api.landingi.com/v1` with `X-Api-Key` (per the WordPress plugin + Rollout JS guide) AND `https://api.landingi.com/v2/` with OAuth Bearer (per the Rollout OAuth guide); path style appears as both `/landing_pages` and `/landing-pages`. Treat constructed JSON shapes as unverified.

**2026-06-28**: Two auth methods — dashboard **API key** (`X-Api-Key`, server-to-server) and **OAuth 2.0** authorization code grant (`/oauth/authorize`, `/oauth/token`, Bearer, scopes like `read_landing_pages`, for apps acting on other accounts).

**2026-06-28**: Webhooks are **per-form** and fire only on **form submission** (form Settings → Integrations → Webhook). GET or POST, configurable Request URL(s), field mapping, custom headers, and static params. **No published HMAC signature** — authenticate with a custom-header shared secret; pair with `GET /forms/{formId}/submissions` reconciliation since delivery isn't guaranteed.

**2026-06-28**: Plan gates that break integrations — A/B testing / EventTracker / Smart Sections / multi-language need **Optimize ($119/mo)**; programmatic (bulk) landing pages, agency sub-accounts, and the **Orbit MCP server** need **Scale ($229/mo+)**; SSO is **Enterprise**. Each tier caps monthly visits (Build 2,000; Optimize 30,000; Scale 100k–500k).

**2026-06-28**: AI features (Lunar generator, AI copy/SEO) consume a monthly **credit** pool; exhausting it blocks generation until top-up (pay-as-you-go bundles ~$15–$40) or upgrade. Credits reset on the billing cycle.

**2026-06-28**: Top user complaints (G2/review roundups): custom-domain connection is slow and not fully automated (#1), and the visual builder is less freeform than Unbounce/Instapage (advanced layouts often need HTML/CSS). Dynamic Text Replacement (DTR) is praised for PPC ad-to-page message match / Quality Score.

**2026-06-28**: **Orbit MCP server** connects Lunar + Solis to an LLM client — it's the headline AI/programmatic interface but was **in development** at research time. Confirm availability + connection string in-account before building against it.

**2026-06-28**: GitHub org exists (github.com/landingi, Wrocław, Poland) but the 9 public repos are internal PHP/TypeScript libraries (core, ui-kit, event-store-bundle, etc.) — not an API SDK. No official open-source API client found.
