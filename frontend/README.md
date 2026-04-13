# AutoTeaKG-Silver Frontend

This is a lightweight static frontend for browsing the AutoTeaKG-Silver KG v3 outputs.

## Run

From the repository root:

```powershell
python -B scripts\prepare_frontend_data.py
cd frontend
python -m http.server 8000
```

Open:

```text
http://localhost:8000
```

## What It Shows

- KG-level metrics
- Activity and uncertainty distributions
- A Canvas-based interactive microbiome subgraph
- Evidence-record filtering by activity, evidence level, uncertainty, component group, and keyword

## Data Source

Generated JSON:

```text
frontend/data/autoteakg_frontend_data.json
```

Source data:

```text
reports/methods_processing_vocab_normalized/kg_v3/nodes.csv
reports/methods_processing_vocab_normalized/kg_v3/edges.csv
reports/methods_processing_vocab_normalized/autoteakg_silver_records.csv
```
