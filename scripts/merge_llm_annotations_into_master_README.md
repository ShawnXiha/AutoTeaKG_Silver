# Merge LLM Annotations Into Master

This script merges GLM5 title/abstract annotation outputs back into the main tea evidence workspace.

## Merge policy

1. paper-level updates from `llm_screened_papers.csv` are applied onto the merged paper table
2. manual adjudicated records remain highest priority
3. LLM records are inserted next
4. auto candidate records are retained only for papers not already covered by manual or LLM records
5. papers with LLM records have their `AUTO` placeholders removed

## Example

```powershell
python scripts\merge_llm_annotations_into_master.py --llm-dir data\llm_annotations\glm5_test_run_v1 --output-dir data\merged_batches\merge_2026-04-01_llm_v1
```

## Outputs

- `included_papers_llm_merged.csv`
- `evidence_records_llm_merged.csv`
- `teakg_llm_merged.sqlite`
- `merge_llm_summary.txt`
