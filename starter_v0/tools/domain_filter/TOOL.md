---
name: domain_filter
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [items, allowed_domains]
outputs: [items, matched_count, filtered_out_count]
side_effect: false
requires_confirmation: false
---
# domain_filter

Lọc danh sách các bài viết / nguồn tin đã thu thập (`items`), chỉ giữ lại các item thuộc danh sách tên miền cho phép (`allowed_domains`).

## Đặc điểm kỹ thuật
- **Khớp domain chính xác:** `example.com` khớp `example.com`.
- **Khớp subdomain hợp lệ:** `news.example.com` và `sub.news.example.com` khớp `example.com`.
- **Chống lừa đảo:** `example.com.evil.org` hoặc `fake-example.com` bị loại bỏ an toàn.
- **Xử lý lỗi:** Không bao giờ raise exception; trả về error dict nếu input truyền sai kiểu dữ liệu.
- **Không truy cập mạng:** Chỉ xử lý lọc metadata cục bộ trên danh sách items đã có.
