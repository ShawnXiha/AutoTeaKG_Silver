# PubMed Batch Pipeline

This pipeline expands the current tea evidence workflow from manual CSV curation to batch PubMed retrieval.

## What it does

1. runs multiple PubMed queries for tea functional activity studies
2. saves raw PubMed metadata and abstracts
3. normalizes results into the `included_papers` schema
4. generates candidate `EvidenceRecord` rows automatically
5. builds a batch-specific SQLite database

## Main scripts

- `pubmed_tea_batch_retrieval.py`
- `run_pubmed_batch_pipeline.py`

## Example

```powershell
python scripts\run_pubmed_batch_pipeline.py --batch-name tea_pubmed_batch_2026-03-31_large --retmax-per-query 250
```

Optional:

```powershell
python scripts\run_pubmed_batch_pipeline.py --batch-name tea_pubmed_batch_2026-03-31_large --retmax-per-query 400 --email your_email@example.com --api-key YOUR_NCBI_API_KEY
```

## Outputs

Each run writes a folder under `data\pubmed_batches\<batch_name>\`:

- `query_manifest.json`
- `summary.json`
- `search_log.csv`
- `pubmed_results_raw.csv`
- `normalized_included_papers.csv`
- `candidate_records.csv`
- `teakg_batch.sqlite`

## Notes

- `normalized_included_papers.csv` is heuristic and should still be title/abstract screened.
- candidate records are generated from normalized paper rows and default to `needs_review`.
- the batch SQLite database is separate from the hand-curated `data\teakg_v1.sqlite`.
