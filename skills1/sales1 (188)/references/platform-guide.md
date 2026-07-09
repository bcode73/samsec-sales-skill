# Frederick AI — Platform Guide

Full reference for the `sales-frederick` skill. Read the section relevant to the user's question; don't dump
the whole file. All pricing/feature details are **best-effort from research (2026-07)** — Frederick is an
early, fast-moving indie AI tool; **confirm live at frederick.ai**.

<!-- Source: https://frederick.ai, https://www.frederick.ai/ai-cofounder, https://www.frederick.ai/pricing (fetched 2026-07-05) -->

## What Frederick is

Frederick AI (**frederick.ai**) positions itself as **"AI teammates for your startup"** / an **AI
co-founder** — a workspace where autonomous agents *do* the work of building and running a startup, from an
idea toward launch. Unlike its idea-validation siblings (aicofounder, SoloLaunch, Foundra) that generate a
report/plan and stop, Frederick's agents **execute**: they ship code, drive browsers, run scheduled research,
and keep shared context. Target audience: **founders and builders** — solo founders, indie hackers/vibe
coders, and small startup teams that want speed and automation without hiring devs.

**Core framing for validation:** Frederick's research modules are informative but they describe what's
*discussed online*, not that anyone will *pay*. The one output that produces real signal is the **landing
page its Coding Agent can build** — pair it with real traffic and read conversions. Keep the research to
sharpen the pitch; take the go/no-go from stranger behavior (see `/sales-idea-validation`).

## The four agent types

| Agent | What it does | API-accessible? | Notes |
|---|---|---|---|
| **Coding Agents** | "Build apps, on demand" — writes, tests, and ships **landing pages, full-stack apps, APIs, and internal tools** end-to-end without a dev team | UI-only (no public API) | The validation-relevant one: it can build the **smoke-test landing page** itself. Runs in a **Coding Sandbox** (limited on the free tier). |
| **Browser Agents** | Autonomously **navigate websites, click buttons, fill forms, and extract data** | UI-only | Runs in a **Browser Sandbox** with **browser session memory** (persists across runs). Limited on free tier. |
| **Background Agents** | Execute **scheduled/recurring tasks** — e.g. SEO content, investor updates, data collection — that "run on a schedule" | UI-only | **Recurring** background agents are **gated to paid tiers**; the free tier allows only one-time background tasks. |
| **Market Insights** (research) | **Competitor tracking, market analysis, customer signals, social monitoring** — scans the web and delivers **structured insights on a schedule** | UI-only | *Limited* on the free tier, *full* on paid. This is research/monitoring, **not validated demand**. |

Supporting surface:

- **Editor / Workspace** — a shared context store holding **plans, research, images, and files**; agents
  "remember everything" and carry context **between tasks and sessions**. Framing a task richly + storing
  context here is the main lever on output quality.
- **Apps** — what users build/deploy (the free tier caps you at **2 apps**).
- **Task statuses** — Running, Done, Scheduled (the scheduling surface for Background Agents).

## AI Credits & pricing (best-effort — confirm at frederick.ai/pricing)

Work is metered in **"AI Credits"** — every agent run (coding, browser, background, insights) draws them
down. Plans bundle a monthly credit allotment + storage + feature gates. **Credit top-ups** are available on
all plans; annual billing is discounted ~**24%**.

| Plan | Price (best-effort) | AI Credits | Storage | Apps | Market Insights | Browser/Coding Sandbox | Background Agents |
|---|---|---|---|---|---|---|---|
| **Free** | $0 (no card) | 15 on sign-up | 1 GB | 2 | Limited | Limited | One-time only (no recurring) |
| **Plus** *(popular)* | ~$25/mo | ~1,000 / mo | 10 GB | Unlimited | Full | Included | Recurring |
| **Pro** | ~$50/mo | ~2,500 / mo | 30 GB | Unlimited | Full | Included | Recurring |

Paid tiers also add **Priority Support** and a **Founders Email**. All plans include private projects, custom
domains, credit top-ups, and browser session memory.

> ⚠️ **Pricing sources conflict.** The homepage/pricing page show ~$25 (Plus) / ~$50 (Pro); some third-party
> listings (SourceForge/Software Finder) quote ~$8 (Plus) / ~$16 (Pro) with different credit counts — likely
> **stale or promotional**. Treat every figure as **best-effort** and tell the user to confirm live. Value
> question = "how many credit-heavy agent runs per month will I do?" against the monthly fee.

