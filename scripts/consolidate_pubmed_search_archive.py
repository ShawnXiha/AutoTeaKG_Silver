import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BATCH_ROOT = ROOT / "data" / "pubmed_batches"
REPORTS_DIR = ROOT / "reports"

BATCH_ORDER = [
    "tea_pubmed_batch_2026-03-31_large",
    "tea_pubmed_batch_2026-03-31_large_v2",
    "tea_full_test_2026-04-01",
    "tea_full_prod_2026-04-01",
]

SUMMARY_FIELDS = [
    "batch_name",
    "date_searched",
    "query_count",
    "requested_retmax_per_query",
    "total_query_hits",
    "unique_pmids",
    "normalized_rows",
    "include_count",
    "maybe_count",
    "exclude_count",
]

QUERY_FIELDS = [
    "batch_name",
    "date_searched",
    "search_id",
    "query_id",
    "query_name",
    "query_string",
    "date_filter",
    "result_count",
    "returned_count",
    "export_filename",
    "notes",
]


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def format_method_note(main_batch: dict) -> str:
    return (
        "Recommended manuscript citation batch: "
        f"{main_batch['batch_name']} searched on {main_batch['date_searched']} "
        f"with five PubMed query blocks over the publication window 2022/01/01 to 2026/03/31; "
        f"returned query hits={main_batch['total_query_hits']}, deduplicated unique PMIDs={main_batch['unique_pmids']}, "
        f"heuristic include={main_batch['include_count']}, maybe={main_batch['maybe_count']}, exclude={main_batch['exclude_count']}."
    )


def build_markdown(summary_rows, query_rows, config, main_batch_name: str) -> str:
    main_batch = next(row for row in summary_rows if row["batch_name"] == main_batch_name)
    query_blocks = {item["id"]: item for item in config["queries"]}
    lines = []
    lines.append("# PubMed Search Archive")
    lines.append("")
    lines.append(f"Archive date: 2026-04-02")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("Topic: tea, tea extracts, tea components, functional activity, influencing factors, processing-aware context, and microbiome-related mechanisms.")
    lines.append("")
    lines.append("Database: PubMed")
    lines.append("")
    lines.append(f"Primary date window: {config['mindate']} to {config['maxdate']}")
    lines.append("")
    lines.append("## Recommended Citation Batch")
    lines.append("")
    lines.append(format_method_note(main_batch))
    lines.append("")
    lines.append("Recommended primary search batch for manuscript reporting: `tea_full_prod_2026-04-01`.")
    lines.append("")
    lines.append("Reason: it is the latest larger retrieval batch with the same 5-query design and a `retmax-per-query` of 100, producing 421 deduplicated PubMed records.")
    lines.append("")
    lines.append("## Query Set")
    lines.append("")
    for item in config["queries"]:
        lines.append(f"### {item['id']}. {item['name']}")
        lines.append("")
        lines.append("```text")
        lines.append(item["query"])
        lines.append("```")
        lines.append("")
    lines.append("## Batch Summary")
    lines.append("")
    lines.append("| Batch | Search Date | Retmax/Query | Total Hits | Unique PMIDs | Include | Maybe | Exclude |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
    for row in summary_rows:
        lines.append(
            f"| {row['batch_name']} | {row['date_searched']} | {row['requested_retmax_per_query']} | "
            f"{row['total_query_hits']} | {row['unique_pmids']} | {row['include_count']} | {row['maybe_count']} | {row['exclude_count']} |"
        )
    lines.append("")
    lines.append("## Per-Query Results")
    lines.append("")
    for batch_name in [row["batch_name"] for row in summary_rows]:
        lines.append(f"### {batch_name}")
        lines.append("")
        lines.append("| Query ID | Query Name | Search Date | Date Filter | PubMed Result Count | Returned Top N |")
        lines.append("|---|---|---|---|---:|---:|")
        for row in [r for r in query_rows if r["batch_name"] == batch_name]:
            lines.append(
                f"| {row['query_id']} | {row['query_name']} | {row['date_searched']} | {row['date_filter']} | "
                f"{row['result_count']} | {row['returned_count']} |"
            )
        lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- `total_query_hits` is the sum of top-N returns across the 5 query blocks before deduplication.")
    lines.append("- `unique_pmids` is the deduplicated PubMed count across those retrieved records.")
    lines.append("- `include/maybe/exclude` counts are heuristic title/abstract normalization outputs and should not be treated as final screening counts unless explicitly adjudicated.")
    lines.append("- Search strings and batch-level logs are also preserved in CSV and JSON outputs generated alongside this archive.")
    lines.append("")
    return "\n".join(lines)


def main():
    config = read_json(ROOT / "scripts" / "pubmed_tea_queries_v1.json")
    summary_rows = []
    query_rows = []
    raw_archive = {"config": config, "batches": []}

    for batch_name in BATCH_ORDER:
        batch_dir = BATCH_ROOT / batch_name
        if not batch_dir.exists():
            continue
        summary = read_json(batch_dir / "summary.json")
        search_log = read_csv(batch_dir / "search_log.csv")
        manifest = {item["search_id"]: item for item in read_json(batch_dir / "query_manifest.json")}

        summary_rows.append({field: summary.get(field, "") for field in SUMMARY_FIELDS})
        batch_archive = {
            "summary": summary,
            "search_log": search_log,
            "query_manifest": list(manifest.values()),
        }
        raw_archive["batches"].append({"batch_name": batch_name, **batch_archive})

        for row in search_log:
            manifest_row = manifest.get(row["search_id"], {})
            query_rows.append(
                {
                    "batch_name": batch_name,
                    "date_searched": row.get("date_searched", ""),
                    "search_id": row.get("search_id", ""),
                    "query_id": manifest_row.get("query_id", ""),
                    "query_name": row.get("query_name", ""),
                    "query_string": row.get("query_string", ""),
                    "date_filter": row.get("date_filter", ""),
                    "result_count": row.get("result_count", ""),
                    "returned_count": manifest_row.get("returned_count", ""),
                    "export_filename": row.get("export_filename", ""),
                    "notes": row.get("notes", ""),
                }
            )

    summary_csv = REPORTS_DIR / "pubmed_search_batch_summary_2026-04-02.csv"
    query_csv = REPORTS_DIR / "pubmed_search_query_details_2026-04-02.csv"
    archive_json = REPORTS_DIR / "pubmed_search_archive_2026-04-02.json"
    archive_md = REPORTS_DIR / "pubmed_search_archive_2026-04-02.md"

    write_csv(summary_csv, SUMMARY_FIELDS, summary_rows)
    write_csv(query_csv, QUERY_FIELDS, query_rows)
    write_json(archive_json, raw_archive)
    archive_md.write_text(build_markdown(summary_rows, query_rows, config, "tea_full_prod_2026-04-01"), encoding="utf-8")

    print(f"Wrote: {summary_csv}")
    print(f"Wrote: {query_csv}")
    print(f"Wrote: {archive_json}")
    print(f"Wrote: {archive_md}")


if __name__ == "__main__":
    main()
