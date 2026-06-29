# 📚 Library Pro - Hệ Thống Quản Lý Thư Viện

Hệ thống quản lý thư viện hiện đại được xây dựng với Flask, có giao diện đẹp và đầy đủ chức năng.

## ✨ Tính năng

### 🔐 Quản lý người dùng
- Đăng nhập / Đăng xuất
- Đăng ký tài khoản thủ thư
- Phân quyền (Admin/User)

### 📖 Quản lý sách
- Thêm sách mới
- Chỉnh sửa thông tin sách
- Xóa sách (kiểm tra trạng thái mượn)
- Tìm kiếm sách theo tên/tác giả
- Quản lý số lượng sách

### 👥 Quản lý độc giả
- Đăng ký độc giả mới
- Xem danh sách độc giả
- Xóa độc giả (kiểm tra sách đang mượn)
- Quản lý thông tin liên hệ

### 🔄 Quản lý mượn trả
- Lập phiếu mượn sách
- Tự động tính hạn trả (14 ngày)
- Nhận trả sách
- Tính tiền phạt quá hạn (5,000 VNĐ/ngày)
- Theo dõi trạng thái mượn

### 📊 Thống kê & Báo cáo
- Dashboard tổng quan
- Thống kê theo thể loại sách
- Biểu đồ mượn sách theo tháng
- Báo cáo sách quá hạn
- Thống kê tiền phạt

## 🎨 Giao diện

- **Thiết kế hiện đại**: Giao diện đẹp mắt, chuyên nghiệp
- **Responsive**: Tương thích mọi thiết bị (Desktop, Tablet, Mobile)
- **Sidebar navigation**: Thanh điều hướng bên trái
- **Bootstrap 5**: Framework CSS mới nhất
- **FontAwesome**: Icon đẹp và đa dạng
- **Chart.js**: Biểu đồ trực quan
- **Animations**: Hiệu ứng mượt mà

## 🗄️ Cơ sở dữ liệu

### Các bảng chính:
1. **users** - Tài khoản người dùng
2. **members** - Độc giả
3. **books** - Kho sách
4. **borrows** - Phiếu mượn trả

### Dữ liệu mẫu:
- Tài khoản admin mặc định: `admin` / `123456`
- Tài khoản thủ thư: `thuthu01` / `123456`
- 3 độc giả mẫu
- 3 sách mẫu + dữ liệu từ books.csv

## 🚀 Cài đặt & Chạy

### Yêu cầu
- Python 3.8+
- pip (Python package manager)

### Các bước cài đặt:

1. **Clone hoặc tải project**
```bash
cd LibraryManagement
```

2. **Cài đặt dependencies**
```bash
pip install -r requirements.txt
```

3. **Khởi tạo database (lần đầu chạy)**
```bash
python app.py
```
Hệ thống sẽ tự động:
- Tạo file `library.db`
- Chạy script SQL từ `database/Library.sql`
- Nạp dữ liệu từ `database/books.csv`

4. **Truy cập ứng dụng**
```
Mở trình duyệt: http://localhost:5000
Đăng nhập với: admin / 123456
```

## 📁 Cấu trúc thư mục

```
LibraryManagement/
├── app.py                      # File chính Flask
├── config/
│   └── database.py             # Cấu hình database
├── database/
│   ├── Library.sql             # Schema database
│   └── books.csv               # Dữ liệu sách mẫu
├── modules/
│   ├── auth.py                 # Xác thực người dùng
│   ├── books.py                # Thao tác sách
│   ├── borrow.py               # Mượn trả sách
│   └── members.py              # Quản lý độc giả
├── static/
│   ├── css/
│   │   └── style.css           # Styles chính
│   ├── js/
│   │   └── script.js           # JavaScript
│   └── images/                 # Hình ảnh
├── templates/
│   ├── base.html               # Template gốc
│   ├── index.html              # Dashboard
│   ├── login.html              # Đăng nhập
│   ├── register.html           # Đăng ký
│   ├── books.html              # Danh sách sách
│   ├── add_book.html           # Thêm sách
│   ├── edit_book.html          # Sửa sách
│   ├── members.html            # Quản lý độc giả
│   ├── borrow.html             # Mượn trả
│   └── statistics.html         # Thống kê
├── library.db                  # Database SQLite (tự động tạo)
├── requirements.txt            # Dependencies
└── README.md                   # Tài liệu
```

## 🎯 Cách sử dụng

### 1. Đăng nhập
- Truy cập `http://localhost:5000`
- Nhập tài khoản: `admin` / `123456`

### 2. Quản lý sách
- Vào menu **Kho sách**
- Thêm sách mới bằng nút "Thêm sách mới"
- Tìm kiếm theo tên hoặc tác giả
- Sửa/Xóa sách bằng các nút chức năng

### 3. Quản lý độc giả
- Vào menu **Độc giả**
- Điền thông tin form bên trái
- Xem danh sách bên phải
- Xóa độc giả nếu không còn mượn sách

### 4. Mượn trả sách
- Vào menu **Mượn trả**
- Chọn sách, độc giả, hạn trả
- Nhấn "Cho mượn"
- Trả sách bằng nút "Trả" (tự động tính phạt nếu quá hạn)

### 5. Xem thống kê
- Vào menu **Thống kê**
- Xem biểu đồ phân tích
- Theo dõi tình hình hoạt động

## 🔧 Cấu hình

### Database Configuration
File `config/database.py`:
```python
app.config['DATABASE'] = 'library.db'
```

### Secret Key
File `app.py`:
```python
app.secret_key = 'thu_vien_mat_khau_bao_mat_cao_cap_2026'
```

## 🛠️ Công nghệ sử dụng

- **Backend**: Flask 3.0.2
- **Database**: SQLite3
- **Frontend**: 
  - Bootstrap 5.3.3
  - FontAwesome 6.4.2
  - Chart.js (biểu đồ)
- **Python**: 3.8+

## 📝 Ghi chú

- Database tự động khởi tạo khi chạy lần đầu
- Dữ liệu sách được nạp từ `books.csv` (tối đa 100 cuốn)
- Tiền phạt quá hạn: 5,000 VNĐ/ngày
- Hạn mượn mặc định: 14 ngày
- Hệ thống tự động cập nhật trạng thái "Quá hạn"

## 🐛 Troubleshooting

### Lỗi "Database is locked"
- Đóng tất cả các tiến trình Python đang chạy
- Xóa file `library.db` và chạy lại

### Lỗi "Module not found"
```bash
pip install Flask==3.0.2 Werkzeug==3.0.1
```

### Port 5000 đã được sử dụng
```bash
# Thay đổi port trong app.py
app.run(debug=True, port=5001)
```

## 📞 Hỗ trợ

Nếu có vấn đề, vui lòng kiểm tra:
1. Python version >= 3.8
2. Tất cả dependencies đã được cài đặt
3. File `database/Library.sql` tồn tại
4. Quyền ghi file trong thư mục project

## 📄 License

MIT License - Free to use for educational purposes.

---

**Phát triển bởi**: Library Pro Team  
**Phiên bản**: 1.0.0  
**Cập nhật**: 2026