from config.database import get_db


def list_borrows():
    db = get_db()
    return db.execute(
        "SELECT b.id, bk.title, m.name, b.borrow_date, b.return_date FROM borrows b "
        "JOIN books bk ON b.book_id = bk.id JOIN members m ON b.member_id = m.id ORDER BY b.id DESC"
    ).fetchall()


def borrow_book(book_id, member_id):
    db = get_db()
    db.execute(
        "INSERT INTO borrows (book_id, member_id, borrow_date, return_date) VALUES (?, ?, date('now'), NULL)",
        (book_id, member_id),
    )
    db.commit()


def return_book(borrow_id):
    db = get_db()
    db.execute("UPDATE borrows SET return_date = date('now') WHERE id = ?", (borrow_id,))
    db.commit()
