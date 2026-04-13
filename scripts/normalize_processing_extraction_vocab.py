import argparse
import csv
import json
from collections import Counter
from pathlib import Path

import build_autoteakg_silver_v1 as silver


ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "reports" / "targeted_processing_llm_extractor_final" / "patched_autoteakg_silver_v1"
INPUT_RECORDS = INPUT_DIR / "autoteakg_silver_records.csv"
OUT_DIR = ROOT / "reports" / "targeted_processing_vocab_normalized"


PROCESSING_MAP = {
    "compressed/brick tea processing": "compressed/brick tea processing",
    "black tea processing": "black tea processing",
    "green tea processing": "green tea processing",
    "white tea processing": "white tea processing",
    "oolong tea processing": "oolong tea processing",
    "powder/matcha processing": "powder/matcha processing",
    "processing by-product": "processing by-product",
    "thermal processing/heating": "thermal processing/heating",
    "raw vs ripened processing": "raw vs ripened processing",
    "enzymatic oxidation": "enzymatic oxidation",
    "crushing/grinding/sieving": "crushing/grinding/sieving",
    "cleaning": "cleaning",
    "shading": "shading",
    "fermentation/oxidation": "fermentation/oxidation",
    "storage/aging": "storage/aging",
    "enzymatic treatment": "enzymatic treatment",
    "roasting": "roasting",
    "pan-firing/fixation": "pan-firing/fixation",
    "drying": "drying",
    "decaffeination": "decaffeination",
    "brick-like form": "compressed/brick tea processing",
    "brick tea processing": "compressed/brick tea processing",
    "black tea manufacturing": "black tea processing",
    "black tea formation": "black tea processing",
    "black tea processing": "black tea processing",
    "green tea processing": "green tea processing",
    "white tea processing": "white tea processing",
    "oolong tea processing": "oolong tea processing",
    "matcha production": "powder/matcha processing",
    "finely ground powder production": "powder/matcha processing",
    "finely ground powder": "powder/matcha processing",
    "shading": "shading",
    "tea processing by-product": "processing by-product",
    "tea dust production": "processing by-product",
    "thermal processing": "thermal processing/heating",
    "heating": "thermal processing/heating",
    "processing transformations": "processing category contrast",
    "processing category contrast": "processing category contrast",
    "minimal processing": "minimal processing",
    "raw": "raw vs ripened processing",
    "ripened": "raw vs ripened processing",
    "raw pu-erh": "raw vs ripened processing",
    "ripened pu-erh": "raw vs ripened processing",
    "post-fermentation": "storage/aging",
    "shade drying": "drying",
    "hot-air drying": "drying",
    "vacuum freeze-drying": "drying",
    "crushed": "crushing/grinding/sieving",
    "sieved (20-mesh)": "crushing/grinding/sieving",
    "sieved through 20-mesh sieve": "crushing/grinding/sieving",
    "cleaned": "cleaning",
    "shade dried": "drying",
    "shade-dried": "drying",
    "blended to powder": "crushing/grinding/sieving",
    "vacuum-drying": "drying",
    "grinding": "crushing/grinding/sieving",
    "fermentation": "fermentation/oxidation",
    "oxidative conversion": "fermentation/oxidation",
    "oxidation": "fermentation/oxidation",
    "polyphenol oxidase catalysis": "enzymatic oxidation",
    "peroxidase catalysis": "enzymatic oxidation",
    "polyphenol oxidase-catalysed oxidation": "enzymatic oxidation",
    "peroxidase-catalysed oxidation": "enzymatic oxidation",
    "dimerization of epicatechins": "enzymatic oxidation",
    "roasted": "roasting",
    "powdered": "crushing/grinding/sieving",
    "steaming": "steaming",
    "polyphenol oxidase inactivation": "pan-firing/fixation",
}

EXTRACTION_MAP = {
    "analytical characterization": "analytical characterization",
    "brewing/infusion": "brewing/infusion",
    "isolation/purification": "isolation/purification",
    "ultrasound-assisted extraction": "ultrasound-assisted extraction",
    "ethanol extraction": "ethanol extraction",
    "filtration/concentration": "filtration/concentration",
    "commercial preparation": "commercial preparation",
    "microwave-assisted extraction": "microwave-assisted extraction",
    "other extraction": "other extraction",
    "aqueous extraction": "aqueous extraction",
    "solvent extraction": "solvent extraction",
    "supercritical fluid extraction": "supercritical fluid extraction",
    "essential oil extraction": "essential oil extraction",
    "cold brewing": "brewing/infusion",
    "hot brewing": "brewing/infusion",
    "isolation": "isolation/purification",
    "isolated": "isolation/purification",
    "purification": "isolation/purification",
    "extract": "other extraction",
    "chromatography": "analytical characterization",
    "mass spectrometry": "analytical characterization",
    "nuclear magnetic resonance": "analytical characterization",
    "lc-ms/ms": "analytical characterization",
    "hs-spme-gcms": "analytical characterization",
    "soaked overnight": "aqueous extraction",
    "ultrasonic extraction": "ultrasound-assisted extraction",
    "ethanol 70% extraction": "ethanol extraction",
    "ethanol 70%": "ethanol extraction",
    "filtration": "filtration/concentration",
    "evaporation under reduced pressure": "filtration/concentration",
    "laboratory preparation": "other extraction",
    "hplc": "analytical characterization",
    "lc-ms/ms": "analytical characterization",
    "brewed": "brewing/infusion",
    "methanol extraction": "solvent extraction",
    "sonication": "ultrasound-assisted extraction",
    "microwave-assisted extraction": "microwave-assisted extraction",
    "tea extract": "other extraction",
    "high performance liquid chromatography": "analytical characterization",
    "thin-layer chromatography": "analytical characterization",
    "commercial preparation": "commercial preparation",
    "commercial extract": "commercial preparation",
}


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def split_labels(value: str):
    return [part.strip() for part in silver.split_values(value)]


