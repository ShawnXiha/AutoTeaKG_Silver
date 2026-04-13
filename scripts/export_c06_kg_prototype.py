import csv
import re
import sqlite3
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "teakg_v1.sqlite"
OUT_DIR = ROOT / "data" / "c06_kg_prototype"
NODES_PATH = OUT_DIR / "nodes.csv"
EDGES_PATH = OUT_DIR / "edges.csv"
SUMMARY_PATH = OUT_DIR / "summary.md"


def slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "unknown"


def norm_text(value: str) -> str:
    return (value or "").strip()


def is_meaningful(value: str) -> bool:
    value = norm_text(value)
    if not value:
        return False
    lowered = value.lower()
    blocked = {
        "needs manual extraction",
        "not_applicable",
        "unspecified",
    }
    return lowered not in blocked


def add_node(nodes: dict, node_id: str, node_type: str, label: str, **attrs):
    if node_id not in nodes:
        row = {"node_id": node_id, "node_type": node_type, "label": label}
        row.update(attrs)
        nodes[node_id] = row


def add_edge(edges: list, source: str, target: str, edge_type: str, provenance: str = ""):
    edges.append(
        {
            "source_id": source,
            "target_id": target,
            "edge_type": edge_type,
            "provenance": provenance,
        }
    )


def fetch_rows():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        query = """
        SELECT
            r.record_id,
            r.paper_id,
            p.title,
            p.year,
            p.journal,
            r.tea_type,
            r.component_group,
            r.activity_category,
            r.study_type,
            r.evidence_level,
            r.mechanism_label,
            r.microbiota_taxon,
            r.microbial_metabolite,
            r.host_phenotype,
            r.effect_direction,
            r.claim_text_raw,
            r.confidence_score
        FROM evidence_records_raw r
        LEFT JOIN included_papers_raw p ON p.paper_id = r.paper_id
        WHERE
            r.activity_category IN (
                'gut microbiota modulation',
                'anti-obesity',
                'metabolic improvement',
                'neuroprotection',
                'anti-inflammatory',
                'antioxidant'
            )
            OR LOWER(COALESCE(r.mechanism_label, '')) LIKE '%microbiota%'
            OR LOWER(COALESCE(r.mechanism_label, '')) LIKE '%scfa%'
            OR LOWER(COALESCE(r.mechanism_label, '')) LIKE '%bile acid%'
            OR LOWER(COALESCE(r.mechanism_label, '')) LIKE '%barrier%'
            OR COALESCE(r.microbiota_taxon, '') <> ''
            OR COALESCE(r.microbial_metabolite, '') <> ''
        ORDER BY r.paper_id, r.record_id
        """
        return cur.execute(query).fetchall()
    finally:
        conn.close()


