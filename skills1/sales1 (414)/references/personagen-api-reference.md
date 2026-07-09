# PersonaGen API Reference

<!-- Source: personagen.app (live site unreachable at research 2026-07); no API docs located across
futuretools.io, findmyaitool.com, aicenter.ai, toolai.io, creati.ai -->

## No public API

PersonaGen has **no documented public API**. As of research (2026-07):

- **No REST/GraphQL API** — no developer docs, no auth scheme, no base URL.
- **No webhooks** — no event notifications for generated personas.
- **No Zapier / Make / iPaaS modules** — no triggers or actions.
- **No MCP server.**

It is a **UI-only web app**: you answer questions in the browser and copy the generated persona and
content prompts out by hand. There is no supported programmatic or batch interface.

## If you need automation (workaround)

Because there is no API, do **not** build an integration against PersonaGen. For programmatic or
batch persona generation, call an LLM API directly with your own prompt — this produces the same class
of output and is scriptable. See `platform-guide.md` → "Programmatic persona generation" for working
cURL and Python examples using the Anthropic API.

## Gaps

- Live site (personagen.app) was unreachable at research (ECONNREFUSED); the backlog URL
  `personagen.io` does not resolve. If PersonaGen later ships an API, re-verify this file against the
  live docs.
- Exact pricing tiers and any per-plan persona limits were not fetchable — see `platform-guide.md` for
  best-effort notes.
