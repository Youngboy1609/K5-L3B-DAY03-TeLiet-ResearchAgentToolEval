---
name: source_audit
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [items]
outputs: [ok, checked_count, valid_count, issues]
side_effect: false
requires_confirmation: false
---
# source_audit

Kiểm tra tính hợp lệ về mặt kỹ thuật của danh sách nguồn tin (`items`): URL có đúng định dạng HTTP/HTTPS không và có thông tin metadata cơ bản không. Tool chỉ kiểm tra metadata, không xác minh nội dung là thật hay giả.
