import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List

from nvidia_chatnvidia_compat import ChatNVIDIA

import build_autoteakg_silver_v1 as silver


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SILVER_DIR = ROOT / "reports" / "autoteakg_silver_v1"
DEFAULT_INPUT = DEFAULT_SILVER_DIR / "autoteakg_silver_records.csv"
DEFAULT_OUTPUT_DIR = ROOT / "reports" / "targeted_processing_llm_extractor"

PATCH_FIELDS = [
    "record_id",
    "paper_id",
    "processing_present",
    "extraction_present",
    "component_present",
    "tea_type",
    "material_form",
    "component_group",
    "processing_step",
    "extraction_method",
    "compound_name",
    "cultivar",
    "origin",
    "evidence_terms",
    "raw_context_phrase",
    "confidence_score",
    "reasoning_short",
    "patch_status",
    "patch_uncertainty_flags",
]

ALLOWED_TEA_TYPES = {
    "green tea",
    "oolong tea",
    "black tea",
    "white tea",
    "yellow tea",
    "dark/post-fermented tea",
    "fermented tea",
    "fermented tea beverage",
    "unspecified tea",
}

ALLOWED_MATERIAL_FORMS = {
    "tea leaf",
    "tea infusion",
    "tea extract",
    "purified component",
    "enriched fraction",
    "fermented beverage",
    "unspecified material",
}

ALLOWED_COMPONENT_GROUPS = {
    "catechins",
    "theaflavins",
    "theanine",
    "caffeine",
    "tea polysaccharides",
    "volatile compounds",
    "mixed polyphenols",
    "whole extract",
    "multiple component groups",
    "unspecified",
}

SYSTEM_PROMPT = """You extract tea processing, extraction, and component context for a tea functional evidence database.
Return only valid JSON. No markdown. No commentary outside JSON.
Use only the provided title, abstract, methods_text/full_text excerpt, and existing record fields.
Prioritize the methods_text/full_text excerpt when it is available.
Do not infer tea processing from host disease/model terms such as skin aging, middle-aged, oxidative stress, freeze-dried sperm, or storage of non-tea samples.
If no tea-material processing or extraction context is reported, use empty strings and false booleans.
Keep labels schema-compatible and concise.
"""


def read_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames: List[str], rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_jsonl(path: Path, rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def extract_json_object(text: str) -> dict:
    stripped = (text or "").strip()
    if stripped.startswith("```"):
        parts = [part for part in stripped.split("```") if part.strip()]
        stripped = parts[-1].strip()
        if stripped.lower().startswith("json"):
            stripped = stripped[4:].strip()
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"No JSON object found: {stripped[:300]}")
    return json.loads(stripped[start : end + 1])


def safe_bool(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value or "").strip().lower()
    if text in {"true", "yes", "1", "present"}:
        return "true"
    if text in {"false", "no", "0", "absent", ""}:
        return "false"
    return "false"


def safe_score(value) -> str:
    try:
        score = float(value)
    except Exception:
        return "0.60"
    score = max(0.0, min(score, 1.0))
    return f"{score:.2f}"


def normalize_label(value, allowed, default="") -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    lower = text.lower()
    aliases = {
        "dark tea": "dark/post-fermented tea",
        "post-fermented tea": "dark/post-fermented tea",
        "post fermented tea": "dark/post-fermented tea",
        "kombucha": "fermented tea beverage",
        "polyphenols": "mixed polyphenols",
        "tea polyphenols": "mixed polyphenols",
        "polysaccharides": "tea polysaccharides",
        "egcg": "catechins",
        "epigallocatechin gallate": "catechins",
        "extract": "whole extract",
    }
    lower = aliases.get(lower, lower)
    for item in allowed:
        if lower == item.lower():
            return item
    return default


def split_join(values) -> str:
    if isinstance(values, list):
        return "; ".join(str(item).strip() for item in values if str(item).strip())
    return str(values or "").strip()


