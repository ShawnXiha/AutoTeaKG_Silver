import argparse
import csv
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "scripts" / "pubmed_tea_queries_v1.json"
DEFAULT_BATCH_ROOT = ROOT / "data" / "pubmed_batches"
DEFAULT_LLM_ROOT = ROOT / "data" / "llm_annotations"
DEFAULT_MERGE_ROOT = ROOT / "data" / "merged_batches"
DEFAULT_VENV_PYTHON = ROOT / ".venv_nvidia_glm5" / "Scripts" / "python.exe"


def run_step(command, env=None):
    print(f"Running: {' '.join(str(part) for part in command)}")
    subprocess.run(command, check=True, env=env)


def read_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(__import__("json").loads(line))
    return rows


def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def pick_existing_llm_dir(llm_dir: Path, llm_final_dir: Path) -> Optional[Path]:
    if llm_final_dir.exists():
        return llm_final_dir
    if llm_dir.exists():
        return llm_dir
    return None


def load_completed_ids(existing_llm_dir: Path):
    candidates = [
        existing_llm_dir / "llm_screened_papers_cleaned.csv",
        existing_llm_dir / "llm_screened_papers.csv",
    ]
    for path in candidates:
        if path.exists():
            return {row["paper_id"] for row in read_csv(path) if row.get("paper_id")}
    return set()


def load_failed_ids(existing_llm_dir: Path):
    return {row["paper_id"] for row in read_jsonl(existing_llm_dir / "llm_errors.jsonl") if row.get("paper_id")}


