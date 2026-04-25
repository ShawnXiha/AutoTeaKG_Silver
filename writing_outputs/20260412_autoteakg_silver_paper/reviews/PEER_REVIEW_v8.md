# Formal Peer Review of AutoTeaKG-Silver v8

Date: 2026-04-25

Manuscript:

`AutoTeaKG-Silver: A Validated Silver-Standard Evidence Graph for Tea Functional Activity Literature`

Review mode:

- `$peer-review`
- Structured manuscript review
- Resource/database paper criteria

## Summary Statement

This manuscript presents AutoTeaKG-Silver, an automatically generated, provenance-rich evidence graph for tea functional activity literature. The work converts PubMed records into structured evidence records, normalizes activity and evidence labels, recovers processing and extraction context, assigns uncertainty classes, and exports a queryable graph with 635 records, 1,989 nodes, and 8,195 edges.

The manuscript is appropriate for a database, resource, or informatics venue. Its main strengths are the explicit silver-standard framing, provenance-aware evidence-record design, external validation sample, and useful characterization of processing/extraction reporting gaps. The main weaknesses are the limited validation scope, insufficient comparison between graph querying and simpler keyword retrieval, and several wording/layout issues that could lead reviewers to perceive overclaiming.

Recommendation:

`Major revision before submission` if targeting a selective database/bioinformatics journal.  
`Minor-to-major polish` if targeting a more applied computational food-science venue.

## Major Comments

1. The title may overstate the validation scope.

The title uses `Validated Silver-Standard Evidence Graph`, but validation covers 47 completed records and field-level completed judgments ranging from 33 to 37. This is useful validation, but not a comprehensive validation of the entire 635-record graph. The word "validated" is not wrong, but it should be bounded more carefully.

Suggested revision:

- Use `Externally Audited` or `Human-Audited` if the venue is strict.
- If keeping `Validated`, add "stratified external validation sample" in the abstract and Methods.

2. The graph utility case needs a stronger contrast with flat retrieval.

The manuscript claims graph utility by showing a tea-polysaccharide microbiome case. The example is plausible and useful, but the paper does not yet demonstrate what would fail under flat keyword retrieval. A skeptical reviewer may ask why the resource needs to be a graph rather than a structured table.

Suggested revision:

- Add a small supplementary table comparing a graph query against a flat keyword query.
- Report at least: query expression, number of records returned, whether evidence level is retained, whether uncertainty is retained, and whether metabolite/phenotype constraints are enforced.

3. Validation reporting should make denominator logic clearer.

The abstract and Results report acceptable rates, including 100% for processing step and extraction method. The validation table states that the rates are based on completed judgments, but the abstract does not. Because completed field counts vary, some readers may incorrectly interpret these as rates over all 47 reviewed records.

Suggested revision:

- Add "among completed field judgments" to the abstract or the Results.
- Add a validation-by-field denominator note in the table caption or main text.

4. The paper should include a validation error analysis.

The text mentions major issue tags such as out-of-scope records, wrong activity labels, and wrong study-type assignments, but no table summarizes their distribution. Because study type and evidence level are the weakest fields, a small error analysis would strengthen the manuscript.

Suggested revision:

- Add a compact table with major issue categories and counts.
- Add one sentence explaining whether these errors are mostly extraction errors, taxonomy errors, or corpus-boundary errors.

5. The appendix contains stale validation wording.

The supplementary validation section still states that field-level results should be reported only after the worksheet is completed. This is inconsistent with the main text, which already reports completed validation results.

Required revision:

- Update the appendix to describe the completed worksheet and released validation result files.

## Minor Comments

1. Replace the SSH repository URL in Data and Code Availability.

The manuscript uses `git@github.com:ShawnXiha/AutoTeaKG_Silver.git`. This is appropriate for Git operations but not for readers. Use `https://github.com/ShawnXiha/AutoTeaKG_Silver`.

2. The phrase "strongest utility test" is overly self-assessive.

In the graph-query Results subsection, replace this phrase with a more neutral formulation such as "most structured utility example".

3. The claim-evidence table is useful but may be better as Supplement for page-limited venues.

Some biological/database venues may not expect a claim-evidence table in the Introduction. Consider moving it to Supplement if page count becomes tight.

4. Several figure/table layout warnings remain.

The LaTeX log shows overfull boxes in the uncertainty table, long subsection title, graph query case table, and appendix uncertainty flag table. These do not block compilation but should be fixed before camera-ready submission.

5. Methods should include or reference prompt/schema details more explicitly.

The reproducibility appendix lists scripts, but the manuscript would be stronger if it included a compact supplementary schema/prompt table.

## Section-by-Section Evaluation

### Title and Abstract

The abstract is clear, quantitative, and appropriately bounded at the end. The main concern is that "validated" and the validation percentages should be interpreted over a stratified sample and completed judgments, not over the full KG.

### Introduction

The Introduction gives a coherent rationale: tea bioactivity evidence is fragmented; existing tea databases do not encode functional evidence and processing context; a silver-standard KG is a practical middle ground. The claim-evidence table strengthens the narrative, but it may be too process-oriented for some journals.

### Methods

The Methods section is generally reproducible at the pipeline level. The strongest parts are the auto-only construction statement, patch-first targeted extraction, vocabulary normalization, uncertainty assignment, and separation of external validation from graph construction. More detail is needed on prompts, schema constraints, and field-level validation procedures if the target venue emphasizes reproducibility.

### Results

The Results are logically ordered: graph composition, evidence imbalance, context recovery, vocabulary normalization, uncertainty, microbiome queries, graph utility case, and validation. The dashboard is the best central figure. The weakest result is the graph utility demonstration because it remains illustrative rather than comparative.

### Discussion and Limitations

The Discussion is appropriately conservative. The Limitations section is present and honest. It should also explicitly mention the small validation sample and absence of inter-annotator agreement if no independent double annotation was performed.

### Data, Code, Ethics, and LLM Use

The compliance sections are present and useful. The repository URL should be changed to HTTPS. The LLM usage statement is appropriately transparent.

## Reproducibility and Transparency

Strengths:

- Public repository is provided.
- Data/code/LLM/ethics statements exist.
- Scripts and generated artifacts are organized.
- Raw LLM logs are excluded with a rationale.

Weaknesses:

- No archived DOI or release tag is cited.
- Prompt/schema details are not easy to inspect from the manuscript itself.
- The validation worksheet is described, but completed validation artifacts need clearer pointer paths in the appendix.

## Figure and Table Assessment

Strong figures:

- `fig_evidence_quality_dashboard_v8`: useful central evidence-quality summary.
- `fig_graph_utility_case_v8`: better explains why graph paths matter.

Potentially redundant figures:

- Dashboard already contains activity-by-evidence and validation views; individual versions may still be useful but could move to Supplement depending on venue.

Tables needing polish:

- Graph query table: narrow columns create underfull warnings.
- Uncertainty flag table: long flag names create overfull warnings.
- Claim-evidence map: useful but may be more appropriate as supplementary material.

## Ethical and Reporting Considerations

No human-subject, animal, or clinical intervention data are generated by this work. The ethics statement is appropriate for literature-mining research. The manuscript should disclose whether human validators were students or domain experts only if the venue expects validation assessor details.

## Final Recommendation

The manuscript is publishable in principle as a resource/informatics paper after targeted revision. The core work is now credible: it has data, code, validation, uncertainty modeling, and a use case. The remaining weaknesses are manageable and mostly concern wording precision, validation denominator transparency, graph-utility comparison, and camera-ready formatting.

Recommended next decision:

`Revise v9 before submission`.
