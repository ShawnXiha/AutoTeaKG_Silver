import argparse
import csv
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "reports" / "targeted_processing_vocab_normalized" / "autoteakg_silver_records.csv"
DEFAULT_METHODS_CSV = ROOT / "reports" / "fulltext_methods_remaining_context" / "remaining_context_methods_sections.csv"
DEFAULT_OUT_ROOT = ROOT / "reports" / "methods_processing_llm_batches"


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def select_target_ids(input_path: Path, methods_csv: Path):
    methods = {
        row.get("record_id", ""): row
        for row in read_csv(methods_csv)
        if row.get("methods_text", "")
    }
    rows = read_csv(input_path)
    ids = []
    for row in rows:
        record_id = row.get("record_id", "")
        if (
            row.get("source_is_auto_only") == "true"
            and "missing_processing_or_extraction_context" in row.get("uncertainty_flags", "")
            and record_id in methods
        ):
            ids.append(record_id)
    return ids


def chunks(values, size):
    for start in range(0, len(values), size):
        yield start // size + 1, values[start : start + size]


def run_batch(args, batch_index, record_ids):
    out_dir = args.output_root / f"batch_{batch_index:03d}"
    summary = out_dir / "summary.json"
    if summary.exists() and not args.force:
        print(f"SKIP batch {batch_index:03d}: summary exists")
        return 0
    command = [
        sys.executable,
        "-B",
        str(ROOT / "scripts" / "targeted_processing_llm_extractor.py"),
        "--input",
        str(args.input),
        "--methods-csv",
        str(args.methods_csv),
        "--require-methods-text",
        "--output-dir",
        str(out_dir),
        "--min-interval-seconds",
        str(args.min_interval_seconds),
        "--max-retries",
        str(args.max_retries),
        "--timeout-seconds",
        str(args.timeout_seconds),
        "--max-tokens",
        str(args.max_tokens),
        "--record-ids",
        *record_ids,
    ]
    print(f"RUN batch {batch_index:03d}: {len(record_ids)} records")
    result = subprocess.run(command, cwd=ROOT)
    return result.returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--methods-csv", type=Path, default=DEFAULT_METHODS_CSV)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUT_ROOT)
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--max-batches", type=int, default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--min-interval-seconds", type=float, default=4.0)
    parser.add_argument("--max-retries", type=int, default=5)
    parser.add_argument("--timeout-seconds", type=int, default=420)
    parser.add_argument("--max-tokens", type=int, default=1024)
    args = parser.parse_args()

    args.output_root.mkdir(parents=True, exist_ok=True)
    target_ids = select_target_ids(args.input, args.methods_csv)
    print(f"target_ids={len(target_ids)} batch_size={args.batch_size}")
    failures = []
    for batch_index, record_ids in chunks(target_ids, args.batch_size):
        if args.max_batches is not None and batch_index > args.max_batches:
            break
        code = run_batch(args, batch_index, record_ids)
        if code != 0:
            failures.append({"batch": batch_index, "returncode": code})
            print(f"FAILED batch {batch_index:03d}: returncode={code}")
    if failures:
        print(f"FAILURES={failures}")
        sys.exit(1)
    print("BATCH_RUN_COMPLETE")


if __name__ == "__main__":
    main()