def sanitize_patch(payload: dict, record: dict) -> dict:
    payload = payload or {}
    patch = {
        "record_id": record.get("record_id", ""),
        "paper_id": record.get("paper_id", ""),
        "processing_present": safe_bool(payload.get("processing_present")),
        "extraction_present": safe_bool(payload.get("extraction_present")),
        "component_present": safe_bool(payload.get("component_present", True)),
        "tea_type": normalize_label(payload.get("tea_type"), ALLOWED_TEA_TYPES),
        "material_form": normalize_label(payload.get("material_form"), ALLOWED_MATERIAL_FORMS),
        "component_group": normalize_label(payload.get("component_group"), ALLOWED_COMPONENT_GROUPS),
        "processing_step": split_join(payload.get("processing_step")),
        "extraction_method": split_join(payload.get("extraction_method")),
        "compound_name": split_join(payload.get("compound_name")),
        "cultivar": split_join(payload.get("cultivar")),
        "origin": split_join(payload.get("origin")),
        "evidence_terms": split_join(payload.get("evidence_terms")),
        "raw_context_phrase": split_join(payload.get("raw_context_phrase")),
        "confidence_score": safe_score(payload.get("confidence_score")),
        "reasoning_short": split_join(payload.get("reasoning_short")),
        "patch_status": "llm_extracted",
        "patch_uncertainty_flags": split_join(payload.get("uncertainty_flags")),
    }
    if patch["processing_present"] == "false":
        patch["processing_step"] = ""
    if patch["extraction_present"] == "false":
        patch["extraction_method"] = ""
    if patch["component_present"] == "false":
        patch["component_group"] = ""
        patch["compound_name"] = ""
    return patch


def build_prompt(record: dict) -> List[Dict[str, str]]:
    user_prompt = {
        "task": "Extract only tea-material processing, extraction, and component context.",
        "allowed_values": {
            "tea_type": sorted(ALLOWED_TEA_TYPES),
            "material_form": sorted(ALLOWED_MATERIAL_FORMS),
            "component_group": sorted(ALLOWED_COMPONENT_GROUPS),
        },
        "output_schema": {
            "processing_present": "boolean",
            "extraction_present": "boolean",
            "component_present": "boolean",
            "tea_type": "string from allowed values or empty",
            "material_form": "string from allowed values or empty",
            "component_group": "string from allowed values or empty",
            "processing_step": "semicolon-separated concise tea processing labels or empty",
            "extraction_method": "semicolon-separated concise extraction methods or empty",
            "compound_name": "semicolon-separated named compounds or empty",
            "cultivar": "reported cultivar or empty",
            "origin": "reported origin or empty",
            "evidence_terms": "short exact evidence terms from title/abstract",
            "raw_context_phrase": "short phrase supporting the extracted context",
            "confidence_score": "0.0-1.0",
            "reasoning_short": "one short reason",
            "uncertainty_flags": "semicolon-separated flags if any",
        },
        "record": {
            "record_id": record.get("record_id", ""),
            "paper_id": record.get("paper_id", ""),
            "title": record.get("title", ""),
            "abstract": record.get("abstract", ""),
            "methods_text": (record.get("methods_text", "") or "")[:6000],
            "pmcid": record.get("pmcid", ""),
            "fulltext_retrieval_status": record.get("retrieval_status", ""),
            "claim_text_raw": record.get("claim_text_raw", ""),
            "activity_category": record.get("activity_category", ""),
            "endpoint_label": record.get("endpoint_label", ""),
            "existing_tea_type": record.get("silver_tea_type", record.get("tea_type", "")),
            "existing_material_form": record.get("silver_material_form", record.get("material_form", "")),
            "existing_component_group": record.get("silver_component_group", record.get("component_group", "")),
            "existing_processing_step": record.get("silver_processing_step", ""),
            "existing_extraction_method": record.get("silver_extraction_method", ""),
        },
    }
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(user_prompt, ensure_ascii=False)},
    ]


