# Paper Structure Draft v1

Title candidate:
- Evidence-Graded Tea Functional Activity Database with Processing-Aware Context and a Gut-Microbiome Mechanism Graph Prototype

Date: 2026-03-31

## 1. Paper Positioning

This paper should be framed as a **resource paper with mechanistic demonstration**, not as a pure database paper and not as a full KG paper.

The core logic is:
1. tea functional activity evidence is fragmented
2. we build an evidence-graded structured resource to normalize it
3. we show that adding processing-aware context improves interpretability
4. we demonstrate graph value through a C06 gut-microbiome mechanism prototype

This keeps the claim narrow enough for phase 1, while still showing a forward-looking methodological contribution.

## 2. One-Sentence Paper Claim

We present a structured tea functional activity resource that normalizes heterogeneous evidence across tea types, components, study systems, and evidence levels, and show that the same resource can be extended into processing-aware analysis and a gut-microbiome mechanism graph with interpretable multi-hop biological paths.

## 3. Introduction Draft Structure

### Paragraph 1. Why tea functional activity research matters

Tea, tea extracts, and tea-derived components are widely studied for antioxidant, anti-inflammatory, metabolic, neuroprotective, cardiovascular, and gut microbiota-related effects. However, the literature has expanded unevenly across tea categories, component classes, model systems, and outcome definitions, making it difficult to compare findings across studies or identify which claims are most strongly supported.

### Paragraph 2. What is missing in the current literature

Existing narrative reviews summarize tea bioactive compounds, processing effects, microbiota interactions, and bioavailability constraints, but they do not convert this knowledge into a machine-readable evidence layer. Likewise, tea-specific databases have focused on genomics, transcriptomics, or risk substances rather than functional activity evidence. As a result, researchers still lack a unified resource that can answer simple but important questions such as which activities are supported mainly by in vitro studies, which have human evidence, and how processing and microbiota-related mechanisms modify interpretation.

### Paragraph 3. The key challenge

The main bottleneck is not lack of literature, but lack of evidence structure. Tea activity studies differ in tea type, extract/component definition, processing context, study design, endpoint choice, and evidence strength. Without a normalized representation, strong and weak claims are mixed together, and mechanistic paths spanning microbiota, metabolites, host signaling, and phenotype are difficult to reconstruct.

### Paragraph 4. Our insight

We argue that a database-first evidence model is the right first step. Instead of attempting to build a broad tea knowledge graph from the start, we first normalize the literature into evidence records that preserve tea type, component group, activity category, study type, evidence level, dose/exposure, and source provenance. This creates a reliable substrate that can later absorb processing-aware context and graph-native mechanistic relationships.

### Paragraph 5. What we built

Based on this idea, we construct an evidence-graded tea functional activity resource, extend it with processing- and extraction-aware fields, and use its microbiota-related subset to build a gut-microbiome mechanism graph prototype. The resulting graph captures interpretable multi-hop biological paths linking tea components to microbiota changes, microbial metabolites, host signaling processes, and phenotypic outcomes.

### Paragraph 6. Contributions

Suggested contribution list:

1. We define a tea-specific evidence schema that makes functional activity claims comparable across study types, tea materials, and component groups.
2. We curate a structured resource covering core tea activity families with explicit evidence-level representation and provenance.
3. We add processing-aware context that prepares the resource for phase-2 analysis of composition and activity shifts.
4. We demonstrate that the same resource can be transformed into a gut-microbiome mechanism graph and recover three biologically interpretable multi-hop storylines.

## 4. Results Draft Structure

Recommended Results section order:

### 4.1 Overview of the evidence-graded tea activity resource

Purpose:
- establish what the dataset contains
- show why the resource is needed before the graph story starts

What to show:
- paper count
- evidence record count
- activity-category distribution
- evidence-level distribution
- human vs preclinical vs review-derived composition

Main message:
- the corpus is broad enough to justify structured modeling, but heterogeneous enough that ordinary review-style synthesis is insufficient

### 4.2 Evidence grading improves interpretation of tea activity claims

Purpose:
- justify C04 as a real contribution, not bookkeeping

What to show:
- human evidence subset
- anti-inflammatory records with mixed/no_clear_effect outcomes
- examples where review or preclinical enthusiasm exceeds direct human support

Main message:
- evidence-level normalization prevents over-reading weak or indirect claims

### 4.3 Processing-aware context reveals why activity comparisons are difficult

Purpose:
- justify the C01 extension

What to show:
- processing/extraction-context subset
- examples where tea category, processing route, or extraction method changes interpretation
- one small table or figure illustrating why similar activity labels can mask process-dependent chemistry differences

Main message:
- processing-aware context is required if the resource is to support meaningful comparison instead of flat claim aggregation

