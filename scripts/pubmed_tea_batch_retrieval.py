import argparse
import csv
import json
import math
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "scripts" / "pubmed_tea_queries_v1.json"
DEFAULT_OUTPUT_ROOT = ROOT / "data" / "pubmed_batches"

RAW_FIELDS = [
    "pmid",
    "query_ids",
    "title",
    "abstract",
    "authors",
    "journal",
    "year",
    "pubdate",
    "doi",
    "publication_types",
    "mesh_terms",
    "keywords",
]

NORMALIZED_FIELDS = [
    "paper_id",
    "source_db",
    "title",
    "authors",
    "journal",
    "year",
    "doi",
    "pmid",
    "study_type",
    "tea_type",
    "material_form",
    "component_group",
    "activity_category",
    "processing_present",
    "extraction_present",
    "microbiome_present",
    "include_status",
    "exclusion_reason",
    "notes",
]

SEARCH_LOG_FIELDS = [
    "search_id",
    "date_searched",
    "database",
    "query_name",
    "query_string",
    "date_filter",
    "result_count",
    "export_filename",
    "notes",
]

NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_csv(path: Path, fields, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def fetch_url(url: str, pause: float) -> str:
    with urllib.request.urlopen(url, timeout=60) as response:
        text = response.read().decode("utf-8")
    if pause > 0:
        time.sleep(pause)
    return text


def build_url(endpoint: str, params: dict) -> str:
    return f"{NCBI_BASE}/{endpoint}?{urllib.parse.urlencode(params)}"


def esearch(query: str, mindate: str, maxdate: str, retmax: int, api_key: str, email: str, pause: float):
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax,
        "retstart": 0,
        "sort": "pub date",
        "usehistory": "n",
        "datetype": "pdat",
        "mindate": mindate,
        "maxdate": maxdate,
    }
    if api_key:
        params["api_key"] = api_key
    if email:
        params["email"] = email
    payload = json.loads(fetch_url(build_url("esearch.fcgi", params), pause))
    result = payload["esearchresult"]
    count = int(result.get("count", 0))
    return count, result.get("idlist", [])


def chunked(seq, size: int):
    for idx in range(0, len(seq), size):
        yield seq[idx : idx + size]


def esummary(pmids, api_key: str, email: str, pause: float):
    if not pmids:
        return {}
    params = {
        "db": "pubmed",
        "retmode": "json",
        "id": ",".join(pmids),
    }
    if api_key:
        params["api_key"] = api_key
    if email:
        params["email"] = email
    payload = json.loads(fetch_url(build_url("esummary.fcgi", params), pause))
    return payload.get("result", {})


def efetch_abstracts(pmids, api_key: str, email: str, pause: float):
    if not pmids:
        return {}
    params = {
        "db": "pubmed",
        "retmode": "xml",
        "id": ",".join(pmids),
    }
    if api_key:
        params["api_key"] = api_key
    if email:
        params["email"] = email
    xml_text = fetch_url(build_url("efetch.fcgi", params), pause)
    root = ET.fromstring(xml_text)
    abstracts = {}
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//MedlineCitation/PMID", default="").strip()
        parts = []
        for abstract_text in article.findall(".//Abstract/AbstractText"):
            label = abstract_text.attrib.get("Label", "").strip()
            text = "".join(abstract_text.itertext()).strip()
            if not text:
                continue
            parts.append(f"{label}: {text}" if label else text)
        if pmid:
            abstracts[pmid] = " ".join(parts)
    return abstracts


def infer_study_type(text: str, publication_types: str) -> str:
    full = f"{text} {publication_types}".lower()
    if any(
        term in full
        for term in [
            "stem cuttings",
            "adventitious root",
            "tea plant",
            "leaf color",
            "flavor analysis",
            "sensory evaluation",
        ]
    ):
        return "plant/agronomy study"
    if "meta-analysis" in full:
        return "meta-analysis"
    if "systematic review" in full or "review" in full:
        return "systematic review"
    if "randomized controlled trial" in full or "randomized" in full or "placebo-controlled" in full:
        return "randomized controlled trial"
    if "cohort" in full or "prospective study" in full:
        return "cohort study"
    if "mice" in full or "mouse" in full or "rat" in full or "murine" in full:
        return "animal study"
    if "cell" in full or "in vitro" in full:
        return "in vitro"
    return "unspecified"


def infer_tea_type(text: str) -> str:
    lower = text.lower()
    if "green tea" in lower:
        return "green tea"
    if "oolong tea" in lower:
        return "oolong tea"
    if "black tea" in lower:
        return "black tea"
    if "white tea" in lower:
        return "white tea"
    if "yellow tea" in lower:
        return "yellow tea"
    if "dark tea" in lower or "heimao tea" in lower:
        return "dark tea"
    if "fermented tea" in lower or "kombucha" in lower:
        return "fermented tea"
    if "tea flower" in lower:
        return "tea flower"
    return "unspecified tea"


