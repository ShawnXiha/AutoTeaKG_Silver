# Scripts

## build_sqlite_db.py

Builds `data/teakg_v1.sqlite` from:
- `templates/included_papers_expanded_batch_2026-03-31.csv`
- `templates/evidence_records_expanded_batch_v1_2026-03-31.csv`

## generate_candidate_records.py

Creates low-confidence candidate `EvidenceRecord` rows from included-paper metadata.

Purpose:
- occupy the schema quickly
- reduce blank-template work
- provide human annotators with a draft row to correct

This is intentionally conservative and heuristic. It does not replace manual curation.
