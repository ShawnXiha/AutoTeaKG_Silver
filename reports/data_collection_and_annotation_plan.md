# Data Collection and Annotation Plan

Date: 2026-03-31

## 1. Goal

Build a high-quality gold set and a scalable extraction workflow for:
- C04 evidence-graded tea activity database
- C01 processing-aware extension
- C06 microbiome mechanism KG pilot

## 2. Retrieval Plan

### Seed corpus
- start from the curated 2022-2026 reviews and resource papers already collected
- expand by backward citation tracing
- expand by PubMed query templates

### Query blocks

Tea block:
- tea
- green tea
- oolong tea
- black tea
- fermented tea
- Camellia sinensis

Component block:
- catechin
- EGCG
- theaflavin
- theanine
- caffeine
- tea polysaccharide
- tea extract

Activity block:
- antioxidant
- anti-inflammatory
- gut microbiota
- microbiome
- obesity
- metabolic syndrome
- neuroprotection

Processing block:
- processing
- fermentation
- extraction
- ultrasound extraction
- microwave extraction
- supercritical extraction
- withering
- rolling
- drying

### Search output files
- raw_search_results.csv
- deduplicated_results.csv
- screened_titles.csv
- screened_abstracts.csv
- included_papers.csv

## 3. Annotation Unit

One paper can yield multiple evidence records.  
The atomic unit is not the paper, but the `EvidenceRecord`.

## 4. Annotation Fields

Required:
- paper id
- evidence record id
- tea type
- extract/component group
- activity category
- endpoint
- study type
- evidence level
- model system
- dose/exposure
- effect direction

Optional:
- processing step
- extraction method
- cultivar
- origin
- mechanism phrase
- microbiota taxon
- microbial metabolite

## 5. Annotation Rules

1. Normalize to controlled vocabulary whenever possible.
2. Preserve raw text for every normalized field.
3. If a study reports multiple activities, create multiple evidence records.
4. If the exact compound is uncertain, annotate at compound-group level.
5. If evidence level is ambiguous, mark for adjudication rather than guessing.

## 6. Quality Control

### Double annotation
- first 30 papers fully double-annotated
- compute agreement
- revise guidelines

### Adjudication
- maintain an adjudication log for disputed cases
- record why the final label was chosen

### Sampling for audit
- random audit by activity category
- random audit by study type
- random audit by tea type

## 7. Outputs for Paper 1

- annotation guideline
- gold set
- normalized dictionaries
- quality report

## 8. Outputs for Phase 2 and 3

- processing-context enrichment table
- microbiome triple candidates
- graph export mapping rules
