# Frederick AI Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each
invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-05**: Research baseline — platform positioning ("AI teammates for your startup" / an AI co-founder;
frederick.ai) and the four agent types captured from live sources on this date (frederick.ai homepage,
/ai-cofounder, /pricing, plus SourceForge/Software Finder/AIChief listings and comparison articles): **Coding
Agents** (build/ship landing pages, full-stack apps, APIs, internal tools), **Browser Agents** (navigate,
click, fill forms, extract data), **Background Agents** (scheduled recurring tasks — SEO content, investor
updates, data collection), **Market Insights** (competitor tracking, market analysis, customer signals, social
monitoring on a schedule), and a shared **Editor/workspace** (plans/research/files persisted across sessions).
Work metered in **AI Credits**. Re-verify at frederick.ai.

**2026-07-05**: Distinctive angle vs idea-validation siblings — Frederick **executes** (ships real
apps/pages, automates browsers, runs scheduled research) rather than only generating a report/plan like
aicofounder / SoloLaunch / Foundra. The validation-relevant upside: its **Coding Agent can build the
smoke-test landing page itself** (the one output that yields real demand signal). But **Market Insights is
AI-scanned research, not validated demand** — it reports what's discussed online, not that anyone will pay.
Keep research to sharpen the pitch; take the go/no-go from real behavior ([[sales-idea-validation]]).

**2026-07-05**: No documented public API. Despite building APIs *for* your projects, Frederick exposes **no
public API, webhooks, MCP, or Zapier/Make**. It's a UI workspace — the Background Agent automates work
*within* Frederick (scheduled), not outbound to your stack. Don't design integrations around it; copy outputs
manually or automate the real demand signal (landing-page analytics / waitlist events) instead. Re-check
periodically — an early tool may add an API later.

**2026-07-05**: Pricing sources conflict — homepage/pricing page show Free (15 credits, 1GB, 2 apps, limited
insights) → **Plus ~$25/mo** (~1,000 credits, 10GB, unlimited apps, full insights, recurring background
agents) → **Pro ~$50/mo** (~2,500 credits, 30GB); annual ~24% off. Some third-party listings quote ~$8/$16
with different credit counts — likely stale/promo. Treat ALL figures as best-effort; confirm at
frederick.ai/pricing. Recurring background agents and full Market Insights are gated to paid tiers; the free
tier's 15 credits / 2 apps run out fast.
