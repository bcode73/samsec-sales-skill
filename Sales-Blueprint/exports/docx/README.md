# DOCX Export

**`sales-blueprint.docx`**: a genuinely editable Word document, generated from the manuscript with the pipeline in `/build` (see `build/README.md`, "DOCX build pipeline"). Unlike the PDF, this file is meant to be opened and edited directly. Real Word paragraph and heading styles (not floating text boxes), native tables, embedded diagram images with captions, an auto-updating page-number footer, and a plain-list table of contents. 249 pages at 6in x 9in in Word's default view; the exact count will drift as it's edited, which is expected for a reflowable document.

If changes made directly in this file need to flow back into the manuscript source (`manuscript/`, `worksheets/`, `templates/`, `checklists/`), that has to happen by hand; there is no reverse pipeline from docx back to Markdown.