def compute_incremental_paper_ids(batch_dir: Path, existing_llm_dir: Optional[Path], explicit_paper_ids: str, include_failed: bool):
    explicit_ids = [item.strip() for item in explicit_paper_ids.split(",") if item.strip()]
    if explicit_ids and not existing_llm_dir:
        return explicit_ids
    papers = read_csv(batch_dir / "normalized_included_papers.csv")
    pending = [row["paper_id"] for row in papers if row.get("include_status") in {"include", "maybe"} and row.get("paper_id")]
    if not existing_llm_dir:
        return pending
    completed = load_completed_ids(existing_llm_dir)
    failed = load_failed_ids(existing_llm_dir) if include_failed else set()
    if explicit_ids:
        incremental = [paper_id for paper_id in explicit_ids if paper_id not in completed]
        for paper_id in failed:
            if paper_id in explicit_ids and paper_id not in incremental:
                incremental.append(paper_id)
        return incremental
    incremental = [paper_id for paper_id in pending if paper_id not in completed]
    for paper_id in failed:
        if paper_id not in incremental:
            incremental.append(paper_id)
    return incremental


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-name", required=True)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--retmax-per-query", type=int, default=100)
    parser.add_argument("--pause-seconds", type=float, default=0.34)
    parser.add_argument("--candidate-statuses", default="include,maybe")
    parser.add_argument("--email", default="")
    parser.add_argument("--pubmed-api-key", default="")
    parser.add_argument("--nvidia-api-key", default="")
    parser.add_argument("--llm-model", default="z-ai/glm5")
    parser.add_argument("--llm-max-papers", type=int, default=10)
    parser.add_argument("--llm-paper-ids", default="")
    parser.add_argument("--llm-min-interval-seconds", type=float, default=1.6)
    parser.add_argument("--llm-timeout-seconds", type=int, default=420)
    parser.add_argument("--llm-max-retries", type=int, default=2)
    parser.add_argument("--llm-max-tokens", type=int, default=2048)
    parser.add_argument("--llm-enable-thinking", action="store_true")
    parser.add_argument("--venv-python", type=Path, default=DEFAULT_VENV_PYTHON)
    parser.add_argument("--skip-pubmed", action="store_true")
    parser.add_argument("--skip-llm", action="store_true")
    parser.add_argument("--skip-merge", action="store_true")
    parser.add_argument("--retry-failed-llm", action="store_true")
    parser.add_argument("--incremental", action="store_true")
    parser.add_argument("--skip-annotated", action="store_true")
    args = parser.parse_args()

    batch_dir = DEFAULT_BATCH_ROOT / args.batch_name
    llm_dir = DEFAULT_LLM_ROOT / f"{args.batch_name}_glm5"
    llm_increment_dir = DEFAULT_LLM_ROOT / f"{args.batch_name}_glm5_increment"
    llm_retry_dir = DEFAULT_LLM_ROOT / f"{args.batch_name}_glm5_retry"
    llm_final_dir = DEFAULT_LLM_ROOT / f"{args.batch_name}_glm5_final"
    merge_dir = DEFAULT_MERGE_ROOT / f"{args.batch_name}_llm_merged"

    if not args.skip_pubmed:
        run_step(
            [
                sys.executable,
                str(ROOT / "scripts" / "run_pubmed_batch_pipeline.py"),
                "--config",
                str(args.config),
                "--batch-name",
                args.batch_name,
                "--retmax-per-query",
                str(args.retmax_per_query),
                "--pause-seconds",
                str(args.pause_seconds),
                "--candidate-statuses",
                args.candidate_statuses,
                "--api-key",
                args.pubmed_api_key,
                "--email",
                args.email,
            ]
        )

    llm_env = os.environ.copy()
    if args.nvidia_api_key:
        llm_env["NVIDIA_API_KEY"] = args.nvidia_api_key

    if not args.skip_llm:
        if "NVIDIA_API_KEY" not in llm_env or not llm_env["NVIDIA_API_KEY"]:
            raise RuntimeError("NVIDIA_API_KEY is required unless --skip-llm is set.")
        if not args.venv_python.exists():
            raise RuntimeError(f"LLM venv python not found: {args.venv_python}")
        use_existing_filter = args.incremental or args.skip_annotated
        existing_llm_dir = pick_existing_llm_dir(llm_dir, llm_final_dir) if use_existing_filter else None
        selected_paper_ids = compute_incremental_paper_ids(
            batch_dir=batch_dir,
            existing_llm_dir=existing_llm_dir,
            explicit_paper_ids=args.llm_paper_ids,
            include_failed=args.retry_failed_llm,
        )

        if use_existing_filter and not selected_paper_ids:
            print("No PMIDs remain after skipping already annotated papers. Reusing existing LLM outputs.")
            llm_final_dir = existing_llm_dir if existing_llm_dir else llm_final_dir
        else:
            llm_run_dir = llm_increment_dir if args.incremental else llm_dir
            llm_command = [
                str(args.venv_python),
                str(ROOT / "scripts" / "annotate_pubmed_batch_with_glm5.py"),
                "--batch-dir",
                str(batch_dir),
                "--output-dir",
                str(llm_run_dir),
                "--max-papers",
                str(args.llm_max_papers),
                "--min-interval-seconds",
                str(args.llm_min_interval_seconds),
                "--timeout-seconds",
                str(args.llm_timeout_seconds),
                "--max-retries",
                str(args.llm_max_retries),
                "--max-tokens",
                str(args.llm_max_tokens),
                "--model",
                args.llm_model,
            ]
            if args.llm_enable_thinking:
                llm_command.append("--enable-thinking")
            if selected_paper_ids:
                llm_command.extend(["--paper-ids", ",".join(selected_paper_ids)])
            run_step(llm_command, env=llm_env)

            if args.retry_failed_llm:
                errors = read_jsonl(llm_run_dir / "llm_errors.jsonl")
                failed_ids = [row["paper_id"] for row in errors if row.get("paper_id")]
                if failed_ids:
                    retry_command = [
                        str(args.venv_python),
                        str(ROOT / "scripts" / "annotate_pubmed_batch_with_glm5.py"),
                        "--batch-dir",
                        str(batch_dir),
                        "--output-dir",
                        str(llm_retry_dir),
                        "--paper-ids",
                        ",".join(failed_ids),
                        "--min-interval-seconds",
                        str(args.llm_min_interval_seconds),
                        "--timeout-seconds",
                        str(max(args.llm_timeout_seconds, 420)),
                        "--max-retries",
                        str(max(args.llm_max_retries, 2)),
                        "--max-tokens",
                        str(args.llm_max_tokens),
                        "--model",
                        args.llm_model,
                    ]
                    if args.llm_enable_thinking:
                        retry_command.append("--enable-thinking")
                    run_step(retry_command, env=llm_env)
                    run_step(
                        [
                            sys.executable,
                            str(ROOT / "scripts" / "merge_llm_run_outputs.py"),
                            "--primary-dir",
                            str(llm_run_dir),
                            "--retry-dir",
                            str(llm_retry_dir),
                            "--output-dir",
                            str(llm_final_dir if args.incremental else llm_final_dir),
                        ]
                    )
                else:
                    if not args.incremental:
                        llm_final_dir = llm_run_dir
                    else:
                        run_step(
                            [
                                sys.executable,
                                str(ROOT / "scripts" / "merge_llm_run_outputs.py"),
                                "--primary-dir",
                                str(llm_run_dir),
                                "--retry-dir",
                                str(llm_run_dir),
                                "--output-dir",
                                str(llm_final_dir),
                            ]
                        )
            else:
                if not args.incremental:
                    llm_final_dir = llm_run_dir
                else:
                    run_step(
                        [
                            sys.executable,
                            str(ROOT / "scripts" / "merge_llm_run_outputs.py"),
                            "--primary-dir",
                            str(llm_run_dir),
                            "--retry-dir",
                            str(llm_run_dir),
                            "--output-dir",
                            str(llm_final_dir),
                        ]
                    )

            if use_existing_filter and existing_llm_dir:
                run_step(
                    [
                        sys.executable,
                        str(ROOT / "scripts" / "merge_llm_run_outputs.py"),
                        "--primary-dir",
                        str(existing_llm_dir),
                        "--retry-dir",
                        str(llm_final_dir),
                        "--output-dir",
                        str(llm_final_dir),
                    ]
                )

            run_step(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "postprocess_llm_annotations.py"),
                    "--llm-dir",
                    str(llm_final_dir),
                ]
            )
    else:
        llm_final_dir = pick_existing_llm_dir(llm_dir, llm_final_dir) or llm_dir

    if not args.skip_merge:
        run_step(
            [
                sys.executable,
                str(ROOT / "scripts" / "merge_llm_annotations_into_master.py"),
                "--llm-dir",
                str(llm_final_dir),
                "--output-dir",
                str(merge_dir),
            ]
        )

    print(f"Batch dir: {batch_dir}")
    print(f"LLM dir: {llm_dir}")
    print(f"Final LLM dir: {llm_final_dir}")
    print(f"Merge dir: {merge_dir}")
    print("Full pipeline complete.")


if __name__ == "__main__":
    main()
