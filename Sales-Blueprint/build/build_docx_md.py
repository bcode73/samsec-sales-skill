#!/usr/bin/env python3
"""Assembles a single Pandoc-flavoured Markdown file covering the whole book
(front matter, all 14 modules, full appendices including every worksheet,
template, and checklist), for conversion to an editable .docx via Pandoc.
Figure callouts become real Markdown images. Page breaks between major
sections are raw OOXML passthrough blocks, since Pandoc's Markdown reader
has no native page-break syntax that survives to the docx writer."""
import re
import os
import glob
from PIL import Image

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BUILD_DIR)
DIAGRAM_IMG_DIR = f"{BUILD_DIR}/diagram-images"
COVER_IMG = f"{REPO}/assets/brand/exports/front-cover.png"

PAGE_BREAK = '\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'

FIGURE_RE = re.compile(
    r'^> \*\*(Figure [\d.]+): ([^*]+?)\.?\*\*\s*See `visuals/(?:diagrams|charts)/([\w.\-]+)\.mmd`\.\s*(.*)$',
    re.MULTILINE,
)
SIMPLE_FIGURE_RE = re.compile(r"^\*(Figure ([\d.]+): ([^*]+?))\*$", re.MULTILINE)
SIMPLE_FIGURE_FILES = {"0.1": "figure-0.1-blueprint-framework"}

# Reference page is 6in wide with 0.8in left/right margins and 9in tall with
# 0.75in top/bottom margins (see make_reference_docx.py), leaving 4.4in x
# 7.5in of usable space. The mermaid-cli renders are exported at a high
# pixel scale for print sharpness, so without an explicit size Pandoc embeds
# them at native size (many are 15-25in at 96dpi) and Word/LibreOffice/WPS
# each handle the overflow differently, some clipping the image instead of
# scaling it down. Sizing every figure to fit within one page, whichever of
# width or height is more restrictive for its own aspect ratio, removes that
# per-renderer guesswork.
MAX_FIGURE_WIDTH_IN = 4.3
MAX_FIGURE_HEIGHT_IN = 6.3


def figure_size(img_path):
    with Image.open(img_path) as im:
        w, h = im.size
    aspect = h / w
    width_in = min(MAX_FIGURE_WIDTH_IN, MAX_FIGURE_HEIGHT_IN / aspect)
    return round(width_in, 2)


def convert_figures(src):
    def replace_figure(m):
        fig_label, fig_title, fig_name, caption_rest = m.groups()
        img_path = f"{DIAGRAM_IMG_DIR}/{fig_name}.png"
        width_in = figure_size(img_path)
        return f"![{fig_label}: {fig_title}. {caption_rest}]({img_path}){{width={width_in}in}}"

    src = FIGURE_RE.sub(replace_figure, src)

    def replace_simple(m):
        full_label, fig_num, rest = m.groups()
        fig_name = SIMPLE_FIGURE_FILES.get(fig_num)
        if not fig_name:
            return m.group(0)
        img_path = f"{DIAGRAM_IMG_DIR}/{fig_name}.png"
        width_in = figure_size(img_path)
        return f"![{full_label}]({img_path}){{width={width_in}in}}"

    src = SIMPLE_FIGURE_RE.sub(replace_simple, src)
    return src


def read(path):
    with open(path, encoding="utf-8") as f:
        return convert_figures(f.read()).strip()


def divider(title, subtitle=""):
    md = f"# {title}\n"
    if subtitle:
        md += f"\n### {subtitle}\n"
    return md


# Full usable width (page width minus left/right margins); explicit so the
# cover renders identically across Word, LibreOffice, and WPS instead of
# relying on each one's own fallback for an oversized inline image.
COVER_WIDTH_IN = 4.4


def cover_page():
    return f"![]({COVER_IMG}){{width={COVER_WIDTH_IN}in}}\n"


