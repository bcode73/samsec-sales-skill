# Build pipelines

Two independent pipelines turn the Markdown manuscript into reader-facing files. Neither runs automatically; run by hand when the manuscript changes and a new export is needed.

- **PDF** (`exports/pdf/sales-blueprint.pdf`): fixed layout, for reading and for the Selar listing. See "PDF build pipeline" below.
- **DOCX** (`exports/docx/sales-blueprint.docx`): a genuinely editable Word document, for the author to revise directly. See "DOCX build pipeline" further down.

## PDF build pipeline

## Requirements

- Python 3 with `pip install markdown pymdown-extensions`
- Node with `npm install playwright` (run from this directory, or anywhere and adjust the import path)
- A Chromium binary Playwright can launch. If `npx playwright install chromium` isn't practical, point `render_pdf.mjs`'s `chromium.launch()` at an existing Chromium build's `executablePath` instead of downloading a new one.
- `@mermaid-js/mermaid-cli`, run via `npx` (no separate install needed)

## Steps

1. **Render the diagrams to images.** From the repo root:

   ```
   mkdir -p build/diagram-images
   for f in visuals/diagrams/*.mmd visuals/charts/*.mmd; do
     name=$(basename "$f" .mmd)
     npx -y @mermaid-js/mermaid-cli -i "$f" -o "build/diagram-images/${name}.png" \
       -p build/puppeteer-config.json -b transparent -s 3
   done
   ```

   `build/puppeteer-config.json` should contain `{"args": ["--no-sandbox", "--disable-setuid-sandbox"]}` if running as root.

2. **Assemble the HTML.**

   ```
   cd build
   python3 build_html.py > body.html
   python3 -c "
   body = open('body.html', encoding='utf-8').read()
   css = open('style.css', encoding='utf-8').read()
   open('full.html', 'w', encoding='utf-8').write(
       f'<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"/><title>Sales Blueprint</title><style>{css}</style></head><body>{body}</body></html>'
   )
   "
   ```

