# Paper Self-Review for AutoTeaKG-Silver v8

Date: 2026-04-25

Manuscript reviewed:

- `drafts/v8_database_draft.tex`
- `final/AutoTeaKG_Silver_v8_database.pdf`

Review mode:

- `$paper-review`
- Reject-first simulation
- Claim-evidence audit
- Five-aspect self-review
- Figure/table quality check
- Pre-submission risk triage

## Executive Judgment

v8 is substantially stronger than v7. The manuscript now has a clear resource-paper shape, explicit validation, uncertainty formalization, a graph utility case, and a stronger claim-evidence thread. It is close to a submission-ready database/resource manuscript, but not yet camera-ready. The likely editorial status is `major revision before first submission` if judged strictly, or `minor-to-major polish` if the target venue is explicitly a resource/database journal.

Recommended status:

`Revise once more before submission`.

Best-fit venue class:

`database / bioinformatics resource / computational food science informatics`.

## Reject-First Simulation

A strict reviewer could reject the current version by arguing that AutoTeaKG-Silver is an engineering resource built from LLM extraction rather than a methodologically novel knowledge-graph contribution. The validation sample is useful but small: only 47 completed records out of 635, with field-level completion counts as low as 33-37, and study-type accuracy is only 80%. The graph utility case is plausible, but it does not yet compare graph querying against flat keyword retrieval or show that the retrieved case changes a scientific conclusion. The title uses "Validated", but the validation is stratified and partial rather than comprehensive. Several figures and tables are dense, and the appendix still contains a stale sentence saying field-level results should be reported only after worksheet completion, even though the results are already reported in the main text.

## Contribution Sufficiency

Assessment: `Moderate to strong for a resource paper; moderate for a methods paper`.

Strengths:

- The paper defines a useful tea-functional-activity evidence schema that separates activity, evidence level, component context, processing/extraction context, provenance, and uncertainty.
- The resource size is concrete: 635 evidence records, 1,989 nodes, and 8,195 edges.
- The uncertainty-aware silver-standard framing is honest and defensible.
- The external validation results reduce the main trust objection compared with earlier versions.

Major risks:

- The computational novelty remains mostly integrative rather than algorithmic.
- The phrase "Validated Silver-Standard" in the title may overstate the validation scope because only 47 records were externally reviewed.
- The graph utility case is illustrative, but not yet a convincing comparison against non-graph retrieval.

Recommended fix:

- Change title to a lower-risk version, for example: `AutoTeaKG-Silver: A Validated Silver-Standard Evidence Graph for Tea Functional Activity Literature` can become `AutoTeaKG-Silver: A Validated Silver-Standard Evidence Graph Resource for Tea Functional Activity Literature`, or use `Externally Audited` instead of `Validated`.
- Add a short "graph vs flat retrieval" comparison paragraph or supplementary table for the tea-polysaccharide query.

## Writing Clarity

Assessment: `Good, with localized issues`.

Strengths:

- The Introduction now flows from domain fragmentation to resource gap to silver-standard graph contribution.
- The claim-evidence map is a strong addition and helps reviewer navigation.
- The Methods section describes pipeline stages, uncertainty rules, and validation separation clearly.

Issues:

- The Methods section still lacks enough low-level prompt/schema detail for complete reproduction from the paper alone. It points to scripts, which is acceptable for a resource paper, but reviewers may ask for prompt templates or schema snippets in Supplement.
- The Data and Code Availability section uses the SSH URL `git@github.com:ShawnXiha/AutoTeaKG_Silver.git`; manuscript readers need an HTTPS URL.
- Supplementary Data: Validation Sample still says field-level results should only be reported after worksheet completion, which is stale in v8.

Recommended fix:

- Add one supplementary table listing key extraction schema fields, allowed labels, and whether each field is controlled vocabulary or free text.
- Replace the repository URL with `https://github.com/ShawnXiha/AutoTeaKG_Silver`.
- Update the stale validation appendix sentence to say the completed worksheet and field-level results are released.

## Results Quality

Assessment: `Good for resource characterization; still thin for utility demonstration`.

Strengths:

- The evidence-quality dashboard is a strong anchor figure.
- Stage-wise context recovery and missing-context counts are clear.
- Validation results are useful and correctly framed as external to construction.

Risks:

