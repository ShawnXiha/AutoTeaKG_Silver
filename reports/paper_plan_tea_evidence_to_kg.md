# Paper Planning

Title: From Evidence-Graded Tea Functional Activity Database to Processing-Aware Atlas and Microbiome Mechanism KG

Date: 2026-03-31

## 0. Planning Decision

Chosen roadmap:
1. Phase 1 paper: C04 `Evidence-Graded Tea Health Claims Database`
2. Phase 2 extension: integrate C01 `Processing-Bioactivity Atlas` fields
3. Phase 3 extension: build C06 `Tea Microbiome Mechanism Graph`

Planning principle:
- Scope first, graph later
- Narrow claim before broad claim
- Design ablations before polishing method narrative

---

## 1. Mock Rejection Letter First

These are the top likely reviewer objections and the planning response to each.

### R1. "This is only a database / curation paper with limited methodological novelty."

Response in planning:
- Emphasize that the contribution is not raw collection, but evidence normalization plus cross-study comparability plus extension-ready schema.
- Include an explicit evidence model and study-type grading framework.
- Add utility experiments showing that the resource answers questions standard review retrieval cannot answer efficiently.

### R2. "The scope is too broad and the schema may be under-specified."

Response in planning:
- Freeze phase 1 scope to 4 activity families, 4-6 component groups, and 3-4 tea categories.
- Publish the schema with explicit entity and relation definitions.
- Treat KG as an extension path, not as the core phase-1 claim.

### R3. "There is no convincing evaluation beyond descriptive statistics."

Response in planning:
- Add curation quality metrics, extraction precision, inter-curator agreement, coverage analysis, and question-answering utility benchmarks.
- Add ablations on processing context, evidence grading, and component granularity.

### R4. "The evidence grading may be subjective."

Response in planning:
- Use a formal evidence ladder.
- Define annotation rules in advance.
- Measure annotator agreement and adjudication rate.

### R5. "The work may not generalize because tea endpoints and process terminology are heterogeneous."

Response in planning:
- Use a hierarchical schema: broad normalized labels plus raw reported labels.
- Include a heterogeneity audit as an explicit result rather than treating it as noise.

---

## 2. Story Design

### 2.1 Smallest Defensible Core Claim

We present the first evidence-graded structured tea functional activity resource that normalizes tea type, extract/component group, activity category, model system, dose/exposure, and evidence level, while remaining extensible to processing-aware atlas and mechanism-focused knowledge graph construction.

This is the narrow claim.  
Do not claim in paper 1 that we have already solved full tea knowledge graph construction.

### 2.2 Broad Claim for Later

Structured evidence modeling can serve as the substrate for tea-specific atlas construction, mechanism graph reasoning, and future hypothesis generation.

### 2.3 Task -> Challenge -> Insight -> Contribution -> Advantage

#### Task
Systematically organize literature on tea, tea extracts, and tea components with respect to functional activity and influencing factors.

#### Challenge
Existing tea activity evidence is fragmented across tea types, component names, study designs, endpoints, and processing contexts. Narrative reviews summarize this knowledge but do not make it computable or directly comparable.

#### Insight
The key bottleneck is not missing literature, but missing evidence structure. If we normalize the literature around evidence level and a constrained tea-specific schema, we can create a reliable substrate that later absorbs processing fields and graph-native relations.

#### Contribution
1. A tea functional activity evidence schema with explicit entities, attributes, and relation-ready fields.
2. A curated database that grades evidence across in vitro, animal, RCT, cohort, and meta-analysis studies.
3. A processing-aware extension layer that connects composition and activity context.
4. A forward-compatible mapping from structured database records to microbiome mechanism KG triples.

#### Advantage
1. More interpretable than narrative reviews.
2. More feasible than building a full broad tea KG from the start.
3. More reusable for later graph, prediction, and proposal-generation tasks.

### 2.4 Story in Forward Narrative Form

