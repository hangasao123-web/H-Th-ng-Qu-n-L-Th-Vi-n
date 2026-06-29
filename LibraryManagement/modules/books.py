from config.database import get_db


def list_books():
    db = get_db()
    return db.execute(
        "SELECT * FROM books ORDER BY id DESC"
    ).fetchall()


def get_book(book_id):
    db = get_db()
    return db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()


def add_book(title, author, category, quantity):
    db = get_db()
    db.execute(
        "INSERT INTO books (title, author, category, quantity) VALUES (?, ?, ?, ?)",
        (title, author, category, quantity),
    )
    db.commit()


def update_book(book_id, title, author, category, quantity):
    db = get_db()
    db.execute(
        "UPDATE books SET title = ?, author = ?, category = ?, quantity = ? WHERE id = ?",
        (title, author, category, quantity, book_id),
    )
    db.commit()