### 4.4 A gut-microbiome graph prototype recovers a microbiota-barrier-obesity mechanism path

Use:
- Story A
- Figure C06-1

Main message:
- the graph can encode a microbiota-metabolite-barrier-host route centered on tea polyphenols and obesity-related phenotypes

Paragraph logic:
- introduce the graph subset
- describe tea polyphenols -> Blautia/Faecalibaculum/Colidextribacter -> SCFAs
- describe barrier and inflammation mechanism layer
- end on obesity phenotype interpretation

### 4.5 A gut-brain-axis subgraph links oolong tea polyphenols to cognition-related outcomes

Use:
- Story B
- Figure C06-2

Main message:
- the same graph formalism extends beyond metabolic disease into cognition and neuroinflammation

Paragraph logic:
- introduce gut-brain path
- describe taxa and metabolite/signal nodes
- describe microglial and synaptic plasticity mechanism layer
- end on cognition phenotype

### 4.6 Tea polysaccharides form a multi-branch microbiota-mediated mechanism family

Use:
- Story C
- Figure C06-3

Main message:
- one tea component family can support multiple microbiota-mediated host programs, which is exactly the type of pattern the graph is designed to reveal

Paragraph logic:
- present branch 1: butyrate / thermogenesis / adipose browning
- present branch 2: bile-acid remodeling / FXR-FGF15-FGFR4-ASBT / NAFLD
- present branch 3: Lactobacillus / NF-kB / oxidative-neural protection
- conclude that the graph exposes a family of related mechanisms rather than isolated pairs

### 4.7 Limitations of the current graph and implications for future expansion

Purpose:
- control reviewer expectations

What to say:
- some nodes still represent grouped taxa rather than fully normalized taxon nodes
- human mechanistic evidence is still sparse
- review-derived evidence remains in the provenance layer and should not be interpreted as direct causal support
- full C06 construction requires another round of full-text refinement and entity normalization

## 5. Suggested Section Headers

### Abstract

- Background
- Methods
- Results
- Conclusions

### Main sections

1. Introduction
2. Materials and Methods
3. Results
4. Discussion
5. Conclusion

### Recommended Results subsections

1. Construction of an evidence-graded tea functional activity resource
2. Evidence-level normalization clarifies the strength of tea activity claims
3. Processing-aware context improves the interpretability of structured tea evidence
4. A graph prototype reveals a microbiota-barrier-obesity route for tea polyphenols
5. A gut-brain-axis subgraph links oolong tea polyphenols to cognition-related outcomes
6. Tea polysaccharides form a multi-branch microbiota-mediated mechanism family
7. Limitations and future refinement of the C06 graph

## 6. Figure-to-Section Mapping

| Figure | Section | Role |
|-------|---------|------|
| Resource overview figure | 4.1 | establishes scope |
| Evidence-level / human-evidence figure | 4.2 | proves grading value |
| Processing-aware context figure | 4.3 | justifies C01 extension |
| Figure C06-1 | 4.4 | main graph story |
| Figure C06-2 | 4.5 | specialty graph story |
| Figure C06-3 | 4.6 | strongest graph-family story |

## 7. Discussion Draft Structure

### Paragraph 1

Summarize the paper as a transition from fragmented tea literature to a structured resource with mechanistic graph capability.

### Paragraph 2

Argue that evidence grading is essential because tea activity claims are often discussed without explicit distinction between preclinical and human support.

### Paragraph 3

Argue that processing-aware context is not optional if tea resources are expected to support realistic interpretation of component-activity relations.

### Paragraph 4

Highlight the graph result: tea-microbiota mechanisms can be represented as multi-hop biological programs, not just pairwise associations.

### Paragraph 5

State limitations frankly:
- grouped taxa
- sparse human mechanism data
- incomplete full-text refinement
- no causal weighting yet

### Paragraph 6

Future work:
- refine taxon-level normalization
- expand graph coverage
- link C04/C01/C06 into a single evolving tea knowledge infrastructure

## 8. Recommended Writing Order

1. Write Results 4.4, 4.5, 4.6 first because the graph stories are now the strongest narrative element.
2. Then write Results 4.1 to 4.3 to establish why the graph matters.
3. Then write Introduction from the narrow claim upward.
4. Write Discussion last after deciding how strongly to frame the graph contribution.

## 9. Narrow Claim Reminder

Do not frame the paper as:
- a complete tea knowledge graph
- a complete causal model of tea microbiome biology
- a final normalized microbiota ontology

Frame it as:
- an evidence-graded tea activity resource
- a processing-aware extension-ready schema
- a refined gut-microbiome graph prototype that already recovers interpretable mechanism stories