def select_targets(records: List[dict], args) -> List[dict]:
    rows = []
    requested_ids = set(args.record_ids or [])
    for row in records:
        if requested_ids and row.get("record_id") not in requested_ids:
            continue
        if row.get("source_is_auto_only") != "true":
            continue
        flags = row.get("uncertainty_flags", "")
        if args.only_missing_context and "missing_processing_or_extraction_context" not in flags:
            continue
        if args.only_with_abstract and not row.get("abstract"):
            continue
        if args.require_methods_text and not row.get("methods_text"):
            continue
        rows.append(row)
    if args.max_records is not None:
        rows = rows[: args.max_records]
    return rows


def merge_methods_text(records: List[dict], methods_csv: Path) -> List[dict]:
    if not methods_csv:
        return records
    methods_rows = read_csv(methods_csv)
    by_record = {row.get("record_id", ""): row for row in methods_rows}
    merged = []
    for row in records:
        next_row = dict(row)
        methods = by_record.get(row.get("record_id", ""), {})
        if methods:
            next_row["methods_text"] = methods.get("methods_text", "")
            next_row["pmcid"] = methods.get("pmcid", "")
            next_row["retrieval_status"] = methods.get("retrieval_status", "")
            next_row["section_count"] = methods.get("section_count", "")
        merged.append(next_row)
    return merged


def mock_patch(record: dict) -> dict:
    text = " ".join([record.get("title", ""), record.get("abstract", "")])
    processing, processing_terms = silver.detect_patterns(text, silver.PROCESSING_PATTERNS)
    extraction, extraction_terms = silver.detect_patterns(text, silver.EXTRACTION_PATTERNS)
    component, component_terms = silver.detect_patterns(text, silver.COMPONENT_PATTERNS)
    tea_type, _ = silver.detect_patterns(text, silver.TEA_TYPE_PATTERNS)
    material, _ = silver.detect_patterns(text, silver.MATERIAL_PATTERNS)
    return sanitize_patch(
        {
            "processing_present": bool(processing),
            "extraction_present": bool(extraction),
            "component_present": bool(component),
            "tea_type": tea_type or record.get("silver_tea_type", ""),
            "material_form": material or record.get("silver_material_form", ""),
            "component_group": component or record.get("silver_component_group", ""),
            "processing_step": processing,
            "extraction_method": extraction,
            "evidence_terms": "; ".join(item for item in [component_terms, processing_terms, extraction_terms] if item),
            "raw_context_phrase": "",
            "confidence_score": 0.70,
            "reasoning_short": "mock rule-based extraction",
            "uncertainty_flags": "mock_extraction",
        },
        record,
    )


def run_extraction(targets: List[dict], args):
    patches = []
    raw_responses = []
    errors = []
    if args.dry_run:
        return patches, raw_responses, errors

    client = None
    if not args.mock:
        api_key = args.api_key or os.environ.get("NVIDIA_API_KEY", "")
        client = ChatNVIDIA(
            model=args.model,
            api_key=api_key,
            temperature=args.temperature,
            top_p=args.top_p,
            max_tokens=args.max_tokens,
            timeout=args.timeout_seconds,
            min_interval_seconds=args.min_interval_seconds,
            extra_body={"chat_template_kwargs": {"enable_thinking": False, "clear_thinking": True}},
        )

    for index, record in enumerate(targets, start=1):
        try:
            if args.mock:
                patch = mock_patch(record)
                raw = {"mock": True}
            else:
                result = client.invoke_with_retries(build_prompt(record), max_retries=args.max_retries)
                raw_payload = extract_json_object(result.content)
                patch = sanitize_patch(raw_payload, record)
                raw = result.raw
            patches.append(patch)
            raw_responses.append(
                {
                    "record_id": record.get("record_id", ""),
                    "paper_id": record.get("paper_id", ""),
                    "raw": raw,
                    "patch": patch,
                }
            )
            print(f"[{index}/{len(targets)}] OK {record.get('record_id')}")
        except Exception as exc:
            error = {
                "record_id": record.get("record_id", ""),
                "paper_id": record.get("paper_id", ""),
                "error": str(exc),
            }
            errors.append(error)
            print(f"[{index}/{len(targets)}] FAILED {record.get('record_id')}: {exc}", file=sys.stderr)
        if not args.mock and args.min_interval_seconds > 0:
            time.sleep(0.01)
    return patches, raw_responses, errors


