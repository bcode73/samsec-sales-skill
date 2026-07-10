# Changelog

All material changes to the *Sales Blueprint* manuscript and repository are recorded here, most recent first. This is a production changelog, not a marketing one: every entry should let a reviewer understand exactly what changed and why without opening the diff.

Format: `## [Date] Phase: Summary`, followed by a short bullet list of changes.

---

## [Unreleased] Phase 20: first sellable PDF built for Selar

- User decision: launch as an ebook on Selar first; wider distribution (Amazon KDP, Apple Books, Google Play) is deferred, along with EPUB, ISBN, and print.
- Built a full PDF compilation pipeline in `/build`:
  - Renders all 19 Mermaid diagrams to high-resolution transparent PNGs via `mermaid-cli`.
  - Converts every manuscript file, worksheet, template, and checklist to HTML with Python's `markdown` library (tables, task-list checkboxes, fenced code).
  - Replaces each figure callout (both the standard blockquote form used by all 14 modules and the older italic form used once in the front matter) with the actual embedded diagram image and caption.
  - Assembles one HTML document: a full-bleed cover page, a fully clickable table of contents, part-divider pages (deep teal, matching the brand palette), and every front-matter file, module, and appendix section starting on its own page.
  - Renders to PDF with headless Chromium via Playwright at a 6in x 9in page size, with a page-number footer.
- Included the full text of all 14 worksheets, 3 templates, and 1 checklist in the PDF itself, not just their index entries, so a Selar buyer gets a complete, standalone product rather than an index pointing elsewhere.
- Typography: "Bitstream Charter" serif for body text, "Liberation Sans" for headings, both metric-compatible system fonts (no external font downloads needed), on the book's established cream/deep-teal/charcoal palette.
- Visually reviewed a sample of pages before finalizing (cover, contents, copyright, disclaimer, a comparison table, an embedded figure, a worksheet with checkboxes, a part divider, the final page) and fixed one real defect found in review: wrapped checkbox list items lost their hanging indent, now fixed with a flex layout.
- **Output:** `exports/pdf/sales-blueprint.pdf`, 186 pages, 2.9 MB.
- **Known rough edges** (documented in `build/README.md`): a small page number appears in the footer margin on the cover and part-divider pages, since Chromium's header/footer templates apply uniformly to every page with no per-page suppression; no PDF bookmarks/outline (navigation relies on the clickable in-document table of contents instead). Neither blocks a sale.
- This is a digital-only build: no ISBN, no print bleed or crop marks, no CMYK conversion. Print-ready export and the full wraparound cover (spine + back) remain future work.

## [Unreleased] Phase 20 (partial): front cover generated, approved, and committed

- Generated a front-cover concept directly in Canva rather than as a written external-generation prompt, since Canva's tools were connected in this session. Used the book's own palette (cream `#FBF9F4` background, deep teal `#0F3D3E` accent, charcoal `#1B1F1E` ink) and minimal business-consulting style from `BOOK_BIBLE.md` §7, not a Canva brand kit.
- Four candidates generated; user selected one, converted to a permanent, editable Canva design, and approved the result.
- Exported the design as a PNG. The direct download from Canva's export URL was blocked by this session's network egress policy (canva.com and its subdomains are denied), so the user downloaded it themselves and attached the file back into the session.
- Committed the file to `assets/brand/exports/front-cover.png` (1587 x 2245 px). Updated `assets/brand/cover.md` to point at the committed file, keeping the Canva edit/view links for future changes.
- Scope: front cover only. Spine and back cover (full wraparound) intentionally deferred until a firm final page count is set, since spine width depends on it. The committed PNG is sized for digital/ebook use; a 300 DPI print-resolution export is still needed before a print run.

## [Unreleased] Phase 19 (diagram QA sweep): fixed 7 badly proportioned diagrams