Tea is widely studied for beneficial functional activities, but the field has accumulated in a fragmented way. Existing reviews and isolated resources do not let researchers directly compare claims by evidence level, tea category, component group, and context. We therefore build a structured evidence-graded tea activity resource as a first step. We then show that adding processing/composition context improves cross-study interpretability, and we define a principled path from database records to a microbiome mechanism KG.

### 2.5 Module Motivation Mapping

| Module | Why needed | What problem it solves | What would happen without it |
|--------|------------|------------------------|------------------------------|
| Evidence schema | Normalize literature | Makes heterogeneous studies comparable | Resource becomes a spreadsheet dump |
| Evidence grading layer | Distinguish claim strength | Prevents over-reading in vitro evidence | Strong and weak claims get mixed |
| Processing/context fields | Capture C01 extension | Links activity differences to process/composition context | Bioactivity remains decontextualized |
| KG mapping layer | Prepare C06 extension | Enables mechanism graph construction later | Database cannot evolve into graph reasoning |

### 2.6 Fallback Narrative

If reviewers see the work as insufficiently novel as a database paper, pivot to:
- "A reproducible evidence-modeling framework for tea functional activity literature"
- "A domain-specific benchmark for converting food bioactivity literature into structured evidence"

This fallback preserves the paper even if the database scale is modest.

---

## 3. Experiment Plan

## 3.1 Research Questions

RQ1:
- Can tea functional activity literature be normalized into a structured evidence resource with acceptable curation reliability?

RQ2:
- Does explicit evidence grading materially improve interpretability over ordinary literature aggregation?

RQ3:
- Does adding processing/composition context improve the usefulness of the resource for cross-study comparison?

RQ4:
- Can the structured database be mapped into a graph-ready representation for microbiome mechanism modeling?

## 3.2 Data Acquisition Pipeline

### Stage A. Corpus construction

Input sources:
- Seed set from 2022-2026 core reviews already identified
- Primary studies cited by these reviews
- PubMed expansion using queries combining:
  - tea type
  - extract/component
  - activity endpoint
  - microbiota / metabolism / inflammation keywords

Deliverables:
- Search log
- Inclusion/exclusion criteria
- Deduplicated corpus
- PRISMA-style flow summary

### Stage B. Screening

Screening tiers:
1. Title screening
2. Abstract screening
3. Full-text targeted extraction where needed

Include:
- Tea, tea extract, tea component studies
- Functional activity claims
- Clear model system and endpoint information

Exclude:
- Pure agronomy papers without functional endpoint
- Pure sensory studies with no biological activity
- Non-tea mixed botanical systems unless tea-specific effect is separable

### Stage C. Annotation gold set

Gold set target:
- 100-200 papers

Annotation units:
- Paper-level metadata
- Evidence records
- Tea sample / extract / component mentions
- Activity claim
- Study type
- Dose/exposure
- Processing and extraction context where available
- Mechanism statements where available

### Stage D. Semi-automatic extraction

Pipeline:
1. Rule-based paper triage
2. Dictionary normalization
3. Template-based extraction
4. Ontology-constrained LLM extraction
5. Human validation

### Stage E. Database assembly

Build:
- core evidence table
- tea sample table
- component/extract table
- process/extraction context table
- activity endpoint table
- study model/evidence table
- provenance table

### Stage F. KG mapping

For phase 1:
- not full graph population
- only define mapping rules and a pilot graph subset

For phase 3:
- instantiate microbiome triples for selected domain subset

## 3.3 Schema Design

### Core entities

1. `Paper`
2. `TeaMaterial`
3. `TeaType`
4. `Cultivar`
5. `Origin`
6. `ProcessingStep`
7. `ExtractionMethod`
8. `Extract`
9. `CompoundGroup`
10. `Compound`
11. `BioactivityCategory`
12. `Endpoint`
13. `Mechanism`
14. `ModelSystem`
15. `StudyType`
16. `EvidenceLevel`
17. `DoseExposure`
18. `MicrobiotaTaxon`
19. `MicrobialMetabolite`
20. `HostPhenotype`

