import os
import sqlite3
import csv
from flask import g, current_app

def get_db():
    if "db" not in g:
        try:
            # Lấy cấu hình từ Flask App nếu đã vào luồng request
            db_path = current_app.config.get("DATABASE", "library.db")
        except RuntimeError:
            # Phương án dự phòng nếu chạy bên ngoài luồng context
            db_path = "library.db"
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    """
    Hàm khởi tạo độc lập: Tự kết nối trực tiếp đến file SQLite, loại bỏ hoàn toàn 
    sự phụ thuộc vào Flask Context để tránh tuyệt đối lỗi RuntimeError.
    """
    db_path = "library.db"
    print(f"[...] Đang tiến hành kết nối thiết lập cơ sở dữ liệu: {db_path}")
    db = sqlite3.connect(db_path)

    # Xác định đường dẫn thư mục gốc và file schema
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Thử các đường dẫn có thể có
    possible_paths = [
        os.path.join(base_dir, "database", "Library.sql"),  # database/Library.sql
        os.path.join(base_dir, "Library.sql"),              # Library.sql ở root
        "database/Library.sql",                             # relative path
        "Library.sql"                                       # current dir
    ]
    
    schema_path = None
    for path in possible_paths:
        if os.path.exists(path):
            schema_path = path
            break
    
    # 1. Đọc và thực thi cấu trúc bảng từ Library.sql
    if schema_path:
        _extracted_from_init_db_16(
            schema_path,
            db,
            f"[OK] Đã cấu hình cấu trúc bảng thành công từ {schema_path}!",
        )
    else:
        print("[Lỗi nghiêm trọng] Không tìm thấy file cấu trúc Library.sql!")
        print(f"Đã thử các đường dẫn: {possible_paths}")
        db.close()
        return

    # 2. Đọc file dữ liệu đối tác books.csv và nạp bổ sung vào bảng sách
    csv_path = os.path.join(base_dir, "books.csv")
    if not os.path.exists(csv_path) and os.path.exists("books.csv"):
        csv_path = "books.csv"

    if os.path.exists(csv_path):
        with open(csv_path, mode='r', encoding='utf-8-sig', errors='ignore') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader, None) # Bỏ qua dòng tiêu đề cột

            count = 0
            for row in reader:
                if len(row) >= 5:
                    title = row[1].strip()
                    author = row[2].strip()
                    publisher = row[4].strip()
                    try:
                        publish_year = int(row[3].strip())
                    except ValueError:
                        publish_year = 2026

                    # Kiểm tra trùng lặp tựa đề sách để tránh làm chật bộ nhớ
                    cursor = db.cursor()
                    cursor.execute("SELECT id FROM books WHERE title = ? AND author = ?", (title, author))
                    if not cursor.fetchone():
                        cursor.execute("""
                            INSERT INTO books (title, author, category, publisher, publish_year, quantity, available)
                            VALUES (?, ?, ?, ?, ?, 10, 10)
                        """, (title, author, "Văn học", publisher, publish_year))
                        count += 1
                if count >= 100: # Lấy tối đa 100 cuốn sách mẫu chất lượng cao từ CSV
                    break
        db.commit()
        print(f"[OK] Đã liên kết và nạp thành công {count} cuốn sách từ tập dữ liệu books.csv!")
    else:
        print("[Cảnh báo] Không tìm thấy file dữ liệu books.csv để nạp bổ sung.")

    db.close()


# TODO Rename this here and in `init_db`
def _extracted_from_init_db_16(arg0, db, arg2):
    with open(arg0, "r", encoding="utf-8") as file:
        db.executescript(file.read())
    db.commit()
    print(arg2)

# Tạo bí danh (alias) bảo mật để ngăn lỗi AttributeError dù app.py gọi theo tên nào
init_db_from_files = init_db