- The validation table reports "acceptable" rather than separating "correct" and "minor issue" in the main text. This is defensible, but some reviewers may prefer seeing both.
- The graph utility case uses five representative records; it does not show recall, precision, or contrast with keyword search.
- The result "100% processing/extraction" is based on completed judgments only, not all 47 reviewed records; the caption states this, but the abstract may still read stronger than warranted.

Recommended fix:

- In the main text, add one sentence: "These rates are computed over completed field judgments, not over all sampled records."
- Add a small supplementary table comparing the graph query output with a flat keyword query for `tea polysaccharide microbiome liver`.

## Testing Completeness

Assessment: `Adequate for a first resource submission; not enough for a strong methods paper`.

Completed:

- Stage-wise QC table exists.
- External validation exists.
- Graph query case exists.
- Uncertainty model exists.
- Data/code/LLM usage statements exist.

Missing or weak:

- No inter-annotator agreement is reported.
- No baseline comparison to keyword retrieval or generic LLM extraction is reported.
- No error analysis table for the major validation issues is included.

Recommended fix:

- Add a compact validation-error table summarizing major issue categories: out-of-scope, wrong activity, wrong study type, wrong component, duplicate/unclear.
- If two reviewers independently annotated any subset, report agreement. If not, explicitly state that the current validation is single-reviewer field assessment.

## Method Design

Assessment: `Defensible as a silver-standard pipeline`.

Strengths:

- Manual validation is correctly separated from graph construction.
- Uncertainty is record-level and propagated to graph edges.
- Patch-first targeted extraction is a good auditability design.

Risks:

- The uncertainty thresholds are heuristic. They are explained, but not calibrated against validation outcomes.
- The "severe flag" set mixes extraction reliability, taxonomy status, and evidence strength. This is useful operationally but may need clearer rationale.

Recommended fix:

- Add a paragraph saying the uncertainty model is operational rather than probabilistically calibrated.
- Add a supplementary cross-tab of validation outcome by uncertainty class.

## Claim-Evidence Audit

High-risk claims:

- Title line 25: `Validated Silver-Standard Evidence Graph` may overstate the validation scope.
- Abstract line 33: `External validation ... showed acceptable rates` is accurate, but should mention "completed field judgments" if space allows.
- Results line 268: `strongest utility test` is too self-evaluative. Prefer "most structured utility example".
- Results line 304: `supports silver-standard use` is acceptable, but should be bounded by field-level and sample-size limitations.

Supported claims:

- Resource scale: supported by Table 2 and Figure 2/dashboard.
- Context recovery: supported by stage-wise QC table and context figure.
- Evidence imbalance: supported by heatmap.
- Uncertainty composition: supported by uncertainty figure and class table.
- Validation rates: supported by validation table.

## Figure and Table Quality

Strengths:

- New dashboard figure is useful and centralizes the evidence.
- Graph utility case is clearer than the previous case-only graph.
- Most tables use booktabs and captions are above tables.

Issues:

- v8 still has overfull warnings from long tables and a long subsection title.
- The dashboard is information-rich; it may be too dense for a single-column venue.
- The graph utility figure is conceptually clear, but evidence text may be small after journal scaling.
- The claim-evidence table in Introduction may be unusual in some biological journals; it is useful, but could be moved to Supplement depending on venue.

Recommended fix:

- For final template conversion, decide whether the dashboard is full-width and move claim-evidence map to Supplement if page-limited.
- Shorten the long subsection heading: `AutoTeaKG-Silver constructs a provenance-rich tea functional activity graph` -> `Resource Composition`.

## Pre-Submission Checklist

Pass:

- All major sections drafted.
- Limitation section present.
- Data/code statement present.
- LLM usage statement present.
- Ethics statement present.
- No undefined citations or references in v8 log.
- No TODO markers identified.

Needs action:

- Replace SSH repository URL with HTTPS in manuscript text.
- Fix stale validation appendix sentence.
- Decide whether `Validated` in title should be softened.
- Add graph-vs-keyword retrieval comparison or explicitly state that the case study is illustrative.
- Add validation error analysis or validation-by-uncertainty supplement.

## Bottom Line

v8 is scientifically coherent and much more defensible than v7. The next revision should not add broad new sections. It should make four targeted fixes: soften validation wording, remove stale appendix text, add graph utility comparison, and add validation error/uncertainty cross-tab. After that, the paper should be ready for venue-specific template conversion and cover-letter preparation.
