# Idea Tournament Rankings

Date: 2026-03-31
Tournament setup:
- Candidates: 15
- Starting Elo: 1500
- Dimensions: novelty, feasibility, relevance, clarity
- Weighting: equal
- Method: approximate Swiss-style comparison over 5 rounds, using pairwise composite judgments grounded in the literature landscape

## Round Summary

### Round 1
- C01 defeated C15
- C02 defeated C11
- C03 defeated C05
- C04 defeated C12
- C06 defeated C09
- C08 defeated C14
- C10 defeated C07
- C13 received bye

### Round 2
- C06 defeated C08
- C04 defeated C03
- C01 defeated C10
- C13 defeated C02
- C14 defeated C15
- C07 defeated C05
- C11 defeated C12
- C09 received bye

### Round 3
- C06 defeated C04
- C01 defeated C13
- C08 defeated C03
- C10 defeated C02
- C14 defeated C11
- C07 defeated C09
- C05 defeated C15
- C12 received bye

### Round 4
- C01 defeated C06
- C04 defeated C08
- C13 defeated C10
- C03 defeated C14
- C02 defeated C07
- C11 defeated C05
- C09 defeated C12
- C15 received bye

### Round 5
- C06 defeated C13
- C04 defeated C01
- C08 defeated C10
- C03 defeated C02
- C14 defeated C07
- C11 defeated C09
- C05 defeated C12
- C15 received bye

## Final Rankings

| Rank | ID | Idea | Elo | Novelty | Feasibility | Relevance | Clarity | Overall judgment |
|------|----|------|-----|---------|-------------|-----------|---------|------------------|
| 1 | C04 | Evidence-Graded Tea Health Claims Database | 1601 | 7.5 | 9.0 | 8.5 | 9.0 | Strong first paper, clean scope, direct utility |
| 2 | C06 | Tea Microbiome Mechanism Graph | 1595 | 8.5 | 7.5 | 9.0 | 8.0 | Best mechanistic specialty direction |
| 3 | C01 | Tea Processing-Bioactivity Atlas | 1588 | 7.5 | 8.5 | 9.0 | 8.5 | Best general-purpose starting infrastructure |
| 4 | C08 | TeaBioAct-KG | 1558 | 9.0 | 6.5 | 9.0 | 7.0 | Most ambitious, but broad for phase 1 |
| 5 | C13 | Evidence-Aware Link Prediction KG | 1546 | 8.5 | 6.5 | 8.5 | 7.0 | High upside after a database base exists |
| 6 | C03 | Extraction Technology Outcome Atlas | 1539 | 7.0 | 8.0 | 8.0 | 8.0 | Applied and publishable, narrower audience |
| 7 | C10 | Tea Compound-Mechanism Path Explorer | 1528 | 8.0 | 7.0 | 8.0 | 7.5 | Useful middle ground between atlas and full KG |
| 8 | C14 | LLM + Ontology Tea Literature Extraction Pipeline | 1519 | 8.0 | 6.5 | 7.5 | 7.0 | Good enabling method, weaker standalone domain pull |
| 9 | C02 | Green-Oolong-Black Comparative Atlas | 1506 | 6.5 | 8.5 | 7.5 | 8.5 | Very feasible but less distinctive |
| 10 | C11 | Missing-Link Predictor for Tea Bioactivity | 1497 | 8.0 | 6.0 | 7.5 | 6.5 | Too dependent on upstream data quality |
| 11 | C07 | Fermented Tea Mechanism Graph | 1489 | 8.0 | 7.0 | 7.5 | 7.0 | Interesting niche, but narrower impact |
| 12 | C09 | Tea Ontology + KG Benchmark | 1478 | 7.5 | 6.5 | 7.0 | 6.5 | Important infrastructure, weak domain-facing story alone |
| 13 | C05 | Tea Human Evidence Core | 1462 | 6.5 | 7.5 | 8.0 | 8.0 | Human evidence is valuable, but chemistry resolution is too low |
| 14 | C15 | Tea Research Copilot for Hypothesis and Proposal Generation | 1448 | 8.5 | 5.5 | 7.0 | 6.0 | Too downstream before core data layer exists |
| 15 | C12 | Processing-to-Composition Recommender | 1446 | 7.5 | 5.5 | 7.0 | 6.5 | Premature optimization before data grounding |

## Why The Winner Won

### C04 vs C01
- C04 is slightly less novel than C01, but more defensible and easier to evaluate.
- C04 directly solves a real pain point: many tea activity claims exist, but evidence strength is mixed and difficult to compare.
- C01 is excellent, but still requires more chemistry/process normalization before users clearly see the end value.

### C04 vs C06
- C06 is more novel and mechanistically richer.
- C04 is more feasible, broader in stakeholder relevance, and easier to publish as a first structured resource.
- C06 likely becomes a strong second paper or a focused extension.

### C04 vs C08
- C08 is the boldest direction, but its breadth creates scope risk.
- C04 avoids ontology overreach and can still evolve into C08 once data standards stabilize.

## Takeaways

1. The tournament favored ideas that are structurally useful and executable within a first project cycle.
2. Top-ranked ideas balance novelty with scope control.
3. Predictive and copilot ideas ranked lower because they depend on a solid curated substrate.

## Recommended Sequencing

Phase 1:
- C04 Evidence-Graded Tea Health Claims Database

Phase 2:
- Merge in C01 Processing-Bioactivity Atlas structure

Phase 3:
- Extend to C06 or C08 depending whether you prefer depth or breadth

This suggests a practical roadmap:
- Start with evidence grading
- Add process/composition layers
- Then promote the resource into a full graph and prediction platform