def patch_replaces_missing(existing: str, patch_value: str) -> str:
    patch_value = str(patch_value or "").strip()
    existing = str(existing or "").strip()
    if patch_value:
        return patch_value
    return existing


def recompute_after_patch(row: dict) -> dict:
    mech_score = silver.mechanism_specificity(
        row.get("mechanism_label", ""),
        row.get("microbiota_taxon", ""),
        row.get("microbial_metabolite", ""),
    )
    context_score = silver.context_completeness(
        row.get("silver_tea_type", ""),
        row.get("silver_component_group", ""),
        row.get("silver_processing_step", ""),
        row.get("silver_extraction_method", ""),
    )
    component_score = silver.specificity_for_value(
        row.get("silver_component_group", ""),
        {"unspecified", "multiple component groups"},
    )
    tea_score = silver.specificity_for_value(row.get("silver_tea_type", ""), {"unspecified tea"})
    llm_confidence = silver.confidence_to_float(row.get("confidence_score"))
    record_specificity = round((component_score + tea_score + mech_score + context_score) / 4, 3)
    silver_confidence = round((0.55 * llm_confidence) + (0.25 * record_specificity) + (0.20 * context_score), 3)
    flags = silver.assign_uncertainty(row)
    row["uncertainty_flags"] = "; ".join(flags)
    row["schema_validation_flags"] = "; ".join(silver.validate_schema(row))
    row["record_specificity_score"] = f"{record_specificity:.3f}"
    row["mechanism_specificity_score"] = f"{mech_score:.3f}"
    row["context_completeness_score"] = f"{context_score:.3f}"
    row["silver_confidence_score"] = f"{silver_confidence:.3f}"
    row["uncertainty_class"] = silver.classify_uncertainty(flags, silver_confidence)
    return row


def apply_patches(records: List[dict], patches: List[dict]) -> List[dict]:
    patch_by_record = {patch["record_id"]: patch for patch in patches if patch.get("patch_status") == "llm_extracted"}
    patched = []
    for row in records:
        next_row = dict(row)
        patch = patch_by_record.get(row.get("record_id", ""))
        if patch:
            next_row["silver_tea_type"] = patch_replaces_missing(next_row.get("silver_tea_type", ""), patch.get("tea_type", ""))
            next_row["silver_material_form"] = patch_replaces_missing(
                next_row.get("silver_material_form", ""),
                patch.get("material_form", ""),
            )
            next_row["silver_component_group"] = patch_replaces_missing(
                next_row.get("silver_component_group", ""),
                patch.get("component_group", ""),
            )
            next_row["silver_processing_step"] = patch_replaces_missing(
                next_row.get("silver_processing_step", ""),
                patch.get("processing_step", ""),
            )
            next_row["silver_extraction_method"] = patch_replaces_missing(
                next_row.get("silver_extraction_method", ""),
                patch.get("extraction_method", ""),
            )
            next_row["compound_name"] = patch_replaces_missing(next_row.get("compound_name", ""), patch.get("compound_name", ""))
            next_row["cultivar"] = patch_replaces_missing(next_row.get("cultivar", ""), patch.get("cultivar", ""))
            next_row["origin"] = patch_replaces_missing(next_row.get("origin", ""), patch.get("origin", ""))
            next_row["component_evidence_terms"] = patch_replaces_missing(
                next_row.get("component_evidence_terms", ""),
                patch.get("evidence_terms", ""),
            )
            next_row["processing_evidence_terms"] = patch_replaces_missing(
                next_row.get("processing_evidence_terms", ""),
                patch.get("evidence_terms", ""),
            )
            next_row["extraction_evidence_terms"] = patch_replaces_missing(
                next_row.get("extraction_evidence_terms", ""),
                patch.get("evidence_terms", ""),
            )
            note = f"targeted_processing_llm_patch={patch.get('patch_status')}; patch_confidence={patch.get('confidence_score')}"
            next_row["notes"] = "; ".join(item for item in [next_row.get("notes", ""), note] if item)
            next_row = recompute_after_patch(next_row)
        patched.append(next_row)
    return patched


