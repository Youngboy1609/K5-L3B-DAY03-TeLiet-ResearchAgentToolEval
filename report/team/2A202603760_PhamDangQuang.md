# Báo cáo cá nhân — Phạm Đăng Quang (2A202603760)

## 1. Thông tin thành viên

- **Họ tên:** Phạm Đăng Quang
- **MSSV:** 2A202603760
- **Email:** 26ai.quangpd@vinuni.edu.vn
- **GitHub:** DanggQuangg
- **Nhóm:** TeLiet (Lớp L3B)

---

## 2. Phần việc phụ trách

- **Tool `domain_filter`:** Thiết kế, xây dựng mã nguồn tại `starter_v0/tools/domain_filter/tool.py` và tài liệu hợp đồng `starter_v0/tools/domain_filter/TOOL.md`.
- **Unit Testing:** Viết bộ unit tests cho `domain_filter` trong `starter_v0/tests/test_tools_todo.py`, đảm bảo bao phủ các trường hợp biên, subdomain, chống giả mạo URL và khả năng chịu lỗi (fault tolerance).
- **Bộ dữ liệu đánh giá nhóm:** Sở hữu và thiết kế `starter_v0/data/eval_group.json` gồm đúng 10 case (5 single-turn và 5 multi-turn), có case định tuyến tới cả 4 tool mới của nhóm.
- **Eval nhóm và Báo cáo nhóm:** Chạy bộ đánh giá `--suite group`, phân tích kết quả và hoàn thiện Bảng B3 trong `report/team/group_report.md` *(hoàn thiện sau khi nhóm chạy eval với API key)*.

---

## 3. Đóng góp cụ thể

1. **Phát triển tool `domain_filter`:**
   - Xây dựng hàm `filter_by_domain(items, allowed_domains)`:
     - Tự động chuẩn hóa URL và tên miền đầu vào (loại bỏ `www.`, scheme `http/https`, trailing slash, port).
     - Hỗ trợ so khớp chính xác tên miền và khớp subdomain hợp lệ (ví dụ: `news.example.com` hay `deep.sub.example.com` khớp `example.com`).
     - Tích hợp cơ chế bảo vệ chống URL giả mạo/lừa đảo: chặn an toàn các URL như `example.com.evil.org` hoặc `fake-example.com`.
     - Tuân thủ hợp đồng lỗi: Không bao giờ raise exception làm sập agent; trả về error dict (`err("domain_filter", ...)`) khi input sai kiểu dữ liệu.
   - Soạn thảo `TOOL.md` đầy đủ YAML frontmatter chuẩn theo yêu cầu dự án.

2. **Xây dựng bộ Unit Tests chuyên sâu:**
   - Hiện thực hóa 3 hàm test chuẩn theo mẫu gốc của đề bài (`test_my_new_tool_happy_path`, `test_my_new_tool_bad_input_from_model`, `test_my_new_tool_failure_returns_error_dict`).
   - Mở rộng thêm 8 test cases chuyên sâu kiểm thử toàn diện: khớp subdomain, chặn phishing, chuẩn hóa domain bẩn từ LLM, xử lý item/URL hỏng, giữ nguyên thứ tự kết quả, không phân biệt hoa thường, và kiểm tra kiểu dữ liệu đầu vào.
   - Toàn bộ các bài test đều vượt qua 100% (`PASSED`).

3. **Thiết kế bộ 10 Eval Cases nhóm (`eval_group.json`):**
   - Đúng quy cách: 5 câu đơn lượt (`query`) + 5 hội thoại đa lượt (`turns`).
   - Cung cấp đầy đủ dữ liệu mẫu `items` trong input và assert chặt chẽ `items` cùng các arguments đặc thù (`allowed_domains` cho `domain_filter`; `query` và `limit` cho `rank_sources`) trong `expect.tool_calls[*].args`.
   - Case G08 được bổ sung danh sách nguồn tin mẫu vào các lượt hội thoại để kiểm tra `source_audit` kèm assertion `items` chính xác.
   - Đảm bảo có case kiểm tra định tuyến đến cả 4 tool mới tự viết của nhóm:
     - `domain_filter` (Quang)
     - `source_audit` (Nghĩa)
     - `deduplicate_sources` (Chuẩn)
     - `rank_sources` (Quân)
   - Kiểm tra thêm các tình huống: câu hỏi ngoài phạm vi research (`out_of_scope`), chuyển đổi tool đa lượt, kế thừa ngữ cảnh & cập nhật tham số `limit`, và ranh giới bảo vệ không gửi khi user từ chối xác nhận (`wrong_boundary`).
   - Đã kiểm tra tương thích schema 100% với trình nạp `run_eval.py` và kiểm tra hợp đồng `test_tool_contract.py`.

---

## 4. Bằng chứng

### 4.1. Mã nguồn, nhánh và commit
- **Nhánh làm việc:** `2A202603760_PhamDangQuang`
- **Pull Request:** [GitHub PR #1](https://github.com/Youngboy1609/K5-L3B-DAY03-TeLiet-ResearchAgentToolEval/pull/1)
- **Các file bằng chứng trực tiếp:**
  - `starter_v0/tools/domain_filter/tool.py`
  - `starter_v0/tools/domain_filter/TOOL.md`
  - `starter_v0/tests/test_tools_todo.py` (các bài test `domain_filter`)
  - `starter_v0/data/eval_group.json` (bộ 10 case hoàn chỉnh)
  - `starter_v0/artifacts/tools.yaml` (khai báo tool `domain_filter`)
  - `starter_v0/tools/__init__.py` (đăng ký `domain_filter` vào `TOOL_FUNCTIONS`)

### 4.2. Công cụ AI và cách tự kiểm tra kết quả
- **Công cụ AI đã sử dụng:** Google Antigravity Assistant (Gemini 3.8 Flash). Sử dụng để hỗ trợ thiết kế edge cases kiểm thử, sinh các trường hợp URL mạo danh và rà soát schema test case.
- **Cách tự kiểm tra kết quả:**
  - Chạy `pytest tests/test_tools_todo.py -k domain_filter -v`: **8 passed**, 17 deselected in 0.12s.
  - Chạy `pytest tests/test_tool_contract.py -v`: **75/75 passed** in 0.62s.
  - Kiểm tra nạp và tự đối chiếu dataset: Chạy `run_eval.load_cases(Path('data/eval_group.json'), 'B')` và `compare_subset` thành công 10/10 case không lỗi schema hay kiểu dữ liệu.

### 4.3. Bằng chứng chạy Eval nhóm *(Điền sau khi chạy eval cloud)*
- **File run kết quả:** `starter_v0/runs/[DIEN_SAU_KHI_CHAY_EVAL]`
- **Tóm tắt độ chính xác nhóm:** `[DIEN_SAU_KHI_CHAY_EVAL]`

---

## 5. Tự đánh giá

- **Mức độ hoàn thành:** Đã hoàn thành 100% các yêu cầu lập trình tool, unit test và bộ eval nhóm được giao.
- **Tính liêm chính:** Tự tay kiểm tra toàn bộ mã nguồn, chạy test thực tế trên môi trường máy, không commit file `.env` hay dữ liệu giả mạo.
- **Đóng góp cho nhóm:** Cung cấp đầy đủ tool và bộ 10 eval case hoàn chỉnh để nhóm chạy eval và đưa vào báo cáo chung.
