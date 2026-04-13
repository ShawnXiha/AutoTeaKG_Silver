import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
KG_DIR = ROOT / "reports" / "methods_processing_vocab_normalized"
RECORDS_CSV = KG_DIR / "autoteakg_silver_records.csv"
NODES_CSV = KG_DIR / "kg_v3" / "nodes.csv"
EDGES_CSV = KG_DIR / "kg_v3" / "edges.csv"

AUTO_SUMMARY = ROOT / "reports" / "autoteakg_silver_v1" / "summary.json"
TARGETED_SUMMARY = ROOT / "reports" / "targeted_processing_vocab_normalized" / "summary.json"
METHODS_ANALYSIS = ROOT / "reports" / "fulltext_methods_processing_result_analysis_2026-04-12.md"

OUT_TABLE_DIR = ROOT / "reports" / "kg_v3_query_tables"
OUT_FIG_DIR = ROOT / "figures" / "kg_v3"

ACTIVITY_ORDER = [
    "gut microbiota modulation",
    "antioxidant",
    "anti-inflammatory",
    "anti-obesity",
    "metabolic improvement",
    "cardiovascular protection",
    "neuroprotection",
    "other",
]

EVIDENCE_ORDER = [
    "preclinical_in_vivo",
    "evidence_synthesis_nonquantitative",
    "human_observational",
    "human_interventional",
    "evidence_synthesis",
    "low_preclinical",
    "in_vitro",
]

STAGE_LABELS = ["Auto rules", "Abstract LLM", "Methods LLM"]


def setup_style():
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif"],
            "font.size": 9.5,
            "axes.titlesize": 11,
            "axes.titleweight": "bold",
            "axes.labelsize": 9.5,
            "legend.fontsize": 8.3,
            "legend.frameon": False,
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.16,
            "grid.linestyle": "-",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


COLORS = {
    "deep": "#264653",
    "teal": "#2A9D8F",
    "gold": "#E9C46A",
    "sand": "#F4A261",
    "coral": "#E76F51",
    "blue": "#0072B2",
    "sky": "#56B4E9",
    "gray": "#B0BEC5",
    "darkgray": "#5F6C72",
    "green": "#009E73",
}


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def present(value):
    return bool((value or "").strip())


def split_values(value):
    return [part.strip() for part in (value or "").split(";") if part.strip()]


def count_present(records, field):
    return sum(1 for row in records if present(row.get(field, "")))


def save_fig(fig, name):
    OUT_FIG_DIR.mkdir(parents=True, exist_ok=True)
    pdf = OUT_FIG_DIR / f"{name}.pdf"
    png = OUT_FIG_DIR / f"{name}.png"
    svg = OUT_FIG_DIR / f"{name}.svg"
    fig.savefig(pdf)
    fig.savefig(png, dpi=300)
    fig.savefig(svg)
    plt.close(fig)


def table_activity_evidence(records):
    counts = Counter((r.get("activity_category", ""), r.get("evidence_level", "")) for r in records)
    rows = []
    for activity in ACTIVITY_ORDER:
        total = sum(counts[(activity, ev)] for ev in EVIDENCE_ORDER)
        for evidence in EVIDENCE_ORDER:
            rows.append(
                {
                    "activity_category": activity,
                    "evidence_level": evidence,
                    "count": counts[(activity, evidence)],
                    "activity_total": total,
                }
            )
    return rows


def table_activity_study(records):
    counts = Counter((r.get("activity_category", ""), r.get("study_type", "")) for r in records)
    study_types = [label for label, _ in Counter(r.get("study_type", "") for r in records).most_common()]
    rows = []
    for activity in ACTIVITY_ORDER:
        for study in study_types:
            rows.append(
                {
                    "activity_category": activity,
                    "study_type": study,
                    "count": counts[(activity, study)],
                }
            )
    return rows


