# AutoTeaKG-Silver v1 Summary

Date: 2026-04-12

This run builds an auto-only silver-standard evidence layer and uncertainty-aware KG v3. Manual adjudication and manual audit files are not used as construction inputs.

## Outputs

- Silver records: `D:\projects\paper_writing\teakg\reports\autoteakg_silver_v1\autoteakg_silver_records.csv`
- Processing/component report: `D:\projects\paper_writing\teakg\reports\autoteakg_silver_v1\processing_component_extraction_report.csv`
- KG v3 nodes: `D:\projects\paper_writing\teakg\reports\autoteakg_silver_v1\kg_v3\nodes.csv`
- KG v3 edges: `D:\projects\paper_writing\teakg\reports\autoteakg_silver_v1\kg_v3\edges.csv`

## Counts

- Silver records: 635
- KG v3 nodes: 1963
- KG v3 edges: 8162
- Excluded records: {'manual_annotator': 28, 'non_standard_auto_or_malformed_annotator': 6}

## Uncertainty Classes

- high_uncertainty: 70
- low_uncertainty: 86
- moderate_uncertainty: 479

## Top Component Groups

- catechins: 152
- mixed polyphenols: 150
- multiple component groups: 135
- whole extract: 83
- tea polysaccharides: 43
- theaflavins: 27
- caffeine: 26
- theanine: 16
- volatile compounds; mixed polyphenols: 3

## Top Processing Steps

- (blank): 489
- fermentation/oxidation: 89
- storage/aging: 22
- enzymatic treatment: 12
- fermentation/oxidation; storage/aging: 6
- roasting: 5
- fermentation/oxidation; roasting: 4
- pan-firing/fixation: 2
- fermentation/oxidation; enzymatic treatment: 2
- processing category contrast: 2
- storage/aging; enzymatic treatment: 1
- drying: 1

## Top Extraction Methods

- (blank): 481
- other extraction: 133
- aqueous extraction; other extraction: 11
- aqueous extraction: 8
- supercritical fluid extraction: 1
- aqueous extraction; solvent extraction; other extraction: 1

## Uncertainty Flags

- missing_processing_or_extraction_context: 365
- preclinical_only: 288
- generic_mechanism: 237
- review_summary_record: 197
- taxonomy_expansion_needed: 172
- uncertain_effect_direction: 164
- missing_named_microbiota: 65
- low_llm_confidence: 60
- low_evidence_level: 4
- invalid_evidence_level: 2