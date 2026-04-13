import argparse
import csv
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_BASE_PAPERS = ROOT / "data" / "merged_batches" / "merge_2026-03-31_v1" / "included_papers_merged.csv"
DEFAULT_BASE_RECORDS = ROOT / "data" / "merged_batches" / "merge_2026-03-31_v1" / "candidate_records_merged.csv"
DEFAULT_MANUAL_RECORDS = ROOT / "templates" / "evidence_records_expanded_batch_v1_2026-03-31.csv"
DEFAULT_LLM_DIR = ROOT / "data" / "llm_annotations" / "glm5_test_run_v1"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "merged_batches" / "merge_2026-04-01_llm_v1"

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


def merge_notes(*values) -> str:
    seen = []
    for value in values:
        for item in (value or "").split(";"):
            cleaned = item.strip()
            if cleaned and cleaned not in seen:
                seen.append(cleaned)
    return "; ".join(seen)


def normalize_evidence_level(value: str, study_type: str) -> str:
    lower = normalize_text(value)
    study_type_lower = normalize_text(study_type)
    if not lower:
        lower = study_type_lower
    mapping = {
        "animal": "preclinical_in_vivo",
        "animal study": "preclinical_in_vivo",
        "preclinical": "preclinical_in_vivo",
        "preclinical_in_vivo": "preclinical_in_vivo",
        "preclinical_in_vitro_in_vivo": "preclinical_in_vivo",
        "preclinical_animal_model": "preclinical_in_vivo",
        "in vivo (animal)": "preclinical_in_vivo",
        "in vivo animal": "preclinical_in_vivo",
        "in vitro": "low_preclinical",
        "review": "evidence_synthesis_nonquantitative",
        "systematic review": "evidence_synthesis_nonquantitative",
        "meta-analysis": "evidence_synthesis",
        "cohort study": "human_observational",
        "rct": "human_interventional",
        "randomized controlled trial": "human_interventional",
        "human trial": "human_interventional",
        "human interventional": "human_interventional",
        "human observational": "human_observational",
        "evidence_synthesis_nonquantitative": "evidence_synthesis_nonquantitative",
        "evidence_synthesis": "evidence_synthesis",
        "high": "preclinical_in_vivo" if study_type_lower == "animal study" else "evidence_synthesis_nonquantitative",
    }
    return mapping.get(lower, value)


def normalize_effect_direction(value: str) -> str:
    lower = normalize_text(value)
    if not lower:
        return "unclear"
    if lower in {"positive", "negative", "mixed", "no_clear_effect", "unclear"}:
        return lower
    if any(token in lower for token in ["increase", "promot", "ameliorat", "improv", "reduce", "suppress", "protect", "enhanc", "restore", "skews", "shift", "decrease inflammatory"]):
        return "positive"
    if any(token in lower for token in ["worsen", "aggravat", "impair"]):
        return "negative"
    return "unclear"


def sanitize_record(row: dict) -> dict:
    cleaned = {field: row.get(field, "") for field in RECORD_FIELDS}
    cleaned["evidence_level"] = normalize_evidence_level(cleaned.get("evidence_level", ""), cleaned.get("study_type", ""))
    cleaned["effect_direction"] = normalize_effect_direction(cleaned.get("effect_direction", ""))
    return cleaned


def update_papers(base_rows, llm_rows):
    by_paper = {row["paper_id"]: {field: row.get(field, "") for field in PAPER_FIELDS} for row in base_rows}
    updated_count = 0
    for llm_row in llm_rows:
        paper_id = llm_row["paper_id"]
        llm_clean = {field: llm_row.get(field, "") for field in PAPER_FIELDS}
        if paper_id not in by_paper:
            by_paper[paper_id] = llm_clean
            updated_count += 1
            continue
        current = by_paper[paper_id]
        for field in PAPER_FIELDS:
            if field in {"notes"}:
                continue
            if llm_clean.get(field):
                current[field] = llm_clean[field]
        current["notes"] = merge_notes(current.get("notes", ""), llm_clean.get("notes", ""), "llm_screened=true")
        updated_count += 1
    merged = list(by_paper.values())
    merged.sort(key=lambda row: (row.get("year", ""), row.get("pmid", ""), row.get("title", "")), reverse=True)
    return merged, updated_count


