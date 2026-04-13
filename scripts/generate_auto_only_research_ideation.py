import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"

MERGED_DIR = ROOT / "data" / "merged_batches" / "tea_pubmed_batch_2026-03-31_large_v2_llm_merged"
PAPERS_CSV = MERGED_DIR / "included_papers_llm_merged.csv"
RECORDS_CSV = MERGED_DIR / "evidence_records_llm_merged.csv"
SEARCH_ARCHIVE = REPORTS_DIR / "pubmed_search_archive_2026-04-02.json"

OUT_MD = REPORTS_DIR / "research_ideation_auto_only_2026-04-12.md"
OUT_JSON = REPORTS_DIR / "research_ideation_auto_only_data_profile_2026-04-12.json"
OUT_CSV = REPORTS_DIR / "research_ideation_auto_only_candidate_directions_2026-04-12.csv"


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def pct(value, total):
    if not total:
        return "0.0%"
    return f"{value / total * 100:.1f}%"


def safe_float(value):
    try:
        return float(value)
    except Exception:
        return None


def top_counts(rows, field, n=12):
    return Counter((row.get(field) or "").strip() for row in rows).most_common(n)


def markdown_count_table(title, counts, total):
    lines = [f"### {title}", "", "| Label | Count | Share |", "|---|---:|---:|"]
    for label, count in counts:
        display = label if label else "(blank)"
        lines.append(f"| {display} | {count} | {pct(count, total)} |")
    lines.append("")
    return "\n".join(lines)


def summarize_data():
    papers = read_csv(PAPERS_CSV)
    records = read_csv(RECORDS_CSV)
    llm_records = [row for row in records if row.get("annotator_id") == "glm5_nvidia"]
    auto_candidate_records = [row for row in records if row.get("annotator_id") == "auto_v1"]
    excluded_manual_records = [
        row
        for row in records
        if row.get("annotator_id") in {"codex_v1", "adjudicated"}
    ]

    confidence_values = [
        value
        for value in (safe_float(row.get("confidence_score")) for row in llm_records)
        if value is not None
    ]
    low_confidence = sum(value < 0.80 for value in confidence_values)

    human_types = {"cohort study", "randomized controlled trial", "meta-analysis"}
    human_records = [row for row in llm_records if row.get("study_type") in human_types]
    microbiome_records = [
        row
        for row in llm_records
        if row.get("activity_category") == "gut microbiota modulation"
        or row.get("microbiota_taxon")
        or row.get("microbial_metabolite")
    ]
    missing_mechanism = [row for row in llm_records if not (row.get("mechanism_label") or "").strip()]
    generic_mechanism = [
        row
        for row in llm_records
        if (row.get("mechanism_label") or "").strip().lower()
        in {"microbiota-associated mechanism", "antioxidant activity", ""}
    ]

    profile = {
        "date": "2026-04-12",
        "ideation_mode": "auto_only_no_manual_annotation_dependency",
        "input_files": {
            "papers": str(PAPERS_CSV.relative_to(ROOT)),
            "records": str(RECORDS_CSV.relative_to(ROOT)),
            "search_archive": str(SEARCH_ARCHIVE.relative_to(ROOT)),
        },
        "excluded_manual_sources": [
            "templates/evidence_records_expanded_batch_v1_2026-03-31.csv",
            "templates/evidence_records_mini_gold_set_v1_2026-03-31.csv",
            "templates/adjudication_log_mini_gold_set_v1_2026-03-31.csv",
            "templates/llm_manual_audit_worksheet_2026-04-02.csv",
        ],
        "counts": {
            "merged_papers": len(papers),
            "merged_records_all": len(records),
            "llm_records_used": len(llm_records),
            "auto_candidate_records_available": len(auto_candidate_records),
            "manual_records_excluded_detected": len(excluded_manual_records),
            "llm_distinct_papers": len({row.get("paper_id") for row in llm_records}),
            "llm_human_records": len(human_records),
            "llm_microbiome_records": len(microbiome_records),
            "llm_low_confidence_records_lt_0_80": low_confidence,
            "llm_missing_mechanism_records": len(missing_mechanism),
            "llm_generic_or_missing_mechanism_records": len(generic_mechanism),
        },
        "confidence": {
            "n": len(confidence_values),
            "min": min(confidence_values) if confidence_values else None,
            "max": max(confidence_values) if confidence_values else None,
            "mean": sum(confidence_values) / len(confidence_values) if confidence_values else None,
        },
        "distributions": {
            "activity_category": top_counts(llm_records, "activity_category", 20),
            "study_type": top_counts(llm_records, "study_type", 20),
            "evidence_level": top_counts(llm_records, "evidence_level", 20),
            "effect_direction": top_counts(llm_records, "effect_direction", 20),
            "tea_type": top_counts(llm_records, "tea_type", 20),
            "mechanism_label": top_counts(
                [row for row in llm_records if row.get("mechanism_label")],
                "mechanism_label",
                20,
            ),
            "microbiota_taxon": top_counts(
                [row for row in llm_records if row.get("microbiota_taxon")],
                "microbiota_taxon",
                20,
            ),
        },
    }
    return profile


