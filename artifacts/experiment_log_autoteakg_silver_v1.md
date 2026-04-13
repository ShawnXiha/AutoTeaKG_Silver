# AutoTeaKG-Silver v1 Experiment Log

Date: 2026-04-12

## Experiment 1: Baseline Auto-Only Silver Pipeline

### Purpose

Build a working baseline that uses only automatic PubMed retrieval, automatic normalization, and GLM5/auto candidate records. Manual adjudication and manual audit files are excluded from the construction path.

### Setting

- Input papers: `data/merged_batches/tea_pubmed_batch_2026-03-31_large_v2_llm_merged/included_papers_llm_merged.csv`
- Input records: `data/merged_batches/tea_pubmed_batch_2026-03-31_large_v2_llm_merged/evidence_records_llm_merged.csv`
- Abstract source: `data/pubmed_batches/**/pubmed_results_raw.csv`
- Output script: `scripts/build_autoteakg_silver_v1.py`
- Default output directory: `reports/autoteakg_silver_v1`

### Results

Initial run failed before logic evaluation because the workspace denied creation of `data/autoteakg_silver_v1` and Python bytecode compilation attempted to write under `scripts/__pycache__`.

### Analysis

Failure was environmental rather than algorithmic. A simple working version should avoid new `data/` subdirectory creation and avoid bytecode-based syntax validation.

### Next Steps

Use `reports/autoteakg_silver_v1` as the default output path, validate syntax through `ast.parse`, and run the script with `python -B`.

## Experiment 2: Processing Pattern Failure-Case Isolation

### Purpose

Diagnose whether the processing/component extractor is filling context fields with real tea processing signals or false positives from biomedical endpoint language.

### Setting

Same data and script as Experiment 1, with failure-case inspection focused on `silver_processing_step` and `processing_evidence_terms`.

### Results

The initial extractor over-matched `storage/aging` because broad `aging` and `aged` tokens appeared in terms such as `skin aging`, `middle-aged`, and age-related disease abstracts. After removing bare `aging`, `aged`, and bare `oxidation`, storage/aging records dropped from 65 to 22 and no longer included the inspected `skin aging` / `middle-aged` examples. A second failure case remained: `freeze-drying` of sperm samples was incorrectly treated as tea-material drying.

### Analysis

The failure cause is broad processing terms that are valid in tea production but also common in endpoint/model descriptions. The fix should keep processing extraction conservative unless the phrase is tied to tea material or process context.

### Next Steps

Restrict `drying` to tea-specific phrases such as `dried tea`, `tea drying`, `drying temperature`, `dried leaves`, or `spray-dried tea`.

## Experiment 3: Final Integrity Check

### Purpose

Verify that the final auto-only pipeline produces internally consistent output and that no manual records leak into the silver dataset.

### Setting

- Command: `python -B scripts\build_autoteakg_silver_v1.py`
- Output directory: `reports/autoteakg_silver_v1`
- Integrity checks: record count equality, node count equality, edge count equality, unresolved edge detection, manual annotator exclusion.

### Results

- Silver records: 635
- KG v3 nodes: 1963
- KG v3 edges: 8162
- Unresolved KG edges: 0
- Manual records in silver output: 0
- Uncertainty classes: 86 low, 479 moderate, 70 high

### Analysis

The pipeline now has a working version. The main confirmed limitation is not runtime stability but scientific specificity: processing/extraction context remains sparse because conservative rules avoid false positives. This limitation is useful for the paper narrative because it quantifies the next method gap.

### Next Steps

[Reusable] Use conservative rule-based processing extraction as the first silver layer, then add a targeted LLM extraction module only for records with `missing_processing_or_extraction_context`.

## Experiment 4: Targeted Processing LLM Extractor

### Purpose

Create a focused LLM module that only targets records missing tea processing/extraction context instead of rerunning the full annotation pipeline.

### Setting

- Input: `reports/autoteakg_silver_v1/autoteakg_silver_records.csv`
- Script: `scripts/targeted_processing_llm_extractor.py`
- Target rule: auto-only records with `missing_processing_or_extraction_context`
- Safety: patch-first outputs, no direct overwrite of base silver records
- Rate limit: default `1.6` seconds/request

### Results

- Dry-run target count: 365 records
- Mock-run target count: 5 records
- Mock-run patch count: 5
- Mock-run patched KG integrity: 635 records, 1963 nodes, 8162 edges, 0 unresolved edges

### Analysis

