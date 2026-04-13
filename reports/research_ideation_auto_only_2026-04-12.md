# Auto-Only Research Ideation for Tea Functional Activity KG

Date: 2026-04-12

Mode: `research-ideation` rerun using only previously retrieved literature, automatic PubMed normalization, automatic candidate generation, and GLM5 annotation outputs.

Manual annotation dependency: **excluded**. This ideation does not use the mini gold set, adjudication logs, manual audit worksheet, or `codex_v1` records as evidence for selecting the research direction.

## 1. Long-Term Goal

Build a living, automatically updateable tea functional-activity evidence infrastructure that converts PubMed literature into uncertainty-aware database records and knowledge-graph edges without requiring manual annotation as the primary data-generation step.

The scientific endpoint is not only a larger tea database. The endpoint is a reproducible system that can answer: which tea types, extracts, or components are associated with which activities, under which study designs and evidence levels, and where the evidence remains weak, generic, or under-specified.

## 2. Auto-Only Data Basis

- Merged papers available: `524`.
- All merged evidence records: `669`.
- GLM5 records used for this ideation: `596` across `365` distinct papers.
- Auto candidate records available as fallback context: `39`.
- Manual/adjudicated records detected and excluded from ideation evidence: `28`.
- Human evidence-like GLM5 records: `128`.
- Microbiome-related GLM5 records: `184`.
- Low-confidence GLM5 records (`confidence_score < 0.80`): `21`.
- Missing or generic mechanism records: `194`.

Mean GLM5 confidence was `0.890` over `596` records, with range `0.50` to `0.95`.

### Activity Distribution From GLM5 Records

| Label | Count | Share |
|---|---:|---:|
| other | 160 | 26.8% |
| gut microbiota modulation | 151 | 25.3% |
| antioxidant | 78 | 13.1% |
| anti-inflammatory | 70 | 11.7% |
| metabolic improvement | 41 | 6.9% |
| anti-obesity | 40 | 6.7% |
| cardiovascular protection | 30 | 5.0% |
| neuroprotection | 26 | 4.4% |

### Study-Type Distribution From GLM5 Records

| Label | Count | Share |
|---|---:|---:|
| animal study | 270 | 45.3% |
| systematic review | 192 | 32.2% |
| cohort study | 65 | 10.9% |
| randomized controlled trial | 38 | 6.4% |
| meta-analysis | 25 | 4.2% |
| unspecified | 4 | 0.7% |
| in vitro | 2 | 0.3% |

### Evidence-Level Distribution From GLM5 Records

| Label | Count | Share |
|---|---:|---:|
| preclinical_in_vivo | 270 | 45.3% |
| evidence_synthesis_nonquantitative | 195 | 32.7% |
| human_observational | 63 | 10.6% |
| human_interventional | 38 | 6.4% |
| evidence_synthesis | 24 | 4.0% |
| low_preclinical | 3 | 0.5% |
| in_vitro | 1 | 0.2% |
| ex vivo | 1 | 0.2% |
| significant | 1 | 0.2% |

### Effect-Direction Distribution From GLM5 Records

| Label | Count | Share |
|---|---:|---:|
| positive | 293 | 49.2% |
| unclear | 155 | 26.0% |
| negative | 142 | 23.8% |
| no_clear_effect | 5 | 0.8% |
| mixed | 1 | 0.2% |

### Tea-Type Distribution From GLM5 Records

| Label | Count | Share |
|---|---:|---:|
| unspecified tea | 315 | 52.9% |
| green tea | 198 | 33.2% |
| fermented tea | 27 | 4.5% |
| black tea | 21 | 3.5% |
| dark tea | 19 | 3.2% |
| white tea | 8 | 1.3% |
| yellow tea | 6 | 1.0% |
| oolong tea | 2 | 0.3% |

## 3. Literature Tree Rebuilt From the Auto Data

### 3.1 Novelty Tree