def build_graph(rows):
    nodes = {}
    edges = []
    edge_counter = Counter()
    type_counter = Counter()

    for row in rows:
        paper_id = row["paper_id"]
        record_id = row["record_id"]
        provenance = paper_id

        paper_node = f"paper:{paper_id}"
        add_node(
            nodes,
            paper_node,
            "Paper",
            paper_id,
            year=row["year"],
            journal=row["journal"],
            title=row["title"],
        )

        record_node = f"record:{record_id}"
        add_node(
            nodes,
            record_node,
            "EvidenceRecord",
            record_id,
            effect_direction=row["effect_direction"],
            confidence_score=row["confidence_score"],
            claim_text_raw=row["claim_text_raw"],
        )
        add_edge(edges, paper_node, record_node, "HAS_RECORD", provenance)

        tea_type = norm_text(row["tea_type"])
        if is_meaningful(tea_type):
            tea_node = f"tea_type:{slug(tea_type)}"
            add_node(nodes, tea_node, "TeaType", tea_type)
            add_edge(edges, record_node, tea_node, "HAS_TEA_TYPE", provenance)

        component_group = norm_text(row["component_group"])
        if is_meaningful(component_group):
            comp_node = f"component_group:{slug(component_group)}"
            add_node(nodes, comp_node, "ComponentGroup", component_group)
            add_edge(edges, record_node, comp_node, "HAS_COMPONENT_GROUP", provenance)

        activity = norm_text(row["activity_category"])
        if is_meaningful(activity):
            act_node = f"activity:{slug(activity)}"
            add_node(nodes, act_node, "ActivityCategory", activity)
            add_edge(edges, record_node, act_node, "SUPPORTS_ACTIVITY", provenance)

        study_type = norm_text(row["study_type"])
        if is_meaningful(study_type):
            study_node = f"study_type:{slug(study_type)}"
            add_node(nodes, study_node, "StudyType", study_type)
            add_edge(edges, record_node, study_node, "HAS_STUDY_TYPE", provenance)

        evidence_level = norm_text(row["evidence_level"])
        if is_meaningful(evidence_level):
            ev_node = f"evidence_level:{slug(evidence_level)}"
            add_node(nodes, ev_node, "EvidenceLevel", evidence_level)
            add_edge(edges, record_node, ev_node, "HAS_EVIDENCE_LEVEL", provenance)

        mechanism = norm_text(row["mechanism_label"])
        mechanism_nodes = []
        if is_meaningful(mechanism):
            for mech_part in [m.strip() for m in mechanism.split(";") if m.strip()]:
                mech_node = f"mechanism:{slug(mech_part)}"
                add_node(nodes, mech_node, "Mechanism", mech_part)
                add_edge(edges, record_node, mech_node, "ACTS_VIA", provenance)
                mechanism_nodes.append(mech_node)

        microbiota = norm_text(row["microbiota_taxon"])
        micro_node = ""
        if is_meaningful(microbiota):
            micro_node = f"microbiota:{slug(microbiota)}"
            add_node(nodes, micro_node, "MicrobiotaFeature", microbiota)
            add_edge(edges, record_node, micro_node, "MODULATES_MICROBIOTA", provenance)

        metabolite = norm_text(row["microbial_metabolite"])
        metabolite_node = ""
        if is_meaningful(metabolite):
            metabolite_node = f"metabolite:{slug(metabolite)}"
            add_node(nodes, metabolite_node, "MicrobialMetabolite", metabolite)
            if micro_node:
                add_edge(edges, micro_node, metabolite_node, "LINKS_TO_METABOLITE", provenance)
            else:
                add_edge(edges, record_node, metabolite_node, "LINKS_TO_METABOLITE", provenance)

        phenotype = norm_text(row["host_phenotype"])
        phenotype_node = ""
        if is_meaningful(phenotype):
            phenotype_node = f"phenotype:{slug(phenotype)}"
            add_node(nodes, phenotype_node, "HostPhenotype", phenotype)
            add_edge(edges, record_node, phenotype_node, "ASSOCIATED_HOST_PHENOTYPE", provenance)
            if metabolite_node:
                add_edge(edges, metabolite_node, phenotype_node, "AFFECTS_HOST_PHENOTYPE", provenance)

        for edge in edges[-20:]:
            edge_counter[edge["edge_type"]] += 0

    for node in nodes.values():
        type_counter[node["node_type"]] += 1
    edge_counter = Counter(edge["edge_type"] for edge in edges)
    return nodes, edges, type_counter, edge_counter


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_summary(rows, node_counts, edge_counts):
    lines = [
        "# C06 KG Prototype Summary",
        "",
        f"Date: 2026-03-31",
        f"Source database: `{DB_PATH.name}`",
        "",
        "## Scope",
        "",
        f"- Source evidence records selected for prototype: {len(rows)}",
        f"- Exported node count: {sum(node_counts.values())}",
        f"- Exported edge count: {sum(edge_counts.values())}",
        "",
        "## Node Types",
        "",
    ]
    for node_type, count in sorted(node_counts.items()):
        lines.append(f"- {node_type}: {count}")
    lines.extend(["", "## Edge Types", ""])
    for edge_type, count in sorted(edge_counts.items()):
        lines.append(f"- {edge_type}: {count}")
    lines.extend(
        [
            "",
            "## Graph Design",
            "",
            "- `EvidenceRecord` is kept as a first-class node so every mechanistic statement remains traceable to a source paper.",
            "- The prototype is database-first and provenance-preserving, not a fully normalized biological graph.",
            "- Generic placeholders such as `taxa as reported` are retained when present in the curated source records to avoid inventing unsupported specificity.",
            "",
            "## Recommended Uses",
            "",
            "- Import into Neo4j for prototype exploration",
            "- Use in NetworkX for path inspection",
            "- Identify which nodes need full-text refinement before a production KG build",
        ]
    )
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def main():
    rows = fetch_rows()
    nodes, edges, node_counts, edge_counts = build_graph(rows)
    node_rows = list(nodes.values())
    edge_rows = edges
    write_csv(
        NODES_PATH,
        ["node_id", "node_type", "label", "year", "journal", "title", "effect_direction", "confidence_score", "claim_text_raw"],
        node_rows,
    )
    write_csv(EDGES_PATH, ["source_id", "target_id", "edge_type", "provenance"], edge_rows)
    write_summary(rows, node_counts, edge_counts)
    print(f"Exported nodes to: {NODES_PATH}")
    print(f"Exported edges to: {EDGES_PATH}")
    print(f"Exported summary to: {SUMMARY_PATH}")
    print(f"Rows used: {len(rows)}")
    print(f"Node count: {sum(node_counts.values())}")
    print(f"Edge count: {sum(edge_counts.values())}")


if __name__ == "__main__":
    main()