- Rendered all 19 Mermaid diagrams through `mermaid-cli` to check for syntax errors and print proportions.
- Found 7 rendering as extreme, flat single-row layouts unsuitable for a printed page: Figure 0.1 (the flagship Blueprint Framework diagram) at 14:1, down to Figure 5.1 at 5.4:1. Figures affected: 0.1, 4.1, 5.1, 7.1, 10.1, 11.1, 13.1.
- Rewrote each as a wrapped grid (3x3 for the two nine-stage diagrams, 2x2 for the four-node ones) using Mermaid subgraphs. This surfaced a dagre layout quirk: a directed cycle-back edge (the "referral restarts the cycle" arrows in Figures 0.1 and 11.1) flips the whole row order; fixed by writing those edges as undirected-with-single-arrowhead links (e.g. `B <-.-|label| T`) instead of fully directed ones.
- All 19 diagrams re-verified to render without errors; ratios now range 0.44:1 to 3.22:1.
- Found and fixed a follow-on inconsistency: 5 of the premium visual-generation prompts in `visuals/prompts/` (Blueprint Framework, Customer Journey, Offer Builder, Follow-up Timeline, Lead Pipeline) still described the old flat "landscape" layouts. Updated to describe the same wrapped-grid arrangement. Two others (Buying Psychology Wheel, Referral Flywheel) already specified a proper circular/square layout and needed no change.
- Text-level QA sweep also found and fixed two documentation errors: the FAQ appendix was logged as "20 questions" in CHANGELOG.md/PROJECT_ROADMAP.md but actually has 22; and `README.md` still stated the original "220 to 280 pages" target after `BOOK_BIBLE.md`'s target had already been revised to 125 to 150.
- Full-repository sweep otherwise found no Humanizer Pass violations, no figure-reference mismatches, no continuity contradictions among the "in a different kind of business" secondary characters, and no stale appendix index counts.

## [Unreleased] Phase 19 (final length pass): FAQ appendix, expanded glossary, quick reference

- User decision: the manuscript's length is essentially fine as is; add roughly 10 more pages of new content rather than another full deepening round.
- Added a new appendix, `manuscript/appendices/05-frequently-asked-questions.md`: 22 direct questions and answers covering practical reader concerns not fully addressed elsewhere (genuine commodity markets, selling inside a larger company, internal pitches, formal RFPs, product churn, team consistency without identical scripts, one-off no-repeat businesses, and more), each referencing the relevant module. Added the file to the front-matter table of contents.
- Added a "quick reference: the nine stages and their key question" table inside the same appendix, a one-line summary of what each Blueprint stage is actually asking, useful for a quick pipeline check.
- Expanded the glossary with 11 additional terms (asserted value, demonstrated value, discovery, friction, loop-back, nurture cadence, pipeline, status quo gravity, symptom, trust signal), cross-referenced to the modules that define them.
- Self-reviewed against the Humanizer Pass.
- Revised `BOOK_BIBLE.md`'s target length from 220 to 280 pages to 125 to 150 pages, to reflect the manuscript's actual, user-accepted scope after three deepening rounds and this final content pass.
- **New total:** approximately 40,427 words altogether (31,870 words of manuscript plus 5,688 words of worksheets/templates/checklists plus the new appendix content), approximately 124 to 147 pages at typical business-book density, up from about 37,558 words before this pass. This closes the length-expansion work started in Phase 19; the manuscript is considered complete at this length.

## [Unreleased] Phase 19 (round 3 expansion): a second worked scenario per module

- User decision: a third pass with substantially larger additions per module than rounds 1 or 2, specifically to test whether bigger increments close meaningfully more of the length gap.
- Added a full "In a different kind of business" section (roughly 200 to 300 words each) to all 14 modules: a compact, distinct worked scenario in a different small business, illustrating the same chapter principle outside the Kestrel/Bramble Analytics arc. Businesses used: a freelance copywriter (Module 1, later reused as the capstone example in Module 14), a wedding photographer (Module 2), an independent accountant (Module 3), a commercial cleaning company (Module 4), a small marketing agency (Module 5), a bespoke furniture maker (Module 6), an IT support provider (Module 7), a landscaping company (Module 8), a corporate training consultant (Module 9), a boutique PR agency (Module 10), a specialty coffee roaster (Module 11), a fully asynchronous text-only digital deal (Module 12), and a three-partner events staffing agency (Module 13).
- Every addition was self-reviewed against the Humanizer Pass and checked for continuity against the rest of the manuscript.
- **New total:** 31,870 words of manuscript (front matter, modules, appendices) plus 5,688 words of worksheets, templates, and checklists, approximately 37,558 words altogether, up from about 34,648 before this pass. At typical business-book density (275 to 325 words per page) that is approximately 116 to 137 pages.
- **Finding:** this round added roughly 2,910 words, essentially the same order of magnitude as round 2's 3,150 words, despite each section being deliberately two to three times larger than round 2's additions. This confirms the pattern scales at roughly 3,000 words per round regardless of section size, meaning closing the remaining gap to 220 to 280 pages by repeating this method would take another 10 to 15 rounds. Reported honestly rather than continuing the same pattern; flagged for a decision between adding genuinely new content types or revising the page target.

