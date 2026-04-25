# AutoTeaKG-Silver Paper Draft Summary

Date: 2026-04-12

## Main Deliverables

- Latest final PDF: `final/AutoTeaKG_Silver_v9_database.pdf`
- Latest final TeX: `final/AutoTeaKG_Silver_v9_database.tex`
- Previous PDF: `final/AutoTeaKG_Silver_v8_database.pdf`
- Previous TeX: `final/AutoTeaKG_Silver_v8_database.tex`
- Previous PDF: `final/AutoTeaKG_Silver_v8_database.pdf`
- Previous TeX: `final/AutoTeaKG_Silver_v8_database.tex`
- Previous PDF: `final/AutoTeaKG_Silver_v8_database.pdf`
- Previous TeX: `final/AutoTeaKG_Silver_v8_database.tex`
- Previous PDF: `final/AutoTeaKG_Silver_v7_database.pdf`
- Previous TeX: `final/AutoTeaKG_Silver_v7_database.tex`
- Previous PDF: `final/AutoTeaKG_Silver_v6_database.pdf`
- Previous TeX: `final/AutoTeaKG_Silver_v6_database.tex`
- Previous PDF: `final/AutoTeaKG_Silver_v5.pdf`
- Previous TeX: `final/AutoTeaKG_Silver_v5.tex`
- Previous PDF: `final/AutoTeaKG_Silver_v4.pdf`
- Previous TeX: `final/AutoTeaKG_Silver_v4.tex`
- Previous PDF: `final/AutoTeaKG_Silver_v3.pdf`
- Previous TeX: `final/AutoTeaKG_Silver_v3.tex`
- Previous PDF: `final/AutoTeaKG_Silver_v2.pdf`
- Previous TeX: `final/AutoTeaKG_Silver_v2.tex`
- Previous PDF: `final/AutoTeaKG_Silver_v1.pdf`
- Previous TeX: `final/AutoTeaKG_Silver_v1.tex`
- Editable draft: `drafts/v1_draft.tex`
- Latest editable draft: `drafts/v9_database_draft.tex`
- References: `references/references.bib`
- Figures: `figures/`
- Figure-ready tables: `data/`

## Draft Scope

Title:

`AutoTeaKG-Silver: A Validated Silver-Standard Evidence Graph for Tea Functional Activity Literature`

Core framing:

AutoTeaKG-Silver is an automatically generated, provenance-rich, uncertainty-aware silver-standard evidence graph for tea functional activity literature. It is positioned as an automated evidence infrastructure, not as a manually verified gold-standard database.

## Current Quantitative Claims

- 635 evidence records
- 1,989 KG nodes
- 8,195 KG edges
- 190 microbiome-relevant records
- Processing context: 146 -> 183 records
- Extraction context: 154 -> 185 records
- Residual missing processing/extraction context after methods extraction: 303 records

## Figures Included

- Graphical abstract / pipeline overview
- KG composition
- Activity-by-evidence heatmap
- Context coverage by extraction stage
- Full-text methods availability funnel
- Processing/extraction label distribution
- Uncertainty by activity
- Evidence-quality dashboard
- Graph utility case diagram

## QA

- `pdflatex -> bibtex -> pdflatex -> pdflatex` completed through v8 Database-oriented draft.
- Final v8 Database-oriented PDF generated successfully.
- Citation keys checked against BibTeX: no missing keys.
- LaTeX log checked: no undefined citations or references.
- v8 Database-oriented draft length: 3,955 words by `texcount -1 -sum`.
- v8 Database-oriented PDF length: 18 pages.
- v9 Database-oriented PDF length: 20 pages.

## v2 Additions

- Added standalone `Related Work`.
- Added Methods table summarizing reproducible construction stages.
- Added `Reproducibility package` subsection with final KG, query-table, and figure-generation paths.

## v3 Additions

- Compressed the pipeline-stage table for cleaner layout.
- Added a compact Results table of final KG v3 statistics.
- Moved detailed reproducibility paths to an appendix.
- Reduced major layout warnings; only one small overfull hbox remains.

## v4 Additions

- Added Methods paragraph formalizing the uncertainty model.
- Added main-text uncertainty-class table.
- Added Results stage-wise ablation / quality-control table.
- Added Appendix uncertainty flag definitions.
- Added graph query case study for tea polysaccharide microbiome/gut-liver paths.
- Added external validation protocol and 48-record stratified validation sample.
- Generated `data/uncertainty_flags_v4.csv` and `data/stagewise_qc_v4.csv`.
- Generated `data/graph_query_case_study_polysaccharide_microbiome_v4.csv`.
- Generated `data/validation_v4/validation_sample_v4.csv` and `data/validation_v4/validation_worksheet_v4.csv`.
- v4 compiles with no undefined citations or references. Some table overfull warnings remain and should be polished during camera-ready formatting.

