# C06 Paper-Ready Story Pack v1

Date: 2026-03-31
Based on:
- `data/c06_kg_prototype_v2`
- refined evidence records in `templates/evidence_records_expanded_batch_v1_2026-03-31.csv`

## 1. Positioning

The current C06 prototype is now strong enough to support a paper-ready mechanistic narrative, not just a resource description.

The best strategy is not to present the graph as a giant undifferentiated network.  
Instead, present 3 concrete mechanism stories that demonstrate why a tea microbiome KG is scientifically useful.

Recommended framing:

> The value of the graph is that it converts scattered tea-microbiome findings into reusable mechanistic paths linking component groups, microbial changes, microbial metabolites, host signaling, and phenotypes.

## 2. Three Main Storylines

### Story A. Tea Polyphenols -> SCFAs / Barrier -> Inflammation -> Obesity

#### Core evidence anchor
- `PMID_39574401_R1`
- `PMID_39574401_R2`

#### Mechanistic path

`Tea polyphenols`
-> `Blautia / Faecalibaculum / Colidextribacter`
-> `SCFAs`
-> `G protein-coupled receptor activation / histone deacetylase inhibition / tight junction enhancement / barrier protection`
-> `reduced inflammation and obesity-related phenotype`

#### Why this story is strong

1. It is a clean microbiota-metabolite-barrier-host phenotype chain.
2. It directly supports the claim that the graph can encode multi-hop biological causality.
3. It is aligned with the most mature tea-microbiome-obesity literature pattern.

#### What to claim

The graph captures a mechanistic route by which tea polyphenols may reduce obesity-related phenotypes through microbiota remodeling, SCFA-linked signaling, barrier preservation, and inflammatory suppression.

#### What not to overclaim

Do not claim causal certainty beyond the reported animal model.  
Keep wording at the level of “supports a mechanistic path” or “captures reported evidence for”.

#### Figure sketch

Left to right 5-column layout:
- Column 1: component group
- Column 2: microbiota taxa
- Column 3: metabolite
- Column 4: host signaling / barrier mechanisms
- Column 5: phenotype

Use color:
- blue for component
- green for microbiota
- orange for metabolites
- red for host phenotype

#### Figure caption draft

**Figure X. A graph-derived mechanistic path linking tea polyphenols to obesity-related phenotypes through microbiota and barrier regulation.**  
The C06 prototype captures evidence that tea polyphenols modulate taxa including Blautia and Faecalibaculum, alter SCFA-associated signaling, enhance tight-junction and barrier-related mechanisms, and suppress inflammatory processes associated with obesity-related phenotypes in high-fat-diet mouse models.

---

### Story B. Oolong Tea Polyphenols -> Gut-Brain Axis -> Synaptic Plasticity -> Cognition

#### Core evidence anchor
- `PMID_38745351_R1`

#### Mechanistic path

`Oolong tea polyphenols`
-> `Muribaculaceae / Clostridia_UCG-014 / Desulfovibrio`
-> `LPS / SCFAs / glutamate`
-> `microglia activation reduction / intestinal barrier protection / BDNF-PSD95-SYN synaptic plasticity support`
-> `cognitive impairment phenotype`

#### Why this story is strong

1. It expands the graph beyond metabolic disease into gut-brain communication.
2. It includes both inflammatory and synaptic-plasticity layers.
3. It shows that the graph supports domain transfer from obesity to cognition while using the same graph logic.

#### What to claim

The graph supports a gut-brain-axis mechanism in which tea polyphenols link microbiota and microbial-metabolite changes to neuroinflammatory and synaptic-plasticity outcomes relevant to cognition.

#### What not to overclaim

Do not imply this is already a clinically validated human mechanism.  
State clearly that this path is anchored in a preclinical circadian-disruption model.

#### Figure sketch

Use a vertical layered layout:
- top: tea component
- second: microbiota taxa
- third: metabolites and gut-derived signals
- fourth: brain mechanisms
- bottom: cognition phenotype

Add a side annotation:
- `preclinical in vivo`

#### Figure caption draft

**Figure Y. A gut-brain-axis subgraph linking oolong tea polyphenols to cognition-related outcomes.**  
The refined C06 prototype encodes reported relationships among oolong tea polyphenols, microbiota shifts involving Muribaculaceae and related taxa, metabolite and signal changes including SCFAs, LPS, and glutamate, and downstream neuroprotective mechanisms involving reduced microglial activation and improved synaptic plasticity markers.

---

### Story C. Tea Polysaccharides -> Microbiota / Butyrate or Bile Acids -> Thermogenesis / Liver Phenotype / Oxidative-Neural Protection

#### Core evidence anchors
- `PMID_40957830_R1/R2`
- `PMID_39153277_R1/R2`
- `PMID_36449351_R1/R2`
- `PMID_39479919_R1/R2`

#### Why this should be one story family

