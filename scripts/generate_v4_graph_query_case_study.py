import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "writing_outputs" / "20260412_autoteakg_silver_paper"
DATA_DIR = PAPER_DIR / "data"
FIG_DIR = PAPER_DIR / "figures"
SOURCE = ROOT / "reports" / "kg_v3_query_tables" / "table_microbiome_mechanism_records.csv"


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def select_case_rows(rows):
    selected = []
    for row in rows:
        text = " ".join(row.values()).lower()
        if "polysaccharide" in row.get("component_group", "").lower() and (
            "butyric" in text
            or "butyrate" in text
            or "scfa" in text
            or "liver" in text
            or "nafld" in text
            or "hepatic" in text
            or "inflammation" in text
        ):
            selected.append(row)
    priority = {
        "PMID_41899489_GLM1": 0,
        "PMID_41899489_GLM2": 1,
        "PMID_41475763_GLM1": 2,
        "PMID_41475763_GLM2": 3,
        "PMID_41861686_GLM1": 4,
        "PMID_41544875_GLM1": 5,
    }
    selected.sort(key=lambda r: (priority.get(r.get("record_id", ""), 99), r.get("record_id", "")))
    return selected[:10]


def make_simplified_table(rows):
    out = []
    for row in rows:
        out.append(
            {
                "record_id": row.get("record_id", ""),
                "paper_id": row.get("paper_id", ""),
                "tea_type": row.get("tea_type", ""),
                "component_group": row.get("component_group", ""),
                "mechanism_or_path": row.get("mechanism_label", ""),
                "microbial_metabolite": row.get("microbial_metabolite", ""),
                "host_phenotype": row.get("host_phenotype", ""),
                "evidence_level": row.get("evidence_level", ""),
                "uncertainty_class": row.get("uncertainty_class", ""),
            }
        )
    return out


def add_box(ax, xy, w, h, title, body, color):
    patch = FancyBboxPatch(
        xy,
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.025",
        facecolor=color,
        edgecolor="#263238",
        linewidth=1.0,
    )
    ax.add_patch(patch)
    x, y = xy
    ax.text(x + w / 2, y + h * 0.67, title, ha="center", va="center", fontsize=10, weight="bold")
    ax.text(x + w / 2, y + h * 0.34, body, ha="center", va="center", fontsize=8.2, linespacing=1.2)


def add_arrow(ax, start, end, label=""):
    arrow = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13, linewidth=1.4, color="#546E7A")
    ax.add_patch(arrow)
    if label:
        mx = (start[0] + end[0]) / 2
        my = (start[1] + end[1]) / 2 + 0.045
        ax.text(mx, my, label, ha="center", va="center", fontsize=7.5, color="#37474F")


def plot_case_study(path):
    plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42, "ps.fonttype": 42})
    fig, ax = plt.subplots(figsize=(8.2, 3.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    boxes = [
        ((0.04, 0.42), 0.16, 0.32, "Tea exposure", "tea polysaccharides\nblack/yellow/dark tea", "#E8EDF2"),
        ((0.25, 0.42), 0.17, 0.32, "Microbiota", "gut microbiota\nSCFA producers", "#E8F2EE"),
        ((0.48, 0.42), 0.15, 0.32, "Metabolites", "butyric acid\nSCFAs", "#FFF4DE"),
        ((0.69, 0.42), 0.16, 0.32, "Host programs", "liver inflammation\nbarrier integrity\nlipid deposition", "#FDE8E1"),
    ]
    for args in boxes:
        add_box(ax, *args)
    add_arrow(ax, (0.205, 0.58), (0.245, 0.58), "modulates")
    add_arrow(ax, (0.425, 0.58), (0.475, 0.58), "produces")
    add_arrow(ax, (0.635, 0.58), (0.685, 0.58), "associates with")
    ax.text(0.5, 0.88, "KG query case study: tea polysaccharides -> microbiota/metabolites -> host phenotypes", ha="center", fontsize=12, weight="bold")
    ax.text(0.5, 0.18, "Query filter: component_group contains tea polysaccharides; microbiome/metabolite/host phenotype fields non-empty; evidence and uncertainty retained.", ha="center", fontsize=8.5, color="#37474F")
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def main():
    rows = read_csv(SOURCE)
    selected = select_case_rows(rows)
    table = make_simplified_table(selected)
    write_csv(
        DATA_DIR / "graph_query_case_study_polysaccharide_microbiome_v4.csv",
        [
            "record_id",
            "paper_id",
            "tea_type",
            "component_group",
            "mechanism_or_path",
            "microbial_metabolite",
            "host_phenotype",
            "evidence_level",
            "uncertainty_class",
        ],
        table,
    )
    plot_case_study(FIG_DIR / "fig_graph_query_polysaccharide_microbiome")
    print(f"selected={len(selected)}")
    print(f"wrote={DATA_DIR / 'graph_query_case_study_polysaccharide_microbiome_v4.csv'}")
    print(f"wrote={FIG_DIR / 'fig_graph_query_polysaccharide_microbiome.pdf'}")


if __name__ == "__main__":
    main()
