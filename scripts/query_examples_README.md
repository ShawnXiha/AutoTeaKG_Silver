# Query Examples README

Files:
- `scripts/query_examples.sql`
- `data/teakg_v1.sqlite`

## Purpose

These queries provide a starter set for exploring the current SQLite database without writing SQL from scratch.

## Covered use cases

1. Basic table/view counts
2. Phase-1 activity distribution
3. Evidence-level distribution
4. Human evidence subset
5. Primary-study subset
6. Microbiome-focused records
7. Processing/extraction context records
8. Non-positive anti-inflammatory records
9. Tea polysaccharide-focused records
10. High-confidence records
11. Papers with multiple activity categories
12. Candidate records for phase-3 C06 graph expansion

## How to run

If `sqlite3` CLI is installed:

```powershell
sqlite3 data/teakg_v1.sqlite < scripts/query_examples.sql
```

If you prefer Python:

```python
import sqlite3
from pathlib import Path

db = Path("data/teakg_v1.sqlite")
conn = sqlite3.connect(db)
cur = conn.cursor()
rows = cur.execute("SELECT activity_category, COUNT(*) FROM v_phase1_core_records GROUP BY activity_category").fetchall()
print(rows)
conn.close()
```

## Recommended first queries

Start with:
- phase-1 activity distribution
- human evidence only
- microbiome-focused records

Those three queries usually give the clearest immediate picture of the current corpus.
