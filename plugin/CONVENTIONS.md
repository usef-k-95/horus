# Plugin content conventions

These rules apply to every file under `plugin/skills/`.

- **Audience**: the Horus Principal (a senior policy consultant) and its workers. Write as a crisp operating manual, not as a textbook. Sentence case headings. No em-dashes.
- **Reference files** (`references/**.md`): one topic per file, 400 to 1,500 words (up to 2,500 when a complete table such as the archetype library or the document structures requires it), starting with a two-line summary and a "when Horus uses this" line. Frameworks end with a "Source" line naming the originating organisation or author and the canonical document (no fabricated URLs; cite by name and year when unsure of the link).
- **Framework files** (`horus-method/references/frameworks/<id>.md`): sections `What it is`, `When Horus uses it`, `Steps`, `Outputs → state records` (name the collections and fields from docs/STATE_SCHEMA.md the outputs land in), `Pitfalls`, `Source`.
- **Pathway packs** (`horus-policy/references/pathways/<id>.md`): sections `Classification signals`, `Diagnostic lens`, `Option logic`, `Appraisal method` (with the appraisal `kind`, standards and toolkit modules), `Stakeholder emphasis`, `Core Tier-2 deliverables and structures`, `Gate criteria variants`, `Frameworks` (links to framework ids), `Benchmark documents` (from docs/BENCHMARKS.md), `Typical pitfalls`.
- **IDs and enumerations** must match `docs/STATE_SCHEMA.md` (collections, kinds, statuses). Do not invent new record types; propose them in a `Proposed schema additions` note at the end of the file instead.
- **Evidence discipline** applies to the content itself: no invented statistics; where a number is illustrative say so.
- Files are UTF-8 Markdown; no front matter except in `SKILL.md`.
