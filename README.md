# AutoTeaKG-Silver

AutoTeaKG-Silver is an automatically generated, provenance-rich, uncertainty-aware evidence graph for tea functional activity literature. The project converts PubMed records and open PMC methods sections into structured evidence records, processing/extraction context fields, query tables, publication figures, and a manuscript draft.

The current manuscript frames the resource as a **silver-standard evidence infrastructure**, not as a manually verified gold-standard database. Manual review is separated from graph construction and used only as an optional external validation step.

## Current Release Snapshot

Primary KG version:

```text
reports/methods_processing_vocab_normalized
```

Key counts:

| Quantity | Count |
|---|---:|
| Silver evidence records | 635 |
| KG nodes | 1,989 |
| KG edges | 8,195 |
| Microbiome-relevant records | 190 |
| Records with processing context | 183 |
| Records with extraction context | 185 |
| Low-uncertainty records | 100 |
| Moderate-uncertainty records | 470 |
| High-uncertainty records | 65 |
| Residual missing-context records | 303 |

## Repository Structure

```text
.
├── data/                         # PubMed batches, merged tables, KG prototype outputs
├── figures/kg_v3/                # Publication-style PDF/PNG/SVG figures
├── protocols/                    # Annotation and refinement protocols
├── reports/                      # Search archives, KG summaries, query tables, paper planning
├── schemas/                      # Tea evidence schema
├── scripts/                      # Reproducible pipeline scripts
├── templates/                    # CSV templates and validation/audit sheets
└── writing_outputs/
    └── 20260412_autoteakg_silver_paper/
        ├── final/                # Latest manuscript PDFs and TeX files
        ├── drafts/               # Editable draft versions
        ├── figures/              # Manuscript-local figure copies
        ├── references/           # BibTeX files
        ├── reviews/              # Paper-review, peer-review, ScholarEval, revision plans
        └── data/                 # Figure-ready tables and validation worksheets
```

## Manuscript

Latest compiled manuscript:

```text
writing_outputs/20260412_autoteakg_silver_paper/final/AutoTeaKG_Silver_v4.pdf
writing_outputs/20260412_autoteakg_silver_paper/final/AutoTeaKG_Silver_v4.tex
```

The manuscript currently includes:

- Graphical abstract
- Related Work
- Methods with reproducibility and uncertainty model
- Results with KG composition, evidence heatmap, context recovery, uncertainty, and graph query case study
- Limitations
- Appendix with reproducibility paths, uncertainty flag definitions, and validation sample design

## Main Pipeline Stages

| Stage | Main artifact or script | Output |
|---|---|---|
| PubMed retrieval archive | `reports/pubmed_search_archive_2026-04-02.md` | Query logs and batch summaries |
| Auto-only ideation/profile | `scripts/generate_auto_only_research_ideation.py` | Auto-only research direction and data profile |
| Silver KG construction | `scripts/build_autoteakg_silver_v1.py` | `reports/autoteakg_silver_v1` |
| Abstract-level context extraction | `scripts/targeted_processing_llm_extractor.py` | `reports/targeted_processing_llm_extractor_final` |
| Vocabulary normalization | `scripts/normalize_processing_extraction_vocab.py` | `reports/targeted_processing_vocab_normalized` |
| PMC methods retrieval | `scripts/retrieve_pmc_methods_for_remaining_context.py` | `reports/fulltext_methods_remaining_context` |
| Methods-section extraction | `scripts/run_methods_processing_extraction_batches.py` | `reports/methods_processing_llm_final` |
| Final KG v3 query tables and figures | `scripts/generate_kg_v3_query_tables_and_figures.py` | `reports/kg_v3_query_tables`, `figures/kg_v3` |

## Reproducing Key Outputs

Generate AutoTeaKG-Silver v1:

```powershell
python -B scripts\build_autoteakg_silver_v1.py
```

Generate KG v3 query tables and figures:

```powershell
python -B scripts\generate_kg_v3_query_tables_and_figures.py
```

Generate v4 uncertainty/QC tables:

```powershell
python -B scripts\generate_v4_uncertainty_and_qc_tables.py
```

Generate the graph query case study:

```powershell
python -B scripts\generate_v4_graph_query_case_study.py
```

Prepare the external validation pack:

```powershell
python -B scripts\prepare_v4_validation_pack.py
```

Compile the latest manuscript:

```powershell
cd writing_outputs\20260412_autoteakg_silver_paper\drafts
pdflatex -interaction=nonstopmode -halt-on-error v4_draft.tex
bibtex v4_draft
pdflatex -interaction=nonstopmode -halt-on-error v4_draft.tex
pdflatex -interaction=nonstopmode -halt-on-error v4_draft.tex
```

## LLM/API Notes

Some extraction steps use NVIDIA-hosted GLM5 through the OpenAI-compatible NVIDIA API. API keys are never committed to this repository. If rerunning LLM extraction, set the key externally:

```powershell
$env:NVIDIA_API_KEY="your_key"
```

The public repository intentionally ignores raw LLM response logs (`llm_raw_responses.jsonl` and `processing_llm_raw_responses.jsonl`) because they are large and not required for public reproduction of processed tables.

## Validation Status

The graph construction path is auto-only. A 48-record stratified validation worksheet is provided for external review:

```text
writing_outputs/20260412_autoteakg_silver_paper/data/validation_v4/
```

The validation worksheet evaluates activity category, study type, evidence level, component group, processing step, extraction method, and mechanism label. Validation results should only be reported after reviewer completion; no validation accuracy is fabricated in the current manuscript.

## Citation Collection

The project includes verified BibTeX references for:

- Tea bioactivity and processing literature
- Tea and natural-product database resources
- Scientific information extraction
- Biomedical NLP and biomedical knowledge graphs
- LLM-based KG construction

Main BibTeX:

```text
writing_outputs/20260412_autoteakg_silver_paper/references/references.bib
```

## Current Revision Status

Completed v4 tasks:

- Computational related work expansion
- Uncertainty model formalization
- Stage-wise ablation/QC table
- Graph query case study
- External validation protocol and sample worksheet

Remaining before submission:

- Fill validation worksheet and compute field-level quality metrics
- Add data/code availability statement
- Add LLM usage statement
- Choose target venue and convert template
- Polish appendix tables and figure placement
