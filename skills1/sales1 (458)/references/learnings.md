# ReadySetLaunch Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-05**: Research baseline — platform positioning, the 7 pillars / 13-question Launch Control structure, pricing (credit-based, no subscription; 3 free credits; packs from ~£14.99; credits never expire), and the no-public-API automation reality captured from live sources on this date. Homepage and /pricing are JS-rendered and returned near-empty to WebFetch; the methodology detail (7 pillars, 13 questions, 4 sub-prompts each, gap-surfacing scoring) came from WebSearch snippets and the vendor's own /compare/ideaproof/review/ page. Re-verify exact per-pack credit counts and prices against readysetlaunch.ai/pricing before relying on them — they aren't fully published.

**2026-07-05**: ReadySetLaunch publishes competitor review pages at `/compare/{tool}/review/` (IdeaProof, BuildOrNot, RebeccAi, Informly seen) and a startup case database at `/cases/`. These are vendor content that positions Launch Control favourably — cite as vendor comparison, not a neutral benchmark.
