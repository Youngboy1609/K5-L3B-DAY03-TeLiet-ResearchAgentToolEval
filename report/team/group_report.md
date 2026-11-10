# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: TeLiet
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3:

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

Từ `starter_v0/`: `streamlit run app.py` (dependency: `streamlit>=1.40.0`).
Smoke test bằng Streamlit `AppTest` trên `main` đã xác nhận app render được khi thiếu key, ô chat bị khóa và Telegram credentials không còn trong tiến trình.

Playwright smoke ngày 10/11/2026 kiểm tra thêm trạng thái thiếu key ở desktop/mobile và một lượt chat OpenRouter một câu hỏi không cần tool; ảnh và phạm vi kiểm tra ở [ui_playwright_smoke_2026-11-10.md](evidence/ui_playwright_smoke_2026-11-10.md).

**Link dùng thử (deploy):**

Chưa có link public; đã có browser smoke cục bộ, chưa phải UAT đầy đủ hoặc deploy.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
| deduplicate_sources | loại nguồn trùng URL, giữ item đầu tiên và thứ tự ban đầu | có |
| source_audit | kiểm tra title và URL HTTP(S) trong danh sách nguồn trước khi trình bày digest | có |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- Thêm `source_audit` (`starter_v0/tools/source_audit/`): kiểm tra title và URL HTTP(S) cho từng citation, trả danh sách lỗi theo index; tool không tải URL và không xác minh claim.
- Thêm `deduplicate_sources` (`starter_v0/tools/deduplicate_sources/`): gộp URL trùng, chuẩn hóa slash cuối, giữ item đầu tiên và thứ tự ban đầu.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo chất lượng ban đầu trước tối ưu | - | 0.65 | `starter_v0/runs/v0_B_base_gemini_20261110T183708553548.json` |
| v1 | `artifacts/system_prompt.md` | Routing rõ hơn sẽ giảm `wrong_tool` | 0.65 | 0.70 | `starter_v0/runs/v1_B_base_gemini_20261110T184719240561.json` |
| v2 | `artifacts/system_prompt.md` | Quy tắc `clarify` rõ hơn sẽ giảm `missing_info` | 0.70 | 0.80 | `starter_v0/runs/v2_B_base_gemini_20261110T185133380730.json` |
| v3 | `artifacts/system_prompt.md` | Quy tắc args và boundary rõ hơn sẽ cải thiện kết quả | 0.80 | 0.80 | `starter_v0/runs/v3_B_base_gemini_20261110T215643805698.json` |