def candidate_directions():
    return [
        {
            "rank": 1,
            "direction_id": "A01",
            "direction": "AutoTeaKG-Silver: fully automated tea functional evidence graph",
            "core_problem": "The field has enough literature, but manual curation does not scale and cannot support a living resource.",
            "approach": "Use PubMed retrieval, LLM extraction, schema validation, confidence calibration, duplicate consolidation, and graph export to create a silver-standard KG without manual labels.",
            "why_auto_only": "Uses only retrieval logs, abstracts, LLM outputs, rule validators, and graph consistency checks.",
            "novelty_claim": "Shifts the contribution from a curated tea database to a reproducible auto-updating evidence infrastructure.",
            "main_risk": "LLM hallucination and coarse extraction may contaminate KG edges.",
            "risk_control": "Store raw claim text, confidence, source PMID, schema-validation flags, and uncertainty class on every record/edge.",
        },
        {
            "rank": 2,
            "direction_id": "A02",
            "direction": "Processing-aware extraction gap miner",
            "core_problem": "Automatic records currently capture activity/study type, but processing/extraction/component fields are nearly blank.",
            "approach": "Develop specialized extraction prompts and weak rules for tea type, processing step, extraction method, and component group.",
            "why_auto_only": "Weak supervision comes from controlled vocabularies and title/abstract patterns rather than hand labels.",
            "novelty_claim": "Turns a real failure mode of the current pipeline into the next research problem.",
            "main_risk": "Many abstracts omit detailed processing parameters.",
            "risk_control": "Separate `reported_absent` from extraction failure; supplement with full-text retrieval only when abstract-level evidence is insufficient.",
        },
        {
            "rank": 3,
            "direction_id": "A03",
            "direction": "Uncertainty-aware tea microbiome mechanism graph",
            "core_problem": "Microbiome records are abundant but mechanism labels and taxa are often generic.",
            "approach": "Build a graph focused on tea -> microbiota -> metabolite -> host phenotype chains, with uncertainty classes for generic vs named mechanisms.",
            "why_auto_only": "Use automated entity linking, taxa/metabolite lexicons, and graph consistency constraints instead of manual refinement.",
            "novelty_claim": "Provides an automated mechanism-discovery layer on top of tea literature rather than a static expert-drawn pathway.",
            "main_risk": "Animal-study dominance may produce overconfident health narratives.",
            "risk_control": "Stratify every edge by study type and evidence level; never merge animal and human edges without provenance.",
        },
        {
            "rank": 4,
            "direction_id": "A04",
            "direction": "Human-preclinical translation gap atlas",
            "core_problem": "Many activity claims are preclinical, while human evidence is uneven across endpoints.",
            "approach": "Compare activity categories across animal, RCT, cohort, and meta-analysis records to identify translation gaps and mature claims.",
            "why_auto_only": "Uses study-type and evidence-level fields already extracted by GLM5 plus automatic consistency checks.",
            "novelty_claim": "Creates a computable map of where tea bioactivity claims have or lack human support.",
            "main_risk": "Study-type extraction errors may distort gap estimates.",
            "risk_control": "Use PubMed publication types and title keywords as rule-based cross-checks.",
        },
        {
            "rank": 5,
            "direction_id": "A05",
            "direction": "Automated tea claim monitor for future PubMed updates",
            "core_problem": "Tea bioactivity literature is moving quickly, making one-off reviews stale.",
            "approach": "Schedule incremental PubMed retrieval, skip already annotated PMIDs, auto-label new records, and update dashboards/KG deltas.",
            "why_auto_only": "The pipeline already supports incremental LLM annotation and skip-annotated behavior.",
            "novelty_claim": "Frames TeaKG as a living evidence surveillance system rather than a static resource.",
            "main_risk": "As an infrastructure paper alone, novelty may seem weaker.",
            "risk_control": "Pair with A01 or A02 so the monitor demonstrates a scientific use case.",
        },
    ]


