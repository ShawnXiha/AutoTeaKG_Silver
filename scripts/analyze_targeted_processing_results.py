import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = ROOT / "reports" / "autoteakg_silver_v1"
FINAL_DIR = ROOT / "reports" / "targeted_processing_llm_extractor_final"
PATCHED_DIR = FINAL_DIR / "patched_autoteakg_silver_v1"
OUT_MD = ROOT / "reports" / "targeted_processing_result_analysis_2026-04-12.md"
OUT_CSV = ROOT / "reports" / "targeted_processing_before_after_2026-04-12.csv"


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def present(value: str) -> bool:
    return bool((value or "").strip())


def get_summary(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def count_present(rows, field):
    return sum(1 for row in rows if present(row.get(field, "")))


def compare_records(base_rows, patched_rows):
    base = {row["record_id"]: row for row in base_rows}
    patched = {row["record_id"]: row for row in patched_rows}
    rows = []
    for record_id in sorted(set(base) & set(patched)):
        b = base[record_id]
        p = patched[record_id]
        rows.append(
            {
                "record_id": record_id,
                "paper_id": p.get("paper_id", ""),
                "activity_category": p.get("activity_category", ""),
                "study_type": p.get("study_type", ""),
                "component_before": b.get("silver_component_group", ""),
                "component_after": p.get("silver_component_group", ""),
                "processing_before": b.get("silver_processing_step", ""),
                "processing_after": p.get("silver_processing_step", ""),
                "extraction_before": b.get("silver_extraction_method", ""),
                "extraction_after": p.get("silver_extraction_method", ""),
                "uncertainty_before": b.get("uncertainty_class", ""),
                "uncertainty_after": p.get("uncertainty_class", ""),
                "context_score_before": b.get("context_completeness_score", ""),
                "context_score_after": p.get("context_completeness_score", ""),
                "component_added": str(not present(b.get("silver_component_group", "")) and present(p.get("silver_component_group", ""))).lower(),
                "processing_added": str(not present(b.get("silver_processing_step", "")) and present(p.get("silver_processing_step", ""))).lower(),
                "extraction_added": str(not present(b.get("silver_extraction_method", "")) and present(p.get("silver_extraction_method", ""))).lower(),
            }
        )
    return rows


def pct(value, total):
    return f"{(value / total * 100):.1f}%" if total else "0.0%"


def write_report(base_rows, patched_rows, patches, before_after, base_summary, final_summary):
    total = len(patched_rows)
    patch_total = len(patches)
    patch_modes = Counter(
        (
            patch.get("processing_present", ""),
            patch.get("extraction_present", ""),
            patch.get("component_present", ""),
        )
        for patch in patches
    )
    added_component = sum(1 for row in before_after if row["component_added"] == "true")
    added_processing = sum(1 for row in before_after if row["processing_added"] == "true")
    added_extraction = sum(1 for row in before_after if row["extraction_added"] == "true")
    missing_context_before = base_summary["uncertainty_flag_counts"].get("missing_processing_or_extraction_context", 0)
    missing_context_after = final_summary["patched_summary"]["uncertainty_flag_counts"].get(
        "missing_processing_or_extraction_context",
        0,
    )
    lines = [
        "# Targeted Processing Extractor Result Analysis",
        "",
        "Date: 2026-04-12",
        "",
        "## Purpose",
        "",
        "This analysis quantifies what the targeted GLM5 processing/component extractor added after `AutoTeaKG-Silver v1`. It is based only on automatic outputs and does not depend on manual annotation.",
        "",
        "## Run Completion",
        "",
        f"- Target records: {final_summary['target_count']}",
        f"- Final patches: {final_summary['patch_count']}",
        f"- Remaining errors: {final_summary['remaining_error_count']}",
        f"- Missing patches: {final_summary['missing_patch_count']}",
        f"- Source 429 errors recovered by retry: {final_summary.get('source_error_count', 0)}",
        "",
        "## Before/After Context Coverage",
        "",
        "| Field | Before | After | Added |",
        "|---|---:|---:|---:|",
        f"| component group present | {count_present(base_rows, 'silver_component_group')} | {count_present(patched_rows, 'silver_component_group')} | {added_component} |",
        f"| processing step present | {count_present(base_rows, 'silver_processing_step')} | {count_present(patched_rows, 'silver_processing_step')} | {added_processing} |",
        f"| extraction method present | {count_present(base_rows, 'silver_extraction_method')} | {count_present(patched_rows, 'silver_extraction_method')} | {added_extraction} |",
        f"| missing processing/extraction uncertainty flag | {missing_context_before} | {missing_context_after} | {missing_context_before - missing_context_after} resolved |",
        "",
        "## Patch Content Profile",
        "",
        "| processing_present | extraction_present | component_present | Count | Share of patches |",
        "|---|---|---|---:|---:|",
    ]
    for (processing, extraction, component), count in patch_modes.most_common():
        lines.append(f"| {processing} | {extraction} | {component} | {count} | {pct(count, patch_total)} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The targeted extractor completed the missing-context pass, but most abstracts still do not report tea-material processing or extraction details. The largest patch class was `component_present=true` with `processing_present=false` and `extraction_present=false`, indicating that the model mostly confirmed component context rather than finding hidden processing context.",
            "",
            "This is scientifically useful: it suggests that abstract-level tea bioactivity literature often supports component/activity/evidence extraction, but processing and extraction variables require either full text, methods sections, or specialized process-focused retrieval.",
            "",
            "## Method Implication",
            "",
            "For the next experiment, do not simply rerun GLM5 on the same abstracts. The better next step is a full-text or methods-section extractor for the remaining `missing_processing_or_extraction_context` records, plus vocabulary normalization for noisy LLM labels such as `black tea manufacturing`, `matcha production`, and `cold brewing; hot brewing`.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    base_rows = read_csv(BASE_DIR / "autoteakg_silver_records.csv")
    patched_rows = read_csv(PATCHED_DIR / "autoteakg_silver_records.csv")
    patches = read_csv(FINAL_DIR / "processing_llm_patches.csv")
    before_after = compare_records(base_rows, patched_rows)
    write_csv(
        OUT_CSV,
        [
            "record_id",
            "paper_id",
            "activity_category",
            "study_type",
            "component_before",
            "component_after",
            "processing_before",
            "processing_after",
            "extraction_before",
            "extraction_after",
            "uncertainty_before",
            "uncertainty_after",
            "context_score_before",
            "context_score_after",
            "component_added",
            "processing_added",
            "extraction_added",
        ],
        before_after,
    )
    write_report(
        base_rows,
        patched_rows,
        patches,
        before_after,
        get_summary(BASE_DIR / "summary.json"),
        get_summary(FINAL_DIR / "summary.json"),
    )
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_CSV}")


if __name__ == "__main__":
    main()
