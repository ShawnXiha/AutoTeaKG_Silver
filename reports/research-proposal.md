# Research Proposal

Title: Evidence-Graded Tea Functional Activity Database with Expansion Paths to Processing Atlas and Mechanism Graph

Date: 2026-03-31

## 1. Background

Tea, tea extracts, and tea-derived components are associated with a wide range of reported functional activities, including antioxidant, anti-inflammatory, metabolic, cardiovascular, neuroprotective, and gut microbiota-related effects. However, this literature is fragmented across different tea categories, extraction methods, study systems, and endpoint definitions. The same claimed activity may be supported by cell assays, animal studies, randomized trials, or cohort/meta-analysis evidence, yet these evidence types are rarely made directly comparable.

The core problem is therefore not lack of studies, but lack of structure. Existing tea-focused resources are concentrated in genomics, transcriptomics, or tea risk substances, while a resource centered on functional activity claims, influencing factors, and evidence strength is still missing. A reliable first step is to build an evidence-graded database that standardizes tea type, extract/component, activity class, model system, dose/exposure, and evidence level, while preserving traceability to source literature.

## 2. Related Work

Recent reviews synthesize tea bioactive compounds and mechanisms, processing effects, gut microbiota modulation, and bioavailability constraints, showing that the domain is mature enough for structured integration. Key examples include the updated tea bioactive compounds review in 2024, processing and extraction reviews in 2023, gut microbiota-oriented reviews in 2024, and bioavailability-focused synthesis in 2025.

On the resource side, tea-specific databases do exist, but they do not target functional activity evidence integration. TRSRD demonstrates that tea literature can be organized using NLP and graph techniques, but its focus is risky substances rather than beneficial activity. TeaPVs and TeaNekT show that tea-specific data infrastructure is viable, but they serve genomic and transcriptomic questions. Outside tea, natural-product KGs and databases such as NPASS and pharmacokinetic natural product-drug interaction KG work provide methodological inspiration for ontology design, evidence representation, and downstream graph expansion.

The gap is therefore clear: there is no evidence-graded tea functional activity database that systematically links claims to evidence strength and major influencing factors while remaining extensible to graph reasoning.

## 3. Proposed Method

### 3.1 Core idea

Build a first-release structured database for tea functional activity evidence, then design the schema so it can later expand into a processing atlas and mechanistic knowledge graph.

### 3.2 Scope of phase 1

Tea classes:
- Green tea
- Oolong tea
- Black tea
- Fermented/post-fermented tea where evidence is strong enough

Component/extract groups:
- Catechins
- Theaflavins
- Theanine
- Caffeine
- Tea polysaccharides
- Whole extracts

Activity families:
- Antioxidant
- Anti-inflammatory
- Gut microbiota modulation
- Metabolic improvement or anti-obesity

Evidence levels:
- In vitro
- Animal
- RCT
- Cohort
- Meta-analysis

### 3.3 Data model

Each evidence record will include:
- Source article metadata
- Tea type
- Extract or component
- Processing context if available
- Extraction method if available
- Bioactivity class
- Specific endpoint
- Model system
- Dose or exposure information
- Direction of effect
- Evidence level
- Confidence or curation quality tag

### 3.4 Data acquisition pipeline

1. Build a seed corpus from 2022-2026 core reviews and their cited primary studies.
2. Expand via PubMed and Crossref searches using tea type, component, and activity keywords.
3. Manually curate a gold-standard set of 100-200 papers.
4. Define normalization dictionaries for tea classes, component names, activity families, and study types.
5. Apply semi-automatic extraction using template rules and ontology-constrained LLM support.
6. Perform human validation on a fixed sample from each category.

### 3.5 Technical contributions

Contribution 1:
- A tea-specific evidence schema that jointly represents functional activity, influencing factors, and evidence level.

Contribution 2:
- A curated database that makes tea activity claims directly comparable across study types and activity classes.

Contribution 3:
- An expansion-ready architecture that supports later conversion into a processing atlas and graph resource.

## 4. Experiment Plan

### 4.1 Dataset construction

Gold set:
- 100-200 manually curated studies

Phase 1 release target:
- 400-800 structured evidence records from 150-300 papers

### 4.2 Baselines and comparisons

Compare against:
- Narrative review style retrieval
- Simple spreadsheet-based curation without evidence normalization
- TRSRD-style literature organization as a reference for tea-domain database framing

### 4.3 Evaluation metrics

For data quality:
- Inter-curator agreement on entity normalization and evidence labeling
- Precision of semi-automatic extraction on held-out manually curated records
- Coverage of major tea classes, components, and activity families

For utility:
- Time-to-answer benchmark for predefined research questions
- Ability to support cross-study comparison that is difficult with raw literature search
- Expert usefulness scoring for review writing and project design tasks

### 4.4 Case studies

Case study 1:
- Compare antioxidant and anti-inflammatory evidence across green, oolong, and black tea

Case study 2:
- Compare microbiota-related evidence across whole extracts versus isolated catechin-enriched systems

Case study 3:
- Trace whether high-confidence human evidence aligns with dominant in vitro and animal claims

### 4.5 Ablations

- With vs without processing context
- With vs without evidence-level scoring
- Manual-only curation vs semi-automatic pipeline
- Broad component labels vs fine-grained compound grouping

## 5. Expected Results

Expected quantitative outcomes:
- A first release covering at least 4 activity families, 4-6 component groups, and 4-5 evidence levels
- Semi-automatic extraction precision above 0.80 on normalized core fields after ontology constraints
- Inter-curator agreement above 0.85 on evidence level and study type labels

Expected qualitative outcomes:
- Researchers can quickly identify which tea activity claims are supported only by in vitro studies and which have stronger in vivo or human evidence.
- The resource exposes major evidence gaps, such as activity areas dominated by low-translation preclinical claims.
- The schema demonstrates a credible path toward phase-2 graph expansion.

## 6. Risks and Mitigations

Risk 1:
- Endpoint heterogeneity makes cross-study comparison difficult.

Mitigation:
- Use a two-level endpoint design with broad activity families plus specific measured endpoints.

Risk 2:
- Component naming is inconsistent across studies.

Mitigation:
- Normalize to component groups in phase 1 and preserve raw labels for later fine-grained mapping.

Risk 3:
- The project becomes a descriptive database with limited novelty.

Mitigation:
- Emphasize evidence grading, cross-study comparability, and explicit modeling of influencing factors.

Risk 4:
- Scope creep into a full knowledge graph too early.

Mitigation:
- Freeze phase-1 scope to evidence database deliverables and defer graph-native features to phase 2.

Risk 5:
- Human evidence is sparse or low resolution for some activity classes.

Mitigation:
- Treat this as an output finding and encode evidence gaps explicitly rather than forcing false completeness.

## Practical Extension

Recommended roadmap after the first paper:

1. Add processing and extraction context fields to evolve into a processing-bioactivity atlas.
2. Build a microbiome specialty graph as the first graph-native module.
3. Add evidence-aware link prediction only after the curated substrate reaches sufficient density.