### Core relations

Phase 1 database-ready relations:
- `Paper reports EvidenceRecord`
- `EvidenceRecord studies TeaMaterial`
- `TeaMaterial belongs_to TeaType`
- `TeaMaterial processed_by ProcessingStep`
- `TeaMaterial extracted_by ExtractionMethod`
- `Extract enriched_in CompoundGroup`
- `CompoundGroup associated_with BioactivityCategory`
- `EvidenceRecord evaluated_in ModelSystem`
- `EvidenceRecord has_evidence_level EvidenceLevel`
- `EvidenceRecord has_dose DoseExposure`
- `EvidenceRecord supports_or_refutes BioactivityCategory`

Phase 2 processing-aware relations:
- `ProcessingStep alters CompoundGroup`
- `ExtractionMethod enriches CompoundGroup`
- `ProcessingContext modifies EvidencePattern`

Phase 3 microbiome KG relations:
- `CompoundGroup modulates MicrobiotaTaxon`
- `MicrobiotaTaxon produces_or_associates MicrobialMetabolite`
- `MicrobialMetabolite affects HostPhenotype`
- `CompoundGroup acts_via Mechanism`

### Minimal schema for paper 1

Mandatory fields:
- PMID/DOI
- tea type
- extract/component group
- activity category
- specific endpoint
- study type
- evidence level
- model system
- dose or exposure
- direction of effect

Optional but recommended:
- processing step
- extraction method
- cultivar/origin
- mechanism note
- microbiota entity

## 3.4 Comparisons

### Comparison C1. Narrative review baseline

Question:
- How easily can a researcher answer a structured question from ordinary review-style literature reading versus our database?

Tasks:
- Find strongest evidence for anti-inflammatory effects of green tea catechins
- Compare microbiota evidence for fermented vs non-fermented tea
- Identify which claims have human support versus only in vitro support

Metrics:
- answer time
- number of source papers needed
- completeness
- consistency across users

### Comparison C2. Unstructured spreadsheet baseline

Question:
- Does evidence grading plus schema normalization outperform simple spreadsheet aggregation?

Metrics:
- ambiguity count
- unresolved label count
- inability to answer cross-study questions

### Comparison C3. TRSRD-style reference positioning

Question:
- What new capability is gained by shifting from a tea-risk literature graph to a tea-benefit evidence resource?

Show:
- domain difference
- relation granularity difference
- evidence stratification difference

## 3.5 Ablations

### A1. Without evidence grading

Claim tested:
- Evidence grading is necessary for meaningful interpretation.

Expected result:
- Mixed-quality claims become indistinguishable and user trust decreases.

### A2. Without processing/context fields

Claim tested:
- Processing/composition context improves cross-study explanation.

Expected result:
- Activity differences remain uninterpretable when tea categories or extraction processes differ.

### A3. Broad component groups vs fine-grained compounds

Claim tested:
- A two-level chemical representation is more robust than immediately forcing fine granularity.

Expected result:
- Broad groups improve coverage and consistency in phase 1, while preserving optional fine mapping later.

### A4. Manual-only vs semi-automatic extraction

Claim tested:
- Semi-automatic extraction reduces labor while preserving acceptable quality.

Expected result:
- Semi-automatic workflow improves throughput with acceptable precision after normalization constraints.

### A5. Database records vs graph-ready transformation

Claim tested:
- The phase-1 schema can be transformed into graph-native triples without redesign.

Expected result:
- Pilot microbiome subgraph can be generated directly from structured records with modest manual adjustment.

## 3.6 Stress Tests

Stress test 1:
- Endpoint heterogeneity stress test
  - Use multiple anti-inflammatory markers from different study systems and test whether the hierarchy still supports meaningful grouping.

Stress test 2:
- Cross-evidence conflict stress test
  - Cases where in vitro positive claims coexist with weak or absent animal/human support.

