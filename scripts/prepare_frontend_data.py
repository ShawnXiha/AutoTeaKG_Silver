import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KG_DIR = ROOT / "reports" / "methods_processing_vocab_normalized"
QUERY_DIR = ROOT / "reports" / "kg_v3_query_tables"
OUT_DIR = ROOT / "frontend" / "data"

NODES_CSV = KG_DIR / "kg_v3" / "nodes.csv"
EDGES_CSV = KG_DIR / "kg_v3" / "edges.csv"
RECORDS_CSV = KG_DIR / "autoteakg_silver_records.csv"


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def compact_node(row):
    return {
        "id": row.get("node_id", ""),
        "type": row.get("node_type", ""),
        "label": row.get("label", ""),
        "title": row.get("title", ""),
        "year": row.get("year", ""),
        "journal": row.get("journal", ""),
        "uncertainty_class": row.get("uncertainty_class", ""),
        "uncertainty_flags": row.get("uncertainty_flags", ""),
        "confidence_score": row.get("confidence_score", ""),
        "claim_text_raw": row.get("claim_text_raw", ""),
    }


def compact_edge(row):
    return {
        "source": row.get("source_id", ""),
        "target": row.get("target_id", ""),
        "type": row.get("edge_type", ""),
        "record_id": row.get("record_id", ""),
        "paper_id": row.get("paper_id", ""),
        "evidence_level": row.get("evidence_level", ""),
        "study_type": row.get("study_type", ""),
        "effect_direction": row.get("effect_direction", ""),
        "uncertainty_class": row.get("uncertainty_class", ""),
        "confidence_score": row.get("confidence_score", ""),
    }


def build_record_lookup(records):
    lookup = {}
    for row in records:
        lookup[row.get("record_id", "")] = {
            "record_id": row.get("record_id", ""),
            "paper_id": row.get("paper_id", ""),
            "title": row.get("title", ""),
            "year": row.get("year", ""),
            "journal": row.get("journal", ""),
            "tea_type": row.get("silver_tea_type", ""),
            "component_group": row.get("silver_component_group", ""),
            "activity_category": row.get("activity_category", ""),
            "evidence_level": row.get("evidence_level", ""),
            "study_type": row.get("study_type", ""),
            "effect_direction": row.get("effect_direction", ""),
            "mechanism_label": row.get("mechanism_label", ""),
            "microbiota_taxon": row.get("microbiota_taxon", ""),
            "microbial_metabolite": row.get("microbial_metabolite", ""),
            "host_phenotype": row.get("host_phenotype", ""),
            "processing_step": row.get("silver_processing_step", ""),
            "extraction_method": row.get("silver_extraction_method", ""),
            "uncertainty_class": row.get("uncertainty_class", ""),
            "uncertainty_flags": row.get("uncertainty_flags", ""),
            "confidence_score": row.get("silver_confidence_score", ""),
            "claim_text_raw": row.get("claim_text_raw", ""),
        }
    return lookup


def make_subgraph(nodes, edges, seed_record_ids, max_records=90):
    allowed_records = set(seed_record_ids[:max_records])
    selected_edges = []
    selected_nodes = set()
    for edge in edges:
        record_id = edge.get("record_id", "")
        if record_id in allowed_records:
            selected_edges.append(edge)
            selected_nodes.add(edge["source"])
            selected_nodes.add(edge["target"])
    node_by_id = {node["id"]: node for node in nodes}
    selected_node_rows = [node_by_id[node_id] for node_id in selected_nodes if node_id in node_by_id]
    return {"nodes": selected_node_rows, "edges": selected_edges}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    nodes = [compact_node(row) for row in read_csv(NODES_CSV)]
    edges = [compact_edge(row) for row in read_csv(EDGES_CSV)]
    records = read_csv(RECORDS_CSV)
    record_lookup = build_record_lookup(records)

    node_counts = Counter(node["type"] for node in nodes)
    edge_counts = Counter(edge["type"] for edge in edges)
    activity_counts = Counter(row.get("activity_category", "") for row in records)
    uncertainty_counts = Counter(row.get("uncertainty_class", "") for row in records)
    evidence_counts = Counter(row.get("evidence_level", "") for row in records)
    component_counts = Counter(row.get("silver_component_group", "") for row in records)
    processing_counts = Counter()
    extraction_counts = Counter()
    for row in records:
        for value in (row.get("silver_processing_step", "") or "").split(";"):
            value = value.strip()
            if value:
                processing_counts[value] += 1
        for value in (row.get("silver_extraction_method", "") or "").split(";"):
            value = value.strip()
            if value:
                extraction_counts[value] += 1

    microbiome_records = [
        row
        for row in record_lookup.values()
        if row["activity_category"] == "gut microbiota modulation"
        or row["microbiota_taxon"]
        or row["microbial_metabolite"]
    ]
    case_records = [
        row
        for row in microbiome_records
        if "polysaccharide" in row["component_group"].lower()
        and (
            "butyr" in (row["microbial_metabolite"] + row["mechanism_label"] + row["host_phenotype"]).lower()
            or "scfa" in (row["microbial_metabolite"] + row["mechanism_label"] + row["host_phenotype"]).lower()
            or "liver" in (row["microbial_metabolite"] + row["mechanism_label"] + row["host_phenotype"]).lower()
        )
    ]
    case_record_ids = [row["record_id"] for row in case_records]
    microbiome_record_ids = [row["record_id"] for row in microbiome_records]

    # Start with graph-query case records, then fill with microbiome records to make a rich but readable demo graph.
    demo_ids = list(dict.fromkeys(case_record_ids + microbiome_record_ids))
    graph = make_subgraph(nodes, edges, demo_ids, max_records=85)

    filters = {
        "activity_categories": sorted(v for v in activity_counts if v),
        "evidence_levels": sorted(v for v in evidence_counts if v),
        "uncertainty_classes": sorted(v for v in uncertainty_counts if v),
        "component_groups": sorted(v for v in component_counts if v),
    }
    metrics = {
        "records": len(records),
        "nodes": len(nodes),
        "edges": len(edges),
        "microbiome_records": len(microbiome_records),
        "processing_present": sum(1 for row in records if row.get("silver_processing_step")),
        "extraction_present": sum(1 for row in records if row.get("silver_extraction_method")),
        "node_counts": node_counts,
        "edge_counts": edge_counts,
        "activity_counts": activity_counts,
        "uncertainty_counts": uncertainty_counts,
        "evidence_counts": evidence_counts,
        "component_counts": component_counts,
        "processing_counts": processing_counts,
        "extraction_counts": extraction_counts,
    }

    payload = {
        "metrics": metrics,
        "filters": filters,
        "graph": graph,
        "records": list(record_lookup.values()),
        "case_record_ids": case_record_ids[:12],
    }
    (OUT_DIR / "autoteakg_frontend_data.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT_DIR / 'autoteakg_frontend_data.json'}")
    print(f"Demo graph nodes={len(graph['nodes'])} edges={len(graph['edges'])} records={len(records)}")


if __name__ == "__main__":
    main()