## [Unreleased] Phase 19 (round 2 expansion): comparison tables and practice drills

- User decision: another deepening pass rather than adding new content or accepting the shorter length.
- Added one scannable comparison or reference table and one standing-habit "practice drill" section to all 14 modules, each distinct from the round 1 additions (mechanism explanations and edge cases). Tables include "The four myths, side by side" (Module 1), "Asserted versus demonstrated, three examples" (Module 6), "Menu, ladder, and single recommendation, compared" (Module 7), and similar reference tables for every other module. Drill sections turn each module's single-deal worksheet exercise into a recurring habit, for example "A weekly drill, not a one-off exercise" (Module 1) and "Run the same four-number review every month, regardless" (Module 13).
- Every edit was self-reviewed against the Humanizer Pass (dash check, curly-quote check, banned-vocabulary check) and checked for continuity against the rest of the manuscript.
- **New total:** 28,960 words of manuscript (front matter, modules, appendices) plus 5,688 words of worksheets, templates, and checklists, approximately 34,648 words altogether, up from about 31,500 before this pass. At typical business-book density (275 to 325 words per page) that is approximately 107 to 126 pages. This round added roughly 3,150 words against a remaining gap of several tens of thousands of words to reach the 220 to 280 page target in `BOOK_BIBLE.md` §1; a third round of the same kind of addition is unlikely to close that gap on its own. Reported honestly for a further decision on approach.

## [Unreleased] Phase 19 (expansion): deepen all 14 modules

- User decision: deepen every module rather than add new content or accept the shorter length.
- Expanded all 14 modules with mechanism explanations (why each behaviour works, not just what it is), edge cases (first-time buyers, procurement-mandated menus, unquantifiable value, longer sales cycles, and more), and two to three new steps per worksheet. Module 14 gained a closing retrospective, "Where Kestrel ended up," tying the book's full arc together.
- Every expanded module was self-reviewed against the Humanizer Pass and checked for continuity against the rest of the manuscript.
- **New total:** approximately 25,800 words of manuscript (front matter, modules, appendices) plus approximately 5,700 words of worksheets/templates/checklists, roughly 31,500 words altogether, up from about 23,300 before this pass. At typical business-book density (275 to 325 words per page) that is approximately 95 to 115 pages. This is real growth, not padding, but it remains short of the 220 to 280 page target in `BOOK_BIBLE.md` §1. Reported honestly rather than closed prematurely; further expansion, a revised target, or additional content are all still open decisions.

## [Unreleased] Phase 19: Final QC pass

- Fixed 3 stray em dashes in CHANGELOG.md phase headers, introduced during later phases after the initial Humanizer cleanup; a full-repository sweep found no other em dashes, en dashes, curly quotes, or emoji anywhere in the project.
- Verified all 19 figure references in the manuscript prose (Figures 0.1 through 14.1) match an actual file in `visuals/diagrams/` or `visuals/charts/`.
- Verified every cross-module reference (e.g. "Module 4's three questions," "Module 3's trust signals," "Module 8's specific-doubt resolution") against the module it cites; all accurate.
- Verified appendix index counts against actual files: 14 worksheets, 3 templates, 1 checklist, 15 visual prompts, all match.
- Verified no contradictions in established Kestrel Office Interiors facts across any module.
- **Finding:** total manuscript word count (front matter, all 14 modules, appendices) is approximately 18,900 words; including worksheets, templates, and checklists brings the total to roughly 23,300 words, which is approximately 65 to 80 formatted pages at typical business-book density. This is well short of the 220 to 280 page target set in `BOOK_BIBLE.md` §1. Flagged for a decision rather than closed by padding existing chapters with filler, which `BOOK_BIBLE.md` §10 explicitly prohibits.

