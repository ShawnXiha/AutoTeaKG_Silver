# v9 Revision Plan for AutoTeaKG-Silver

Date: 2026-04-25

Inputs:

- `reviews/PAPER_REVIEW_v8.md`
- `reviews/PEER_REVIEW_v8.md`
- v8 manuscript and compile log

## Revision Goal

Move v8 from a strong working submission draft to a cleaner first-submission package by reducing overclaim risk, fixing stale text, improving validation transparency, and making graph utility harder to dismiss.

## Priority 1: Bound the Validation Claim

Problem:

The title and abstract may imply broader validation than the 47-record stratified sample supports.

Actions:

1. Decide whether to keep `Validated` in the title.
2. Add "stratified" and "completed field judgments" where validation percentages are reported.
3. Add one sentence in Limitations noting the validation sample size and lack of full-graph manual verification.

Expected manuscript changes:

- Title or abstract wording.
- Results validation paragraph.
- Limitations section.

## Priority 2: Fix Stale and Reader-Facing Metadata

Problem:

The appendix still says validation results should be reported only after worksheet completion, and Data Availability uses an SSH repository URL.

Actions:

1. Replace `git@github.com:ShawnXiha/AutoTeaKG_Silver.git` with `https://github.com/ShawnXiha/AutoTeaKG_Silver`.
2. Update Supplementary Data: Validation Sample to describe completed validation artifacts.
3. Add paths to `validation_results_v4.json`, `validation_results_by_field_v4.csv`, and cleaned worksheet.

Expected manuscript changes:

- Data and Code Availability.
- Appendix validation section.

## Priority 3: Add Graph-vs-Flat-Retrieval Comparison

Problem:

The graph utility case is clear but still illustrative. Reviewers may ask why a graph is needed.

Actions:

1. Create a small query comparison table.
2. Compare graph query with a simple flat keyword query for the tea-polysaccharide microbiome case.
3. Report which constraints are preserved: component, metabolite, phenotype, evidence level, uncertainty, provenance.

Expected output:

- `data/graph_vs_flat_query_comparison_v9.csv`
- `drafts/v9_snippets/graph_vs_flat_query_table.tex`

Expected manuscript changes:

- Add one paragraph in the graph utility Results subsection.
- Optionally add table to Supplement if main text is crowded.

## Priority 4: Add Validation Error Analysis

Problem:

The manuscript mentions major issue categories but does not summarize them.

Actions:

1. Add a compact table of major issue category counts.
2. Add one sentence interpreting the dominant error type.
3. If available, add validation-by-uncertainty-class summary.

Expected output:

- `data/validation_error_summary_v9.csv`
- `drafts/v9_snippets/validation_error_summary_table.tex`

Expected manuscript changes:

- Add one compact Results paragraph after validation table.
- Add detailed table to Supplement if main text is crowded.

## Priority 5: Layout and Figure/Table Polish

Problem:

v8 compiles cleanly but still has overfull/underfull warnings.

Actions:

1. Shorten the long Results subsection title.
2. Convert graph query table to smaller font or supplementary longtable-style table.
3. Shorten appendix uncertainty flag severity labels or widen the severity column.
4. Decide whether claim-evidence map stays in Introduction or moves to Supplement.

Expected manuscript changes:

- Fewer overfull warnings.
- Cleaner main-text flow.

## Priority 6: Optional Reproducibility Detail

Problem:

Pipeline-level reproducibility is good, but prompt/schema details are not visible enough in the manuscript.

Actions:

1. Add a supplementary schema table listing fields, controlled vocabulary status, and source.
2. Add a short note pointing to prompt/script files.

Expected output:

- `drafts/v9_snippets/extraction_schema_summary_table.tex`

## v9 Success Criteria

- No stale validation appendix sentence.
- HTTPS repository link appears in manuscript.
- Validation rates are explicitly tied to completed field judgments.
- Graph utility has a flat-retrieval contrast.
- Validation error categories are summarized.
- No undefined citations or references.
- Overfull warnings reduced or justified.

## Recommended Work Order

1. Fix wording and stale metadata.
2. Generate graph-vs-flat comparison table.
3. Generate validation error summary table.
4. Edit v9 manuscript.
5. Recompile and check log.
6. Commit and push v9.
