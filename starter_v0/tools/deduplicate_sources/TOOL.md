---
name: deduplicate_sources
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [items, keep_no_url]
outputs: [items, original_count, deduped_count, removed_count]
side_effect: false
requires_confirmation: false
---
# deduplicate_sources

Loại bỏ các bài viết/nguồn tin trùng lặp URL trong danh sách `items`, giữ lại bài viết xuất hiện đầu tiên và bảo toàn thứ tự ban đầu.
