# Changelog

All material changes to the *Sales Blueprint* manuscript and repository are recorded here, most recent first. This is a production changelog, not a marketing one: every entry should let a reviewer understand exactly what changed and why without opening the diff.

Format: `## [Date] Phase: Summary`, followed by a short bullet list of changes.

---

## [Unreleased] Phase 9: Module 7 (Present the Offer)

- Module 6 approved and marked Final, along with Figure 6.1.
- Drafted Module 7, "Present the Offer," continuing the Bramble Analytics deal. One recommended package replaces Priya's old three-tier menu, with an explicit "what's included / what's a variation" boundary answering the overrun concern raised in Modules 2 and 4, and a specific dated next step replacing an open-ended close.
- Added Figure 7.1 (the Offer Builder), Figure 7.2 (the Pricing Ladder), and Worksheet 7 (offer builder).
- Self-reviewed against the Humanizer Pass and checked for continuity against Modules 1-6.

## [Unreleased] Phase 8: Module 6 (Establish Value)

- Module 5 approved and marked Final, along with Figure 5.1.
- Drafted Module 6, "Establish Value," continuing the Bramble Analytics deal. Priya replaces her old generic design pitch with a three-item value stack built entirely from Dominic's own numbers and language: recovered focus time, avoided cost of a full office expansion, and improved in-office attendance.
- Added Figure 6.1, the Value Stack, and Worksheet 6, value stack builder.
- Self-reviewed against the Humanizer Pass and checked for continuity against Modules 1-5.

## [Unreleased] Phase 7: Module 5 (Understand the Problem)

- Module 4 approved and marked Final, along with Figure 4.1.
- Drafted Module 5, "Understand the Problem," continuing the Bramble Analytics deal. Dominic's stated symptom ("we've outgrown this office") is diagnosed down to the real cause: fixed office space that doesn't flex to attendance that varies by roughly 40 per cent between the busiest and quietest days.
- Added Figure 5.1, the Buying Psychology Wheel, and Worksheet 5, problem diagnosis.
- Self-reviewed against the Humanizer Pass and checked for continuity against Modules 1-4.

## [Unreleased] Phase 6: Module 4 (Learn the Customer)

- Module 3 approved and marked Final, along with Figure 3.1.
- Drafted Module 4, "Learn the Customer," continuing the same Bramble Analytics deal from Module 3 rather than introducing a new example. Priya asks Dominic direct discovery questions now that trust is established, surfacing the full buying committee (Dominic and his co-founder Marguerite) before it can blindside her the way Neil and Farah did in Module 2.
- Added Figure 4.1, the Customer Journey, and Worksheet 4, discovery questions.
- Self-reviewed against the Humanizer Pass and checked for continuity against Modules 1-3.

## [Unreleased] Phase 5: Module 3 (Build Trust)

- Part One approved; Modules 1 and 2 marked Final in `PROJECT_ROADMAP.md`.
- Drafted Module 3, "Build Trust," the first module of Part Two and the first letter of the Blueprint Framework. Introduces the trust deficit concept and three trust signals (competence, reliability, candour) through a new Kestrel client, Bramble Analytics, a 45-person analytics company.
- Added Figure 3.1, the Trust Pyramid (one of the fifteen tracked signature visuals), and Worksheet 3, the trust audit.
- Self-reviewed against the Humanizer Pass and checked for continuity against Modules 1-2 and `BOOK_BIBLE.md` §8.

## [Unreleased] Phase 3-4: Part One (Modules 1-2)

- Author renamed to Samuel Omobusuyi (dropped the middle initial) throughout the manuscript and legal files.
- Phase 2 front matter approved and marked Final in `PROJECT_ROADMAP.md`.
- Drafted Module 1, "The Truth About Sales": the first appearance of Kestrel Office Interiors and Priya Shah, structured around four myths that stop skilled business owners from selling well. Added Figure 1.1 (two sellers, same deal) and Worksheet 1 (myth audit).
- Drafted Module 2, "How Customers Really Buy": introduces the buying committee (office manager, finance director, managing director) through a new Kestrel client scene, without repeating Module 1's story. Added Figure 2.1 (the hidden committee) and Worksheet 2 (buying committee map).
- Both modules self-reviewed against the Humanizer Pass and checked for continuity against `BOOK_BIBLE.md` §8 (no contradiction of established Kestrel facts).

