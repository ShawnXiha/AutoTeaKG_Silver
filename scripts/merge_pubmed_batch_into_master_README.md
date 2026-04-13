# Merge PubMed Batch Into Master

Use this after title/abstract screening of a PubMed batch.

## What it does

1. reads the current hand-curated master `included_papers` file
2. reads a screened PubMed batch `normalized_included_papers.csv`
3. merges by `pmid`, then `doi`, then normalized `title`
4. keeps existing master rows as the default authority
5. upgrades metadata when the new batch has a stronger `include_status` or fills blanks
6. writes a merged `included_papers` file
7. regenerates merged candidate records
8. rebuilds a merged SQLite database

## Example

```powershell
python scripts\merge_pubmed_batch_into_master.py --batch-dir data\pubmed_batches\tea_pubmed_batch_2026-03-31_large_v2 --output-dir data\merged_batches\merge_2026-03-31_v1
```

## Outputs

- `included_papers_merged.csv`
- `candidate_records_merged.csv`
- `teakg_merged.sqlite`
- `merge_summary.txt`

## Important note

This script merges paper-level metadata only. It does not overwrite your hand-curated adjudicated `evidence_records_expanded_batch_v1_2026-03-31.csv`.