def infer_material_form(text: str) -> str:
    lower = text.lower()
    if "kombucha" in lower:
        return "fermented beverage"
    if "extract" in lower:
        return "tea extract"
    if "polysaccharide" in lower or "polyphenol" in lower or "catechin" in lower or "theaflavin" in lower:
        return "purified component"
    if "consumption" in lower or "beverage" in lower or "drinking tea" in lower:
        return "tea infusion"
    if "leaf" in lower or "processing" in lower:
        return "tea leaf"
    return "unspecified material"


def infer_component_group(text: str) -> str:
    lower = text.lower()
    if "theaflavin" in lower:
        return "theaflavins"
    if "theanine" in lower:
        return "theanine"
    if "caffeine" in lower:
        return "caffeine"
    if "polysaccharide" in lower:
        return "tea polysaccharides"
    if "catechin" in lower or "egcg" in lower:
        return "catechins"
    if "polyphenol" in lower:
        return "mixed polyphenols"
    if "extract" in lower:
        return "whole extract"
    return "multiple component groups"


def infer_activity_category(text: str) -> str:
    lower = text.lower()
    if "microbiota" in lower or "microbiome" in lower:
        return "gut microbiota modulation"
    if "obesity" in lower or "thermogenesis" in lower or "adipose" in lower:
        return "anti-obesity"
    if "metabolic" in lower or "glucose" in lower or "nafld" in lower or "insulin" in lower:
        return "metabolic improvement"
    if "neuroprotect" in lower or "cognition" in lower or "microglia" in lower or "brain" in lower:
        return "neuroprotection"
    if "cardiovascular" in lower or "mortality" in lower or "vascular" in lower:
        return "cardiovascular protection"
    if "anti-inflammatory" in lower or "inflammation" in lower:
        return "anti-inflammatory"
    if "antioxidant" in lower or "oxidative stress" in lower:
        return "antioxidant"
    return "other"


def yes_no(flag: bool) -> str:
    return "yes" if flag else "no"


def infer_include_status(text: str, study_type: str) -> tuple[str, str]:
    lower = text.lower()
    has_tea = any(term in lower for term in ["tea", "camellia sinensis", "kombucha"])
    has_function = any(
        term in lower
        for term in [
            "microbiota",
            "microbiome",
            "obesity",
            "metabolic",
            "anti-inflammatory",
            "inflammation",
            "antioxidant",
            "neuroprotect",
            "cognition",
            "cardiovascular",
            "bioactive",
            "functional",
        ]
    )
    analytical_only = any(
        term in lower
        for term in [
            "sensor",
            "spectroscopy",
            "authentication",
            "machine vision",
            "pesticide residue",
            "packaging",
            "stem cuttings",
            "adventitious root",
            "tea plant",
            "flavor analysis",
            "sensory evaluation",
            "harvest maturity",
            "quality formation",
        ]
    )
    if study_type == "plant/agronomy study":
        return "exclude", "Out of scope: plant/agronomy rather than functional activity evidence."
    if analytical_only or not has_tea:
        return "exclude", "Out of scope for tea functional activity evidence."
    if has_function and study_type != "unspecified":
        return "include", ""
    if has_function:
        return "maybe", ""
    return "maybe", ""


def normalize_record(raw: dict) -> dict:
    text = " ".join(
        [
            raw.get("title", ""),
            raw.get("abstract", ""),
            raw.get("publication_types", ""),
            raw.get("mesh_terms", ""),
            raw.get("keywords", ""),
        ]
    )
    study_type = infer_study_type(text, raw.get("publication_types", ""))
    include_status, exclusion_reason = infer_include_status(text, study_type)
    processing_present = any(
        token in text.lower()
        for token in ["processing", "fermentation", "withering", "rolling", "drying"]
    )
    extraction_present = any(
        token in text.lower()
        for token in ["extraction", "extract", "ultrasound extraction", "microwave extraction", "supercritical"]
    )
    microbiome_present = any(
        token in text.lower()
        for token in ["microbiota", "microbiome", "scfa", "short-chain fatty acid", "butyrate", "bile acid"]
    )
    notes = []
    if raw.get("query_ids"):
        notes.append(f"matched_queries={raw['query_ids']}")
    if raw.get("abstract"):
        notes.append("abstract_saved_in_raw_batch")
    return {
        "paper_id": f"PMID_{raw['pmid']}",
        "source_db": "PubMed",
        "title": raw.get("title", ""),
        "authors": raw.get("authors", ""),
        "journal": raw.get("journal", ""),
        "year": raw.get("year", ""),
        "doi": raw.get("doi", ""),
        "pmid": raw.get("pmid", ""),
        "study_type": study_type,
        "tea_type": infer_tea_type(text),
        "material_form": infer_material_form(text),
        "component_group": infer_component_group(text),
        "activity_category": infer_activity_category(text),
        "processing_present": yes_no(processing_present),
        "extraction_present": yes_no(extraction_present),
        "microbiome_present": yes_no(microbiome_present),
        "include_status": include_status,
        "exclusion_reason": exclusion_reason,
        "notes": "; ".join(notes),
    }


