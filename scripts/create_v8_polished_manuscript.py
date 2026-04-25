"""Create v8 manuscript with polished figures, tables, and section edits.

The script keeps v7 intact and writes a reproducible v8 draft plus figure/table
artifacts under the existing manuscript output directory.
"""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "writing_outputs" / "20260412_autoteakg_silver_paper"
DRAFT_DIR = PAPER_DIR / "drafts"
FIG_DIR = PAPER_DIR / "figures"
DATA_DIR = PAPER_DIR / "data"
SNIPPET_DIR = DRAFT_DIR / "v8_snippets"
FINAL_DIR = PAPER_DIR / "final"

KG_DIR = ROOT / "reports" / "methods_processing_vocab_normalized"
RECORDS_CSV = KG_DIR / "autoteakg_silver_records.csv"
NODES_CSV = KG_DIR / "kg_v3" / "nodes.csv"
EDGES_CSV = KG_DIR / "kg_v3" / "edges.csv"
STAGE_QC = DATA_DIR / "stagewise_qc_v4.csv"
VALIDATION_JSON = DATA_DIR / "validation_v4" / "validation_results_v4.json"
CASE_CSV = DATA_DIR / "graph_query_case_study_polysaccharide_microbiome_v4.csv"

V7 = DRAFT_DIR / "v7_database_draft.tex"
V8 = DRAFT_DIR / "v8_database_draft.tex"


PALETTE = {
    "ink": "#24343D",
    "teal": "#2A9D8F",
    "blue": "#0072B2",
    "sky": "#56B4E9",
    "gold": "#E9C46A",
    "coral": "#E76F51",
    "green": "#009E73",
    "gray": "#B7C0C7",
    "light": "#F4F7F6",
    "line": "#D8DEE3",
}

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

