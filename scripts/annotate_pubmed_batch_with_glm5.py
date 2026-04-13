import argparse
import csv
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from nvidia_chatnvidia_compat import ChatNVIDIA


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BATCH_DIR = ROOT / "data" / "pubmed_batches" / "tea_pubmed_batch_2026-03-31_large_v2"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "llm_annotations" / "glm5_test_run"

PAPER_FIELDS = [
    "paper_id",
    "source_db",
    "title",
    "authors",
    "journal",
    "year",
    "doi",
    "pmid",
    "study_type",
    "tea_type",
    "material_form",
    "component_group",
    "activity_category",
    "processing_present",
    "extraction_present",
    "microbiome_present",
    "include_status",
    "exclusion_reason",
    "notes",
]

RECORD_FIELDS = [
    "record_id",
    "paper_id",
    "tea_type",
    "material_form",
    "component_group",
    "compound_name",
    "activity_category",
    "endpoint_label",
    "study_type",
    "evidence_level",
    "model_system",
    "dose_exposure",
    "effect_direction",
    "processing_step",
    "extraction_method",
    "cultivar",
    "origin",
    "mechanism_label",
    "microbiota_taxon",
    "microbial_metabolite",
    "host_phenotype",
    "claim_text_raw",
    "confidence_score",
    "annotator_id",
    "adjudication_status",
    "notes",
]

RECORD_FIELD_ALIASES = {
    "microbiota_taxa": "microbiota_taxon",
    "microbiome_taxa": "microbiota_taxon",
    "microbiome_taxon": "microbiota_taxon",
    "microbial_metabolites": "microbial_metabolite",
    "host_phenotypes": "host_phenotype",
    "mechanism": "mechanism_label",
    "endpoint": "endpoint_label",
}

ALLOWED_VALUES = {
    "activity_category": {
        "antioxidant",
        "anti-inflammatory",
        "metabolic improvement",
        "anti-obesity",
        "gut microbiota modulation",
        "neuroprotection",
        "cardiovascular protection",
        "other",
    },
    "study_type": {
        "systematic review",
        "meta-analysis",
        "randomized controlled trial",
        "cohort study",
        "animal study",
        "in vitro",
        "unspecified",
    },
    "effect_direction": {"positive", "negative", "mixed", "no_clear_effect", "unclear"},
    "include_status": {"include", "maybe", "exclude"},
}

