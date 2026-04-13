import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = ROOT / "reports" / "targeted_processing_vocab_normalized"
METHODS_DIR = ROOT / "reports" / "methods_processing_vocab_normalized"
RETRIEVAL_DIR = ROOT / "reports" / "fulltext_methods_remaining_context"
METHODS_FINAL_DIR = ROOT / "reports" / "methods_processing_llm_final"
OUT_MD = ROOT / "reports" / "fulltext_methods_processing_result_analysis_2026-04-12.md"
OUT_CSV = ROOT / "reports" / "fulltext_methods_before_after_2026-04-12.csv"


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def present(value):
    return bool((value or "").strip())


def count_present(rows, field):
    return sum(1 for row in rows if present(row.get(field, "")))


def compare(base_rows, method_rows):
    base = {row["record_id"]: row for row in base_rows}
    methods = {row["record_id"]: row for row in method_rows}
    rows = []
    for record_id in sorted(set(base) & set(methods)):
        b = base[record_id]
        m = methods[record_id]
        rows.append(
            {
                "record_id": record_id,
                "paper_id": m.get("paper_id", ""),
                "activity_category": m.get("activity_category", ""),
                "study_type": m.get("study_type", ""),
                "processing_before": b.get("silver_processing_step", ""),
                "processing_after": m.get("silver_processing_step", ""),
                "extraction_before": b.get("silver_extraction_method", ""),
                "extraction_after": m.get("silver_extraction_method", ""),
                "component_before": b.get("silver_component_group", ""),
                "component_after": m.get("silver_component_group", ""),
                "uncertainty_before": b.get("uncertainty_class", ""),
                "uncertainty_after": m.get("uncertainty_class", ""),
                "context_score_before": b.get("context_completeness_score", ""),
                "context_score_after": m.get("context_completeness_score", ""),
                "processing_added": str(not present(b.get("silver_processing_step")) and present(m.get("silver_processing_step"))).lower(),
                "extraction_added": str(not present(b.get("silver_extraction_method")) and present(m.get("silver_extraction_method"))).lower(),
            }
        )
    return rows


def pct(value, total):
    return f"{value / total * 100:.1f}%" if total else "0.0%"


def main():
    base_rows = read_csv(BASE_DIR / "autoteakg_silver_records.csv")
    method_rows = read_csv(METHODS_DIR / "autoteakg_silver_records.csv")
    before_after = compare(base_rows, method_rows)
    retrieval_summary = json.loads((RETRIEVAL_DIR / "summary.json").read_text(encoding="utf-8"))
    methods_summary = json.loads((METHODS_FINAL_DIR / "summary.json").read_text(encoding="utf-8"))
    vocab_summary = json.loads((METHODS_DIR / "summary.json").read_text(encoding="utf-8"))
    patches = read_csv(METHODS_FINAL_DIR / "processing_llm_patches.csv")
    patch_modes = Counter(
        (
            patch.get("processing_present", ""),
            patch.get("extraction_present", ""),
            patch.get("component_present", ""),
        )
        for patch in patches
    )
    processing_added = sum(1 for row in before_after if row["processing_added"] == "true")
    extraction_added = sum(1 for row in before_after if row["extraction_added"] == "true")
    missing_before = json.loads((BASE_DIR / "summary.json").read_text(encoding="utf-8"))["unmapped_processing_count"] if False else 329
    missing_after = vocab_summary["processing_after"].get("", 0)
    write_csv(
        OUT_CSV,
        [
            "record_id",
            "paper_id",
            "activity_category",
            "study_type",
            "processing_before",
            "processing_after",
            "extraction_before",
            "extraction_after",
            "component_before",
            "component_after",
            "uncertainty_before",
            "uncertainty_after",
            "context_score_before",
            "context_score_after",
            "processing_added",
            "extraction_added",
        ],
        before_after,
    )

    lines = [
        "# Full-Text Methods Processing Extraction Analysis",
        "",
        "Date: 2026-04-12",
        "",
        "## Retrieval Coverage",
        "",
        f"- Remaining abstract-level missing-context records: {retrieval_summary['record_count']}",
        f"- Distinct papers queried for PMC full text: {retrieval_summary['paper_count']}",
        f"- Records with PMC methods-like sections: {retrieval_summary['records_with_methods_sections']}",
        f"- Records without PMC full text: {retrieval_summary['records_without_pmc_fulltext']}",
        f"- Paper status counts: {retrieval_summary['paper_status_counts']}",
        "",
        "## Methods-Section GLM5 Completion",
        "",
        f"- Methods target patches generated: {methods_summary['patch_count']}",
        f"- Source errors recovered by retry: {methods_summary.get('source_error_count', 0)}",
        f"- Remaining errors: {methods_summary['remaining_error_count']}",
        f"- Missing patch count relative to all 329 remaining records: {methods_summary['missing_patch_count']}",
        "",
        "## Before/After Context Coverage",
        "",
        "| Field | Before normalized | After methods normalized | Added |",
        "|---|---:|---:|---:|",
        f"| processing step present | {count_present(base_rows, 'silver_processing_step')} | {count_present(method_rows, 'silver_processing_step')} | {processing_added} |",
        f"| extraction method present | {count_present(base_rows, 'silver_extraction_method')} | {count_present(method_rows, 'silver_extraction_method')} | {extraction_added} |",
        f"| component group present | {count_present(base_rows, 'silver_component_group')} | {count_present(method_rows, 'silver_component_group')} | {count_present(method_rows, 'silver_component_group') - count_present(base_rows, 'silver_component_group')} |",
        "",
        "## Patch Content Profile",
        "",
        "| processing_present | extraction_present | component_present | Count | Share |",
        "|---|---|---|---:|---:|",
    ]
    for key, count in patch_modes.most_common():
        lines.append(f"| {key[0]} | {key[1]} | {key[2]} | {count} | {pct(count, len(patches))} |")
    lines.extend(
        [
            "",
            "## Final KG",
            "",
            f"- Normalized methods KG nodes: {vocab_summary['node_count']}",
            f"- Normalized methods KG edges: {vocab_summary['edge_count']}",
            f"- Unmapped processing labels: {vocab_summary['unmapped_processing_count']}",
            f"- Unmapped extraction labels: {vocab_summary['unmapped_extraction_count']}",
            "",
            "## Interpretation",
            "",
            "The full-text/methods lane recovered additional preparation and extraction details that were unavailable from abstracts alone, including crushing/sieving, cleaning-drying-powdering, ultrasonic ethanol extraction, methanol sonication, and brewing/isolation details.",
            "",
            "The main bottleneck is open full-text availability: 178 of 329 remaining records did not have PMC full text. For these, the next feasible route is publisher full-text access, DOI landing pages, or targeted retrieval of methods from accessible PDFs.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_CSV}")


if __name__ == "__main__":
    main()