## [Unreleased] Phase 18: Visual generation prompts

- Added all fifteen detailed generation prompts in `visuals/prompts/`, one per tracked signature visual (The Blueprint Framework, Trust Pyramid, Customer Journey, Buying Psychology Wheel, Value Stack, Offer Builder, Pricing Ladder, Objection Flowchart, Decision Tree, Sales Funnel, Follow-up Timeline, Referral Flywheel, Customer Lifetime Value, Lead Pipeline, Sales Dashboard). Each includes purpose, placement, caption, and a full image-generation prompt consistent with the visual style in `BOOK_BIBLE.md` §7 (minimal, premium, business-consulting; deep teal accent; no gradients or drop shadows).
- Self-reviewed against the Humanizer Pass.
- Remaining visual work: generating the actual premium graphics from these prompts and exporting them to `visuals/exports/`, which depends on an external image-generation tool rather than manuscript writing.

## [Unreleased] Phase 17: Appendices

- Added three new template files: `templates/proposal-template.md` (the seven-part structure behind Module 7's proposals), `templates/customer-persona-template.md` (one per stakeholder, tied to Module 4's discovery questions), and `templates/follow-up-email-template.md` (the check-ins, referral ask, and loop-closing note from Modules 10-11).
- Added `manuscript/appendices/00-worksheets-index.md` through `04-references.md`: an index of all fourteen worksheets, an index of the three templates, an index of the one checklist, an alphabetical glossary cross-referenced to the modules that use each term, and a references page that states plainly the case study is fictional and offers four further-reading titles without claiming them as sources.
- Added `manuscript/references/traceability-notes.md`, an internal (non-reader-facing) record mapping manuscript concepts to the general topic areas of the repository's SKILL.md library that informed them, per `BOOK_BIBLE.md` §10.
- Self-reviewed all new files against the Humanizer Pass.

## [Unreleased] Phase 16 (approved): all manuscript content Final

- Module 14 approved and marked Final, along with Figure 14.1.
- Every piece of manuscript content, all front matter and Modules 1-14, is now Final. Remaining work is appendices, remaining visual prompts and exports, a final quality control pass, and compiled export.

## [Unreleased] Phase 16: Module 14 (The 30-Day Sales Blueprint), all manuscript content drafted

- Module 13 approved and marked Final, along with Figures 13.1 and 13.2. Part Three is complete and Final in full.
- Drafted Module 14, "The 30-Day Sales Blueprint," completing Part Four and all core manuscript content. Compresses the nine Blueprint stages into a four-week rollout (Week 1: Build Trust + Learn the Customer; Week 2: Understand the Problem + Establish Value; Week 3: Present the Offer + Remove Doubt + Inspire Action; Week 4: Nurture + Advocates + Systems), tied directly to the relevant worksheet from each earlier module.
- Added Figure 14.1 (the 30-Day Rollout), Worksheet 14 (rollout planner), and Checklist 14 (the first file in `/checklists`, a quick-reference tick-list version of the rollout).
- Self-reviewed against the Humanizer Pass and checked for continuity against all thirteen preceding modules.
- With this module drafted, every planned module (1-14) and all front matter exists in the repository. Remaining work: appendices (glossary, references, worksheet/template/checklist index), remaining visual prompts and exports, a final quality control pass, and compiled export.

## [Unreleased] Phase 15: Module 13 (Sales Systems), Part Three complete

- Module 12 approved and marked Final, along with Figure 12.1.
- Drafted Module 13, "Sales Systems," completing Part Three. Priya rebuilds her pipeline around the nine Blueprint letters instead of generic stage labels, tracks stakeholders individually so a new person joining a deal doesn't get assumed to be at the same stage as everyone else, and adopts four dashboard metrics. Win rate and referral rate are shown rising over four quarters, consistent with the improvement arc set out in `BOOK_BIBLE.md` §8.
- Added Figure 13.1 (the Lead Pipeline) and Figure 13.2 (the Sales Dashboard, in `visuals/charts/`), and Worksheet 13 (pipeline rebuild).
- Self-reviewed against the Humanizer Pass and checked for continuity against Modules 1-12.