EVIDENCE_SHORT = {
    "preclinical_in_vivo": "Preclin.\nin vivo",
    "evidence_synthesis_nonquantitative": "Synth.\nnonquant.",
    "human_observational": "Human\nobs.",
    "human_interventional": "Human\nint.",
    "evidence_synthesis": "Evidence\nsynth.",
    "low_preclinical": "Low\npreclin.",
    "in_vitro": "In vitro",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_figure(fig: plt.Figure, basename: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    for suffix in [".pdf", ".png", ".svg"]:
        target = FIG_DIR / f"{basename}{suffix}"
        kwargs = {"bbox_inches": "tight"}
        if suffix == ".png":
            kwargs["dpi"] = 300
        fig.savefig(target, **kwargs)
    plt.close(fig)


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif"],
            "font.size": 9.5,
            "axes.titlesize": 10.5,
            "axes.titleweight": "bold",
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "legend.frameon": False,
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.16,
            "grid.color": PALETTE["line"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def present(value: str | None) -> bool:
    return bool((value or "").strip())


def plot_evidence_quality_dashboard() -> None:
    records = read_csv(RECORDS_CSV)
    stages = read_csv(STAGE_QC)
    validation = json.loads(VALIDATION_JSON.read_text(encoding="utf-8"))

    fig = plt.figure(figsize=(7.8, 6.5), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, height_ratios=[0.95, 1.05])

    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])

    stats = [
        ("Records", len(records), PALETTE["ink"]),
        ("Nodes", sum(1 for _ in read_csv(NODES_CSV)), PALETTE["teal"]),
        ("Edges", sum(1 for _ in read_csv(EDGES_CSV)), PALETTE["coral"]),
        ("Microbiome", sum(1 for r in records if r.get("activity_category") == "gut microbiota modulation" or present(r.get("microbiota_taxon")) or present(r.get("microbial_metabolite"))), PALETTE["blue"]),
    ]
    x = np.arange(len(stats))
    bars = ax0.bar(x, [s[1] for s in stats], color=[s[2] for s in stats], edgecolor="white", linewidth=0.6)
    ax0.set_yscale("log")
    ax0.set_xticks(x)
    ax0.set_xticklabels([s[0] for s in stats], fontsize=8.4)
    ax0.set_ylabel("Count, log scale")
    ax0.set_title("A. Resource scale")
    for bar, (_, val, _) in zip(bars, stats):
        ax0.text(bar.get_x() + bar.get_width() / 2, val * 1.08, f"{val:,}", ha="center", va="bottom", fontsize=8)

    stage_labels = ["Rules", "Abstract\nLLM", "Methods\nLLM"]
    processing = [int(s["processing_present"]) for s in stages]
    extraction = [int(s["extraction_present"]) for s in stages]
    missing = [int(s["missing_context_flags"]) for s in stages]
    idx = np.arange(len(stage_labels))
    width = 0.26
    ax1.bar(idx - width, processing, width, label="Processing", color=PALETTE["teal"], edgecolor="white", linewidth=0.5)
    ax1.bar(idx, extraction, width, label="Extraction", color=PALETTE["blue"], edgecolor="white", linewidth=0.5)
    ax1.bar(idx + width, missing, width, label="Missing flag", color=PALETTE["gray"], edgecolor="white", linewidth=0.5)
    ax1.set_xticks(idx)
    ax1.set_xticklabels(stage_labels)
    ax1.set_ylabel("Record count")
    ax1.set_title("B. Context recovery and residual gaps")
    ax1.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.12))

    counts = Counter((r.get("activity_category", ""), r.get("evidence_level", "")) for r in records)
    matrix = np.array([[counts[(a, e)] for e in EVIDENCE_ORDER] for a in ACTIVITY_ORDER])
    im = ax2.imshow(matrix, aspect="auto", cmap="YlGnBu")
    ax2.set_title("C. Activity by evidence level")
    ax2.set_xticks(np.arange(len(EVIDENCE_ORDER)))
    ax2.set_xticklabels([EVIDENCE_SHORT[e] for e in EVIDENCE_ORDER], fontsize=6.2)
    ax2.set_yticks(np.arange(len(ACTIVITY_ORDER)))
    ax2.set_yticklabels(ACTIVITY_ORDER, fontsize=7.3)
    ax2.grid(False)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] >= 10:
                ax2.text(j, i, str(matrix[i, j]), ha="center", va="center", fontsize=6.5, color="#1F2933")
    cbar = fig.colorbar(im, ax=ax2, shrink=0.82)
    cbar.set_label("Records")

    field_rows = validation["field_rows"]
    fields = [r["field"] for r in field_rows]
    acceptable = [float(r["acceptable_rate_on_completed"]) * 100 for r in field_rows]
    major = [int(r["major_issue"]) for r in field_rows]
    y = np.arange(len(fields))
    colors = [PALETTE["green"] if v >= 90 else PALETTE["gold"] if v >= 85 else PALETTE["coral"] for v in acceptable]
    ax3.barh(y, acceptable, color=colors, edgecolor="white", linewidth=0.5)
    ax3.set_yticks(y)
    ax3.set_yticklabels(fields, fontsize=7.5)
    ax3.set_xlim(0, 105)
    ax3.set_xlabel("Acceptable judgments (%)")
    ax3.set_title("D. External validation by field")
    ax3.axvline(90, color="#4B5563", linewidth=0.9, linestyle="--", alpha=0.7)
    ax3.invert_yaxis()
    for yi, val, maj in zip(y, acceptable, major):
        ax3.text(val + 1.2, yi, f"{val:.0f}% / M{maj}", va="center", fontsize=7)

    fig.suptitle("AutoTeaKG-Silver evidence-quality dashboard", fontsize=12.5, fontweight="bold")
    save_figure(fig, "fig_evidence_quality_dashboard_v8")


