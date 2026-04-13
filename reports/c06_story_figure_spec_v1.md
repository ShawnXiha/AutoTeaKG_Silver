# C06 Story Figure Spec v1

Date: 2026-03-31

Source subgraphs are exported to:
- `data/c06_story_subgraphs/story_A_polyphenol_obesity_nodes.csv`
- `data/c06_story_subgraphs/story_A_polyphenol_obesity_edges.csv`
- `data/c06_story_subgraphs/story_B_oolong_cognition_nodes.csv`
- `data/c06_story_subgraphs/story_B_oolong_cognition_edges.csv`
- `data/c06_story_subgraphs/story_C_polysaccharide_family_nodes.csv`
- `data/c06_story_subgraphs/story_C_polysaccharide_family_edges.csv`

## Figure C06-1: Story A

Title:
- Tea polyphenols may reduce obesity-related phenotypes through microbiota remodeling, SCFA-linked signaling, and barrier protection

Layout:
- horizontal left-to-right path

Node order:
1. `mixed polyphenols`
2. `Blautia / Faecalibaculum / Colidextribacter`
3. `SCFAs`
4. `G protein-coupled receptor activation / histone deacetylase inhibition / tight junction enhancement / barrier protection`
5. `obesity-related phenotype`

Highlight:
- bold the microbiota -> metabolite -> barrier transition

## Figure C06-2: Story B

Title:
- Oolong tea polyphenols are connected to cognition through a gut-brain-axis mechanism path

Layout:
- vertical layered figure

Layers:
1. tea component
2. microbiota taxa
3. LPS / SCFAs / glutamate
4. synaptic and microglial mechanisms
5. cognition phenotype

Highlight:
- `BDNF-PSD95-SYN synaptic plasticity support`
- `microglia activation reduction`

## Figure C06-3: Story C

Title:
- Tea polysaccharides form a multi-branch microbiota-mediated mechanism family

Layout:
- radial figure centered on `tea polysaccharides`

Three branches:
1. `Bifidobacterium -> butyrate -> PGC-1alpha/UCP1 -> adipose browning`
2. `Muribaculaceae / related taxa -> bile acids -> FXR-FGF15-FGFR4-ASBT suppression -> NAFLD`
3. `Firmicutes/Bacteroidota + Lactobacillus -> NF-kB suppression / antioxidant restoration -> oxidative-neural protection`

Highlight:
- use one color per branch
- center node should visually anchor the family concept

## Styling Guidance

Recommended node color map:
- Tea component / component group: dark green
- Microbiota: teal
- Metabolite: amber
- Mechanism: deep red
- Phenotype: navy
- EvidenceRecord / Paper provenance nodes: light gray

Recommended final paper use:
- Hide provenance nodes in the main schematic
- keep provenance nodes in supplementary graph figure

## Caption Strategy

Main paper captions should describe:
- the biological path
- the graph role
- the study context level

Do not include long provenance details in the main caption. Put PMIDs in figure notes or supplementary legends.
