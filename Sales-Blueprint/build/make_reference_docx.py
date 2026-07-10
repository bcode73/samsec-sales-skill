#!/usr/bin/env python3
"""Builds build/reference.docx: pandoc's default reference doc, restyled to
match the book's brand (deep teal headings, charcoal body, serif body text,
6in x 9in page size). Run once; pandoc uses the result via --reference-doc."""
import os
import subprocess
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
REF_PATH = f"{BUILD_DIR}/reference.docx"

TEAL = RGBColor(0x0F, 0x3D, 0x3E)
CHARCOAL = RGBColor(0x1B, 0x1F, 0x1E)
GREY = RGBColor(0x4A, 0x4A, 0x44)

BODY_FONT = "Cambria"
HEADING_FONT = "Calibri"


def style_font(style, name=None, size=None, color=None, bold=None):
    f = style.font
    if name:
        f.name = name
    if size:
        f.size = size
    if color:
        f.color.rgb = color
    if bold is not None:
        f.bold = bold


def main():
    subprocess.run(
        ["pandoc", "-o", REF_PATH, "--print-default-data-file", "reference.docx"],
        check=True,
    )
    d = docx.Document(REF_PATH)
    by_name = {s.name: s for s in d.styles}

    style_font(by_name["Normal"], name=BODY_FONT, size=Pt(11), color=CHARCOAL)
    by_name["Normal"].paragraph_format.line_spacing = 1.3
    by_name["Normal"].paragraph_format.space_after = Pt(8)

    style_font(by_name["Body Text"], name=BODY_FONT, size=Pt(11), color=CHARCOAL)
    style_font(by_name["First Paragraph"], name=BODY_FONT, size=Pt(11), color=CHARCOAL)
    style_font(by_name["Compact"], name=BODY_FONT, size=Pt(11), color=CHARCOAL)

    style_font(by_name["Title"], name=HEADING_FONT, size=Pt(30), color=TEAL, bold=True)
    by_name["Title"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style_font(by_name["Subtitle"], name=HEADING_FONT, size=Pt(14), color=TEAL, bold=False)
    by_name["Subtitle"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style_font(by_name["Author"], name=HEADING_FONT, size=Pt(13), color=GREY)
    by_name["Author"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    style_font(by_name["Heading 1"], name=HEADING_FONT, size=Pt(20), color=TEAL, bold=True)
    style_font(by_name["Heading 2"], name=HEADING_FONT, size=Pt(14), color=TEAL, bold=True)
    style_font(by_name["Heading 3"], name=HEADING_FONT, size=Pt(12), color=TEAL, bold=True)
    for h in ("Heading 1", "Heading 2", "Heading 3"):
        by_name[h].paragraph_format.space_before = Pt(18)
        by_name[h].paragraph_format.space_after = Pt(6)
        by_name[h].paragraph_format.keep_with_next = True

    # Every major section (front-matter file, module, worksheet, template,
    # checklist, part divider) starts with exactly one Heading 1. Forcing
    # the break here, on the heading itself, guarantees exactly one page
    # break per section regardless of how the previous section's content
    # happens to fill its last page. A separately inserted manual page-break
    # paragraph doesn't have that guarantee: if the prior content happens to
    # end exactly at the bottom of a page, the manual break paragraph has to
    # start its own (blank) page before it can force the next one.
    by_name["Heading 1"].paragraph_format.page_break_before = True

    style_font(by_name["Image Caption"], name=HEADING_FONT, size=Pt(9), color=CHARCOAL)
    style_font(by_name["Caption"], name=HEADING_FONT, size=Pt(9), color=CHARCOAL)

    # Table style: header row background + borders are set via table style XML;
    # python-docx's high-level API doesn't expose shading, so leave pandoc's
    # default "Table" style (clean grid) in place rather than fight the XML.

    # Page size: 6in x 9in, comfortable margins for an editable working doc.
    for section in d.sections:
        section.page_width = Inches(6)
        section.page_height = Inches(9)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)

    d.save(REF_PATH)
    print("wrote", REF_PATH)


if __name__ == "__main__":
    main()
