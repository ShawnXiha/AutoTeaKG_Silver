# AutoTeaKG-Silver Paper Draft Summary

Date: 2026-04-12

## Main Deliverables

- Latest final PDF: `final/AutoTeaKG_Silver_v5.pdf`
- Latest final TeX: `final/AutoTeaKG_Silver_v5.tex`
- Previous PDF: `final/AutoTeaKG_Silver_v4.pdf`
- Previous TeX: `final/AutoTeaKG_Silver_v4.tex`
- Previous PDF: `final/AutoTeaKG_Silver_v3.pdf`
- Previous TeX: `final/AutoTeaKG_Silver_v3.tex`
- Previous PDF: `final/AutoTeaKG_Silver_v2.pdf`
- Previous TeX: `final/AutoTeaKG_Silver_v2.tex`
- Previous PDF: `final/AutoTeaKG_Silver_v1.pdf`
- Previous TeX: `final/AutoTeaKG_Silver_v1.tex`
- Editable draft: `drafts/v1_draft.tex`
- Latest editable draft: `drafts/v5_draft.tex`
- References: `references/references.bib`
- Figures: `figures/`
- Figure-ready tables: `data/`

## Draft Scope

Title:

`AutoTeaKG-Silver: An Uncertainty-Aware Evidence Graph for Tea Functional Activity Literature`

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

## QA

- `pdflatex -> bibtex -> pdflatex -> pdflatex` completed for v1, v2, v3, v4, and v5.
- Final v5 PDF generated successfully.
- Citation keys checked against BibTeX: no missing keys.
- LaTeX log checked: no undefined citations or references.
- v5 draft length: 4,699 words.

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

## Review Artifacts

- Paper self-review: `reviews/PAPER_REVIEW_v3.md`
- Formal peer review: `reviews/PEER_REVIEW_v3.md`
- ScholarEval scoring: `reviews/SCHOLAR_EVALUATION_v3.md`
- v4 revision plan: `reviews/REVISION_PLAN_v4.md`
- v4 action matrix: `reviews/revision_action_matrix_v4.csv`

## Highest-Priority v4 Tasks

1. Add extraction-quality validation.
2. Add one graph query case study.
3. Formalize the uncertainty model.
4. Add a stage-wise ablation / quality-control table.
5. Expand computational related work. **Completed as a reference collection task on 2026-04-12; integration into v4 manuscript remains.**

## Computational Related Work Collection

- Verified BibTeX: `references/computational_related_work_refs.bib`
- Merged main BibTeX: `references/references.bib`
- Verification notes: `sources/papers_20260412_computational_related_work_verified.md`
- Mini literature review and insertion guide: `sources/literature_review_20260412_computational_related_work.md`
- Added 13 verified references covering scientific IE, LLM extraction, biomedical IE resources, scientific/biomedical language models, biomedical KGs, and LLM KG construction.

## Next Revision Priorities

1. Add a formal Related Work section.
2. Add a compact table of dataset construction stages.
3. Tighten Methods with exact commands/scripts and release paths.
4. Decide target venue/journal style and convert template if needed.
5. Add supplementary material for query tables and schema details.
