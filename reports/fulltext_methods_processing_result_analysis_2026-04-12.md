# Full-Text Methods Processing Extraction Analysis

Date: 2026-04-12

## Retrieval Coverage

- Remaining abstract-level missing-context records: 329
- Distinct papers queried for PMC full text: 213
- Records with PMC methods-like sections: 151
- Records without PMC full text: 178
- Paper status counts: {'sections_extracted': 109, 'no_pmc_fulltext': 104}

## Methods-Section GLM5 Completion

- Methods target patches generated: 151
- Source errors recovered by retry: 4
- Remaining errors: 0
- Missing patch count relative to all 329 remaining records: 178

## Before/After Context Coverage

| Field | Before normalized | After methods normalized | Added |
|---|---:|---:|---:|
| processing step present | 167 | 183 | 16 |
| extraction method present | 170 | 185 | 15 |
| component group present | 635 | 635 | 0 |

## Patch Content Profile

| processing_present | extraction_present | component_present | Count | Share |
|---|---|---|---:|---:|
| false | false | true | 81 | 53.6% |
| false | false | false | 44 | 29.1% |
| true | false | true | 11 | 7.3% |
| false | true | true | 10 | 6.6% |
| true | true | true | 5 | 3.3% |

## Final KG

- Normalized methods KG nodes: 1989
- Normalized methods KG edges: 8195
- Unmapped processing labels: 0
- Unmapped extraction labels: 0

## Interpretation

The full-text/methods lane recovered additional preparation and extraction details that were unavailable from abstracts alone, including crushing/sieving, cleaning-drying-powdering, ultrasonic ethanol extraction, methanol sonication, and brewing/isolation details.

The main bottleneck is open full-text availability: 178 of 329 remaining records did not have PMC full text. For these, the next feasible route is publisher full-text access, DOI landing pages, or targeted retrieval of methods from accessible PDFs.