def table_context_by_activity(records, field, out_field):
    rows = []
    for record in records:
        values = split_values(record.get(field, ""))
        if not values:
            continue
        for value in values:
            rows.append(
                {
                    out_field: value,
                    "activity_category": record.get("activity_category", ""),
                    "evidence_level": record.get("evidence_level", ""),
                    "study_type": record.get("study_type", ""),
                    "record_id": record.get("record_id", ""),
                    "paper_id": record.get("paper_id", ""),
                    "uncertainty_class": record.get("uncertainty_class", ""),
                }
            )
    return rows


def table_uncertainty_by_activity(records):
    classes = ["low_uncertainty", "moderate_uncertainty", "high_uncertainty"]
    counts = Counter((r.get("activity_category", ""), r.get("uncertainty_class", "")) for r in records)
    rows = []
    for activity in ACTIVITY_ORDER:
        total = sum(counts[(activity, c)] for c in classes)
        for cls in classes:
            rows.append(
                {
                    "activity_category": activity,
                    "uncertainty_class": cls,
                    "count": counts[(activity, cls)],
                    "activity_total": total,
                    "share": counts[(activity, cls)] / total if total else 0,
                }
            )
    return rows


def table_microbiome(records):
    rows = []
    for row in records:
        if (
            row.get("activity_category") == "gut microbiota modulation"
            or present(row.get("microbiota_taxon"))
            or present(row.get("microbial_metabolite"))
        ):
            rows.append(
                {
                    "record_id": row.get("record_id", ""),
                    "paper_id": row.get("paper_id", ""),
                    "tea_type": row.get("silver_tea_type", ""),
                    "component_group": row.get("silver_component_group", ""),
                    "activity_category": row.get("activity_category", ""),
                    "mechanism_label": row.get("mechanism_label", ""),
                    "microbiota_taxon": row.get("microbiota_taxon", ""),
                    "microbial_metabolite": row.get("microbial_metabolite", ""),
                    "host_phenotype": row.get("host_phenotype", ""),
                    "evidence_level": row.get("evidence_level", ""),
                    "uncertainty_class": row.get("uncertainty_class", ""),
                }
            )
    return rows


def table_kg_counts(nodes, edges):
    node_counts = Counter(n.get("node_type", "") for n in nodes)
    edge_counts = Counter(e.get("edge_type", "") for e in edges)
    rows = []
    for label, count in node_counts.most_common():
        rows.append({"kind": "node", "type": label, "count": count})
    for label, count in edge_counts.most_common():
        rows.append({"kind": "edge", "type": label, "count": count})
    return rows


def compute_stage_metrics(records):
    auto = load_json(AUTO_SUMMARY)
    targeted = load_json(TARGETED_SUMMARY)
    methods = load_json(KG_DIR / "summary.json")
    # Count present fields directly for the final stage; summaries provide intermediate stages.
    auto_proc = sum(v for k, v in auto["silver_processing_step_counts"].items() if k)
    auto_ext = sum(v for k, v in auto["silver_extraction_method_counts"].items() if k)
    targeted_proc = sum(v for k, v in targeted["processing_after"].items() if k)
    targeted_ext = sum(v for k, v in targeted["extraction_after"].items() if k)
    method_proc = count_present(records, "silver_processing_step")
    method_ext = count_present(records, "silver_extraction_method")
    metrics = [
        {"stage": "Auto rules", "processing_present": auto_proc, "extraction_present": auto_ext, "missing_context_flag": 365},
        {"stage": "Abstract LLM", "processing_present": targeted_proc, "extraction_present": targeted_ext, "missing_context_flag": 329},
        {"stage": "Methods LLM", "processing_present": method_proc, "extraction_present": method_ext, "missing_context_flag": 303},
    ]
    return metrics


