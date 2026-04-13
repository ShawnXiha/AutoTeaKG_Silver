# Full GLM5 Tea Pipeline

This is the one-command orchestrator for:

1. PubMed batch retrieval
2. candidate record generation
3. batch SQLite build
4. GLM5 title/abstract annotation
5. merge-back into the master workspace
6. final merged SQLite build

## Prerequisites

- the NVIDIA annotation venv exists at `.venv_nvidia_glm5`
- `NVIDIA_API_KEY` is available in the environment, or passed with `--nvidia-api-key`

## Example

```powershell
$env:NVIDIA_API_KEY="your_key"
python scripts\run_full_glm5_pipeline.py --batch-name tea_full_test_2026-04-01 --retmax-per-query 5 --llm-max-papers 1 --llm-timeout-seconds 420 --llm-max-retries 2
```

The full pipeline now disables `thinking` by default for better stability. Add `--llm-enable-thinking` only if you explicitly want the model's thinking mode.

Retry failed papers and postprocess LLM outputs:

```powershell
$env:NVIDIA_API_KEY="your_key"
python scripts\run_full_glm5_pipeline.py --batch-name tea_full_test_2026-04-01 --retmax-per-query 5 --llm-max-papers 5 --retry-failed-llm
```

Incremental mode:

```powershell
$env:NVIDIA_API_KEY="your_key"
python scripts\run_full_glm5_pipeline.py --batch-name tea_pubmed_batch_2026-03-31_large_v2 --skip-pubmed --incremental --retry-failed-llm
```

In incremental mode, the pipeline reuses existing `*_glm5_final` or `*_glm5` outputs and only annotates PMIDs that are not already present in the prior `llm_screened_papers(.cleaned).csv`.

If you only want the skip behavior without thinking about incremental semantics, use:

```powershell
$env:NVIDIA_API_KEY="your_key"
python scripts\run_full_glm5_pipeline.py --batch-name tea_pubmed_batch_2026-03-31_large_v2 --skip-pubmed --skip-annotated
```

## Outputs

- batch outputs: `data\pubmed_batches\<batch_name>\`
- LLM outputs: `data\llm_annotations\<batch_name>_glm5\`
- merged/final LLM outputs: `data\llm_annotations\<batch_name>_glm5_final\`
- merged outputs: `data\merged_batches\<batch_name>_llm_merged\`
