# v4 Revision Plan for AutoTeaKG-Silver

Date: 2026-04-12

Inputs:

- `reviews/PAPER_REVIEW_v3.md`
- `reviews/PEER_REVIEW_v3.md`
- `reviews/SCHOLAR_EVALUATION_v3.md`

## Revision Goal

Move the manuscript from a coherent resource-pipeline draft to a submission-ready resource/informatics paper by strengthening trust, validation, graph utility, and methodological positioning.

## Priority 0: Preserve the Current Core Framing

Keep:

- Auto-only construction as the central framing.
- Silver-standard rather than gold-standard claim.
- Provenance-rich and uncertainty-aware graph language.
- Processing/extraction context as the main measurable bottleneck.
- Full-text availability as a real limitation rather than a hidden failure.

Do not:

- Claim expert verification of every edge.
- Claim causal biological mechanisms from the KG alone.
- Claim that LLM extraction is generally accurate without validation.

## Priority 1: Add Extraction-Quality Validation

Why:

This is the most likely reviewer objection. A silver-standard KG still needs some evidence that fields are not mostly wrong.

Action:

1. Use the existing manual audit worksheet or create a smaller v4 validation sample.
2. Sample 30-50 records stratified by uncertainty class and activity category.
3. Evaluate at least these fields:
   - activity category
   - study type
   - evidence level
   - component group
   - processing step
   - extraction method
   - mechanism label
4. Report accept / accept-with-correction / reject rates.
5. State clearly that validation is external and not used to construct the KG.

Manuscript change:

- Add `Results: Extraction quality and validation`.
- Add one compact validation table.
- Add one sentence in Abstract if validation is strong enough.

Expected impact:

High. This directly improves trust and publication readiness.

## Priority 2: Add One Graph Query Case Study

Why:

The graph currently looks useful, but the paper must show what graph structure enables beyond descriptive tables.

Action:

1. Use `data/table_microbiome_mechanism_records.csv`.
2. Select one case study:
   - tea polysaccharides -> gut microbiota/metabolite -> NAFLD/inflammation,
   - tea polyphenols -> microbiota/SCFAs/barrier -> obesity,
   - oolong tea polyphenols -> gut-brain axis -> cognition.
3. Generate a small query result table or subgraph figure.
4. Compare graph query output against flat keyword retrieval in 2-3 sentences.

Manuscript change:

- Add a new Results subsection after microbiome query paragraph.
- Add a case-study figure or table.

Expected impact:

High. This protects the paper against "why KG?" criticism.

## Priority 3: Formalize the Uncertainty Model

Why:

Uncertainty-aware is in the title. The model needs to be inspectable.

Action:

1. Add a table of uncertainty flags.
2. Define each flag trigger.
3. Define low/moderate/high uncertainty classification.
4. Clarify whether flags are record-level, edge-level, or both.

Manuscript change:

- Add a Methods paragraph and an appendix table.
- Link uncertainty flags to Figure `fig_uncertainty_by_activity`.

Expected impact:

High. This makes the central method more defensible.

## Priority 4: Add Stage-Wise Ablation / Quality-Control Table

Why:

The pipeline has natural stages. Reviewers will ask which stage matters.

Action:

Create a table with rows:

- rules-only silver layer,
- abstract-level targeted extraction,
- methods-section targeted extraction,
- vocabulary-normalized final KG.

Columns:

- processing context present,
- extraction context present,
- missing context flags,
- unmapped labels,
- unresolved graph edges,
- patch errors after retry.

Manuscript change:

- Add to Results or Methods after Table 1.
- Reference it when discussing context recovery.

Expected impact:

Medium-high. It makes the pipeline look experimentally tested rather than merely implemented.

## Priority 5: Expand Computational Related Work

Why:

The current Related Work is strong on tea and natural products but thin on information extraction and scientific KGs.

Action:

Find and verify 5-8 additional citations on:

- biomedical/scientific information extraction,
- LLM-assisted literature extraction,
- knowledge graph construction from literature,
- uncertainty/provenance in biomedical KGs.

Manuscript change:

- Add one Related Work subsection: `Scientific information extraction and evidence graphs`.

Expected impact:

Medium. It will improve reviewer confidence that the authors know the computational literature.

## Priority 6: Add Data, Code, and LLM Usage Statements

Why:

Many venues require reproducibility and AI-tool disclosure.

Action:

Add short unnumbered sections or appendix notes:

- Data availability
- Code availability
- LLM/API usage
- Ethics statement: public literature only; no human/animal subjects directly studied

Expected impact:

Medium. This improves submission compliance.

## Priority 7: Venue/Template Decision

Why:

The current draft is a generic article. Final structure depends on target venue.

Recommended direction:

- Resource/database journal or computational food science venue if targeting a full paper.
- Biomedical/natural-products knowledge graph workshop if targeting faster feedback.

Action:

After v4 content improvements, choose venue and convert template.

Expected impact:

Medium. Formatting should happen after content stabilizes.

## Proposed v4 Section Changes

Add:

- `Results: Extraction quality and validation`
- `Results: Graph query case study`
- `Methods: Uncertainty model`
- `Related Work: Scientific information extraction and evidence graphs`
- `Data and Code Availability`
- `LLM Usage Statement`

Move or expand:

- Move detailed reproducibility paths to Supplement if venue is page-limited.
- Expand Appendix with uncertainty flag definitions and vocabulary mapping.

## v4 Success Criteria

The next version should satisfy:

- At least one validation table exists.
- At least one graph query case study exists.
- Uncertainty flags and classes are formally defined.
- Stage-wise quality-control table exists.
- No unsupported claim remains in Abstract or Introduction.
- No missing citations or placeholder citations.
- No undefined references in compiled PDF.

## Recommended Work Order

1. Generate validation sample and compute field-level audit metrics.
2. Generate graph query case study and figure/table.
3. Generate uncertainty flag table from code/schema.
4. Add stage-wise quality-control table.
5. Expand Related Work with verified computational citations.
6. Write v4 manuscript sections.
7. Compile and run paper-review again.
