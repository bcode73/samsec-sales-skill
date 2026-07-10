#!/usr/bin/env bash
# Builds exports/docx/sales-blueprint.docx from the manuscript.
# Requires: pandoc, python3 with `markdown` and `python-docx` installed,
# and diagram images already rendered into build/diagram-images/
# (see the "Render the diagrams" step in build/README.md).
set -euo pipefail
cd "$(dirname "$0")"

python3 build_docx_md.py > combined.md

if [ ! -f reference.docx ]; then
  python3 make_reference_docx.py
fi

pandoc --from=markdown-smart combined.md -o ../exports/docx/sales-blueprint.docx --reference-doc=reference.docx

python3 add_page_numbers.py ../exports/docx/sales-blueprint.docx

echo "Done: exports/docx/sales-blueprint.docx"
