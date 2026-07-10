# PDF build pipeline

Turns the Markdown manuscript into `exports/pdf/sales-blueprint.pdf`. Not run automatically; run by hand when the manuscript changes and a new PDF is needed.

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
