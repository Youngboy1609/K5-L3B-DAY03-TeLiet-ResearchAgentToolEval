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

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:
`report/team/MSSV_HoTen.md`

### PhamDangQuang-2A202603760

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
