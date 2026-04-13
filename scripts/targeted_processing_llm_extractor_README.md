# Targeted Processing LLM Extractor

This module fills the main gap identified in `AutoTeaKG-Silver v1`: missing or under-specified tea processing, extraction, and component context.

It is intentionally patch-first. It does not overwrite the base silver records. Instead, it writes `processing_llm_patches.csv` and, when patches exist, a patched copy of the silver dataset plus a regenerated uncertainty-aware KG v3.

## Inputs

Default input:

```text
reports/autoteakg_silver_v1/autoteakg_silver_records.csv
```

Default target selection:

- `source_is_auto_only == true`
- `uncertainty_flags` contains `missing_processing_or_extraction_context`
- abstract is available

In the current locked silver run this selects `365` records.

## Dry Run

Use this before spending API calls:

```powershell
python -B scripts\targeted_processing_llm_extractor.py --dry-run --output-dir reports\targeted_processing_llm_extractor
```

This writes:

```text
reports/targeted_processing_llm_extractor/target_records.csv
reports/targeted_processing_llm_extractor/summary.json
```

## GLM5 Run

```powershell
$env:NVIDIA_API_KEY="your_key"
python -B scripts\targeted_processing_llm_extractor.py --max-records 20 --output-dir reports\targeted_processing_llm_extractor_run20
```

Defaults are conservative:

- model: `z-ai/glm5`
- thinking: disabled
- max tokens: `1024`
- timeout: `420`
- max retries: `2`
- minimum interval: `1.6` seconds/request, below 40 calls/minute

## Outputs

Main files:

```text
target_records.csv
processing_llm_patches.csv
processing_llm_raw_responses.jsonl
processing_llm_errors.jsonl
summary.json
```

If at least one patch is produced and `--no-apply` is not set:

```text
patched_autoteakg_silver_v1/autoteakg_silver_records.csv
patched_autoteakg_silver_v1/kg_v3/nodes.csv
patched_autoteakg_silver_v1/kg_v3/edges.csv
patched_autoteakg_silver_v1/summary.json
patched_autoteakg_silver_v1/summary.md
```

## Smoke / Mock Run

Use mock mode to test patch application and KG regeneration without network access:

```powershell
python -B scripts\targeted_processing_llm_extractor.py --mock --max-records 5 --output-dir reports\targeted_processing_llm_extractor_mock
```

## Notes

- The prompt explicitly tells the model not to treat host/model terms such as `skin aging`, `middle-aged`, `oxidative stress`, or `freeze-dried sperm` as tea processing.
- Use `--record-ids RECORD_ID ...` to rerun specific difficult records.
- Use `--no-apply` if you only want patches and do not want patched silver/KG outputs.
