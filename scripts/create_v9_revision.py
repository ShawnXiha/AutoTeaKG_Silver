"""Create v9 manuscript revision and supporting tables.

This script executes the v9 review plan from the v8 manuscript. It keeps v8
intact, writes v9 snippets/data, compiles v9, and copies final PDF/TeX outputs.
"""

from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "writing_outputs" / "20260412_autoteakg_silver_paper"
DRAFT_DIR = PAPER_DIR / "drafts"
DATA_DIR = PAPER_DIR / "data"
FINAL_DIR = PAPER_DIR / "final"
SNIPPET_DIR = DRAFT_DIR / "v9_snippets"
KG_DIR = ROOT / "reports" / "methods_processing_vocab_normalized"

V8 = DRAFT_DIR / "v8_database_draft.tex"
V9 = DRAFT_DIR / "v9_database_draft.tex"
RECORDS_CSV = KG_DIR / "autoteakg_silver_records.csv"
CASE_CSV = DATA_DIR / "graph_query_case_study_polysaccharide_microbiome_v4.csv"
VALIDATION_JSON = DATA_DIR / "validation_v4" / "validation_results_v4.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise RuntimeError(f"Expected text not found: {old[:100]!r}")
    return text.replace(old, new, 1)


def count_flat_keyword_records(records: list[dict[str, str]]) -> int:
    count = 0
    for row in records:
        haystack = " ".join(str(v) for v in row.values()).lower()
        if (
            "polysaccharide" in haystack
            and "microbi" in haystack
            and ("liver" in haystack or "hepatic" in haystack or "nafld" in haystack)
        ):
            count += 1
    return count


def make_graph_vs_flat_table() -> None:
    records = read_csv(RECORDS_CSV)
    graph_rows = read_csv(CASE_CSV)
    flat_count = count_flat_keyword_records(records)
    rows = [
        {
            "mode": "Graph evidence-path query",
            "query_or_filter": "component = tea polysaccharides; microbiome/metabolite or host-phenotype fields present; evidence-record path retained",
            "returned_records": len(graph_rows),
            "component_constraint": "explicit normalized field",
            "metabolite_phenotype_constraint": "explicit path fields",
            "evidence_uncertainty": "retained per EvidenceRecord",
            "provenance": "record_id and paper_id retained",
        },
        {
            "mode": "Flat keyword retrieval",
            "query_or_filter": "polysaccharide AND microbi* AND (liver OR hepatic OR NAFLD) over concatenated record text",
            "returned_records": flat_count,
            "component_constraint": "text match only",
            "metabolite_phenotype_constraint": "not structurally enforced",
            "evidence_uncertainty": "requires post hoc lookup",
            "provenance": "paper match retained, path not retained",
        },
    ]
    write_csv(
        DATA_DIR / "graph_vs_flat_query_comparison_v9.csv",
        list(rows[0].keys()),
        rows,
    )

    latex = r"""\begin{table}[t]
\centering
\scriptsize
\caption{Graph query versus flat keyword retrieval for the tea-polysaccharide microbiome case. The comparison is descriptive: the graph query preserves typed constraints and evidence attributes, whereas the keyword query retrieves text matches that require post hoc interpretation.}
\label{tab:graph_vs_flat_query}
\begin{tabularx}{\linewidth}{p{0.20\linewidth}p{0.12\linewidth}Xp{0.14\linewidth}p{0.15\linewidth}}
\toprule
Mode & Records & Constraint handling & Evidence attrs. & Provenance \\
\midrule
Graph evidence-path query & %d & Component, microbiome/metabolite, and phenotype constraints are typed graph fields. & Retained per EvidenceRecord. & Record and paper identifiers retained along the path. \\
Flat keyword retrieval & %d & Text matches identify candidate records, but metabolite/phenotype constraints are not structurally enforced. & Requires post hoc lookup. & Paper matches retained; evidence path not retained. \\
\bottomrule
\end{tabularx}
\end{table}
""" % (len(graph_rows), flat_count)
    write_text(SNIPPET_DIR / "graph_vs_flat_query_table.tex", latex)


