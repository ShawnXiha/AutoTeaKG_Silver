# Annotation Guideline v1

Project: Tea Functional Activity Evidence Database  
Date: 2026-03-31  
Version: v1

## 1. Purpose

This guideline defines how to annotate literature for:
- Phase 1: evidence-graded tea functional activity database
- Phase 2: processing-aware extension
- Phase 3: microbiome mechanism KG pilot

The annotation target is the `EvidenceRecord`, not the paper.

## 2. Annotation Unit

Create one `EvidenceRecord` for each distinct claim that combines:
- tea material or extract or component group
- activity category
- study system
- endpoint/result context

Examples:
- One paper reports antioxidant and anti-inflammatory effects of green tea extract in mice.
  - Annotate 2 records if the activities are distinct.
- One paper reports EGCG effects in both cell and mouse experiments.
  - Annotate 2 records if model systems differ materially.

## 3. Required Fields

Every record must include:
- `paper_id`
- `record_id`
- `tea_type`
- `material_form`
- `component_group`
- `activity_category`
- `endpoint_label`
- `study_type`
- `evidence_level`
- `model_system`
- `dose_exposure`
- `effect_direction`
- `claim_text_raw`

## 4. Optional Fields

Add when available:
- `processing_step`
- `extraction_method`
- `cultivar`
- `origin`
- `compound_name`
- `mechanism_label`
- `microbiota_taxon`
- `microbial_metabolite`
- `host_phenotype`

## 5. Normalization Rules

### 5.1 Tea Type

Use one of:
- `green tea`
- `oolong tea`
- `black tea`
- `white tea`
- `dark/post-fermented tea`
- `fermented tea beverage`
- `unspecified tea`

If the paper uses a branded or local name, preserve it in raw text and map to the closest normalized class only if justified.

### 5.2 Material Form

Use one of:
- `tea leaf`
- `tea infusion`
- `tea extract`
- `purified component`
- `enriched fraction`
- `fermented beverage`
- `unspecified material`

### 5.3 Component Group

Use one of:
- `catechins`
- `theaflavins`
- `theanine`
- `caffeine`
- `tea polysaccharides`
- `volatile compounds`
- `mixed polyphenols`
- `whole extract`
- `multiple component groups`
- `unspecified`

If the paper reports EGCG only, set:
- `compound_name = EGCG`
- `component_group = catechins`

### 5.4 Activity Category

Use one primary category:
- `antioxidant`
- `anti-inflammatory`
- `metabolic improvement`
- `anti-obesity`
- `gut microbiota modulation`
- `neuroprotection`
- `cardiovascular protection`
- `anticancer`
- `other`

If a claim fits multiple categories, create separate records only when the paper reports separate evidence.

### 5.5 Study Type

Use one of:
- `in vitro`
- `animal study`
- `randomized controlled trial`
- `cohort study`
- `meta-analysis`
- `systematic review`

### 5.6 Evidence Level

Map from study type:
- `in vitro` -> `low_preclinical`
- `animal study` -> `preclinical_in_vivo`
- `randomized controlled trial` -> `human_interventional`
- `cohort study` -> `human_observational`
- `meta-analysis` -> `evidence_synthesis`
- `systematic review` -> `evidence_synthesis_nonquantitative`

### 5.7 Effect Direction

Use one of:
- `positive`
- `negative`
- `mixed`
- `no_clear_effect`

`positive` means the reported result supports the claimed activity.

## 6. Processing and Extraction Annotation

### 6.1 Processing Step

Use controlled labels when explicit:
- `withering`
- `fixation/kill-green`
- `rolling`
- `fermentation/oxidation`
- `drying`
- `aging/post-fermentation`
- `blending/flavoring`

If only overall tea category is known, do not infer a specific step.

### 6.2 Extraction Method

Use controlled labels:
- `water extraction`
- `ethanol extraction`
- `methanol extraction`
- `ultrasound extraction`
- `microwave extraction`
- `supercritical extraction`
- `pressurized liquid extraction`
- `other extraction`

## 7. Mechanism and Microbiome Annotation

### 7.1 Mechanism Label

Capture only explicit mechanism claims, such as:
- `NF-kB inhibition`
- `AMPK activation`
- `antioxidant enzyme modulation`
- `barrier protection`

Do not infer a mechanism from general discussion unless the study presents evidence.

### 7.2 Microbiota Taxon

Record the taxon exactly as reported in raw text and add normalized name if clear.

Examples:
- `Akkermansia muciniphila`
- `Bacteroides`
- `Lactobacillus`

### 7.3 Microbial Metabolite

Examples:
- `SCFAs`
- `butyrate`
- `acetate`
- `propionate`

## 8. Ambiguity Handling

If uncertain:
- preserve raw text
- choose the broadest defensible normalized label
- add a note in adjudication log if the case is important

Never force fine-grained normalization when the paper does not justify it.

## 9. Double Annotation Protocol

For the first 30 papers:
- 2 annotators independently annotate all records
- compare all required fields
- compute agreement
- revise the guideline before scaling

## 10. Common Error Patterns

1. Annotating the whole paper as one record when it reports multiple distinct claims
2. Confusing `study_type` with `evidence_level`
3. Normalizing tea type too aggressively from ambiguous local names
4. Using exact compounds where only broad fractions are justified
5. Treating speculative discussion as mechanism evidence

## 11. Minimal Record Example

```json
{
  "paper_id": "PMID_39574401",
  "record_id": "PMID_39574401_R1",
  "tea_type": "unspecified tea",
  "material_form": "purified component",
  "component_group": "mixed polyphenols",
  "activity_category": "anti-obesity",
  "endpoint_label": "body weight gain reduction",
  "study_type": "animal study",
  "evidence_level": "preclinical_in_vivo",
  "model_system": "high-fat diet-induced mice",
  "dose_exposure": "as reported in paper",
  "effect_direction": "positive",
  "claim_text_raw": "Tea polyphenols reduced obesity by modulating gut microbiota..."
}
```
