# Personadeck Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-06**: Research baseline — persona-type choice (User vs Negative), persona field set, personality-trait predictions, multilingual/PDF-only surface, and best-effort EUR pricing captured from third-party sources (capterra.com, appsumo.com/products/personadeck, getapp.com, softwarefinder.com, creati.ai) on this date. Re-verify specifics against the live site before relying on them.

**2026-07-06**: Homepage `personadeck.io` returned HTTP 404 (redirects/serves the app at `app.personadeck.io`); the app pricing page `app.personadeck.io/en/pricing` returned HTTP 503 at research. Data assembled from third-party listings — flag pricing/features as best-effort and re-fetch the live site when reachable.

**2026-07-06**: No public API, no webhooks, no Zapier/Make, no MCP. UI-only, with **PDF-only export** (persona is static, cannot be embedded elsewhere — a real reviewer complaint). For automation, recommend a direct LLM API call (see platform-guide.md) rather than any Personadeck integration.

**2026-07-06**: Top reviewer complaint (Capterra, ~3.8/5): the tool can "repackage" thin input without adding actionable insight ("half-pregnant solution"). Coach users hard on input depth + re-running variants; this is the #1 quality lever.

**2026-07-06**: Distinguishing feature vs sibling prompt-only generators (PersonaGen, InstantPersonas): the explicit **persona-type selector** — User Persona vs **Negative Persona** — plus personality-trait axes (practical-vs-emotional, introvert-vs-extrovert) and a multilingual UI (EN/FR/DE/ES). Pricing is in **EUR** and there's an AppSumo lifetime deal.
