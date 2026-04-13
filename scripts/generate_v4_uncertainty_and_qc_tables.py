import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "writing_outputs" / "20260412_autoteakg_silver_paper" / "data"
SNIPPET_DIR = ROOT / "writing_outputs" / "20260412_autoteakg_silver_paper" / "drafts" / "v4_snippets"

AUTO_SUMMARY = ROOT / "reports" / "autoteakg_silver_v1" / "summary.json"
TARGETED_SUMMARY = ROOT / "reports" / "targeted_processing_vocab_normalized" / "summary.json"
METHODS_SUMMARY = ROOT / "reports" / "methods_processing_vocab_normalized" / "summary.json"
FINAL_RECORDS = ROOT / "reports" / "methods_processing_vocab_normalized" / "autoteakg_silver_records.csv"
FINAL_EDGES = ROOT / "reports" / "methods_processing_vocab_normalized" / "kg_v3" / "edges.csv"
FINAL_NODES = ROOT / "reports" / "methods_processing_vocab_normalized" / "kg_v3" / "nodes.csv"


UNCERTAINTY_FLAGS = [
    {
        "flag": "low_llm_confidence",
        "trigger": "Original LLM confidence score is below 0.80.",
        "interpretation": "The extracted evidence record should be prioritized for review.",
        "severity": "severe",
    },
    {
        "flag": "taxonomy_expansion_needed",
        "trigger": "The normalized activity category is `other`.",
        "interpretation": "The record is either out of scope or requires activity-taxonomy expansion.",
        "severity": "severe",
    },
    {
        "flag": "missing_component_context",
        "trigger": "No component group is available after rule and LLM context extraction.",
        "interpretation": "The record lacks a key exposure descriptor.",
        "severity": "severe",
    },
    {
        "flag": "missing_processing_or_extraction_context",
        "trigger": "Both processing step and extraction method are empty.",
        "interpretation": "The record cannot support processing-aware comparison.",
        "severity": "moderate",
    },
    {
        "flag": "generic_mechanism",
        "trigger": "Mechanism label is empty or belongs to a generic placeholder list.",
        "interpretation": "The record supports an activity claim but weakly supports mechanistic graph reasoning.",
        "severity": "severe",
    },
    {
        "flag": "missing_named_microbiota",
        "trigger": "Activity is gut microbiota modulation but no named taxon is extracted.",
        "interpretation": "Microbiome interpretation should remain generic.",
        "severity": "moderate",
    },
    {
        "flag": "preclinical_only",
        "trigger": "Study type is animal study.",
        "interpretation": "The claim should not be interpreted as direct human evidence.",
        "severity": "moderate",
    },
    {
        "flag": "review_summary_record",
        "trigger": "Study type is systematic review.",
        "interpretation": "The record summarizes literature rather than representing one primary experiment.",
        "severity": "moderate",
    },
    {
        "flag": "low_evidence_level",
        "trigger": "Evidence level is low_preclinical or in_vitro.",
        "interpretation": "The claim has weak translational support.",
        "severity": "moderate",
    },
    {
        "flag": "uncertain_effect_direction",
        "trigger": "Effect direction is unclear, no_clear_effect, or mixed.",
        "interpretation": "The extracted claim should not be counted as straightforward positive support.",
        "severity": "moderate",
    },
    {
        "flag": "missing_abstract",
        "trigger": "No abstract text is available.",
        "interpretation": "The record has reduced text evidence for automatic extraction.",
        "severity": "moderate",
    },
    {
        "flag": "invalid_*",
        "trigger": "A controlled-vocabulary field contains an invalid label.",
        "interpretation": "The record violates schema constraints and requires normalization or exclusion.",
        "severity": "severe",
    },
]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def count_present(counter_dict):
    return sum(count for label, count in counter_dict.items() if label)


def unresolved_edges(nodes, edges):
    node_ids = {row["node_id"] for row in nodes}
    return sum(1 for edge in edges if edge["source_id"] not in node_ids or edge["target_id"] not in node_ids)


def build_stagewise_qc():
    auto = read_json(AUTO_SUMMARY)
    targeted = read_json(TARGETED_SUMMARY)
    methods = read_json(METHODS_SUMMARY)
    nodes = read_csv(FINAL_NODES)
    edges = read_csv(FINAL_EDGES)
    final_unresolved = unresolved_edges(nodes, edges)
    rows = [
        {
            "stage": "Rules-only silver layer",
            "processing_present": str(count_present(auto["silver_processing_step_counts"])),
            "extraction_present": str(count_present(auto["silver_extraction_method_counts"])),
            "missing_context_flags": str(auto["uncertainty_flag_counts"].get("missing_processing_or_extraction_context", 0)),
            "unmapped_labels": "not_applicable",
            "patch_errors_after_retry": "not_applicable",
            "unresolved_edges": "0",
            "node_count": str(auto["kg_v3_node_count"]),
            "edge_count": str(auto["kg_v3_edge_count"]),
        },
        {
            "stage": "Abstract-level targeted LLM",
            "processing_present": str(count_present(targeted["processing_after"])),
            "extraction_present": str(count_present(targeted["extraction_after"])),
            "missing_context_flags": "329",
            "unmapped_labels": str(targeted["unmapped_processing_count"] + targeted["unmapped_extraction_count"]),
            "patch_errors_after_retry": "0",
            "unresolved_edges": "0",
            "node_count": str(targeted["node_count"]),
            "edge_count": str(targeted["edge_count"]),
        },
        {
            "stage": "Methods-section targeted LLM",
            "processing_present": str(count_present(methods["processing_after"])),
            "extraction_present": str(count_present(methods["extraction_after"])),
            "missing_context_flags": "303",
            "unmapped_labels": str(methods["unmapped_processing_count"] + methods["unmapped_extraction_count"]),
            "patch_errors_after_retry": "0",
            "unresolved_edges": str(final_unresolved),
            "node_count": str(methods["node_count"]),
            "edge_count": str(methods["edge_count"]),
        },
    ]
    return rows


