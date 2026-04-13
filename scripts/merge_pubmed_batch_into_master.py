import argparse
import csv
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MASTER_PAPERS = ROOT / "templates" / "included_papers_expanded_batch_2026-03-31.csv"
DEFAULT_MASTER_RECORDS = ROOT / "templates" / "evidence_records_expanded_batch_v1_2026-03-31.csv"
DEFAULT_BATCH_DIR = ROOT / "data" / "pubmed_batches" / "tea_pubmed_batch_2026-03-31_large_v2"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "merged_batches"

PAPER_FIELDS = [
    "paper_id",
    "source_db",
    "title",
    "authors",
    "journal",
    "year",
    "doi",
    "pmid",
    "study_type",
    "tea_type",
    "material_form",
    "component_group",
    "activity_category",
    "processing_present",
    "extraction_present",
    "microbiome_present",
    "include_status",
    "exclusion_reason",
    "notes",
]


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def normalize_text(value: str) -> str:
    return " ".join((value or "").strip().lower().split())


def paper_key(row: dict):
    pmid = normalize_text(row.get("pmid", ""))
    doi = normalize_text(row.get("doi", ""))
    title = normalize_text(row.get("title", ""))
    if pmid:
        return ("pmid", pmid)
    if doi:
        return ("doi", doi)
    return ("title", title)


def merge_notes(master_notes: str, batch_notes: str) -> str:
    parts = []
    for text in [master_notes, batch_notes]:
        for item in (text or "").split(";"):
            cleaned = item.strip()
            if cleaned and cleaned not in parts:
                parts.append(cleaned)
    return "; ".join(parts)


def choose_row(existing: dict, incoming: dict):
    if not existing:
        return incoming, "new"
    existing_status = existing.get("include_status", "")
    incoming_status = incoming.get("include_status", "")
    existing_priority = {"include": 3, "maybe": 2, "exclude": 1}.get(existing_status, 0)
    incoming_priority = {"include": 3, "maybe": 2, "exclude": 1}.get(incoming_status, 0)
    chosen = dict(existing)
    if incoming_priority > existing_priority:
        for field in PAPER_FIELDS:
            if field == "notes":
                continue
            chosen[field] = incoming.get(field, chosen.get(field, ""))
    else:
        for field in PAPER_FIELDS:
            if field in {"notes", "include_status", "exclusion_reason"}:
                continue
            if not chosen.get(field) and incoming.get(field):
                chosen[field] = incoming[field]
    chosen["notes"] = merge_notes(existing.get("notes", ""), incoming.get("notes", ""))
    return chosen, "updated"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--master-papers", type=Path, default=DEFAULT_MASTER_PAPERS)
    parser.add_argument("--master-records", type=Path, default=DEFAULT_MASTER_RECORDS)
    parser.add_argument("--batch-dir", type=Path, default=DEFAULT_BATCH_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR / "merge_2026-03-31_v1")
    parser.add_argument("--batch-screened-file", default="normalized_included_papers.csv")
    parser.add_argument("--candidate-statuses", default="include,maybe")
    args = parser.parse_args()

    batch_papers_path = args.batch_dir / args.batch_screened_file
    master_rows = read_csv(args.master_papers)
    batch_rows = read_csv(batch_papers_path)

    merged_by_key = {}
    for row in master_rows:
        row_copy = {field: row.get(field, "") for field in PAPER_FIELDS}
        merged_by_key[paper_key(row_copy)] = row_copy

    added = 0
    updated = 0
    duplicates = 0
    for row in batch_rows:
        row_copy = {field: row.get(field, "") for field in PAPER_FIELDS}
        key = paper_key(row_copy)
        if key in merged_by_key:
            chosen, state = choose_row(merged_by_key[key], row_copy)
            merged_by_key[key] = chosen
            duplicates += 1
            if state == "updated":
                updated += 1
        else:
            merged_by_key[key] = row_copy
            added += 1

    merged_rows = list(merged_by_key.values())
    merged_rows.sort(key=lambda row: (row.get("year", ""), row.get("pmid", ""), row.get("title", "")), reverse=True)

    output_dir = args.output_dir
    papers_out = output_dir / "included_papers_merged.csv"
    records_out = output_dir / "candidate_records_merged.csv"
    db_out = output_dir / "teakg_merged.sqlite"
    summary_out = output_dir / "merge_summary.txt"

    write_csv(papers_out, PAPER_FIELDS, merged_rows)

    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate_candidate_records.py"),
            "--input",
            str(papers_out),
            "--output",
            str(records_out),
            "--include-statuses",
            args.candidate_statuses,
        ],
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_sqlite_db.py"),
            "--papers",
            str(papers_out),
            "--records",
            str(records_out),
            "--db-path",
            str(db_out),
        ],
        check=True,
    )

    summary_lines = [
        f"master_papers={args.master_papers}",
        f"master_records={args.master_records}",
        f"batch_dir={args.batch_dir}",
        f"batch_screened_file={batch_papers_path}",
        f"merged_paper_count={len(merged_rows)}",
        f"master_paper_count={len(master_rows)}",
        f"batch_paper_count={len(batch_rows)}",
        f"new_rows_added={added}",
        f"duplicate_rows_seen={duplicates}",
        f"rows_updated_or_enriched={updated}",
        f"merged_papers_file={papers_out}",
        f"merged_candidate_records_file={records_out}",
        f"merged_db_file={db_out}",
    ]
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_out.write_text("\n".join(summary_lines), encoding="utf-8")

    print("\n".join(summary_lines))


if __name__ == "__main__":
    main()
