# InstantPersonas API Reference

<!-- Source: https://www.instantpersonas.com (homepage + search, research 2026-07) -->

## No public API

As of the 2026-07 research date, **InstantPersonas has no documented public API**, no webhooks, no
Zapier/Make integration, and no MCP server. It is a **UI-only web application**: you enter a product
or audience description in the browser and copy the generated persona/insights out by hand. There is
also **no GitHub org** (`github.com/orgs/instantpersonas` → 404).

Review sites that list "integrations" for InstantPersonas are echoing generic marketing copy — there
is no supported developer surface to build on. Do not attempt to reverse-engineer or scrape internal
endpoints; they are unsupported and may change or break without notice.

## Programmatic surface (what to use instead)

| Need | Supported path |
|---|---|
| Generate one persona | InstantPersonas UI (manual) |
| Batch/scripted persona generation | Call an LLM API directly (e.g. Anthropic `POST /v1/messages`) with a persona prompt — see `platform-guide.md` → "Programmatic persona generation" |
| Export a persona to a CRM/doc | Manual copy-paste from the UI |
| Automate a real demand test around a persona | See `/sales-idea-validation` and `/sales-funnel` |

## Gaps

- **Pricing page not directly fetchable** — `instantpersonas.com/pricing` returned 404 on fetch; pricing
  in `platform-guide.md` is best-effort from the homepage and third-party review sites. Re-verify live.
- **No published data schema** — the JSON persona shape in `platform-guide.md` is constructed from the
  visible product output, not from an API contract. Marked as such.
- **AI model undisclosed** — the underlying model(s) powering persona generation are not published.