## v5 Additions

- Added `Data and Code Availability`.
- Added `LLM Usage Statement`.
- Added `Ethics Statement`.
- Marked data/code availability and LLM usage statement as completed in the v4 action matrix.
- v5 compiles with no undefined citations or references. Some table overfull warnings remain and should be polished during camera-ready formatting.

## v6 Database-Oriented Additions

- Added Database URL after the abstract.
- Folded Related Work into the Introduction as `Prior work and resource gap`.
- Renamed appendices as `Supplementary Data` sections.
- Converted long appendix tables to `tabularx` where useful.
- Added `reviews/VENUE_CONVERSION_NOTE_v6.md`.
- Marked venue conversion and appendix refinement as completed in the action matrix.
- v6 compiles with no undefined citations or references. Minor table layout warnings remain for camera-ready polish.

## v7 Database-Oriented Additions

- Integrated completed external validation results from 47 reviewed records.
- Added validation-results sentence to the abstract.
- Added a dedicated Results subsection for field-level validation.
- Validation artifacts now include:
  - `reviews/VALIDATION_RESULTS_v4.md`
  - `data/validation_v4/validation_results_by_field_v4.csv`
  - `data/validation_v4/validation_results_v4.json`
- The v4 action matrix now marks extraction-quality validation as completed.

## v8 Database-Oriented Additions

- Applied `$paper-writing` section-level polish across title, abstract, Introduction, Methods, Results, Discussion, Limitations, and Conclusion.
- Added a claim--evidence map table to make the main claims auditable against figure and table anchors.
- Added a new evidence-quality dashboard figure summarizing resource scale, context recovery, evidence-level distribution, and external validation.
- Added a clearer graph utility case diagram showing multi-field query constraints, EvidenceRecord provenance, and returned evidence paths.
- Replaced the longer validation table with a compact field-level validation table in the main text.
- Added reproducible generation script: `scripts/create_v8_polished_manuscript.py`.
- Recompiled successfully with no undefined citations or references. Minor overfull warnings remain in long tables and one long subsection title.


## v9 Database-Oriented Additions

- Bounded validation wording to the stratified validation sample and completed field judgments.
- Replaced the reader-facing repository URL with HTTPS.
- Fixed stale validation appendix wording and added completed validation artifact paths.
- Added graph-vs-flat keyword retrieval comparison for the tea-polysaccharide microbiome case.
- Added validation error summary and validation-by-uncertainty supplementary tables.
- Added an extraction schema summary table to Supplementary Data.
- Shortened one long Results subsection heading and tightened table layout.
- Recompiled successfully with no undefined citations or references.

## Review Artifacts

- Paper self-review v8: `reviews/PAPER_REVIEW_v8.md`
- Formal peer review v8: `reviews/PEER_REVIEW_v8.md`
- v9 revision plan: `reviews/REVISION_PLAN_v9.md`
- v9 action matrix: `reviews/revision_action_matrix_v9.csv`
- Paper self-review: `reviews/PAPER_REVIEW_v3.md`
- Formal peer review: `reviews/PEER_REVIEW_v3.md`
- ScholarEval scoring: `reviews/SCHOLAR_EVALUATION_v3.md`
- v4 revision plan: `reviews/REVISION_PLAN_v4.md`
- v4 action matrix: `reviews/revision_action_matrix_v4.csv`

## Highest-Priority v4 Tasks

1. Extraction-quality validation. **Completed on 2026-04-25 and integrated into v7.**
2. Add one graph query case study. **Completed on 2026-04-25 and integrated into v7.**
3. Formalize the uncertainty model. **Completed.**
4. Add a stage-wise ablation / quality-control table. **Completed.**
5. Expand computational related work. **Completed.**

## Computational Related Work Collection

- Verified BibTeX: `references/computational_related_work_refs.bib`
- Merged main BibTeX: `references/references.bib`
- Verification notes: `sources/papers_20260412_computational_related_work_verified.md`
- Mini literature review and insertion guide: `sources/literature_review_20260412_computational_related_work.md`
- Added 13 verified references covering scientific IE, LLM extraction, biomedical IE resources, scientific/biomedical language models, biomedical KGs, and LLM KG construction.

## Next Revision Priorities

1. Camera-ready layout polish for long tables and appendix pages.
2. Decide whether to keep the validation table in the main paper or move it to supplement for page-limited venues.
3. Choose the final target venue and adapt to the official template.
4. Prepare cover letter / submission package.
5. If desired, add one more graph utility example beyond the tea-polysaccharide gut-liver case.
