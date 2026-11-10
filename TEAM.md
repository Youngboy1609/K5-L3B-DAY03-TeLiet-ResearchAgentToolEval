# Team

## Thông tin nhóm

- Tên nhóm: TeLiet
- Lớp: L3B
- Repo nhóm: K5-L3B-DAY03-TeLiet-ResearchAgentToolEval
- URL repo: https://github.com/Youngboy1609/K5-L3B-DAY03-TeLiet-ResearchAgentToolEval
- Nhánh nộp, commit chốt: main

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò | Báo cáo cá nhân |
| --: | ------ | ---- | ----- | ------ | ------- | --------------- |
|   1 | Hồ Trọng Nghĩa | 2A202603729 | 26ai.nghiaht@vinuni.edu.vn | Youngboy1609 | Nhóm trưởng; tự làm `source_audit` và ≥3 test; tích hợp registry; chạy bonus model local và ghi B7 | [2A202603729_HoTrongNghia.md](report/team/2A202603729_HoTrongNghia.md) |
|   2 | Phạm Lê Chuẩn | 2A202603784 | 26ai.chuanpl@vinuni.edu.vn | 22520160 | Tự làm `deduplicate_sources` và ≥3 test; tối ưu system prompt v1-v3; chạy eval cloud và ghi version log | [2A202603784_PhamLeChuan.md](report/team/2A202603784_PhamLeChuan.md) |
|   3 | Phạm Đăng Quang | 2A202603760 | 26ai.quangpd@vinuni.edu.vn | DanggQuangg | Tự làm `domain_filter` và ≥3 test; viết đúng 10 eval case nhóm, có case route tới cả 4 tool mới; chuẩn hóa Evaluator; phân tích kết quả | [2A202603760_PhamDangQuang.md](report/team/2A202603760_PhamDangQuang.md) |
|   4 | Nguyễn Minh Quân | 2A202603747 | 26ai.quannm8@vinuni.edu.vn | minhquannm0905-cloud | Tự làm `rank_sources` và ≥3 test; làm UI (`app.py`), live chat/transcript và Phần A báo cáo | [2A202603747_NguyenMinhQuan.md](report/team/2A202603747_NguyenMinhQuan.md) |

---

## Cá nhân

### 1. HoTrongNghia-2A202603729

#### Phần việc phụ trách
- Nhóm trưởng; tích hợp các tool mới vào registry và khai báo chung.
- Tự xây dựng tool `source_audit` và viết ít nhất 3 unit tests.
- Chạy bonus model local với preflight CPU và ghi nhận kết quả tại B7.

#### Đóng góp cụ thể
- Xây dựng tool local `source_audit` kiểm tra tính hợp lệ của metadata (title, URL scheme HTTP/HTTPS, kiểm tra cổng URL).
- Viết 4 unit tests cho citation hợp lệ, thiếu metadata, scheme sai, cổng sai và input sai kiểu.
- Thiết lập môi trường Ollama và chạy CPU preflight với `qwen2.5:3b-cpu` xác nhận nhận diện tool call thành công.

#### Bằng chứng
- `starter_v0/tools/source_audit/`
- `starter_v0/tests/test_tools_todo.py`
- `report/team/evidence/local_cpu_preflight_2026-11-10.md`
- [2A202603729_HoTrongNghia.md](report/team/2A202603729_HoTrongNghia.md)

---

### 2. PhamLeChuan-2A202603784

#### Phần việc phụ trách
- Tự làm tool `deduplicate_sources` và ít nhất 3 unit test.
- Tối ưu `system_prompt.md` qua các phiên bản v1–v3.
- Chạy eval cloud bằng Gemini (`gemini-2.5-flash-lite`) và ghi version log.

#### Đóng góp cụ thể
- Xây dựng hàm `deduplicate_sources` loại bỏ item trùng URL, chuẩn hóa trailing slash, giữ item đầu tiên và thứ tự ban đầu.
- Xử lý item không có URL và input sai kiểu bằng error dict phù hợp.
- Phân tích kết quả baseline v0 (0.65) và các vòng tối ưu v1 (0.70), v2 (0.80), v3 (0.80).