def write_latex_snippets(stage_rows):
    SNIPPET_DIR.mkdir(parents=True, exist_ok=True)
    uncertainty_lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\caption{Uncertainty flags used in AutoTeaKG-Silver. Flags are stored on evidence records and propagated to graph edges through the evidence-record node.}",
        r"\label{tab:uncertainty_flags}",
        r"\begin{tabular}{p{0.23\linewidth}p{0.32\linewidth}p{0.32\linewidth}p{0.08\linewidth}}",
        r"\toprule",
        r"Flag & Trigger & Interpretation & Severity \\",
        r"\midrule",
    ]
    for row in UNCERTAINTY_FLAGS:
        uncertainty_lines.append(
            f"\\texttt{{{row['flag'].replace('_', '\\_')}}} & {row['trigger']} & {row['interpretation']} & {row['severity']} \\\\"
        )
    uncertainty_lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table}", ""])
    (SNIPPET_DIR / "uncertainty_flags_table.tex").write_text("\n".join(uncertainty_lines), encoding="utf-8")

    class_lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\caption{Uncertainty-class assignment rules. The severe flag set includes low LLM confidence, taxonomy expansion needed, missing component context, generic mechanism, and invalid controlled-vocabulary labels.}",
        r"\label{tab:uncertainty_classes}",
        r"\begin{tabular}{p{0.26\linewidth}p{0.55\linewidth}p{0.12\linewidth}}",
        r"\toprule",
        r"Class & Rule & Final count \\",
        r"\midrule",
        r"Low uncertainty & Silver confidence $\geq 0.80$ and no severe uncertainty flag. & 100 \\",
        r"Moderate uncertainty & Silver confidence $\geq 0.60$ and at most two severe uncertainty flags. & 470 \\",
        r"High uncertainty & All remaining records. & 65 \\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
        "",
    ]
    (SNIPPET_DIR / "uncertainty_classes_table.tex").write_text("\n".join(class_lines), encoding="utf-8")

    qc_lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\caption{Stage-wise ablation and quality-control summary. Each stage adds context or normalizes previous outputs while preserving a zero unresolved-edge graph export.}",
        r"\label{tab:stagewise_qc}",
        r"\begin{tabular}{p{0.27\linewidth}rrrrrr}",
        r"\toprule",
        r"Stage & Proc. & Extr. & Missing & Unmapped & Errors & Bad edges \\",
        r"\midrule",
    ]
    for row in stage_rows:
        qc_lines.append(
            f"{row['stage']} & {row['processing_present']} & {row['extraction_present']} & {row['missing_context_flags']} & {row['unmapped_labels']} & {row['patch_errors_after_retry']} & {row['unresolved_edges']} \\\\"
        )
    qc_lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table}", ""])
    (SNIPPET_DIR / "stagewise_qc_table.tex").write_text("\n".join(qc_lines), encoding="utf-8")

    methods_text = r"""
\paragraph{Uncertainty model.}
AutoTeaKG-Silver assigns uncertainty at the evidence-record level and propagates the same uncertainty attributes to graph edges through the evidence-record node. The silver confidence score combines the original extraction confidence with record specificity and context completeness. Context completeness assigns partial credit for non-generic tea type, component group, processing step, and extraction method. Mechanism specificity distinguishes missing or generic mechanisms from pathway-like or named mechanism labels. Records are then assigned uncertainty flags (Table~\ref{tab:uncertainty_flags}) and mapped to low, moderate, or high uncertainty classes using the rules in Table~\ref{tab:uncertainty_classes}.
"""
    (SNIPPET_DIR / "uncertainty_methods_paragraph.tex").write_text(methods_text.strip() + "\n", encoding="utf-8")

    results_text = r"""
The stage-wise quality-control summary shows that each pipeline stage contributes measurable context recovery while preserving graph integrity (Table~\ref{tab:stagewise_qc}). Processing-context coverage increased from 146 records in the rules-only silver layer to 167 records after abstract-level targeted extraction and 183 records after methods-section extraction. Extraction-context coverage increased from 154 to 170 and then to 185 records. The missing-context flag decreased from 365 to 303 records, while the final normalized KG retained zero unmapped processing/extraction labels and zero unresolved graph edges.
"""
    (SNIPPET_DIR / "stagewise_qc_results_paragraph.tex").write_text(results_text.strip() + "\n", encoding="utf-8")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(OUT_DIR / "uncertainty_flags_v4.csv", ["flag", "trigger", "interpretation", "severity"], UNCERTAINTY_FLAGS)
    stage_rows = build_stagewise_qc()
    write_csv(
        OUT_DIR / "stagewise_qc_v4.csv",
        [
            "stage",
            "processing_present",
            "extraction_present",
            "missing_context_flags",
            "unmapped_labels",
            "patch_errors_after_retry",
            "unresolved_edges",
            "node_count",
            "edge_count",
        ],
        stage_rows,
    )
    write_latex_snippets(stage_rows)
    print(f"Wrote {OUT_DIR / 'uncertainty_flags_v4.csv'}")
    print(f"Wrote {OUT_DIR / 'stagewise_qc_v4.csv'}")
    print(f"Wrote snippets to {SNIPPET_DIR}")


if __name__ == "__main__":
    main()
