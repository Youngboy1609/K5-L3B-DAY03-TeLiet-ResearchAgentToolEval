# Local model setup and preflight attempts — 2026-11-10

## Observed setup

- Ollama `0.40.16`.
- NVIDIA GeForce RTX 3060 Laptop GPU, 6144 MiB reported VRAM; driver `621.01`.
- `qwen2.5:3b` was already installed (about 1.9 GB); `llama3.2:3b` was downloaded (about 2.0 GB). Both model tags meet the assignment's 3B–8B range.
- `llama3.2:1b` is also installed, but is outside that range.
- A local `llama3.2:3b-cpu` alias was created from the downloaded model with `PARAMETER num_gpu 0`. Its provider preflight was not reached in this attempt.

## Commands and results

The repo preflight asks the model for a structured tool call; it does not execute the selected tool.

```powershell
starter_v0\.venv\Scripts\python.exe starter_v0\scripts\preflight_provider.py --provider ollama --model qwen2.5:3b
```

Failed before producing a tool call. Ollama returned:

```text
llama-server reported out-of-memory during startup: cudaMalloc failed: out of memory
ggml_backend_buft_alloc_buffer_n_default: failed to allocate CUDA0 buffer of size 1923955712
error loading model: unable to allocate CUDA0 buffer
```

Then the existing CPU alias was tried:

```powershell
starter_v0\.venv\Scripts\python.exe starter_v0\scripts\preflight_provider.py --provider ollama --model qwen2.5:3b-cpu
```

It also failed before producing a tool call:

```text
ggml_backend_cpu_buffer_type_alloc_buffer: failed to allocate buffer of size 1327104000
ggml_backend_buft_alloc_buffer_n_default: failed to allocate CPU_REPACK buffer
error loading model: unable to allocate CPU_REPACK buffer
```

After closing the UI test app, the newly downloaded Llama model was also preflighted on GPU:

```powershell
starter_v0\\.venv\\Scripts\\python.exe starter_v0\\scripts\\preflight_provider.py --provider ollama --model llama3.2:3b
```

It failed before producing a tool call:

```text
llama-server process has terminated: exit status 1: cudaMalloc failed: out of memory
ggml_backend_buft_alloc_buffer_n_default: failed to allocate CUDA0 buffer of size 2011539712
error loading model: unable to allocate CUDA0 buffer
```

At the later resource snapshot, Windows reported about 1.00 GB free physical memory and 0.74 GB free virtual memory; `ollama ps` showed no resident model. This is a resource snapshot, not proof of the GPU allocation root cause.

## Status and next step

An earlier successful CPU preflight for `qwen2.5:3b-cpu` is recorded in [local_cpu_preflight_2026-11-10.md](local_cpu_preflight_2026-11-10.md). On 2026-11-11, after the user freed RAM (Windows later reported about 4.89 GB free physical memory and 5.47 GB free virtual memory), GPU preflights succeeded for both models:

```text
OK provider=ollama model=qwen2.5:3b
tool=social_search
args={'query': 'Sam Altman', 'search_type': 'Latest'}

OK provider=ollama model=llama3.2:3b
tool=timeline
args={'screenname': 'Sam Altman', 'limit': '1'}
```

`ollama ps` reported both models as `100% GPU` during their respective preflights. Full 20-case baselines were then recorded for both models; see [local_model_baseline_2026-11-11.md](local_model_baseline_2026-11-11.md). The earlier OOMs remain part of the setup history, but are no longer a blocker after RAM was freed.