def plot_context_coverage(stage_rows):
    x = np.arange(len(stage_rows))
    width = 0.34
    proc = [row["processing_present"] for row in stage_rows]
    ext = [row["extraction_present"] for row in stage_rows]
    fig, ax = plt.subplots(figsize=(5.6, 3.0), constrained_layout=True)
    bars1 = ax.bar(x - width / 2, proc, width, label="Processing step", color=COLORS["teal"], edgecolor="white", linewidth=0.6)
    bars2 = ax.bar(x + width / 2, ext, width, label="Extraction method", color=COLORS["coral"], edgecolor="white", linewidth=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels([row["stage"] for row in stage_rows])
    ax.set_ylabel("Records with context")
    ax.set_title("Context coverage improves through targeted extraction")
    ax.legend(ncol=2, loc="upper left")
    for bars in [bars1, bars2]:
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 4, f"{int(bar.get_height())}", ha="center", va="bottom", fontsize=8)
    ax.set_ylim(0, max(max(proc), max(ext)) * 1.22)
    save_fig(fig, "fig_context_coverage")


def plot_remaining_missing(stage_rows):
    labels = [row["stage"] for row in stage_rows]
    values = [row["missing_context_flag"] for row in stage_rows]
    fig, ax = plt.subplots(figsize=(4.8, 2.8), constrained_layout=True)
    bars = ax.bar(labels, values, color=[COLORS["gray"], COLORS["gold"], COLORS["deep"]], edgecolor="white", linewidth=0.6)
    ax.set_ylabel("Records flagged missing")
    ax.set_title("Residual missing-context burden")
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 4, str(val), ha="center", fontsize=8)
    ax.set_ylim(0, max(values) * 1.18)
    save_fig(fig, "fig_missing_context_burden")


def plot_activity_evidence_heatmap(activity_evidence_rows):
    matrix = np.zeros((len(ACTIVITY_ORDER), len(EVIDENCE_ORDER)), dtype=int)
    lookup = {(r["activity_category"], r["evidence_level"]): int(r["count"]) for r in activity_evidence_rows}
    for i, activity in enumerate(ACTIVITY_ORDER):
        for j, evidence in enumerate(EVIDENCE_ORDER):
            matrix[i, j] = lookup.get((activity, evidence), 0)
    fig, ax = plt.subplots(figsize=(7.1, 4.0), constrained_layout=True)
    im = ax.imshow(matrix, cmap="YlGnBu", aspect="auto")
    ax.set_xticks(np.arange(len(EVIDENCE_ORDER)))
    ax.set_xticklabels([label.replace("_", "\n") for label in EVIDENCE_ORDER], rotation=0, fontsize=7.2)
    ax.set_yticks(np.arange(len(ACTIVITY_ORDER)))
    ax.set_yticklabels(ACTIVITY_ORDER)
    ax.set_title("Activity categories stratified by evidence level")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            val = matrix[i, j]
            if val:
                ax.text(j, i, str(val), ha="center", va="center", fontsize=7, color="#1F2933")
    cbar = fig.colorbar(im, ax=ax, shrink=0.78)
    cbar.set_label("Record count")
    ax.grid(False)
    save_fig(fig, "fig_activity_evidence_heatmap")


def plot_uncertainty_stacked(records):
    classes = ["low_uncertainty", "moderate_uncertainty", "high_uncertainty"]
    colors = [COLORS["green"], COLORS["gold"], COLORS["coral"]]
    counts = Counter((r.get("activity_category", ""), r.get("uncertainty_class", "")) for r in records)
    totals = {activity: sum(counts[(activity, c)] for c in classes) for activity in ACTIVITY_ORDER}
    y = np.arange(len(ACTIVITY_ORDER))
    left = np.zeros(len(ACTIVITY_ORDER))
    fig, ax = plt.subplots(figsize=(6.4, 3.6), constrained_layout=True)
    for cls, color in zip(classes, colors):
        vals = np.array([counts[(activity, cls)] / totals[activity] if totals[activity] else 0 for activity in ACTIVITY_ORDER])
        ax.barh(y, vals, left=left, label=cls.replace("_", " "), color=color, edgecolor="white", linewidth=0.5)
        left += vals
    ax.set_yticks(y)
    ax.set_yticklabels(ACTIVITY_ORDER)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel("Share within activity")
    ax.set_title("Uncertainty composition by activity")
    ax.legend(ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.28))
    ax.xaxis.set_major_formatter(lambda x, pos: f"{int(x * 100)}%")
    save_fig(fig, "fig_uncertainty_by_activity")


