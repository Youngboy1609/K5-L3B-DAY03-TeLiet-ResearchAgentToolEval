# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: TeLiet
- Lớp: L3B
- Repo nhóm: K5-L3B-DAY03-TeLiet-ResearchAgentToolEval
- URL repo: https://github.com/Youngboy1609/K5-L3B-DAY03-TeLiet-ResearchAgentToolEval
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: Google Gemini (`gemini-2.5-flash-lite`)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research Agent đa năng phục vụ nghiên cứu và tổng hợp thông tin: tìm kiếm bài báo khoa học trên arXiv, tra cứu tin tức trên web và bài đăng mạng xã hội, lọc nguồn tin theo tên miền tin cậy, kiểm toán metadata và liên kết trích dẫn, loại bỏ nguồn tin trùng lặp, xếp hạng mức độ liên quan theo từ khóa, định dạng báo cáo digest có cấu trúc, và gửi tin lên kênh Telegram bảo mật sau khi được người dùng phê duyệt rõ ràng.

**Cách chạy UI:**

Giao diện người dùng được xây dựng bằng Streamlit (`starter_v0/app.py`), dependency `streamlit>=1.40.0` đã được khai báo trong `starter_v0/requirements.txt`.

Lệnh chạy giao diện từ thư mục `starter_v0`:
```bash
cd starter_v0
streamlit run app.py
```

**Link dùng thử (deploy):**

Để chạy demo public an toàn bằng Cloudflare Tunnel (không để lộ Telegram token):
```bash
cloudflared tunnel --url http://localhost:8501
```
URL nội bộ: `http://localhost:8501`

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin cốt lõi hoặc xin phê duyệt trước action | không |
| lookup | tra cứu thông tin và tin tức tổng hợp trên internet qua search engine | không |
| fetch | đọc và trích xuất nội dung văn bản từ một địa chỉ web (URL) | không |
| timeline | lấy danh sách các bài đăng gần đây của một tài khoản mạng xã hội theo handle | không |
| social_search | tìm kiếm bài đăng trên mạng xã hội theo từ khóa và cách xếp hạng | không |
| papers | tìm kiếm bài báo khoa học và công trình nghiên cứu trên arXiv | không |
| paper_text | trích xuất toàn văn nội dung một bài báo arXiv theo ID hoặc URL | không |
| policy | tra cứu chính sách và quy chế nội bộ của công ty trong kho tri thức | không |
| format | định dạng danh sách dữ liệu thu thập được thành văn bản/digest có cấu trúc | không |
| send | gửi nội dung tóm tắt lên kênh Telegram bảo mật sau khi người dùng xác nhận | không |
| domain_filter | lọc danh sách bài viết theo tên miền cho phép (hỗ trợ subdomain, chống phishing) | có |
| source_audit | kiểm tra metadata title và cú pháp URL HTTP(S) cho từng trích dẫn nguồn tin | có |
| deduplicate_sources | loại bỏ các bài viết trùng lặp URL khỏi danh sách, chuẩn hóa URL và giữ item đầu tiên | có |
| rank_sources | xếp hạng danh sách bài viết theo mức độ trùng khớp từ khóa với truy vấn | có |

### A3. Câu hỏi mẫu để thử

1. "Tìm cho tôi 3 bài báo mới nhất về LLM reasoning trên arXiv và đọc tóm tắt bài đầu tiên."
2. "Tìm tin tức hôm nay về công nghệ chip AI, lọc chỉ lấy nguồn từ arxiv.org hoặc techcrunch.com, loại bỏ các bài trùng link rồi xếp hạng theo từ khóa 'GPU'."
3. "Tôi muốn đăng bản tóm tắt này lên Telegram, hãy kiểm toán lại metadata danh sách nguồn và hỏi tôi xác nhận trước khi gửi."

## 3. Giải pháp

- **Tối ưu System Prompt (`starter_v0/artifacts/system_prompt.md`):**
  - Loại bỏ các chỉ dẫn mặc định mơ hồ của bản starter.
  - Thiết lập ma trận định tuyến (routing rules) phân biệt rõ ràng giữa tìm kiếm hàn lâm (`papers`), tin tức web (`lookup`), và phản ứng cộng đồng (`social_search`, `timeline`).
  - Thiết lập quy tắc missing-information: bắt buộc gọi `clarify` khi người dùng yêu cầu đọc tài khoản nhưng không đưa handle, hoặc yêu cầu đọc web nhưng không đưa URL.
  - Thiết lập ranh giới an toàn nghiêm ngặt (confirmation guardrail): tuyệt đối không tự ý gọi `send`; bắt buộc gọi `clarify` dạng `yes_no` để người dùng xác nhận trước khi gửi.