def plot_graph_utility_case() -> None:
    rows = read_csv(CASE_CSV)
    fig, ax = plt.subplots(figsize=(7.4, 3.9), constrained_layout=True)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def box(x: float, y: float, w: float, h: float, title: str, body: str, color: str) -> None:
        patch = plt.Rectangle((x, y), w, h, facecolor=color, edgecolor="#263238", linewidth=0.9)
        ax.add_patch(patch)
        ax.text(x + 0.02, y + h - 0.045, title, fontsize=8.4, fontweight="bold", va="top")
        ax.text(x + 0.02, y + h - 0.105, body, fontsize=6.7, va="top", linespacing=1.1)

    def value_box(x: float, y: float, w: float, h: float, value: str, color: str = "#F7FAFC") -> None:
        patch = plt.Rectangle((x, y), w, h, facecolor=color, edgecolor="#263238", linewidth=0.8)
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, value, fontsize=7.2, va="center", ha="center", linespacing=1.1)

    def arrow(start: tuple[float, float], end: tuple[float, float], label: str) -> None:
        ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "-|>", "lw": 1.2, "color": "#455A64"})
        ax.text((start[0] + end[0]) / 2, (start[1] + end[1]) / 2 + 0.035, label, ha="center", fontsize=7.3, color="#37474F")

    box(0.04, 0.67, 0.23, 0.20, "Query constraints", "component = tea polysaccharides\nmicrobiome/metabolite present\nhost phenotype present", "#E8EDF2")
    box(0.37, 0.67, 0.22, 0.20, "EvidenceRecord layer", "record id; paper id\nevidence level\nuncertainty class", "#E8F2EE")
    box(0.70, 0.67, 0.24, 0.20, "Returned subgraph", "exposure -> microbiota\nmicrobiota -> metabolite\nmetabolite -> phenotype", "#FFF4DE")
    arrow((0.27, 0.78), (0.37, 0.78), "filters")
    arrow((0.59, 0.78), (0.70, 0.78), "projects")

    ax.text(0.16, 0.57, "Exposure", fontsize=8.4, fontweight="bold", ha="center")
    ax.text(0.47, 0.57, "Metabolite", fontsize=8.4, fontweight="bold", ha="center")
    ax.text(0.76, 0.57, "Phenotype", fontsize=8.4, fontweight="bold", ha="center")
    ax.text(0.94, 0.57, "Evidence", fontsize=8.4, fontweight="bold", ha="center")

    y0 = 0.44
    path_rows = rows[:3]
    path_text = [
        ("Black tea polysaccharides", "butyric acid", "reduced liver inflammation", "preclinical, low"),
        ("Tea polysaccharides", "SCFAs", "reduced hepatic lipid deposition", "preclinical, moderate"),
        ("Yellow tea polysaccharides", "SCFAs", "intestinal barrier integrity", "preclinical, low"),
    ]
    for i, (exposure, metabolite, phenotype, badge) in enumerate(path_text):
        y = y0 - i * 0.14
        value_box(0.05, y, 0.23, 0.07, exposure)
        value_box(0.37, y, 0.16, 0.07, metabolite)
        value_box(0.64, y, 0.21, 0.07, phenotype)
        arrow((0.28, y + 0.035), (0.37, y + 0.035), "links")
        arrow((0.53, y + 0.035), (0.64, y + 0.035), "links")
        ax.text(0.925, y + 0.035, badge, fontsize=6.5, va="center", ha="center", color="#263238")

    ax.text(0.5, 0.95, "Graph utility case: multi-field query with provenance retained", ha="center", fontsize=12, fontweight="bold")
    ax.text(0.5, 0.045, f"Representative records shown: {len(path_rows)} of {len(rows)} retrieved case rows; evidence level and uncertainty remain attached to each path.", ha="center", fontsize=8, color="#37474F")
    save_figure(fig, "fig_graph_utility_case_v8")


def write_claim_evidence_table() -> None:
    rows = [
        {
            "claim": "The resource is a graph rather than a flat bibliography.",
            "evidence": "635 evidence records, 1,989 nodes, and 8,195 edges with explicit EvidenceRecord provenance.",
            "anchor": "Table~\\ref{tab:dataset_stats}; Figure~\\ref{fig:quality_dashboard}",
        },
        {
            "claim": "Evidence support differs across activity classes.",
            "evidence": "Activity-by-evidence heatmap separates preclinical, synthesis, observational, and interventional support.",
            "anchor": "Figure~\\ref{fig:activity_evidence}; Figure~\\ref{fig:quality_dashboard}",
        },
        {
            "claim": "Processing and extraction context remain a reporting bottleneck.",
            "evidence": "Context recovery improves across extraction stages, but 303 records retain missing-context flags.",
            "anchor": "Table~\\ref{tab:stagewise_qc}; Figure~\\ref{fig:quality_dashboard}",
        },
        {
            "claim": "The graph supports constrained mechanism queries.",
            "evidence": "A tea-polysaccharide query returns microbiome, metabolite, phenotype, evidence, and uncertainty-linked paths.",
            "anchor": "Table~\\ref{tab:graph_query_case}; Figure~\\ref{fig:graph_utility_case}",
        },
        {
            "claim": "Human validation supports silver-standard use while identifying weak fields.",
            "evidence": "Acceptable rates range from 80\\% for study type to 100\\% for processing and extraction fields.",
            "anchor": "Table~\\ref{tab:validation_results}; Figure~\\ref{fig:quality_dashboard}",
        },
    ]
    write_csv(DATA_DIR / "table_claim_evidence_map_v8.csv", ["claim", "evidence", "anchor"], rows)

    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\caption{Claim--evidence map for the main manuscript. Each central claim is tied to at least one table or figure anchor.}",
        "\\label{tab:claim_evidence_map}",
        "\\begin{tabularx}{\\linewidth}{p{0.28\\linewidth}Xp{0.22\\linewidth}}",
        "\\toprule",
        "Claim & Supporting evidence & Anchor \\\\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(f"{row['claim']} & {row['evidence']} & {row['anchor']} \\\\")
    lines.extend(["\\bottomrule", "\\end{tabularx}", "\\end{table}", ""])
    SNIPPET_DIR.mkdir(parents=True, exist_ok=True)
    (SNIPPET_DIR / "claim_evidence_map_table.tex").write_text("\n".join(lines), encoding="utf-8")


