import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_NODES = ROOT / "data" / "c06_kg_prototype_v2" / "nodes.csv"
SOURCE_EDGES = ROOT / "data" / "c06_kg_prototype_v2" / "edges.csv"
OUT_DIR = ROOT / "data" / "c06_story_subgraphs"


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def relevant_edge(edge, story_terms):
    text = " ".join([edge["source_id"], edge["target_id"], edge["edge_type"], edge["provenance"]]).lower()
    return any(term in text for term in story_terms)


def relevant_node(node, story_terms):
    text = " ".join(str(v) for v in node.values() if v).lower()
    return any(term in text for term in story_terms)


def export_story(name, story_terms, nodes, edges):
    matched_edges = [e for e in edges if relevant_edge(e, story_terms)]
    node_ids = set()
    for edge in matched_edges:
        node_ids.add(edge["source_id"])
        node_ids.add(edge["target_id"])

    matched_nodes = [n for n in nodes if n["node_id"] in node_ids or relevant_node(n, story_terms)]
    node_ids = {n["node_id"] for n in matched_nodes}
    matched_edges = [e for e in matched_edges if e["source_id"] in node_ids and e["target_id"] in node_ids]

    node_path = OUT_DIR / f"{name}_nodes.csv"
    edge_path = OUT_DIR / f"{name}_edges.csv"
    write_csv(node_path, list(nodes[0].keys()), matched_nodes)
    write_csv(edge_path, list(edges[0].keys()), matched_edges)
    return len(matched_nodes), len(matched_edges)


def main():
    nodes = read_csv(SOURCE_NODES)
    edges = read_csv(SOURCE_EDGES)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    stories = {
        "story_A_polyphenol_obesity": [
            "pmid_39574401",
            "blautia",
            "faecalibaculum",
            "colidextribacter",
            "scfas",
            "tight_junction",
            "barrier",
            "tlr4",
            "obesity_related_phenotype",
        ],
        "story_B_oolong_cognition": [
            "pmid_38745351",
            "muribaculaceae",
            "clostridia_ucg_014",
            "desulfovibrio",
            "lps",
            "glutamate",
            "bdnf",
            "synaptic",
            "cognitive_impairment",
            "microglia",
        ],
        "story_C_polysaccharide_family": [
            "pmid_40957830",
            "pmid_39153277",
            "pmid_36449351",
            "pmid_39479919",
            "tea_polysaccharides",
            "bifidobacterium",
            "butyrate",
            "thermogenesis",
            "fxr",
            "bile",
            "nafld",
            "lactobacillus",
            "oxidative",
            "nf_kb",
            "microglial",
            "dubosiella",
            "romboutsia",
        ],
    }

    summary_rows = []
    for name, terms in stories.items():
        node_count, edge_count = export_story(name, terms, nodes, edges)
        summary_rows.append(
            {
                "story_name": name,
                "node_count": node_count,
                "edge_count": edge_count,
                "terms": "; ".join(terms),
            }
        )

    write_csv(
        OUT_DIR / "story_subgraph_summary.csv",
        ["story_name", "node_count", "edge_count", "terms"],
        summary_rows,
    )
    print(f"Exported story subgraphs to: {OUT_DIR}")
    for row in summary_rows:
        print(f"{row['story_name']}: nodes={row['node_count']} edges={row['edge_count']}")


if __name__ == "__main__":
    main()
