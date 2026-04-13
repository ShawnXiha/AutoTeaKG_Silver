import csv
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MERGED_DIR = ROOT / "data" / "merged_batches" / "tea_pubmed_batch_2026-03-31_large_v2_llm_merged"
REPORTS_DIR = ROOT / "reports"
TEMPLATES_DIR = ROOT / "templates"
PROTOCOLS_DIR = ROOT / "protocols"
PUBMED_BATCHES_DIR = ROOT / "data" / "pubmed_batches"

PAPERS_CSV = MERGED_DIR / "included_papers_llm_merged.csv"
RECORDS_CSV = MERGED_DIR / "evidence_records_llm_merged.csv"
DB_PATH = MERGED_DIR / "teakg_llm_merged.sqlite"


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256_of_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def lock_manifest():
    manifest = {
        "lock_id": "tea_evidence_release_2026-04-02_v1",
        "date_locked": "2026-04-02",
        "recommended_for_paper": True,
        "files": [
            {
                "role": "papers_table",
                "path": str(PAPERS_CSV),
                "sha256": sha256_of_file(PAPERS_CSV),
                "size_bytes": PAPERS_CSV.stat().st_size,
            },
            {
                "role": "evidence_records_table",
                "path": str(RECORDS_CSV),
                "sha256": sha256_of_file(RECORDS_CSV),
                "size_bytes": RECORDS_CSV.stat().st_size,
            },
            {
                "role": "sqlite_database",
                "path": str(DB_PATH),
                "sha256": sha256_of_file(DB_PATH),
                "size_bytes": DB_PATH.stat().st_size,
            },
        ],
    }
    out_json = REPORTS_DIR / "teakg_release_lock_2026-04-02_v1.json"
    out_md = REPORTS_DIR / "teakg_release_lock_2026-04-02_v1.md"
    out_json.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    lines = [
        "# TeaKG Release Lock",
        "",
        f"Release ID: `{manifest['lock_id']}`",
        "",
        f"Lock date: `{manifest['date_locked']}`",
        "",
        "Use this release as the fixed paper-writing dataset unless a new lock is created.",
        "",
        "| Role | Path | Size (bytes) | SHA256 |",
        "|---|---|---:|---|",
    ]
    for item in manifest["files"]:
        lines.append(f"| {item['role']} | {item['path']} | {item['size_bytes']} | `{item['sha256']}` |")
    out_md.write_text("\n".join(lines), encoding="utf-8")
    return manifest


def build_paper_lookup():
    papers = read_csv(PAPERS_CSV)
    return {row["paper_id"]: row for row in papers}


def build_abstract_lookup():
    lookup = {}
    raw_files = sorted(PUBMED_BATCHES_DIR.glob("**/pubmed_results_raw.csv"))
    for raw_file in raw_files:
        for row in read_csv(raw_file):
            pmid = (row.get("pmid") or "").strip()
            if not pmid:
                continue
            paper_id = f"PMID_{pmid}"
            abstract = (row.get("abstract") or "").strip()
            title = (row.get("title") or "").strip()
            existing = lookup.get(paper_id, {})
            if not existing or (abstract and not existing.get("abstract", "")):
                lookup[paper_id] = {
                    "abstract": abstract,
                    "title": title,
                    "source_file": str(raw_file.relative_to(ROOT)),
                }
    return lookup


