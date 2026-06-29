from functools import wraps

from flask import redirect, session, url_for

from config.database import get_db


def login_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return decorated_view


def login_user(username, password):
    db = get_db()
    user = db.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    return user is not None


def register_user(fullname, username, email, password):
    db = get_db()
    db.execute(
        "INSERT INTO users (fullname, username, email, password, role) VALUES (?, ?, ?, ?, ?)",
        (fullname, username, email, password, "user"),
    )
    db.commit()


def logout_user():
    session.pop("user", None)
