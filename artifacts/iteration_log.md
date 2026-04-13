# Iteration Log

## Iteration 1 (Phase 1/3)
- **Score**: 0.35 (lint=skipped format=skipped test=0.0 self=0.7)
- **Lint**: skipped (`ruff` not installed)
- **Tests**: failed (script could not create default output directory)
- **Changes**: [`scripts/build_autoteakg_silver_v1.py`, `artifacts/experiment_log_autoteakg_silver_v1.md`]
- **Feedback**: Initial implementation compiled logically but runtime was blocked by Windows ACL on `data/` directory creation and bytecode writing under `scripts/__pycache__`.
- **Next**: continue

## Iteration 2 (Phase 1/3)
- **Score**: 0.72 (lint=skipped format=skipped test=1.0 self=0.65)
- **Lint**: skipped (`ruff` not installed)
- **Tests**: passed for AST parse and full script run
- **Changes**: [`scripts/build_autoteakg_silver_v1.py`]
- **Feedback**: Pipeline produced silver records and KG v3, but failure-case inspection found false processing positives from broad `aging` and `oxidation` patterns.
- **Next**: continue

## Iteration 3 (Phase 2/3)
- **Score**: 0.78 (lint=skipped format=skipped test=1.0 self=0.70)
- **Lint**: skipped (`ruff` not installed)
- **Tests**: passed for AST parse and full script run
- **Changes**: [`scripts/build_autoteakg_silver_v1.py`, `artifacts/experiment_log_autoteakg_silver_v1.md`]
- **Feedback**: Broad `aging`/`oxidation` false positives were reduced; failure-case inspection found remaining broad `drying` false positives from non-tea model processing.
- **Next**: continue

## Iteration 4 (Phase 3/3)
- **Score**: 0.88 (lint=skipped format=skipped test=1.0 self=0.88)
- **Lint**: skipped (`ruff` not installed)
- **Tests**: passed for AST parse, full script run, output row-count checks, KG edge integrity checks, and manual-annotator exclusion check
- **Changes**: [`scripts/build_autoteakg_silver_v1.py`, `artifacts/experiment_log_autoteakg_silver_v1.md`]
- **Feedback**: Auto-only silver records and KG v3 are reproducible; all KG edges resolve to existing nodes; no `codex_v1`/manual records remain in silver output. Known limitation: rule-based processing extraction is conservative and leaves many records with missing processing context.
- **Next**: done

## Iteration 5 (Targeted Extractor)
- **Score**: 0.86 (lint=skipped format=skipped test=1.0 self=0.86)
- **Lint**: skipped (`ruff` not installed)
- **Tests**: passed for AST parse, dry-run target selection, mock patch generation, patched KG export, and KG edge integrity
- **Changes**: [`scripts/targeted_processing_llm_extractor.py`, `scripts/targeted_processing_llm_extractor_README.md`, `artifacts/experiment_log_autoteakg_silver_v1.md`]
- **Feedback**: Targeted extractor selects 365 missing-context records and can write patch-first outputs plus regenerated patched KG. Network/API run was not executed in this sandboxed validation.
- **Next**: done
