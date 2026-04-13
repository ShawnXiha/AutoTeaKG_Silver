# AutoTeaKG-Silver v1 Summary

Date: 2026-04-12

This run builds an auto-only silver-standard evidence layer and uncertainty-aware KG v3. Manual adjudication and manual audit files are not used as construction inputs.

## Outputs

- Silver records: `reports\targeted_processing_llm_extractor_final\patched_autoteakg_silver_v1\autoteakg_silver_records.csv`
- Processing/component report: `reports\targeted_processing_llm_extractor_final\patched_autoteakg_silver_v1\processing_component_extraction_report.csv`
- KG v3 nodes: `reports\targeted_processing_llm_extractor_final\patched_autoteakg_silver_v1\kg_v3\nodes.csv`
- KG v3 edges: `reports\targeted_processing_llm_extractor_final\patched_autoteakg_silver_v1\kg_v3\edges.csv`

## Counts

- Silver records: 635
- KG v3 nodes: 2002
- KG v3 edges: 8183
- Excluded records: {'targeted_processing_llm_patches': 365}

## Uncertainty Classes

- high_uncertainty: 68
- low_uncertainty: 92
- moderate_uncertainty: 475

## Top Component Groups

- catechins: 160
- mixed polyphenols: 158
- multiple component groups: 145
- whole extract: 83
- tea polysaccharides: 26
- theaflavins: 24
- caffeine: 24
- theanine: 12
- volatile compounds; mixed polyphenols: 3

## Top Processing Steps

- (blank): 468
- fermentation/oxidation: 89
- storage/aging: 22
- enzymatic treatment: 12
- fermentation/oxidation; storage/aging: 6
- roasting: 5
- fermentation/oxidation; roasting: 4
- black tea manufacturing: 2
- pan-firing/fixation: 2
- tea processing by-product: 2
- minimal processing: 2
- fermentation/oxidation; enzymatic treatment: 2

## Top Extraction Methods

- (blank): 465
- other extraction: 133
- aqueous extraction; other extraction: 11
- aqueous extraction: 8
- isolation; purification: 3
- essential oil extraction: 2
- chromatography; mass spectrometry; nuclear magnetic resonance: 2
- cold brewing; hot brewing: 2
- isolation: 2
- purification: 2
- supercritical fluid extraction: 1
- LC-MS/MS; HS-SPME-GCMS: 1

## Uncertainty Flags

- missing_processing_or_extraction_context: 329
- preclinical_only: 288
- generic_mechanism: 237
- review_summary_record: 197
- taxonomy_expansion_needed: 172
- uncertain_effect_direction: 164
- missing_named_microbiota: 65
- low_llm_confidence: 60
- low_evidence_level: 4
- invalid_evidence_level: 2