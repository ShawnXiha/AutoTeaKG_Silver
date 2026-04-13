# C06 KG Prototype Summary

Date: 2026-03-31
Source database: `teakg_v1.sqlite`

## Scope

- Source evidence records selected for prototype: 29
- Exported node count: 110
- Exported edge count: 245

## Node Types

- ActivityCategory: 6
- ComponentGroup: 5
- EvidenceLevel: 4
- EvidenceRecord: 29
- HostPhenotype: 12
- Mechanism: 20
- MicrobialMetabolite: 4
- MicrobiotaFeature: 4
- Paper: 17
- StudyType: 4
- TeaType: 5

## Edge Types

- ACTS_VIA: 20
- AFFECTS_HOST_PHENOTYPE: 7
- ASSOCIATED_HOST_PHENOTYPE: 17
- HAS_COMPONENT_GROUP: 29
- HAS_EVIDENCE_LEVEL: 29
- HAS_RECORD: 29
- HAS_STUDY_TYPE: 29
- HAS_TEA_TYPE: 29
- LINKS_TO_METABOLITE: 7
- MODULATES_MICROBIOTA: 20
- SUPPORTS_ACTIVITY: 29

## Graph Design

- `EvidenceRecord` is kept as a first-class node so every mechanistic statement remains traceable to a source paper.
- The prototype is database-first and provenance-preserving, not a fully normalized biological graph.
- Generic placeholders such as `taxa as reported` are retained when present in the curated source records to avoid inventing unsupported specificity.

## Recommended Uses

- Import into Neo4j for prototype exploration
- Use in NetworkX for path inspection
- Identify which nodes need full-text refinement before a production KG build