# KG v3 Query Tables

Date: 2026-04-12

Source KG version: `reports/methods_processing_vocab_normalized`

Table directory: `reports/kg_v3_query_tables`

## Tables

- `figure_ready_summary_metrics.csv`: one-row summary for paper Results.
- `table_context_coverage_by_stage.csv`: processing/extraction context recovery across auto rules, abstract LLM, and methods LLM.
- `table_activity_evidence_counts.csv`: activity category by evidence level matrix.
- `table_activity_study_counts.csv`: activity category by study type matrix.
- `table_processing_activity_records.csv`: record-level processing context linked to activity/evidence/study labels.
- `table_extraction_activity_records.csv`: record-level extraction context linked to activity/evidence/study labels.
- `table_uncertainty_by_activity.csv`: uncertainty class counts and shares by activity category.
- `table_microbiome_mechanism_records.csv`: microbiome-relevant records with mechanism/taxon/metabolite/phenotype fields.
- `table_kg_node_edge_counts.csv`: node and edge type counts for KG v3.
- `figure_manifest.csv`: figure names and intended usage.

## Suggested Paper Uses

- Use `table_context_coverage_by_stage.csv` for Methods/Results claims about extraction gains.
- Use `table_activity_evidence_counts.csv` for the evidence-map result.
- Use `table_processing_activity_records.csv` and `table_extraction_activity_records.csv` for processing-aware examples and case studies.
- Use `table_microbiome_mechanism_records.csv` for C06/microbiome mechanism subgraph selection.
- Use `table_kg_node_edge_counts.csv` for resource statistics.

## Current Main Numbers

- Silver records: 635
- KG nodes: 1,989
- KG edges: 8,195
- Microbiome-relevant records: 190
- Records with processing context: 183
- Records with extraction context: 185
- Residual missing-context records after methods extraction: 303
