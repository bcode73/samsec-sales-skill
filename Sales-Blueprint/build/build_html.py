#!/usr/bin/env python3
import re
import html
import os
import markdown

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BUILD_DIR)
DIAGRAM_IMG_DIR = f"{BUILD_DIR}/diagram-images"
COVER_IMG = f"{REPO}/assets/brand/exports/front-cover.png"

MD_EXTENSIONS = ["tables", "sane_lists", "fenced_code", "pymdownx.tasklist", "pymdownx.tilde"]
MD_EXT_CONFIG = {"pymdownx.tasklist": {"custom_checkbox": False, "clickable_checkbox": False}}

FIGURE_RE = re.compile(
    r'<blockquote>\s*<p><strong>(Figure [\d.]+): ([^*<]+?)\.?</strong>\s*See <code>visuals/(?:diagrams|charts)/([\w.\-]+)\.mmd</code>\.\s*(.*?)</p>\s*</blockquote>',
    re.DOTALL,
)

SIMPLE_FIGURE_RE = re.compile(r"<p><em>(Figure ([\d.]+): ([^<]+?))</em></p>")
SIMPLE_FIGURE_FILES = {
    "0.1": "figure-0.1-blueprint-framework",
}


def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_]+", "-", text).strip("-")


def md_to_html(path):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    body = markdown.markdown(src, extensions=MD_EXTENSIONS, extension_configs=MD_EXT_CONFIG)

    def replace_figure(m):
        fig_label, fig_title, fig_name, caption_rest = m.groups()
        img_path = f"{DIAGRAM_IMG_DIR}/{fig_name}.png"
        return (
            '<div class="figure">'
            f'<img src="file://{img_path}" alt="{html.escape(fig_title)}"/>'
            f'<p class="caption"><strong>{fig_label}: {fig_title}.</strong> {caption_rest}</p>'
            "</div>"
        )

    body = FIGURE_RE.sub(replace_figure, body)

    def replace_simple_figure(m):
        full_label, fig_num, rest = m.groups()
        fig_name = SIMPLE_FIGURE_FILES.get(fig_num)
        if not fig_name:
            return m.group(0)
        img_path = f"{DIAGRAM_IMG_DIR}/{fig_name}.png"
        return (
            '<div class="figure">'
            f'<img src="file://{img_path}" alt="{html.escape(rest)}"/>'
            f'<p class="caption"><strong>{full_label}</strong></p>'
            "</div>"
        )

    body = SIMPLE_FIGURE_RE.sub(replace_simple_figure, body)
    return body


def section(path, anchor_id, extra_class=""):
    body_html = md_to_html(path)
    return f'<section id="{anchor_id}" class="content-section {extra_class}">{body_html}</section>'


def divider(title, subtitle=""):
    sub = f'<p class="divider-subtitle">{subtitle}</p>' if subtitle else ""
    return (
        f'<section class="divider-page"><div class="divider-inner">'
        f'<p class="divider-kicker">Sales Blueprint</p>'
        f'<h1 class="divider-title">{title}</h1>{sub}'
        f"</div></section>"
    )


def cover_page():
    return f'<section class="cover-page"><img src="file://{COVER_IMG}" alt="Sales Blueprint front cover"/></section>'


TOC_STRUCTURE = [
    ("Front matter", None, [
        ("Copyright", "copyright"),
        ("Disclaimer", "disclaimer"),
        ("Dedication", "dedication"),
        ("Preface", "preface"),
        ("How to use this book", "how-to-use-this-book"),
        ("Introduction", "introduction"),
        ("The Blueprint Framework", "blueprint-framework-overview"),
    ]),
    ("Part one: Foundations", "part-one", [
        ("Module 1: The truth about sales", "module-1"),
        ("Module 2: How customers really buy", "module-2"),
    ]),
    ("Part two: The Blueprint Framework", "part-two", [
        ("Module 3: Build trust", "module-3"),
        ("Module 4: Learn the customer", "module-4"),
        ("Module 5: Understand the problem", "module-5"),
        ("Module 6: Establish value", "module-6"),
        ("Module 7: Present the offer", "module-7"),
        ("Module 8: Remove doubt", "module-8"),
        ("Module 9: Inspire action", "module-9"),
        ("Module 10: Nurture relationships", "module-10"),
        ("Module 11: Turn customers into advocates", "module-11"),
    ]),
    ("Part three: Modern selling", "part-three", [
        ("Module 12: Digital selling", "module-12"),
        ("Module 13: Sales systems", "module-13"),
    ]),
    ("Part four: Implementation", "part-four", [
        ("Module 14: The 30-day sales blueprint", "module-14"),
    ]),
    ("Appendices", "appendices", [
        ("Worksheets index", "worksheets-index"),
        ("Templates index", "templates-index"),
        ("Checklists index", "checklists-index"),
        ("Glossary", "glossary"),
        ("Frequently asked questions", "faq"),
        ("References", "references"),
    ]),
    ("Worksheets", "worksheets-full", [(f"Worksheet {i}", f"worksheet-{i}") for i in range(1, 15)]),
    ("Templates", "templates-full", [
        ("Proposal structure", "template-proposal"),
        ("Customer persona", "template-persona"),
        ("Follow-up email", "template-followup"),
    ]),
    ("Checklists", "checklists-full", [
        ("The 30-day sales blueprint checklist", "checklist-30-day"),
    ]),
]


