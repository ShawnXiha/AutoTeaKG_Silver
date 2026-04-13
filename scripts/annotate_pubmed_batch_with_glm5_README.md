# GLM5 LLM Annotation Pipeline

This script uses NVIDIA's chat-completions API with the `z-ai/glm5` model to replace part of the manual title/abstract annotation workload.

By default, `thinking` is disabled for stability. Pass `--enable-thinking` only when you explicitly want it.

## Environment

Recommended local environment:

```powershell
python -m venv .venv_nvidia_glm5
.venv_nvidia_glm5\Scripts\Activate.ps1
```

No third-party package is required because the project uses a local `ChatNVIDIA` compatibility wrapper.

## API key

Set the API key in an environment variable:

```powershell
$env:NVIDIA_API_KEY="your_key_here"
```

## Usage

Small test:

```powershell
.venv_nvidia_glm5\Scripts\python.exe scripts\annotate_pubmed_batch_with_glm5.py --batch-dir data\pubmed_batches\tea_pubmed_batch_2026-03-31_large_v2 --output-dir data\llm_annotations\glm5_test_run --max-papers 3
```

Specific papers:

```powershell
.venv_nvidia_glm5\Scripts\python.exe scripts\annotate_pubmed_batch_with_glm5.py --batch-dir data\pubmed_batches\tea_pubmed_batch_2026-03-31_large_v2 --output-dir data\llm_annotations\glm5_selected --paper-ids PMID_41899489,PMID_41907215
```

## Rate limiting

Default request interval is `1.6` seconds, which stays under the stated `40 requests/minute` platform limit.

## Outputs

- `llm_screened_papers.csv`
- `llm_annotated_records.csv`
- `llm_raw_responses.jsonl`
- `llm_errors.jsonl`
- `summary.json`

## Important scope note

This is title/abstract-level LLM annotation. It is useful for triage and draft evidence extraction, but it should not overwrite fully adjudicated manual records without review.
