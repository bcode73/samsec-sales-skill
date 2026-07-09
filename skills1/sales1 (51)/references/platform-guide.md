# BetaList Platform Guide

## How BetaList works

BetaList is an editorially curated directory for pre-launch and recently launched startups. Key mechanics:

**Submission process:**
1. Go to betalist.com/submit and fill out the form: startup name, URL, tagline, description, category, screenshots/GIFs
2. BetaList reviews your submission against acceptance criteria
3. If accepted, your startup is featured on the homepage for 24 hours and included in the daily newsletter
4. If rejected, no specific feedback is provided — improve and resubmit

**Two submission paths:**

| Path | Cost | Review time | Newsletter | Queue |
|---|---|---|---|---|
| Free | $0 | "Up to a few weeks" to get reviewed; "about two months to get featured" | Not guaranteed — only most popular included | Yes (~2 months) |
| Priority | $129 | Reviewed "within a few days," featured shortly after | Guaranteed — expedited reviews always included | Skip the queue |

**Review timing (official, betalist.com/support + /faq, verified 2026-06-13):** Regular submissions — "It can take up to a few weeks to get reviewed" and "it typically takes about two months to get featured, though this can vary depending on our queue." Priority/expedited — "your submission will be reviewed within a few days and, if accepted, featured shortly after."

**Newsletter inclusion (official, verified 2026-06-13):** "Expedited reviews will always be included in the newsletter. For regular submissions, the newsletter does not include all featured startups, but only the most popular ones." So a free listing being featured does NOT guarantee a newsletter slot — only Priority does.

**Refunds (official, verified 2026-06-13):** "If your startup is not selected, you will receive a full refund automatically." Allow "5–10 business days for the refund to appear on your statement." Once featured, "refunds are not available."

> Pricing note: The $129 Priority figure is from third-party reports and the skill's research baseline; it is NOT displayed on BetaList's public pages (the price appears only inside the authenticated submit flow). Third-party sources in 2026 cite $99, $129, and a higher $299 "funded" tier. Treat the exact dollar amount as approximate and reconfirm at submit time.

## Acceptance criteria

BetaList has a 21% acceptance rate (15,000 featured from 70,000+ submissions). They prioritize:

| Criterion | What they look for |
|---|---|
| Value proposition | Clear, distinct — what problem does it solve? |
| Novelty | Innovative idea, not a clone of existing products |
| Design quality | Well-designed landing page, professional appearance |
| Stage | Pre-launch or recently launched (not established products) |
| Domain | Own domain required — no free hosting subdomains (e.g., no .herokuapp.com) |
| Exclusivity | Not already launched on Product Hunt or other major platforms |

**What gets rejected:**
- Products that are already well-established or widely known
- Landing pages with no clear value proposition
- Poor design quality or broken pages
- Free subdomain hosting
- Products already featured on other major launch platforms

## Platform data model

| Concept | Description |
|---|---|
| Startup | A featured listing with name, URL, tagline, description, category, screenshots |
| Category | Topic classification (SaaS, AI Tools, Developer Tools, Analytics, etc.) |
| Newsletter | Daily digest sent to 30K+ subscribers featuring new startups |
| Trending | Highlighted startups getting the most attention |
| Early adopter | Registered user browsing for new products to try |

## Who uses BetaList

- **Founders submitting**: Pre-launch startups wanting beta testers, early feedback, and a DR67 dofollow backlink
- **Early adopters browsing**: 100,000+ registered users actively seeking new products
- **Audience composition**: Shifted toward makers/builders rather than mainstream consumers (especially post-2016)

## Pricing

| Tier | Cost | What you get |
|---|---|---|
| Free | $0 | Submission enters review queue (~2 month wait), featured on homepage + newsletter if accepted |
| Priority | $129 | Skip queue, reviewed within days, guaranteed newsletter inclusion if accepted, full refund if rejected |

## Backlink value

| Metric | Value |
|---|---|
| Domain | betalist.com |
| DR | 67 |
| Dofollow | Yes |
| Traffic | ~250,000 page views/mo |
| Cost for backlink | Free (if accepted through queue) or $129 (Priority) |

## API access

BetaList offers API access on a case-by-case basis (verified 2026-06-13 via betalist.com/support):
- Email api@betalist.com with: intended use, use case description, estimated request volume
- Each request is reviewed individually; if approved, you receive an API key and access to documentation
- No public API documentation, base URL, auth scheme, endpoints, rate limits, or webhooks are published
- A `betalist-ruby` "client library for BetaList API" exists at github.com/betalist/betalist-ruby, but its README still reads "Ruby bindings for the upcoming BetaList API" and it was last updated in 2014 — treat it as a stub, not a usable/documented surface

## Related ecosystem

BetaList operates alongside other properties by the same founder:
- **Startup Jobs** — job listings for startups
- **AI Jobs** — AI-specific job board
- **Web3 Jobs** — Web3 job board
- **WIP** — Work in Progress community for makers
