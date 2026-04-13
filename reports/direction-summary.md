# Direction Summary: Top-3 from Idea Tournament

Date: 2026-03-31

## Top 1. Evidence-Graded Tea Health Claims Database (C04)

Core direction:
- Build a structured tea evidence resource that organizes claimed activities by tea type, component/extract, model system, dose/exposure, and evidence level.

Why it is promising:
- It directly addresses the field's biggest interpretability problem: claims are abundant, but evidence quality is uneven.
- It is feasible with current literature and does not require perfect ontology coverage on day 1.

Primary risk:
- If the schema is too coarse, the database becomes only a prettier review.

What must be added to avoid that risk:
- Explicit linkage to component groups, activity definitions, dose context, and study-type-specific confidence.

## Top 2. Tea Microbiome Mechanism Graph (C06)

Core direction:
- Build a mechanistic graph around tea component -> microbiota -> metabolite -> host phenotype pathways, initially for obesity, metabolic dysfunction, and cognition.

Why it is promising:
- This subfield is active, mechanistically interesting, and structurally graph-friendly.
- It is narrower than a general tea KG but rich enough for high-value path analysis.

Primary risk:
- It can become too specialized if the first dataset is small or too animal-heavy.

What must be added to avoid that risk:
- Keep explicit evidence stratification by species and study type, and include human studies wherever available.

## Top 3. Tea Processing-Bioactivity Atlas (C01)

Core direction:
- Build a curated atlas that links tea processing and extraction variables to compound shifts and downstream activity outcomes.

Why it is promising:
- It captures the main scientific intuition of the domain: bioactivity is not static and depends on how tea is produced and processed.
- It provides a high-quality structured substrate that later feeds a graph.

Primary risk:
- Process nomenclature and endpoint heterogeneity may slow normalization.

What must be added to avoid that risk:
- Restrict phase 1 to a few tea classes, a few component groups, and four activity families.

## Cross-Idea Synthesis

Common thread across the top-3:
- The winning ideas all succeed because they convert fragmented tea literature into structured, comparable evidence.

Shared design principle:
- Scope first, graph later.

Best combined direction:
- Use C04 as the initial core resource.
- Add C01 fields so the database captures process/composition context.
- Build C06 as the first graph-native specialty module.

What none of the top-3 fully solve:
- Fully automated extraction.
- Strong predictive modeling.
- Broad tea-wide ontology coverage from day 1.

This is a useful omission, not a weakness. These should be second-cycle additions after the first curated resource exists.
