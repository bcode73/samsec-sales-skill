# DOCX Export

**`sales-blueprint.docx`**: a genuinely editable Word document, generated from the manuscript with the pipeline in `/build` (see `build/README.md`, "DOCX build pipeline"). Unlike the PDF, this file is meant to be opened and edited directly. Real Word paragraph and heading styles (not floating text boxes), native tables, embedded diagram images sized to fit their page, an auto-updating page-number footer, and a plain-list table of contents. 246 pages at 6in x 9in in Word's default view; the exact count will drift as it's edited, which is expected for a reflowable document.

Verified page-by-page (via a throwaway LibreOffice-rendered PDF, since a `.docx` has no fixed pages of its own): no clipped or oversized diagrams, and no blank pages between sections. Both were real defects in the first version of this file, caused by images embedded at their native (much too large) pixel size and by an occasional double page break; see "Two defects fixed after the first version" in `build/README.md` for the detail.

If changes made directly in this file need to flow back into the manuscript source (`manuscript/`, `worksheets/`, `templates/`, `checklists/`), that has to happen by hand; there is no reverse pipeline from docx back to Markdown.
