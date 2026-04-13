-- Query examples for teakg_v1.sqlite
-- Usage example:
-- sqlite3 data/teakg_v1.sqlite < scripts/query_examples.sql

-- 1. Basic table and view counts
SELECT 'included_papers_raw' AS object_name, COUNT(*) AS n FROM included_papers_raw
UNION ALL
SELECT 'evidence_records_raw', COUNT(*) FROM evidence_records_raw
UNION ALL
SELECT 'v_phase1_core_records', COUNT(*) FROM v_phase1_core_records
UNION ALL
SELECT 'v_primary_study_records', COUNT(*) FROM v_primary_study_records
UNION ALL
SELECT 'v_microbiome_records', COUNT(*) FROM v_microbiome_records
UNION ALL
SELECT 'v_processing_context_records', COUNT(*) FROM v_processing_context_records;

-- 2. Phase-1 core records by activity category
SELECT
    activity_category,
    COUNT(*) AS n_records
FROM v_phase1_core_records
GROUP BY activity_category
ORDER BY n_records DESC, activity_category;

-- 3. Phase-1 core records by evidence level
SELECT
    evidence_level,
    COUNT(*) AS n_records
FROM v_phase1_core_records
GROUP BY evidence_level
ORDER BY n_records DESC, evidence_level;

-- 4. Human evidence only
SELECT
    record_id,
    paper_id,
    title,
    year,
    tea_type,
    component_group,
    activity_category,
    endpoint_label,
    study_type,
    evidence_level,
    effect_direction
FROM v_phase1_core_records
WHERE evidence_level IN ('human_interventional', 'human_observational', 'evidence_synthesis')
ORDER BY year DESC, activity_category, paper_id;

-- 5. Primary-study records only
SELECT
    record_id,
    paper_id,
    title,
    tea_type,
    component_group,
    activity_category,
    study_type,
    model_system,
    effect_direction
FROM v_primary_study_records
ORDER BY activity_category, paper_id, record_id;

-- 6. Microbiome-focused records
SELECT
    record_id,
    paper_id,
    title,
    tea_type,
    component_group,
    activity_category,
    evidence_level,
    mechanism_label,
    microbiota_taxon,
    microbial_metabolite,
    host_phenotype
FROM v_microbiome_records
ORDER BY paper_id, record_id;

-- 7. Processing/extraction context records
SELECT
    record_id,
    paper_id,
    title,
    tea_type,
    component_group,
    activity_category,
    processing_step,
    extraction_method
FROM v_processing_context_records
ORDER BY paper_id, record_id;

-- 8. Anti-inflammatory records with non-positive outcomes
SELECT
    record_id,
    paper_id,
    title,
    study_type,
    evidence_level,
    endpoint_label,
    effect_direction
FROM v_phase1_core_records
WHERE activity_category = 'anti-inflammatory'
  AND effect_direction IN ('mixed', 'negative', 'no_clear_effect')
ORDER BY year DESC, paper_id;

-- 9. Tea polysaccharide records
SELECT
    record_id,
    paper_id,
    title,
    activity_category,
    evidence_level,
    mechanism_label,
    microbial_metabolite,
    host_phenotype
FROM v_phase1_core_records
WHERE component_group = 'tea polysaccharides'
ORDER BY year DESC, paper_id, record_id;

-- 10. High-confidence records (0.94+)
SELECT
    record_id,
    paper_id,
    title,
    activity_category,
    evidence_level,
    confidence_score
FROM v_phase1_core_records
WHERE confidence_score >= 0.94
ORDER BY confidence_score DESC, paper_id, record_id;

-- 11. Papers with multiple activity categories
SELECT
    paper_id,
    title,
    COUNT(DISTINCT activity_category) AS n_activity_categories,
    GROUP_CONCAT(DISTINCT activity_category) AS activity_categories
FROM v_phase1_core_records
GROUP BY paper_id, title
HAVING COUNT(DISTINCT activity_category) > 1
ORDER BY n_activity_categories DESC, paper_id;

-- 12. Candidate records that may warrant phase-3 C06 graph expansion
SELECT
    record_id,
    paper_id,
    title,
    tea_type,
    component_group,
    activity_category,
    mechanism_label,
    microbiota_taxon,
    microbial_metabolite,
    host_phenotype
FROM v_microbiome_records
WHERE activity_category IN ('gut microbiota modulation', 'anti-obesity', 'metabolic improvement', 'neuroprotection')
ORDER BY paper_id, record_id;
