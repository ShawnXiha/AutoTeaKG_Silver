import argparse
import csv
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_DIR = ROOT / "data"
DB_PATH = DB_DIR / "teakg_v1.sqlite"

DEFAULT_PAPERS_CSV = ROOT / "templates" / "included_papers_expanded_batch_2026-03-31.csv"
DEFAULT_RECORDS_CSV = ROOT / "templates" / "evidence_records_expanded_batch_v1_2026-03-31.csv"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def create_tables(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=MEMORY;")
    cur.execute("PRAGMA synchronous=OFF;")
    cur.execute("PRAGMA temp_store=MEMORY;")
    cur.executescript(
        """
        PRAGMA foreign_keys = OFF;

        DROP TABLE IF EXISTS included_papers_raw;
        DROP TABLE IF EXISTS evidence_records_raw;
        DROP VIEW IF EXISTS v_phase1_core_records;
        DROP VIEW IF EXISTS v_primary_study_records;
        DROP VIEW IF EXISTS v_microbiome_records;
        DROP VIEW IF EXISTS v_processing_context_records;

        CREATE TABLE included_papers_raw (
            paper_id TEXT PRIMARY KEY,
            source_db TEXT,
            title TEXT,
            authors TEXT,
            journal TEXT,
            year TEXT,
            doi TEXT,
            pmid TEXT,
            study_type TEXT,
            tea_type TEXT,
            material_form TEXT,
            component_group TEXT,
            activity_category TEXT,
            processing_present TEXT,
            extraction_present TEXT,
            microbiome_present TEXT,
            include_status TEXT,
            exclusion_reason TEXT,
            notes TEXT
        );

        CREATE TABLE evidence_records_raw (
            record_id TEXT PRIMARY KEY,
            paper_id TEXT,
            tea_type TEXT,
            material_form TEXT,
            component_group TEXT,
            compound_name TEXT,
            activity_category TEXT,
            endpoint_label TEXT,
            study_type TEXT,
            evidence_level TEXT,
            model_system TEXT,
            dose_exposure TEXT,
            effect_direction TEXT,
            processing_step TEXT,
            extraction_method TEXT,
            cultivar TEXT,
            origin TEXT,
            mechanism_label TEXT,
            microbiota_taxon TEXT,
            microbial_metabolite TEXT,
            host_phenotype TEXT,
            claim_text_raw TEXT,
            confidence_score REAL,
            annotator_id TEXT,
            adjudication_status TEXT,
            notes TEXT
        );

        CREATE VIEW v_phase1_core_records AS
        SELECT
            r.record_id,
            r.paper_id,
            p.title,
            p.year,
            p.journal,
            r.tea_type,
            r.material_form,
            r.component_group,
            r.compound_name,
            r.activity_category,
            r.endpoint_label,
            r.study_type,
            r.evidence_level,
            r.model_system,
            r.dose_exposure,
            r.effect_direction,
            r.confidence_score
        FROM evidence_records_raw r
        LEFT JOIN included_papers_raw p ON p.paper_id = r.paper_id
        WHERE p.include_status = 'include'
          AND r.activity_category IN (
              'antioxidant',
              'anti-inflammatory',
              'metabolic improvement',
              'anti-obesity',
              'gut microbiota modulation',
              'neuroprotection',
              'cardiovascular protection'
          );

        CREATE VIEW v_primary_study_records AS
        SELECT
            r.*,
            p.title,
            p.journal,
            p.year
        FROM evidence_records_raw r
        LEFT JOIN included_papers_raw p ON p.paper_id = r.paper_id
        WHERE r.study_type IN ('animal study', 'randomized controlled trial', 'cohort study');

        CREATE VIEW v_microbiome_records AS
        SELECT
            r.record_id,
            r.paper_id,
            p.title,
            r.tea_type,
            r.component_group,
            r.activity_category,
            r.study_type,
            r.evidence_level,
            r.mechanism_label,
            r.microbiota_taxon,
            r.microbial_metabolite,
            r.host_phenotype
        FROM evidence_records_raw r
        LEFT JOIN included_papers_raw p ON p.paper_id = r.paper_id
        WHERE r.activity_category = 'gut microbiota modulation'
           OR COALESCE(r.microbiota_taxon, '') <> ''
           OR COALESCE(r.microbial_metabolite, '') <> '';

        CREATE VIEW v_processing_context_records AS
        SELECT
            r.record_id,
            r.paper_id,
            p.title,
            r.tea_type,
            r.material_form,
            r.component_group,
            r.activity_category,
            r.processing_step,
            r.extraction_method,
            r.effect_direction
        FROM evidence_records_raw r
        LEFT JOIN included_papers_raw p ON p.paper_id = r.paper_id
        WHERE COALESCE(r.processing_step, '') <> ''
           OR COALESCE(r.extraction_method, '') <> '';
        """
    )
    conn.commit()


def insert_rows(conn: sqlite3.Connection, table: str, rows) -> None:
    if not rows:
        return
    columns = list(rows[0].keys())
    placeholders = ", ".join(["?"] * len(columns))
    column_list = ", ".join(columns)
    sql = f"INSERT INTO {table} ({column_list}) VALUES ({placeholders})"
    values = [tuple(row.get(col, "") for col in columns) for row in rows]
    conn.executemany(sql, values)
    conn.commit()


def print_summary(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    summary_queries = {
        "included_papers_raw": "SELECT COUNT(*) FROM included_papers_raw",
        "evidence_records_raw": "SELECT COUNT(*) FROM evidence_records_raw",
        "v_phase1_core_records": "SELECT COUNT(*) FROM v_phase1_core_records",
        "v_primary_study_records": "SELECT COUNT(*) FROM v_primary_study_records",
        "v_microbiome_records": "SELECT COUNT(*) FROM v_microbiome_records",
        "v_processing_context_records": "SELECT COUNT(*) FROM v_processing_context_records",
    }
    for label, query in summary_queries.items():
        count = cur.execute(query).fetchone()[0]
        print(f"{label}: {count}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--papers", type=Path, default=DEFAULT_PAPERS_CSV)
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS_CSV)
    parser.add_argument("--db-path", type=Path, default=DB_PATH)
    args = parser.parse_args()

    ensure_dir(DB_DIR)
    papers = load_csv(args.papers)
    records = load_csv(args.records)

    db_path = args.db_path
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if db_path.exists():
        try:
            db_path.unlink()
        except PermissionError:
            pass
    journal_path = Path(f"{db_path}-journal")
    if journal_path.exists():
        try:
            journal_path.unlink()
        except PermissionError:
            pass

    conn = sqlite3.connect(db_path)
    try:
        create_tables(conn)
        insert_rows(conn, "included_papers_raw", papers)
        insert_rows(conn, "evidence_records_raw", records)
        print(f"Built SQLite database at: {db_path}")
        print_summary(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