def toc_page():
    parts = ['<section class="toc-page"><h1 class="toc-heading">Contents</h1>']
    for part_title, part_anchor, items in TOC_STRUCTURE:
        head_link = f'<a href="#{part_anchor}">{part_title}</a>' if part_anchor else part_title
        parts.append(f'<p class="toc-part">{head_link}</p>')
        parts.append('<ul class="toc-list">')
        for label, anchor in items:
            parts.append(f'<li><a href="#{anchor}">{label}</a></li>')
        parts.append("</ul>")
    parts.append("</section>")
    return "\n".join(parts)


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

    parts = [cover_page(), toc_page()]

    parts.append(section(f"{fm}/00-copyright.md", "copyright", "copyright-page"))
    parts.append(section(f"{fm}/01-disclaimer.md", "disclaimer"))
    parts.append(section(f"{fm}/02-dedication.md", "dedication", "dedication-page"))
    parts.append(section(f"{fm}/03-preface.md", "preface"))
    parts.append(section(f"{fm}/05-how-to-use-this-book.md", "how-to-use-this-book"))
    parts.append(section(f"{fm}/06-introduction.md", "introduction"))
    parts.append(section(f"{fm}/07-the-blueprint-framework.md", "blueprint-framework-overview"))

    parts.append(divider("Part one", "Foundations"))
    parts.append(section(f"{p1}/module-01-the-truth-about-sales.md", "module-1"))
    parts.append(section(f"{p1}/module-02-how-customers-really-buy.md", "module-2"))

    parts.append(divider("Part two", "The Blueprint Framework"))
    p2_files = [
        "module-03-build-trust.md", "module-04-learn-the-customer.md",
        "module-05-understand-the-problem.md", "module-06-establish-value.md",
        "module-07-present-the-offer.md", "module-08-remove-doubt.md",
        "module-09-inspire-action.md", "module-10-nurture-relationships.md",
        "module-11-turn-customers-into-advocates.md",
    ]
    for i, fname in enumerate(p2_files, start=3):
        parts.append(section(f"{p2}/{fname}", f"module-{i}"))

    parts.append(divider("Part three", "Modern selling"))
    parts.append(section(f"{p3}/module-12-digital-selling.md", "module-12"))
    parts.append(section(f"{p3}/module-13-sales-systems.md", "module-13"))

    parts.append(divider("Part four", "Implementation"))
    parts.append(section(f"{p4}/module-14-the-30-day-sales-blueprint.md", "module-14"))

    parts.append(divider("Appendices", ""))
    parts.append(section(f"{ap}/00-worksheets-index.md", "worksheets-index"))
    parts.append(section(f"{ap}/01-templates-index.md", "templates-index"))
    parts.append(section(f"{ap}/02-checklists-index.md", "checklists-index"))
    parts.append(section(f"{ap}/03-glossary.md", "glossary"))
    parts.append(section(f"{ap}/05-frequently-asked-questions.md", "faq"))
    parts.append(section(f"{ap}/04-references.md", "references"))

    parts.append(divider("Worksheets", "All fourteen, in full"))
    for i in range(1, 15):
        import glob
        matches = glob.glob(f"{ws}/{i:02d}-*.md")
        if matches:
            parts.append(section(matches[0], f"worksheet-{i}"))

    parts.append(divider("Templates", ""))
    parts.append(section(f"{tp}/proposal-template.md", "template-proposal"))
    parts.append(section(f"{tp}/customer-persona-template.md", "template-persona"))
    parts.append(section(f"{tp}/follow-up-email-template.md", "template-followup"))

    parts.append(divider("Checklists", ""))
    parts.append(section(f"{cl}/14-thirty-day-checklist.md", "checklist-30-day"))

    return "\n".join(parts)


if __name__ == "__main__":
    print(build())