def write_report(profile, directions):
    counts = profile["counts"]
    distributions = profile["distributions"]
    confidence = profile["confidence"]
    activity_counts = distributions["activity_category"]
    study_counts = distributions["study_type"]
    evidence_counts = distributions["evidence_level"]
    effect_counts = distributions["effect_direction"]
    tea_type_counts = distributions["tea_type"]

    lines = [
        "# Auto-Only Research Ideation for Tea Functional Activity KG",
        "",
        "Date: 2026-04-12",
        "",
        "Mode: `research-ideation` rerun using only previously retrieved literature, automatic PubMed normalization, automatic candidate generation, and GLM5 annotation outputs.",
        "",
        "Manual annotation dependency: **excluded**. This ideation does not use the mini gold set, adjudication logs, manual audit worksheet, or `codex_v1` records as evidence for selecting the research direction.",
        "",
        "## 1. Long-Term Goal",
        "",
        "Build a living, automatically updateable tea functional-activity evidence infrastructure that converts PubMed literature into uncertainty-aware database records and knowledge-graph edges without requiring manual annotation as the primary data-generation step.",
        "",
        "The scientific endpoint is not only a larger tea database. The endpoint is a reproducible system that can answer: which tea types, extracts, or components are associated with which activities, under which study designs and evidence levels, and where the evidence remains weak, generic, or under-specified.",
        "",
        "## 2. Auto-Only Data Basis",
        "",
        f"- Merged papers available: `{counts['merged_papers']}`.",
        f"- All merged evidence records: `{counts['merged_records_all']}`.",
        f"- GLM5 records used for this ideation: `{counts['llm_records_used']}` across `{counts['llm_distinct_papers']}` distinct papers.",
        f"- Auto candidate records available as fallback context: `{counts['auto_candidate_records_available']}`.",
        f"- Manual/adjudicated records detected and excluded from ideation evidence: `{counts['manual_records_excluded_detected']}`.",
        f"- Human evidence-like GLM5 records: `{counts['llm_human_records']}`.",
        f"- Microbiome-related GLM5 records: `{counts['llm_microbiome_records']}`.",
        f"- Low-confidence GLM5 records (`confidence_score < 0.80`): `{counts['llm_low_confidence_records_lt_0_80']}`.",
        f"- Missing or generic mechanism records: `{counts['llm_generic_or_missing_mechanism_records']}`.",
        "",
        f"Mean GLM5 confidence was `{confidence['mean']:.3f}` over `{confidence['n']}` records, with range `{confidence['min']:.2f}` to `{confidence['max']:.2f}`.",
        "",
        markdown_count_table("Activity Distribution From GLM5 Records", activity_counts, counts["llm_records_used"]),
        markdown_count_table("Study-Type Distribution From GLM5 Records", study_counts, counts["llm_records_used"]),
        markdown_count_table("Evidence-Level Distribution From GLM5 Records", evidence_counts, counts["llm_records_used"]),
        markdown_count_table("Effect-Direction Distribution From GLM5 Records", effect_counts, counts["llm_records_used"]),
        markdown_count_table("Tea-Type Distribution From GLM5 Records", tea_type_counts, counts["llm_records_used"]),
        "## 3. Literature Tree Rebuilt From the Auto Data",
        "",
        "### 3.1 Novelty Tree",
        "",
        "| Branch | What the auto data shows | Research implication |",
        "|---|---|---|",
        f"| Evidence-graded functional activity | GLM5 extracted `{counts['llm_records_used']}` records with clear activity and study-type structure. | C04 remains feasible, but the stronger novelty is automated evidence conversion rather than manual curation. |",
        f"| Microbiome mechanism layer | `{counts['llm_microbiome_records']}` records are microbiome-related, making C06 a strong graph-native demonstration. | Focus on uncertainty-aware microbiome subgraphs rather than hand-refined mechanism stories. |",
        "| Processing/composition context | GLM5 records largely miss component, processing, and extraction fields. | This is no longer just a data field; it is a core method problem and likely the highest-value technical gap. |",
        f"| Human/preclinical alignment | `{counts['llm_human_records']}` human evidence-like records coexist with a large animal-study block. | A translation-gap atlas is feasible without manual labels if study types are cross-checked automatically. |",
        "| Living update pipeline | PubMed retrieval, skip-annotated, retry, postprocess, merge, and SQLite refresh already exist. | The project can be reframed as an auto-updating evidence system rather than a static dataset. |",
        "",
        "### 3.2 Challenge-Insight Tree",
        "",
        "| Challenge | Observed in current data | Insight for the next research cycle |",
        "|---|---|---|",
        "| Manual curation does not scale | Hundreds of records are already produced automatically, while manual audit is separate and slower. | Make manual review optional evaluation, not the production bottleneck. |",
        "| Generic mechanisms | Many records use generic labels such as microbiota-associated mechanism or antioxidant activity. | Store mechanism specificity as a quality dimension and use entity-linking constraints to improve named mechanisms. |",
        "| Processing fields are sparse | `compound_group`, `processing_method`, and `extraction_method` are effectively absent in GLM5 outputs. | Design a specialized extraction module for process/component context. |",
        "| Broad `other` category | `other` is the largest activity class in GLM5 outputs. | Use automatic taxonomy expansion and out-of-scope detection before expanding the KG. |",
        "| Evidence-strength inflation risk | Animal studies dominate several activity categories. | Make evidence level a first-class graph attribute and restrict claims by study design. |",
        "",
        "## 4. Problem Selection",
        "",
        "The best problem is not simply building a bigger manually curated TeaKG. The better problem is:",
        "",
        "> Can a fully automated, uncertainty-aware pipeline convert tea functional-activity literature into a useful evidence database and KG without relying on manual annotation?",
        "",
        "### Well-Established Solution Check",
        "",
        "| Check | Assessment | Decision |",
        "|---|---|---|",
        "| Is there already a tea functional-activity KG? | Existing tea resources are closer to risky substances, genomics, transcriptomics, or narrative reviews. | Proceed. |",
        "| Is generic LLM extraction enough? | Current GLM5 output captures activity/study type but fails processing/component extraction and mechanism specificity. | Proceed; domain-specific constraints are needed. |",
        "| Is manual curation the only defensible path? | Manual review improves quality but cannot support a living resource at PubMed scale. | Do not make manual labels a dependency. |",
        "| Is this only engineering? | The scientific contribution becomes evidence modeling, uncertainty-aware KG construction, and discovery of translation/process gaps. | Proceed if evaluation includes utility tasks and failure-case analysis. |",
        "",
        "Selected problem: **Auto-only tea functional evidence graph construction with explicit uncertainty and processing-context gap recovery.**",
        "",
        "## 5. Solution Design",
        "",
        "### 5.1 Recommended Direction",
        "",
        "**A01 + A02 combined:** build `AutoTeaKG-Silver`, then make processing/component extraction the first method module.",
        "",
        "This is stronger than the previous C04-first framing because it no longer depends on hand-curated evidence records. The resource is treated as a silver-standard, automatically updated evidence layer, and quality is represented explicitly rather than hidden behind manual adjudication.",
        "",
        "### 5.2 Proposed Pipeline",
        "",
        "1. PubMed retrieval and query archiving: reuse the fixed query blocks and search logs.",
        "2. Automatic screening: use title/abstract rules and GLM5 paper-level screening.",
        "3. Automatic evidence extraction: extract activity, endpoint, study type, evidence level, mechanism, taxa/metabolites, and host phenotype.",
        "4. Specialized processing/component extractor: add controlled-vocabulary matching and focused prompts for tea type, processing step, extraction method, and component group.",
        "5. Schema validation: reject or flag records with invalid labels, missing provenance, impossible study/evidence combinations, or generic mechanisms.",
        "6. Uncertainty assignment: label each record/edge as high-confidence, low-confidence, generic-mechanism, missing-context, or taxonomy-expansion-needed.",
        "7. KG export: generate provenance-preserving nodes and edges where every edge retains PMID, raw claim text, confidence, and evidence level.",
        "8. Utility evaluation without manual labels: run consistency checks, duplicate-stability tests, query-answering coverage, and graph retrieval tasks.",
        "",
        "### 5.3 Non-Manual Evaluation Plan",
        "",
        "| Evaluation | No-manual signal | What it tests |",
        "|---|---|---|",
        "| Schema validity rate | Percentage of records passing controlled vocabularies and required-field rules. | Structural reliability. |",
        "| Prompt stability | Agreement across retry/prompt variants for the same PMID. | LLM extraction robustness. |",
        "| PubMed-type consistency | Agreement between LLM study type and PubMed publication type/title keywords. | Evidence-level reliability. |",
        "| Duplicate consolidation stability | Whether repeated records collapse to the same semantic key. | Incremental pipeline reliability. |",
        "| Graph query coverage | Number of answerable questions such as tea type -> activity -> evidence level -> mechanism. | Practical utility. |",
        "| Specificity score | Share of records with named mechanisms/taxa/metabolites instead of generic placeholders. | Biological usefulness. |",
        "| Human-preclinical gap map | Activity categories stratified by animal/RCT/cohort/meta-analysis records. | Scientific insight. |",
        "",
        "Manual audit can still be reported later as an external quality check, but it is not required for the core method or dataset construction.",
        "",
        "## 6. Candidate Directions",
        "",
        "| Rank | ID | Direction | Why it matters | Main risk |",
        "|---:|---|---|---|---|",
    ]
    for row in directions:
        lines.append(
            f"| {row['rank']} | {row['direction_id']} | {row['direction']} | {row['core_problem']} | {row['main_risk']} |"
        )
    lines.extend(
        [
            "",
            "## 7. Final Ideation Decision",
            "",
            "The new recommended research direction is:",
            "",
            "> **AutoTeaKG-Silver: an automatically generated, uncertainty-aware tea functional activity evidence graph, with a specialized module for processing/component context extraction.**",
            "",
            "The first paper should not claim that every extracted relation is manually verified. It should claim that the system creates a reproducible, updateable, provenance-rich silver evidence graph and makes uncertainty visible.",
            "",
            "## 8. Immediate Next Actions",
            "",
            "1. Build an auto-only quality dashboard over the locked merged database.",
            "2. Add a processing/component extractor and quantify how much it fills the current missing fields.",
            "3. Generate an auto-only KG v3 where each edge has uncertainty and specificity attributes.",
            "4. Run non-manual evaluation: schema validity, prompt stability, PubMed-type consistency, duplicate stability, and graph query coverage.",
            "5. Rewrite the paper story from `curated database` to `automated living evidence graph`.",
            "",
            "## 9. Boundary Conditions",
            "",
            "- Do not use manual adjudication as training data in this cycle.",
            "- Do not present `other` as a biological activity; treat it as taxonomy failure or out-of-scope signal.",
            "- Do not collapse animal and human evidence into the same claim strength.",
            "- Do not infer processing effects when abstracts do not report processing/extraction context.",
            "- Keep raw text, PMID, confidence, and uncertainty flags on every record and edge.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    profile = summarize_data()
    directions = candidate_directions()
    OUT_JSON.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(OUT_CSV, list(directions[0].keys()), directions)
    write_report(profile, directions)
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_CSV}")


if __name__ == "__main__":
    main()
