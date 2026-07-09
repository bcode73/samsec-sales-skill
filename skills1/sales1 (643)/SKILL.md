---
name: sales-venturevault
description: "VentureVault (venturevault.space) platform help — a free IdeaBrowser alternative: a browsable vault of AI-scored, pre-researched startup ideas (market analysis, opportunity scores, revenue/execution/go-to-market signals) for indie hackers, makers, and first-time founders hunting for something to build. 100% free forever, no credit card; a web app plus iOS/Android apps, open-source on GitHub. Use when browsing VentureVault's idea vault to find a niche worth building, interpreting its opportunity scores and market analysis, comparing it to the paid IdeaBrowser, asking whether it has an API to export the ideas, or judging whether a browsable idea equals validated demand. UI-only, NO public API/webhooks/Zapier/MCP; the GitHub repo is the app source, not a data API. Do NOT use for the tool-agnostic validate-before-building method or comparing idea validators across the market (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in VentureVault]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
github: "https://github.com/Stevekaplanai/venturevault"
---

# VentureVault Platform Help

VentureVault (**venturevault.space** — the canonical domain; `venturevault.co` is a dead skeleton and
there are unrelated "Venture Vault" namesakes) is a **free IdeaBrowser alternative**: a browsable
**vault of AI-scored, pre-researched startup ideas**. Each idea entry comes with AI-powered market
analysis and **opportunity scores** (revenue potential, execution difficulty, go-to-market signals,
community interest) so you can **discover → analyze → launch** something worth building. It's **100%
free forever, no credit card** — a web app plus native iOS/Android apps, open-source on GitHub. It's an
**idea-discovery / research tool**, not proof of demand, and it has **no public API** (a UI app; the
GitHub repo is the app's own source, not a data API).

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from VentureVault?**
   - A) **Browse the vault** to find a niche / idea worth building
   - B) **Interpret an idea's opportunity score** and market analysis
   - C) Compare it to the **paid IdeaBrowser** (or other free alternatives)
   - D) Get the ideas out / automate them (export / API reality)
   - E) Judge whether a **browsable idea = validated demand**
2. **What's the real question — "what should I build / is this idea worth building?" or "how do I use
   this tool?"** If it's the go/no-go decision, that's `/sales-idea-validation` (browsing a curated idea
   list and reading an AI score are not demand) — route in Step 2.