def write_validation_compact_table() -> None:
    validation = json.loads(VALIDATION_JSON.read_text(encoding="utf-8"))
    rows = []
    for row in validation["field_rows"]:
        rows.append(
            {
                "field": row["field"],
                "completed": row["completed"],
                "acceptable": f"{round(row['acceptable_rate_on_completed'] * 100):.0f}\\%",
                "major": row["major_issue"],
            }
        )
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\caption{External validation results on the 47 completed records. Acceptable = correct or minor issue among completed judgments.}",
        "\\label{tab:validation_results}",
        "\\begin{tabular}{lrrr}",
        "\\toprule",
        "Field & Completed & Acceptable & Major issues \\\\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(f"{row['field']} & {row['completed']} & {row['acceptable']} & {row['major']} \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}", ""])
    SNIPPET_DIR.mkdir(parents=True, exist_ok=True)
    (SNIPPET_DIR / "validation_results_compact_table.tex").write_text("\n".join(lines), encoding="utf-8")


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise RuntimeError(f"Expected text not found: {old[:80]!r}")
    return text.replace(old, new, 1)


def build_v8_tex() -> None:
    text = V7.read_text(encoding="utf-8")
    text = text.replace("AutoTeaKG-Silver: An Uncertainty-Aware Evidence Graph for Tea Functional Activity Literature", "AutoTeaKG-Silver: A Validated Silver-Standard Evidence Graph for Tea Functional Activity Literature")

    old_abs = text[text.index("\\begin{abstract}") : text.index("\\end{abstract}") + len("\\end{abstract}")]
    new_abs = """\\begin{abstract}
Tea functional-activity literature is difficult to synthesize because tea type, component identity, processing state, extraction method, study design, endpoint label, and mechanism evidence are often reported in incompatible forms. AutoTeaKG-Silver addresses this gap by converting PubMed tea bioactivity records into a provenance-rich, uncertainty-aware evidence graph. The pipeline retrieves PubMed records, extracts structured title/abstract and open full-text methods evidence, normalizes activity and evidence labels, recovers processing and extraction context, and exports graph edges through explicit evidence-record nodes. In the current KG v3 release, AutoTeaKG-Silver contains 635 evidence records, 1,989 nodes, and 8,195 edges. Targeted extraction increased processing-context coverage from 146 to 183 records and extraction-context coverage from 154 to 185 records, while retaining missing-context flags for 303 records. External validation of 47 completed stratified records showed acceptable rates of 92\\% for activity category, 80\\% for study type, 86\\% for evidence level, 94\\% for component group, 100\\% for processing step, 100\\% for extraction method, and 94\\% for mechanism label. The resource exposes uneven evidence support across activity classes and enables constrained microbiome-mechanism queries that preserve evidence level and uncertainty. AutoTeaKG-Silver is therefore intended as a reproducible silver-standard infrastructure for living tea bioactivity synthesis, not as a manually verified gold-standard database.
\\end{abstract}"""
    text = text.replace(old_abs, new_abs)

    old_intro_last = """The contributions are fourfold. First, we define a graph-ready evidence model for tea functional activity literature that separates activity claims from study design, evidence level, component context, processing context, and uncertainty. Second, we build an automated silver-standard resource with 635 evidence records and 8,195 graph edges, excluding manual annotation as a data-generation dependency. Third, we show that processing and extraction context remain a measurable bottleneck: targeted extraction improves coverage, but many records lack open full-text or report insufficient methods detail. Fourth, we provide figure-ready query tables and graph outputs that support evidence mapping, processing-aware analysis, and microbiome mechanism exploration."""
    new_intro_last = """The contributions are fourfold and each is tied to a result-level evidence anchor (Table~\\ref{tab:claim_evidence_map}). First, we define a graph-ready evidence model that separates activity claims from study design, evidence level, component context, processing context, and uncertainty. Second, we build an automated silver-standard resource with 635 evidence records and 8,195 graph edges, excluding manual annotation from the data-generation path. Third, we show that processing and extraction context remain a measurable reporting bottleneck: targeted extraction improves coverage, but many records lack open full text or sufficient methods detail. Fourth, we provide query tables and graph outputs that support evidence mapping, processing-aware analysis, and microbiome mechanism exploration under explicit uncertainty filters."""
    text = replace_once(text, old_intro_last, new_intro_last)

    text = replace_once(text, "\\subsection{Prior work and resource gap}", "\\input{v8_snippets/claim_evidence_map_table.tex}\n\n\\subsection{Prior work and resource gap}")

    old_unc = """Each record was assigned uncertainty flags and an uncertainty class. Flags captured low LLM confidence, missing processing or extraction context, generic mechanism labels, missing named microbiota, taxonomy expansion needs, preclinical-only evidence, review-summary records, uncertain effect direction, and schema validation problems. The uncertainty class summarized these signals into low, moderate, or high uncertainty. This design keeps uncertainty in the graph rather than hiding it during filtering.

\\paragraph{Uncertainty model.}
AutoTeaKG-Silver assigns uncertainty at the evidence-record level and propagates the same uncertainty attributes to graph edges through the evidence-record node. The silver confidence score combines the original extraction confidence with record specificity and context completeness. Context completeness assigns partial credit for non-generic tea type, component group, processing step, and extraction method. Mechanism specificity distinguishes missing or generic mechanisms from pathway-like or named mechanism labels. Records are then assigned uncertainty flags (Appendix Table~\\ref{tab:uncertainty_flags}) and mapped to low, moderate, or high uncertainty classes using the rules in Table~\\ref{tab:uncertainty_classes}."""
    new_unc = """AutoTeaKG-Silver assigns uncertainty at the evidence-record level and propagates the same attributes to graph edges through the evidence-record node. The silver confidence score combines the original extraction confidence with record specificity and context completeness. Context completeness assigns partial credit for non-generic tea type, component group, processing step, and extraction method, while mechanism specificity distinguishes missing or generic mechanisms from pathway-like or named mechanism labels. Records are then assigned uncertainty flags (Appendix Table~\\ref{tab:uncertainty_flags}) and mapped to low, moderate, or high uncertainty classes using the rules in Table~\\ref{tab:uncertainty_classes}. This design keeps uncertainty queryable rather than hiding it during filtering."""
    text = replace_once(text, old_unc, new_unc)

    dashboard_block = """\\begin{figure}[t]
  \\centering
  \\includegraphics[width=\\linewidth]{fig_evidence_quality_dashboard_v8.pdf}
  \\caption{Evidence-quality dashboard for AutoTeaKG-Silver. The figure summarizes resource scale, context recovery, activity-by-evidence structure, and external validation rates in one reproducible anchor figure.}
  \\label{fig:quality_dashboard}
\\end{figure}

"""
    text = replace_once(text, "\\subsection{AutoTeaKG-Silver constructs a provenance-rich tea functional activity graph}\n\n", "\\subsection{AutoTeaKG-Silver constructs a provenance-rich tea functional activity graph}\n\n" + dashboard_block)

    old_results_first = """The final KG v3 contains 635 silver evidence records, 1,989 nodes, and 8,195 edges (Figure~\\ref{fig:kg_composition}). The graph includes paper nodes, evidence-record nodes, activity-category nodes, study-type nodes, evidence-level nodes, tea and component context nodes, processing and extraction context nodes, mechanism nodes, microbiota-feature nodes, microbial-metabolite nodes, host-phenotype nodes, and uncertainty-flag nodes. The explicit EvidenceRecord layer is important because it prevents mechanistic and activity relations from becoming detached from their source papers."""
    new_results_first = """The final KG v3 contains 635 silver evidence records, 1,989 nodes, and 8,195 edges (Table~\\ref{tab:dataset_stats}; Figure~\\ref{fig:quality_dashboard}). The graph includes paper, evidence-record, activity-category, study-type, evidence-level, tea/context, mechanism, microbiota, metabolite, phenotype, and uncertainty nodes. The explicit EvidenceRecord layer is the central design choice: it prevents mechanistic and activity relations from becoming detached from source papers, raw claims, evidence levels, and uncertainty classes."""
    text = replace_once(text, old_results_first, new_results_first)

    old_query = """To test whether the KG supports structured queries beyond flat keyword retrieval, we queried records with tea-polysaccharide component context and microbiome/metabolite/host-phenotype fields. The query recovered five representative records linking tea polysaccharides to gut microbiota modulation, butyric acid or SCFA-related metabolites, and liver, barrier, or lipid-deposition phenotypes (Table~\\ref{tab:graph_query_case}; Figure~\\ref{fig:graph_query_case}). The retrieved paths preserve evidence level and uncertainty class, allowing the user to distinguish low-uncertainty preclinical gut-liver-axis records from broader moderate-uncertainty microbiome records. This query illustrates the practical advantage of the graph representation: component, microbiome, metabolite, phenotype, evidence, and uncertainty constraints can be applied together rather than searched as independent keywords."""
    new_query = """To test whether the KG supports structured queries beyond flat keyword retrieval, we queried records with tea-polysaccharide component context and microbiome, metabolite, or host-phenotype fields. The query recovered five representative records linking tea polysaccharides to gut microbiota modulation, butyric acid or SCFA-related metabolites, and liver, barrier, or lipid-deposition phenotypes (Table~\\ref{tab:graph_query_case}; Figures~\\ref{fig:graph_utility_case} and~\\ref{fig:graph_query_case}). The retrieved paths preserve evidence level and uncertainty class, allowing users to separate low-uncertainty preclinical gut-liver-axis records from broader moderate-uncertainty microbiome records. This case is the strongest utility test in the manuscript because the answer requires simultaneous constraints on component, mechanism, metabolite, phenotype, evidence, and uncertainty fields."""
    text = replace_once(text, old_query, new_query)

    utility_fig = """\\begin{figure}[t]
  \\centering
  \\includegraphics[width=\\linewidth]{fig_graph_utility_case_v8.pdf}
  \\caption{Graph utility case. The same query simultaneously filters component context, microbiome/metabolite evidence, host phenotype, evidence level, and uncertainty, then returns provenance-retaining evidence paths.}
  \\label{fig:graph_utility_case}
\\end{figure}

"""
    text = replace_once(text, "\\begin{table}[t]\n\\centering\n\\small\n\\caption{Graph query case study", utility_fig + "\\begin{table}[t]\n\\centering\n\\small\n\\caption{Graph query case study")

    old_val = """The completed 47-record validation sample provides an external check on the silver-standard graph (Table~\\ref{tab:validation_results}). The strongest fields were those most directly tied to the new context-recovery pipeline: processing step and extraction method were correct in all completed judgments, while component group and mechanism label achieved acceptable rates of 94\\% or above. Activity category also remained strong with a 92\\% acceptable rate. Study type and evidence level were the main residual error sources, with acceptable rates of 80\\% and 86\\%, respectively. Major issue tags were concentrated in out-of-scope records, wrong activity labels, and wrong study-type assignments. These results support the use of AutoTeaKG-Silver as a silver-standard evidence graph while highlighting which fields should be prioritized in future correction and retraining cycles.

\\input{v4_snippets/validation_results_table.tex}"""
    new_val = """The completed 47-record validation sample provides an external check on the silver-standard graph (Table~\\ref{tab:validation_results}; Figure~\\ref{fig:quality_dashboard}). The strongest fields were those most directly tied to context recovery: processing step and extraction method were correct in all completed judgments, while component group and mechanism label achieved acceptable rates of 94\\% or above. Activity category also remained strong with a 92\\% acceptable rate. Study type and evidence level were the main residual error sources, with acceptable rates of 80\\% and 86\\%, respectively. Major issue tags were concentrated in out-of-scope records, wrong activity labels, and wrong study-type assignments. These results support silver-standard use while identifying the fields that should be prioritized in future correction cycles.

\\input{v8_snippets/validation_results_compact_table.tex}"""
    text = replace_once(text, old_val, new_val)

    old_disc = """The uncertainty layer is a practical compromise between scale and reliability. A manually curated gold-standard resource would be smaller and slower to update. A raw LLM graph would be larger but difficult to trust. AutoTeaKG-Silver occupies the middle ground: it keeps all records provenance-rich, marks uncertainty explicitly, and provides query tables and figures that can be regenerated from the graph."""
    new_disc = """The uncertainty layer is a practical compromise between scale and reliability. A manually curated gold-standard resource would be smaller and slower to update, whereas a raw LLM graph would be larger but difficult to audit. AutoTeaKG-Silver occupies the middle ground: records remain provenance-rich, uncertainty is explicit, validation results identify weak fields, and query tables and figures can be regenerated from the graph."""
    text = replace_once(text, old_disc, new_disc)

    old_lim = """This work has four important limitations. First, AutoTeaKG-Silver is a silver-standard resource, not a manually verified gold-standard database. The graph should be used with uncertainty filters when precise biological conclusions are required. Second, the current system relies on PubMed abstracts and open PMC full text; records without PMC full text remain difficult to refine. Third, processing and extraction labels are normalized by rules after LLM extraction, but some labels still represent broad process categories rather than complete experimental protocols. Fourth, the microbiome subgraph includes grouped taxa and generic mechanism labels, so causal interpretation requires additional normalization and full-text validation."""
    new_lim = """This work has four important limitations. First, AutoTeaKG-Silver is a silver-standard resource, not a manually verified gold-standard database; users should apply uncertainty filters when drawing precise biological conclusions. Second, the current system relies on PubMed abstracts and open PMC full text, so records without accessible methods sections remain difficult to refine. Third, processing and extraction labels are normalized after LLM extraction, but some labels still represent broad process categories rather than complete experimental protocols. Fourth, the microbiome subgraph includes grouped taxa and generic mechanism labels, so causal interpretation requires additional taxonomy normalization, full-text validation, and domain review."""
    text = replace_once(text, old_lim, new_lim)

    old_conc = """AutoTeaKG-Silver demonstrates that tea functional activity literature can be converted into an automated, provenance-rich, uncertainty-aware evidence graph. The current KG v3 release contains 635 evidence records, 1,989 nodes, and 8,195 edges, and provides figure-ready query tables for evidence mapping, processing-aware analysis, uncertainty assessment, and microbiome mechanism exploration. The results support a practical conclusion: automated evidence graphs can accelerate tea bioactivity synthesis, provided that uncertainty, provenance, and missing context are treated as first-class data rather than hidden errors."""
    new_conc = """AutoTeaKG-Silver demonstrates that tea functional activity literature can be converted into an automated, provenance-rich, uncertainty-aware evidence graph. The current KG v3 release contains 635 evidence records, 1,989 nodes, and 8,195 edges, and provides figure-ready query tables for evidence mapping, processing-aware analysis, uncertainty assessment, validation tracking, and microbiome mechanism exploration. The practical conclusion is deliberately bounded: automated evidence graphs can accelerate tea bioactivity synthesis when uncertainty, provenance, validation status, and missing context are treated as first-class data rather than hidden errors."""
    text = replace_once(text, old_conc, new_conc)

    text = text.replace("\\input{v4_snippets/validation_results_table.tex}", "\\input{v8_snippets/validation_results_compact_table.tex}")

    V8.write_text(text, encoding="utf-8")


def compile_v8() -> None:
    for cmd in [
        ["pdflatex", "-interaction=nonstopmode", "v8_database_draft.tex"],
        ["bibtex", "v8_database_draft"],
        ["pdflatex", "-interaction=nonstopmode", "v8_database_draft.tex"],
        ["pdflatex", "-interaction=nonstopmode", "v8_database_draft.tex"],
    ]:
        subprocess.run(cmd, cwd=DRAFT_DIR, check=True)
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(V8, FINAL_DIR / "AutoTeaKG_Silver_v8_database.tex")
    shutil.copy2(DRAFT_DIR / "v8_database_draft.pdf", FINAL_DIR / "AutoTeaKG_Silver_v8_database.pdf")


def main() -> None:
    setup_style()
    SNIPPET_DIR.mkdir(parents=True, exist_ok=True)
    plot_evidence_quality_dashboard()
    plot_graph_utility_case()
    write_claim_evidence_table()
    write_validation_compact_table()
    build_v8_tex()
    compile_v8()
    print(f"Wrote {V8}")
    print(f"Wrote {FINAL_DIR / 'AutoTeaKG_Silver_v8_database.pdf'}")


if __name__ == "__main__":
    main()