## Integrations & API reality

- **No documented public API.** No developer docs, endpoints, or auth flow were found — despite Frederick
  *building* APIs for your projects, it exposes none for itself.
- **No webhooks, no MCP server, no Zapier/Make** connectors found.
- **No native CRM/third-party integrations** surfaced on the marketing site.
- **Automation reality:** the **Background Agent** automates recurring work *inside* Frederick (on a
  schedule), but it is **not an outbound integration surface**. To pull data out, copy from the workspace
  manually. For a validation/GTM pipeline, automate the **real signal** — landing-page analytics, waitlist
  events — with tools built for it, not Frederick's research output.

Re-check periodically: an early tool like this may add an API/MCP later — verify at frederick.ai before
telling a user an integration is impossible long-term.

## Quick-start recipes (best-effort — no API, so these are in-product workflows)

Frederick has **no public API**, so these are UI recipes, not code. The one place code enters is what
Frederick's **Coding Agent builds for you** (e.g. a landing page you then instrument).

### Recipe 1 — Build a smoke-test landing page, then measure real demand
1. In the Editor, write a rich brief: exact customer, the problem, the one promise, and a single CTA ("Join the waitlist" / "Get early access").
2. Ask the **Coding Agent** to build a one-page landing page from that brief; publish on a custom domain.
3. Add an analytics + email-capture snippet to the page (the real signal lives here, not in Frederick's report). A minimal capture instrument you can drop in:

```html
<!-- paste into the page the Coding Agent builds -->
<form onsubmit="capture(event)">
  <input type="email" name="email" required placeholder="you@work.com" />
  <button>Get early access</button>
</form>
<script>
async function capture(e){
  e.preventDefault();
  const email = e.target.email.value;
  // send to your own store / waitlist tool — this action is the demand signal
  await fetch("https://YOUR-WAITLIST-ENDPOINT/subscribe", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({ email, source:"frederick-smoke-test" })
  });
  e.target.reset(); alert("You're on the list!");
}
</script>
```
4. Drive a little targeted traffic (a community post, a small ad budget) and read conversion. A commonly cited bar: **~5%+ of targeted visitors** taking the action = active demand. Route the page strategy to `/sales-funnel` and signups to `/sales-audience-growth`.

### Recipe 2 — Schedule recurring competitor monitoring (Background Agent + Market Insights)
1. Confirm you're on a **paid tier** (recurring background agents are gated).
2. Create a **Background Agent** task: "Every week, run Market Insights on {competitor list / keyword} and summarize new launches, pricing changes, and customer complaints into the workspace."
3. Set the schedule (weekly); results land in the Editor as structured insights.
4. Read it as **monitoring of published signals**, not demand — use it to sharpen positioning, not to decide build-or-not.

### Recipe 3 — Automate a repetitive web task (Browser Agent)
1. Describe the task concretely: "Go to {site}, filter by {criteria}, extract {fields} into a table."
2. The **Browser Agent** navigates, fills forms, and extracts data into the workspace; browser session memory persists logins/context across runs.
3. Watch credit spend — long browser runs consume more **AI Credits**.

## Data model (no API — this is the in-product object shape, illustrative)

Frederick exposes no API/schema publicly. Conceptually the workspace organizes around:

```json
{
  "project": {
    "id": "proj_...",
    "name": "My Startup",
    "apps": [{ "id": "app_...", "type": "landing_page|app|api|internal_tool", "status": "shipped" }],
    "workspace": { "plans": [], "research": [], "files": [], "images": [] }
  },
  "task": {
    "id": "task_...",
    "agent": "coding|browser|background|insights",
    "status": "Running|Done|Scheduled",
    "schedule": "one-time|recurring",
    "credits_spent": 0
  },
  "account": { "plan": "free|plus|pro", "credits_remaining": 15, "storage_gb": 1, "apps_used": 0 }
}
```

Treat this as illustrative (from observed product behavior), **not** a documented contract.

## Framing tips (get better output)

- **Depth in → depth out.** A one-line idea yields generic research/plans/pages; give a specific customer,
  the exact problem, current stage, and how you're different.
- **Use the Editor as memory.** Store plans/research/files so every agent run builds on the last instead of
  starting cold.
- **Treat every output as a draft.** Pages, plans, and reports are editable first drafts — re-run variants
  and compare.
- **Spend credits where they buy real signal.** The highest-value run is the **Coding Agent building the
  smoke-test page**; the research runs are supporting context, not the decision.
