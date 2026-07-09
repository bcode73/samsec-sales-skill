# PersonaGen Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-06**: Research baseline — persona modules, no-API surface, and best-effort pricing captured from third-party sources (futuretools.io, findmyaitool.com, aicenter.ai, toolai.io, creati.ai) on this date. Re-verify specifics against current docs before relying on them.

**2026-07-06**: Live site unreachable during research. The backlog URL `personagen.io` does NOT resolve (getaddrinfo ENOTFOUND); `personagen.app` returned ECONNREFUSED over HTTPS; `personagen.net` also failed to resolve via WebFetch. Canonical domain per most third-party listings is `personagen.app`. Research assembled from third-party sources only — flag pricing/features as best-effort and re-fetch the live site when reachable.

**2026-07-06**: Possible name collision — `personagen.net` markets itself as "PersonaGen - Custom User Personas in minutes," which may be a related/newer domain or a distinct product sharing the name. Confirm which one the user is on before giving pricing.

**2026-07-06**: No public API, no webhooks, no Zapier/Make, no MCP. UI-only. For automation, recommend a direct LLM API call (see platform-guide.md) rather than any PersonaGen integration.
