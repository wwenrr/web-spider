## n8n NiceGUI

Ứng dụng demo dùng NiceGUI với URL path sạch.

Route hiện tại:

- `/dashboard`: danh sách jobs
- `/jobs/create`: tạo mới
- `/jobs/<id>`: xem chi tiết
- `/jobs/<id>/edit`: cập nhật
- `/crawl?site=tiki`: demo query params trên route thật

### Cài đặt

- **Bước 1**: Cài Poetry (nếu chưa có), tham khảo hướng dẫn tại trang chủ Poetry.
- **Bước 2**: Từ thư mục dự án, chạy:

```bash
poetry install
```

### Chạy ứng dụng

```bash
poetry run start
```

Sau khi chạy, mở:

```text
http://localhost:3000
```
