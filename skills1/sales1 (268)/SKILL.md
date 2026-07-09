---
name: sales-juma
description: "Juma (juma.ai, formerly Team-GPT) platform help — an AI marketing workspace whose standout in the persona/idea-validation cluster is a real MCP server (mcp.juma.ai): 40+ tools that let Claude Code, Claude Desktop, ChatGPT, or Cursor drive brand profiles, project-knowledge search, on-brand content, SEO/GEO audits, campaigns, and buyer-persona generation over OAuth (no API keys). Also a UI workspace: 700+ marketing Flows, shared Projects holding brand voice, and multi-model chat (Claude/GPT/Gemini). Credit-metered — only successful runs charge, MCP reads don't. Use when connecting Juma's MCP server to Claude Code or Cursor, generating a buyer persona from its Prompt Builder, driving content/SEO tools over MCP, understanding the credit model, or migrating from Team-GPT. A generated persona tracks input depth and is not validated demand. Do NOT use for the validate-before-building method or comparing persona/validator tools (use /sales-idea-validation), or tool-agnostic content strategy (use /sales-content)."
argument-hint: "[describe what you need help with in Juma]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
github: "https://github.com/team-gpt"
---

# Juma Platform Help

Juma (**juma.ai**, formerly **Team-GPT**) is an **AI marketing workspace** for marketing teams,
agencies, and solo marketers. Its core is **Flows** (700+ pre-built marketing workflows that run a task
end-to-end), **Projects** (persistent workspaces that hold brand voice, briefs, and client context so
every chat is on-brand), and **multi-model chat** (Claude, GPT-5, Gemini, Perplexity, and more from one
seat). Its distinctive edge for this catalog is twofold: (1) **buyer-persona generation** via a Prompt
Builder is one of its Flows, so it sits in the persona/idea-validation cluster; and (2) it is the **only
tool in that cluster with a real, callable MCP server** (`mcp.juma.ai`) — you can drive its brand,
persona, content, and SEO/GEO tools from **Claude Code, Claude Desktop, ChatGPT, or Cursor** over OAuth.
It's **credit-metered** (only successful runs charge; MCP reads don't) with a full-featured **Free plan**.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from Juma?**
   - A) **Connect the MCP server** to Claude Code / Cursor / Claude Desktop and drive its tools
   - B) **Generate a buyer/user persona** with the Prompt Builder (and judge whether it's any good)
   - C) Run **content / SEO-GEO / campaign** Flows (in the UI or over MCP)
   - D) Understand **pricing / the credit model** (free vs Pro vs Enterprise, what burns credits)
   - E) **Migrate from Team-GPT** / understand what changed in the rebrand
2. **UI or programmatic?** If they want to automate, Juma's programmatic surface is the **MCP server**,
   not a REST API — route the answer accordingly (Step 3 / the api-reference file).
3. **If it's persona/validation:** is the real question "is this a good persona?" or "will anyone buy?"
   A generated persona is an AI hypothesis, not demand — route the go/no-go in Step 2.

Skip-ahead: if the user wants the validate-before-building *method* or to compare persona/validator tools
across the market, route to `/sales-idea-validation` immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| Comparing Juma's persona generator against other persona/validator tools (InstantPersonas, PersonaGen, Personadeck, Marketing Mary, Validator AI…) | `/sales-idea-validation {question}` |
| Tool-agnostic **content-marketing strategy** (calendars, briefs, repurposing across tools) | `/sales-content {question}` |
| Building the smoke-test / fake-door **landing page** to test the persona's audience for real | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer Juma-specific questions using Step 3.

## Step 3 — Juma platform reference

**Read `references/platform-guide.md`** for the full reference — Flows/Projects/multi-model chat, the
persona Prompt-Builder workflow, pricing and the credit model (what burns credits, rollover, only-success
charging), integrations, and how it compares to the persona/validator cluster.

