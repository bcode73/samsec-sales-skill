# FounderPal Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of
each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-04**: Research baseline — platform positioning (AI marketing tools for "solopreneurs who hate
marketing," by Dan Kulkov), the ~8 free single-purpose generators (marketing strategy, buyer/user
persona, value proposition, business model, idea validator, ad copy, pricing, action plan), and the
paid one-time/lifetime Marketing Strategy product (best-effort: ~$69 per strategy / ~$199 unlimited-
lifetime / Idea·Founder·Agency plans / newer annual credits pass — sources disagree) captured from
live sources on this date (founderpal.ai, uneed.best review, third-party listings). Homepage is
JS-rendered/near-empty to WebFetch — research assembled from review articles. Re-verify at founderpal.ai.

**2026-07-04**: No documented public API. FounderPal is UI-only — the generators run in the browser off
a product profile the user enters. Don't plan integrations around it; automate real demand signals instead.

**2026-07-04**: Output quality tracks input depth — the whole edge over generic ChatGPT is
personalization to a detailed product profile. Thin input → generic output. A generated marketing
strategy is NOT validated demand; pair it with a real demand test ([[sales-idea-validation]]).

**2026-07-04**: Pricing is one-time / lifetime (not a subscription) and inconsistent across third-party
sources — always present as best-effort and tell the user to confirm on founderpal.ai. Many generators
are free; start there.
