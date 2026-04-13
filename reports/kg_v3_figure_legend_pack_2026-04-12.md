# KG v3 Figure Legend Pack

Date: 2026-04-12

Source KG version: `reports/methods_processing_vocab_normalized`

Figure directory: `figures/kg_v3`

Query table directory: `reports/kg_v3_query_tables`

## Figure 1. Context Recovery Across Extraction Stages

Files:

- `figures/kg_v3/fig_context_coverage.pdf`
- `figures/kg_v3/fig_context_coverage.png`
- `figures/kg_v3/fig_context_coverage.svg`

Caption draft:

The number of records with explicit processing and extraction context increased across the automated extraction pipeline. Rule-based extraction established the initial context layer, abstract-level targeted GLM5 extraction added additional context, and PMC methods-section extraction further improved recovery of processing and extraction variables.

Result callout:

Processing context increased from 146 to 183 records, while extraction context increased from 154 to 185 records after the full auto-only extraction workflow.

## Figure 2. Residual Missing-Context Burden

Files:

- `figures/kg_v3/fig_missing_context_burden.pdf`
- `figures/kg_v3/fig_missing_context_burden.png`
- `figures/kg_v3/fig_missing_context_burden.svg`

Caption draft:

The residual burden of records flagged as missing processing or extraction context decreased across the extraction stages, but remained substantial after methods-section extraction. This indicates that open full-text availability and reporting completeness, rather than only model capability, limit processing-aware evidence construction.

Result callout:

The missing-context flag decreased from 365 records after the initial silver layer to 303 records after methods-section extraction.

## Figure 3. Activity-by-Evidence Heatmap

Files:

- `figures/kg_v3/fig_activity_evidence_heatmap.pdf`
- `figures/kg_v3/fig_activity_evidence_heatmap.png`
- `figures/kg_v3/fig_activity_evidence_heatmap.svg`

Caption draft:

Heatmap of normalized activity categories stratified by evidence level in KG v3. The distribution shows that animal evidence and non-quantitative evidence syntheses dominate several activity categories, while human interventional and observational evidence is concentrated in fewer endpoints.

Result callout:

The evidence map makes clear that tea functional activity evidence is unevenly distributed across activity classes and study designs.

## Figure 4. Uncertainty Composition by Activity

Files:

- `figures/kg_v3/fig_uncertainty_by_activity.pdf`
- `figures/kg_v3/fig_uncertainty_by_activity.png`
- `figures/kg_v3/fig_uncertainty_by_activity.svg`

Caption draft:

Stacked uncertainty composition for each activity category. Each record was assigned an uncertainty class based on LLM confidence, schema validity, mechanism specificity, context completeness, evidence level, and taxonomy status.

Result callout:

Moderate-uncertainty records dominate the current KG, which supports treating AutoTeaKG-Silver as a provenance-rich silver-standard resource rather than a manually verified gold-standard database.

## Figure 5. Normalized Processing and Extraction Labels

Files:

- `figures/kg_v3/fig_processing_extraction_labels.pdf`
- `figures/kg_v3/fig_processing_extraction_labels.png`
- `figures/kg_v3/fig_processing_extraction_labels.svg`

Caption draft:

Top normalized processing and extraction labels after abstract-level and methods-section extraction. Vocabulary normalization reduces LLM label fragmentation by mapping surface forms such as black tea manufacturing, matcha production, brewing, isolation, and chromatographic analysis into controlled context labels.

Result callout:

Fermentation/oxidation is the dominant processing context, while extraction context remains concentrated in broad labels such as other extraction, aqueous extraction, and isolation/purification.

## Figure 6. KG v3 Composition

Files:

- `figures/kg_v3/fig_kg_composition.pdf`
- `figures/kg_v3/fig_kg_composition.png`
- `figures/kg_v3/fig_kg_composition.svg`

Caption draft:

Node and edge type composition of KG v3. The graph preserves evidence-record provenance while linking papers, activity categories, evidence levels, tea/component context, processing/extraction context, mechanisms, microbiota features, metabolites, phenotypes, and uncertainty flags.

Result callout:

KG v3 contains 1,989 nodes and 8,195 edges, with every evidence edge retaining provenance and uncertainty attributes.

## Figure 7. Full-Text Methods Availability Funnel

Files:

- `figures/kg_v3/fig_fulltext_methods_funnel.pdf`
- `figures/kg_v3/fig_fulltext_methods_funnel.png`
- `figures/kg_v3/fig_fulltext_methods_funnel.svg`

Caption draft:

Funnel of full-text methods retrieval for records that remained missing context after abstract-level extraction. Of 329 remaining records, PMC methods-like sections were available for 151 records, while 178 records lacked open PMC full text.

Result callout:

Methods-section extraction successfully patched all 151 records with available PMC methods text, but 178 records require non-PMC full text or publisher/PDF access.

## Recommended Figure Order

1. `fig_context_coverage`
2. `fig_activity_evidence_heatmap`
3. `fig_processing_extraction_labels`
4. `fig_uncertainty_by_activity`
5. `fig_kg_composition`
6. `fig_fulltext_methods_funnel`
7. `fig_missing_context_burden`

For a short paper, use Figures 1, 3, 5, and 6 as main figures and move the others to supplement.
