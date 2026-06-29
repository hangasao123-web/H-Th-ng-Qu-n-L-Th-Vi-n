import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from config.database import get_db, close_db, init_db_from_files

app = Flask(__name__)
app.secret_key = 'thu_vien_mat_khau_bao_mat_cao_cap_2026'
app.config['DATABASE'] = 'library.db'

# Khởi tạo database và nạp dữ liệu từ books.csv (chỉ lần đầu)
if not os.path.exists('library.db'):
    print("🔧 Lần đầu chạy: Khởi tạo database và nạp dữ liệu từ books.csv...")
    init_db_from_files()

# Đóng kết nối DB sau khi xử lý xong request
app.teardown_appcontext(close_db)

# ==================== AUTH ROUTES ====================

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    
    # Thống kê cho dashboard
    total_books = db.execute('SELECT SUM(quantity) FROM books').fetchone()[0] or 0
    total_titles = db.execute('SELECT COUNT(*) FROM books').fetchone()[0] or 0
    total_members = db.execute('SELECT COUNT(*) FROM members').fetchone()[0] or 0
    active_borrows = db.execute("SELECT COUNT(*) FROM borrows WHERE status = 'Đang mượn'").fetchone()[0] or 0
    overdue_borrows = db.execute("SELECT COUNT(*) FROM borrows WHERE status = 'Quá hạn'").fetchone()[0] or 0
    
    # Lịch sử mượn gần đây
    recent_borrows = db.execute("""
        SELECT b.id, m.name as member_name, bk.title as book_title, b.borrow_date, b.status 
        FROM borrows b
        JOIN members m ON b.member_id = m.id
        JOIN books bk ON b.book_id = bk.id
        ORDER BY b.id DESC LIMIT 5
    """).fetchall()
    
    from datetime import datetime
    now = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    return render_template('index.html', 
        total_books=total_books, total_titles=total_titles,
        total_members=total_members, active_borrows=active_borrows,
        overdue_borrows=overdue_borrows, recent_borrows=recent_borrows,
        datetime=now)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        db = get_db()
        if user := db.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password),
        ).fetchone():
            session['user_id'] = user['id']
            session['fullname'] = user['fullname']
            session['role'] = user['role']
            flash('Đăng nhập hệ thống quản lý thành công!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname'].strip()
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (fullname, username, email, password, role) VALUES (?, ?, ?, ?, ?)",
                (fullname, username, email, password, 'user')
            )
            db.commit()
            flash('Đăng ký tài khoản thành công! Vui lòng đăng nhập.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Tên đăng nhập hoặc email đã tồn tại!', 'danger')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Đã đăng xuất an toàn khỏi hệ thống.', 'info')
    return redirect(url_for('login'))

# ==================== BOOKS ROUTES ====================

@app.route('/books')
def books_list():
    if 'user_id' not in session: 
        return redirect(url_for('login'))
    db = get_db()
    search = request.args.get('search', '').strip()
    
    if search:
        books = db.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY id DESC", 
            (f'%{search}%', f'%{search}%')
        ).fetchall()
    else:
        books = db.execute('SELECT * FROM books ORDER BY id DESC').fetchall()
    
    return render_template('books.html', books=books, search_query=search)

