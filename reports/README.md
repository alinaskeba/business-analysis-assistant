# Submission materials

- Evaluation_Report.docx: one editable consolidated evaluation report; matching Markdown source.
- Project_Report.docx: editable project report with CRISP-DM, architecture, results and limitations.
- diagrams/system_diagram.png: high-resolution image for Word/slides.
- diagrams/system_diagram.svg: scalable vector diagram with editable text.
- diagrams/system_diagram.pdf: vector diagram for print and PDF composition.
- diagrams/system_diagram.mmd: editable Mermaid source.
- figures/: the six existing evaluation plots in PNG/SVG.
- component_review.json: per-record retrospective dev review with original source evidence.
- test_metrics.json: preserved final-test/assisted-branch metrics with explicit scope.

All prose is English, matching the project language. Word headings, paragraphs and tables are native
editable content; diagrams/plots are embedded images, with separate vector/source files for editing.
Semantic judgments use one assistant-assisted assessment without an independent second-rating study.
Historical outputs are separated from final-test evidence. Building the reports makes no API calls.

Rebuild with `python build_submission.py` (matplotlib, numpy and Pillow are used for figures).
DOCX generation uses standard-library OOXML and does not require Microsoft Word or python-docx.
Historical outputs, frozen system code and approved test labels remain unchanged.
