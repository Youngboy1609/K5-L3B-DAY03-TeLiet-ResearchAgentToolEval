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
python run_eval.py --provider ollama --model qwen2.5:3b --version v5-gpu-final-schema-qwen2.5-3b --suite base --eval-cases data/eval_base.json --system-prompt artifacts/system_prompt_v5_local.md --tools artifacts/tools.yaml
python scripts/preflight_provider.py --provider openrouter
python run_eval.py --provider openrouter --model openai/gpt-4o-mini --version v5-final-schema-openrouter --suite base --eval-cases data/eval_base.json --system-prompt artifacts/system_prompt_v5_local.md --tools artifacts/tools.yaml
```

| Run | Cases | Passed | Accuracy | Routing | Arguments | Multiturn | Provider errors | Artifact |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Qwen 2.5 3B, base | 20 | 12 | 0.60 | 0.60 | 0.60 | 0.3333 | 0 | [JSON](../../../starter_v0/runs/v5-final-qwen2.5-3b_B_base_ollama_20261111T102714912533.json) |
| Qwen 2.5 3B, group | 10 | 2 | 0.20 | 0.70 | 0.20 | 0.00 | 0 | [JSON](../../../starter_v0/runs/v5-final-qwen2.5-3b_B_group_ollama_20261111T102852565586.json) |
| Qwen 2.5 3B, base with GPU allocation sampled | 20 | 12 | 0.60 | 0.60 | 0.60 | 0.3333 | 0 | [JSON](../../../starter_v0/runs/v5-gpu-final-schema-qwen2.5-3b_B_base_ollama_20261111T105120046714.json) |
| OpenRouter `openai/gpt-4o-mini`, base | 20 | 19 | 0.95 | 0.95 | 0.95 | 0.8333 | 0 | [JSON](../../../starter_v0/runs/v5-final-schema-openrouter_B_base_openrouter_20261111T103351055446.json) |

### GPU allocation observed during the new Qwen run

Two live snapshots were taken while this 20-case run was in progress. At `2026-11-11 10:50:32 +07:00`, `ollama ps` listed `qwen2.5:3b` with `PROCESSOR=100% GPU`; `nvidia-smi` reported the RTX 3060 at 63% utilization and 2,284 MiB VRAM used. At `10:51:14 +07:00`, `ollama ps` still reported `100% GPU`, with 2,279 MiB VRAM used. The instantaneous utilization percentage varied between samples; Ollama's processor allocation is the evidence that the model was fully assigned to GPU during inference.

## Limits

- The initial OpenRouter preflight returned HTTP 401 because the previous API key had expired. After the user updated the key, preflight passed and the cloud run completed; no credential value was printed or saved.
- Each model has one run per evaluated suite, so repeatability is unknown.
- The first two final-schema Ollama evals were not sampled for GPU allocation. The additional base rerun above is directly verified as 100% GPU by `ollama ps` during inference.
- The local group score shows weak routing/argument performance on the custom-tool cases. No API-backed tool executor was called by the local eval.