def merge_records(manual_rows, base_candidate_rows, llm_rows):
    manual_rows = [sanitize_record(row) for row in manual_rows]
    llm_rows = [sanitize_record(row) for row in llm_rows]
    llm_paper_ids = {row["paper_id"] for row in llm_rows}
    manual_paper_ids = {row["paper_id"] for row in manual_rows}

    kept_base = []
    removed_auto_due_to_llm = 0
    removed_auto_due_to_manual = 0
    for row in base_candidate_rows:
        if row["paper_id"] in llm_paper_ids:
            removed_auto_due_to_llm += 1
            continue
        if row["paper_id"] in manual_paper_ids:
            removed_auto_due_to_manual += 1
            continue
        kept_base.append(sanitize_record(row))

    merged = []
    seen_ids = set()
    for source_rows in [manual_rows, llm_rows, kept_base]:
        for row in source_rows:
            record_id = row["record_id"]
            if record_id in seen_ids:
                continue
            seen_ids.add(record_id)
            merged.append(row)
    return merged, removed_auto_due_to_llm, removed_auto_due_to_manual


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-papers", type=Path, default=DEFAULT_BASE_PAPERS)
    parser.add_argument("--base-records", type=Path, default=DEFAULT_BASE_RECORDS)
    parser.add_argument("--manual-records", type=Path, default=DEFAULT_MANUAL_RECORDS)
    parser.add_argument("--llm-dir", type=Path, default=DEFAULT_LLM_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    llm_papers_path = args.llm_dir / "llm_screened_papers_cleaned.csv"
    llm_records_path = args.llm_dir / "llm_annotated_records_cleaned.csv"
    if not llm_papers_path.exists():
        llm_papers_path = args.llm_dir / "llm_screened_papers.csv"
    if not llm_records_path.exists():
        llm_records_path = args.llm_dir / "llm_annotated_records.csv"

    base_papers = read_csv(args.base_papers)
    base_records = read_csv(args.base_records)
    manual_records = read_csv(args.manual_records)
    llm_papers = read_csv(llm_papers_path)
    llm_records = read_csv(llm_records_path)

    merged_papers, updated_papers = update_papers(base_papers, llm_papers)
    merged_records, removed_llm_auto, removed_manual_auto = merge_records(manual_records, base_records, llm_records)

    output_dir = args.output_dir
    papers_out = output_dir / "included_papers_llm_merged.csv"
    records_out = output_dir / "evidence_records_llm_merged.csv"
    db_out = output_dir / "teakg_llm_merged.sqlite"
    summary_out = output_dir / "merge_llm_summary.txt"

    write_csv(papers_out, PAPER_FIELDS, merged_papers)
    write_csv(records_out, RECORD_FIELDS, merged_records)

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
        f"base_papers={args.base_papers}",
        f"base_records={args.base_records}",
        f"manual_records={args.manual_records}",
        f"llm_dir={args.llm_dir}",
        f"llm_papers={llm_papers_path}",
        f"llm_records={llm_records_path}",
        f"merged_paper_count={len(merged_papers)}",
        f"merged_record_count={len(merged_records)}",
        f"llm_papers_applied={updated_papers}",
        f"llm_records_applied={len(llm_records)}",
        f"removed_auto_due_to_llm={removed_llm_auto}",
        f"removed_auto_due_to_manual={removed_manual_auto}",
        f"papers_out={papers_out}",
        f"records_out={records_out}",
        f"db_out={db_out}",
    ]
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_out.write_text("\n".join(summary_lines), encoding="utf-8")
    print("\n".join(summary_lines))


if __name__ == "__main__":
    main()