TOC_STRUCTURE = [
    ("Front matter", [
        "Copyright", "Disclaimer", "Dedication", "Preface",
        "How to use this book", "Introduction", "The Blueprint Framework",
    ]),
    ("Part One: Foundations", [
        "Module 1: The Truth About Sales", "Module 2: How Customers Really Buy",
    ]),
    ("Part Two: The Blueprint Framework", [
        "Module 3: Build Trust", "Module 4: Learn the Customer",
        "Module 5: Understand the Problem", "Module 6: Establish Value",
        "Module 7: Present the Offer", "Module 8: Remove Doubt",
        "Module 9: Inspire Action", "Module 10: Nurture Relationships",
        "Module 11: Turn Customers into Advocates",
    ]),
    ("Part Three: Modern Selling", [
        "Module 12: Digital Selling", "Module 13: Sales Systems",
    ]),
    ("Part Four: Implementation", ["Module 14: The 30-Day Sales Blueprint"]),
    ("Appendices", [
        "Worksheets index", "Templates index", "Checklists index",
        "Glossary", "Frequently asked questions", "References",
    ]),
    ("Worksheets", [f"Worksheet {i}" for i in range(1, 15)]),
    ("Templates", ["Proposal structure", "Customer persona", "Follow-up email"]),
    ("Checklists", ["The 30-Day Sales Blueprint Checklist"]),
]


def toc_page():
    lines = ["# Contents\n"]
    for part_title, items in TOC_STRUCTURE:
        lines.append(f"**{part_title}**\n")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines)


def build():
    fm = f"{REPO}/manuscript/front-matter"
    p1 = f"{REPO}/manuscript/part-01-foundations"
    p2 = f"{REPO}/manuscript/part-02-blueprint-framework"
    p3 = f"{REPO}/manuscript/part-03-modern-selling"
    p4 = f"{REPO}/manuscript/part-04-implementation"
    ap = f"{REPO}/manuscript/appendices"
    ws = f"{REPO}/worksheets"
    tp = f"{REPO}/templates"
    cl = f"{REPO}/checklists"

    # Every module/worksheet/template/checklist file and every divider()
    # starts with exactly one Heading 1, which is styled with
    # page-break-before in the reference doc (see make_reference_docx.py),
    # so a manual PAGE_BREAK before them would be redundant and, worse, can
    # produce a genuinely blank page if the preceding content happens to
    # fill its page exactly. Only 00-copyright.md has no leading heading,
    # so it's the one place a manual break is still needed.
    parts = [cover_page(), toc_page(), PAGE_BREAK]

    # Front matter (skip the hand-written 04-table-of-contents.md; the
    # hand-built toc_page() above serves as the table of contents instead)
    front_matter_files = [
        "00-copyright.md", "01-disclaimer.md", "02-dedication.md", "03-preface.md",
        "05-how-to-use-this-book.md", "06-introduction.md", "07-the-blueprint-framework.md",
    ]
    for fname in front_matter_files:
        parts.append(read(f"{fm}/{fname}"))

    parts.append(divider("Part One: Foundations"))
    parts.append(read(f"{p1}/module-01-the-truth-about-sales.md"))
    parts.append(read(f"{p1}/module-02-how-customers-really-buy.md"))

    parts.append(divider("Part Two: The Blueprint Framework"))
    p2_files = [
        "module-03-build-trust.md", "module-04-learn-the-customer.md",
        "module-05-understand-the-problem.md", "module-06-establish-value.md",
        "module-07-present-the-offer.md", "module-08-remove-doubt.md",
        "module-09-inspire-action.md", "module-10-nurture-relationships.md",
        "module-11-turn-customers-into-advocates.md",
    ]
    for fname in p2_files:
        parts.append(read(f"{p2}/{fname}"))

    parts.append(divider("Part Three: Modern Selling"))
    parts.append(read(f"{p3}/module-12-digital-selling.md"))
    parts.append(read(f"{p3}/module-13-sales-systems.md"))

    parts.append(divider("Part Four: Implementation"))
    parts.append(read(f"{p4}/module-14-the-30-day-sales-blueprint.md"))

    parts.append(divider("Appendices"))
    for fname in [
        "00-worksheets-index.md", "01-templates-index.md", "02-checklists-index.md",
        "03-glossary.md", "05-frequently-asked-questions.md", "04-references.md",
    ]:
        parts.append(read(f"{ap}/{fname}"))

    parts.append(divider("Worksheets", "All fourteen, in full"))
    for i in range(1, 15):
        matches = glob.glob(f"{ws}/{i:02d}-*.md")
        if matches:
            parts.append(read(matches[0]))

    parts.append(divider("Templates"))
    for fname in ["proposal-template.md", "customer-persona-template.md", "follow-up-email-template.md"]:
        parts.append(read(f"{tp}/{fname}"))

    parts.append(divider("Checklists"))
    parts.append(PAGE_BREAK)
    parts.append(read(f"{cl}/14-thirty-day-checklist.md"))

    return "\n\n".join(parts)


if __name__ == "__main__":
    print(build())