| Branch | What the auto data shows | Research implication |
|---|---|---|
| Evidence-graded functional activity | GLM5 extracted `596` records with clear activity and study-type structure. | C04 remains feasible, but the stronger novelty is automated evidence conversion rather than manual curation. |
| Microbiome mechanism layer | `184` records are microbiome-related, making C06 a strong graph-native demonstration. | Focus on uncertainty-aware microbiome subgraphs rather than hand-refined mechanism stories. |
| Processing/composition context | GLM5 records largely miss component, processing, and extraction fields. | This is no longer just a data field; it is a core method problem and likely the highest-value technical gap. |
| Human/preclinical alignment | `128` human evidence-like records coexist with a large animal-study block. | A translation-gap atlas is feasible without manual labels if study types are cross-checked automatically. |
| Living update pipeline | PubMed retrieval, skip-annotated, retry, postprocess, merge, and SQLite refresh already exist. | The project can be reframed as an auto-updating evidence system rather than a static dataset. |

### 3.2 Challenge-Insight Tree

| Challenge | Observed in current data | Insight for the next research cycle |
|---|---|---|
| Manual curation does not scale | Hundreds of records are already produced automatically, while manual audit is separate and slower. | Make manual review optional evaluation, not the production bottleneck. |
| Generic mechanisms | Many records use generic labels such as microbiota-associated mechanism or antioxidant activity. | Store mechanism specificity as a quality dimension and use entity-linking constraints to improve named mechanisms. |
| Processing fields are sparse | `compound_group`, `processing_method`, and `extraction_method` are effectively absent in GLM5 outputs. | Design a specialized extraction module for process/component context. |
| Broad `other` category | `other` is the largest activity class in GLM5 outputs. | Use automatic taxonomy expansion and out-of-scope detection before expanding the KG. |
| Evidence-strength inflation risk | Animal studies dominate several activity categories. | Make evidence level a first-class graph attribute and restrict claims by study design. |

## 4. Problem Selection

The best problem is not simply building a bigger manually curated TeaKG. The better problem is:

> Can a fully automated, uncertainty-aware pipeline convert tea functional-activity literature into a useful evidence database and KG without relying on manual annotation?

### Well-Established Solution Check

| Check | Assessment | Decision |
|---|---|---|
| Is there already a tea functional-activity KG? | Existing tea resources are closer to risky substances, genomics, transcriptomics, or narrative reviews. | Proceed. |
| Is generic LLM extraction enough? | Current GLM5 output captures activity/study type but fails processing/component extraction and mechanism specificity. | Proceed; domain-specific constraints are needed. |
| Is manual curation the only defensible path? | Manual review improves quality but cannot support a living resource at PubMed scale. | Do not make manual labels a dependency. |
| Is this only engineering? | The scientific contribution becomes evidence modeling, uncertainty-aware KG construction, and discovery of translation/process gaps. | Proceed if evaluation includes utility tasks and failure-case analysis. |

Selected problem: **Auto-only tea functional evidence graph construction with explicit uncertainty and processing-context gap recovery.**

## 5. Solution Design

### 5.1 Recommended Direction

**A01 + A02 combined:** build `AutoTeaKG-Silver`, then make processing/component extraction the first method module.

This is stronger than the previous C04-first framing because it no longer depends on hand-curated evidence records. The resource is treated as a silver-standard, automatically updated evidence layer, and quality is represented explicitly rather than hidden behind manual adjudication.

### 5.2 Proposed Pipeline

