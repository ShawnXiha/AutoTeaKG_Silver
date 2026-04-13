# Mini Literature Review: Computational Related Work for AutoTeaKG-Silver

Date: 2026-04-12

Purpose: expand the v4 Related Work section with verified references on scientific information extraction, LLM-based extraction, biomedical literature mining, and biomedical knowledge graph construction.

Search sources used:

- Semantic Scholar API search, saved as `papers_20260412_computational_related_work_semantic_scholar.json`.
- DOI-based metadata retrieval through `https://doi.org/<DOI>` with BibTeX accept headers.
- Existing web search was used for topic discovery; final saved references were included only if DOI BibTeX retrieval succeeded.

Tavily was not used because open scholarly APIs and DOI metadata were sufficient for this pass. The supplied Tavily key was not written to any file.

## Output Files

- Verified reference notes: `sources/papers_20260412_computational_related_work_verified.md`
- Structured verification JSON: `sources/papers_20260412_computational_related_work_verified.json`
- New BibTeX file: `references/computational_related_work_refs.bib`
- Main merged BibTeX: `references/references.bib`

## Theme 1: LLM-Based Scientific Information Extraction

Large language models are increasingly used to extract structured data from scientific text. Dagdelen et al. show that LLMs can perform structured information extraction from scientific text when the extraction task is constrained by explicit schemas and prompts. Polak and Morgan similarly show that conversational language models and prompt engineering can extract materials data from research papers. These papers directly support AutoTeaKG-Silver's design choice to use schema-constrained LLM extraction rather than unrestricted summarization.

Recommended v4 citations:

- `dagdelen2024structured_ie_llm`
- `polak2024materials_data_llm`

Suggested Related Work sentence:

> Recent work shows that LLMs can extract structured information from scientific papers when prompts are tied to explicit schemas and domain constraints, particularly in materials-science settings \cite{dagdelen2024structured_ie_llm,polak2024materials_data_llm}.

## Theme 2: Biomedical Literature Mining and Information Extraction Resources

Biomedical text mining has a long history of transforming PubMed-scale literature into structured annotations and relations. SemMedDB extracts semantic predications at PubMed scale, while PubTator 3.0 provides an AI-powered biomedical literature resource for entity-centric search and annotation. BioPREP demonstrates deep learning predicate classification using SemMedDB-derived relations. These systems motivate the idea that literature-scale structured extraction can support downstream discovery, but AutoTeaKG-Silver differs by targeting tea functional activity, evidence grading, processing context, and uncertainty-aware graph outputs.

Recommended v4 citations:

- `kilicoglu2012semmeddb`
- `chen2024pubtator3`
- `hong2021bioprep_semmeddb`

Suggested Related Work sentence:

> Biomedical literature-mining systems such as SemMedDB, PubTator, and BioPREP demonstrate that large literature corpora can be converted into structured biomedical annotations and relations \cite{kilicoglu2012semmeddb,chen2024pubtator3,hong2021bioprep_semmeddb}.

## Theme 3: Scientific and Biomedical Language Models

Domain-specific language models provide important context for why scientific and biomedical extraction benefits from domain-aware methods. SciBERT was pretrained on scientific text, BioBERT on biomedical literature, and PubMedBERT on PubMed-domain text. AutoTeaKG-Silver currently uses GLM5 through prompt-based extraction rather than fine-tuned domain language models, but these references provide the broader background for scientific and biomedical NLP.

Recommended v4 citations:

- `beltagy2019scibert`
- `lee2020biobert`
- `gu2021pubmedbert`

Suggested Related Work sentence:

> Domain-specific language models such as SciBERT, BioBERT, and PubMedBERT demonstrate that scientific and biomedical text benefits from domain-specific representation learning \cite{beltagy2019scibert,lee2020biobert,gu2021pubmedbert}.

## Theme 4: Biomedical and Mechanistic Knowledge Graphs

Biomedical knowledge graphs integrate heterogeneous entities and relations to support drug repurposing, precision medicine, and mechanistic reasoning. Hetionet systematically integrates biomedical knowledge for drug repurposing, PrimeKG provides a multimodal precision-medicine KG, and COVID-19 drug-repurposing work demonstrates practical KG use in biomedical hypothesis generation. INDRA-related work shows how text mining and curated databases can be assembled into mechanistic representations at scale. These works motivate the graph layer of AutoTeaKG-Silver, while also highlighting the need for provenance, uncertainty, and normalization.

Recommended v4 citations:

- `himmelstein2017hetionet`
- `chandak2023primekg`
- `zeng2021kg_drug_repurposing_covid`
- `gyori2023automated_assembly_indra`

Suggested Related Work sentence:

> Biomedical KGs such as Hetionet and PrimeKG, together with mechanism-assembly frameworks such as INDRA, show how heterogeneous biomedical evidence can be organized for repurposing and mechanistic reasoning \cite{himmelstein2017hetionet,chandak2023primekg,zeng2021kg_drug_repurposing_covid,gyori2023automated_assembly_indra}.

## Theme 5: LLM-Based Knowledge Graph Construction

Recent NLP work explores LLM-based pipelines for extracting, defining, and canonicalizing entities and relations during KG construction. This literature is directly relevant to AutoTeaKG-Silver's patch-first extraction and vocabulary-normalization stages.

Recommended v4 citation:

- `zhang2024extract_define_canonicalize`

Suggested Related Work sentence:

> LLM-based KG construction pipelines increasingly combine extraction with definition and canonicalization steps, which parallels AutoTeaKG-Silver's separation of extraction patches from vocabulary-normalized KG export \cite{zhang2024extract_define_canonicalize}.

## Recommended v4 Related Work Subsection

Suggested heading:

`Scientific information extraction and biomedical knowledge graphs`

Suggested paragraph:

> AutoTeaKG-Silver also builds on scientific information extraction and biomedical KG research. Scientific text extraction studies show that LLMs can produce structured outputs from papers when prompts are constrained by schemas and domain-specific instructions \cite{dagdelen2024structured_ie_llm,polak2024materials_data_llm}. Biomedical literature-mining systems such as SemMedDB, PubTator 3.0, and BioPREP demonstrate that PubMed-scale text can be transformed into structured biomedical entities and relations \cite{kilicoglu2012semmeddb,chen2024pubtator3,hong2021bioprep_semmeddb}. Domain language models including SciBERT, BioBERT, and PubMedBERT further show the value of scientific and biomedical pretraining for text mining \cite{beltagy2019scibert,lee2020biobert,gu2021pubmedbert}. Biomedical KGs such as Hetionet and PrimeKG, and mechanism-assembly systems such as INDRA, demonstrate the utility of graph representations for biomedical reasoning \cite{himmelstein2017hetionet,chandak2023primekg,gyori2023automated_assembly_indra}. AutoTeaKG-Silver differs from these systems by focusing on tea functional activity evidence and by treating processing context, evidence level, provenance, and uncertainty as first-class graph attributes.

## Verified BibTeX Keys Added

- `dagdelen2024structured_ie_llm`
- `polak2024materials_data_llm`
- `chen2024pubtator3`
- `kilicoglu2012semmeddb`
- `gyori2023automated_assembly_indra`
- `himmelstein2017hetionet`
- `chandak2023primekg`
- `zeng2021kg_drug_repurposing_covid`
- `hong2021bioprep_semmeddb`
- `zhang2024extract_define_canonicalize`
- `beltagy2019scibert`
- `lee2020biobert`
- `gu2021pubmedbert`