def choose_audit_sample(records, n_total=48, seed=20260402):
    rng = random.Random(seed)
    pools = defaultdict(list)
    for row in records:
        annotator = row.get("annotator_id", "")
        try:
            confidence = float(row.get("confidence_score") or 0)
        except Exception:
            confidence = 0.0
        activity = row.get("activity_category", "")
        paper_id = row.get("paper_id", "")
        if annotator == "glm5_nvidia":
            pools["llm_all"].append(row)
        if annotator == "glm5_nvidia" and confidence < 0.80:
            pools["llm_low_conf"].append(row)
        if annotator == "glm5_nvidia" and activity == "other":
            pools["llm_other"].append(row)
        if annotator == "glm5_nvidia" and (
            activity == "gut microbiota modulation"
            or row.get("microbiota_taxon", "")
            or row.get("microbial_metabolite", "")
        ):
            pools["llm_microbiome"].append(row)
        if annotator == "glm5_nvidia" and row.get("study_type") in {"systematic review", "meta-analysis"}:
            pools["llm_reviews"].append(row)
        if annotator == "glm5_nvidia" and row.get("study_type") == "animal study":
            pools["llm_animals"].append(row)
        if annotator == "codex_v1":
            pools["manual_reference"].append(row)
        if paper_id:
            pools["by_paper:" + paper_id].append(row)

    sample = []
    seen = set()

    def add_from_pool(name, target):
        candidates = list(pools.get(name, []))
        rng.shuffle(candidates)
        added = 0
        for row in candidates:
            if row["record_id"] in seen:
                continue
            sample.append(row)
            seen.add(row["record_id"])
            added += 1
            if added >= target:
                break

    add_from_pool("llm_low_conf", 10)
    add_from_pool("llm_other", 10)
    add_from_pool("llm_microbiome", 12)
    add_from_pool("llm_reviews", 6)
    add_from_pool("llm_animals", 10)

    llm_remaining = [row for row in pools["llm_all"] if row["record_id"] not in seen]
    rng.shuffle(llm_remaining)
    for row in llm_remaining:
        if len(sample) >= n_total:
            break
        sample.append(row)
        seen.add(row["record_id"])

    if len(sample) < n_total:
        manual_ref = [row for row in pools["manual_reference"] if row["record_id"] not in seen]
        rng.shuffle(manual_ref)
        for row in manual_ref:
            if len(sample) >= n_total:
                break
            sample.append(row)
            seen.add(row["record_id"])

    return sample[:n_total]


