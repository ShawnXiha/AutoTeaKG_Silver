# C06 Refinement Plan v1

Date: 2026-03-31

## Purpose

Move from `c06_kg_prototype_v2` to a more specific mechanism graph by refining the subset of records that currently carry the most signal but still contain placeholder biology.

## Current Diagnosis

The current prototype is structurally usable, but the main bottlenecks are:
- microbiota nodes remain underspecified in many key anchor records
- some mechanism labels are still broad summary phrases
- several host phenotypes are syndrome-level rather than endpoint-level
- review-derived records are useful for provenance but should not dominate the graph

## Priority Structure

### P1: Full-text refinement now

These are the records that should drive the next real C06 build:
- `PMID_39574401_R1`
- `PMID_39574401_R2`
- `PMID_38745351_R1`
- `PMID_40957830_R1`
- `PMID_40957830_R2`
- `PMID_39153277_R1`
- `PMID_39153277_R2`
- `PMID_39255891_R1`
- `PMID_39255891_R2`
- `PMID_39479919_R1`
- `PMID_39479919_R2`
- `PMID_39732435_R1`
- `PMID_38430822_R1`
- `PMID_36449351_R1`
- `PMID_36449351_R2`

Why these first:
- they already carry strong mechanism scaffolds
- several have explicit metabolite or barrier terms
- they cover obesity, metabolic syndrome, NAFLD, cognition, oxidative stress, and human intervention

### P2: Abstract-first refinement

These help contextualize the graph but are not the first bottleneck:
- `PMID_38430822_R2`
- `PMID_40640361_R1`
- `PMID_40640361_R2`
- `PMID_39274868_R1`
- `PMID_39452088_R1`
- `PMID_38745671_R1`
- `PMID_38745671_R2`

### P3: Context-only records

Keep them in the evidence layer, but do not prioritize them for graph specificity:
- `PMID_38056775_R1`
- `PMID_38056775_R2`
- `PMID_39920567_R1`
- `PMID_40160899_R1`
- `PMID_40160899_R2`
- `PMID_38031409_R1`
- `PMID_38031409_R2`
- `PMID_40314930_R1`

## What “Done” Looks Like For P1

For each P1 record:
- replace placeholder microbiota node with named taxa where explicit
- replace generic metabolite with named SCFA or bile acid where explicit
- replace syndrome-level host phenotype with specific measurable phenotype where explicit
- split mechanism string into graph-meaningful mechanism nodes
- keep provenance and evidence level unchanged

## Immediate Execution Order

1. `PMID_39574401`
2. `PMID_38745351`
3. `PMID_40957830`
4. `PMID_39153277`
5. `PMID_39255891`
6. `PMID_39479919`
7. `PMID_39732435`
8. `PMID_38430822`
9. `PMID_36449351`

This order is deliberate:
- first refine the strongest graph-native anchors
- then the best human bridge records
- then older but still valuable fermented-tea anchors

## Files To Use

- Priority table:
  [c06_refinement_priority_table_v1.csv](D:\projects\paper_writing\teakg\templates\c06_refinement_priority_table_v1.csv)
- Update log:
  [c06_refined_records_log_v1.csv](D:\projects\paper_writing\teakg\templates\c06_refined_records_log_v1.csv)
- Protocol:
  [c06_full_text_refinement_protocol_v1.md](D:\projects\paper_writing\teakg\protocols\c06_full_text_refinement_protocol_v1.md)

## Recommendation

The next concrete move should be to refine the first 3 P1 papers manually against abstract/full text, update the source evidence CSV, and then regenerate `c06_kg_prototype_v2`. That will show whether node specificity improves enough to justify a larger refinement cycle.
