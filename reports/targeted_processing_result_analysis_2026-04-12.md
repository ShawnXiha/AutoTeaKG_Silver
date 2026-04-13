# Targeted Processing Extractor Result Analysis

Date: 2026-04-12

## Purpose

This analysis quantifies what the targeted GLM5 processing/component extractor added after `AutoTeaKG-Silver v1`. It is based only on automatic outputs and does not depend on manual annotation.

## Run Completion

- Target records: 365
- Final patches: 365
- Remaining errors: 0
- Missing patches: 0
- Source 429 errors recovered by retry: 15

## Before/After Context Coverage

| Field | Before | After | Added |
|---|---:|---:|---:|
| component group present | 635 | 635 | 0 |
| processing step present | 146 | 167 | 21 |
| extraction method present | 154 | 170 | 16 |
| missing processing/extraction uncertainty flag | 365 | 329 | 36 resolved |

## Patch Content Profile

| processing_present | extraction_present | component_present | Count | Share of patches |
|---|---|---|---:|---:|
| false | false | true | 236 | 64.7% |
| false | false | false | 92 | 25.2% |
| true | false | true | 17 | 4.7% |
| false | true | true | 16 | 4.4% |
| true | false | false | 3 | 0.8% |
| true | true | true | 1 | 0.3% |

## Interpretation

The targeted extractor completed the missing-context pass, but most abstracts still do not report tea-material processing or extraction details. The largest patch class was `component_present=true` with `processing_present=false` and `extraction_present=false`, indicating that the model mostly confirmed component context rather than finding hidden processing context.

This is scientifically useful: it suggests that abstract-level tea bioactivity literature often supports component/activity/evidence extraction, but processing and extraction variables require either full text, methods sections, or specialized process-focused retrieval.

## Method Implication

For the next experiment, do not simply rerun GLM5 on the same abstracts. The better next step is a full-text or methods-section extractor for the remaining `missing_processing_or_extraction_context` records, plus vocabulary normalization for noisy LLM labels such as `black tea manufacturing`, `matcha production`, and `cold brewing; hot brewing`.