def write_patched_outputs(out_dir: Path, records: List[dict], patches: List[dict]) -> dict:
    patched = apply_patches(records, patches)
    nodes, edges = silver.build_kg_v3(patched)
    summary = silver.summarize_records(patched, {"targeted_processing_llm_patches": len(patches)}, nodes, edges)
    patched_dir = out_dir / "patched_autoteakg_silver_v1"
    kg_dir = patched_dir / "kg_v3"
    patched_dir.mkdir(parents=True, exist_ok=True)
    kg_dir.mkdir(parents=True, exist_ok=True)
    silver.write_csv(patched_dir / "autoteakg_silver_records.csv", silver.SILVER_FIELDS, patched)
    silver.write_csv(kg_dir / "nodes.csv", sorted({field for row in nodes for field in row}), nodes)
    silver.write_csv(kg_dir / "edges.csv", sorted({field for row in edges for field in row}), edges)
    (patched_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    silver.write_markdown_summary(patched_dir / "summary.md", summary, patched_dir)
    return summary


def write_target_manifest(out_dir: Path, targets: List[dict], args) -> None:
    rows = [
        {
            "record_id": row.get("record_id", ""),
            "paper_id": row.get("paper_id", ""),
            "title": row.get("title", ""),
            "silver_tea_type": row.get("silver_tea_type", ""),
            "silver_component_group": row.get("silver_component_group", ""),
            "silver_processing_step": row.get("silver_processing_step", ""),
            "silver_extraction_method": row.get("silver_extraction_method", ""),
            "uncertainty_class": row.get("uncertainty_class", ""),
            "uncertainty_flags": row.get("uncertainty_flags", ""),
            "abstract_available": "true" if row.get("abstract") else "false",
        }
        for row in targets
    ]
    write_csv(
        out_dir / "target_records.csv",
        [
            "record_id",
            "paper_id",
            "title",
            "silver_tea_type",
            "silver_component_group",
            "silver_processing_step",
            "silver_extraction_method",
            "uncertainty_class",
            "uncertainty_flags",
            "abstract_available",
        ],
        rows,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--methods-csv", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-records", type=int, default=None)
    parser.add_argument("--record-ids", nargs="*", default=None)
    parser.add_argument("--only-missing-context", action="store_true", default=True)
    parser.add_argument("--include-all-context-statuses", action="store_true")
    parser.add_argument("--only-with-abstract", action="store_true", default=True)
    parser.add_argument("--require-methods-text", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--mock", action="store_true")
    parser.add_argument("--no-apply", action="store_true")
    parser.add_argument("--api-key", default="")
    parser.add_argument("--model", default="z-ai/glm5")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--top-p", type=float, default=1.0)
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--timeout-seconds", type=int, default=420)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--min-interval-seconds", type=float, default=1.6)
    args = parser.parse_args()

    if args.include_all_context_statuses:
        args.only_missing_context = False

    records = merge_methods_text(read_csv(args.input), args.methods_csv)
    targets = select_targets(records, args)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_target_manifest(args.output_dir, targets, args)

    patches, raw_responses, errors = run_extraction(targets, args)
    write_csv(args.output_dir / "processing_llm_patches.csv", PATCH_FIELDS, patches)
    write_jsonl(args.output_dir / "processing_llm_raw_responses.jsonl", raw_responses)
    write_jsonl(args.output_dir / "processing_llm_errors.jsonl", errors)

    patched_summary = None
    if patches and not args.no_apply:
        patched_summary = write_patched_outputs(args.output_dir, records, patches)

    summary = {
        "input": str(args.input),
        "output_dir": str(args.output_dir),
        "target_count": len(targets),
        "patch_count": len(patches),
        "error_count": len(errors),
        "dry_run": args.dry_run,
        "mock": args.mock,
        "applied_patches": bool(patches and not args.no_apply),
        "patched_summary": patched_summary,
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
