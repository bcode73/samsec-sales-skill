# Sales Blueprint
### The Practical System for Attracting Customers, Closing More Sales and Building a Business People Trust

**Author:** Samuel S. Omobusuyi · **Publisher:** SamSec Publishing · **Language:** British English

This directory is the working repository for the manuscript, worksheets, templates, checklists, diagrams and premium visual prompts that make up *Sales Blueprint* — a commercially publishable business book (220–280 pages), built and edited to sit alongside the best-known books on sales and customer psychology.

This is a **publishing project**, not a generated ebook. Every module is drafted, then reviewed, then revised against [`BOOK_BIBLE.md`](./BOOK_BIBLE.md) before being marked final. Nothing is copied from source material — the repository's existing `SKILL.md` files (in `sales-skills/`, `skills1/`, `skills2/`, `skills3/`) are used only as research to identify principles worth teaching. All explanations, analogies, exercises, diagrams and the running case study are original.

---

## Start here

**[`BOOK_BIBLE.md`](./BOOK_BIBLE.md)** is the single source of truth for this project: voice, style, formatting, terminology, the Blueprint Framework definitions, visual style, the running case study (Kestrel Office Interiors), and the quality bar every chapter must clear. Read it before writing or reviewing anything else. If any file in this repository contradicts the Book Bible, the Book Bible wins and the file is corrected.

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
sales-blueprint-book/
├── BOOK_BIBLE.md                     # Single source of truth — read first
├── README.md                         # This file
├── STATUS.md                         # Live progress tracker, phase by phase
│
├── manuscript/
│   ├── front-matter/                 # Copyright, disclaimer, dedication, preface,
│   │                                 # TOC, how-to-use-this-book, introduction,
│   │                                 # Blueprint Framework overview
│   ├── modules/
│   │   ├── part-one-foundations/             # Modules 1–2
│   │   ├── part-two-the-blueprint-framework/ # Modules 3–11 (one per letter)
│   │   ├── part-three-modern-selling/        # Modules 12–13
│   │   └── part-four-implementation/         # Module 14
│   └── appendices/                   # Glossary, references index, worksheet/
│                                      # template/checklist index
│
├── worksheets/                       # Standalone worksheet files (fillable),
│                                      # one per exercise referenced in a module
├── templates/                        # Reusable business templates (proposal,
│                                      # persona builder, scorecards, etc.)
├── checklists/                       # Action checklists referenced per module
├── diagrams/                         # Mermaid source for every in-manuscript
│                                      # figure, named figure-{module}.{n}.mmd
├── visuals/
│   └── prompts/                      # Detailed generation prompts for premium
│                                      # full-page graphics (purpose, placement,
│                                      # caption, prompt) — for external image tools
├── assets/                           # Any exported/rendered image assets
└── references/                       # Source notes: which principles were
                                       # synthesised from which research areas
                                       # (no source wording retained)
```

**Why `manuscript/front-matter/` and `manuscript/modules/` sit inside `manuscript/`, rather than as flat top-level folders:** the manuscript is one continuous document assembled from many files. Nesting front matter and modules under a shared parent keeps the reading order obvious from the file tree and makes it trivial to concatenate the whole book into a single export later. Supporting material that lives *outside* the linear reading order — worksheets, templates, checklists, diagrams, visual prompts, assets, references — stays at the top level because each of those is used independently (a worksheet is meant to be printed on its own; a diagram is meant to be regenerated on its own).

This project lives in its own folder (`sales-blueprint-book/`) rather than at the repository root so it never collides with the existing `templates/`, `sales-skills/`, `marketing-skills/`, `skills1/`, `skills2/`, `skills3/` material already in this repository, which remains untouched and is used purely as reference research.

---

## Workflow

This book is written **phase by phase**, never all at once. Each phase is drafted, reviewed for quality and consistency, and confirmed before the next begins.

| Phase | Content | Status |
|---|---|---|
| 1 | Repository architecture, `BOOK_BIBLE.md`, `README.md` | ✅ Complete — awaiting review |
| 2 | Front matter (copyright → introduction → Blueprint Framework overview) | Not started |
| 3–4 | Part One: Modules 1–2 | Not started |
| 5–13 | Part Two: Modules 3–11 (one per Blueprint letter) | Not started |
| 14–15 | Part Three: Modules 12–13 | Not started |
| 16 | Part Four: Module 14 (30-Day Sales Blueprint) | Not started |
| 17 | Appendices: worksheets, templates, checklists, glossary, references | Not started |
| 18 | Visual prompts and diagrams for all 15 required visuals | Not started |
| 19 | Final quality control pass across the full manuscript | Not started |

See [`STATUS.md`](./STATUS.md) for the live, file-by-file tracker.

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
