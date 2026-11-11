# Local model baseline — 2026-11-11

## Setup and method

- Models: `qwen2.5:3b` and `llama3.2:3b`, both served by Ollama on RTX 3060 Laptop GPU (6 GB VRAM, 100% GPU in `ollama ps`).
- Dataset: `starter_v0/data/eval_base.json`, phase B, all 20 cases per model.
- Same v3 system prompt (`ba78cd0306b2…`) and tool declarations (`1ded0d564101…`) for both.
- Commands: `python -u run_eval.py --provider ollama --model <model> --version <version> --suite base --eval-cases data/eval_base.json`.
- For containment, the run process used a nonexistent `DAY03_ENV_FILE`, removed credentials for RapidAPI, Tavily, Firecrawl, Telegram, and cloud providers, and routed external HTTP(S) through a refused local proxy. Ollama localhost remained reachable. This measures tool selection/arguments; it does not validate external tool APIs. External API tools that were selected returned errors, and those tool results do not contribute to the routing metrics.

## Results

| Model | Passed | Case accuracy | Tool routing | Arguments | Multiturn | Provider errors | Run JSON |
|---|---:|---:|---:|---:|---:|---:|---|
| `qwen2.5:3b` | 7/20 | 0.35 | 0.60 | 0.35 | 0.50 | 0 | [run](../../starter_v0/runs/v3-qwen2.5-3b_B_base_ollama_20261111T000647728345.json) |
| `llama3.2:3b` | 5/20 | 0.25 | 0.45 | 0.25 | 0.1667 | 0 | [run](../../starter_v0/runs/v3-llama3.2-3b_B_base_ollama_20261111T001334521498.json) |

## Failure classification

Counts are per failing case and may overlap. `missing_tool_call` includes cases where a required tool was omitted; `missed clarify` is a subset of that count.

| Pattern | Qwen 2.5 3B | Llama 3.2 3B |
|---|---:|---:|
| Wrong tool | 5 | 5 |
| Invalid JSON arguments | 0 | 0 |
| Missing expected tool call | 6 | 9 |
| Missed required `clarify` | 3 | 3 |
| Wrong argument value/type | 4 | 5 |
| Out-of-scope tool use | 1 | 1 |
| Unnecessary extra tool call | 1 | 1 |
| Wrong confirmation boundary | 1 | 1 |

Observed examples: Qwen routed broad tweet search to `timeline` in R02 and R07, while Llama routed the OpenAI URL case to `format` instead of `fetch` in R04. Both used `send` instead of asking `clarify` for Telegram confirmation in R12. Llama also failed the no-tool coding boundary in R08; Qwen called a tool on the out-of-scope coding case R14. Neither model emitted malformed JSON in these runs.

## Interpretation and next experiment

The baseline points to routing/clarification and argument normalization as the main prompt targets, rather than JSON parsing. Qwen led on all four reported metrics for this 20-case set only; this is not a general model-quality claim. The measured v4/v5 prompt experiments and their tradeoffs are in [local_prompt_iterations_2026-11-11.md](local_prompt_iterations_2026-11-11.md). A separate OpenRouter reverse-check remains to be run after local optimization.
