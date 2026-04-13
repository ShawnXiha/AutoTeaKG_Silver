import argparse
import csv
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT_RECORDS = ROOT / "reports" / "targeted_processing_vocab_normalized" / "autoteakg_silver_records.csv"
OUT_DIR = ROOT / "reports" / "fulltext_methods_remaining_context"
NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

METHOD_TITLE_PATTERNS = [
    "method",
    "materials",
    "experimental",
    "sample preparation",
    "preparation",
    "extraction",
    "processing",
    "tea preparation",
    "chemicals",
]

CONTEXT_KEYWORDS = [
    "tea",
    "extract",
    "extraction",
    "processing",
    "fermentation",
    "fermented",
    "infusion",
    "decoction",
    "catechin",
    "egcg",
    "polyphenol",
    "polysaccharide",
    "theaflavin",
    "theanine",
    "caffeine",
    "preparation",
]


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def paper_id_to_pmid(paper_id: str) -> str:
    return (paper_id or "").replace("PMID_", "").strip()


def select_remaining_records(records):
    return [
        row
        for row in records
        if row.get("source_is_auto_only") == "true"
        and "missing_processing_or_extraction_context" in row.get("uncertainty_flags", "")
    ]


def http_get(url: str, timeout: int, min_interval: float, last_call: list):
    elapsed = time.time() - last_call[0]
    if elapsed < min_interval:
        time.sleep(min_interval - elapsed)
    request = urllib.request.Request(url, headers={"User-Agent": "AutoTeaKG/0.1 (research; contact=local)"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()
    last_call[0] = time.time()
    return data


def elink_pmid_to_pmcid(pmid: str, timeout: int, min_interval: float, last_call: list) -> str:
    params = urllib.parse.urlencode(
        {
            "dbfrom": "pubmed",
            "db": "pmc",
            "id": pmid,
            "retmode": "json",
            "linkname": "pubmed_pmc",
        }
    )
    url = f"{NCBI_BASE}/elink.fcgi?{params}"
    raw = http_get(url, timeout, min_interval, last_call)
    data = json.loads(raw.decode("utf-8"))
    linksets = data.get("linksets", [])
    for linkset in linksets:
        for linkdb in linkset.get("linksetdbs", []):
            for link in linkdb.get("links", []):
                if link:
                    return f"PMC{link}"
    return ""


def efetch_pmc_xml(pmcid: str, timeout: int, min_interval: float, last_call: list) -> bytes:
    pmc_numeric = pmcid.replace("PMC", "")
    params = urllib.parse.urlencode({"db": "pmc", "id": pmc_numeric, "retmode": "xml"})
    url = f"{NCBI_BASE}/efetch.fcgi?{params}"
    return http_get(url, timeout, min_interval, last_call)


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def element_text(element) -> str:
    return clean_text(" ".join(element.itertext()))


def section_title(sec) -> str:
    for child in list(sec):
        if child.tag.endswith("title"):
            return element_text(child)
    return ""


def section_has_method_title(title: str) -> bool:
    lower = title.lower()
    return any(pattern in lower for pattern in METHOD_TITLE_PATTERNS)


def section_has_context(text: str) -> bool:
    lower = text.lower()
    return any(keyword in lower for keyword in CONTEXT_KEYWORDS)


def extract_sections_from_xml(xml_bytes: bytes):
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []
    sections = []
    for sec in root.iter():
        if not sec.tag.endswith("sec"):
            continue
        title = section_title(sec)
        text = element_text(sec)
        if not text:
            continue
        is_method = section_has_method_title(title)
        has_context = section_has_context(text)
        if is_method or (has_context and len(text) < 6000):
            sections.append(
                {
                    "section_title": title,
                    "is_method_like": str(is_method).lower(),
                    "has_context_keywords": str(has_context).lower(),
                    "section_text": text[:5000],
                    "section_char_count": str(len(text)),
                }
            )
    return sections


def load_cache(path: Path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_cache(path: Path, cache):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")


def retrieve_for_pmids(pmids, args):
    cache_path = args.output_dir / "pmc_lookup_cache.json"
    cache = load_cache(cache_path)
    last_call = [0.0]
    for index, pmid in enumerate(pmids, start=1):
        if pmid in cache and not args.force:
            print(f"[{index}/{len(pmids)}] CACHED {pmid}")
            continue
        row = {"pmid": pmid, "pmcid": "", "retrieval_status": "", "error": "", "sections": []}
        try:
            pmcid = elink_pmid_to_pmcid(pmid, args.timeout_seconds, args.min_interval_seconds, last_call)
            row["pmcid"] = pmcid
            if not pmcid:
                row["retrieval_status"] = "no_pmc_fulltext"
            else:
                xml_bytes = efetch_pmc_xml(pmcid, args.timeout_seconds, args.min_interval_seconds, last_call)
                row["sections"] = extract_sections_from_xml(xml_bytes)
                row["retrieval_status"] = "sections_extracted" if row["sections"] else "pmc_found_no_relevant_sections"
        except Exception as exc:
            row["retrieval_status"] = "error"
            row["error"] = str(exc)
        cache[pmid] = row
        save_cache(cache_path, cache)
        print(f"[{index}/{len(pmids)}] {pmid} {row['retrieval_status']} {row.get('pmcid','')}")
    return cache


def build_outputs(records, cache, out_dir: Path):
    rows = []
    no_fulltext = 0
    with_sections = 0
    by_paper = {}
    for record in records:
        pmid = paper_id_to_pmid(record.get("paper_id", ""))
        item = cache.get(pmid, {})
        sections = item.get("sections") or []
        if not item.get("pmcid"):
            no_fulltext += 1
        if sections:
            with_sections += 1
        combined = "\n\n".join(
            f"[{sec.get('section_title','')}] {sec.get('section_text','')}" for sec in sections[:6]
        )
        rows.append(
            {
                "record_id": record.get("record_id", ""),
                "paper_id": record.get("paper_id", ""),
                "pmid": pmid,
                "pmcid": item.get("pmcid", ""),
                "retrieval_status": item.get("retrieval_status", "not_retrieved"),
                "section_count": str(len(sections)),
                "title": record.get("title", ""),
                "abstract": record.get("abstract", ""),
                "methods_text": combined[:12000],
                "error": item.get("error", ""),
            }
        )
        by_paper[pmid] = item
    write_csv(
        out_dir / "remaining_context_methods_sections.csv",
        [
            "record_id",
            "paper_id",
            "pmid",
            "pmcid",
            "retrieval_status",
            "section_count",
            "title",
            "abstract",
            "methods_text",
            "error",
        ],
        rows,
    )
    summary = {
        "record_count": len(records),
        "paper_count": len({paper_id_to_pmid(row.get("paper_id", "")) for row in records}),
        "records_with_pmcid": sum(1 for row in rows if row["pmcid"]),
        "records_with_methods_sections": with_sections,
        "records_without_pmc_fulltext": no_fulltext,
        "paper_status_counts": {},
    }
    for item in by_paper.values():
        status = item.get("retrieval_status", "not_retrieved")
        summary["paper_status_counts"][status] = summary["paper_status_counts"].get(status, 0) + 1
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=INPUT_RECORDS)
    parser.add_argument("--output-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--max-papers", type=int, default=None)
    parser.add_argument("--record-ids", nargs="*", default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--min-interval-seconds", type=float, default=0.34)
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    all_records = read_csv(args.input)
    remaining = select_remaining_records(all_records)
    if args.record_ids:
        wanted = set(args.record_ids)
        remaining = [row for row in remaining if row.get("record_id") in wanted]
    pmids = sorted({paper_id_to_pmid(row.get("paper_id", "")) for row in remaining if row.get("paper_id")})
    if args.max_papers is not None:
        pmids = pmids[: args.max_papers]
        remaining = [row for row in remaining if paper_id_to_pmid(row.get("paper_id", "")) in set(pmids)]

    if args.fetch:
        cache = retrieve_for_pmids(pmids, args)
    else:
        cache = load_cache(args.output_dir / "pmc_lookup_cache.json")
    summary = build_outputs(remaining, cache, args.output_dir)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