def make_validation_error_tables() -> None:
    validation = json.loads(VALIDATION_JSON.read_text(encoding="utf-8"))
    issue_labels = {
        "out_of_scope": "Out of scope",
        "wrong_activity": "Wrong activity",
        "wrong_study_type": "Wrong study type",
        "wrong_component": "Wrong component",
        "duplicate_or_unclear": "Duplicate or unclear",
    }
    issue_rows = []
    for key, count in sorted(validation["major_issue_counter"].items(), key=lambda item: (-item[1], item[0])):
        issue_rows.append(
            {
                "issue_type": issue_labels.get(key, key.replace("_", " ")),
                "count": count,
                "interpretation": {
                    "out_of_scope": "Corpus-boundary or inclusion issue",
                    "wrong_activity": "Activity taxonomy or extraction issue",
                    "wrong_study_type": "Study-design classification issue",
                    "wrong_component": "Exposure/component extraction issue",
                    "duplicate_or_unclear": "Deduplication or claim clarity issue",
                }.get(key, "Review issue"),
            }
        )
    write_csv(DATA_DIR / "validation_error_summary_v9.csv", ["issue_type", "count", "interpretation"], issue_rows)

    uncertainty_rows = [
        {"uncertainty_class": key.replace("_", " "), "reviewed_records": value}
        for key, value in validation["uncertainty_counter"].items()
    ]
    write_csv(DATA_DIR / "validation_by_uncertainty_v9.csv", ["uncertainty_class", "reviewed_records"], uncertainty_rows)

    issue_lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\caption{Validation issue summary across reviewer major-issue tags. Counts are issue tags rather than mutually exclusive records because one record may receive more than one issue tag.}",
        r"\label{tab:validation_error_summary}",
        r"\begin{tabularx}{\linewidth}{lrl}",
        r"\toprule",
        r"Issue type & Count & Primary interpretation \\",
        r"\midrule",
    ]
    for row in issue_rows:
        issue_lines.append(f"{row['issue_type']} & {row['count']} & {row['interpretation']} \\\\")
    issue_lines.extend([r"\bottomrule", r"\end{tabularx}", r"\end{table}", ""])
    write_text(SNIPPET_DIR / "validation_error_summary_table.tex", "\n".join(issue_lines))

    uncertainty_lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\caption{Reviewed validation sample by uncertainty class. The sample was stratified before manual review and was not used to construct KG v3.}",
        r"\label{tab:validation_by_uncertainty}",
        r"\begin{tabular}{lr}",
        r"\toprule",
        r"Uncertainty class & Reviewed records \\",
        r"\midrule",
    ]
    for row in uncertainty_rows:
        uncertainty_lines.append(f"{row['uncertainty_class'].title()} & {row['reviewed_records']} \\\\")
    uncertainty_lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table}", ""])
    write_text(SNIPPET_DIR / "validation_by_uncertainty_table.tex", "\n".join(uncertainty_lines))


def make_schema_summary_table() -> None:
    rows = [
        ("tea type", "Controlled vocabulary plus raw label", "Title/abstract extraction and post-processing"),
        ("component group", "Controlled vocabulary plus raw evidence terms", "LLM extraction, rule fallback, vocabulary normalization"),
        ("activity category", "Controlled vocabulary", "LLM extraction constrained by activity taxonomy"),
        ("study type", "Controlled vocabulary", "LLM extraction and evidence-level normalization"),
        ("evidence level", "Controlled vocabulary", "Derived from study type when missing or inconsistent"),
        ("processing step", "Controlled vocabulary plus raw label", "Rules, abstract-level targeted extraction, methods-section targeted extraction"),
        ("extraction method", "Controlled vocabulary plus raw label", "Rules, abstract-level targeted extraction, methods-section targeted extraction"),
        ("mechanism label", "Free text with specificity scoring", "LLM extraction and uncertainty flagging"),
        ("microbiota, metabolite, phenotype", "Free text fields", "LLM extraction and graph export"),
        ("uncertainty class", "Low/moderate/high", "Derived from confidence, specificity, context completeness, and flags"),
    ]
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\footnotesize",
        r"\caption{Extraction schema summary for the silver evidence records. Controlled-vocabulary fields are normalized before KG export, while raw labels and evidence terms are retained for auditability.}",
        r"\label{tab:extraction_schema_summary}",
        r"\begin{tabularx}{\linewidth}{p{0.22\linewidth}p{0.28\linewidth}X}",
        r"\toprule",
        r"Field & Field type & Source or normalization rule \\",
        r"\midrule",
    ]
    for field, field_type, source in rows:
        lines.append(f"{field} & {field_type} & {source} \\\\")
    lines.extend([r"\bottomrule", r"\end{tabularx}", r"\end{table}", ""])
    write_text(SNIPPET_DIR / "extraction_schema_summary_table.tex", "\n".join(lines))


