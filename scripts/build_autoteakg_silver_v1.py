import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MERGED_DIR = ROOT / "data" / "merged_batches" / "tea_pubmed_batch_2026-03-31_large_v2_llm_merged"
DEFAULT_BATCHES_DIR = ROOT / "data" / "pubmed_batches"
# The local Windows ACL in this workspace may prevent creating new subdirectories
# under data/. Keep the default in reports/ and let callers override --out-dir.
DEFAULT_OUT_DIR = ROOT / "reports" / "autoteakg_silver_v1"

MANUAL_ANNOTATORS = {"codex_v1", "adjudicated"}
AUTO_ANNOTATORS = {"glm5_nvidia", "auto_v1"}

GENERIC_MECHANISMS = {
    "",
    "needs manual extraction",
    "microbiota-associated mechanism",
    "antioxidant activity",
    "antioxidant mechanism",
    "inflammation-related mechanism",
    "metabolite-associated mechanism",
    "modulation of signaling pathways",
    "compound recovery and process efficiency",
    "multiple mechanisms summarized",
    "microbiota-related mechanisms summarized",
}

CONTROLLED_VOCABS = {
    "activity_category": {
        "antioxidant",
        "anti-inflammatory",
        "metabolic improvement",
        "anti-obesity",
        "gut microbiota modulation",
        "neuroprotection",
        "cardiovascular protection",
        "anticancer",
        "other",
    },
    "study_type": {
        "in vitro",
        "animal study",
        "randomized controlled trial",
        "cohort study",
        "meta-analysis",
        "systematic review",
        "unspecified",
    },
    "evidence_level": {
        "low_preclinical",
        "preclinical_in_vivo",
        "human_interventional",
        "human_observational",
        "evidence_synthesis",
        "evidence_synthesis_nonquantitative",
        "in_vitro",
    },
    "effect_direction": {
        "positive",
        "negative",
        "mixed",
        "no_clear_effect",
        "unclear",
    },
}


COMPONENT_PATTERNS = [
    ("catechins", r"\b(catechin|catechins|egcg|epigallocatechin gallate|epicatechin|ecg|egc|gcg)\b"),
    ("theaflavins", r"\b(theaflavin|theaflavins|thearubigin|thearubigins)\b"),
    ("theanine", r"\b(l-theanine|theanine)\b"),
    ("caffeine", r"\b(caffeine)\b"),
    ("tea polysaccharides", r"\b(tea polysaccharide|tea polysaccharides|polysaccharide|polysaccharides|tps)\b"),
    ("volatile compounds", r"\b(volatile compound|volatile compounds|aroma compound|aroma compounds)\b"),
    ("mixed polyphenols", r"\b(polyphenol|polyphenols|phenolic|phenolics|flavonoid|flavonoids)\b"),
    ("whole extract", r"\b(tea extract|green tea extract|black tea extract|aqueous extract|ethanol extract|extracts?)\b"),
]

TEA_TYPE_PATTERNS = [
    ("fermented tea beverage", r"\b(kombucha|fermented beverage|scoby)\b"),
    ("dark/post-fermented tea", r"\b(dark tea|post-fermented tea|post fermented tea|pu-?erh|puerh|pu'er)\b"),
    ("yellow tea", r"\byellow tea\b"),
    ("oolong tea", r"\boolong tea\b"),
    ("white tea", r"\bwhite tea\b"),
    ("black tea", r"\bblack tea\b"),
    ("green tea", r"\bgreen tea\b"),
    ("fermented tea", r"\bfermented tea\b"),
    ("unspecified tea", r"\b(tea|camellia sinensis)\b"),
]

PROCESSING_PATTERNS = [
    ("fermentation/oxidation", r"\b(fermentation|fermented|microbial fermentation|kombucha|scoby|oxidized tea|oxidation process)\b"),
    ("withering", r"\b(withering|withered)\b"),
    ("rolling", r"\b(rolling|rolled)\b"),
    ("drying", r"\b(tea drying|dried tea|drying process|drying temperature|drying periods?|dried leaves|freeze-dried tea|spray-dried tea)\b"),
    ("roasting", r"\b(roasting|roasted|baking|baked)\b"),
    ("steaming", r"\b(steaming|steamed)\b"),
    ("pan-firing/fixation", r"\b(pan-?firing|fixation|kill-?green|de-enzyming|enzyme inactivation)\b"),
    ("storage/aging", r"\b(storage|stored|post-fermentation|post-fermented|aged tea|aging years?|aging process|aging periods?|aged liupao|liupao tea)\b"),
    ("enzymatic treatment", r"\b(enzymatic|enzyme-assisted|enzymolysis)\b"),
]