def normalize_labels(value: str, mapping: dict):
    raw_parts = split_labels(value)
    normalized = []
    unmapped = []
    for part in raw_parts:
        key = part.lower().strip()
        mapped = mapping.get(key)
        if mapped:
            normalized.extend(split_labels(mapped))
        elif part:
            unmapped.append(part)
    deduped = []
    seen = set()
    for item in normalized:
        item = item.strip()
        if item and item not in seen:
            deduped.append(item)
            seen.add(item)
    return "; ".join(deduped), "; ".join(unmapped)


def recompute(row):
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


def normalize_records(rows):
    out = []
    mapping_rows = []
    for row in rows:
        next_row = dict(row)
        raw_processing = row.get("silver_processing_step", "")
        raw_extraction = row.get("silver_extraction_method", "")
        norm_processing, unmapped_processing = normalize_labels(raw_processing, PROCESSING_MAP)
        norm_extraction, unmapped_extraction = normalize_labels(raw_extraction, EXTRACTION_MAP)
        changed = raw_processing != norm_processing or raw_extraction != norm_extraction
        next_row["raw_silver_processing_step"] = raw_processing
        next_row["raw_silver_extraction_method"] = raw_extraction
        next_row["silver_processing_step"] = norm_processing
        next_row["silver_extraction_method"] = norm_extraction
        if unmapped_processing or unmapped_extraction:
            flags = [flag for flag in silver.split_values(next_row.get("uncertainty_flags", ""))]
            flags.append("unmapped_processing_or_extraction_label")
            next_row["uncertainty_flags"] = "; ".join(sorted(set(flags)))
        next_row = recompute(next_row)
        out.append(next_row)
        if raw_processing or raw_extraction or changed or unmapped_processing or unmapped_extraction:
            mapping_rows.append(
                {
                    "record_id": row.get("record_id", ""),
                    "paper_id": row.get("paper_id", ""),
                    "raw_processing": raw_processing,
                    "normalized_processing": norm_processing,
                    "unmapped_processing": unmapped_processing,
                    "raw_extraction": raw_extraction,
                    "normalized_extraction": norm_extraction,
                    "unmapped_extraction": unmapped_extraction,
                    "changed": str(changed).lower(),
                }
            )
    return out, mapping_rows


def write_summary(path: Path, input_records: Path, base_rows, normalized_rows, nodes, edges, mapping_rows):
    summary = {
        "date": "2026-04-12",
        "input_records": str(input_records),
        "record_count": len(normalized_rows),
        "mapping_row_count": len(mapping_rows),
        "changed_mapping_count": sum(1 for row in mapping_rows if row["changed"] == "true"),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "processing_before": dict(Counter(row.get("silver_processing_step", "") for row in base_rows)),
        "processing_after": dict(Counter(row.get("silver_processing_step", "") for row in normalized_rows)),
        "extraction_before": dict(Counter(row.get("silver_extraction_method", "") for row in base_rows)),
        "extraction_after": dict(Counter(row.get("silver_extraction_method", "") for row in normalized_rows)),
        "unmapped_processing_count": sum(1 for row in mapping_rows if row.get("unmapped_processing")),
        "unmapped_extraction_count": sum(1 for row in mapping_rows if row.get("unmapped_extraction")),
    }
    (path / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# Processing/Extraction Vocabulary Normalization Summary",
        "",
        "Date: 2026-04-12",
        "",
        f"- Records: {summary['record_count']}",
        f"- Mapping rows: {summary['mapping_row_count']}",
        f"- Changed mappings: {summary['changed_mapping_count']}",
        f"- KG nodes: {summary['node_count']}",
        f"- KG edges: {summary['edge_count']}",
        f"- Unmapped processing labels: {summary['unmapped_processing_count']}",
        f"- Unmapped extraction labels: {summary['unmapped_extraction_count']}",
        "",
        "## Processing Labels After Normalization",
        "",
    ]
    for label, count in Counter(summary["processing_after"]).most_common(30):
        lines.append(f"- {label or '(blank)'}: {count}")
    lines.extend(["", "## Extraction Labels After Normalization", ""])
    for label, count in Counter(summary["extraction_after"]).most_common(30):
        lines.append(f"- {label or '(blank)'}: {count}")
    (path / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-records", type=Path, default=INPUT_RECORDS)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    kg_dir = args.out_dir / "kg_v3"
    kg_dir.mkdir(parents=True, exist_ok=True)
    rows = read_csv(args.input_records)
    normalized, mapping_rows = normalize_records(rows)
    fields = list(silver.SILVER_FIELDS) + ["raw_silver_processing_step", "raw_silver_extraction_method"]
    write_csv(args.out_dir / "autoteakg_silver_records.csv", fields, normalized)
    write_csv(
        args.out_dir / "processing_extraction_vocab_mapping.csv",
        [
            "record_id",
            "paper_id",
            "raw_processing",
            "normalized_processing",
            "unmapped_processing",
            "raw_extraction",
            "normalized_extraction",
            "unmapped_extraction",
            "changed",
        ],
        mapping_rows,
    )
    nodes, edges = silver.build_kg_v3(normalized)
    write_csv(kg_dir / "nodes.csv", sorted({field for row in nodes for field in row}), nodes)
    write_csv(kg_dir / "edges.csv", sorted({field for row in edges for field in row}), edges)
    write_summary(args.out_dir, args.input_records, rows, normalized, nodes, edges, mapping_rows)
    print(f"Wrote {args.out_dir}")


if __name__ == "__main__":
    main()
