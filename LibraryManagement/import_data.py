import csv
import os
import sqlite3

# Định nghĩa đường dẫn tới file CSV và Database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "database", "books.csv")
DB_FILE = os.path.join(BASE_DIR, "database", "library.db")


def import_books_from_csv():
    # 1. Kiểm tra xem file có tồn tại không
    if not os.path.exists(CSV_FILE):
        print(f"❌ LỖI: Không tìm thấy file '{CSV_FILE}' ở thư mục gốc!")
        return

    if not os.path.exists(DB_FILE):
        print(
            f"❌ LỖI: Chưa có file database '{DB_FILE}'. Hãy chạy app.py 1 lần để tạo db trước!"
        )
        return

    print("⏳ Đang kết nối tới cơ sở dữ liệu SQLite...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 2. Xóa dữ liệu sách cũ để tránh bị trùng lặp khi chạy đi chạy lại nhiều lần
    cursor.execute("DELETE FROM books")

    count = 0
    print("⏳ Đang đọc file books.csv và nạp dữ liệu...")

    # 3. Mở và đọc file CSV (Dùng utf-8-sig để tự động xóa ký tự BOM lỗi phông Excel)
    try:
        with open(CSV_FILE, mode="r", encoding="utf-8-sig") as file:
            # File của bạn phân cách bằng dấu chấm phẩy (;)
            csv_reader = csv.DictReader(file, delimiter=";")

            for row in csv_reader:
                """
                LƯU Ý: Nếu tên cột trong file books.csv của bạn khác với bên dưới,
                hãy sửa lại các chữ trong ngoặc kép ['...'] cho đúng với dòng đầu tiên của file CSV.
                Ví dụ: row['TenSach'], row['TacGia'] v.v...
                """
                title = (
                    row.get("title")
                    or row.get("Title")
                    or row.get("Tên sách")
                    or "Chưa rõ tên"
                )
                author = (
                    row.get("author")
                    or row.get("Author")
                    or row.get("Tác giả")
                    or "Chưa rõ tác giả"
                )
                category = (
                    row.get("category")
                    or row.get("Category")
                    or row.get("Thể loại")
                    or "Khác"
                )
                publisher = (
                    row.get("publisher")
                    or row.get("Publisher")
                    or row.get("Nhà xuất bản")
                    or "NXB Khác"
                )

                # Xử lý số năm và số lượng (nếu CSV bị trống thì để giá trị mặc định)
                try:
                    year = int(
                        row.get("publish_year")
                        or row.get("Year")
                        or row.get("Năm XB")
                        or 2023
                    )
                except ValueError:
                    year = 2023

                try:
                    quantity = int(
                        row.get("quantity")
                        or row.get("Quantity")
                        or row.get("Số lượng")
                        or 10
                    )
                except ValueError:
                    quantity = 10

                # Số sách sẵn có cho mượn mặc định ban đầu bằng đúng tổng số lượng
                available = quantity

                # Bơm vào Database
                sql = """
                INSERT INTO books (title, author, category, publisher, publish_year, quantity, available)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(
                    sql,
                    (
                        title.strip(),
                        author.strip(),
                        category.strip(),
                        publisher.strip(),
                        year,
                        available,
                        available,
                    ),
                )
                count += 1

        conn.commit()
        print(
            f"\n🎉 XONG! Đã nạp thành công {count} cuốn sách từ dataset vào hệ thống."
        )

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Có lỗi xảy ra trong quá trình đọc CSV: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    import_books_from_csv()