> PR #3 ghi nhận v3 là `v3_B_base_gemini_20261110T215643805698.json`,
> với `total_cases=20`, `measured_cases=20`, `provider_error_cases=0`.
> Các run v3 trước đó không được tính do provider errors từ Gemini:
> `185620920233`, `193757883769`, `194616666952`, `195746525886`,
> `200311115832`, `214921174144`.
>
> **Thiếu file bằng chứng:** các đường dẫn run v0–v3 trong bảng hiện không có trong `main` (`starter_v0/runs/` chưa được commit). Vì vậy các metric và trạng thái hợp lệ ở trên chưa thể đối soát từ JSON; cần bổ sung run files trước khi tính là bằng chứng nộp bài.

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`deduplicate_sources`) | `starter_v0/tools/deduplicate_sources/tool.py`, `TOOL.md`; đăng ký trong registry và `tools.yaml` | 4 test: URL trùng, slash cuối, item thiếu URL, input sai kiểu | Chuẩn hóa URL để deduplicate, không xác minh nguồn hoặc nội dung |
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/source_audit/tool.py`, `TOOL.md`; đăng ký tại `starter_v0/tools/__init__.py` và `starter_v0/artifacts/tools.yaml` | 4 test xác nhận citation HTTP hợp lệ, thiếu title/URL FTP và cổng URL sai bị báo lỗi, input `items` sai kiểu trả error dict | Chỉ kiểm tra metadata/cú pháp URL; không xác nhận URL truy cập được hay claim chính xác |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py`, `starter_v0/tests/test_rank_sources.py`, `starter_v0/tests/test_tool_contract.py` | 4 `source_audit`, 4 `deduplicate_sources`, 3 `rank_sources`, 65 contract test đạt; toàn suite `83 passed, 14 skipped` | 14 skip là TODO stub có sẵn; chưa chứng minh model tự route đúng tới mọi tool |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py`; dependency trong `starter_v0/requirements.txt`; [bằng chứng Playwright](evidence/ui_playwright_smoke_2026-11-10.md) | `AppTest`; Playwright desktop 1365×900 và mobile 390×844 khi thiếu key; với key, một câu hỏi không cần tool trả lời `2 + 2 bằng 4`; console 0 lỗi | Chưa có browser UAT đầy đủ hoặc deploy link; chỉ thử một lượt không dùng tool; UI chưa có auth/rate limit, không mở public trước khi kiểm soát lượt gọi/provider spend |

`rank_sources` có implementation và 3 test trên main; registry/schema sẽ được hoàn tất trong PR #1 theo kế hoạch tích hợp cuối.

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

Eval routing: hiện chưa có case nhóm kiểm tra `source_audit`; `starter_v0/data/eval_group.json` đang có `cases: []`. Cần bổ sung theo phần CP4 trước khi kết luận model route tool đúng.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-qwen2.5-3b | `qwen2.5:3b` (Ollama, 100% GPU) | v3 | 0.35 | 0.60 | 0.35 | 0.50 | [run JSON](../../starter_v0/runs/v3-qwen2.5-3b_B_base_ollama_20261111T000647728345.json) |
| v3-llama3.2-3b | `llama3.2:3b` (Ollama, 100% GPU) | v3 | 0.25 | 0.45 | 0.25 | 0.1667 | [run JSON](../../starter_v0/runs/v3-llama3.2-3b_B_base_ollama_20261111T001334521498.json) |
| v4-local-qwen2.5-3b | `qwen2.5:3b` (Ollama, 100% GPU) | ordered routing map | 0.65 | 0.75 | 0.65 | 0.6667 | [run JSON](../../starter_v0/runs/v4-local-qwen2.5-3b_B_base_ollama_20261111T005614499549.json) |
| v5-local-qwen2.5-3b | `qwen2.5:3b` (Ollama, 100% GPU) | clarify/args/boundary examples | 0.65 | 0.65 | 0.65 | 0.3333 | [run JSON](../../starter_v0/runs/v5-local-qwen2.5-3b_B_base_ollama_20261111T005631827068.json) |
| v5-local (cloud check) | OpenRouter | v5-local | pending | pending | pending | pending | not run |

Bằng chứng setup: sau khi giải phóng RAM, preflight GPU thành công cho cả hai model; chi tiết lỗi trước đó và các lần preflight xem [local_model_setup_2026-11-10.md](evidence/local_model_setup_2026-11-10.md). Hai baseline dùng đủ 20 case phase B, prompt hash `ba78cd0306b2`, tools hash `1ded0d564101`, provider errors 0; kết quả và giới hạn offline được ghi ở [local_model_baseline_2026-11-11.md](evidence/local_model_baseline_2026-11-11.md). Hai vòng tối ưu và giả thuyết được ghi ở [local_prompt_iterations_2026-11-11.md](evidence/local_prompt_iterations_2026-11-11.md). Không có kết quả tool API bên ngoài nào được tính vào metric.

B7 đã có baseline local cho hai model và hai vòng tối ưu `v4-local`/`v5-local` trên Qwen; còn thiếu kiểm tra ngược `v5-local` trên cloud. Run JSON cloud v0–v3 chưa được commit nên vẫn chưa đối soát được baseline cloud. Local metrics bên trên chấm routing/arguments trên 20 case; credentials cho tools bên ngoài đã bị gỡ hoặc các executor được stub, nên đây không phải bằng chứng tool API thật hoạt động.

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Qwen v3 | Llama v3 | Qwen v4 | Qwen v5 |
|---|---:|---:|---:|---:|
| wrong / hallucinated tool | 5 | 5 | 2 | 1 |
| invalid JSON args (`_invalid_json_arguments`) | 0 | 0 | 0 | 0 |
| missing expected tool call | 6 | 9 | 3 | 7 |
| missed `clarify` | 3 | 3 | 2 | 2 |
| wrong argument value/type | 4 | 5 | 1 | 3 |
| out-of-scope tool use | 1 | 1 | 2 | 0 |
| unnecessary extra call | 1 | 1 | 2 | 0 |
| wrong confirmation boundary | 1 | 1 | 1 | 0 |

- v4 đạt 0.65 case accuracy và 0.75 routing. v5 giữ case/argument accuracy ở 0.65, nhưng routing giảm còn 0.65 và multiturn giảm còn 0.3333; boundary/out-of-scope lỗi không xuất hiện trong run v5 này. Kết quả chưa chứng minh v5 tốt hơn v4.
- Các run thử trước với cùng nội dung prompt nhưng khác whitespace cho điểm khác nhau; mới có một run canonical cho mỗi hash sạch, nên repeatability chưa được đo.
- Cần chạy reverse-check `v5-local` trên cloud; hiện chưa ghi metric cloud.
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
