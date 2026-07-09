# Sales Blueprint
### The Practical System for Attracting Customers, Closing More Sales and Building a Business People Trust

**Author:** Samuel S. Omobusuyi · **Publisher:** SSO Publishing · **Language:** British English

This directory is the working repository for the manuscript, worksheets, templates, checklists, diagrams and premium visuals that make up *Sales Blueprint* — a commercially publishable business book (220–280 pages), built and edited to sit alongside the best-known books on sales and customer psychology.

This is a **publishing project**, not a generated ebook. Every module is drafted, then reviewed, then revised against [`BOOK_BIBLE.md`](./BOOK_BIBLE.md) before being marked final. Nothing is copied from source material — the repository's existing `SKILL.md` files (in `sales-skills/`, `skills1/`, `skills2/`, `skills3/`) are used only as research to identify principles worth teaching. All explanations, analogies, exercises, diagrams and the running case study are original.

---

## Start here

**[`BOOK_BIBLE.md`](./BOOK_BIBLE.md)** is the single source of truth for this project: voice, style, formatting, terminology, the Blueprint Framework definitions, visual style, the running case study (Kestrel Office Interiors), and the quality bar every chapter must clear. Read it before writing or reviewing anything else. **Every module, worksheet, diagram and export produced from this point forward must be checked against `BOOK_BIBLE.md` before it is marked final.** If any file in this repository contradicts the Book Bible, the Book Bible wins and the file is corrected.

---

## The Blueprint Framework (what the book teaches)

```
B — Build Trust
L — Learn the Customer
U — Understand the Problem
E — Establish Value
P — Present the Offer
R — Remove Doubt
I — Inspire Action
N — Nurture Relationships
T — Turn Customers into Advocates
```

Part Two of the book (Modules 3–11) devotes one module to each letter. Every other part of the book refers back to this sequence. Full definitions are in `BOOK_BIBLE.md` §6.

---

## Repository architecture

```
Sales-Blueprint/
│
├── BOOK_BIBLE.md                 # Single source of truth — read first
├── README.md                     # This file
├── PROJECT_ROADMAP.md            # Phase-by-phase plan and live status tracker
├── CHANGELOG.md                  # Dated record of every material change
├── LICENSE.md                    # Rights and usage terms for this manuscript
│
├── manuscript/
│   ├── front-matter/             # Copyright, disclaimer, dedication, preface,
│   │                             # TOC, how-to-use-this-book, introduction,
│   │                             # Blueprint Framework overview
│   ├── part-01-foundations/              # Modules 1–2
│   ├── part-02-blueprint-framework/      # Modules 3–11 (one per letter)
│   ├── part-03-modern-selling/           # Modules 12–13
│   ├── part-04-implementation/           # Module 14
│   ├── appendices/                # Glossary + index of worksheets/templates/checklists
│   └── references/                # Research traceability notes + manuscript
│                                   # References section content
│
├── visuals/
│   ├── diagrams/                  # Mermaid source, one per in-manuscript figure
│   ├── illustrations/             # Original scene/concept illustrations (non-diagram)
│   ├── charts/                    # Data-style charts (e.g. dashboard, CLV curve)
│   ├── icons/                     # Small supporting iconography
│   ├── prompts/                   # Generation prompts for every premium visual
│   │                               # (purpose, placement, caption, prompt)
│   └── exports/                   # Rendered PNG/SVG output of the above
│
├── worksheets/                    # Standalone, fillable exercise files
├── templates/                     # Reusable business templates (proposal,
│                                   # persona builder, scorecards, etc.)
├── checklists/                    # Action checklists referenced per module
│
├── assets/
│   ├── logos/                     # SSO Publishing / Sales Blueprint logo marks
│   ├── fonts/                     # Licensed typefaces used in layout/export
│   └── brand/                     # Colour palette, cover art, brand guidelines
│
└── exports/
    ├── docx/                      # Compiled manuscript — Word
    ├── pdf/                       # Compiled manuscript — PDF
    ├── epub/                      # Compiled manuscript — EPUB
    └── print/                     # Print-ready, press ready files
```

**Design notes:**

- **`manuscript/`** holds everything that is part of the continuous, linear read — front matter, the four parts, appendices, and references — so the reading order is visible directly from the file tree and the whole book can be concatenated for export in one pass.
- **`visuals/`** separates lightweight in-manuscript Mermaid diagrams (`diagrams/`) from premium commissioned graphics (`illustrations/`, `charts/`, `icons/`), the prompts used to generate them (`prompts/`), and their rendered output (`exports/`) — each stage of the visual pipeline has its own home.
- **`worksheets/`, `templates/`, `checklists/`** stay at the top level, outside `manuscript/`, because each is designed to be used independently of the book (printed, filled in, or reused in the reader's own business) even though every one of them is introduced by a specific module.
- **`assets/`** is brand and production material (logos, licensed fonts, brand guidelines) — distinct from `visuals/exports/`, which is book-content artwork.
- **`exports/`** is the compiled, reader-facing output of the whole manuscript in each commercial format — the only folder that represents the finished product rather than working material.

This project lives in its own folder (`Sales-Blueprint/`) rather than at the repository root so it never collides with the existing `templates/`, `sales-skills/`, `marketing-skills/`, `skills1/`, `skills2/`, `skills3/` material already in this repository, which remains untouched and is used purely as reference research.

---

## Workflow

This book is written **phase by phase**, never all at once. Each phase is drafted, reviewed for quality and consistency, and confirmed before the next begins. See [`PROJECT_ROADMAP.md`](./PROJECT_ROADMAP.md) for the full phase plan and the live, file-by-file status tracker.

---

## Every module, without exception, contains

Learning objectives · opening story · core principles · the Kestrel Office Interiors case study (advanced by exactly one stage) · original diagrams · a worksheet/exercise · common mistakes · chapter summary · key takeaway.

And every module must visibly answer five questions: **What? Why? How? How do I apply this today? How do I measure success?** (`BOOK_BIBLE.md` §9.)

---

## Quality control

No module is marked final until it has been checked against:

1. `BOOK_BIBLE.md` — voice, style, formatting, terminology, framework accuracy
2. Every previously completed module — no contradictions, no repeated explanations, continuous case study facts
3. Originality — no source wording or structure copied from the repository's SKILL.md research files or from any other published author

---

## Rights

© 2026 Samuel S. Omobusuyi. Published by SSO Publishing. See [`LICENSE.md`](./LICENSE.md) for full terms.
