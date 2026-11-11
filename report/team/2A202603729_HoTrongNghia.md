# Báo cáo cá nhân — Hồ Trọng Nghĩa (2A202603729)

## 1. Thông tin thành viên

- Họ tên: Hồ Trọng Nghĩa
- MSSV: 2A202603729
- Email: 26ai.nghiaht@vinuni.edu.vn

## 2. Phần việc phụ trách

- Nhóm trưởng; tích hợp các tool mới vào registry và khai báo chung.
- Tự xây tool `source_audit` và viết ít nhất 3 unit test.
- Chạy bonus model local với ít nhất hai model; ghi các vòng tối ưu và bằng chứng vào B7.

## 3. Đóng góp cụ thể

- Tạo nhánh làm việc cá nhân `feature/nghia-source-audit-local-bonus` từ `main`.
- Tạo môi trường Python 3.11.9 trong `starter_v0/.venv` và cài các dependency trong `requirements.txt`.
- Xây tool local `source_audit`, đăng ký vào tool registry và khai báo schema để kiểm tra title/URL HTTP(S) của nguồn.
- Viết 4 unit test cho citation hợp lệ, metadata lỗi, cổng URL sai và input sai kiểu.
- Cài Ollama `0.40.16` tại `D:\Apps\Ollama`, chuyển kho model sang `D:\AIModels\TeLietOllama` và tải `qwen2.5:3b`.
- Tạo alias cục bộ `qwen2.5:3b-cpu` với `num_gpu=0`; preflight của repo đã nhận tool call `social_search` và `ollama ps` xác nhận `100% CPU`.
- Đã chạy benchmark base 20 case với Qwen 2.5 3B và Llama 3.2 3B trên GPU; đã ghi hai vòng prompt local v4/v5 và phân tích vào B7. Các run local có 0 provider error nhưng dùng tool schema base trước PR #1, nên không phải đo trên schema cuối.

## 4. Bằng chứng

- Nhánh làm việc: `feature/nghia-source-audit-local-bonus`.
- Setup: `.venv` dùng Python 3.11.9; cài dependency bằng `uv pip install --python .venv\Scripts\python.exe -r requirements.txt`.
- Kiểm tra setup: import thành công `requests`, `yaml`, `pypdf`, `pytest`, `openai`, `anthropic`, `google.genai`.
- Tool và schema: `starter_v0/tools/source_audit/`, `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml`.
- Unit test: từ `starter_v0/`, `.venv\Scripts\python.exe -m pytest tests/test_tools_todo.py -k source_audit -q` — 4 passed; `.venv\Scripts\python.exe -m pytest tests/test_tool_contract.py -q` — 60 passed.
- Ollama preflight ban đầu gặp lỗi CUDA `device kernel image is invalid`; sau khi driver được cập nhật, preflight `qwen2.5:3b` đã pass ngày 2026-11-11.
- Bằng chứng local/cloud: [setup/preflight](evidence/local_model_setup_2026-11-10.md), [benchmark](evidence/local_model_baseline_2026-11-11.md), [v4/v5 prompt loops](evidence/local_prompt_iterations_2026-11-11.md), [final-schema runs](evidence/local_final_schema_2026-11-11.md). Hai run Qwen v5 trên schema tool hiện tại: [base 12/20](../../starter_v0/runs/v5-final-qwen2.5-3b_B_base_ollama_20261111T102714912533.json) và [group 2/10](../../starter_v0/runs/v5-final-qwen2.5-3b_B_group_ollama_20261111T102852565586.json). Sau khi cập nhật key, OpenRouter preflight pass; reverse-check cùng prompt/schema đạt [19/20](../../starter_v0/runs/v5-final-schema-openrouter_B_base_openrouter_20261111T103351055446.json). Cả ba run có 0 provider error; mức GPU allocation của hai run Ollama mới không được lấy mẫu riêng.
- AI/công cụ: Codex hỗ trợ setup và code; tự kiểm tra bằng import, targeted pytest và contract test.

## 5. Tự đánh giá

Tool `source_audit` và unit test đã hoàn tất và được merge qua PR #4. Full suite gần nhất: 114 passed, 14 starter stubs skipped, 0 failed. Bonus local có benchmark hai model và hai vòng prompt; Qwen v5 đã được đo lại trên schema tool hiện tại, và reverse-check OpenRouter cùng prompt đạt 19/20. Run local chỉ được ghi là Ollama; mức GPU của hai run final-schema không được lấy mẫu riêng.
