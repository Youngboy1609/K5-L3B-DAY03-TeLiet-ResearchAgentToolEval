# UI Playwright smoke — 2026-11-10

## Scope

- App: Streamlit `starter_v0/app.py`, commit `2c1ca2394395157f880796e83523e023074c4d6b` (current `origin/main` app code).
- Local targets: `http://127.0.0.1:8765` (keyless) and `http://127.0.0.1:8766` (OpenRouter key loaded from the repo-root `.env` through `DAY03_ENV_FILE`). No key value was displayed or copied into this report.
- Browser: Playwright MCP.

## Results

| Mode | Viewport | Action | Result |
|---|---:|---|---|
| Keyless | 1365×900 | Load page | App title and missing-key notice rendered; chat input and send button disabled. |
| Keyless | 390×844 | Resize and inspect | Same notice and disabled chat controls remained visible; no horizontal overflow observed in the page snapshot. |
| OpenRouter | 824×798 | Submit one no-tool question | `Hãy trả lời ngắn gọn: 2 + 2 bằng mấy? Không cần tra cứu hoặc gọi công cụ.` returned `2 + 2 bằng 4.`; no tool event appeared. |

Playwright reported 0 browser console errors after the OpenRouter response. The keyless check did not make a model call. The OpenRouter check made one live request and is only a basic chat smoke, not a full tool-routing or UX acceptance pass.

## Screenshots

- [Keyless desktop](ui_smoke_desktop_2026-11-10.png)
- [Keyless mobile](ui_smoke_mobile_2026-11-10.png)
- [OpenRouter chat response](ui-openrouter-chat_2026-11-10.png)

## Reproduction

From `starter_v0/`, with the repo `.env` available for the key-enabled case:

```powershell
$env:DAY03_ENV_FILE = (Resolve-Path '..\.env').Path
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8766 --server.headless true --browser.gatherUsageStats false
```

The `.env` file itself is not part of the evidence and must not be committed.

## Limits

- No public deploy or owner UAT was performed.
- Only one no-tool request was sent; tool execution, provider error recovery, and repeated turns were not tested.
- This smoke does not verify benchmark performance or complete the local-model bonus.
