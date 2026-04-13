# Entity-Relation Schema v1

Date: 2026-03-31

## 1. Design Principles

1. Phase 1 must support evidence comparison, not ontology perfection.
2. Every normalized field should preserve raw reported text.
3. Database-first, graph-ready.
4. Broad controlled vocabularies first, fine-grained expansion later.

## 2. Core Tables / Entities

### Paper
- paper_id
- title
- authors
- journal
- year
- doi
- pmid
- abstract

### EvidenceRecord
- record_id
- paper_id
- claim_text_raw
- activity_category_id
- endpoint_id
- study_type_id
- evidence_level_id
- model_system_id
- dose_exposure_id
- effect_direction
- confidence_score

### TeaMaterial
- tea_material_id
- tea_type_id
- cultivar_id
- origin_id
- material_form
- raw_description

### Extract
- extract_id
- tea_material_id
- extraction_method_id
- extract_type
- solvent
- raw_description

### CompoundGroup
- compound_group_id
- normalized_name
- description

### Compound
- compound_id
- compound_group_id
- normalized_name
- synonym_list

### ProcessingContext
- processing_context_id
- tea_material_id
- processing_step_id
- stage_order
- raw_description

### MechanismRecord
- mechanism_record_id
- record_id
- mechanism_label
- raw_text

### MicrobiomeRecord
- microbiome_record_id
- record_id
- taxon_name
- metabolite_name
- host_phenotype
- raw_text

## 3. Core Controlled Vocabularies

### TeaType
- green tea
- oolong tea
- black tea
- white tea
- dark/post-fermented tea
- fermented tea beverage
- unspecified tea

### StudyType
- in vitro
- animal study
- randomized controlled trial
- cohort study
- meta-analysis
- review-derived summary

### ActivityCategory
- antioxidant
- anti-inflammatory
- metabolic improvement
- anti-obesity
- gut microbiota modulation
- neuroprotection
- cardiovascular protection
- anticancer

### ComponentGroup
- catechins
- theaflavins
- theanine
- caffeine
- tea polysaccharides
- volatile compounds
- mixed polyphenols
- whole extract

## 4. Relations

### Database logical relations
- Paper `has` EvidenceRecord
- EvidenceRecord `abouts` TeaMaterial or Extract or CompoundGroup
- EvidenceRecord `supports` ActivityCategory
- EvidenceRecord `measured_by` Endpoint
- EvidenceRecord `evaluated_in` ModelSystem
- EvidenceRecord `has_level` EvidenceLevel
- TeaMaterial `has_processing` ProcessingContext
- Extract `derived_from` TeaMaterial
- Extract `contains_or_enriches` CompoundGroup

### Graph mapping relations
- TeaMaterial `processed_by` ProcessingStep
- ProcessingStep `alters` CompoundGroup
- CompoundGroup `associated_with` BioactivityCategory
- CompoundGroup `modulates` MicrobiotaTaxon
- MicrobiotaTaxon `links_to` MicrobialMetabolite
- MicrobialMetabolite `affects` HostPhenotype
- EvidenceRecord `supported_by` Paper

## 5. Phase Boundaries

### Phase 1 required
- Paper
- EvidenceRecord
- TeaMaterial
- Extract
- CompoundGroup
- ActivityCategory
- StudyType
- EvidenceLevel
- DoseExposure

### Phase 2 added
- ProcessingContext
- Cultivar
- Origin
- finer compound mapping

### Phase 3 added
- MechanismRecord
- MicrobiomeRecord
- graph-native node and edge export
