import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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

RECORD_FIELDS = [
    "record_id",
    "paper_id",
    "tea_type",
    "material_form",
    "component_group",
    "compound_name",
    "activity_category",
    "endpoint_label",
    "study_type",
    "evidence_level",
    "model_system",
    "dose_exposure",
    "effect_direction",
    "processing_step",
    "extraction_method",
    "cultivar",
    "origin",
    "mechanism_label",
    "microbiota_taxon",
    "microbial_metabolite",
    "host_phenotype",
    "claim_text_raw",
    "confidence_score",
    "annotator_id",
    "adjudication_status",
    "notes",
]


def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def merge_notes(*values) -> str:
    seen = []
    for value in values:
        for item in (value or "").split(";"):
            cleaned = item.strip()
            if cleaned and cleaned not in seen:
                seen.append(cleaned)
    return "; ".join(seen)


def normalize_text(value: str) -> str:
    return " ".join((value or "").strip().lower().split())


def normalize_field_for_key(value: str) -> str:
    text = normalize_text(value)
    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    stop_phrases = [
        "markers",
        "marker",
        "severity",
        "outcome",
        "activity",
        "activities",
        "related",
        "general",
        "modulation",
        "suppression",
        "inhibition",
        "improvement",
        "amelioration",
    ]
    parts = [part for part in text.split() if part not in stop_phrases]
    return " ".join(parts)


def semantic_record_key(row: dict):
    paper_id = normalize_text(row.get("paper_id", ""))
    activity = normalize_text(row.get("activity_category", ""))
    endpoint = normalize_field_for_key(row.get("endpoint_label", ""))
    mechanism = normalize_field_for_key(row.get("mechanism_label", ""))
    # For LLM reruns, most duplicate noise occurs within the same paper/activity pair.
    # Keep only one representative record per activity unless the microbiome endpoint is clearly distinct.
    if activity != "gut microbiota modulation":
        return (paper_id, activity)
    return (
        paper_id,
        activity,
        endpoint,
        mechanism,
    )


def confidence_value(row: dict) -> float:
    try:
        return float(row.get("confidence_score", 0) or 0)
    except Exception:
        return 0.0


def completeness_score(row: dict) -> int:
    fields = [
        "activity_category",
        "endpoint_label",
        "study_type",
        "evidence_level",
        "model_system",
        "effect_direction",
        "mechanism_label",
        "microbiota_taxon",
        "microbial_metabolite",
        "host_phenotype",
        "claim_text_raw",
    ]
    return sum(1 for field in fields if normalize_text(row.get(field, "")))


def choose_better_record(existing: dict, incoming: dict, incoming_source_rank: int):
    existing_rank = int(existing.get("_source_rank", 0))
    existing_conf = confidence_value(existing)
    incoming_conf = confidence_value(incoming)
    existing_complete = completeness_score(existing)
    incoming_complete = completeness_score(incoming)

    keep_incoming = False
    if incoming_source_rank > existing_rank:
        keep_incoming = True
    elif incoming_source_rank == existing_rank and incoming_conf > existing_conf:
        keep_incoming = True
    elif incoming_source_rank == existing_rank and incoming_conf == existing_conf and incoming_complete > existing_complete:
        keep_incoming = True

    if keep_incoming:
        merged = dict(incoming)
    else:
        merged = dict(existing)

    merged["notes"] = merge_notes(existing.get("notes", ""), incoming.get("notes", ""))
    merged["_source_rank"] = max(existing_rank, incoming_source_rank)
    return merged


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary-dir", type=Path, required=True)
    parser.add_argument("--retry-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    primary_papers = read_csv(args.primary_dir / "llm_screened_papers.csv")
    retry_papers = read_csv(args.retry_dir / "llm_screened_papers.csv")
    primary_records = read_csv(args.primary_dir / "llm_annotated_records.csv")
    retry_records = read_csv(args.retry_dir / "llm_annotated_records.csv")
    primary_errors = read_jsonl(args.primary_dir / "llm_errors.jsonl")
    retry_errors = read_jsonl(args.retry_dir / "llm_errors.jsonl")
    primary_responses = read_jsonl(args.primary_dir / "llm_raw_responses.jsonl")
    retry_responses = read_jsonl(args.retry_dir / "llm_raw_responses.jsonl")

    papers_by_id = {row["paper_id"]: {field: row.get(field, "") for field in PAPER_FIELDS} for row in primary_papers}
    for row in retry_papers:
        paper_id = row["paper_id"]
        cleaned = {field: row.get(field, "") for field in PAPER_FIELDS}
        if paper_id in papers_by_id:
            cleaned["notes"] = merge_notes(papers_by_id[paper_id].get("notes", ""), cleaned.get("notes", ""), "llm_retry_merged=true")
        papers_by_id[paper_id] = cleaned

    merged_records_by_key = {}
    for row in primary_records:
        working = dict(row)
        working["_source_rank"] = 1
        key = semantic_record_key(working)
        if key in merged_records_by_key:
            merged_records_by_key[key] = choose_better_record(merged_records_by_key[key], working, 1)
        else:
            merged_records_by_key[key] = working
    for row in retry_records:
        working = dict(row)
        working["_source_rank"] = 2
        key = semantic_record_key(working)
        if key in merged_records_by_key:
            merged_records_by_key[key] = choose_better_record(merged_records_by_key[key], working, 2)
        else:
            merged_records_by_key[key] = working
    merged_records = []
    for row in merged_records_by_key.values():
        cleaned = {field: row.get(field, "") for field in RECORD_FIELDS}
        merged_records.append(cleaned)

    resolved_error_ids = {row["paper_id"] for row in retry_papers}
    merged_errors = [row for row in primary_errors if row.get("paper_id") not in resolved_error_ids]
    merged_errors.extend(retry_errors)

    merged_responses = primary_responses + retry_responses

    output_dir = args.output_dir
    write_csv(output_dir / "llm_screened_papers.csv", PAPER_FIELDS, list(papers_by_id.values()))
    write_csv(output_dir / "llm_annotated_records.csv", RECORD_FIELDS, merged_records)
    write_jsonl(output_dir / "llm_errors.jsonl", merged_errors)
    write_jsonl(output_dir / "llm_raw_responses.jsonl", merged_responses)

    summary = {
        "primary_dir": str(args.primary_dir),
        "retry_dir": str(args.retry_dir),
        "output_dir": str(output_dir),
        "paper_count": len(papers_by_id),
        "record_count": len(merged_records),
        "remaining_errors": len(merged_errors),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
