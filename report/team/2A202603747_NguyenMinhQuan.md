# Báo cáo cá nhân — Nguyễn Minh Quân (2A202603747)

## 1. Thông tin thành viên

- Họ tên: Nguyễn Minh Quân
- MSSV: 2A202603747
- Email: 26ai.quannm8@vinuni.edu.vn
- GitHub: minhquannm0905-cloud
- Nhóm: TeLiet (Lớp L3B)

## 2. Phần việc phụ trách

- Xây dựng tool `rank_sources` và bộ unit test tương ứng (≥ 3 tests).
- Thiết kế giao diện người dùng (UI) bằng Streamlit (`starter_v0/app.py`).
- Cấu hình chạy demo công khai an toàn (loại bỏ token/credential của action tool như `send`).
- Phối hợp tạo live chat/transcript và soạn thảo Phần A (Giới thiệu agent) trong báo cáo nhóm.

## 3. Đóng góp cụ thể

- Tạo nhánh làm việc cá nhân `quan-ui` và mở Pull Request #2 tích hợp vào repo chung.
- Xây dựng tool local `rank_sources` (`starter_v0/tools/rank_sources/tool.py` và `TOOL.md`):
  - Xếp hạng các bài viết/nguồn tin đã thu thập dựa trên mức độ trùng khớp từ khóa với truy vấn `query`.
  - Giữ nguyên thứ tự ban đầu đối với các bài có cùng điểm số (stable sort).
  - Giới hạn số lượng kết quả trả về theo tham số `limit`.
  - Xử lý lỗi an toàn: trả về error dict với mã `invalid_input` khi tham số đầu vào không đúng kiểu dữ liệu.
- Viết bộ unit test cho `rank_sources` trong `starter_v0/tests/test_rank_sources.py` (3 passed) và đồng bộ vào `starter_v0/tests/test_tools_todo.py`.
- Xây dựng giao diện Streamlit tại `starter_v0/app.py`:
  - Giao diện chat trực quan với Streamlit chat messages và chat input.
  - Tích hợp vòng lặp `run_model_tool_loop` để agent gọi tool và phản hồi người dùng.
  - Hiển thị chi tiết các `tool_events` đã gọi trong khối accordion/expander dưới mỗi câu trả lời.
  - Bảo vệ an toàn cho demo public: tự động gỡ bỏ `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` khỏi môi trường và loại bỏ tool `send` khỏi danh sách tool đưa vào prompt để tránh rò rỉ hoặc gửi tin nhắn ngoài ý muốn.
- Bổ sung dependency `streamlit>=1.40.0` vào `starter_v0/requirements.txt`.

## 4. Bằng chứng

- Nhánh làm việc: `quan-ui` (PR #2).
- Mã nguồn UI: `starter_v0/app.py`.
- Mã nguồn tool và hợp đồng: `starter_v0/tools/rank_sources/tool.py`, `starter_v0/tools/rank_sources/TOOL.md`.
- Unit test: `starter_v0/tests/test_rank_sources.py` (3 passed).
- Công cụ hỗ trợ: Trợ lý AI hỗ trợ dựng khung giao diện Streamlit; tự kiểm tra bằng cách chạy thử `streamlit run app.py` và chạy pytest offline.

## 5. Tự đánh giá

Tool `rank_sources` và UI Streamlit đã hoàn thành, tích hợp sạch sẽ vào nhánh chính của nhóm và toàn bộ test đều vượt qua.