def build_audit_files():
    records = read_csv(RECORDS_CSV)
    paper_lookup = build_paper_lookup()
    abstract_lookup = build_abstract_lookup()
    sample = choose_audit_sample(records)

    sample_fields = [
        "audit_id",
        "record_id",
        "paper_id",
        "title",
        "abstract",
        "abstract_source",
        "year",
        "journal",
        "annotator_id",
        "adjudication_status",
        "confidence_score",
        "activity_category",
        "endpoint_label",
        "study_type",
        "evidence_level",
        "effect_direction",
        "mechanism_label",
        "microbiota_taxon",
        "microbial_metabolite",
        "host_phenotype",
        "claim_text_raw",
        "sampling_reason",
    ]
    worksheet_fields = [
        "audit_id",
        "record_id",
        "paper_id",
        "annotator_id",
        "confidence_score",
        "field_activity_category",
        "field_endpoint_label",
        "field_study_type",
        "field_evidence_level",
        "field_effect_direction",
        "field_mechanism_label",
        "field_microbiota_taxon",
        "field_microbial_metabolite",
        "field_host_phenotype",
        "paper_scope_decision",
        "overall_record_decision",
        "major_issue_type",
        "corrected_activity_category",
        "corrected_endpoint_label",
        "corrected_study_type",
        "corrected_evidence_level",
        "corrected_effect_direction",
        "corrected_mechanism_label",
        "corrected_microbiota_taxon",
        "corrected_microbial_metabolite",
        "corrected_host_phenotype",
        "reviewer_id",
        "review_date",
        "comments",
    ]

    sample_rows = []
    worksheet_rows = []
    for idx, row in enumerate(sample, start=1):
        paper = paper_lookup.get(row["paper_id"], {})
        abstract_info = abstract_lookup.get(row["paper_id"], {})
        reasons = []
        if row.get("annotator_id") == "glm5_nvidia":
            reasons.append("llm")
        if float(row.get("confidence_score") or 0) < 0.80:
            reasons.append("low_confidence")
        if row.get("activity_category") == "other":
            reasons.append("other_activity")
        if row.get("activity_category") == "gut microbiota modulation" or row.get("microbiota_taxon") or row.get("microbial_metabolite"):
            reasons.append("microbiome")
        if row.get("study_type") in {"systematic review", "meta-analysis"}:
            reasons.append("review")
        audit_id = f"AUDIT_{idx:03d}"
        sample_rows.append(
            {
                "audit_id": audit_id,
                "record_id": row["record_id"],
                "paper_id": row["paper_id"],
                "title": paper.get("title", ""),
                "abstract": abstract_info.get("abstract", ""),
                "abstract_source": abstract_info.get("source_file", ""),
                "year": paper.get("year", ""),
                "journal": paper.get("journal", ""),
                "annotator_id": row.get("annotator_id", ""),
                "adjudication_status": row.get("adjudication_status", ""),
                "confidence_score": row.get("confidence_score", ""),
                "activity_category": row.get("activity_category", ""),
                "endpoint_label": row.get("endpoint_label", ""),
                "study_type": row.get("study_type", ""),
                "evidence_level": row.get("evidence_level", ""),
                "effect_direction": row.get("effect_direction", ""),
                "mechanism_label": row.get("mechanism_label", ""),
                "microbiota_taxon": row.get("microbiota_taxon", ""),
                "microbial_metabolite": row.get("microbial_metabolite", ""),
                "host_phenotype": row.get("host_phenotype", ""),
                "claim_text_raw": row.get("claim_text_raw", ""),
                "sampling_reason": "; ".join(reasons),
            }
        )
        worksheet_rows.append(
            {
                "audit_id": audit_id,
                "record_id": row["record_id"],
                "paper_id": row["paper_id"],
                "annotator_id": row.get("annotator_id", ""),
                "confidence_score": row.get("confidence_score", ""),
                "field_activity_category": "",
                "field_endpoint_label": "",
                "field_study_type": "",
                "field_evidence_level": "",
                "field_effect_direction": "",
                "field_mechanism_label": "",
                "field_microbiota_taxon": "",
                "field_microbial_metabolite": "",
                "field_host_phenotype": "",
                "paper_scope_decision": "",
                "overall_record_decision": "",
                "major_issue_type": "",
                "corrected_activity_category": "",
                "corrected_endpoint_label": "",
                "corrected_study_type": "",
                "corrected_evidence_level": "",
                "corrected_effect_direction": "",
                "corrected_mechanism_label": "",
                "corrected_microbiota_taxon": "",
                "corrected_microbial_metabolite": "",
                "corrected_host_phenotype": "",
                "reviewer_id": "",
                "review_date": "",
                "comments": "",
            }
        )

    sample_out = TEMPLATES_DIR / "llm_manual_audit_sample_2026-04-02.csv"
    worksheet_out = TEMPLATES_DIR / "llm_manual_audit_worksheet_2026-04-02.csv"
    summary_out = REPORTS_DIR / "llm_manual_audit_pack_summary_2026-04-02.md"
    write_csv(sample_out, sample_fields, sample_rows)
    write_csv(worksheet_out, worksheet_fields, worksheet_rows)

    lines = [
        "# LLM Manual Audit Pack Summary",
        "",
        "Audit pack date: 2026-04-02",
        "",
        f"Audit sample size: {len(sample_rows)} records",
        "",
        "Sampling principles:",
        "- prioritize `glm5_nvidia` records",
        "- over-sample `other` activity labels",
        "- over-sample low-confidence records (`confidence_score < 0.80`)",
        "- over-sample microbiome-related records",
        "- retain some review-based records",
        "- include PubMed abstract text whenever available so reviewers can audit from the sample sheet directly",
        "",
        f"Sample file: `{sample_out}`",
        f"Worksheet file: `{worksheet_out}`",
    ]
    summary_out.write_text("\n".join(lines), encoding="utf-8")


