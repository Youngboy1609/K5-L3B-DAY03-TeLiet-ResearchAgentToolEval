# Báo cáo cá nhân — HoVaTen-MSSV

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Phạm Lê Chuẩn
- MSSV: 2A202603784
- Email: 26ai.chuanpl@vinuni.edu.vn

## 2. Phần việc phụ trách

- Phát triển tool `deduplicate_sources`.
- Viết tối thiểu 3 unit test cho tool mới.
- Tối ưu `system_prompt.md` qua các phiên bản v1, v2, v3.
- Chạy và phân tích eval cloud bằng Gemini `gemini-3.5-flash-lite`.
- Ghi nhận metric, hash artifact và đường dẫn run để làm bằng chứng.

## 3. Đóng góp cụ thể

- Tạo [tool.py](../../starter_v0/tools/deduplicate_sources/tool.py) và [TOOL.md](../../starter_v0/tools/deduplicate_sources/TOOL.md).
- Đăng ký `deduplicate_sources` trong [tools/__init__.py](../../starter_v0/tools/__init__.py) và khai báo trong [tools.yaml](../../starter_v0/artifacts/tools.yaml).
- Tool loại các item trùng URL, giữ item xuất hiện đầu tiên và giữ nguyên thứ tự ban đầu.
- Item không có URL hoặc URL rỗng được giữ nguyên và không dùng để deduplicate.
- Input không phải list, item không phải object hoặc URL không phải chuỗi trả về error dict thay vì raise exception.
- Thay các test stub bằng 3 test cho happy path, item thiếu URL và input sai kiểu trong [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py).
- Tối ưu prompt theo từng giả thuyết: routing ở v1, xử lý thiếu thông tin ở v2, và argument/boundary ở v3.

## 4. Bằng chứng

- File/commit/PR:
  - [deduplicate_sources/tool.py](../../starter_v0/tools/deduplicate_sources/tool.py)
  - [deduplicate_sources/TOOL.md](../../starter_v0/tools/deduplicate_sources/TOOL.md)
  - [tools/__init__.py](../../starter_v0/tools/__init__.py)
  - [tools.yaml](../../starter_v0/artifacts/tools.yaml)
  - [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py)
  - [system_prompt.md](../../starter_v0/artifacts/system_prompt.md)
  - [v0 run](../../starter_v0/runs/v0_B_base_gemini_20261110T183708553548.json)
  - [v1 run](../../starter_v0/runs/v1_B_base_gemini_20261110T184719240561.json)
  - [v2 run](../../starter_v0/runs/v2_B_base_gemini_20261110T185133380730.json)
  - [v3 run hợp lệ](../../starter_v0/runs/v3_B_base_gemini_20261110T215643805698.json)

- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng Gemini cloud với model `gemini-3.5-flash-lite`.
  - Chạy `pytest tests/test_tools_todo.py -v` và `pytest tests/test_tool_contract.py -v`.
  - Ba test của `deduplicate_sources` đạt 3 passed; các stub challenge khác vẫn skipped.
  - Kiểm tra run JSON, đặc biệt `summary`, `failure_counts`, `observed_mismatch_counts`,
    `prompt_hash`, `tools_hash` và `provider_error_cases`.

### 4.1. Kết quả eval cloud

| Version | Passed/Measured | Case accuracy | Tool routing | Argument | Multiturn | Provider errors |
|---|---:|---:|---:|---:|---:|---:|
| v0 | 13/20 | 0.65 | 0.80 | 0.65 | 0.6667 | 0 |
| v1 | 14/20 | 0.70 | 0.95 | 0.70 | 0.5000 | 0 |
| v2 | 16/20 | 0.80 | 1.00 | 0.80 | 0.8333 | 0 |
| v3 | 16/20 | 0.80 | 1.00 | 0.80 | 0.8333 | 0 |

Các giả thuyết:

- v1: routing rules rõ hơn sẽ giảm lỗi chọn sai tool.
- v2: quy tắc `clarify` khi thiếu thông tin sẽ giảm lỗi `missing_info`.
- v3: quy tắc argument và confirmation boundary rõ hơn sẽ cải thiện argument/boundary.

Run v3 hợp lệ ở trên có 20/20 case được đo và 0 provider error. Các lần chạy v3
trước đó có provider errors và không được dùng làm bằng chứng cuối.

## 5. Tự đánh giá

- Hoàn thành phần tool mới và 3 unit test theo yêu cầu.
- v2 và v3 cùng đạt `case_accuracy=0.80`, `tool_routing_accuracy=1.00`,
  `argument_accuracy=0.80`; v3 là run cuối hợp lệ và có `provider_error_cases=0`.
