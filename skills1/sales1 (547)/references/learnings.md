# SoloLaunch Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each
invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-05**: Research baseline — platform positioning (AI startup builder / co-pilot for solo founders,
"transform any startup idea into a complete startup foundation"), the generator lineup (company names,
taglines, logo/brand identity, market analysis, interactive timeline/roadmap, marketing strategy playbooks,
multi-project workspace/canvas), and the subscription pricing (free Starter: ~3 name gens/24h, 1 tagline,
watermarked logo → Pro Launch ~$4.99/mo or ~$44.99/yr, best-effort/promo pricing) captured from live
sources on this date (sololaunch.app, SourceForge/Slashdot listings, comparison articles). Re-verify at sololaunch.app.

**2026-07-05**: Domain collision — the co-pilot is **sololaunch.app**; **sololaunch.ai** is a *different*
product: an AI-app launch directory ("Where solo builders launch AI apps" — free listing, upvotes, weekly
newsletter). The backlog row listed the .ai URL but described the .app co-pilot. Route directory questions
to [[sales-launch-directory]]; sololaunch.ai queued to the platforms backlog as its own skill.

**2026-07-05**: No documented public API. SoloLaunch (.app) is UI-only — generators run in the browser off
the idea you enter. Don't plan integrations around it; automate real demand signals instead.

**2026-07-05**: Pricing differentiator vs siblings — SoloLaunch is a **monthly subscription**, unlike
FounderPal (one-time/lifetime) or IdeaProof/ReadySetLaunch (credit packs that never expire). A generated
"startup foundation" (names/logo/timeline/strategy) is NOT validated demand; pair it with a real demand
test ([[sales-idea-validation]]). Output quality tracks input depth — thin idea → generic output.