def write_guideline():
    guideline = """# LLM Manual Audit Guideline

Date: 2026-04-02

## 1. Purpose

This audit is not a full re-annotation pass. Its goal is to estimate how reliable the current merged tea evidence resource is, especially for records generated by `glm5_nvidia`.

The reviewer should decide whether each sampled record is:

- broadly correct
- partially correct but needs field correction
- incorrect / unsupported by the source abstract or title

## 2. Files You Will Use

- audit sample table: `templates/llm_manual_audit_sample_2026-04-02.csv`
- audit worksheet: `templates/llm_manual_audit_worksheet_2026-04-02.csv`
- merged papers table: `data/merged_batches/tea_pubmed_batch_2026-03-31_large_v2_llm_merged/included_papers_llm_merged.csv`
- merged evidence table: `data/merged_batches/tea_pubmed_batch_2026-03-31_large_v2_llm_merged/evidence_records_llm_merged.csv`

The audit sample table already includes the PubMed abstract and its source file. In most cases you should be able to review directly from that table without going back to PubMed.

## 3. What To Check

For each sampled record, check these fields against the title and abstract shown in the audit sample table:

1. `activity_category`
2. `endpoint_label`
3. `study_type`
4. `evidence_level`
5. `effect_direction`
6. `mechanism_label`
7. `microbiota_taxon`
8. `microbial_metabolite`
9. `host_phenotype`

Also check whether the paper is in scope at all for the tea functional-activity resource.

## 4. How To Fill The Worksheet

For each field-level column named `field_*`, use one of:

- `correct`
- `minor_issue`
- `major_issue`
- `not_applicable`

For `paper_scope_decision`, use one of:

- `in_scope`
- `borderline`
- `out_of_scope`

For `overall_record_decision`, use one of:

- `accept`
- `accept_with_correction`
- `reject`

For `major_issue_type`, use short labels such as:

- `wrong_activity`
- `wrong_endpoint`
- `wrong_study_type`
- `wrong_evidence_level`
- `wrong_direction`
- `hallucinated_mechanism`
- `hallucinated_taxon`
- `out_of_scope_paper`
- `duplicate_record`

## 5. Correction Rules

Use the `corrected_*` columns only when the original field is not acceptable.

Keep corrections short and schema-compatible.

Examples:

- `animal` -> `preclinical_in_vivo`
- `review` -> `evidence_synthesis_nonquantitative`
- `promotes` -> `positive`
- `microbiota_taxa` should become `microbiota_taxon`

Do not rewrite long prose unless necessary. The aim is structured correction, not polishing.

## 6. What Counts As A Major Error

A record should be treated as majorly wrong if:

- the activity category is unsupported by the title/abstract
- the study type is wrong in a way that changes evidence interpretation
- the mechanism/taxon/metabolite is invented rather than supported
- the paper itself is out of scope

## 7. What Counts As A Minor Error

A record can still be usable with minor correction if:

- the label is slightly too broad or too narrow
- the endpoint wording is imprecise but directionally right
- the mechanism is incomplete but not invented
- the host phenotype is vague but still consistent with the abstract

## 8. Suggested Review Order

1. Review all `other_activity` rows first.
2. Review all low-confidence rows next.
3. Review microbiome rows next.
4. Review the remaining rows last.

## 9. Expected Output

After the worksheet is filled, we should be able to compute:

- acceptance rate
- accept-with-correction rate
- rejection rate
- field-level error profile
- common LLM failure patterns

This will support the paper's resource-quality section and the methods/limitations discussion.
"""
    out = PROTOCOLS_DIR / "llm_manual_audit_guideline_2026-04-02.md"
    out.write_text(guideline, encoding="utf-8")


def main():
    lock_manifest()
    build_audit_files()
    write_guideline()
    print("Wrote lock manifest, audit sample, worksheet, and guideline.")


if __name__ == "__main__":
    main()
