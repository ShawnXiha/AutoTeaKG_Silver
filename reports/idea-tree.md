# Idea Tree: Tea Functional Bioactivity Database / KG

Date: 2026-03-31
Seed direction: Build a structured knowledge infrastructure for tea, tea extracts, and tea components, linking bioactivities with influencing factors such as cultivar, origin, processing, extraction, bioavailability, and gut microbiota.

No prior ideation memory was available at `/memory/ideation-memory.md`, so no memory-based pruning was applied.

## Level 0: Seed

Root idea:
- Create a tea bioactivity knowledge resource that goes beyond narrative review and supports structured comparison, evidence tracing, and new hypothesis generation.

## Level 1: Technique Variants

### T1. Evidence-Curated Atlas
A high-quality structured database centered on manual-plus-semi-automatic curation. The priority is reliability, normalized schema, and direct usability for review writing and downstream modeling.

### T2. Knowledge Graph and Reasoning Layer
A graph-native resource that explicitly models multi-hop relations among tea type, compound, process, mechanism, model system, and outcome. The priority is explainable path discovery and graph querying.

### T3. Predictive and Generative Discovery Layer
A machine-assisted platform that uses the structured tea resource to predict missing links, suggest experiments, and prioritize promising tea-process-compound-activity combinations. The priority is hypothesis generation rather than only data organization.

## Level 2: Domain Adaptations

### T1-D1. Processing-to-Bioactivity
Focus on how processing and extraction reshape composition and downstream bioactivity. This domain is tightly aligned with current literature density and offers a clean first scope.

### T1-D2. Evidence-Graded Health Claims
Focus on health outcomes and evidence levels across in vitro, animal, RCT, cohort, and meta-analysis studies. This domain is more translational and useful for industry and regulatory-style evidence review.

### T2-D1. Gut Microbiome Mechanisms
Focus on tea component to microbiota to metabolite to phenotype chains. This domain is mechanistically rich and growing rapidly in 2024-2025 literature.

### T2-D2. Multi-Scale Tea KG
Focus on a broad tea bioactivity KG spanning cultivar, origin, processing, chemistry, bioavailability, mechanisms, and outcomes. This domain maximizes novelty but raises integration difficulty.

### T3-D1. Link Prediction for Missing Evidence
Use graph and tabular features to predict untested or under-studied edges, such as which processing changes may enrich compounds linked to target activities.

### T3-D2. LLM-Assisted Evidence Extraction and Proposal Generation
Use LLM plus ontology constraints to extract claims from literature and convert the structured graph into experiment-ready proposals.

## Level 3: Formulation Variants (15 leaf candidates)

### C01. Tea Processing-Bioactivity Atlas
Build a curated atlas connecting tea type, processing step, extraction method, major compound classes, and four outcome families: antioxidant, anti-inflammatory, microbiota modulation, and metabolic improvement. Use 100-200 gold-standard papers and normalized evidence tables as the first release.

### C02. Green-Oolong-Black Comparative Atlas
Restrict the atlas to green, oolong, and black tea, and quantify how processing intensity changes catechins, theaflavins, theanine, caffeine, and polysaccharides alongside reported bioactivities. The key claim is a cleaner comparative benchmark rather than a broad database.

### C03. Extraction Technology Outcome Atlas
Build a database focused on extraction technologies such as ultrasound, microwave, supercritical CO2, and pressurized liquid extraction, linking process parameters to yield, composition shift, and measured activity endpoints. This idea is highly practical for food engineering and formulation research.

### C04. Evidence-Graded Tea Health Claims Database
Create a structured evidence database for claimed tea health effects with explicit evidence level, model system, dose/exposure, and consistency tags. The main deliverable is a health-claim reliability layer rather than chemistry detail.

### C05. Tea Human Evidence Core
Build a human-first tea evidence resource centered on RCTs, cohorts, and meta-analyses, with links back to tea types and broad component groups. The novelty is not scale but a clinically interpretable bridge between tea science and public health claims.

### C06. Tea Microbiome Mechanism Graph
Build a graph for tea component -> microbiota taxa -> microbial metabolites -> barrier/inflammation -> host phenotype relations, with explicit evidence provenance and species tags. The graph is scoped to obesity, metabolic syndrome, and cognition.

### C07. Fermented Tea Mechanism Graph
Focus only on fermented teas and post-fermented tea products, modeling fermentation type, composition shifts, microbiome modulation, and metabolic outcomes. The constrained scope may produce a cleaner, more novel benchmark graph.

### C08. TeaBioAct-KG
Build a general tea functional bioactivity KG spanning tea type, cultivar, origin, processing, extract, compound, mechanism, model, activity, and evidence level. The main contribution is the ontology and the graph schema for multi-hop reasoning.

### C09. Tea Ontology + KG Benchmark
Design a tea domain ontology and create a benchmark dataset for entity recognition, relation extraction, and graph population from tea literature. The novelty is methodological and would support many later database releases.

### C10. Tea Compound-Mechanism Path Explorer
Build a graph optimized for path exploration from compounds to mechanisms and phenotypes, prioritizing explainable mechanistic chains rather than exhaustive coverage. It is narrower than a full KG but more immediately useful for discovery.

### C11. Missing-Link Predictor for Tea Bioactivity
Train models to predict plausible but under-studied links between process settings, component shifts, and bioactivity outcomes using structured literature-derived features. The contribution is computational prioritization of new experiments.

### C12. Processing-to-Composition Recommender
Build a recommender that suggests processing or extraction settings likely to enrich target compound groups associated with selected activities. It translates structured tea science into actionable design suggestions.

### C13. Evidence-Aware Link Prediction KG
Use a graph model that incorporates evidence level and study type so predictions do not overfit noisy in vitro claims. This idea directly addresses the key controversy that strong in vitro effects often do not translate in vivo.

### C14. LLM + Ontology Tea Literature Extraction Pipeline
Build a constrained extraction pipeline that maps abstracts/full texts into standardized entities and relations for tea bioactivity. The key research question is whether ontology-constrained LLM extraction can reach acceptable precision for tea-specific knowledge graph construction.

### C15. Tea Research Copilot for Hypothesis and Proposal Generation
Use the structured database/KG plus LLM retrieval to produce ranked experiment ideas, literature-backed rationales, and proposal drafts for tea functional activity research. The novelty lies in turning the knowledge resource into a working scientific assistant.

## Pruning Notes

No leaf was pruned as fundamentally infeasible. The highest-risk leaves are:
- C08 due to breadth
- C11/C13 due to data sparsity and label quality
- C15 due to evaluation difficulty

They remain in the tournament because risk is not the same as infeasibility.