@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if 'user_id' not in session: 
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title'].strip()
        author = request.form['author'].strip()
        category = request.form['category'].strip()
        publisher = request.form.get('publisher', '').strip()
        publish_year = request.form.get('publish_year', '')
        quantity = int(request.form['quantity'])
        
        db = get_db()
        db.execute("""
            INSERT INTO books (title, author, category, publisher, publish_year, quantity, available)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, author, category, publisher, publish_year, quantity, quantity))
        db.commit()
        
        flash('Đã thêm sách mới thành công!', 'success')
        return redirect(url_for('books_list'))
    
    return render_template('add_book.html')

@app.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if 'user_id' not in session: 
        return redirect(url_for('login'))
    
    db = get_db()
    book = db.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    
    if not book:
        flash('Không tìm thấy sách!', 'danger')
        return redirect(url_for('books_list'))
    
    if request.method == 'POST':
        title = request.form['title'].strip()
        author = request.form['author'].strip()
        category = request.form['category'].strip()
        publisher = request.form.get('publisher', '').strip()
        publish_year = request.form.get('publish_year', '')
        quantity = int(request.form['quantity'])
        
        db.execute("""
            UPDATE books 
            SET title=?, author=?, category=?, publisher=?, publish_year=?, quantity=?, available=?
            WHERE id=?
        """, (title, author, category, publisher, publish_year, quantity, quantity, book_id))
        db.commit()
        
        flash('Đã cập nhật thông tin sách!', 'success')
        return redirect(url_for('books_list'))
    
    return render_template('edit_book.html', book=book)

@app.route('/books/delete/<int:book_id>')
def delete_book(book_id):
    if 'user_id' not in session: 
        return redirect(url_for('login'))
    
    db = get_db()
    # Kiểm tra xem sách có đang được mượn không
    borrow_count = db.execute(
        "SELECT COUNT(*) FROM borrows WHERE book_id = ? AND status = 'Đang mượn'", 
        (book_id,)
    ).fetchone()[0]
    
    if borrow_count > 0:
        flash('Không thể xóa sách đang được mượn!', 'danger')
    else:
        db.execute('DELETE FROM books WHERE id = ?', (book_id,))
        db.commit()
        flash('Đã xóa sách thành công!', 'success')
    
    return redirect(url_for('books_list'))

# ==================== MEMBERS ROUTES ====================

@app.route('/members', methods=['GET', 'POST'])
def members_list():
    if 'user_id' not in session: 
        return redirect(url_for('login'))
    
    db = get_db()
    
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        
        try:
            db.execute(
                "INSERT INTO members (name, email, phone, address) VALUES (?, ?, ?, ?)",
                (name, email, phone, address)
            )
            db.commit()
            flash('Đã thêm độc giả mới thành công!', 'success')
        except Exception as e:
            flash('Email đã tồn tại!', 'danger')
        
        return redirect(url_for('members_list'))
    
    members = db.execute('SELECT * FROM members ORDER BY id DESC').fetchall()
    return render_template('members.html', members=members)

@app.route('/members/delete/<int:member_id>')
def delete_member(member_id):
    if 'user_id' not in session: 
        return redirect(url_for('login'))
    
    db = get_db()
    # Kiểm tra xem độc giả có sách đang mượn không
    borrow_count = db.execute(
        "SELECT COUNT(*) FROM borrows WHERE member_id = ? AND status = 'Đang mượn'", 
        (member_id,)
    ).fetchone()[0]
    
    if borrow_count > 0:
        flash('Không thể xóa độc giả đang có sách mượn!', 'danger')
    else:
        db.execute('DELETE FROM members WHERE id = ?', (member_id,))
        db.commit()
        flash('Đã xóa độc giả thành công!', 'success')
    
    return redirect(url_for('members_list'))

# ==================== BORROWS ROUTES ====================

@app.route('/borrows', methods=['GET', 'POST'])
def borrows_list():
    if 'user_id' not in session: 
        return redirect(url_for('login'))
    
    db = get_db()
    
    if request.method == 'POST':
        book_id = request.form['book_id']
        member_id = request.form['member_id']
        due_date = request.form.get('due_date', '')
        
        # Kiểm tra sách còn khả dụng không
        book = db.execute('SELECT available FROM books WHERE id = ?', (book_id,)).fetchone()
        if not book or book['available'] <= 0:
            flash('Sách này đã hết, không thể mượn!', 'danger')
            return redirect(url_for('borrows_list'))
        
        # Tạo phiếu mượn
        db.execute("""
            INSERT INTO borrows (member_id, book_id, borrow_date, due_date, status)
            VALUES (?, ?, DATE('now'), ?, 'Đang mượn')
        """, (member_id, book_id, due_date if due_date else None))
        
        # Cập nhật số lượng sách
        db.execute('UPDATE books SET available = available - 1 WHERE id = ?', (book_id,))
        db.commit()
        
        flash('Đã lập phiếu mượn sách thành công!', 'success')
        return redirect(url_for('borrows_list'))
    
    # Lấy danh sách phiếu mượn với thông tin đầy đủ
    borrows = db.execute("""
        SELECT b.id, bk.title as book_title, m.name as member_name, 
               b.borrow_date, b.due_date, b.return_date, b.status, b.fine
        FROM borrows b
        JOIN books bk ON b.book_id = bk.id
        JOIN members m ON b.member_id = m.id
        ORDER BY b.id DESC
    """).fetchall()
    
    books = db.execute('SELECT id, title, available FROM books WHERE available > 0').fetchall()
    members = db.execute('SELECT id, name FROM members').fetchall()
    
    return render_template('borrow.html', borrows=borrows, books=books, members=members)

@app.route('/borrows/return/<int:borrow_id>')
def return_borrow(borrow_id):
    if 'user_id' not in session: 
        return redirect(url_for('login'))

    db = get_db()
    if borrow := db.execute(
        'SELECT book_id, due_date FROM borrows WHERE id = ?', (borrow_id,)
    ).fetchone():
        # Tính tiền phạt nếu quá hạn
        from datetime import datetime
        due_date = datetime.strptime(borrow['due_date'], '%Y-%m-%d')
        today = datetime.now()
        fine = 0

        if today > due_date:
            days_late = (today - due_date).days
            fine = days_late * 5000  # 5000 VNĐ/ngày

        # Cập nhật trạng thái
        status = 'Quá hạn' if fine > 0 else 'Đã trả'

        db.execute("""
            UPDATE borrows 
            SET return_date = DATE('now'), status = ?, fine = ?
            WHERE id = ?
        """, (status, fine, borrow_id))

        # Cập nhật số lượng sách
        db.execute('UPDATE books SET available = available + 1 WHERE id = ?', 
                  (borrow['book_id'],))
        db.commit()

        if fine > 0:
            flash(f'Đã trả sách! Tiền phạt quá hạn: {fine:,.0f} VNĐ', 'warning')
        else:
            flash('Đã hoàn tất thủ tục nhận trả sách!', 'success')

    return redirect(url_for('borrows_list'))

# ==================== STATISTICS ROUTE ====================

@app.route('/statistics')
def statistics():
    if 'user_id' not in session: 
        return redirect(url_for('login'))
    
    db = get_db()
    
    # Thống kê chi tiết
    total_books = db.execute('SELECT COUNT(*) FROM books').fetchone()[0]
    total_members = db.execute('SELECT COUNT(*) FROM members').fetchone()[0]
    total_borrows = db.execute('SELECT COUNT(*) FROM borrows').fetchone()[0]
    active_borrows = db.execute("SELECT COUNT(*) FROM borrows WHERE status = 'Đang mượn'").fetchone()[0]
    overdue_borrows = db.execute("SELECT COUNT(*) FROM borrows WHERE status = 'Quá hạn'").fetchone()[0]
    total_fine = db.execute("SELECT COALESCE(SUM(fine), 0) FROM borrows").fetchone()[0]
    
    # Thống kê theo thể loại
    categories = db.execute("""
        SELECT category, COUNT(*) as count, SUM(quantity) as total_qty
        FROM books 
        WHERE category IS NOT NULL AND category != ''
        GROUP BY category
        ORDER BY count DESC
    """).fetchall()
    
    # Thống kê mượn theo tháng (6 tháng gần nhất)
    monthly_stats = db.execute("""
        SELECT strftime('%Y-%m', borrow_date) as month, COUNT(*) as count
        FROM borrows
        WHERE borrow_date >= date('now', '-6 months')
        GROUP BY month
        ORDER BY month
    """).fetchall()
    
    return render_template('statistics.html',
        total_books=total_books, total_members=total_members,
        total_borrows=total_borrows, active_borrows=active_borrows,
        overdue_borrows=overdue_borrows, total_fine=total_fine,
        categories=categories, monthly_stats=monthly_stats)

# ==================== MAIN ====================

if __name__ == '__main__':
    # Kiểm tra nếu chưa tồn tại cơ sở dữ liệu, tự động chạy liên kết nạp dữ liệu
    if not os.path.exists('library.db'):
        with app.app_context():
            print("[!] Phát hiện hệ thống chạy lần đầu, đang thiết lập cơ sở dữ liệu...")
            init_db_from_files()
    app.run(debug=True, host='0.0.0.0', port=5000)