**Read `references/juma-api-reference.md`** for the **MCP server** — the server URL and transport, the
OAuth connect flow, the exact `claude mcp add` command, the full 40+ tool inventory by category, credit
rules, and the three functions that stay in the web app. This file is the programmatic surface; there is
**no documented REST API, no webhooks, and no Zapier/Make** — the MCP server is how you automate Juma.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **When the user wants to automate Juma, point to the MCP server — not a REST API.** Juma's
  programmatic surface is an **MCP server at `https://mcp.juma.ai/mcp`** (HTTP transport, OAuth sign-in,
  **no API keys**). Give the exact Claude Code setup: `claude mcp add --transport http juma "https://mcp.juma.ai/mcp"`,
  then run `/mcp` and complete the browser OAuth (visit `juma.ai/mcp/connect` first if you lack access).
  State plainly there is **no documented REST API, no webhooks, no Zapier/Make** — if they need those,
  the MCP server (from Claude Code/Cursor/ChatGPT) is the supported path, or call an LLM API directly.
- **Explain the credit model FIRST whenever pricing comes up, and frame every figure as best-effort.**
  Juma is **credit-metered, and features are NOT gated by tier** — the **Free plan has full feature
  access** (every Flow, integration, and model), and tiers differ mainly by **credit allowance**: a
  per-user free credit grant; Pro ~$49/mo adds a larger monthly credit pool with **rollover** and
  auto-recharge; Enterprise adds private cloud + SSO/SAML. Two facts that defuse the top complaint: **only successful runs consume credits** (a failed
  Flow charges nothing) and over **MCP, reading knowledge/brand profiles is free — only running agent
  sessions burns credits**. Simple chats/rewrites cost a few credits; full Flows cost more. Point to
  juma.ai/pricing and flag all prices/credit numbers as best-effort.
- **Treat a Juma persona as an editable hypothesis whose quality tracks input depth — not validated
  demand.** The Prompt Builder → follow-up-questions → refined-prompt flow (plus your Project's brand
  context) produces a richer persona than a one-line prompt, but it's still an **AI opinion**: it can
  describe a convincing buyer for an audience that won't pay. Keep the structured outputs (segments,
  pain points, channels, objections) to sharpen messaging; take the go/no-go from **real behavior** — a
  smoke test or pre-sale — routed to `/sales-idea-validation` and `/sales-funnel`.
- **Use Projects for persistent context instead of one long chat.** If a user reports the AI "forgetting"
  mid-conversation, the fix is to put brand voice, briefs, and reference docs into a **Project** (shared,
  reusable across chats and reachable over MCP as knowledge items) rather than pasting everything into a
  single thread that runs out of context.
- **Frame Juma as a broad marketing workspace, not a single-shot persona generator.** Unlike the
  prompt-only persona tools in this cluster (InstantPersonas, PersonaGen, Personadeck), persona is *one*
  Flow among 700+; its real differentiators are the multi-model workspace + Projects + the MCP server.
  For cross-market persona/validator comparison or the validation method, route to `/sales-idea-validation`.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — Juma is a recent rebrand of Team-GPT and community coverage under
the new name is thin; verify pricing, the credit model, and the MCP tool list at juma.ai.*

- **Programmatic access is the MCP server, not a REST API.** There is no documented public REST API, no
  webhooks, and no Zapier/Make. Automate via `mcp.juma.ai` from Claude Code/Cursor/ChatGPT, or call an
  LLM API directly. Don't design an integration around endpoints that don't exist.
- **Credits, not seats — and the model shifted.** Team-GPT was sold on "seats"; Juma is **credit-metered**
  (unlimited seats, a shared credit pool). This surprised legacy AppSumo buyers. Key mitigations to state:
  **only successful runs charge**, credits **roll over** on Pro, and **MCP reads are free** (only agent
  sessions burn credits).
- **A generated persona is not validated demand.** It's an AI hypothesis; output quality tracks input
  depth and it can be confidently wrong. Validate against real customers before building.
- **Long single chats lose context.** Users report the chat "running out of memory." Put durable context
  in a **Project**, don't rely on one ever-growing thread.
- **Three things stay in the web app.** Over MCP you cannot **upload files as knowledge, edit existing
  images, or do workspace administration** — those remain UI-only.
- **MCP tasks have a ~30s wait window.** The connection waits ~30 seconds; longer tasks continue in the
  background with automatic agent check-ins rather than blocking the call.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full persona/validator landscape (use this to actually decide build-or-not; a generated persona is not demand)
