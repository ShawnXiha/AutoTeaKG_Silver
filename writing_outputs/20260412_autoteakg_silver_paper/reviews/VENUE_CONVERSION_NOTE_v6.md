# Venue Conversion Note for AutoTeaKG-Silver v6

Date: 2026-04-13

## Recommended Primary Venue

Primary target: **Database: The Journal of Biological Databases and Curation**.

Rationale:

- The manuscript is a resource/informatics paper rather than a purely algorithmic ML paper.
- The contribution is a biological literature evidence graph, with database construction, annotation, provenance, uncertainty, and reproducibility as central themes.
- The current paper includes a Database URL and database/resource-oriented Results.

## v6 Conversion Performed

File:

- `drafts/v6_database_draft.tex`
- `final/AutoTeaKG_Silver_v6_database.pdf`
- `final/AutoTeaKG_Silver_v6_database.tex`

Changes:

- Added `Database URL` line after the abstract.
- Folded the standalone `Related Work` section into the `Introduction` as `Prior work and resource gap`.
- Retained `Materials and Methods`, `Results`, `Discussion`, `Limitations`, and `Conclusion`.
- Renamed appendix sections as `Supplementary Data` sections.
- Converted long appendix tables to `tabularx` where useful.
- Added data/code availability, LLM usage, and ethics statements in the main manuscript.

## Current Compile Status

- `pdflatex -> bibtex -> pdflatex -> pdflatex` completed.
- No undefined citations.
- No undefined references.
- v6 Database-oriented draft length: 4,712 words.
- PDF length: 16 pages.
- Remaining layout warnings are mostly table-related overfull/underfull boxes.

## Remaining Before Submission

1. Select final journal and check exact author instructions.
2. Convert to the journal's exact Word/LaTeX format if required.
3. Finish external validation worksheet if quality metrics are to be reported.
4. Polish table layouts, especially the graph query and uncertainty flag tables.
5. Decide whether detailed appendix tables should move to supplementary files.

## Secondary Venue Options

- Scientific Data, if reframed as a data descriptor with less emphasis on methodological Results.
- Journal of Biomedical Informatics, if validation and graph utility are strengthened.
- Food Chemistry / Food Research International adjacent venues, if framed more around tea processing and bioactivity evidence rather than graph infrastructure.
