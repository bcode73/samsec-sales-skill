# Changelog

All material changes to the *Sales Blueprint* manuscript and repository are recorded here, most recent first. This is a production changelog, not a marketing one: every entry should let a reviewer understand exactly what changed and why without opening the diff.

Format: `## [Date] Phase: Summary`, followed by a short bullet list of changes.

---

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