- `/sales-instantpersonas` — InstantPersonas platform help (a prompt-only AI persona generator + website-perception insights — contrast Juma, where persona is one Flow in a broader MCP-driven workspace)
- `/sales-personagen` — PersonaGen platform help (a prompt-only user-persona generator organized into projects/feature sections; contrast Juma's multi-model workspace + MCP server)
- `/sales-marketing-mary` — Marketing Mary platform help (a data-grounded, *conversational* persona co-pilot built from your real CRM/analytics data; contrast Juma, whose personas come from a Prompt Builder and whose automation is a real MCP server)
- `/sales-content` — Tool-agnostic content-marketing strategy (calendars, briefs, repurposing) once you've generated the persona and on-brand copy
- `/sales-funnel` — Build the smoke-test / fake-door landing page to test the persona's audience for real
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Connect Juma to Claude Code and generate a persona over MCP (developer/automation)
**User says**: "How do I hook Juma up to Claude Code so I can generate a buyer persona from my terminal?"
**Skill does**: Gives the exact setup — `claude mcp add --transport http juma "https://mcp.juma.ai/mcp"`,
then `/mcp` and browser OAuth (no API keys; visit `juma.ai/mcp/connect` first if access is missing) —
and explains that once connected, Claude Code can call Juma's 40+ tools (e.g. `create_project`,
`search_knowledge_items`, `write_content`, and the brand tools) to produce an on-brand persona.
Clarifies that **reading knowledge/brand profiles is free while running agent sessions burns credits**,
and that a generated persona is a hypothesis to validate, not demand.
**Result**: The user drives Juma from Claude Code and knows what will and won't cost credits.

### Example 2: "Will I run out of credits? I bought Team-GPT on seats."
**User says**: "I got Team-GPT as an AppSumo seat deal — now it's Juma with credits. Am I going to get nickel-and-dimed?"
**Skill does**: Explains the credit model as best-effort: a full-featured **Free plan** with a per-user
credit grant, **Pro (~$49/mo)** with a larger pool that **rolls over** plus auto-recharge, and Enterprise
for private cloud/SSO. Defuses the fear with the two facts that matter — **only successful runs charge**
(failed Flows cost nothing) and simple chats cost a few credits while full end-to-end Flows cost more —
and points to juma.ai/pricing to confirm current numbers.
**Result**: The user understands what consumes credits and stops worrying about surprise charges.

### Example 3: "The persona Juma generated looks generic — is it any good?"
**User says**: "I typed one line and Juma made a persona, but it feels like it could be anyone. Should I trust it?"
**Skill does**: Explains that persona quality **tracks input depth** — a one-line prompt yields a generic
echo, while the Prompt Builder's follow-up questions plus a Project loaded with real brand/customer
context produce something sharper. Stresses that even a good persona is an **AI hypothesis, not validated
demand**: keep the segments/pain points/channels to sharpen messaging, then test the audience for real
with a smoke test or pre-sale, routed to `/sales-idea-validation` and `/sales-funnel`.
**Result**: The user improves the input, keeps the useful structure, and validates before building.

## Troubleshooting

### I want to automate Juma / pull its output via API
**Symptom**: The user wants to script Juma or export content/personas programmatically and is looking for REST endpoints.
**Cause**: Juma has **no documented public REST API, no webhooks, and no Zapier/Make** — its programmatic
surface is an **MCP server** (`https://mcp.juma.ai/mcp`).
**Solution**: Add the MCP server to Claude Code (`claude mcp add --transport http juma "https://mcp.juma.ai/mcp"`),
Cursor, or ChatGPT, authenticate over OAuth, and call the 40+ tools from there. If you truly need a raw
HTTP API, there isn't one — call an LLM API directly for generation, or drive Juma through an MCP client.

### The AI "forgets" earlier in the conversation / runs out of memory
**Symptom**: A long chat loses track of brand voice or earlier instructions and the user has to re-paste context.
**Cause**: A single ever-growing thread exceeds the model's usable context.
**Solution**: Move durable context into a **Project** (brand guidelines, tone-of-voice docs, briefs).
Projects persist across chats, apply automatically, and are reachable over MCP as knowledge items — so you
start each task with the context already loaded instead of re-pasting it.

### I connected the MCP server but a task seems to hang
**Symptom**: A long-running Flow over MCP doesn't return immediately and looks stuck.
**Cause**: The MCP connection **waits ~30 seconds**; longer tasks continue in the **background** with
automatic agent check-ins rather than blocking the call.
**Solution**: Let it run — check back for the completed result rather than assuming failure. Also note
three actions stay in the web app (uploading files as knowledge, editing existing images, workspace admin),
so if one of those is what you're attempting over MCP, do it in the UI.
