# VentureVault Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-07**: Research baseline — platform positioning, pricing (100% free, no tier), the no-public-API reality, and the domain/namesake facts captured from live sources on this date. The homepage and pricing pages are JS-rendered SPAs that did not return content to automated fetches; details were assembled from search snippets, the GitHub repo metadata (`github.com/Stevekaplanai/venturevault`, TypeScript/Vite + Supabase + Capacitor, homepage `venturevault.space`, actively pushed), and the IdeaBrowser model VentureVault clones. Re-verify catalog size, scoring rubric specifics, and idea-freshness cadence against current docs before relying on them.

**2026-07-07**: Canonical domain is **venturevault.space** (GitHub `homepage` field), NOT `venturevault.co` — the `.co` domain listed in the intake backlog renders a blank skeleton and appears defunct/parked. Many unrelated "Venture Vault" namesakes exist (VC fund venturevault.vc, funding marketplace venturevaultnetwork.com, think tank venturesvault.com) — always confirm the user means the startup-idea vault.

**2026-07-07**: Closest cataloged analog is `/sales-buildornot` (idea-discovery data platform + AI evaluator). Key difference: VentureVault is a **free IdeaBrowser clone** (curated, AI-scored idea entries) with **no paid tier**, native iOS/Android apps, and a **public, open-source maker** — contrast with BuildOrNot's paid preview-gated datasets and anonymous founder. Both share the core caveat: a browsable/scored idea is not validated demand, and neither has a public API.
