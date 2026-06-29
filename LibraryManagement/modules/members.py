from config.database import get_db


def list_members():
    db = get_db()
    return db.execute("SELECT * FROM members ORDER BY id DESC").fetchall()


def add_member(name, email, phone):
    db = get_db()
    db.execute(
        "INSERT INTO members (name, email, phone) VALUES (?, ?, ?)",
        (name, email, phone),
    )
    db.commit()
