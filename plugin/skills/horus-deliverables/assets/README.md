# Horus templates

The neutral Horus design system (`../references/design-system.md`) is implemented as:

- `horus-neutral-v1.pptx`: the deck master, built with the `pptx` skill during build step 5 from the type scale, grid, palette, tracker, stamp and source-line conventions. Until the file exists the producer applies the rules programmatically.
- `horus-neutral-v1.docx`: the document template (numbered paragraphs, 12 pt body, exhibit captions as full sentences, confidentiality mark in the header).
- `chart-theme.json`: colours and typography for charts produced by the appraisal toolkit (`horus_appraisal.report`) and by the pptx skill.

Brand assets (logo, colours, typeface) replace the neutral values when the Supervisor provides them (decision 7 in docs/DECISIONS.md).