SYSTEM_PROMPT = """You are annotating tea functional-activity literature for a structured evidence database.
Return only valid JSON. No markdown. No commentary outside JSON.
Use only the provided title, abstract, metadata, and auto-candidate hints.
Do not invent details not supported by the abstract or title.
If information is missing, use an empty string.
Keep values concise and schema-compatible.
Keep the output compact.
Set adjudication_status for generated records to "llm_title_abstract_annotated".
Set annotator_id to "glm5_nvidia".
"""


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fields: List[str], rows: List[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: List[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def extract_json_object(text: str) -> dict:
    stripped = text.strip()
    if stripped.startswith("```"):
        parts = [part for part in stripped.split("```") if part.strip()]
        stripped = parts[-1].strip()
        if stripped.lower().startswith("json"):
            stripped = stripped[4:].strip()
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"No JSON object found in model response: {text[:400]}")
    return json.loads(stripped[start : end + 1])


def normalize_score(value) -> str:
    try:
        score = float(value)
    except Exception:
        return "0.60"
    score = max(0.0, min(score, 1.0))
    return f"{score:.2f}"


def safe_text(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_model_dict_keys(payload):
    if not isinstance(payload, dict):
        return payload
    normalized = {}
    for key, value in payload.items():
        clean_key = str(key).strip()
        if isinstance(value, dict):
            normalized[clean_key] = normalize_model_dict_keys(value)
        elif isinstance(value, list):
            normalized[clean_key] = [
                normalize_model_dict_keys(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            normalized[clean_key] = value
    return normalized


def normalize_record_payload(record: dict) -> dict:
    record = normalize_model_dict_keys(record or {})
    normalized = {}
    for key, value in record.items():
        mapped_key = RECORD_FIELD_ALIASES.get(key, key)
        if mapped_key in RECORD_FIELDS:
            normalized[mapped_key] = value
    return normalized


def infer_evidence_level_from_study_type(study_type: str) -> str:
    mapping = {
        "in vitro": "low_preclinical",
        "animal study": "preclinical_in_vivo",
        "randomized controlled trial": "human_interventional",
        "cohort study": "human_observational",
        "meta-analysis": "evidence_synthesis",
        "systematic review": "evidence_synthesis_nonquantitative",
        "unspecified": "",
    }
    return mapping.get(study_type, "")


def normalize_evidence_level(value: str, study_type: str) -> str:
    lower = safe_text(value).lower()
    if not lower:
        return infer_evidence_level_from_study_type(study_type)
    synonym_map = {
        "animal": "preclinical_in_vivo",
        "animal study": "preclinical_in_vivo",
        "preclinical": "preclinical_in_vivo" if study_type == "animal study" else infer_evidence_level_from_study_type(study_type),
        "review": "evidence_synthesis_nonquantitative",
        "systematic review": "evidence_synthesis_nonquantitative",
        "meta-analysis": "evidence_synthesis",
        "rct": "human_interventional",
        "randomized controlled trial": "human_interventional",
        "cohort study": "human_observational",
        "in vitro": "low_preclinical",
    }
    if lower in synonym_map:
        return synonym_map[lower]
    return value


def normalize_effect_direction(value: str) -> str:
    lower = safe_text(value).lower()
    if not lower:
        return "unclear"
    if lower in ALLOWED_VALUES["effect_direction"]:
        return lower
    if any(term in lower for term in ["positive", "improve", "ameliorat", "increase", "reduce", "restor", "protect", "promot", "enhanc", "suppress"]):
        return "positive"
    if any(term in lower for term in ["negative", "worsen", "aggravat", "decrease", "impair"]):
        return "negative"
    if "mixed" in lower:
        return "mixed"
    if "no clear" in lower or "no effect" in lower:
        return "no_clear_effect"
    return "unclear"


def sanitize_record(record: dict, paper_row: dict, index: int) -> dict:
    record = normalize_record_payload(record)
    cleaned = {field: "" for field in RECORD_FIELDS}
    cleaned.update(record)
    cleaned["record_id"] = f"{paper_row['paper_id']}_GLM{index}"
    cleaned["paper_id"] = paper_row["paper_id"]
    cleaned["tea_type"] = cleaned["tea_type"] or paper_row.get("tea_type", "")
    cleaned["material_form"] = cleaned["material_form"] or paper_row.get("material_form", "")
    cleaned["component_group"] = cleaned["component_group"] or paper_row.get("component_group", "")
    cleaned["study_type"] = cleaned["study_type"] or paper_row.get("study_type", "")
    cleaned["activity_category"] = cleaned["activity_category"] or paper_row.get("activity_category", "other")
    if cleaned["activity_category"] not in ALLOWED_VALUES["activity_category"]:
        cleaned["activity_category"] = "other"
    if cleaned["study_type"] not in ALLOWED_VALUES["study_type"]:
        cleaned["study_type"] = paper_row.get("study_type", "unspecified") or "unspecified"
    cleaned["evidence_level"] = normalize_evidence_level(cleaned.get("evidence_level", ""), cleaned["study_type"])
    cleaned["effect_direction"] = normalize_effect_direction(cleaned.get("effect_direction", ""))
    cleaned["confidence_score"] = normalize_score(cleaned.get("confidence_score", "0.60"))
    cleaned["annotator_id"] = "glm5_nvidia"
    cleaned["adjudication_status"] = "llm_title_abstract_annotated"
    return cleaned


def sanitize_paper_update(model_json: dict, paper_row: dict) -> dict:
    model_json = normalize_model_dict_keys(model_json or {})
    updated = dict(paper_row)
    final_status = model_json.get("final_include_status", paper_row.get("include_status", "maybe"))
    if final_status not in ALLOWED_VALUES["include_status"]:
        final_status = paper_row.get("include_status", "maybe")
    updated["include_status"] = final_status
    updated["notes"] = "; ".join(
        item
        for item in [
            safe_text(paper_row.get("notes", "")),
            safe_text(model_json.get("paper_notes", "")),
        ]
        if item
    )
    if final_status != "exclude":
        updated["exclusion_reason"] = ""
    elif not updated.get("exclusion_reason"):
        updated["exclusion_reason"] = safe_text(model_json.get("paper_exclusion_reason", ""))
    return updated


def build_user_prompt(paper_row: dict, raw_row: dict, candidate_rows: List[dict]) -> str:
    candidate_payload = []
    for row in candidate_rows:
        candidate_payload.append(
            {
                "record_id": row.get("record_id", ""),
                "activity_category": row.get("activity_category", ""),
                "endpoint_label": row.get("endpoint_label", ""),
                "mechanism_label": row.get("mechanism_label", ""),
                "microbiota_taxon": row.get("microbiota_taxon", ""),
                "microbial_metabolite": row.get("microbial_metabolite", ""),
                "host_phenotype": row.get("host_phenotype", ""),
            }
        )
    schema_hint = {
        "final_include_status": "include|maybe|exclude",
        "paper_notes": "brief note",
        "paper_exclusion_reason": "",
        "records": [
            {
                "activity_category": "",
                "endpoint_label": "",
                "evidence_level": "",
                "model_system": "",
                "effect_direction": "",
                "mechanism_label": "",
                "microbiota_taxon": "",
                "microbial_metabolite": "",
                "host_phenotype": "",
                "claim_text_raw": "",
                "confidence_score": 0.75,
                "notes": ""
            }
        ]
    }
    payload = {
        "paper_metadata": paper_row,
        "pubmed_raw": {
            "title": raw_row.get("title", ""),
            "abstract": raw_row.get("abstract", ""),
            "publication_types": raw_row.get("publication_types", ""),
            "mesh_terms": raw_row.get("mesh_terms", ""),
            "keywords": raw_row.get("keywords", ""),
        },
        "auto_candidate_hints": candidate_payload,
        "required_output_schema": schema_hint,
        "annotation_rules": [
            "Generate 0-3 evidence records from title/abstract only.",
            "Use empty string when not supported by the abstract.",
            "Do not invent dose, taxa, metabolites, or mechanisms.",
            "If the paper is clearly out of scope, set final_include_status to exclude and records to [].",
            "If the abstract supports multiple distinct outcomes, split into multiple records.",
            "Prefer concise field values over long explanations.",
        ],
    }
    return json.dumps(payload, ensure_ascii=False)


def load_grouped_rows(batch_dir: Path):
    papers = read_csv(batch_dir / "normalized_included_papers.csv")
    raw_rows = read_csv(batch_dir / "pubmed_results_raw.csv")
    candidates = read_csv(batch_dir / "candidate_records.csv")

    raw_by_paper = {f"PMID_{row['pmid']}": row for row in raw_rows}
    candidates_by_paper = defaultdict(list)
    for row in candidates:
        candidates_by_paper[row["paper_id"]].append(row)
    return papers, raw_by_paper, candidates_by_paper


def build_client(api_key: str, model: str, min_interval_seconds: float, timeout_seconds: int, max_tokens: int, enable_thinking: bool, clear_thinking: bool):
    return ChatNVIDIA(
        model=model,
        api_key=api_key,
        temperature=1,
        top_p=1,
        max_tokens=max_tokens,
        extra_body={"chat_template_kwargs": {"enable_thinking": enable_thinking, "clear_thinking": clear_thinking}},
        timeout=timeout_seconds,
        min_interval_seconds=min_interval_seconds,
    )


def response_needs_fallback(response) -> bool:
    content = response.content
    finish_reason = ""
    try:
        finish_reason = safe_text(response.raw["choices"][0].get("finish_reason", ""))
    except Exception:
        finish_reason = ""
    return not content or finish_reason == "length"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-dir", type=Path, default=DEFAULT_BATCH_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-papers", type=int, default=3)
    parser.add_argument("--paper-ids", default="")
    parser.add_argument("--min-interval-seconds", type=float, default=1.6)
    parser.add_argument("--model", default="z-ai/glm5")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--enable-thinking", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("NVIDIA_API_KEY", "")
    if not api_key:
        raise RuntimeError("NVIDIA_API_KEY is not set.")

    papers, raw_by_paper, candidates_by_paper = load_grouped_rows(args.batch_dir)
    allowed_ids = {item.strip() for item in args.paper_ids.split(",") if item.strip()}
    selected = []
    for row in papers:
        if row.get("include_status") not in {"include", "maybe"}:
            continue
        if allowed_ids and row["paper_id"] not in allowed_ids:
            continue
        selected.append(row)
        if not allowed_ids and len(selected) >= args.max_papers:
            break

    primary_client = build_client(
        api_key=api_key,
        model=args.model,
        min_interval_seconds=args.min_interval_seconds,
        timeout_seconds=args.timeout_seconds,
        max_tokens=args.max_tokens,
        enable_thinking=args.enable_thinking,
        clear_thinking=not args.enable_thinking,
    )
    fallback_client = build_client(
        api_key=api_key,
        model=args.model,
        min_interval_seconds=args.min_interval_seconds,
        timeout_seconds=args.timeout_seconds,
        max_tokens=args.max_tokens,
        enable_thinking=True,
        clear_thinking=True,
    )
    final_fallback_client = build_client(
        api_key=api_key,
        model=args.model,
        min_interval_seconds=args.min_interval_seconds,
        timeout_seconds=args.timeout_seconds,
        max_tokens=args.max_tokens,
        enable_thinking=False,
        clear_thinking=True,
    )

    annotated_papers = []
    annotated_records = []
    raw_responses = []
    errors = []

    for paper_row in selected:
        raw_row = raw_by_paper.get(paper_row["paper_id"], {})
        prompt = build_user_prompt(paper_row, raw_row, candidates_by_paper.get(paper_row["paper_id"], []))
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        try:
            response = primary_client.invoke_with_retries(messages, max_retries=args.max_retries)
            raw_responses.append(
                {
                    "paper_id": paper_row["paper_id"],
                    "stage": "primary",
                    "response_content": response.content,
                    "raw_response": response.raw,
                }
            )
            if response_needs_fallback(response):
                response = fallback_client.invoke_with_retries(messages, max_retries=args.max_retries)
                raw_responses.append(
                    {
                        "paper_id": paper_row["paper_id"],
                        "stage": "fallback_clear_thinking",
                        "response_content": response.content,
                        "raw_response": response.raw,
                    }
                )
            if response_needs_fallback(response):
                response = final_fallback_client.invoke_with_retries(messages, max_retries=args.max_retries)
                raw_responses.append(
                    {
                        "paper_id": paper_row["paper_id"],
                        "stage": "fallback_disable_thinking",
                        "response_content": response.content,
                        "raw_response": response.raw,
                    }
                )
            model_json = extract_json_object(response.content)
            model_json = normalize_model_dict_keys(model_json)
            updated_paper = sanitize_paper_update(model_json, paper_row)
            annotated_papers.append(updated_paper)
            for index, record in enumerate(model_json.get("records", []), start=1):
                annotated_records.append(sanitize_record(record, updated_paper, index))
            print(f"Annotated {paper_row['paper_id']} with {len(model_json.get('records', []))} records.")
        except Exception as exc:
            errors.append({"paper_id": paper_row["paper_id"], "error": str(exc)})
            print(f"Failed {paper_row['paper_id']}: {exc}")

    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "llm_screened_papers.csv", PAPER_FIELDS, annotated_papers)
    write_csv(out_dir / "llm_annotated_records.csv", RECORD_FIELDS, annotated_records)
    write_jsonl(out_dir / "llm_raw_responses.jsonl", raw_responses)
    write_jsonl(out_dir / "llm_errors.jsonl", errors)

    summary = {
        "batch_dir": str(args.batch_dir),
        "model": args.model,
        "selected_papers": len(selected),
        "annotated_papers": len(annotated_papers),
        "annotated_records": len(annotated_records),
        "errors": len(errors),
        "output_dir": str(out_dir),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
