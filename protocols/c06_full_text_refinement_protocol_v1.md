# C06 Full-Text Refinement Protocol v1

Project: Tea Gut-Microbiome Mechanism Graph  
Date: 2026-03-31

## 1. Goal

Convert the current C06 prototype from a provenance-preserving but partially abstract graph into a more biologically specific mechanism graph by revisiting abstracts and full texts for the most informative records.

The current main limitations are:
- placeholder microbiota entities such as `taxa as reported`
- broad mechanism phrases such as `microbiota-associated activity`
- generic host phenotypes such as `physiological health indicators`
- review-level summaries that should not be treated like primary mechanistic edges

## 2. Refinement Priorities

Priority is determined by:
1. whether the record is a primary study rather than a review
2. whether it already contains a strong mechanism scaffold
3. whether it includes microbiota-metabolite-host phenotype structure
4. whether it is human evidence
5. whether it is central to the planned C06 story

Priority tiers:
- `P1`: immediate full-text refinement
- `P2`: abstract-first, full-text if needed
- `P3`: retain as context/provenance only

## 3. What to Refine

### 3.1 Microbiota entities

Replace placeholders with:
- genus/species names where explicitly reported
- direction if available: enriched, depleted, restored

Preferred structure:
- `CompoundGroup modulates MicrobiotaTaxon`
- with optional edge attributes:
  - `direction`
  - `model_system`
  - `evidence_level`

### 3.2 Microbial metabolites

Replace broad labels with:
- butyrate
- acetate
- propionate
- bile acids or specific bile-acid families

Preferred structure:
- `MicrobiotaTaxon links_to MicrobialMetabolite`
- `MicrobialMetabolite affects HostPhenotype`

### 3.3 Host phenotypes

Replace generic phenotype labels with more specific outputs such as:
- body weight gain
- adipose browning
- fasting glucose
- endotoxemia
- NAFLD severity
- cognitive impairment score
- oxidative stress markers
- inflammatory marker profile

### 3.4 Mechanism nodes

Split broad mechanisms into more specific mechanism nodes when supported:
- gut barrier protection
- SCFA signaling
- bile acid metabolism regulation
- MAPKs/MMP-9 inhibition
- thermogenesis activation
- microglial oxidative damage reduction

### 3.5 Evidence status

For each refined record, preserve:
- study type
- evidence level
- source paper
- whether the edge is direct evidence or inferred summary

## 4. Refinement Workflow

### Step 1. Abstract pass

For each target record:
- read title and abstract
- extract named microbiota taxa
- extract named metabolites
- extract specific host phenotypes
- tighten the mechanism phrase

If abstract is sufficient, update the record and mark `abstract_refined`.

### Step 2. Full-text pass

Use full text when:
- microbiota taxa are only summarized generically in the abstract
- directionality is unclear
- host phenotype is vague
- multiple mechanisms are conflated
- the paper is a key anchor for C06

If full text is used, update the record and mark `full_text_refined`.

### Step 3. KG remapping

After refinement:
- regenerate `c06_kg_prototype_v2`
- compare node/edge counts
- inspect whether biologically informative node density increases

## 5. Field-Level Update Rules

### microbiota_taxon

Allowed updates:
- `taxa as reported` -> explicit taxa list

Do not:
- infer taxa not explicitly reported

### microbial_metabolite

Allowed updates:
- `SCFAs` -> `butyrate`, `acetate`, `propionate` only if explicitly stated
- `bile-acid-related metabolites` -> specific bile acid term only if explicit

### host_phenotype

Allowed updates:
- broad syndrome label -> measurable phenotype if explicitly stated

### mechanism_label

Allowed updates:
- split one broad label into multiple specific labels separated by `;`

## 6. Recommended Order

1. P1 animal mechanistic anchors
2. P1 human microbiome / human intervention anchors
3. P2 strong review bridges
4. P3 broad context reviews

## 7. Output Files To Maintain

- `templates/c06_refinement_priority_table_v1.csv`
- `templates/c06_refined_records_log_v1.csv`
- regenerated `data/c06_kg_prototype_v2/*`
