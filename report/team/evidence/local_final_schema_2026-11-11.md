# Final-schema local model check — 2026-11-11

## Scope

Re-ran Qwen 2.5 3B with the v5 local prompt and the current `starter_v0/artifacts/tools.yaml` after the custom tools had merged. Re-ran the same 20-case base suite with OpenRouter `openai/gpt-4o-mini` as the v5 prompt reverse-check. OpenRouter credentials were loaded through `DAY03_ENV_FILE`; no key value is stored here.

Artifact hashes shared by all runs: `prompt_hash=665c73f32a34`, `tools_hash=aad6ed05f395`.

## Commands and results

From `starter_v0/`:

```powershell
python scripts/preflight_provider.py --provider ollama --model qwen2.5:3b
python run_eval.py --provider ollama --model qwen2.5:3b --version v5-final-qwen2.5-3b --suite base --eval-cases data/eval_base.json --system-prompt artifacts/system_prompt_v5_local.md --tools artifacts/tools.yaml
python run_eval.py --provider ollama --model qwen2.5:3b --version v5-final-qwen2.5-3b --suite group --eval-cases data/eval_group.json --system-prompt artifacts/system_prompt_v5_local.md --tools artifacts/tools.yaml
python scripts/preflight_provider.py --provider openrouter
python run_eval.py --provider openrouter --model openai/gpt-4o-mini --version v5-final-schema-openrouter --suite base --eval-cases data/eval_base.json --system-prompt artifacts/system_prompt_v5_local.md --tools artifacts/tools.yaml
```

| Run | Cases | Passed | Accuracy | Routing | Arguments | Multiturn | Provider errors | Artifact |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Qwen 2.5 3B, base | 20 | 12 | 0.60 | 0.60 | 0.60 | 0.3333 | 0 | [JSON](../../../starter_v0/runs/v5-final-qwen2.5-3b_B_base_ollama_20261111T102714912533.json) |
| Qwen 2.5 3B, group | 10 | 2 | 0.20 | 0.70 | 0.20 | 0.00 | 0 | [JSON](../../../starter_v0/runs/v5-final-qwen2.5-3b_B_group_ollama_20261111T102852565586.json) |
| OpenRouter `openai/gpt-4o-mini`, base | 20 | 19 | 0.95 | 0.95 | 0.95 | 0.8333 | 0 | [JSON](../../../starter_v0/runs/v5-final-schema-openrouter_B_base_openrouter_20261111T103351055446.json) |

## Limits

- The initial OpenRouter preflight returned HTTP 401 because the previous API key had expired. After the user updated the key, preflight passed and the cloud run completed; no credential value was printed or saved.
- Each model has one run per evaluated suite, so repeatability is unknown.
- GPU allocation was not sampled during the two new Ollama evals. Do not describe these specific runs as GPU runs; earlier GPU runs are documented separately.
- The local group score shows weak routing/argument performance on the custom-tool cases. No API-backed tool executor was called by the local eval.