Skip-ahead: if the user wants the validate-before-building *method* or to compare validators across the
market, that's a `/sales-idea-validation` question — route immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| Comparing VentureVault against other validators/discovery tools (BuildOrNot, IdeaBrowser, Validator AI…) | `/sales-idea-validation {question}` |
| Deep **Reddit demand-signal** discovery / scoring as its own workflow | `/sales-trendseeker {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer VentureVault-specific questions using Step 3.

## Step 3 — VentureVault platform reference

**Read `references/platform-guide.md`** for the full reference — what the vault contains and how ideas
are scored (opportunity score components, market analysis, community signals — mirroring IdeaBrowser's
model), the **100% free, no-tier** pricing, the no-public-API automation reality (no API/webhooks/
Zapier/MCP; the GitHub repo is the app source, not a data API), the iOS/Android apps, and the
domain/namesake disambiguation.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Use VentureVault for discovery, not for the decision.** Its value is a **curated shortlist** of
  pre-researched ideas with market context — use it to find candidate niches and see what a scored idea
  looks like, then take the go/no-go from a real demand test (smoke test / pre-sale), not from browsing
  the vault. Route the real test to `/sales-idea-validation`.
- **Treat the opportunity scores and market analysis as AI estimates, not facts.** The scores (revenue
  potential, execution difficulty, go-to-market, community interest) are **AI-generated**, not audited —
  tell the user to read them as a directional lens and **verify any market-size or revenue number
  against a primary source** before acting on it. A high opportunity score is not demand; a browsable
  idea has been *researched*, not *validated by a paying stranger*.
- **Frame it against the paid IdeaBrowser honestly.** VentureVault positions itself as the **free
  IdeaBrowser alternative** — same "browse pre-researched, scored ideas" shape, at no cost. Note the
  tradeoff for the user: IdeaBrowser is the established paid product (daily curated idea + deeper
  research agent); VentureVault is a **solo-maker free clone**, so present its idea depth, freshness, and
  catalog size as **best-effort / verify on the live site**, not guaranteed parity.
- **Present pricing as free-but-verify.** VentureVault advertises **100% free forever, no credit card**,
  with **no paid tier** — tell the user to still confirm on venturevault.space, since a solo free
  project's model can change.
- **There's no public API — don't plan an integration around it.** If asked to export or automate, say
  plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP** — it's a UI web/
  mobile app on a Supabase backend, and the `github.com/Stevekaplanai/venturevault` repo is the **app's
  own source, not a consumer data API**. Give the workable fallbacks: (1) **copy the ideas you can see**
  into your own store (mind their terms), and (2) **pull the underlying signals from source** (Reddit's
  API, Product Hunt, each niche's own pages) if you need it scripted. The thing worth automating is a
  real demand signal (landing-page conversions), not a directory.
- **Get the domain right.** The working product is **venturevault.space** (or the iOS/Android apps);
  `venturevault.co` renders empty, and "Venture Vault" also names an unrelated VC fund, a funding
  marketplace, and a think tank — point the user at the right one.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — VentureVault is a young, solo-maker free tool with little public
review coverage and a JS-rendered site; verify pricing, catalog size, and scoring specifics at
venturevault.space.*

- **A browsable, scored idea is not validated demand.** The vault gives you a *researched* idea with an
  AI opportunity score — not proof anyone will pay. Follow it with a real-behavior test (smoke test /
  pre-sale); the go/no-go is a stranger taking an action.
- **Opportunity scores and market analysis are AI estimates.** Revenue potential, execution difficulty,
  GTM and community signals are model-generated, not audited — verify any number against a primary source.
- **It's a free IdeaBrowser clone — treat parity as unproven.** Positioned as the "free IdeaBrowser
  alternative," but catalog depth, idea freshness, and research quality are **best-effort**; don't
  promise it matches the paid original.
- **100% free, no paid tier — but confirm.** Advertised free forever, no credit card; a solo free
  project's model can change, so re-check the live site.
- **No public API, no webhooks, no Zapier/Make/MCP.** UI web + iOS/Android app on Supabase; the GitHub
  repo is the app source, **not** a data API. You can't script or batch-export the ideas.
- **Domain / namesake confusion.** Use **venturevault.space** (`.co` is a dead skeleton). "Venture
  Vault" also names an unrelated VC fund (venturevault.vc), a funding marketplace, and a think tank.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full validator/discovery landscape (use this to actually decide build-or-not; browsing a scored idea list is not demand)
- `/sales-buildornot` — BuildOrNot platform help (the closest analog — a startup-idea discovery data platform + free AI evaluator; a paid-tier discovery sibling to VentureVault's free vault)
- `/sales-trendseeker` — Reddit-based demand discovery + evidence scoring (a real-signal sibling to a curated idea vault)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "I don't have an idea yet — can VentureVault help me find one?"
**User says**: "I want to build a SaaS but have no idea what. Is VentureVault good for finding one?"
**Skill does**: Positions VentureVault as a **discovery** tool — point the user at the vault of
pre-researched, AI-scored ideas to build a shortlist of candidate niches, while explaining the
opportunity scores (revenue potential, execution difficulty, GTM, community interest) are AI estimates
to sanity-check, not facts. Then insists the go/no-go comes from a real demand test, routing the
decision to `/sales-idea-validation` and deeper Reddit signal to `/sales-trendseeker`.
**Result**: The user gets a curated shortlist to research, not a false sense that a vault entry equals demand.

### Example 2: "VentureVault vs the paid IdeaBrowser — is the free one good enough?"
**User says**: "IdeaBrowser costs money. Is VentureVault a real free replacement?"
**Skill does**: Frames VentureVault as the **free IdeaBrowser alternative** with the same browse-scored-
ideas shape at no cost, but flags it's a **solo-maker free clone** — so idea depth, freshness, and
catalog size are best-effort and unproven vs the established paid product. Recommends trying the free
vault for a shortlist, verifying specifics on venturevault.space, and — either way — earning the real
signal with a smoke test rather than trusting any catalog's scores.
**Result**: The founder chooses with clear eyes on the free-vs-paid tradeoff and doesn't over-trust the scores.

### Example 3: Can I export VentureVault's ideas via an API? (developer/automation)
**User says**: "I want to pull VentureVault's scored ideas into my own database via API."
**Skill does**: States plainly there's **no documented public API, no webhooks, no Zapier/Make, no MCP**
— it's a UI web/mobile app on a Supabase backend, and the `github.com/Stevekaplanai/venturevault` repo
is the **app's own source, not a consumer data API** — so there's no supported way to export
programmatically. Suggests the fallbacks: copy the ideas you can see into your own store (mind their
terms), or pull the underlying signals from source (Reddit API, Product Hunt, each niche's own pages).
**Result**: The user avoids building on a non-existent API and picks a workable path to the signal.

## Troubleshooting

### The opportunity scores feel optimistic / every idea looks good
**Symptom**: The vault's scores make most ideas look promising.
**Cause**: The scores and market analysis are **AI-generated estimates**, not audited data — they read
directional and can skew encouraging.
**Solution**: Use the scores to *rank and shortlist*, not to decide. Verify any market/revenue number
against a primary source, then run a real demand test (smoke test / pre-sale) via `/sales-idea-validation`.

### I want an API or a way to export/automate the ideas
**Symptom**: Want to script VentureVault or pull its scored ideas into another system.
**Cause**: VentureVault has no documented public API, webhooks, or iPaaS connectors; it's a UI web +
iOS/Android app on Supabase, and its GitHub repo is the app source, not a developer data API.
**Solution**: Copy the visible ideas into your own store (mind their terms), or pull the underlying
signals from source (Reddit API, Product Hunt, each niche's page). Automate a real demand signal
(landing-page analytics) instead. See `/sales-idea-validation`.

### I can't reach the site / not sure which "Venture Vault" this is
**Symptom**: venturevault.co looks empty, or search surfaces a VC fund and a funding marketplace.
**Cause**: The working product is **venturevault.space** (the `.co` domain renders a blank skeleton),
and several unrelated companies share the "Venture Vault" name (a VC fund at venturevault.vc, a funding
marketplace, a think tank).
**Solution**: Use **venturevault.space** or the iOS/Android apps. If you need the source, it's
`github.com/Stevekaplanai/venturevault` — but that's the app code, not a data feed.
