"""
Buyurtmalarni saqlash uchun oddiy SQLite qatlami.

Har bir buyurtma: kim, qaysi PUBG ID ga, qancha UC, qancha narx, chek fayli
(Telegram file_id sifatida) va holati (kutilmoqda / tasdiqlangan / rad etilgan).
"""

import sqlite3
from contextlib import closing
from datetime import datetime

from config import DB_PATH

STATUS_PENDING = "kutilmoqda"
STATUS_APPROVED = "tasdiqlandi"
STATUS_REJECTED = "rad_etildi"

STATUS_LABELS = {
    STATUS_PENDING: "⏳ Kutilmoqda",
    STATUS_APPROVED: "✅ Tasdiqlandi",
    STATUS_REJECTED: "❌ Rad etildi",
}


def init_db() -> None:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                full_name TEXT,
                player_id TEXT,
                uc_amount INTEGER,
                price INTEGER,
                receipt_file_id TEXT,
                status TEXT NOT NULL DEFAULT 'kutilmoqda',
                admin_message_id INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def create_order(
    user_id: int,
    username: str | None,
    full_name: str,
    player_id: str,
    uc_amount: int,
    price: int,
) -> int:
    now = datetime.utcnow().isoformat()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.execute(
            """
            INSERT INTO orders
                (user_id, username, full_name, player_id, uc_amount, price,
                 status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                full_name,
                player_id,
                uc_amount,
                price,
                STATUS_PENDING,
                now,
                now,
            ),
        )
        conn.commit()
        return cur.lastrowid


def attach_receipt(order_id: int, file_id: str) -> None:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            "UPDATE orders SET receipt_file_id = ?, updated_at = ? WHERE id = ?",
            (file_id, datetime.utcnow().isoformat(), order_id),
        )
        conn.commit()


def set_admin_message_id(order_id: int, message_id: int) -> None:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            "UPDATE orders SET admin_message_id = ? WHERE id = ?",
            (message_id, order_id),
        )
        conn.commit()


def update_status(order_id: int, status: str) -> None:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            "UPDATE orders SET status = ?, updated_at = ? WHERE id = ?",
            (status, datetime.utcnow().isoformat(), order_id),
        )
        conn.commit()


def get_order(order_id: int) -> sqlite3.Row | None:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        return cur.fetchone()


def get_user_orders(user_id: int, limit: int = 10) -> list[sqlite3.Row]:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(
            "SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit),
        )
        return cur.fetchall()
