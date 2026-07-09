# aicofounder Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of
each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-04**: Research baseline — platform positioning (AI "co-founder" guiding solo founders through
structured idea→launch phases, 90K+ founders), features (multi-agent Reddit/X demand research, idea
validation, competitive analysis, visual product canvas, planning agent, website builder, content
calendar, persistent memory, privacy mode), and best-effort pricing (free ~15 credits/mo no card, first
phases free; paid quoted ~$25/mo vs ~$149 — sources disagree) captured from live sources on this date
(aicofounder.com, foundra.ai comparison, aipure/topai listings). Re-verify at aicofounder.com.

**2026-07-04**: No documented public API. aicofounder is UI-only — agents run in the workspace against
credits. Don't plan integrations around it; automate real demand signals instead.

**2026-07-04**: Its distinctive strength vs pure-LLM validators (Validator AI) is that research is
grounded in real Reddit/X discussions — treat demand signals as genuine evidence, but an AI summary of
discussions is still not a stranger paying you. Confirm the go/no-go with a smoke test / pre-sale
([[sales-idea-validation]]). A generated launch plan is not validated demand.

**2026-07-04**: Output quality tracks input depth — a vague idea/target yields a generic plan. Frame a
concrete customer + exact problem before running the phases. GitHub org exists (github.com/aicofounder).