## [Unreleased] Phase 2: Front matter

- Drafted all eight front-matter files in `manuscript/front-matter/`: copyright, disclaimer, dedication, preface, table of contents, how to use this book, introduction, and the Blueprint Framework overview.
- The preface introduces the author's voice and a specific origin story for the framework; the introduction sets up the book's central argument (selling as sequence, not personality) without repeating the preface's anecdote.
- The Blueprint Framework chapter expands each of the nine stages into a short explanation with its failure mode, and introduces the idea that the sequence loops (a referral or a new stakeholder restarts Build Trust).
- Added `visuals/diagrams/figure-0.1-blueprint-framework.mmd`, a Mermaid flowchart of the nine-stage sequence, referenced from the Blueprint Framework chapter. This is the first of the fifteen tracked visuals to reach Drafted status.
- All eight files and the diagram were checked against the Humanizer Pass (`BOOK_BIBLE.md` §13): no em dashes, en dashes, curly quotes, emojis, or AI-vocabulary clusters found on review.

## [Unreleased] Phase 1 addendum: Humanizer Pass

- Added Section 13 to `BOOK_BIBLE.md`, "Humanizer Pass (Mandatory Writing Quality Gate)," which makes the repository-root `SKILL (1).md` (the humanizer skill) a required quality check on every piece of manuscript text before it is marked Final in `PROJECT_ROADMAP.md`.
- Rewrote `BOOK_BIBLE.md`, `README.md`, `PROJECT_ROADMAP.md`, `LICENSE.md`, `CHANGELOG.md`, and all supporting-folder README files to remove every em dash and en dash, in line with the humanizer skill's hard constraint against dash-heavy AI-sounding prose. Number ranges now use "to" or a plain hyphen instead of an en dash.
- Tightened `BOOK_BIBLE.md` §2 (Voice Guide), §4 (Formatting Guide), and §10 (Editorial Rules) to reference the Humanizer Pass directly.

## [Unreleased] Phase 1 revision

- Publisher renamed from "SamSec Publishing" to **SSO Publishing** throughout `BOOK_BIBLE.md` and `README.md`; `BOOK_BIBLE.md` §1 now states explicitly that SSO Publishing is the official imprint for the entire project.
- Repository renamed from `sales-blueprint-book/` to `Sales-Blueprint/` and restructured into the production tree:
  - `manuscript/modules/part-*` flattened to `manuscript/part-01-foundations/`, `part-02-blueprint-framework/`, `part-03-modern-selling/`, `part-04-implementation/`.
  - Top-level `references/` moved inside `manuscript/references/`.
  - Top-level `diagrams/` moved to `visuals/diagrams/`; added `visuals/illustrations/`, `visuals/charts/`, `visuals/icons/`, `visuals/exports/`.
  - `assets/` subdivided into `assets/logos/`, `assets/fonts/`, `assets/brand/`.
  - Added top-level `exports/` with `docx/`, `pdf/`, `epub/`, `print/`.
- Added `PROJECT_ROADMAP.md` (phase plan and live status tracker), `CHANGELOG.md` (this file), and `LICENSE.md`.
- Retired `STATUS.md`; its tracker content now lives in `PROJECT_ROADMAP.md`.
- `README.md` architecture diagram and design notes rewritten to match the new tree.
- `BOOK_BIBLE.md` diagram-path references updated from `/diagrams/` to `/visuals/diagrams/`.

## [Unreleased] Phase 1

- Initial repository scaffold created: `manuscript/`, `worksheets/`, `templates/`, `checklists/`, `diagrams/`, `visuals/prompts/`, `assets/`, `references/`.
- `BOOK_BIBLE.md` drafted: project identity, voice guide, style guide, formatting guide, terminology, Blueprint Framework definitions, visual style, running case study (Kestrel Office Interiors), quality standard, editorial rules, copyright page text.
- `README.md` and `STATUS.md` drafted.
