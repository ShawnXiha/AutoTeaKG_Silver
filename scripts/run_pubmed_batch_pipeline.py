import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "scripts" / "pubmed_tea_queries_v1.json"
DEFAULT_OUTPUT_ROOT = ROOT / "data" / "pubmed_batches"


def run_step(command):
    print(f"Running: {' '.join(str(part) for part in command)}")
    subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--batch-name", required=True)
    parser.add_argument("--retmax-per-query", type=int, default=300)
    parser.add_argument("--pause-seconds", type=float, default=0.34)
    parser.add_argument("--api-key", default="")
    parser.add_argument("--email", default="")
    parser.add_argument("--candidate-statuses", default="include,maybe")
    args = parser.parse_args()

    batch_dir = DEFAULT_OUTPUT_ROOT / args.batch_name
    papers_csv = batch_dir / "normalized_included_papers.csv"
    records_csv = batch_dir / "candidate_records.csv"
    db_path = batch_dir / "teakg_batch.sqlite"

    run_step(
        [
            sys.executable,
            str(ROOT / "scripts" / "pubmed_tea_batch_retrieval.py"),
            "--config",
            str(args.config),
            "--output-root",
            str(DEFAULT_OUTPUT_ROOT),
            "--batch-name",
            args.batch_name,
            "--retmax-per-query",
            str(args.retmax_per_query),
            "--pause-seconds",
            str(args.pause_seconds),
            "--api-key",
            args.api_key,
            "--email",
            args.email,
        ]
    )
    run_step(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate_candidate_records.py"),
            "--input",
            str(papers_csv),
            "--output",
            str(records_csv),
            "--include-statuses",
            args.candidate_statuses,
        ]
    )
    run_step(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_sqlite_db.py"),
            "--papers",
            str(papers_csv),
            "--records",
            str(records_csv),
            "--db-path",
            str(db_path),
        ]
    )

    print(f"Pipeline complete. Batch directory: {batch_dir}")
    print(f"Included papers: {papers_csv}")
    print(f"Candidate records: {records_csv}")
    print(f"SQLite database: {db_path}")


if __name__ == "__main__":
    main()
