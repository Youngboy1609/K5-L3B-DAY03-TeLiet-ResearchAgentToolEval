---
name: rank_sources
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [items, query, limit]
outputs: [items, ranked_count, query_terms]
side_effect: false
requires_confirmation: false
---
# rank_sources

Sắp xếp các item/nguồn tin theo mức độ trùng lặp từ khóa (`keyword overlap`) giữa câu truy vấn `query` với tiêu đề (`title`) và tóm tắt (`summary`). Đây là thuật toán heuristic từ vựng đơn giản, không phản ánh độ tin cậy hay tính xác thực của nội dung.
