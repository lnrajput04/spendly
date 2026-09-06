"""
Database layer for Spendly.

Step 1 — Database Setup
    get_db()   — returns a SQLite connection with row_factory and foreign keys enabled
    init_db()  — creates all tables using CREATE TABLE IF NOT EXISTS
    seed_db()  — inserts sample data for development (idempotent)
"""

import sqlite3
from pathlib import Path

from werkzeug.security import generate_password_hash

# database/spendly.db, next to this file, independent of CWD
DB_PATH = Path(__file__).parent / "spendly.db"


def get_db():
    """Return a new SQLite connection with row access by column name and FK enforcement on."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create the users and expenses tables if they don't already exist."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            email         TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            description TEXT NOT NULL,
            amount      REAL NOT NULL,
            category    TEXT NOT NULL,
            date        DATE NOT NULL,
            created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def seed_db():
    """Insert sample users/expenses for local development, but only if the DB is empty."""
    conn = get_db()
    existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    if existing == 0:
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (
                "Nitish Kumar",
                "nitish@example.com",
                generate_password_hash("password123", method="pbkdf2:sha256"),
            ),
        )
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (
                "Asha Patel",
                "asha@example.com",
                generate_password_hash("password123", method="pbkdf2:sha256"),
            ),
        )
        conn.commit()

        user_id = conn.execute(
            "SELECT id FROM users WHERE email = ?", ("nitish@example.com",)
        ).fetchone()["id"]

        sample_expenses = [
            (user_id, "Groceries", 42.50, "Food", "2026-08-01"),
            (user_id, "Electricity bill", 65.00, "Utilities", "2026-08-05"),
            (user_id, "Movie tickets", 24.00, "Entertainment", "2026-08-10"),
            (user_id, "Bus pass", 30.00, "Transport", "2026-08-12"),
        ]
        conn.executemany(
            "INSERT INTO expenses (user_id, description, amount, category, date) "
            "VALUES (?, ?, ?, ?, ?)",
            sample_expenses,
        )
        conn.commit()

    conn.close()


def get_user_by_email(email):
    """Return the user row matching email (case-insensitive), or None if not found."""
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email,)
    ).fetchone()
    conn.close()
    return user


def create_user(name, email, password_hash):
    """Insert a new user and return its id."""
    conn = get_db()
    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    conn.commit()

    user_id = conn.execute(
        "SELECT id FROM users WHERE email = ?", (email,)
    ).fetchone()["id"]

    conn.close()
    return user_id