- **Chuẩn hóa Tool Declarations (`starter_v0/artifacts/tools.yaml`):**
  - Bổ sung chỉ dẫn "Khi nào dùng" và "Khi nào không dùng" cho từng công cụ.
  - Quy định rõ định dạng và chuẩn mực tham số (như `topic`, `timeframe`, `search_type`).
  - Khai báo đầy đủ 4 công cụ mới của nhóm (`domain_filter`, `source_audit`, `deduplicate_sources`, `rank_sources`).
- **Bộ 4 công cụ mới phát triển:**
  1. `domain_filter`: Lọc items theo danh sách whitelist tên miền; hỗ trợ subdomain; chặn an toàn các URL lừa đảo/spoofed.
  2. `source_audit`: Kiểm tra metadata trích dẫn (bắt buộc title và cú pháp URL HTTP/HTTPS hợp lệ); phát hiện cổng URL sai định dạng.
  3. `deduplicate_sources`: Loại bỏ các bài viết trùng URL, chuẩn hóa trailing slash và scheme, giữ nguyên thứ tự ổn định.
  4. `rank_sources`: Tính điểm trùng khớp từ khóa từ câu truy vấn (lexical overlap), sắp xếp giảm dần và lấy theo `limit`.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo chất lượng ban đầu trước tối ưu | - | 0.65 | `starter_v0/runs/v0_B_base_gemini_20261110T183708553548.json` |
| v1 | `artifacts/system_prompt.md` | Routing rõ hơn sẽ giảm `wrong_tool` | 0.65 | 0.70 | `starter_v0/runs/v1_B_base_gemini_20261110T184719240561.json` |
| v2 | `artifacts/system_prompt.md` | Quy tắc `clarify` rõ hơn sẽ giảm `missing_info` | 0.70 | 0.80 | `starter_v0/runs/v2_B_base_gemini_20261110T185133380730.json` |
| v3 | `artifacts/system_prompt.md` | Quy tắc args và boundary rõ hơn sẽ cải thiện kết quả | 0.80 | 0.80 | `starter_v0/runs/v3_B_base_gemini_20261110T215643805698.json` |

> Run v3 hợp lệ là `v3_B_base_gemini_20261110T215643805698.json`,
> với `total_cases=20`, `measured_cases=20`, `provider_error_cases=0`.
> Các run v3 trước đó không được tính do provider errors từ Gemini:
> `185620920233`, `193757883769`, `194616666952`, `195746525886`,
> `200311115832`, `214921174144`.

### B2. Failure Analysis