Stress test 3:
- Processing terminology stress test
  - Map variable processing labels into normalized processing stages without losing key distinctions.

## 3.7 Case Studies

Case study 1:
- Green vs oolong vs black tea for antioxidant and anti-inflammatory evidence

Case study 2:
- Whole extract vs catechin-dominant systems in microbiota modulation

Case study 3:
- Fermented tea subset as the bridge from database to microbiome mechanism graph

## 3.8 Claim-to-Experiment Mapping

| Claim | Needed experiment / analysis |
|------|------------------------------|
| We normalize tea activity literature reliably | Inter-curator agreement + extraction precision |
| Evidence grading improves interpretability | A1 comparison and user question benchmark |
| Processing fields add explanatory value | A2 ablation + case study 1 |
| The schema is graph-extensible | A5 graph-ready transformation + case study 3 |

---

## 4. Figure Design

## 4.1 Figure 1 Teaser

Concept:
- One visual showing the same tea activity query answered at three layers:
  - evidence-graded database
  - processing-aware extension
  - microbiome mechanism graph

Message:
- This is not just a review table; it is a progressive knowledge infrastructure.

## 4.2 Figure 2 Pipeline Figure

Pipeline blocks:
1. Literature retrieval
2. Screening and corpus building
3. Annotation and normalization
4. Structured evidence schema
5. Database release
6. Processing-aware extension
7. Microbiome KG mapping

Novelty highlight:
- evidence grading layer
- processing-aware extension layer
- graph mapping layer

## 4.3 Figure 3 Schema Diagram

Show:
- core entities
- key attributes
- relation families
- which relations belong to phase 1, 2, and 3

## 4.4 Figure 4 Utility Figure

Show:
- example research queries answered by the database
- side-by-side comparison with unstructured literature search

## 4.5 Figure 5 Case Study Figure

Recommended:
- tea type vs activity evidence heatmap
- optional microbiome subgraph inset

---

## 5. Section Plan

### Introduction

Paragraph order:
1. Tea is heavily studied for multiple functional activities.
2. Existing evidence is fragmented and difficult to compare.
3. Current tea resources do not solve functional evidence integration.
4. We propose an evidence-graded tea activity resource with process-aware and graph-ready design.
5. Contributions list.

### Methods

Suggested subsections:
1. Corpus retrieval and screening
2. Annotation protocol
3. Schema and normalization design
4. Evidence grading framework
5. Semi-automatic extraction pipeline
6. Database construction
7. Processing-aware extension
8. KG mapping strategy

### Experiments / Evaluation

Suggested subsections:
1. Corpus statistics
2. Curation quality
3. Extraction performance
4. Utility benchmark
5. Ablations
6. Case studies
7. Graph-extension pilot

---

## 6. Timeline

## Week 1

- finalize paper story and narrow claim
- freeze phase-1 schema
- write annotation guideline v1
- finalize search strategy and inclusion/exclusion criteria
- start gold-set paper collection

## Week 2

- annotate first 30-50 papers
- refine schema and dictionaries
- implement semi-automatic extraction prototype
- draw first pipeline figure and schema figure
- draft Introduction outline and Method outline

## Week 3

- expand to 100-200 gold-set papers
- compute agreement and extraction precision
- assemble database release candidate
- run utility comparisons and ablations A1-A4
- draft Introduction + Methods full first draft

## Week 4

- run case studies and A5 graph mapping pilot
- finalize figures and tables
- write Experiments, Related Work, Abstract
- revise novelty framing against mock rejection letter
- polish title and contribution statements

---

## 7. Recommended Paper Framing

Most defensible title family:
- Evidence-Graded Tea Functional Activity Database
- A Structured Resource for Tea Functional Activity Evidence and Influencing Factors

Avoid in paper 1:
- claiming full tea KG completion
- claiming complete automation
- claiming definitive biological truth across all tea activities

Recommended contribution framing:
- resource paper with methodological rigor
- domain-specific evidence modeling framework
- extension-ready substrate for atlas and KG research
