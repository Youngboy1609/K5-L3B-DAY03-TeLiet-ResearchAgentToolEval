# Public demo smoke — 2026-11-11

## Setup

- App: `starter_v0/app.py`, served on `127.0.0.1:8501`.
- Public mode: `PUBLIC_DEMO=1`; `DEMO_ACCESS_CODE` was generated for this session and kept out of the repository.
- Public URL: [temporary Cloudflare Quick Tunnel](https://pursue-powerful-mood-rim.trycloudflare.com). The URL stops working when the tunnel process stops.
- `cloudflared` 2026.10.7 was downloaded to the system temp folder and SHA-256 checked against the Cloudflare release checksum before execution; it was not installed globally.
- Provider: OpenRouter, loaded through `DAY03_ENV_FILE`; the key value was not printed or committed.

## Checks

| Check | Result |
|---|---|
| `pytest tests/test_demo_access.py -q` | 5 passed |
| Public access gate | Missing code fails closed; wrong code is rejected; five failed submissions lock that session; valid code unlocks the app. |
| Local mode | Chat remains available without setting `PUBLIC_DEMO`. |
| Browser smoke through public URL | Entered the access code, submitted a chat prompt, and received an assistant response. |
| `pytest -q` | 114 passed, 14 existing TODO stubs skipped, 0 failed. |
| Public error handling | Provider/internal exception text is replaced with a generic message in public mode; local mode retains the detail for debugging. |

## Live chat transcript and limits

The [OpenRouter transcript](../../../starter_v0/transcripts/v3_openrouter_20261111T100829402839.transcript.json) records four live turns. `papers` returned three arXiv items; the model asked for an unspecified account; `timeline` returned a `RuntimeError` after the user supplied `OpenAI`; and the assistant asked for confirmation before Telegram. The `send` executor was stubbed during this run, so no Telegram message could be sent. The timeline failure is recorded, not counted as a successful tool execution.

## Shutdown

Stop the Streamlit and `cloudflared` processes with Ctrl+C in their running sessions. The temporary tunnel URL then becomes unavailable. The portable binary is outside the repository.