Phân tích các ca thất bại thực tế từ run baseline v0 (`starter_v0/runs/v0_B_base_gemini_20261110T183708553548.json`):

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R03_web_news_routing` | `wrong_arg_value` | `lookup` | Truy vấn bị thừa từ khóa (`'AI news today'` thay vì `'AI'`) | Bổ sung quy tắc trích xuất thực thể cô đọng vào `system_prompt.md` |
| `R10_missing_handle` | `missing_info` | `timeline` | Người dùng chưa đưa tên tài khoản nhưng agent vẫn tự ý gọi `timeline` | Thiết lập luật bắt buộc gọi `clarify` khi thiếu handle trong v2 |
| `R11_missing_url` | `missing_info` | `lookup` | Người dùng yêu cầu đọc bài mà không đưa link, agent tự đoán và tra web | Thiết lập luật bắt buộc gọi `clarify` khi thiếu URL trong v2 |
| `R12_confirm_before_send` | `wrong_boundary` | `send` | Chưa có sự xác nhận của người dùng nhưng agent tự ý gọi `send` | Bổ sung confirmation boundary: chỉ gọi `send` sau khi người dùng duyệt |
| `R13_parallel_web_and_tweets` | `wrong_tool` | `lookup` | Chỉ gọi tìm kiếm web mà bỏ quên lượt gọi mạng xã hội song song | Thêm quy tắc nhận diện truy vấn đa kênh vào prompt v1 |
| `M02_carryover_timeframe` | `wrong_arg_value` | `lookup` | Lượt 2 mang theo từ khóa cũ của lượt 1 gây sai lệch (`'AI robotics news today'`) | Tối ưu context handling trong hội thoại đa lượt ở prompt v3 |
| `M06_switch_tool` | `wrong_arg_value` | `social_search` | Query bị gán thêm hậu tố không mong muốn (`'OpenAI news'`) | Chuẩn hóa convention tham số tìm kiếm trong `tools.yaml` |

### B3. Team Eval Cases

10 trường hợp đánh giá độc lập do nhóm thiết kế trong `starter_v0/data/eval_group.json` (5 single-turn + 5 multi-turn):

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_domain_filter_routing` | Lọc danh sách bài viết theo tên miền cho phép `arxiv.org`, `nature.com` | `domain_filter(items, allowed_domains)` | Sẵn sàng (10/10) |
| `G02_source_audit_routing` | Kiểm toán kỹ thuật metadata title và cú pháp URL HTTP(S) của nguồn | `source_audit(items)` | Sẵn sàng (10/10) |
| `G03_dedup_sources_routing` | Loại bỏ các bài viết trùng lặp URL khỏi danh sách items đã thu thập | `deduplicate_sources(items)` | Sẵn sàng (10/10) |
| `G04_rank_sources_routing` | Xếp hạng bài viết theo từ khóa `transformer` với giới hạn `limit=2` | `rank_sources(items, query, limit)` | Sẵn sàng (10/10) |
| `G05_out_of_scope_creative_writing` | Xử lý yêu cầu sáng tác thơ ngoài phạm vi nhiệm vụ của Research Agent | `no_tool` (từ chối lịch sự, nêu rõ phạm vi hỗ trợ) | Sẵn sàng (10/10) |
| `G06_multiturn_domain_filter_clarify` | Đa lượt: Kế thừa danh sách items từ lượt trước, lọc theo domain `openai.com` | `domain_filter(items, allowed_domains)` | Sẵn sàng (10/10) |
| `G07_multiturn_search_then_dedup` | Đa lượt: Lượt 1 tìm kiếm, lượt 2 đưa danh sách và yêu cầu loại bỏ trùng | `deduplicate_sources(items)` | Sẵn sàng (10/10) |
| `G08_multiturn_audit_sources_followup` | Đa lượt: Lượt 1 gửi danh sách nguồn mẫu, lượt 2 yêu cầu kiểm toán metadata | `source_audit(items)` | Sẵn sàng (10/10) |
| `G09_multiturn_rank_limit_update` | Đa lượt: Kế thừa query `LLM benchmark`, cập nhật tham số `limit` từ 5 thành 3 | `rank_sources(items, query, limit)` | Sẵn sàng (10/10) |
| `G10_multiturn_send_guardrail_refusal` | Đa lượt: Người dùng từ chối xác nhận -> tuyệt đối không được gọi `send` | `no_tool` (xác nhận đã hủy thao tác gửi) | Sẵn sàng (10/10) |

### B4. Live Chat Evidence