def clean_authors(author_list) -> str:
    names = []
    for author in author_list or []:
        name = author.get("name") or ""
        if name:
            names.append(name)
    return "; ".join(names)


def first_item(items, key: str) -> str:
    for item in items or []:
        value = item.get(key, "")
        if value:
            return value
    return ""


def build_raw_records(pmids, query_hits, api_key: str, email: str, pause: float):
    summary_rows = []
    abstracts = {}
    for pmid_chunk in chunked(pmids, 200):
        summary = esummary(pmid_chunk, api_key, email, pause)
        for pmid in pmid_chunk:
            item = summary.get(str(pmid), {})
            if item:
                summary_rows.append(item)
    for pmid_chunk in chunked(pmids, 100):
        abstracts.update(efetch_abstracts(pmid_chunk, api_key, email, pause))
    raw_rows = []
    for item in summary_rows:
        pmid = str(item.get("uid", "")).strip()
        article_ids = item.get("articleids", [])
        doi = ""
        for article_id in article_ids:
            if article_id.get("idtype") == "doi":
                doi = article_id.get("value", "")
                break
        pub_types = item.get("pubtype", [])
        mesh_terms = item.get("meshheadinglist", [])
        keywords = item.get("keywordlist", [])
        raw_rows.append(
            {
                "pmid": pmid,
                "query_ids": ";".join(sorted(query_hits.get(pmid, []))),
                "title": item.get("title", "").strip(),
                "abstract": abstracts.get(pmid, "").strip(),
                "authors": clean_authors(item.get("authors", [])),
                "journal": item.get("fulljournalname", "") or item.get("source", ""),
                "year": str(item.get("pubdate", ""))[:4],
                "pubdate": item.get("pubdate", ""),
                "doi": doi,
                "publication_types": "; ".join(pub_types),
                "mesh_terms": "; ".join(mesh_terms),
                "keywords": "; ".join(keywords),
            }
        )
    raw_rows.sort(key=lambda row: (row["year"], row["pmid"]), reverse=True)
    return raw_rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--batch-name", default=f"tea_pubmed_batch_{date.today().isoformat()}")
    parser.add_argument("--retmax-per-query", type=int, default=300)
    parser.add_argument("--pause-seconds", type=float, default=0.34)
    parser.add_argument("--api-key", default="")
    parser.add_argument("--email", default="")
    args = parser.parse_args()

    config = read_json(args.config)
    output_dir = args.output_root / args.batch_name
    output_dir.mkdir(parents=True, exist_ok=True)

    all_pmids = []
    query_hits = {}
    search_log_rows = []
    query_payload = []

    for index, query in enumerate(config["queries"], start=1):
        count, idlist = esearch(
            query=query["query"],
            mindate=config["mindate"],
            maxdate=config["maxdate"],
            retmax=args.retmax_per_query,
            api_key=args.api_key,
            email=args.email,
            pause=args.pause_seconds,
        )
        search_id = f"S{index:03d}"
        query_payload.append(
            {
                "search_id": search_id,
                "query_id": query["id"],
                "query_name": query["name"],
                "query": query["query"],
                "result_count": count,
                "returned_count": len(idlist),
            }
        )
        search_log_rows.append(
            {
                "search_id": search_id,
                "date_searched": date.today().isoformat(),
                "database": "PubMed",
                "query_name": query["name"],
                "query_string": query["query"],
                "date_filter": f"{config['mindate']}:{config['maxdate']}",
                "result_count": str(count),
                "export_filename": f"{args.batch_name}/normalized_included_papers.csv",
                "notes": f"query_id={query['id']}; returned_top_n={len(idlist)}",
            }
        )
        for pmid in idlist:
            all_pmids.append(pmid)
            query_hits.setdefault(pmid, set()).add(query["id"])

    unique_pmids = sorted(set(all_pmids))
    raw_rows = build_raw_records(unique_pmids, query_hits, args.api_key, args.email, args.pause_seconds)
    normalized_rows = [normalize_record(row) for row in raw_rows]

    summary = {
        "batch_name": args.batch_name,
        "date_searched": date.today().isoformat(),
        "config_file": str(args.config),
        "query_count": len(config["queries"]),
        "requested_retmax_per_query": args.retmax_per_query,
        "total_query_hits": len(all_pmids),
        "unique_pmids": len(unique_pmids),
        "normalized_rows": len(normalized_rows),
        "include_count": sum(1 for row in normalized_rows if row["include_status"] == "include"),
        "maybe_count": sum(1 for row in normalized_rows if row["include_status"] == "maybe"),
        "exclude_count": sum(1 for row in normalized_rows if row["include_status"] == "exclude"),
    }

    write_json(output_dir / "query_manifest.json", query_payload)
    write_json(output_dir / "summary.json", summary)
    write_csv(output_dir / "search_log.csv", SEARCH_LOG_FIELDS, search_log_rows)
    write_csv(output_dir / "pubmed_results_raw.csv", RAW_FIELDS, raw_rows)
    write_csv(output_dir / "normalized_included_papers.csv", NORMALIZED_FIELDS, normalized_rows)

    print(f"Batch written to: {output_dir}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
