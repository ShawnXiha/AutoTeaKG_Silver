import argparse
import csv
import json
from pathlib import Path

import build_autoteakg_silver_v1 as silver
from targeted_processing_llm_extractor import PATCH_FIELDS, read_csv, write_csv, write_jsonl, write_patched_outputs


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "reports" / "autoteakg_silver_v1" / "autoteakg_silver_records.csv"
DEFAULT_OUTPUT_DIR = ROOT / "reports" / "targeted_processing_llm_extractor_final"


def read_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def merge_patches(run_dirs):
    merged = {}
    for run_dir in run_dirs:
        patch_path = run_dir / "processing_llm_patches.csv"
        if not patch_path.exists():
            continue
        for patch in read_csv(patch_path):
            record_id = patch.get("record_id", "")
            if record_id:
                merged[record_id] = patch
    return [merged[key] for key in sorted(merged)]


def merge_raw(run_dirs, filename):
    rows = []
    seen = set()
    for run_dir in run_dirs:
        for row in read_jsonl(run_dir / filename):
            key = (row.get("record_id", ""), row.get("paper_id", ""), json.dumps(row.get("patch", row), sort_keys=True))
            if key not in seen:
                rows.append(row)
                seen.add(key)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--run-dirs", type=Path, nargs="+", required=True)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    records = read_csv(args.input)
    patches = merge_patches(args.run_dirs)
    raw_responses = merge_raw(args.run_dirs, "processing_llm_raw_responses.jsonl")
    errors = merge_raw(args.run_dirs, "processing_llm_errors.jsonl")
    patched_ids = {patch.get("record_id", "") for patch in patches}
    unresolved_errors = [error for error in errors if error.get("record_id", "") not in patched_ids]

    write_csv(args.output_dir / "processing_llm_patches.csv", PATCH_FIELDS, patches)
    write_jsonl(args.output_dir / "processing_llm_raw_responses.jsonl", raw_responses)
    write_jsonl(args.output_dir / "processing_llm_errors.jsonl", unresolved_errors)

    patched_summary = write_patched_outputs(args.output_dir, records, patches) if patches else None
    target_count = len(
        [
            row
            for row in records
            if row.get("source_is_auto_only") == "true"
            and "missing_processing_or_extraction_context" in row.get("uncertainty_flags", "")
            and row.get("abstract")
        ]
    )
    summary = {
        "input": str(args.input),
        "output_dir": str(args.output_dir),
        "source_run_dirs": [str(path) for path in args.run_dirs],
        "target_count": target_count,
        "patch_count": len(patches),
        "source_error_count": len(errors),
        "remaining_error_count": len(unresolved_errors),
        "missing_patch_count": max(target_count - len(patches), 0),
        "patched_summary": patched_summary,
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