3. **Render the PDF.**

   ```
   node render_pdf.mjs
   ```

   Output lands at `exports/pdf/sales-blueprint.pdf`. Page size is fixed at 6in x 9in with a small bottom margin reserved for the page-number footer (Chromium's print engine requires nonzero margin for header/footer templates, so the margin is not zero even though it looks close to full-bleed).

## What the script assumes

- `build_html.py` reads directly from `manuscript/`, `worksheets/`, `templates/`, `checklists/`, and `assets/brand/exports/front-cover.png`, in the reading order defined in its `TOC_STRUCTURE` and `build()` function. If a file is renamed or a new module/worksheet is added, update both.
- Figure callouts are matched by two patterns: the blockquote form (`> **Figure X.Y: Title.** See \`visuals/diagrams/...\`. Caption.`) used by all 14 modules, and the older italic form (`*Figure 0.1: ...*`) used once in the front matter. If a new figure callout style is introduced, extend `FIGURE_RE` / `SIMPLE_FIGURE_RE`.
- Worksheets use GitHub-style task-list checkboxes (`- [ ] text`), rendered via the `pymdownx.tasklist` extension.

## Known limitations of this first version

- The cover and part-divider pages carry a small page number in the footer margin; there is no per-page suppression of the footer (Chromium's header/footer templates apply uniformly to every page). Cosmetic only.
- No PDF bookmarks/outline are generated; navigation relies on the in-document table of contents, which is fully clickable.
- Sized for on-screen ebook reading (Selar, direct download), not for print: no bleed, no crop marks, no CMYK conversion. A print-ready version is separate future work once a print run is actually being prepared.

---

## DOCX build pipeline

Turns the same manuscript into a real, editable Word document: proper paragraph and heading styles, an editable table of contents (plain list, not a Word TOC field, see below), native Word tables, embedded images, and an auto-updating page-number footer. Converts from Markdown directly with Pandoc rather than from the PDF, which avoids the floating-text-box mess a PDF-to-Word conversion usually produces.

### Requirements

- `pandoc` (`apt-get install pandoc` or see pandoc.org)
- Python 3 with `pip install python-docx pillow` (also needs `markdown`/`pymdown-extensions` if you haven't already installed them for the PDF pipeline)
- Diagram images already rendered into `build/diagram-images/` (same step as the PDF pipeline, see above)

### Steps

1. Render the diagrams to images (same command as PDF step 1 above; `-b white` rather than `-b transparent` reads better against Word's default white canvas, but either works).
2. From `build/`, run:

   ```
   bash render_docx.sh
   ```

   This runs `build_docx_md.py` (assembles one big Pandoc-Markdown file from the manuscript, worksheets, templates, and checklists, converting figure callouts to real `![]()` images), generates `reference.docx` on first run (via `make_reference_docx.py`, which restyles Pandoc's default reference document: deep teal headings, charcoal serif body text, 6in x 9in page size), converts with `pandoc --from=markdown-smart` (the `-smart` suffix is not optional: Pandoc's default Markdown reader silently turns straight quotes into curly ones and `--`/`---` into en/em dashes, both banned by the Humanizer Pass), and finally adds a centered, auto-updating page-number field to the footer via `add_page_numbers.py` (python-docx has no built-in helper for this; it's a small raw-XML field insert).

3. Output lands at `exports/docx/sales-blueprint.docx`.

### Why the table of contents is a plain list, not a Word TOC field

Pandoc's `--toc` flag generates a genuine, native Word TOC field, which sounds better than a plain list, but it renders **blank** until the user (or an automated pass) explicitly updates it, since Word fields are not calculated until told to. For a document someone is about to open and start editing, an apparently blank first page reads as broken. A plain Markdown bullet list is always visible immediately, at the cost of not being a clickable, auto-updating field. If you'd rather have the real thing, add `--toc --toc-depth=1` back to the pandoc invocation in `render_docx.sh` and remove the `toc_page()` call in `build_docx_md.py`, and tell whoever opens the file to right-click the TOC and choose "Update Field" (or press F9) once.

### Verifying a build without Microsoft Word

`soffice --headless --convert-to pdf exports/docx/sales-blueprint.docx` (LibreOffice, `apt-get install libreoffice-writer`) renders a throwaway PDF for a quick visual check, since a `.docx` has no fixed page images of its own to inspect directly.

### Known limitations of this first version

- No table header shading (Pandoc's default docx table style is a plain grid); add it in Word with Table Design if wanted.
- Page count is not comparable to the PDF's; Word reflows text differently (line spacing, font metrics), so it will differ and will keep changing as the user edits.
- Part-divider pages are a plain heading and subheading, not a full-bleed dark teal page; Word doesn't support per-page background colour, only one background for the whole document.

### Two defects fixed after the first version

The first DOCX build had two real bugs that only became visible once the file was actually converted to a fixed-page format (LibreOffice/print-to-PDF), since Word's on-screen view is more forgiving about both:

- **Oversized images.** `mermaid-cli` renders diagrams at a high pixel scale for print sharpness (many came out 15-25in wide at 96dpi). Pandoc embeds images at their native size unless told otherwise, so every figure was placed far larger than the page and got clipped by whatever renderer eventually produced a fixed page. Fixed in `build_docx_md.py`: `figure_size()` reads each image's actual pixel dimensions with Pillow and computes an explicit `{width=...in}` so every figure fits within one page (4.3in wide, capped at 6.3in tall, whichever is more restrictive for that image's aspect ratio) regardless of which program renders it.
- **Occasional blank page between sections.** Every major section (front-matter file, module, worksheet, template, checklist, divider) was preceded by a manually inserted raw-XML page break. That works most of the time, but if the previous section's content happened to end exactly at the bottom of a page, the manual break paragraph had nowhere to sit except the start of a new, otherwise-empty page before it could force the next one, producing a genuinely blank page. Fixed by removing the manual breaks and instead setting `page_break_before` on the "Heading 1" style in `make_reference_docx.py`; since every section starts with exactly one Heading 1, this guarantees exactly one break per section with no dependence on how full the previous page happened to be.