EXTRACTION_PATTERNS = [
    ("ultrasound-assisted extraction", r"\b(ultrasound extraction|ultrasound-assisted extraction|ultrasonic extraction)\b"),
    ("microwave-assisted extraction", r"\b(microwave extraction|microwave-assisted extraction)\b"),
    ("supercritical fluid extraction", r"\b(supercritical|supercritical co2|supercritical carbon dioxide)\b"),
    ("pressurized liquid extraction", r"\b(pressurized liquid extraction|accelerated solvent extraction|subcritical water)\b"),
    ("enzyme-assisted extraction", r"\b(enzyme-assisted extraction|enzymatic extraction)\b"),
    ("ethanol extraction", r"\b(ethanol extract|ethanolic extract|alcohol extract)\b"),
    ("aqueous extraction", r"\b(aqueous extract|water extract|hot water extract|water extraction|infusion|decoction)\b"),
    ("solvent extraction", r"\b(solvent extraction|methanol extract|ethyl acetate extract|extraction solvent)\b"),
    ("other extraction", r"\b(extract|extraction|extracted)\b"),
]

MATERIAL_PATTERNS = [
    ("fermented beverage", r"\b(kombucha|fermented beverage|scoby)\b"),
    ("tea extract", r"\b(tea extract|extract|extracted)\b"),
    ("purified component", r"\b(egcg|theanine|caffeine|catechin|polyphenol|polysaccharide|theaflavin)\b"),
    ("tea infusion", r"\b(tea consumption|tea intake|tea drinking|infusion|beverage)\b"),
    ("tea leaf", r"\b(tea leaf|tea leaves|camellia sinensis leaf)\b"),
]


BASE_RECORD_FIELDS = [
    "record_id",
    "paper_id",
    "tea_type",
    "material_form",
    "component_group",
    "compound_name",
    "activity_category",
    "endpoint_label",
    "study_type",
    "evidence_level",
    "model_system",
    "dose_exposure",
    "effect_direction",
    "processing_step",
    "extraction_method",
    "cultivar",
    "origin",
    "mechanism_label",
    "microbiota_taxon",
    "microbial_metabolite",
    "host_phenotype",
    "claim_text_raw",
    "confidence_score",
    "annotator_id",
    "adjudication_status",
    "notes",
]

SILVER_EXTRA_FIELDS = [
    "title",
    "abstract",
    "journal",
    "year",
    "source_is_auto_only",
    "silver_tea_type",
    "silver_material_form",
    "silver_component_group",
    "silver_processing_step",
    "silver_extraction_method",
    "component_evidence_terms",
    "processing_evidence_terms",
    "extraction_evidence_terms",
    "schema_validation_flags",
    "uncertainty_flags",
    "record_specificity_score",
    "mechanism_specificity_score",
    "context_completeness_score",
    "silver_confidence_score",
    "uncertainty_class",
]

SILVER_FIELDS = BASE_RECORD_FIELDS + SILVER_EXTRA_FIELDS


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