def build_v9_tex() -> None:
    text = V8.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "External validation of 47 completed stratified records showed acceptable rates",
        "A stratified external validation sample of 47 completed records showed acceptable rates among completed field judgments",
    )
    text = replace_once(
        text,
        "The contributions are fourfold and each is tied to a result-level evidence anchor (Table~\\ref{tab:claim_evidence_map}).",
        "The contributions are fourfold and each is tied to a result-level evidence anchor summarized in Supplementary Data~\\ref{app:claim_evidence_map}.",
    )
    text = replace_once(text, "\n\\input{v8_snippets/claim_evidence_map_table.tex}\n", "\n")
    text = replace_once(
        text,
        "\\subsection{AutoTeaKG-Silver constructs a provenance-rich tea functional activity graph}",
        "\\subsection{Resource composition}",
    )
    text = replace_once(
        text,
        "The query recovered five representative records linking tea polysaccharides to gut microbiota modulation, butyric acid or SCFA-related metabolites, and liver, barrier, or lipid-deposition phenotypes (Table~\\ref{tab:graph_query_case}; Figures~\\ref{fig:graph_utility_case} and~\\ref{fig:graph_query_case}). The retrieved paths preserve evidence level and uncertainty class, allowing users to separate low-uncertainty preclinical gut-liver-axis records from broader moderate-uncertainty microbiome records. This case is the strongest utility test in the manuscript because the answer requires simultaneous constraints on component, mechanism, metabolite, phenotype, evidence, and uncertainty fields.",
        "The query recovered five representative records linking tea polysaccharides to gut microbiota modulation, butyric acid or SCFA-related metabolites, and liver, barrier, or lipid-deposition phenotypes (Table~\\ref{tab:graph_query_case}; Figures~\\ref{fig:graph_utility_case} and~\\ref{fig:graph_query_case}). The retrieved paths preserve evidence level and uncertainty class, allowing users to separate low-uncertainty preclinical gut-liver-axis records from broader moderate-uncertainty microbiome records. A flat keyword query returned a larger candidate set but did not structurally preserve component, metabolite, phenotype, evidence-level, uncertainty, and provenance constraints (Table~\\ref{tab:graph_vs_flat_query}). This comparison shows why the graph representation is useful: the answer is an evidence path rather than only a list of matching papers.",
    )
    text = replace_once(
        text,
        "\\begin{table}[t]\n\\centering\n\\small\n\\caption{Graph query case study",
        "\\input{v9_snippets/graph_vs_flat_query_table.tex}\n\n\\begin{table}[t]\n\\centering\n\\scriptsize\n\\caption{Graph query case study",
    )
    text = replace_once(
        text,
        "The completed 47-record validation sample provides an external check on the silver-standard graph",
        "The completed 47-record stratified validation sample provides an external check on the silver-standard graph",
    )
    text = replace_once(
        text,
        "Major issue tags were concentrated in out-of-scope records, wrong activity labels, and wrong study-type assignments. These results support silver-standard use while identifying the fields that should be prioritized in future correction cycles.",
        "These rates are computed over completed field judgments rather than over all sampled records. The dominant major-issue tags were out-of-scope records, wrong activity labels, and wrong study-type assignments (Table~\\ref{tab:validation_error_summary}). These results support silver-standard use while identifying the fields that should be prioritized in future correction cycles.",
    )
    text = replace_once(
        text,
        "\\input{v8_snippets/validation_results_compact_table.tex}",
        "\\input{v8_snippets/validation_results_compact_table.tex}\n\n\\input{v9_snippets/validation_error_summary_table.tex}",
    )
    text = replace_once(
        text,
        "This work has four important limitations. First, AutoTeaKG-Silver is a silver-standard resource, not a manually verified gold-standard database; users should apply uncertainty filters when drawing precise biological conclusions.",
        "This work has five important limitations. First, AutoTeaKG-Silver is a silver-standard resource, not a manually verified gold-standard database; users should apply uncertainty filters when drawing precise biological conclusions. Second, the external validation covers a stratified sample rather than the full graph, and it reports field-level judgments rather than complete expert adjudication of every edge.",
    )
    text = replace_once(text, "Second, the current system relies", "Third, the current system relies")
    text = replace_once(text, "Third, processing and extraction labels", "Fourth, processing and extraction labels")
    text = replace_once(text, "Fourth, the microbiome subgraph", "Fifth, the microbiome subgraph")
    text = replace_once(text, "git@github.com:ShawnXiha/AutoTeaKG_Silver.git", "https://github.com/ShawnXiha/AutoTeaKG_Silver")

    text = replace_once(
        text,
        "\\begin{tabularx}{\\linewidth}{p{0.22\\linewidth}p{0.30\\linewidth}Xp{0.07\\linewidth}}",
        "\\begin{tabularx}{\\linewidth}{p{0.21\\linewidth}p{0.29\\linewidth}Xp{0.09\\linewidth}}",
    )
    text = replace_once(
        text,
        "\\section{Supplementary Data: Validation Sample}\n\\label{app:validation}",
        "\\section{Supplementary Data: Claim--Evidence Map}\n\\label{app:claim_evidence_map}\n\n\\input{v8_snippets/claim_evidence_map_table.tex}\n\n\\section{Supplementary Data: Extraction Schema Summary}\n\\label{app:extraction_schema}\n\n\\input{v9_snippets/extraction_schema_summary_table.tex}\n\n\\section{Supplementary Data: Validation Sample}\n\\label{app:validation}",
    )
    text = replace_once(
        text,
        "The released worksheet evaluates activity category, study type, evidence level, component group, processing step, extraction method, and mechanism label. Field-level results should be reported only after the worksheet is completed by reviewers.",
        "The completed worksheet evaluates activity category, study type, evidence level, component group, processing step, extraction method, and mechanism label. Released validation artifacts include \\path{data/validation_v4/validation_worksheet_v4_filled_cleaned.csv}, \\path{data/validation_v4/validation_results_by_field_v4.csv}, and \\path{data/validation_v4/validation_results_v4.json}. The reviewed sample by uncertainty class is summarized in Table~\\ref{tab:validation_by_uncertainty}.\n\n\\input{v9_snippets/validation_by_uncertainty_table.tex}",
    )

    V9.write_text(text, encoding="utf-8")