1. PubMed retrieval and query archiving: reuse the fixed query blocks and search logs.
2. Automatic screening: use title/abstract rules and GLM5 paper-level screening.
3. Automatic evidence extraction: extract activity, endpoint, study type, evidence level, mechanism, taxa/metabolites, and host phenotype.
4. Specialized processing/component extractor: add controlled-vocabulary matching and focused prompts for tea type, processing step, extraction method, and component group.
5. Schema validation: reject or flag records with invalid labels, missing provenance, impossible study/evidence combinations, or generic mechanisms.
6. Uncertainty assignment: label each record/edge as high-confidence, low-confidence, generic-mechanism, missing-context, or taxonomy-expansion-needed.
7. KG export: generate provenance-preserving nodes and edges where every edge retains PMID, raw claim text, confidence, and evidence level.
8. Utility evaluation without manual labels: run consistency checks, duplicate-stability tests, query-answering coverage, and graph retrieval tasks.

### 5.3 Non-Manual Evaluation Plan

| Evaluation | No-manual signal | What it tests |
|---|---|---|
| Schema validity rate | Percentage of records passing controlled vocabularies and required-field rules. | Structural reliability. |
| Prompt stability | Agreement across retry/prompt variants for the same PMID. | LLM extraction robustness. |
| PubMed-type consistency | Agreement between LLM study type and PubMed publication type/title keywords. | Evidence-level reliability. |
| Duplicate consolidation stability | Whether repeated records collapse to the same semantic key. | Incremental pipeline reliability. |
| Graph query coverage | Number of answerable questions such as tea type -> activity -> evidence level -> mechanism. | Practical utility. |
| Specificity score | Share of records with named mechanisms/taxa/metabolites instead of generic placeholders. | Biological usefulness. |
| Human-preclinical gap map | Activity categories stratified by animal/RCT/cohort/meta-analysis records. | Scientific insight. |

Manual audit can still be reported later as an external quality check, but it is not required for the core method or dataset construction.

## 6. Candidate Directions

| Rank | ID | Direction | Why it matters | Main risk |
|---:|---|---|---|---|
| 1 | A01 | AutoTeaKG-Silver: fully automated tea functional evidence graph | The field has enough literature, but manual curation does not scale and cannot support a living resource. | LLM hallucination and coarse extraction may contaminate KG edges. |
| 2 | A02 | Processing-aware extraction gap miner | Automatic records currently capture activity/study type, but processing/extraction/component fields are nearly blank. | Many abstracts omit detailed processing parameters. |
| 3 | A03 | Uncertainty-aware tea microbiome mechanism graph | Microbiome records are abundant but mechanism labels and taxa are often generic. | Animal-study dominance may produce overconfident health narratives. |
| 4 | A04 | Human-preclinical translation gap atlas | Many activity claims are preclinical, while human evidence is uneven across endpoints. | Study-type extraction errors may distort gap estimates. |
| 5 | A05 | Automated tea claim monitor for future PubMed updates | Tea bioactivity literature is moving quickly, making one-off reviews stale. | As an infrastructure paper alone, novelty may seem weaker. |

## 7. Final Ideation Decision

The new recommended research direction is:

> **AutoTeaKG-Silver: an automatically generated, uncertainty-aware tea functional activity evidence graph, with a specialized module for processing/component context extraction.**

The first paper should not claim that every extracted relation is manually verified. It should claim that the system creates a reproducible, updateable, provenance-rich silver evidence graph and makes uncertainty visible.

## 8. Immediate Next Actions

1. Build an auto-only quality dashboard over the locked merged database.
2. Add a processing/component extractor and quantify how much it fills the current missing fields.
3. Generate an auto-only KG v3 where each edge has uncertainty and specificity attributes.
4. Run non-manual evaluation: schema validity, prompt stability, PubMed-type consistency, duplicate stability, and graph query coverage.
5. Rewrite the paper story from `curated database` to `automated living evidence graph`.

## 9. Boundary Conditions

- Do not use manual adjudication as training data in this cycle.
- Do not present `other` as a biological activity; treat it as taxonomy failure or out-of-scope signal.
- Do not collapse animal and human evidence into the same claim strength.
- Do not infer processing effects when abstracts do not report processing/extraction context.
- Keep raw text, PMID, confidence, and uncertainty flags on every record and edge.
