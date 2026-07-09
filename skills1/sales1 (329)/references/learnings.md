# Marketing Mary Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-08**: Research baseline — platform positioning, persona/co-pilot modules, connector list, and best-effort GBP tiers captured from the live site and third-party comparison articles on this date. The product was in **waitlist/pre-release**, so features, tiers (Starter ~£99 / Growth ~£299 / Agency ~£999), seat/persona caps, and the connector list are unconfirmed and likely to change at GA. Re-verify against current docs before relying on specifics.

**2026-07-08**: **No public developer API, no webhooks, and no developer MCP server.** The "Model Context Protocol (MCP) Integration Addendum" in the site footer is a **legal/data-processing document**, not a callable Marketing Mary MCP server — do not treat it as a programmatic interface. Automate through the HubSpot/Salesforce API it bidirectionally syncs to, or a direct LLM API for persona generation.

**2026-07-08**: Distinct from prompt-only persona generators already in the catalog (InstantPersonas, PersonaGen, Personadeck) — Marketing Mary personas are **grounded in live CRM/GA4/email/ad data and conversational**, and it maps ~10-stakeholder B2B buying committees. Core caution (same as the whole idea-validation cluster): "talking to" a synthetic persona is directional input, not validated demand.