def slug(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "unknown"


def split_values(value: str):
    if not value:
        return []
    parts = re.split(r";|\|", value)
    return [part.strip() for part in parts if part.strip()]


def normalize_blank(value: str) -> str:
    value = (value or "").strip()
    if value.lower() in {"", "unspecified", "unknown", "not_applicable", "na", "n/a"}:
        return ""
    return value


def load_raw_pubmed_lookup(batches_dir: Path):
    lookup = {}
    for path in sorted(batches_dir.glob("**/pubmed_results_raw.csv")):
        for row in read_csv(path):
            pmid = (row.get("pmid") or "").strip()
            if not pmid:
                continue
            paper_id = f"PMID_{pmid}"
            abstract = (row.get("abstract") or "").strip()
            existing = lookup.get(paper_id, {})
            if not existing or (abstract and not existing.get("abstract", "")):
                lookup[paper_id] = {
                    "title": (row.get("title") or "").strip(),
                    "abstract": abstract,
                    "authors": (row.get("authors") or "").strip(),
                    "journal": (row.get("journal") or "").strip(),
                    "year": (row.get("year") or "").strip(),
                    "doi": (row.get("doi") or "").strip(),
                    "raw_source_file": str(path.relative_to(ROOT)),
                }
    return lookup


def detect_patterns(text: str, patterns):
    lowered = text.lower()
    values = []
    evidence_terms = []
    for label, pattern in patterns:
        matches = re.findall(pattern, lowered, flags=re.IGNORECASE)
        if matches:
            values.append(label)
            flat = []
            for match in matches:
                if isinstance(match, tuple):
                    flat.extend(item for item in match if item)
                else:
                    flat.append(match)
            evidence_terms.extend(flat[:4])
    deduped_values = []
    seen = set()
    for value in values:
        if value not in seen:
            deduped_values.append(value)
            seen.add(value)
    deduped_terms = []
    seen_terms = set()
    for term in evidence_terms:
        term = str(term).strip()
        if term and term not in seen_terms:
            deduped_terms.append(term)
            seen_terms.add(term)
    return "; ".join(deduped_values), "; ".join(deduped_terms)


def prefer_existing_or_extracted(existing: str, extracted: str, generic_values):
    existing = normalize_blank(existing)
    if existing and existing.lower() not in generic_values:
        return existing
    return extracted or existing


def confidence_to_float(value: str) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def specificity_for_value(value: str, generic_values) -> float:
    value = normalize_blank(value)
    if not value:
        return 0.0
    lower = value.lower()
    if lower in generic_values:
        return 0.25
    if ";" in value:
        return 1.0
    return 0.75


def mechanism_specificity(mechanism: str, microbiota: str, metabolite: str) -> float:
    mechanism = (mechanism or "").strip()
    if microbiota or metabolite:
        base = 0.75
    elif not mechanism:
        base = 0.0
    elif mechanism.lower() in GENERIC_MECHANISMS:
        base = 0.25
    elif any(token in mechanism.lower() for token in ["pathway", "signaling", "axis", "scfa", "bile", "nf-", "mapk", "nrf2"]):
        base = 0.85
    else:
        base = 0.55
    return min(base, 1.0)


def context_completeness(tea_type: str, component_group: str, processing_step: str, extraction_method: str) -> float:
    score = 0.0
    if normalize_blank(tea_type) and tea_type.lower() != "unspecified tea":
        score += 0.25
    if normalize_blank(component_group):
        score += 0.30
    if normalize_blank(processing_step):
        score += 0.25
    if normalize_blank(extraction_method):
        score += 0.20
    return round(score, 3)


def validate_schema(row):
    flags = []
    for field, vocab in CONTROLLED_VOCABS.items():
        value = (row.get(field) or "").strip()
        if value and value not in vocab:
            flags.append(f"invalid_{field}")
    if not row.get("paper_id"):
        flags.append("missing_paper_id")
    if not row.get("claim_text_raw") and not row.get("abstract"):
        flags.append("missing_claim_and_abstract")
    return flags


def assign_uncertainty(row):
    flags = []
    confidence = confidence_to_float(row.get("confidence_score"))
    if confidence < 0.80:
        flags.append("low_llm_confidence")
    if row.get("activity_category") == "other":
        flags.append("taxonomy_expansion_needed")
    if not normalize_blank(row.get("silver_component_group")):
        flags.append("missing_component_context")
    if not normalize_blank(row.get("silver_processing_step")) and not normalize_blank(row.get("silver_extraction_method")):
        flags.append("missing_processing_or_extraction_context")
    if (row.get("mechanism_label") or "").strip().lower() in GENERIC_MECHANISMS:
        flags.append("generic_mechanism")
    if not row.get("microbiota_taxon") and row.get("activity_category") == "gut microbiota modulation":
        flags.append("missing_named_microbiota")
    if row.get("study_type") == "animal study":
        flags.append("preclinical_only")
    if row.get("study_type") == "systematic review":
        flags.append("review_summary_record")
    if row.get("evidence_level") in {"low_preclinical", "in_vitro"}:
        flags.append("low_evidence_level")
    if row.get("effect_direction") in {"unclear", "no_clear_effect", "mixed"}:
        flags.append("uncertain_effect_direction")
    if not row.get("abstract"):
        flags.append("missing_abstract")
    flags.extend(validate_schema(row))
    return sorted(set(flags))


def classify_uncertainty(flags, silver_confidence: float) -> str:
    severe = {
        "low_llm_confidence",
        "taxonomy_expansion_needed",
        "missing_component_context",
        "generic_mechanism",
        "invalid_activity_category",
        "invalid_study_type",
        "invalid_evidence_level",
    }
    severe_count = sum(flag in severe for flag in flags)
    if silver_confidence >= 0.80 and severe_count == 0:
        return "low_uncertainty"
    if silver_confidence >= 0.60 and severe_count <= 2:
        return "moderate_uncertainty"
    return "high_uncertainty"


def enrich_record(record, paper, raw_pubmed):
    title = paper.get("title") or raw_pubmed.get("title", "")
    abstract = raw_pubmed.get("abstract", "")
    journal = paper.get("journal") or raw_pubmed.get("journal", "")
    year = paper.get("year") or raw_pubmed.get("year", "")
    text = " ".join(
        [
            title,
            abstract,
            record.get("claim_text_raw", ""),
            record.get("endpoint_label", ""),
            record.get("mechanism_label", ""),
            record.get("tea_type", ""),
            record.get("component_group", ""),
            record.get("processing_step", ""),
            record.get("extraction_method", ""),
        ]
    )

    extracted_tea_type, _ = detect_patterns(text, TEA_TYPE_PATTERNS)
    extracted_material, _ = detect_patterns(text, MATERIAL_PATTERNS)
    extracted_component, component_terms = detect_patterns(text, COMPONENT_PATTERNS)
    extracted_processing, processing_terms = detect_patterns(text, PROCESSING_PATTERNS)
    extracted_extraction, extraction_terms = detect_patterns(text, EXTRACTION_PATTERNS)

    enriched = {field: record.get(field, "") for field in BASE_RECORD_FIELDS}
    enriched.update(
        {
            "title": title,
            "abstract": abstract,
            "journal": journal,
            "year": year,
            "source_is_auto_only": "true",
            "silver_tea_type": prefer_existing_or_extracted(
                record.get("tea_type", ""),
                extracted_tea_type,
                {"unspecified tea"},
            ),
            "silver_material_form": prefer_existing_or_extracted(
                record.get("material_form", ""),
                extracted_material,
                {"unspecified material"},
            ),
            "silver_component_group": prefer_existing_or_extracted(
                record.get("component_group", ""),
                extracted_component,
                {"unspecified", "multiple component groups"},
            ),
            "silver_processing_step": prefer_existing_or_extracted(
                record.get("processing_step", ""),
                extracted_processing,
                set(),
            ),
            "silver_extraction_method": prefer_existing_or_extracted(
                record.get("extraction_method", ""),
                extracted_extraction,
                set(),
            ),
            "component_evidence_terms": component_terms,
            "processing_evidence_terms": processing_terms,
            "extraction_evidence_terms": extraction_terms,
        }
    )

    mech_score = mechanism_specificity(
        enriched.get("mechanism_label", ""),
        enriched.get("microbiota_taxon", ""),
        enriched.get("microbial_metabolite", ""),
    )
    context_score = context_completeness(
        enriched.get("silver_tea_type", ""),
        enriched.get("silver_component_group", ""),
        enriched.get("silver_processing_step", ""),
        enriched.get("silver_extraction_method", ""),
    )
    component_score = specificity_for_value(
        enriched.get("silver_component_group", ""),
        {"unspecified", "multiple component groups"},
    )
    tea_score = specificity_for_value(
        enriched.get("silver_tea_type", ""),
        {"unspecified tea"},
    )
    llm_confidence = confidence_to_float(enriched.get("confidence_score"))
    record_specificity = round((component_score + tea_score + mech_score + context_score) / 4, 3)
    silver_confidence = round((0.55 * llm_confidence) + (0.25 * record_specificity) + (0.20 * context_score), 3)

    schema_flags = validate_schema(enriched)
    uncertainty_flags = assign_uncertainty(enriched)
    enriched.update(
        {
            "schema_validation_flags": "; ".join(schema_flags),
            "uncertainty_flags": "; ".join(uncertainty_flags),
            "record_specificity_score": f"{record_specificity:.3f}",
            "mechanism_specificity_score": f"{mech_score:.3f}",
            "context_completeness_score": f"{context_score:.3f}",
            "silver_confidence_score": f"{silver_confidence:.3f}",
            "uncertainty_class": classify_uncertainty(uncertainty_flags, silver_confidence),
        }
    )
    return enriched


def build_silver_records(merged_dir: Path, batches_dir: Path):
    papers = read_csv(merged_dir / "included_papers_llm_merged.csv")
    records = read_csv(merged_dir / "evidence_records_llm_merged.csv")
    papers_by_id = {row.get("paper_id", ""): row for row in papers}
    raw_lookup = load_raw_pubmed_lookup(batches_dir)
    silver_records = []
    excluded_counts = Counter()

    for record in records:
        annotator = record.get("annotator_id", "")
        if annotator in MANUAL_ANNOTATORS:
            excluded_counts["manual_annotator"] += 1
            continue
        if annotator not in AUTO_ANNOTATORS:
            excluded_counts["non_standard_auto_or_malformed_annotator"] += 1
            continue
        paper_id = record.get("paper_id", "")
        paper = papers_by_id.get(paper_id, {})
        raw_pubmed = raw_lookup.get(paper_id, {})
        silver_records.append(enrich_record(record, paper, raw_pubmed))

    return papers, silver_records, excluded_counts


def add_node(nodes, node_id, node_type, label, **attrs):
    if node_id not in nodes:
        row = {"node_id": node_id, "node_type": node_type, "label": label}
        row.update(attrs)
        nodes[node_id] = row


def add_edge(edges, source_id, target_id, edge_type, record, **attrs):
    base = {
        "source_id": source_id,
        "target_id": target_id,
        "edge_type": edge_type,
        "record_id": record.get("record_id", ""),
        "paper_id": record.get("paper_id", ""),
        "confidence_score": record.get("silver_confidence_score", ""),
        "uncertainty_class": record.get("uncertainty_class", ""),
        "uncertainty_flags": record.get("uncertainty_flags", ""),
        "evidence_level": record.get("evidence_level", ""),
        "study_type": record.get("study_type", ""),
        "effect_direction": record.get("effect_direction", ""),
    }
    base.update(attrs)
    edges.append(base)


def keep_graph_value(value: str) -> bool:
    value = normalize_blank(value)
    return bool(value) and value.lower() not in {"needs manual extraction", "candidate endpoint from title"}


def build_kg_v3(silver_records):
    nodes = {}
    edges = []
    for record in silver_records:
        paper_id = record.get("paper_id", "")
        record_id = record.get("record_id", "")
        paper_node = f"paper:{paper_id}"
        record_node = f"record:{record_id}"
        add_node(
            nodes,
            paper_node,
            "Paper",
            paper_id,
            title=record.get("title", ""),
            year=record.get("year", ""),
            journal=record.get("journal", ""),
        )
        add_node(
            nodes,
            record_node,
            "EvidenceRecord",
            record_id,
            claim_text_raw=record.get("claim_text_raw", ""),
            confidence_score=record.get("silver_confidence_score", ""),
            uncertainty_class=record.get("uncertainty_class", ""),
            uncertainty_flags=record.get("uncertainty_flags", ""),
            context_completeness_score=record.get("context_completeness_score", ""),
            mechanism_specificity_score=record.get("mechanism_specificity_score", ""),
        )
        add_edge(edges, paper_node, record_node, "HAS_RECORD", record)

        node_specs = [
            ("silver_tea_type", "TeaType", "HAS_TEA_TYPE", "tea_type"),
            ("silver_material_form", "MaterialForm", "HAS_MATERIAL_FORM", "material_form"),
            ("silver_component_group", "ComponentGroup", "HAS_COMPONENT_GROUP", "component_group"),
            ("silver_processing_step", "ProcessingStep", "HAS_PROCESSING_STEP", "processing_step"),
            ("silver_extraction_method", "ExtractionMethod", "HAS_EXTRACTION_METHOD", "extraction_method"),
            ("activity_category", "ActivityCategory", "SUPPORTS_ACTIVITY", "activity"),
            ("study_type", "StudyType", "HAS_STUDY_TYPE", "study_type"),
            ("evidence_level", "EvidenceLevel", "HAS_EVIDENCE_LEVEL", "evidence_level"),
            ("effect_direction", "EffectDirection", "HAS_EFFECT_DIRECTION", "effect_direction"),
        ]
        for field, node_type, edge_type, prefix in node_specs:
            for value in split_values(record.get(field, "")):
                if keep_graph_value(value):
                    node_id = f"{prefix}:{slug(value)}"
                    add_node(nodes, node_id, node_type, value)
                    add_edge(edges, record_node, node_id, edge_type, record)

        for mechanism in split_values(record.get("mechanism_label", "")):
            if keep_graph_value(mechanism):
                node_id = f"mechanism:{slug(mechanism)}"
                add_node(nodes, node_id, "Mechanism", mechanism)
                add_edge(edges, record_node, node_id, "ACTS_VIA", record)

        for taxon in split_values(record.get("microbiota_taxon", "")):
            if keep_graph_value(taxon):
                node_id = f"microbiota:{slug(taxon)}"
                add_node(nodes, node_id, "MicrobiotaFeature", taxon)
                add_edge(edges, record_node, node_id, "MODULATES_MICROBIOTA", record)

        for metabolite in split_values(record.get("microbial_metabolite", "")):
            if keep_graph_value(metabolite):
                node_id = f"metabolite:{slug(metabolite)}"
                add_node(nodes, node_id, "MicrobialMetabolite", metabolite)
                add_edge(edges, record_node, node_id, "LINKS_TO_METABOLITE", record)

        for phenotype in split_values(record.get("host_phenotype", "")):
            if keep_graph_value(phenotype):
                node_id = f"phenotype:{slug(phenotype)}"
                add_node(nodes, node_id, "HostPhenotype", phenotype)
                add_edge(edges, record_node, node_id, "ASSOCIATED_HOST_PHENOTYPE", record)

        for flag in split_values(record.get("uncertainty_flags", "")):
            node_id = f"uncertainty:{slug(flag)}"
            add_node(nodes, node_id, "UncertaintyFlag", flag)
            add_edge(edges, record_node, node_id, "HAS_UNCERTAINTY_FLAG", record)

    return list(nodes.values()), edges


def summarize_records(silver_records, excluded_counts, nodes, edges):
    def count(field):
        return Counter(row.get(field, "") for row in silver_records)

    summary = {
        "date": "2026-04-12",
        "mode": "auto_only_silver_no_manual_annotation_dependency",
        "silver_record_count": len(silver_records),
        "excluded_counts": dict(excluded_counts),
        "kg_v3_node_count": len(nodes),
        "kg_v3_edge_count": len(edges),
        "uncertainty_class_counts": dict(count("uncertainty_class")),
        "activity_counts": dict(count("activity_category")),
        "study_type_counts": dict(count("study_type")),
        "silver_component_group_counts": dict(count("silver_component_group")),
        "silver_processing_step_counts": dict(count("silver_processing_step")),
        "silver_extraction_method_counts": dict(count("silver_extraction_method")),
        "uncertainty_flag_counts": dict(
            Counter(flag for row in silver_records for flag in split_values(row.get("uncertainty_flags", "")))
        ),
        "node_type_counts": dict(Counter(row.get("node_type", "") for row in nodes)),
        "edge_type_counts": dict(Counter(row.get("edge_type", "") for row in edges)),
    }
    return summary


def write_markdown_summary(path: Path, summary, out_dir: Path):
    lines = [
        "# AutoTeaKG-Silver v1 Summary",
        "",
        "Date: 2026-04-12",
        "",
        "This run builds an auto-only silver-standard evidence layer and uncertainty-aware KG v3. Manual adjudication and manual audit files are not used as construction inputs.",
        "",
        "## Outputs",
        "",
        f"- Silver records: `{out_dir / 'autoteakg_silver_records.csv'}`",
        f"- Processing/component report: `{out_dir / 'processing_component_extraction_report.csv'}`",
        f"- KG v3 nodes: `{out_dir / 'kg_v3' / 'nodes.csv'}`",
        f"- KG v3 edges: `{out_dir / 'kg_v3' / 'edges.csv'}`",
        "",
        "## Counts",
        "",
        f"- Silver records: {summary['silver_record_count']}",
        f"- KG v3 nodes: {summary['kg_v3_node_count']}",
        f"- KG v3 edges: {summary['kg_v3_edge_count']}",
        f"- Excluded records: {summary['excluded_counts']}",
        "",
        "## Uncertainty Classes",
        "",
    ]
    for label, value in sorted(summary["uncertainty_class_counts"].items()):
        lines.append(f"- {label}: {value}")
    lines.extend(["", "## Top Component Groups", ""])
    for label, value in Counter(summary["silver_component_group_counts"]).most_common(12):
        lines.append(f"- {label or '(blank)'}: {value}")
    lines.extend(["", "## Top Processing Steps", ""])
    for label, value in Counter(summary["silver_processing_step_counts"]).most_common(12):
        lines.append(f"- {label or '(blank)'}: {value}")
    lines.extend(["", "## Top Extraction Methods", ""])
    for label, value in Counter(summary["silver_extraction_method_counts"]).most_common(12):
        lines.append(f"- {label or '(blank)'}: {value}")
    lines.extend(["", "## Uncertainty Flags", ""])
    for label, value in Counter(summary["uncertainty_flag_counts"]).most_common(20):
        lines.append(f"- {label}: {value}")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_processing_report(path: Path, silver_records):
    rows = []
    for row in silver_records:
        rows.append(
            {
                "record_id": row.get("record_id", ""),
                "paper_id": row.get("paper_id", ""),
                "title": row.get("title", ""),
                "silver_tea_type": row.get("silver_tea_type", ""),
                "silver_component_group": row.get("silver_component_group", ""),
                "silver_processing_step": row.get("silver_processing_step", ""),
                "silver_extraction_method": row.get("silver_extraction_method", ""),
                "component_evidence_terms": row.get("component_evidence_terms", ""),
                "processing_evidence_terms": row.get("processing_evidence_terms", ""),
                "extraction_evidence_terms": row.get("extraction_evidence_terms", ""),
                "context_completeness_score": row.get("context_completeness_score", ""),
                "uncertainty_class": row.get("uncertainty_class", ""),
                "uncertainty_flags": row.get("uncertainty_flags", ""),
            }
        )
    write_csv(
        path,
        [
            "record_id",
            "paper_id",
            "title",
            "silver_tea_type",
            "silver_component_group",
            "silver_processing_step",
            "silver_extraction_method",
            "component_evidence_terms",
            "processing_evidence_terms",
            "extraction_evidence_terms",
            "context_completeness_score",
            "uncertainty_class",
            "uncertainty_flags",
        ],
        rows,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--merged-dir", type=Path, default=DEFAULT_MERGED_DIR)
    parser.add_argument("--pubmed-batches-dir", type=Path, default=DEFAULT_BATCHES_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    kg_dir = args.out_dir / "kg_v3"
    kg_dir.mkdir(parents=True, exist_ok=True)

    _, silver_records, excluded_counts = build_silver_records(args.merged_dir, args.pubmed_batches_dir)
    nodes, edges = build_kg_v3(silver_records)
    summary = summarize_records(silver_records, excluded_counts, nodes, edges)

    write_csv(args.out_dir / "autoteakg_silver_records.csv", SILVER_FIELDS, silver_records)
    write_processing_report(args.out_dir / "processing_component_extraction_report.csv", silver_records)
    write_csv(
        kg_dir / "nodes.csv",
        sorted({field for row in nodes for field in row.keys()}),
        nodes,
    )
    write_csv(
        kg_dir / "edges.csv",
        sorted({field for row in edges for field in row.keys()}),
        edges,
    )
    (args.out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown_summary(args.out_dir / "summary.md", summary, args.out_dir)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