#### Bằng chứng
- `starter_v0/tools/deduplicate_sources/`
- `starter_v0/tests/test_tools_todo.py`
- `starter_v0/artifacts/system_prompt.md`
- `starter_v0/artifacts/version_log.csv`
- `starter_v0/runs/v0_B_base_gemini_20261110T183708553548.json`
- `starter_v0/runs/v1_B_base_gemini_20261110T184719240561.json`
- `starter_v0/runs/v2_B_base_gemini_20261110T185133380730.json`
- `starter_v0/runs/v3_B_base_gemini_20261110T215643805698.json`
- [2A202603784_PhamLeChuan.md](report/team/2A202603784_PhamLeChuan.md)

---

### 3. PhamDangQuang-2A202603760

#### Phần việc phụ trách
- Tự làm tool `domain_filter` và bộ unit test chuyên sâu (11 tests).
- Thiết kế bộ dữ liệu đánh giá nhóm `starter_v0/data/eval_group.json` gồm đúng 10 case (5 single-turn + 5 multi-turn).
- Chuẩn hóa Evaluator trong `starter_v0/run_eval.py` giữ nguyên thứ tự tuần tự cho danh sách `items`.
- Phân tích kết quả và hoàn thiện báo cáo nhóm `report/team/group_report.md`.

#### Đóng góp cụ thể
- Xây dựng hàm `filter_by_domain(items, allowed_domains)`:
  - Chuẩn hóa tên miền đầu vào (loại bỏ protocol, `www.`, port, trailing slash).
  - Hỗ trợ khớp domain chính xác và subdomain hợp lệ (ví dụ: `news.example.com` khớp `example.com`).
  - Tích hợp phòng thủ chống lừa đảo/spoofed domain (`example.com.evil.org` bị chặn an toàn).
  - Không bao giờ raise exception; trả về error dict khi input sai kiểu.
- Viết 11 unit tests toàn diện trong `starter_v0/tests/test_tools_todo.py`.
- Thiết kế 10 case trong `eval_group.json` có mẫu `items` thực tế, assert chặt chẽ arguments và ranh giới an toàn.
- Sửa hàm `compare_subset` và `normalize_value` trong `run_eval.py` bảo toàn thứ tự cho danh sách `items`.

#### Bằng chứng
- `starter_v0/tools/domain_filter/`
- `starter_v0/tests/test_tools_todo.py`
- `starter_v0/data/eval_group.json`
- `starter_v0/run_eval.py`
- [2A202603760_PhamDangQuang.md](report/team/2A202603760_PhamDangQuang.md)

---

### 4. NguyenMinhQuan-2A202603747

#### Phần việc phụ trách
- Tự làm tool `rank_sources` và ít nhất 3 unit tests.
- Thiết kế giao diện người dùng bằng Streamlit (`starter_v0/app.py`).
- Cấu hình chạy demo public an toàn và chuẩn bị Phần A báo cáo nhóm.

#### Đóng góp cụ thể
- Xây dựng tool `rank_sources` tính điểm trùng lặp từ khóa giữa query và `title` + `summary`, hỗ trợ giới hạn `limit`.
- Viết 3 unit tests trong `starter_v0/tests/test_rank_sources.py` (và `test_tools_todo.py`).
- Xây dựng `starter_v0/app.py` với giao diện Streamlit hiện đại, hiển thị `tool_events` đã gọi và tự động gỡ bỏ credential của `send` cho demo an toàn.

#### Bằng chứng
- `starter_v0/tools/rank_sources/`
- `starter_v0/tests/test_rank_sources.py`
- `starter_v0/app.py`
- [2A202603747_NguyenMinhQuan.md](report/team/2A202603747_NguyenMinhQuan.md)
