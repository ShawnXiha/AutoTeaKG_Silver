import json
import re
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "writing_outputs" / "20260412_autoteakg_silver_paper"
SOURCES_DIR = PAPER_DIR / "sources"
REF_DIR = PAPER_DIR / "references"
OUT_BIB = REF_DIR / "computational_related_work_refs.bib"
OUT_MD = SOURCES_DIR / "papers_20260412_computational_related_work_verified.md"
OUT_JSON = SOURCES_DIR / "papers_20260412_computational_related_work_verified.json"


SELECTED = [
    {
        "key": "dagdelen2024structured_ie_llm",
        "doi": "10.1038/s41467-024-45563-x",
        "theme": "LLM scientific information extraction",
        "why": "Structured extraction from scientific text with LLMs; supports schema-based extraction framing.",
    },
    {
        "key": "polak2024materials_data_llm",
        "doi": "10.1038/s41467-024-45914-8",
        "theme": "LLM scientific information extraction",
        "why": "Conversational LLMs and prompt engineering for extracting materials data from papers.",
    },
    {
        "key": "chen2024pubtator3",
        "doi": "10.1093/nar/gkae235",
        "theme": "Biomedical literature IE resource",
        "why": "PubTator 3.0 is a large-scale AI-powered biomedical literature annotation/search resource.",
    },
    {
        "key": "kilicoglu2012semmeddb",
        "doi": "10.1093/bioinformatics/bts591",
        "theme": "Biomedical literature IE resource",
        "why": "SemMedDB provides PubMed-scale semantic predications extracted from biomedical literature.",
    },
    {
        "key": "gyori2023automated_assembly_indra",
        "doi": "10.15252/msb.202211325",
        "theme": "Mechanistic knowledge assembly",
        "why": "Automated assembly of molecular mechanisms from text mining and curated databases; supports provenance-aware mechanistic graph discussion.",
    },
    {
        "key": "himmelstein2017hetionet",
        "doi": "10.7554/eLife.26726",
        "theme": "Biomedical knowledge graph",
        "why": "Hetionet integrates biomedical knowledge for drug repurposing; important biomedical KG precedent.",
    },
    {
        "key": "chandak2023primekg",
        "doi": "10.1038/s41597-023-01960-3",
        "theme": "Biomedical knowledge graph",
        "why": "PrimeKG is a modern multimodal precision medicine KG with explicit data integration and updateability.",
    },
    {
        "key": "zeng2021kg_drug_repurposing_covid",
        "doi": "10.1021/acs.jcim.1c00642",
        "theme": "Biomedical knowledge graph",
        "why": "Knowledge graph approach for COVID-19 drug repurposing; supports biomedical KG utility examples.",
    },
    {
        "key": "hong2021bioprep_semmeddb",
        "doi": "10.1016/j.jbi.2021.103888",
        "theme": "Biomedical relation extraction",
        "why": "BioPREP uses SemMedDB-derived relation extraction data and deep learning predicate classification.",
    },
    {
        "key": "zhang2024extract_define_canonicalize",
        "doi": "10.18653/v1/2024.emnlp-main.548",
        "theme": "LLM knowledge graph construction",
        "why": "LLM-based extract-define-canonicalize framework for KG construction; directly relevant to LLM KG pipeline discussion.",
    },
    {
        "key": "beltagy2019scibert",
        "doi": "10.18653/v1/D19-1371",
        "theme": "Scientific NLP foundation model",
        "why": "SciBERT is a foundational scientific-domain language model for scientific text mining.",
    },
    {
        "key": "lee2020biobert",
        "doi": "10.1093/bioinformatics/btz682",
        "theme": "Biomedical NLP foundation model",
        "why": "BioBERT is a foundational biomedical language model for biomedical text mining.",
    },
    {
        "key": "gu2021pubmedbert",
        "doi": "10.1145/3458754",
        "theme": "Biomedical NLP foundation model",
        "why": "PubMedBERT supports domain-specific pretraining for biomedical NLP.",
    },
]


def get_bibtex(doi: str) -> str:
    url = f"https://doi.org/{doi}"
    headers = {"Accept": "application/x-bibtex", "User-Agent": "AutoTeaKG citation collection"}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text.strip()


def replace_key(bibtex: str, new_key: str) -> str:
    return re.sub(r"(@\w+\{)[^,]+,", rf"\1{new_key},", bibtex, count=1)


def main():
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    REF_DIR.mkdir(parents=True, exist_ok=True)
    verified = []
    failures = []
    bibs = []
    for item in SELECTED:
        try:
            bib = replace_key(get_bibtex(item["doi"]), item["key"])
            bibs.append(bib)
            verified.append({**item, "bibtex": bib})
            print(f"OK {item['doi']} {item['key']}")
        except Exception as exc:
            failures.append({**item, "error": str(exc)})
            print(f"FAIL {item['doi']} {exc}")
    OUT_BIB.write_text("\n\n".join(bibs) + "\n", encoding="utf-8")
    OUT_JSON.write_text(json.dumps({"verified": verified, "failures": failures}, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# Verified Computational Related Work References",
        "",
        "Date: 2026-04-12",
        "",
        "Scope: scientific information extraction, LLM extraction, biomedical knowledge graphs, and biomedical/scientific NLP models relevant to AutoTeaKG-Silver.",
        "",
        "## Verified References",
        "",
    ]
    for item in verified:
        lines.append(f"### {item['key']}")
        lines.append("")
        lines.append(f"- DOI: `{item['doi']}`")
        lines.append(f"- Theme: {item['theme']}")
        lines.append(f"- Why relevant: {item['why']}")
        lines.append("")
    if failures:
        lines.append("## Failures / Not Added to BibTeX")
        lines.append("")
        for item in failures:
            lines.append(f"- {item['key']} DOI `{item['doi']}`: {item['error']}")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_BIB}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