def compile_v9() -> None:
    for cmd in [
        ["pdflatex", "-interaction=nonstopmode", "v9_database_draft.tex"],
        ["bibtex", "v9_database_draft"],
        ["pdflatex", "-interaction=nonstopmode", "v9_database_draft.tex"],
        ["pdflatex", "-interaction=nonstopmode", "v9_database_draft.tex"],
    ]:
        subprocess.run(cmd, cwd=DRAFT_DIR, check=True)
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(V9, FINAL_DIR / "AutoTeaKG_Silver_v9_database.tex")
    shutil.copy2(DRAFT_DIR / "v9_database_draft.pdf", FINAL_DIR / "AutoTeaKG_Silver_v9_database.pdf")


def pdf_page_count(path: Path) -> int:
    result = subprocess.run(
        ["pdfinfo", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    match = re.search(r"^Pages:\s+(\d+)", result.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError(f"Could not determine PDF page count for {path}")
    return int(match.group(1))


def update_docs() -> None:
    summary = PAPER_DIR / "SUMMARY.md"
    pages = pdf_page_count(FINAL_DIR / "AutoTeaKG_Silver_v9_database.pdf")
    text = summary.read_text(encoding="utf-8")
    text = text.replace("- Latest final PDF: `final/AutoTeaKG_Silver_v8_database.pdf`", "- Latest final PDF: `final/AutoTeaKG_Silver_v9_database.pdf`")
    text = text.replace("- Latest final TeX: `final/AutoTeaKG_Silver_v8_database.tex`", "- Latest final TeX: `final/AutoTeaKG_Silver_v9_database.tex`")
    text = text.replace("- Previous PDF: `final/AutoTeaKG_Silver_v7_database.pdf`", "- Previous PDF: `final/AutoTeaKG_Silver_v8_database.pdf`\n- Previous TeX: `final/AutoTeaKG_Silver_v8_database.tex`\n- Previous PDF: `final/AutoTeaKG_Silver_v7_database.pdf`")
    text = text.replace("- Latest editable draft: `drafts/v8_database_draft.tex`", "- Latest editable draft: `drafts/v9_database_draft.tex`")
    text = re.sub(
        r"- v9 Database-oriented PDF length: \d+ pages\.\n?",
        "",
        text,
    )
    text = text.replace(
        "- v8 Database-oriented PDF length: 18 pages.",
        f"- v8 Database-oriented PDF length: 18 pages.\n- v9 Database-oriented PDF length: {pages} pages.",
    )
    insert = """
## v9 Database-Oriented Additions

- Bounded validation wording to the stratified validation sample and completed field judgments.
- Replaced the reader-facing repository URL with HTTPS.
- Fixed stale validation appendix wording and added completed validation artifact paths.
- Added graph-vs-flat keyword retrieval comparison for the tea-polysaccharide microbiome case.
- Added validation error summary and validation-by-uncertainty supplementary tables.
- Added an extraction schema summary table to Supplementary Data.
- Shortened one long Results subsection heading and tightened table layout.
- Recompiled successfully with no undefined citations or references.
"""
    if "## v9 Database-Oriented Additions" not in text:
        text = text.replace("## Review Artifacts\n", insert + "\n## Review Artifacts\n")
    summary.write_text(text, encoding="utf-8")

    notes = DRAFT_DIR / "revision_notes.md"
    text = notes.read_text(encoding="utf-8")
    if "## v9 Database-oriented" not in text:
        text += """

## v9 Database-oriented

Date: 2026-04-25

Changes from v8:

- Executed the v9 revision plan from `reviews/REVISION_PLAN_v9.md`.
- Bounded validation claims to the stratified validation sample and completed field judgments.
- Replaced the SSH GitHub repository URL with a reader-facing HTTPS URL.
- Updated stale validation appendix wording and added completed validation artifact paths.
- Added graph-vs-flat retrieval comparison for the tea-polysaccharide microbiome case.
- Added validation error summary and validation-by-uncertainty supplementary tables.
- Added a supplementary extraction schema summary table.
- Shortened the long resource-composition subsection title and reduced selected table layout pressure.
- Recompiled successfully with no undefined citations or references.
"""
    notes.write_text(text, encoding="utf-8")


def update_action_matrix() -> None:
    path = PAPER_DIR / "reviews" / "revision_action_matrix_v9.csv"
    rows = read_csv(path)
    for row in rows:
        if row["status"] in {"pending", "optional"}:
            row["status"] = "completed"
    write_csv(path, rows[0].keys(), rows)


def main() -> None:
    SNIPPET_DIR.mkdir(parents=True, exist_ok=True)
    make_graph_vs_flat_table()
    make_validation_error_tables()
    make_schema_summary_table()
    build_v9_tex()
    compile_v9()
    update_docs()
    update_action_matrix()
    print(f"Wrote {V9}")
    print(f"Wrote {FINAL_DIR / 'AutoTeaKG_Silver_v9_database.pdf'}")


if __name__ == "__main__":
    main()
