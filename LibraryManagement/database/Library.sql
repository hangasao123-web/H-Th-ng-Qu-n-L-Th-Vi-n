-- =================================================================
-- HỆ THỐNG QUẢN LÝ THƯ VIỆN PRO - CƠ SỞ DỮ LIỆU CHUẨN SQLITE
-- =================================================================

-- Xóa bảng cũ nếu tồn tại để làm sạch dữ liệu khi khởi tạo lại
DROP TABLE IF EXISTS borrows;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS users;

-- 1. BẢNG TÀI KHOẢN (Admin & Thủ thư quản lý hệ thống)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user' CHECK(role IN ('admin', 'user')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. BẢNG ĐỘC GIẢ (Thành viên mượn sách)
CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. BẢNG KHO SÁCH
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT,
    publisher TEXT,
    publish_year INTEGER,
    quantity INTEGER DEFAULT 0 CHECK(quantity >= 0),
    available INTEGER DEFAULT 0 CHECK(available >= 0)
);

-- 4. BẢNG QUẢN LÝ MƯỢN TRẢ SÁCH
-- Sửa lỗi logic: Thêm DEFAULT cho due_date (hạn trả mặc định là 14 ngày kể từ lúc mượn)
CREATE TABLE borrows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    borrow_date DATE DEFAULT CURRENT_DATE,
    due_date DATE DEFAULT (date('now', '+14 days')),
    return_date DATE,
    status TEXT DEFAULT 'Đang mượn' CHECK(status IN ('Đang mượn', 'Đã trả', 'Quá hạn')),
    fine REAL DEFAULT 0.0 CHECK(fine >= 0),
    FOREIGN KEY(member_id) REFERENCES members(id) ON DELETE CASCADE,
    FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE CASCADE
);


-- =================================================================
-- CHÈN DỮ LIỆU MẪU BAN ĐẦU (INITIAL SEED DATA)
-- =================================================================

-- Khởi tạo tài khoản đăng nhập mặc định (Tài khoản: admin / Mật khẩu: 123456)
INSERT INTO users (fullname, username, email, password, role) VALUES 
('Quản trị viên Hệ thống', 'admin', 'admin@library.com', '123456', 'admin'),
('Thủ thư Nguyễn Văn A', 'thuthu01', 'thuthu01@library.com', '123456', 'user');

-- Khởi tạo danh sách độc giả mẫu ban đầu
INSERT INTO members (name, email, phone, address) VALUES 
('Trần Minh Quân', 'quan.tm@gmail.com', '0912345678', 'Hà Nội'),
('Lê Thị Mai', 'mai.lt@gmail.com', '0987654321', 'Đà Nẵng'),
('Phạm Hồng Sơn', 'son.ph@gmail.com', '0905123456', 'TP. Hồ Chí Minh');

-- Khởi tạo một số đầu sách nền tảng (Hệ thống sẽ nạp thêm từ file books.csv sau)
INSERT INTO books (title, author, category, publisher, publish_year, quantity, available) VALUES 
('Đắc Nhân Tâm', 'Dale Carnegie', 'Kỹ năng sống', 'NXB Tổng hợp TP.HCM', 2020, 10, 10),
('Nhà Giả Kim', 'Paulo Coelho', 'Tiểu thuyết', 'NXB Hội Nhà Văn', 2021, 5, 5),
('Số Đỏ', 'Vũ Trọng Phụng', 'Văn học Việt Nam', 'NXB Văn Học', 2019, 7, 7);