# AutoTeaKG-Silver v1 Summary

Date: 2026-04-12

This run builds an auto-only silver-standard evidence layer and uncertainty-aware KG v3. Manual adjudication and manual audit files are not used as construction inputs.

## Outputs

- Silver records: `reports\methods_processing_llm_final\patched_autoteakg_silver_v1\autoteakg_silver_records.csv`
- Processing/component report: `reports\methods_processing_llm_final\patched_autoteakg_silver_v1\processing_component_extraction_report.csv`
- KG v3 nodes: `reports\methods_processing_llm_final\patched_autoteakg_silver_v1\kg_v3\nodes.csv`
- KG v3 edges: `reports\methods_processing_llm_final\patched_autoteakg_silver_v1\kg_v3\edges.csv`

## Counts

- Silver records: 635
- KG v3 nodes: 2018
- KG v3 edges: 8207
- Excluded records: {'targeted_processing_llm_patches': 151}

## Uncertainty Classes

- high_uncertainty: 65
- low_uncertainty: 100
- moderate_uncertainty: 470

## Top Component Groups

- catechins: 167
- mixed polyphenols: 151
- multiple component groups: 147
- whole extract: 83
- tea polysaccharides: 26
- theaflavins: 24
- caffeine: 22
- theanine: 12
- volatile compounds; mixed polyphenols: 3

## Top Processing Steps

- (blank): 452
- fermentation/oxidation: 89
- storage/aging: 22
- enzymatic treatment: 12
- fermentation/oxidation; storage/aging: 6
- roasting: 5
- black tea processing: 4
- fermentation/oxidation; roasting: 4
- fermentation; oxidative conversion: 3
- processing by-product: 3
- processing category contrast: 3
- crushed; sieved (20-mesh): 2

## Top Extraction Methods

- (blank): 450
- other extraction: 134
- aqueous extraction; other extraction: 11
- aqueous extraction: 8
- isolation/purification: 8
- analytical characterization: 3
- soaked overnight: 2
- essential oil extraction: 2
- methanol extraction; sonication; filtration: 2
- brewing/infusion: 2
- commercial extract: 2
- ultrasonic extraction; ethanol 70% extraction; filtration; evaporation under reduced pressure: 1

## Uncertainty Flags

- missing_processing_or_extraction_context: 303
- preclinical_only: 288
- generic_mechanism: 237
- review_summary_record: 197
- taxonomy_expansion_needed: 172
- uncertain_effect_direction: 164
- missing_named_microbiota: 65
- low_llm_confidence: 60
- low_evidence_level: 4
- invalid_evidence_level: 2