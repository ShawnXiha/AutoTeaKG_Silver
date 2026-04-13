# Formal Peer Review of AutoTeaKG-Silver v3

Date: 2026-04-12

Manuscript: `AutoTeaKG-Silver: An Uncertainty-Aware Evidence Graph for Tea Functional Activity Literature`

## Summary Statement

The manuscript presents AutoTeaKG-Silver, an automatically generated silver-standard evidence graph for tea functional activity literature. The system converts PubMed records and open full-text methods sections into structured evidence records and a provenance-rich KG with evidence-level, activity, processing, extraction, microbiome, and uncertainty attributes. The work is promising as a resource and workflow paper, but it needs stronger validation and a clearer demonstration of graph utility before it would be competitive for a strong informatics or database venue.

Overall recommendation: **major revision before submission**.

## Key Strengths

1. **Clear domain gap.** The manuscript convincingly argues that tea functional activity evidence is fragmented and that existing tea resources focus on genomics, transcriptomics, risky substances, or narrative reviews.
2. **Appropriate silver-standard framing.** The paper avoids overclaiming expert verification and instead treats uncertainty and provenance as first-class outputs.
3. **Reproducible artifact structure.** The manuscript lists scripts, outputs, query tables, figures, and final KG paths.
4. **Strong figure set.** The figures communicate scale, evidence distribution, context recovery, uncertainty composition, and full-text availability.
5. **Useful negative finding.** The processing-context recovery result shows that missing context is caused partly by reporting and full-text availability, not only by extraction failure.

## Major Comments

### 1. Extraction quality is not yet evaluated.

The manuscript reports construction and coverage metrics, but it does not report field-level correctness. For an automatically generated evidence graph, reviewers will ask how often the LLM and rule-based pipeline extracted correct tea type, component group, activity category, study type, evidence level, processing step, extraction method, mechanism, and uncertainty label.

Recommended revision:

- Add a small validation section with 30-50 sampled records.
- Report field-level accuracy or accept / accept-with-correction / reject rates.
- If manual validation is intentionally excluded from data generation, state that validation is external and does not train or construct the KG.

### 2. The graph utility claim is under-demonstrated.

The manuscript says the graph supports microbiome mechanism queries, but v3 mostly reports graph composition and query-table existence. A reviewer may conclude that the same insights could be obtained from CSV tables.

Recommended revision:

- Add one concrete graph query case study.
- Example: query `tea polysaccharides -> gut microbiota modulation -> microbial metabolite -> host phenotype` and show the resulting subgraph or table.
- Add a small comparison showing what the graph query retrieves that a flat keyword search would not.

### 3. Baselines and ablations are insufficient.

The pipeline has natural ablations: rules-only, abstract-level LLM, abstract + methods LLM, and vocabulary-normalized KG. The context coverage figure shows some stage-wise gains, but the manuscript does not frame these as ablations or report enough quality-control metrics.

Recommended revision:

- Add an "Ablation and quality-control summary" table.
- Include processing coverage, extraction coverage, missing-context count, unresolved KG edges, unmapped labels, low/moderate/high uncertainty counts, and patch errors after retry.

### 4. Related Work is useful but incomplete for text mining and knowledge graph venues.

The Related Work covers tea bioactivity, tea resources, and natural-product resources. It should also discuss biomedical text mining, LLM-based information extraction, and scientific knowledge graph construction. Without these references, reviewers may see the method as under-contextualized.

Recommended revision:

- Add one paragraph on biomedical/scientific IE and KG construction.
- Add one paragraph on LLM-assisted extraction with validation and uncertainty.
- Cite real papers only after verification.

### 5. The uncertainty model needs more formal definition.

The manuscript states that records are assigned uncertainty flags and classes, but the exact criteria are not described in enough detail. Since uncertainty-aware KG construction is part of the title and novelty, this needs a formal table.

Recommended revision:

- Add a table of uncertainty flags with triggers and interpretation.
- Define how `low`, `moderate`, and `high` uncertainty are assigned.
- Clarify whether uncertainty is record-level, edge-level, or both.

## Minor Comments

1. The Abstract is strong but long. Consider shortening the first sentence and moving one numeric detail to the Results.
2. The title is accurate but could be more specific about "automatic" or "silver-standard".
3. The Methods section should define "patch" before using patch-related terminology.
4. The phrase "living tea bioactivity synthesis" is compelling but should be defined or softened.
5. The Results section should refer to Table 2 directly when introducing the KG scale.
6. The Appendix path table is useful, but for a journal submission it may be better as Supplementary Table S1.
7. The remaining overfull hbox is minor but should be fixed before final formatting.
8. The paper currently lacks a data/code availability statement.
9. The paper currently lacks an LLM usage statement, which may be required by some venues.
10. If this is submitted to a biomedical or food science venue, specify whether any ethical approval is not applicable because the work uses public literature only.

## Reproducibility Assessment

Current reproducibility is above average for a draft. The manuscript lists scripts and outputs, and the project directory includes query tables and figure files. However, it still needs:

- software versions or environment information,
- exact command sequence for regenerating KG v3,
- data/code availability statement,
- release archive or DOI plan,
- explicit note that API keys are required for GLM5 regeneration.

## Figure and Table Assessment

The figures are generally clear and useful. The strongest figures are the activity-evidence heatmap, context coverage chart, and KG composition chart. The weakest figure is the missing-context burden chart if used alone, because it duplicates the context recovery message. The graphical abstract is useful for orientation but should be visually checked after venue conversion.

## Ethical and Reporting Considerations

No human or animal subjects are directly studied by this paper; it analyzes public literature and open full-text records. The manuscript should explicitly state this. The use of GLM5 and automated extraction should be disclosed with enough detail to satisfy venue AI-tool policies.

## Final Recommendation

The paper is a strong working draft but not yet submission-ready. It should move to v4 with three additions before serious venue targeting:

1. extraction-quality validation,
2. graph query case study,
3. uncertainty-model formalization.

After these additions, the work would be suitable to position as a resource/informatics paper rather than a purely algorithmic ML paper.