## [Unreleased] Phase 14: Module 12 (Digital Selling)

- Drafted Module 12, "Digital Selling," opening Part Three. A new remote-sourced lead, Tom, finds Kestrel through a published write-up of the Bramble Analytics project and never meets Priya in person until installation is nearly finished. The module maps each Blueprint stage from Part Two onto its digital equivalent (published proof instead of a conversational trust signal, direct questions instead of reading body language, shareable documents instead of an in-person handover).
- Added Figure 12.1 (Digital Trust and Discovery Signals) and Worksheet 12 (digital signal audit).
- Self-reviewed against the Humanizer Pass and checked for continuity against Modules 1-11 and `BOOK_BIBLE.md` §8 (Kestrel's remote-first client base was already established there).

## [Unreleased] Phase 13 (approved): Part Two complete

- Module 11 approved and marked Final, along with Figures 11.1 and 11.2.
- Part Two, all nine Blueprint Framework modules (Build Trust through Turn Customers into Advocates), is now Final in full.

## [Unreleased] Phase 13: Module 11 (Turn Customers into Advocates), Part Two complete

- Module 10 approved and marked Final, along with Figure 10.1.
- Drafted Module 11, "Turn Customers into Advocates," completing Part Two. Priya turns Dominic's offhand comment from Module 10 into a specific, named referral ask, then closes the loop with him afterward, rather than hoping the introduction happens on its own.
- Added Figure 11.1 (the Referral Flywheel) and Figure 11.2 (Customer Lifetime Value), the latter placed in `visuals/charts/` rather than `visuals/diagrams/`, consistent with the architecture split between process diagrams and data-style charts. Added Worksheet 11 (referral ask builder).
- Self-reviewed against the Humanizer Pass and checked for continuity against Modules 1-10.
- All nine Blueprint Framework modules (Build Trust through Turn Customers into Advocates) are now drafted, tracing one continuous deal, Bramble Analytics, from first contact through to a closed, referring customer.

## [Unreleased] Phase 12: Module 10 (Nurture Relationships)

- Module 9 approved and marked Final, along with Figure 9.1.
- Drafted Module 10, "Nurture Relationships," continuing the Bramble Analytics deal. Six weeks after installation, Priya calls Dominic with a genuine, no-pitch question about whether the original problem is actually solved, which surfaces unprompted interest from other Bramble teams in the flexible-room concept, setting up Module 11.
- Added Figure 10.1 (the Follow-up Timeline) and Worksheet 10 (nurture cadence planner).
- Self-reviewed against the Humanizer Pass and checked for continuity against Modules 1-9.

## [Unreleased] Phase 11: Module 9 (Inspire Action)

- Module 8 approved and marked Final, along with Figures 8.1 and 8.2.
- Continuity correction to Module 8: the closing scene originally had Marguerite sign the agreement, which skipped ahead of Module 9. Revised so Marguerite is verbally convinced but the proposal remains unsigned, giving Module 9 a real gap to close.
- Drafted Module 9, "Inspire Action," continuing the Bramble Analytics deal. Priya diagnoses the unsigned proposal as ordinary friction (a busy co-founder, an open-ended task), not lingering doubt, and closes it with a shrunk next step (a fifteen-minute signing call) and the genuine installation-slot deadline established in Module 7.
- Added Figure 9.1 (the Sales Funnel) and Worksheet 9 (action friction audit).
- Self-reviewed against the Humanizer Pass and checked for continuity against Modules 1-8.

## [Unreleased] Phase 10: Module 8 (Remove Doubt)

- Module 7 approved and marked Final, along with Figures 7.1 and 7.2.
- Drafted Module 8, "Remove Doubt," continuing the Bramble Analytics deal. Marguerite, the co-founder introduced in Module 4, appears on the page for the first time and raises a specific, late-stage doubt about construction disruption on Bramble's two busiest days. Priya resolves it with a schedule built around exactly that concern, rather than general reassurance.
- Added Figure 8.1 (the Objection Flowchart), Figure 8.2 (the Decision Tree), and Worksheet 8 (objection resolution).
- Self-reviewed against the Humanizer Pass and checked for continuity against Modules 1-7.

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
