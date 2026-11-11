# Local prompt iterations — 2026-11-11

## Controlled comparison

Canonical v4/v5 runs use the same 20 cases in `starter_v0/data/eval_base.json`, Ollama `qwen2.5:3b` (100% GPU), the same `tools.yaml` hash, and offline stubs for all tool executors. The harness grades model tool calls and arguments; no external tool API was invoked. Raw JSON is linked below.

| Version | Prompt artifact | Hypothesis | Case accuracy | Tool routing | Arguments | Multiturn | Run |
|---|---|---|---:|---:|---:|---:|---|
| v3 baseline | `artifacts/system_prompt.md` | Baseline before local optimization | 0.35 | 0.60 | 0.35 | 0.50 | [run JSON](../../starter_v0/runs/v3-qwen2.5-3b_B_base_ollama_20261111T000647728345.json) |
| v4-local | `artifacts/system_prompt_v4_local.md` | An ordered routing map with account-vs-topic distinctions reduces wrong tools | 0.65 | 0.75 | 0.65 | 0.6667 | [run JSON](../../starter_v0/runs/v4-local-qwen2.5-3b_B_base_ollama_20261111T005614499549.json) |
| v5-local | `artifacts/system_prompt_v5_local.md` | Explicit clarify, intent-switch, argument-type, and confirmation examples improve full-case and argument accuracy | 0.65 | 0.65 | 0.65 | 0.3333 | [run JSON](../../starter_v0/runs/v5-local-qwen2.5-3b_B_base_ollama_20261111T005631827068.json) |

## What changed

- **v4:** case accuracy rose by 0.30 and routing by 0.15 from v3; argument accuracy rose by 0.30. Wrong-tool failures fell from 5 to 2. Out-of-scope and missing-information failures remained.
- **v5:** case and argument accuracy were unchanged from v4; routing fell by 0.10 and multiturn accuracy fell by 0.3334. Wrong-boundary and out-of-scope failures were absent in this run, while missing-tool and wrong-argument failures increased. The v5 hypothesis was not supported as a broad improvement.
- Across v3 to v5, case accuracy and argument accuracy improved from 0.35 to 0.65; routing improved from 0.60 to 0.65. These are results on this fixed 20-case set, not general model quality claims.

Earlier exploratory runs with prompt files differing only by a trailing blank line produced different scores (v4 12/20 and v5 14/20). The final table uses clean-hash canonical prompts; model repeatability was not assessed.

An exploratory full v4 run on `llama3.2:3b` was not counted: it stopped advancing at R09 for over two minutes while Ollama continued reporting GPU activity. It was interrupted and produced no run JSON. The full v3 baseline for Llama is recorded separately.

## Remaining step

Run the v5 prompt against the cloud provider for the required reverse-check. That run will make 20 OpenRouter model requests; it has not been run yet. No cloud score is claimed here.