The module is technically functional. Mock extraction mostly reproduces the conservative rule-based baseline, which is expected; the real value comes from GLM5 resolving whether abstracts contain unstructured processing/extraction context that rules missed. The prompt is explicitly guarded against known false positives such as `skin aging`, `middle-aged`, and `freeze-dried sperm`.

### Next Steps

[Reusable] Run GLM5 on a small batch (`--max-records 20`) first, inspect patches, then scale to the full 365-record target set if false-positive rate is acceptable.

## Experiment 5: 429 Retry Completion

### Purpose

Recover the small number of targeted processing extraction records that failed during the full GLM5 run due to rate limiting.

### Setting

- Full run directory: `reports/targeted_processing_llm_extractor_full`
- Retry directory: `reports/targeted_processing_llm_extractor_retry_429`
- Final merged directory: `reports/targeted_processing_llm_extractor_final`
- Retry command used a slower request interval: `--min-interval-seconds 4.0`
- Retry command used higher retry budget: `--max-retries 5`

### Results

- Full run target records: 365
- Full run successful patches: 350
- Full run 429 errors: 15
- Retry successful patches: 15
- Final merged patches: 365
- Remaining errors after merge: 0
- Final patched KG: 635 records, 2002 nodes, 8183 edges, 0 unresolved edges

### Analysis

The 429 failures were transient rate-limit failures rather than content or prompt failures. Slowing the retry batch to one request every 4 seconds with a retry budget of 5 recovered all failed records.

### Next Steps

[Reusable] For full-batch NVIDIA GLM5 runs, use a conservative retry lane for failures: collect failed record IDs, rerun only those IDs with `--min-interval-seconds 4.0 --max-retries 5`, then merge patch runs with `scripts/merge_targeted_processing_patch_runs.py`.

## Experiment 6: Processing/Extraction Vocabulary Normalization

### Purpose

Normalize noisy LLM-generated processing and extraction labels into a smaller ontology while preserving raw labels for provenance.

### Setting

- Input: `reports/targeted_processing_llm_extractor_final/patched_autoteakg_silver_v1/autoteakg_silver_records.csv`
- Script: `scripts/normalize_processing_extraction_vocab.py`
- Output: `reports/targeted_processing_vocab_normalized`

### Results

- Records normalized: 635
- Mapping rows: 306
- Changed mappings: 31
- Unmapped processing labels: 0
- Unmapped extraction labels: 0
- Normalized KG: 1979 nodes, 8168 edges, 0 unresolved edges

### Analysis

Vocabulary normalization reduced KG fragmentation by mapping labels such as `black tea manufacturing` to `black tea processing`, `brick-like form` to `compressed/brick tea processing`, `cold brewing; hot brewing` to `brewing/infusion`, and analytical-method labels to `analytical characterization`.

### Next Steps

[Reusable] Treat `reports/targeted_processing_vocab_normalized` as the cleanest current KG v3 candidate. For downstream paper figures and queries, prefer this normalized directory over the raw targeted-processing final directory.

## Experiment 7: Full-Text/Methods Retrieval and Extraction

### Purpose

Resolve remaining abstract-level missing processing/extraction context using open PMC full text and methods-like sections.

### Setting

- Input normalized silver: `reports/targeted_processing_vocab_normalized/autoteakg_silver_records.csv`
- Remaining missing-context records: 329
- Distinct PMIDs queried through NCBI E-utilities: 213
- Retrieval script: `scripts/retrieve_pmc_methods_for_remaining_context.py`
- Methods extraction runner: `scripts/run_methods_processing_extraction_batches.py`
- Methods patch final directory: `reports/methods_processing_llm_final`
- Methods normalized KG directory: `reports/methods_processing_vocab_normalized`

### Results

- PMC methods-like sections found for 151 records from 109 papers.
- No PMC full text was available for 178 records from 104 papers.
- Methods-section GLM5 patches generated: 151.
- Initial methods batch errors: 4; retry recovered all 4.
- Final methods extraction remaining errors: 0.
- Processing step present improved from 167 to 183 records.
- Extraction method present improved from 170 to 185 records.
- Final normalized methods KG: 1989 nodes, 8195 edges, 0 unresolved edges.

### Analysis

Full text added preparation/extraction details that were absent from abstracts, including crushing/sieving, cleaning-drying-powdering, steaming/fixation, ultrasonic ethanol extraction, methanol sonication, microwave extraction, and commercial preparation. The dominant bottleneck is full-text availability rather than model failure.

### Next Steps

[Reusable] Treat `reports/methods_processing_vocab_normalized` as the current best KG v3. For the 178 records without PMC full text, use DOI landing pages, publisher PDFs, or institutional full-text access rather than more abstract-level prompting.
