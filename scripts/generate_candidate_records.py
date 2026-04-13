import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "templates" / "included_papers_expanded_batch_2026-03-31.csv"
DEFAULT_OUTPUT = ROOT / "data" / "candidate_records_from_included_papers.csv"


OUTPUT_FIELDS = [
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


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def infer_evidence_level(study_type: str) -> str:
    mapping = {
        "in vitro": "low_preclinical",
        "animal study": "preclinical_in_vivo",
        "randomized controlled trial": "human_interventional",
        "cohort study": "human_observational",
        "meta-analysis": "evidence_synthesis",
        "systematic review": "evidence_synthesis_nonquantitative",
    }
    return mapping.get(study_type, "")


def infer_component_group(text: str) -> str:
    text = text.lower()
    if "theaflavin" in text:
        return "theaflavins"
    if "theanine" in text:
        return "theanine"
    if "caffeine" in text:
        return "caffeine"
    if "polysaccharide" in text:
        return "tea polysaccharides"
    if "catechin" in text or "egcg" in text:
        return "catechins"
    if "polyphenol" in text:
        return "mixed polyphenols"
    if "extract" in text:
        return "whole extract"
    return "unspecified"


def infer_activity(text: str) -> str:
    text = text.lower()
    if "microbiota" in text or "microbiome" in text:
        return "gut microbiota modulation"
    if "obesity" in text or "adipose" in text or "thermogenesis" in text:
        return "anti-obesity"
    if "metabolic syndrome" in text or "fasting glucose" in text or "nafld" in text:
        return "metabolic improvement"
    if "anti-inflammatory" in text or "inflammation" in text or "asthmatic" in text:
        return "anti-inflammatory"
    if "oxidative stress" in text or "antioxidant" in text:
        return "antioxidant"
    if "cognition" in text or "neuroprotect" in text or "microglial" in text:
        return "neuroprotection"
    if "cardiovascular" in text or "mortality" in text:
        return "cardiovascular protection"
    return "other"


def infer_activity_set(text: str):
    text = text.lower()
    activities = []
    if "microbiota" in text or "microbiome" in text:
        activities.append("gut microbiota modulation")
    if "obesity" in text or "adipose" in text or "thermogenesis" in text:
        activities.append("anti-obesity")
    if "metabolic syndrome" in text or "fasting glucose" in text or "nafld" in text:
        activities.append("metabolic improvement")
    if "anti-inflammatory" in text or "inflammation" in text or "asthmatic" in text:
        activities.append("anti-inflammatory")
    if "oxidative stress" in text or "antioxidant" in text:
        activities.append("antioxidant")
    if "cognition" in text or "neuroprotect" in text or "microglial" in text:
        activities.append("neuroprotection")
    if "cardiovascular" in text or "mortality" in text:
        activities.append("cardiovascular protection")
    if not activities:
        activities.append("other")
    # preserve order, drop duplicates
    seen = set()
    ordered = []
    for item in activities:
        if item not in seen:
            ordered.append(item)
            seen.add(item)
    return ordered


def infer_material_form(text: str) -> str:
    text = text.lower()
    if "kombucha" in text:
        return "fermented beverage"
    if "extract" in text:
        return "tea extract"
    if "polysaccharide" in text or "theanine" in text or "polyphenol" in text or "catechin" in text:
        return "purified component"
    if "consumption" in text or "tea consumption" in text:
        return "tea infusion"
    return "unspecified material"


def infer_processing(text: str) -> str:
    text = text.lower()
    labels = []
    if "fermented" in text or "kombucha" in text:
        labels.append("fermentation/oxidation")
    if "processing" in text:
        labels.append("processing category contrast")
    return ";".join(labels)


def infer_extraction(text: str) -> str:
    text = text.lower()
    if "ultrasound extraction" in text:
        return "ultrasound extraction"
    if "microwave extraction" in text:
        return "microwave extraction"
    if "supercritical" in text:
        return "supercritical extraction"
    if "extract" in text:
        return "other extraction"
    return ""


def infer_effect_direction(text: str, study_type: str) -> str:
    text = text.lower()
    if "without affecting systemic inflammation" in text:
        return "no_clear_effect"
    if study_type in {"systematic review", "meta-analysis"} and any(
        phrase in text for phrase in ["key factor", "review", "systematic review"]
    ):
        return "mixed"
    return "positive"


def infer_model_system(study_type: str, title: str) -> str:
    title_lower = title.lower()
    if study_type == "randomized controlled trial":
        if "healthy participants" in title_lower:
            return "healthy human participants"
        if "adults" in title_lower:
            return "human adults"
        if "individuals with and without obesity" in title_lower:
            return "human participants with and without obesity"
        return "human trial participants"
    if study_type == "meta-analysis":
        if "randomized" in title_lower:
            return "human randomized trials"
        return "human prospective cohorts"
    if study_type == "animal study":
        if "mice" in title_lower:
            return "mouse model"
        return "animal model"
    return "review synthesis"


def infer_endpoint_label(activity: str, title: str) -> str:
    title_lower = title.lower()
    if activity == "gut microbiota modulation":
        if "scfa" in title_lower or "short-chain fatty acid" in title_lower:
            return "gut microbiota and SCFA-related modulation"
        return "gut microbiota modulation"
    if activity == "anti-obesity":
        if "thermogenesis" in title_lower:
            return "obesity-related phenotype and thermogenesis"
        return "obesity-related phenotype"
    if activity == "metabolic improvement":
        if "nafld" in title_lower:
            return "NAFLD-related metabolic improvement"
        if "metabolic syndrome" in title_lower:
            return "metabolic syndrome-related improvement"
        return "metabolic improvement"
    if activity == "anti-inflammatory":
        return "inflammation-related outcome"
    if activity == "antioxidant":
        return "oxidative stress or antioxidant-status outcome"
    if activity == "neuroprotection":
        return "cognition or neural-protection-related outcome"
    if activity == "cardiovascular protection":
        return "cardiovascular or mortality-related outcome"
    return "candidate endpoint from title"


def infer_mechanism_label(title: str, activity: str) -> str:
    title_lower = title.lower()
    labels = []
    if "gut microbiota" in title_lower or "microbiome" in title_lower:
        labels.append("microbiota-associated mechanism")
    if "scfa" in title_lower or "short-chain fatty acid" in title_lower:
        labels.append("SCFA-associated mechanism")
    if "barrier" in title_lower:
        labels.append("barrier-related mechanism")
    if "inflammation" in title_lower:
        labels.append("inflammation-related mechanism")
    if "bile acid" in title_lower:
        labels.append("bile-acid-associated mechanism")
    if "thermogenesis" in title_lower:
        labels.append("thermogenesis-related mechanism")
    if "oxidative stress" in title_lower:
        labels.append("oxidative-stress-related mechanism")
    if "mapk" in title_lower or "mmp-9" in title_lower:
        labels.append("MAPKs/MMP-9 signaling")
    if "cognitive" in title_lower or "neuroprotect" in title_lower or "microglial" in title_lower:
        labels.append("neuroprotection-related mechanism")
    if not labels:
        if activity in {"gut microbiota modulation", "anti-obesity", "metabolic improvement", "neuroprotection", "anti-inflammatory", "antioxidant"}:
            return "needs manual extraction"
        return ""
    return "; ".join(labels)


def infer_host_phenotype(activity: str, title: str) -> str:
    title_lower = title.lower()
    if activity == "anti-obesity":
        return "obesity-related phenotype"
    if activity == "metabolic improvement":
        if "nafld" in title_lower:
            return "NAFLD phenotype"
        if "metabolic syndrome" in title_lower:
            return "metabolic syndrome phenotype"
        return "metabolic phenotype"
    if activity == "neuroprotection":
        return "cognition or neural phenotype"
    if activity == "antioxidant":
        return "oxidative stress phenotype"
    if activity == "anti-inflammatory":
        return "inflammation phenotype"
    if activity == "gut microbiota modulation":
        return "microbiota-related host phenotype"
    return ""


def infer_microbiota_metabolite(title: str) -> str:
    title_lower = title.lower()
    if "butyrate" in title_lower:
        return "butyrate"
    if "scfa" in title_lower or "short-chain fatty acid" in title_lower:
        return "SCFAs"
    if "bile acid" in title_lower:
        return "bile-acid-related metabolites"
    return ""


def infer_microbiota_taxon(title: str, activity: str) -> str:
    title_lower = title.lower()
    if "microbiota" in title_lower or "microbiome" in title_lower or activity == "gut microbiota modulation":
        return "taxa as reported"
    return ""


def record_from_paper(row, activity: str, idx: int):
    title = row["title"]
    study_type = row["study_type"]
    text = " ".join(
        [
            row.get("title", ""),
            row.get("component_group", ""),
            row.get("activity_category", ""),
            row.get("notes", ""),
        ]
    )
    return {
        "record_id": f"{row['paper_id']}_AUTO{idx}",
        "paper_id": row["paper_id"],
        "tea_type": row.get("tea_type", ""),
        "material_form": row.get("material_form", "") or infer_material_form(text),
        "component_group": row.get("component_group", "") or infer_component_group(text),
        "compound_name": "",
        "activity_category": activity,
        "endpoint_label": infer_endpoint_label(activity, title),
        "study_type": study_type,
        "evidence_level": infer_evidence_level(study_type),
        "model_system": infer_model_system(study_type, title),
        "dose_exposure": "needs manual extraction",
        "effect_direction": infer_effect_direction(title, study_type),
        "processing_step": infer_processing(text),
        "extraction_method": infer_extraction(text),
        "cultivar": "",
        "origin": "",
        "mechanism_label": infer_mechanism_label(title, activity),
        "microbiota_taxon": infer_microbiota_taxon(title, activity),
        "microbial_metabolite": infer_microbiota_metabolite(title),
        "host_phenotype": infer_host_phenotype(activity, title),
        "claim_text_raw": title,
        "confidence_score": "0.55",
        "annotator_id": "auto_v1",
        "adjudication_status": "needs_review",
        "notes": f"Auto-generated candidate record from included paper metadata/title for activity={activity}.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--include-statuses",
        default="include",
        help="Comma-separated include_status values to convert into candidate records.",
    )
    args = parser.parse_args()

    rows = read_csv(args.input)
    allowed_statuses = {item.strip() for item in args.include_statuses.split(",") if item.strip()}
    rows = [r for r in rows if r.get("include_status") in allowed_statuses]
    candidates = []
    for row in rows:
        title = row.get("title", "")
        text = " ".join(
            [
                row.get("title", ""),
                row.get("component_group", ""),
                row.get("activity_category", ""),
                row.get("notes", ""),
            ]
        )
        activities = infer_activity_set(text)
        for idx, activity in enumerate(activities, start=1):
            candidates.append(record_from_paper(row, activity, idx))
    write_csv(args.output, candidates)
    print(f"Wrote {len(candidates)} candidate records to {args.output}")


if __name__ == "__main__":
    main()
