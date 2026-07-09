# VenturusAI Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-05**: Research baseline — platform overview, framework set (SWOT/PESTEL/Porter's Five Forces/VRIO), report depths (Standard vs Advanced), pricing tiers (Starter/Lite/Pro/Enterprise with reports-per-month and character limits), and the API reality captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-07-05**: API is Enterprise-plan-gated but **undocumented** — `api.venturusai.com` sits behind auth (`/users/sign_in`) and redirects to the homepage; no public API reference, webhooks, Zapier, Make, or MCP server found. Treat as unusable for a DIY integration; direct Enterprise users to VenturusAI support for credentials/docs.

**2026-07-05**: Pure-LLM validator (GPT-3.5/4 class per third-party reviews) with **no source citations** — the opposite of Preuve/DimeADozen. Every number (score, TAM/SAM/SOM, financials) is model-generated. Scores skew encouraging.

**2026-07-05**: #1 user complaint is **generic output**, traced to thin one-line inputs made worse by the free tier's ~1,000-char cap. Coaching a rich input + using paid tiers' higher character limits (Pro ~10,000) is the main quality lever. Secondary complaint: slow loading.

**2026-07-05**: Pricing varies between third-party sources (some report an "Agency"/higher tier or a $20 Pro); the venturusai.com/plans page is authoritative. Present all tier figures as best-effort.