def top_counter_from_records(records, field, n=12):
    counter = Counter()
    for row in records:
        for value in split_values(row.get(field, "")):
            counter[value] += 1
    return counter.most_common(n)


def plot_processing_extraction(records):
    proc = top_counter_from_records(records, "silver_processing_step", 10)
    ext = top_counter_from_records(records, "silver_extraction_method", 10)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6), constrained_layout=True)
    for ax, data, title, color in [
        (axes[0], proc, "Processing labels", COLORS["teal"]),
        (axes[1], ext, "Extraction labels", COLORS["blue"]),
    ]:
        labels = [x[0] for x in data][::-1]
        values = [x[1] for x in data][::-1]
        ax.barh(labels, values, color=color, edgecolor="white", linewidth=0.5)
        ax.set_title(title)
        ax.set_xlabel("Record count")
        for i, val in enumerate(values):
            ax.text(val + 1, i, str(val), va="center", fontsize=7.5)
        ax.set_xlim(0, max(values) * 1.24 if values else 1)
    save_fig(fig, "fig_processing_extraction_labels")


def plot_kg_composition(nodes, edges):
    node_counts = Counter(n["node_type"] for n in nodes).most_common(10)
    edge_counts = Counter(e["edge_type"] for e in edges).most_common(10)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6), constrained_layout=True)
    for ax, data, title, color in [
        (axes[0], node_counts, "Top node types", COLORS["deep"]),
        (axes[1], edge_counts, "Top edge types", COLORS["sand"]),
    ]:
        labels = [x[0] for x in data][::-1]
        vals = [x[1] for x in data][::-1]
        ax.barh(labels, vals, color=color, edgecolor="white", linewidth=0.5)
        ax.set_title(title)
        ax.set_xlabel("Count")
        for i, val in enumerate(vals):
            ax.text(val + max(vals) * 0.01, i, str(val), va="center", fontsize=7.3)
    save_fig(fig, "fig_kg_composition")


def plot_open_fulltext_funnel():
    # From fulltext_methods_processing_result_analysis_2026-04-12.md.
    labels = ["Remaining records", "PMC methods available", "No PMC full text", "Methods patches"]
    vals = [329, 151, 178, 151]
    colors = [COLORS["deep"], COLORS["teal"], COLORS["gray"], COLORS["coral"]]
    fig, ax = plt.subplots(figsize=(5.8, 3.0), constrained_layout=True)
    bars = ax.bar(labels, vals, color=colors, edgecolor="white", linewidth=0.6)
    ax.set_ylabel("Record count")
    ax.set_title("Full-text availability limits methods-level recovery")
    ax.tick_params(axis="x", rotation=18)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 4, str(val), ha="center", va="bottom", fontsize=8)
    ax.set_ylim(0, max(vals) * 1.18)
    save_fig(fig, "fig_fulltext_methods_funnel")


def write_summary_metrics(records, nodes, edges, stage_rows):
    row = {
        "silver_records": len(records),
        "kg_nodes": len(nodes),
        "kg_edges": len(edges),
        "processing_present_final": count_present(records, "silver_processing_step"),
        "extraction_present_final": count_present(records, "silver_extraction_method"),
        "microbiome_records": sum(
            1
            for r in records
            if r.get("activity_category") == "gut microbiota modulation"
            or present(r.get("microbiota_taxon"))
            or present(r.get("microbial_metabolite"))
        ),
        "low_uncertainty": sum(1 for r in records if r.get("uncertainty_class") == "low_uncertainty"),
        "moderate_uncertainty": sum(1 for r in records if r.get("uncertainty_class") == "moderate_uncertainty"),
        "high_uncertainty": sum(1 for r in records if r.get("uncertainty_class") == "high_uncertainty"),
        "missing_context_after_methods": stage_rows[-1]["missing_context_flag"],
    }
    write_csv(OUT_TABLE_DIR / "figure_ready_summary_metrics.csv", list(row.keys()), [row])


