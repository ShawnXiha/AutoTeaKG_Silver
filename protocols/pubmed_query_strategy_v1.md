# PubMed Query Strategy v1

Project: Tea Functional Activity Evidence Database  
Date: 2026-03-31

## 1. Retrieval Principles

1. Start broad enough to avoid recall loss.
2. Split searches by activity family and evidence type.
3. Log exact queries and search dates.
4. Use review-led seed expansion first, then targeted primary-study retrieval.

## 2. Core Time Window

Primary review window:
- 2022/01/01 to 2026/03/31

Primary-study expansion:
- no hard lower limit if retrieved from key reviews
- priority remains recent studies unless foundational older studies are needed

## 3. Query Blocks

### Tea block

```text
("tea"[Title/Abstract] OR "green tea"[Title/Abstract] OR "oolong tea"[Title/Abstract] OR "black tea"[Title/Abstract] OR "white tea"[Title/Abstract] OR "dark tea"[Title/Abstract] OR "fermented tea"[Title/Abstract] OR "Camellia sinensis"[Title/Abstract])
```

### Component block

```text
("tea extract"[Title/Abstract] OR "catechin*"[Title/Abstract] OR "EGCG"[Title/Abstract] OR "theaflavin*"[Title/Abstract] OR "theanine"[Title/Abstract] OR "caffeine"[Title/Abstract] OR "tea polysaccharide*"[Title/Abstract] OR "tea polyphenol*"[Title/Abstract])
```

### Activity block

```text
("antioxidant"[Title/Abstract] OR "anti-inflammatory"[Title/Abstract] OR inflammation[Title/Abstract] OR "gut microbiota"[Title/Abstract] OR microbiome[Title/Abstract] OR obesity[Title/Abstract] OR metabolic[Title/Abstract] OR neuroprotect*[Title/Abstract] OR cardiovascular[Title/Abstract])
```

### Processing block

```text
("processing"[Title/Abstract] OR fermentation[Title/Abstract] OR extraction[Title/Abstract] OR "ultrasound extraction"[Title/Abstract] OR "microwave extraction"[Title/Abstract] OR "supercritical extraction"[Title/Abstract] OR withering[Title/Abstract] OR rolling[Title/Abstract] OR drying[Title/Abstract])
```

## 4. Recommended Queries

### Q1. Broad review retrieval

```text
(("tea"[Title/Abstract] OR "green tea"[Title/Abstract] OR "oolong tea"[Title/Abstract] OR "black tea"[Title/Abstract] OR "Camellia sinensis"[Title/Abstract]) AND ("review"[Publication Type] OR review[Title]) AND ("bioactive"[Title/Abstract] OR "functional activity"[Title/Abstract] OR antioxidant[Title/Abstract] OR anti-inflammatory[Title/Abstract] OR microbiota[Title/Abstract] OR metabolic[Title/Abstract])) AND ("2022/01/01"[Date - Publication] : "2026/03/31"[Date - Publication])
```

### Q2. Functional activity primary studies

```text
(("tea"[Title/Abstract] OR "green tea"[Title/Abstract] OR "oolong tea"[Title/Abstract] OR "black tea"[Title/Abstract] OR "Camellia sinensis"[Title/Abstract]) AND ("tea extract"[Title/Abstract] OR "catechin*"[Title/Abstract] OR EGCG[Title/Abstract] OR theaflavin*[Title/Abstract] OR theanine[Title/Abstract] OR caffeine[Title/Abstract] OR "tea polysaccharide*"[Title/Abstract] OR "tea polyphenol*"[Title/Abstract]) AND ("antioxidant"[Title/Abstract] OR "anti-inflammatory"[Title/Abstract] OR inflammation[Title/Abstract] OR obesity[Title/Abstract] OR metabolic[Title/Abstract] OR neuroprotect*[Title/Abstract] OR cardiovascular[Title/Abstract]))
```

### Q3. Microbiome-focused studies

```text
(("tea"[Title/Abstract] OR "green tea"[Title/Abstract] OR "oolong tea"[Title/Abstract] OR "black tea"[Title/Abstract] OR "fermented tea"[Title/Abstract] OR "Camellia sinensis"[Title/Abstract]) AND ("gut microbiota"[Title/Abstract] OR microbiome[Title/Abstract] OR "short-chain fatty acid*"[Title/Abstract] OR SCFA[Title/Abstract] OR barrier[Title/Abstract]) AND ("tea extract"[Title/Abstract] OR "tea polyphenol*"[Title/Abstract] OR catechin*[Title/Abstract] OR theaflavin*[Title/Abstract]))
```

### Q4. Processing-aware studies

```text
(("tea"[Title/Abstract] OR "green tea"[Title/Abstract] OR "oolong tea"[Title/Abstract] OR "black tea"[Title/Abstract] OR "Camellia sinensis"[Title/Abstract]) AND (processing[Title/Abstract] OR extraction[Title/Abstract] OR fermentation[Title/Abstract] OR "ultrasound extraction"[Title/Abstract] OR "microwave extraction"[Title/Abstract] OR "supercritical extraction"[Title/Abstract]) AND ("bioactive"[Title/Abstract] OR antioxidant[Title/Abstract] OR anti-inflammatory[Title/Abstract] OR metabol*[Title/Abstract] OR microbiota[Title/Abstract]))
```

### Q5. Human evidence

```text
(("tea"[Title/Abstract] OR "green tea"[Title/Abstract] OR "oolong tea"[Title/Abstract] OR "black tea"[Title/Abstract] OR "Camellia sinensis"[Title/Abstract]) AND ("randomized controlled trial"[Publication Type] OR "cohort"[Title/Abstract] OR "meta-analysis"[Publication Type] OR "prospective"[Title/Abstract]) AND (antioxidant[Title/Abstract] OR inflammation[Title/Abstract] OR obesity[Title/Abstract] OR metabolic[Title/Abstract] OR cardiovascular[Title/Abstract]))
```

## 5. Search Log Template

For each query, record:
- search_id
- date searched
- database
- exact query string
- date filter
- result count
- export filename

## 6. Retrieval Order

1. Run Q1 to build review seed set.
2. Extract key primary papers from review references.
3. Run Q2-Q5 for targeted expansion.
4. Deduplicate by DOI first, title second.
5. Screen titles and abstracts.
