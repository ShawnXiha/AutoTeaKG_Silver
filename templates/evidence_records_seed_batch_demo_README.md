# Evidence Records Seed Batch Demo README

File:
- `evidence_records_seed_batch_demo_2026-03-31.csv`

## What this file is

This is a demonstration annotation file built from the seed PubMed batch. It is not yet a final gold-standard dataset.

## How to use it

1. Use it to test whether the current schema is sufficient.
2. Use it to train annotators on the difference between:
   - review-derived summary records
   - primary-study evidence records
3. Use it as a style reference when filling `evidence_records_template.csv`.

## Important distinction

### Review-derived summary record

Examples:
- `PMID_38056775_R1`
- `PMID_39274868_R1`

Use these to:
- seed the database
- map evidence families
- identify candidate primary studies

Do not over-treat them as if they were direct experimental records.

### Primary-study evidence record

Examples:
- `PMID_39574401_R1`
- `PMID_38745351_R1`
- `PMID_39732435_R1`

These are the core units for downstream quantitative evidence comparison and graph construction.

## Recommended next step

Convert the current demo batch into a first adjudicated mini-gold-set by:
- selecting 5-8 papers
- manually checking all fields against abstracts/full texts
- refining normalization rules where conflicts appear
