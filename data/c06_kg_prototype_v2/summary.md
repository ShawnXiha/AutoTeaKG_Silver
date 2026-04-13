# C06 KG Prototype v2 Summary

Date: 2026-03-31
Source database: `teakg_v1.sqlite`

## Scope

- Source evidence records selected for prototype: 29
- Exported node count: 136
- Exported edge count: 262

## Cleanup Rules

- Removed placeholder microbiota nodes such as `taxa as reported`.
- Removed low-information metabolite placeholders such as `microbial metabolites as reported`.
- Removed generic host phenotype placeholders such as `microbiota-related host phenotype`.
- Preserved `EvidenceRecord` nodes and provenance edges.

## Node Types

- ActivityCategory: 6
- ComponentGroup: 5
- EvidenceLevel: 4
- EvidenceRecord: 29
- HostPhenotype: 13
- Mechanism: 39
- MicrobialMetabolite: 4
- MicrobiotaFeature: 10
- Paper: 17
- StudyType: 4
- TeaType: 5

## Edge Types

- ACTS_VIA: 39
- AFFECTS_HOST_PHENOTYPE: 7
- ASSOCIATED_HOST_PHENOTYPE: 19
- HAS_COMPONENT_GROUP: 29
- HAS_EVIDENCE_LEVEL: 29
- HAS_RECORD: 29
- HAS_STUDY_TYPE: 29
- HAS_TEA_TYPE: 29
- LINKS_TO_METABOLITE: 7
- MODULATES_MICROBIOTA: 16
- SUPPORTS_ACTIVITY: 29

## Recommended Uses

- Better suited than v1 for presentation screenshots and graph demos.
- Still not a final production KG because some mechanisms remain broad review-level concepts.
- Use this export when you want clearer topological structure with less placeholder noise.