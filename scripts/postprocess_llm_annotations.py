import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LLM_DIR = ROOT / "data" / "llm_annotations" / "glm5_test_run_v1"

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

ALLOWED_ACTIVITY = {
    "antioxidant",
    "anti-inflammatory",
    "metabolic improvement",
    "anti-obesity",
    "gut microbiota modulation",
    "neuroprotection",
    "cardiovascular protection",
    "other",
}


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def normalize_text(value: str) -> str:
    return " ".join((value or "").strip().lower().split())


def merge_notes(*values) -> str:
    seen = []
    for value in values:
        for item in (value or "").split(";"):
            cleaned = item.strip()
            if cleaned and cleaned not in seen:
                seen.append(cleaned)
    return "; ".join(seen)


def normalize_activity(row: dict) -> str:
    activity = normalize_text(row.get("activity_category", ""))
    endpoint = normalize_text(row.get("endpoint_label", ""))
    mechanism = normalize_text(row.get("mechanism_label", ""))
    phenotype = normalize_text(row.get("host_phenotype", ""))
    title_claim = normalize_text(row.get("claim_text_raw", ""))
    full = " ".join([activity, endpoint, mechanism, phenotype, title_claim])
    if activity in ALLOWED_ACTIVITY:
        return activity
    if any(term in full for term in ["microbiota", "microbiome", "butyr", "scfa", "gut-lung axis", "gut-liver axis"]):
        return "gut microbiota modulation"
    if any(term in full for term in ["obesity", "adipose", "thermogenesis", "weight loss"]):
        return "anti-obesity"
    if any(term in full for term in ["nafld", "metabolic", "glucose", "insulin", "lipid metabolism", "fatty liver", "hepatoprotection"]):
        return "metabolic improvement"
    if any(term in full for term in ["inflammation", "inflammatory", "cytokine", "macrophage"]):
        return "anti-inflammatory"
    if any(term in full for term in ["oxidative", "ferroptosis", "ros", "lipid peroxidation", "antioxidant"]):
        return "antioxidant"
    if any(term in full for term in ["cognition", "neuro", "microglia", "brain"]):
        return "neuroprotection"
    if any(term in full for term in ["cardiovascular", "vascular", "mortality", "arterial"]):
        return "cardiovascular protection"
    return "other"


def normalize_study_type(value: str, evidence_level: str, model_system: str) -> str:
    full = " ".join([normalize_text(value), normalize_text(evidence_level), normalize_text(model_system)])
    if "systematic review" in full or "review" in full:
        return "systematic review"
    if "meta-analysis" in full:
        return "meta-analysis"
    if "randomized controlled trial" in full or "human trial" in full:
        return "randomized controlled trial"
    if "cohort" in full:
        return "cohort study"
    if any(term in full for term in ["mouse", "mice", "rat", "murine", "animal", "in vivo"]):
        return "animal study"
    if any(term in full for term in ["cell", "cells", "in vitro"]):
        return "in vitro"
    return "unspecified"


def normalize_evidence_level(value: str, study_type: str) -> str:
    lower = normalize_text(value)
    if not lower:
        lower = normalize_text(study_type)
    mapping = {
        "animal": "preclinical_in_vivo",
        "animal study": "preclinical_in_vivo",
        "preclinical": "preclinical_in_vivo",
        "preclinical_in_vivo": "preclinical_in_vivo",
        "review": "evidence_synthesis_nonquantitative",
        "systematic review": "evidence_synthesis_nonquantitative",
        "meta-analysis": "evidence_synthesis",
        "high": "preclinical_in_vivo" if study_type == "animal study" else "evidence_synthesis_nonquantitative",
        "in vitro": "low_preclinical",
        "randomized controlled trial": "human_interventional",
        "cohort study": "human_observational",
    }
    if lower in mapping:
        return mapping[lower]
    fallback = {
        "animal study": "preclinical_in_vivo",
        "in vitro": "low_preclinical",
        "systematic review": "evidence_synthesis_nonquantitative",
        "meta-analysis": "evidence_synthesis",
        "randomized controlled trial": "human_interventional",
        "cohort study": "human_observational",
    }
    return fallback.get(study_type, value)


def normalize_effect_direction(value: str) -> str:
    lower = normalize_text(value)
    if lower in {"positive", "negative", "mixed", "no_clear_effect", "unclear"}:
        return lower
    if any(term in lower for term in ["increase", "promote", "ameliorat", "improv", "reduce", "suppress", "protect", "enhanc", "restore", "skews", "shift", "decrease inflammatory", "regulating"]):
        return "positive"
    if any(term in lower for term in ["worsen", "aggravat", "impair", "harm"]):
        return "negative"
    return "unclear"


def normalize_model_system(value: str, study_type: str) -> str:
    lower = normalize_text(value)
    if study_type == "animal study":
        if "c57bl/6j" in lower:
            return "C57BL/6J mouse model"
        if "mouse" in lower or "mice" in lower:
            return "mouse model"
        if "rat" in lower:
            return "rat model"
        return value or "animal model"
    if study_type == "in vitro":
        return value or "cell model"
    if study_type in {"systematic review", "meta-analysis"}:
        return value or "review synthesis"
    return value


def normalize_paper_row(row: dict) -> dict:
    cleaned = {field: row.get(field, "") for field in PAPER_FIELDS}
    cleaned["notes"] = merge_notes(cleaned.get("notes", ""), "llm_postprocessed=true")
    return cleaned


def normalize_record_row(row: dict) -> dict:
    cleaned = {field: row.get(field, "") for field in RECORD_FIELDS}
    cleaned["study_type"] = normalize_study_type(cleaned.get("study_type", ""), cleaned.get("evidence_level", ""), cleaned.get("model_system", ""))
    cleaned["evidence_level"] = normalize_evidence_level(cleaned.get("evidence_level", ""), cleaned["study_type"])
    cleaned["activity_category"] = normalize_activity(cleaned)
    cleaned["effect_direction"] = normalize_effect_direction(cleaned.get("effect_direction", ""))
    cleaned["model_system"] = normalize_model_system(cleaned.get("model_system", ""), cleaned["study_type"])
    cleaned["notes"] = merge_notes(cleaned.get("notes", ""), "llm_postprocessed=true")
    return cleaned


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm-dir", type=Path, default=DEFAULT_LLM_DIR)
    args = parser.parse_args()

    papers_in = args.llm_dir / "llm_screened_papers.csv"
    records_in = args.llm_dir / "llm_annotated_records.csv"
    papers_out = args.llm_dir / "llm_screened_papers_cleaned.csv"
    records_out = args.llm_dir / "llm_annotated_records_cleaned.csv"
    summary_out = args.llm_dir / "llm_postprocess_summary.json"

    papers = [normalize_paper_row(row) for row in read_csv(papers_in)]
    records = [normalize_record_row(row) for row in read_csv(records_in)]

    write_csv(papers_out, PAPER_FIELDS, papers)
    write_csv(records_out, RECORD_FIELDS, records)

    summary = {
        "papers_in": str(papers_in),
        "records_in": str(records_in),
        "papers_out": str(papers_out),
        "records_out": str(records_out),
        "paper_count": len(papers),
        "record_count": len(records),
    }
    summary_out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
