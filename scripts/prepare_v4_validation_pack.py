import csv
import random
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "writing_outputs" / "20260412_autoteakg_silver_paper"
RECORDS = ROOT / "reports" / "methods_processing_vocab_normalized" / "autoteakg_silver_records.csv"
OUT_DIR = PAPER_DIR / "data" / "validation_v4"


FIELDS_TO_REVIEW = [
    "activity_category",
    "study_type",
    "evidence_level",
    "silver_component_group",
    "silver_processing_step",
    "silver_extraction_method",
    "mechanism_label",
]


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def stratified_sample(rows, n=48, seed=20260412):
    rng = random.Random(seed)
    buckets = defaultdict(list)
    for row in rows:
        key = row.get("uncertainty_class", "unknown")
        buckets[key].append(row)
    targets = {"low_uncertainty": 14, "moderate_uncertainty": 24, "high_uncertainty": 10}
    sample = []
    seen = set()
    for key, target in targets.items():
        candidates = list(buckets.get(key, []))
        rng.shuffle(candidates)
        for row in candidates:
            if row["record_id"] in seen:
                continue
            sample.append(row)
            seen.add(row["record_id"])
            if sum(1 for x in sample if x.get("uncertainty_class") == key) >= target:
                break
    remaining = [row for row in rows if row["record_id"] not in seen]
    rng.shuffle(remaining)
    for row in remaining:
        if len(sample) >= n:
            break
        sample.append(row)
        seen.add(row["record_id"])
    return sample[:n]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    records = [row for row in read_csv(RECORDS) if row.get("source_is_auto_only") == "true"]
    sample = stratified_sample(records)
    sample_rows = []
    worksheet_rows = []
    for idx, row in enumerate(sample, start=1):
        audit_id = f"VAL_{idx:03d}"
        sample_rows.append(
            {
                "audit_id": audit_id,
                "record_id": row.get("record_id", ""),
                "paper_id": row.get("paper_id", ""),
                "title": row.get("title", ""),
                "abstract": row.get("abstract", ""),
                "claim_text_raw": row.get("claim_text_raw", ""),
                "activity_category": row.get("activity_category", ""),
                "study_type": row.get("study_type", ""),
                "evidence_level": row.get("evidence_level", ""),
                "silver_component_group": row.get("silver_component_group", ""),
                "silver_processing_step": row.get("silver_processing_step", ""),
                "silver_extraction_method": row.get("silver_extraction_method", ""),
                "mechanism_label": row.get("mechanism_label", ""),
                "uncertainty_class": row.get("uncertainty_class", ""),
                "uncertainty_flags": row.get("uncertainty_flags", ""),
            }
        )
        base = {"audit_id": audit_id, "record_id": row.get("record_id", ""), "reviewer_id": "", "review_date": ""}
        for field in FIELDS_TO_REVIEW:
            base[f"{field}_decision"] = ""
            base[f"{field}_corrected"] = ""
        base["overall_record_decision"] = ""
        base["major_issue_type"] = ""
        base["comments"] = ""
        worksheet_rows.append(base)
    sample_fields = list(sample_rows[0].keys())
    worksheet_fields = list(worksheet_rows[0].keys())
    write_csv(OUT_DIR / "validation_sample_v4.csv", sample_fields, sample_rows)
    write_csv(OUT_DIR / "validation_worksheet_v4.csv", worksheet_fields, worksheet_rows)
    guide = """# AutoTeaKG-Silver v4 Validation Guide

Purpose: externally evaluate a stratified sample of silver evidence records. This validation is not used to construct the KG.

For each field decision column, use one of:

- correct
- minor_issue
- major_issue
- not_applicable

For overall_record_decision, use one of:

- accept
- accept_with_correction
- reject

Review against title, abstract, claim text, and if needed the source paper. Fill corrected values only when the model field is not acceptable.
"""
    (OUT_DIR / "validation_guideline_v4.md").write_text(guide, encoding="utf-8")
    print(f"sample={len(sample_rows)}")
    print(f"wrote={OUT_DIR}")


if __name__ == "__main__":
    main()