Cấu trúc kịch bản hội thoại thực tế được lưu tại `starter_v0/transcripts/`:

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| Turn 1 | "Tìm cho tôi tin tức AI mới nhất trên arXiv" | `papers(query='AI')` | v3 | Trả về danh sách bài báo trích dẫn đầy đủ |
| Turn 2 | "Đọc các tweet mới nhất nhưng không nói rõ của ai" | `clarify(question='...')` | v3 | Agent hỏi lại handle thay vì tự ý gọi tool |
| Turn 3 | "Đăng bản tin này lên Telegram của nhóm" | `clarify(response_type='yes_no')` | v3 | Agent xin xác nhận trước khi thực hiện hành động |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/domain_filter/tool.py`, `TOOL.md`; đăng ký tại `starter_v0/tools/__init__.py` và `starter_v0/artifacts/tools.yaml` | Lọc đúng domain và subdomain hợp lệ; loại bỏ URL giả mạo/lừa đảo; trả error dict an toàn khi sai kiểu input | Không xác minh độ tin cậy hoặc nội dung của trang web |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py` — `domain_filter`: 11 passed; `starter_v0/tests/test_tool_contract.py`: 77 passed | Bắt được subdomain lồng nhau, domain bẩn từ LLM, và lỗi input sai kiểu mà không crash agent | Đây là unit/contract tests, chưa chứng minh model tự route đúng tới tool |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py` | Lệnh chạy: `streamlit run app.py`; giao diện chat trực quan với Streamlit, hiển thị expander tool events | Giao diện demo công khai tự động ẩn credential và không kích hoạt tool `send` |

Tool unit tests: Đã viết 11 unit tests chuyên biệt cho `domain_filter` trong `starter_v0/tests/test_tools_todo.py` (vượt qua 100%). Ví dụ lỗi mà unit test bắt được nhưng eval không bắt được: trường hợp URL giả mạo tinh vi như `example.com.evil.org` hoặc prefix spoofing `fake-example.com` được unit test chặn đứng tại tầng logic của tool.

Eval routing: Đã thiết kế 10 case nhóm trong `starter_v0/data/eval_group.json`, trong đó có G01 và G06 kiểm tra routing tới `domain_filter` kèm assertion đầy đủ `items` và `allowed_domains`.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Hơn 3 tool mới (≥ 4 tool do nhóm tự viết) | `starter_v0/tools/domain_filter/` (đóng góp công cụ thứ 4 cho nhóm đạt mốc ≥ 4 tool) | Đầy đủ `TOOL.md`, đăng ký trong `tools.yaml`, `tools/__init__.py`, 11 unit tests và case route tới trong `eval_group.json` | Đủ điều kiện nhận +3 điểm bonus theo RUBRIC |

### B7. Small Local Model Challenge (bonus)

Bằng chứng setup local (chưa phải benchmark): preflight của repo với alias CPU `qwen2.5:3b-cpu` đã trả về tool call `social_search`; `ollama ps` xác nhận `100% CPU`. Chi tiết lệnh và kết quả: [local_cpu_preflight_2026-11-10.md](evidence/local_cpu_preflight_2026-11-10.md).

## 5. Khó khăn và cách xử lý

1. **Lỗi Quota và 503 Service Unavailable từ Cloud Provider:**
   - Trong quá trình đánh giá các phiên bản v3 trên Gemini cloud (`gemini-2.5-flash-lite`), nhóm nhiều lần gặp lỗi `ServerError: 503 UNAVAILABLE` hoặc giới hạn rate limit khiến run bị gián đoạn.
   - *Cách xử lý:* Ghi nhận trung thực các run gặp lỗi nhà cung cấp (`185620920233`, `200311115832`), thực hiện cơ chế chờ và retry để thu được bản run v3 sạch 100% (`v3_B_base_gemini_20261110T215643805698.json`) với `provider_error_cases = 0`.
2. **Khó khăn về Môi trường Local CUDA:**
   - Khi chạy preflight trên GPU với Ollama model `qwen2.5:3b`, gặp lỗi CUDA driver (`device kernel image is invalid`).
   - *Cách xử lý:* Nhóm trưởng đã cấu hình alias `qwen2.5:3b-cpu` ép chạy trên CPU (`num_gpu=0`), xác nhận preflight thành công trên 100% CPU mà không cần can thiệp driver hệ thống.
3. **Vấn đề so khớp thứ tự danh sách trong Evaluator:**
   - Hàm `normalize_value` mặc định sắp xếp mọi list, khiến các danh sách yêu cầu tính thứ tự nghiêm ngặt (như danh sách `items` trong `deduplicate_sources` hay `rank_sources`) bị so sánh như tập hợp không thứ tự.
   - *Cách xử lý:* Nâng cấp hàm `compare_subset` và `normalize_value` trong `run_eval.py`: giữ nguyên thứ tự tuần tự đối với key `"items"`, chỉ sắp xếp các trường tập hợp (như `allowed_domains`), đồng thời bổ sung 2 contract test xác minh.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của thành viên:
- [Phạm Đăng Quang (2A202603760)](2A202603760_PhamDangQuang.md)

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?**
  - Quy tắc phân định ranh giới giữa các loại công cụ tìm kiếm (arXiv vs Web vs Social).
  - Quy tắc xử lý thông tin thiếu (`clarify`) và ranh giới an toàn (`send` guardrail).
  - Hướng dẫn trích xuất thực thể cô đọng, tránh mang theo các từ khóa dư thừa.
- **Fix nào thuộc `tools.yaml`?**
  - Mô tả rõ ràng ranh giới "Khi nào dùng" và "Khi nào không dùng" cho từng công cụ.
  - Chuẩn hóa các enum hợp lệ và kiểu dữ liệu tham số để mô hình tạo JSON chuẩn xác.
- **Failure nào cần review thủ công thay vì chấm tự động?**
  - Các ca từ chối ngoài phạm vi (`out_of_scope`) hoặc câu hỏi năng lực (`no_tool`): chấm tự động chỉ kiểm tra mô hình có gọi tool hay không, trong khi chất lượng phản hồi văn bản (sự lịch sự, độ chính xác và tính hữu ích) cần con người thẩm định trực tiếp.
- **Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?**
  - Nhóm sẽ thử nghiệm kỹ thuật Few-Shot Demonstration cho các ca hội thoại đa lượt phức tạp, giúp mô hình duy trì ngữ cảnh chính xác mà không bị hiện tượng ảo giác (hallucination) đối với các tham số tìm kiếm qua nhiều lượt.

## 8. Tài liệu tham khảo

- Google GenAI SDK documentation: https://cloud.google.com/vertex-ai/docs/generative-ai/
- Streamlit Documentation: https://docs.streamlit.io/
- Pytest Documentation: https://docs.pytest.org/