def main():
    setup_style()
    OUT_TABLE_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FIG_DIR.mkdir(parents=True, exist_ok=True)

    records = read_csv(RECORDS_CSV)
    nodes = read_csv(NODES_CSV)
    edges = read_csv(EDGES_CSV)

    activity_evidence = table_activity_evidence(records)
    activity_study = table_activity_study(records)
    processing_activity = table_context_by_activity(records, "silver_processing_step", "processing_step")
    extraction_activity = table_context_by_activity(records, "silver_extraction_method", "extraction_method")
    uncertainty_activity = table_uncertainty_by_activity(records)
    microbiome = table_microbiome(records)
    kg_counts = table_kg_counts(nodes, edges)
    stage_metrics = compute_stage_metrics(records)

    write_csv(OUT_TABLE_DIR / "table_activity_evidence_counts.csv", list(activity_evidence[0].keys()), activity_evidence)
    write_csv(OUT_TABLE_DIR / "table_activity_study_counts.csv", list(activity_study[0].keys()), activity_study)
    write_csv(OUT_TABLE_DIR / "table_processing_activity_records.csv", list(processing_activity[0].keys()), processing_activity)
    write_csv(OUT_TABLE_DIR / "table_extraction_activity_records.csv", list(extraction_activity[0].keys()), extraction_activity)
    write_csv(OUT_TABLE_DIR / "table_uncertainty_by_activity.csv", list(uncertainty_activity[0].keys()), uncertainty_activity)
    write_csv(OUT_TABLE_DIR / "table_microbiome_mechanism_records.csv", list(microbiome[0].keys()), microbiome)
    write_csv(OUT_TABLE_DIR / "table_kg_node_edge_counts.csv", list(kg_counts[0].keys()), kg_counts)
    write_csv(OUT_TABLE_DIR / "table_context_coverage_by_stage.csv", list(stage_metrics[0].keys()), stage_metrics)
    write_summary_metrics(records, nodes, edges, stage_metrics)

    plot_context_coverage(stage_metrics)
    plot_remaining_missing(stage_metrics)
    plot_activity_evidence_heatmap(activity_evidence)
    plot_uncertainty_stacked(records)
    plot_processing_extraction(records)
    plot_kg_composition(nodes, edges)
    plot_open_fulltext_funnel()

    figure_manifest = [
        {
            "figure": "fig_context_coverage",
            "purpose": "Grouped bar chart showing processing/extraction context recovery across auto rules, abstract LLM, and methods LLM.",
        },
        {
            "figure": "fig_missing_context_burden",
            "purpose": "Bar chart showing residual missing processing/extraction context after each extraction stage.",
        },
        {
            "figure": "fig_activity_evidence_heatmap",
            "purpose": "Heatmap of activity categories by evidence level.",
        },
        {
            "figure": "fig_uncertainty_by_activity",
            "purpose": "Stacked horizontal bar chart showing uncertainty class composition per activity.",
        },
        {
            "figure": "fig_processing_extraction_labels",
            "purpose": "Two-panel horizontal bar chart of normalized processing and extraction labels.",
        },
        {
            "figure": "fig_kg_composition",
            "purpose": "Two-panel horizontal bar chart of KG node and edge type counts.",
        },
        {
            "figure": "fig_fulltext_methods_funnel",
            "purpose": "Bar chart showing PMC full-text availability and methods extraction coverage.",
        },
    ]
    write_csv(OUT_TABLE_DIR / "figure_manifest.csv", list(figure_manifest[0].keys()), figure_manifest)
    print(f"Wrote query tables to {OUT_TABLE_DIR}")
    print(f"Wrote figures to {OUT_FIG_DIR}")


if __name__ == "__main__":
    main()
