# Revision Notes

## v2

Date: 2026-04-12

Changes from v1:

- Added a standalone `Related Work` section.
- Added a reproducible pipeline-stage table in Methods.
- Added a `Reproducibility package` subsection listing final KG paths, query tables, and figure-generation script.
- Preserved the auto-only/silver-standard framing.
- Reused only citation keys already present in `references/references.bib`.

## v3

Date: 2026-04-12

Changes from v2:

- Compressed the reproducibility pipeline table to reduce overfull layout issues.
- Added a compact Results table with final KG v3 summary statistics.
- Moved detailed reproducibility paths into an appendix.
- Recompiled successfully with no undefined citations or references.

## v4

Date: 2026-04-12

Changes from v3:

- Added an uncertainty model paragraph to Methods.
- Added a main-text uncertainty-class assignment table.
- Added stage-wise ablation / quality-control table to Results.
- Added Appendix table defining uncertainty flags, triggers, interpretation, and severity.
- Added v4 data outputs: `data/uncertainty_flags_v4.csv` and `data/stagewise_qc_v4.csv`.
- Added a graph query case study for tea polysaccharides, microbiota/metabolites, and host phenotypes.
- Added external validation protocol and a stratified 48-record validation sample.
- Recompiled successfully with no undefined citations or references.

## v5

Date: 2026-04-13

Changes from v4:

- Added `Data and Code Availability`.
- Added `LLM Usage Statement`.
- Added `Ethics Statement`.
- Recompiled successfully with no undefined citations or references.

## v6 Database-oriented

Date: 2026-04-13

Changes from v5:

- Added Database URL after the abstract.
- Folded Related Work into the Introduction as `Prior work and resource gap`.
- Converted appendix headings to `Supplementary Data` sections.
- Converted long appendix tables to `tabularx` where appropriate.
- Added `reviews/VENUE_CONVERSION_NOTE_v6.md`.
- Recompiled successfully with no undefined citations or references.

## v7 Database-oriented

Date: 2026-04-25

Changes from v6:

- Integrated completed external validation results from the 47-record reviewed sample.
- Added validation results sentence to the abstract.
- Updated Methods from `External validation protocol` to completed `External validation`.
- Added a Results subsection reporting field-level validation performance.
- Recompiled successfully with no undefined citations or references.

## v8 Database-oriented

Date: 2026-04-25

Changes from v7:

- Revised the title to emphasize the validated silver-standard resource positioning.
- Rewrote the abstract using a challenge-to-contribution structure and more conservative claim language.
- Added a claim--evidence map table in the Introduction.
- Tightened the uncertainty-method description to remove repetition and clarify evidence-record-level propagation.
- Added an evidence-quality dashboard figure that combines resource scale, context recovery, activity-by-evidence structure, and validation performance.
- Added a graph utility case diagram that makes the multi-field query logic more explicit.
- Replaced the detailed validation table in the main text with a compact validation table.
- Revised Results, Discussion, Limitations, and Conclusion to anchor claims to figures/tables and state scope boundaries more explicitly.
- Added `scripts/create_v8_polished_manuscript.py` to regenerate the v8 figures, snippets, manuscript, and final PDF.
- Recompiled successfully with no undefined citations or references.