This is the most interesting graph-native pattern in the current dataset:
- one component family: tea polysaccharides
- multiple host outcome branches:
  - obesity / adipose browning
  - NAFLD / bile acid metabolism
  - oxidative stress and microglial damage

Instead of presenting them as separate disconnected observations, the paper should present them as a *polysaccharide-centered mechanism family*.

#### Subpath C1. Polysaccharides -> Bifidobacterium -> Butyrate -> Thermogenesis / Browning

`Tea polysaccharides`
-> `Bifidobacterium species`
-> `butyrate`
-> `PGC-1alpha/UCP1 thermogenic programming`
-> `adipose browning / obesity phenotype`

Anchors:
- `PMID_40957830_R1`
- `PMID_40957830_R2`

#### Subpath C2. Polysaccharides -> Microbiota remodeling -> Bile-acid pathway -> NAFLD

`Yellow tea polysaccharides`
-> `Muribaculaceae / Pseudomonas / Clostridiales / Delftia / Dubosiella / Romboutsia ...`
-> `conjugated bile acids / non-12OH bile acids`
-> `FXR-FGF15-FGFR4-ASBT suppression / FXR-SHP pathway modulation / alternative bile-acid synthesis`
-> `NAFLD phenotype`

Anchors:
- `PMID_39153277_R1`
- `PMID_39153277_R2`

#### Subpath C3. Polysaccharides -> Firmicutes/Bacteroidota + Lactobacillus -> NF-kB / antioxidant defense -> oxidative-neural protection

`Tea flower polysaccharides`
-> `Firmicutes/Bacteroidota ratio / Lactobacillus`
-> `NF-kB suppression / antioxidant enzyme restoration`
-> `oxidative damage phenotype / microglial oxidative damage`

Anchors:
- `PMID_39479919_R1`
- `PMID_39479919_R2`

#### What to claim

Tea polysaccharides are not a single-function branch in the graph.  
They form a mechanism-rich family linking gut microbiota remodeling to multiple downstream host programs, including thermogenesis, bile-acid regulation, oxidative defense, and neuroinflammation control.

#### What not to overclaim

Do not claim a single unified polysaccharide mechanism.  
Claim instead that the graph reveals a reusable mechanistic pattern family centered on microbiota-mediated host regulation.

#### Figure sketch

Center the figure on `tea polysaccharides` with three outgoing branches:
- obesity / browning branch
- NAFLD / bile-acid branch
- oxidative-neural branch

This should be the most visually distinctive figure in the set.

#### Figure caption draft

**Figure Z. Tea polysaccharides form a multi-branch microbiota-mediated mechanism family in the C06 graph.**  
The refined graph shows that tea polysaccharide studies converge on several distinct but related microbiota-centered routes, including butyrate-associated thermogenesis and adipose browning, bile-acid remodeling linked to NAFLD protection, and oxidative/neuroinflammatory regulation involving Lactobacillus and the Firmicutes/Bacteroidota balance.

---

## 3. Which Story Should Be Main Figure 1?

Best choice:
- Story A as the main explanatory figure

Reason:
- simplest and most intuitive
- strongest microbiota -> metabolite -> barrier -> phenotype chain
- easiest for readers outside microbiome science to follow

Best choice for a second high-impact figure:
- Story C as the most graph-native and “surprising” structure

Best choice for a specialty figure or highlight box:
- Story B

## 4. How To Use These Stories In The Paper

### Introduction

Use the three stories to motivate why a tea microbiome KG is necessary:
- tea effects are distributed across multiple host systems
- the literature is mechanism-rich but fragmented
- the graph unifies these multi-hop routes

### Results

Recommended subsection order:
1. Global C06 graph overview
2. Story A: obesity / barrier route
3. Story B: gut-brain route
4. Story C: polysaccharide mechanism family

### Discussion

Use the stories to argue:
- the graph is biologically interpretable
- the same graph formalism spans metabolism, cognition, and oxidative/neural phenotypes
- graph structure reveals transferable mechanism families

## 5. Figure Plan

### Figure C06-1
- Global graph overview with highlighted subpaths A, B, C

### Figure C06-2
- Detailed Story A path

### Figure C06-3
- Detailed Story C branch-family figure

### Optional Figure C06-4
- Story B gut-brain-axis inset

## 6. Current Limitations To State Explicitly

1. Some microbiota nodes are still grouped multi-taxon strings rather than fully separated taxa nodes.
2. Human evidence is still sparse relative to preclinical evidence.
3. Review-derived records remain useful for provenance but should not be interpreted as direct mechanistic edges.
4. Some pathways remain abstract-level rather than effect-size-aware causal models.

## 7. Immediate Next Move

If this story pack is accepted as the narrative direction, the next useful deliverable is:

- a `story-figure data pack` that exports just the nodes and edges for Stories A, B, and C separately

That would let you or me generate paper-ready schematic figures directly from the current KG.
