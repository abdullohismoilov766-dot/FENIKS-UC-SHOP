"""
SQLite qatlami: foydalanuvchilar, kundalik rejalar va ularning kunlik natijalari.

Uch jadval:
  users      — kimning qaysi vaqt mintaqasi va faol kun oralig'i
  tasks      — kundalik rejalar (nomi, nechidan nechigacha, takrorlanishi)
  task_logs  — har bir reja x har bir kun uchun natija (pending/done/missed);
               aynan shu jadval statistikaning manbasi
"""

from __future__ import annotations

import sqlite3
from contextlib import closing
from datetime import datetime, timezone

from planner_bot.config import DB_PATH, DEFAULT_DAY_END, DEFAULT_DAY_START, DEFAULT_TZ

STATUS_PENDING = "pending"
STATUS_DONE = "done"
STATUS_MISSED = "missed"

STATUS_LABELS = {
    STATUS_PENDING: "⏳ Kutilmoqda",
    STATUS_DONE: "✅ Bajarildi",
    STATUS_MISSED: "❌ Bajarilmadi",
}


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_db() -> None:
    with closing(_connect()) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id          INTEGER PRIMARY KEY,
                full_name        TEXT,
                username         TEXT,
                tz               TEXT NOT NULL,
                day_start        TEXT NOT NULL,
                day_end          TEXT NOT NULL,
                remind_on_start  INTEGER NOT NULL DEFAULT 1,
                created_at       TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                title       TEXT NOT NULL,
                start_time  TEXT NOT NULL,
                end_time    TEXT NOT NULL,
                repeat      TEXT NOT NULL DEFAULT 'daily',
                on_date     TEXT,
                active      INTEGER NOT NULL DEFAULT 1,
                created_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS task_logs (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id           INTEGER NOT NULL,
                user_id           INTEGER NOT NULL,
                log_date          TEXT NOT NULL,
                status            TEXT NOT NULL DEFAULT 'pending',
                started_notified  INTEGER NOT NULL DEFAULT 0,
                asked_at          TEXT,
                answered_at       TEXT,
                UNIQUE (task_id, log_date)
            );

            CREATE INDEX IF NOT EXISTS idx_tasks_user ON tasks (user_id, active);
            CREATE INDEX IF NOT EXISTS idx_logs_user_date ON task_logs (user_id, log_date);
            """
        )
        conn.commit()


# -------------------------------------------------------------- users ------
def ensure_user(user_id: int, full_name: str = "", username: str | None = None) -> sqlite3.Row:
    with closing(_connect()) as conn:
        conn.execute(
            """
            INSERT INTO users (user_id, full_name, username, tz, day_start, day_end, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                full_name = excluded.full_name,
                username  = excluded.username
            """,
            (
                user_id,
                full_name,
                username,
                DEFAULT_TZ,
                DEFAULT_DAY_START,
                DEFAULT_DAY_END,
                _utcnow(),
            ),
        )
        conn.commit()
        return conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()


def get_user(user_id: int) -> sqlite3.Row | None:
    with closing(_connect()) as conn:
        return conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()


def all_users() -> list[sqlite3.Row]:
    with closing(_connect()) as conn:
        return conn.execute("SELECT * FROM users").fetchall()


def update_user(user_id: int, **fields) -> None:
    allowed = {"tz", "day_start", "day_end", "remind_on_start"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return
    assignments = ", ".join(f"{k} = ?" for k in updates)
    with closing(_connect()) as conn:
        conn.execute(
            f"UPDATE users SET {assignments} WHERE user_id = ?",
            (*updates.values(), user_id),
        )
        conn.commit()


# -------------------------------------------------------------- tasks ------
def create_task(
    user_id: int,
    title: str,
    start_time: str,
    end_time: str,
    repeat: str = "daily",
    on_date: str | None = None,
) -> int:
    with closing(_connect()) as conn:
        cur = conn.execute(
            """
            INSERT INTO tasks (user_id, title, start_time, end_time, repeat, on_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, title, start_time, end_time, repeat, on_date, _utcnow()),
        )
        conn.commit()
        return cur.lastrowid


def get_task(task_id: int) -> sqlite3.Row | None:
    with closing(_connect()) as conn:
        return conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()


def get_tasks(user_id: int, only_active: bool = True) -> list[sqlite3.Row]:
    query = "SELECT * FROM tasks WHERE user_id = ?"
    if only_active:
        query += " AND active = 1"
    query += " ORDER BY start_time, id"
    with closing(_connect()) as conn:
        return conn.execute(query, (user_id,)).fetchall()


def set_task_active(task_id: int, active: bool) -> None:
    with closing(_connect()) as conn:
        conn.execute("UPDATE tasks SET active = ? WHERE id = ?", (1 if active else 0, task_id))
        conn.commit()


def delete_task(task_id: int) -> None:
    with closing(_connect()) as conn:
        conn.execute("DELETE FROM task_logs WHERE task_id = ?", (task_id,))
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()


# ----------------------------------------------------------- task_logs -----
def get_or_create_log(task_id: int, user_id: int, log_date: str) -> sqlite3.Row:
    with closing(_connect()) as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO task_logs (task_id, user_id, log_date, status)
            VALUES (?, ?, ?, ?)
            """,
            (task_id, user_id, log_date, STATUS_PENDING),
        )
        conn.commit()
        return conn.execute(
            "SELECT * FROM task_logs WHERE task_id = ? AND log_date = ?",
            (task_id, log_date),
        ).fetchone()


def get_log(task_id: int, log_date: str) -> sqlite3.Row | None:
    with closing(_connect()) as conn:
        return conn.execute(
            "SELECT * FROM task_logs WHERE task_id = ? AND log_date = ?",
            (task_id, log_date),
        ).fetchone()


def mark_started_notified(task_id: int, log_date: str) -> None:
    with closing(_connect()) as conn:
        conn.execute(
            "UPDATE task_logs SET started_notified = 1 WHERE task_id = ? AND log_date = ?",
            (task_id, log_date),
        )
        conn.commit()


def mark_asked(task_id: int, log_date: str) -> None:
    with closing(_connect()) as conn:
        conn.execute(
            "UPDATE task_logs SET asked_at = ? WHERE task_id = ? AND log_date = ?",
            (_utcnow(), task_id, log_date),
        )
        conn.commit()


def set_log_status(task_id: int, log_date: str, status: str, answered: bool = True) -> None:
    with closing(_connect()) as conn:
        if answered:
            conn.execute(
                "UPDATE task_logs SET status = ?, answered_at = ? WHERE task_id = ? AND log_date = ?",
                (status, _utcnow(), task_id, log_date),
            )
        else:
            conn.execute(
                "UPDATE task_logs SET status = ? WHERE task_id = ? AND log_date = ?",
                (status, task_id, log_date),
            )
        conn.commit()


def unanswered_logs() -> list[sqlite3.Row]:
    """Savol berilgan, lekin hali javob berilmagan yozuvlar."""
    with closing(_connect()) as conn:
        return conn.execute(
            "SELECT * FROM task_logs WHERE status = ? AND asked_at IS NOT NULL",
            (STATUS_PENDING,),
        ).fetchall()


def logs_for_date(user_id: int, log_date: str) -> list[sqlite3.Row]:
    with closing(_connect()) as conn:
        return conn.execute(
            """
            SELECT l.*, t.title, t.start_time, t.end_time
              FROM task_logs l
              JOIN tasks t ON t.id = l.task_id
             WHERE l.user_id = ? AND l.log_date = ?
             ORDER BY t.start_time
            """,
            (user_id, log_date),
        ).fetchall()


# ---------------------------------------------------------- statistika -----
def status_counts(user_id: int, date_from: str, date_to: str) -> dict[str, int]:
    with closing(_connect()) as conn:
        rows = conn.execute(
            """
            SELECT status, COUNT(*) AS n
              FROM task_logs
             WHERE user_id = ? AND log_date BETWEEN ? AND ?
             GROUP BY status
            """,
            (user_id, date_from, date_to),
        ).fetchall()
    counts = {STATUS_DONE: 0, STATUS_MISSED: 0, STATUS_PENDING: 0}
    for row in rows:
        counts[row["status"]] = row["n"]
    return counts


def per_task_counts(user_id: int, date_from: str, date_to: str) -> list[sqlite3.Row]:
    with closing(_connect()) as conn:
        return conn.execute(
            """
            SELECT t.id, t.title, t.start_time, t.end_time,
                   SUM(CASE WHEN l.status = 'done'    THEN 1 ELSE 0 END) AS done,
                   SUM(CASE WHEN l.status = 'missed'  THEN 1 ELSE 0 END) AS missed,
                   SUM(CASE WHEN l.status = 'pending' THEN 1 ELSE 0 END) AS pending
              FROM task_logs l
              JOIN tasks t ON t.id = l.task_id
             WHERE l.user_id = ? AND l.log_date BETWEEN ? AND ?
             GROUP BY t.id
             ORDER BY missed DESC, done DESC
            """,
            (user_id, date_from, date_to),
        ).fetchall()


def daily_totals(user_id: int, date_from: str, date_to: str) -> list[sqlite3.Row]:
    with closing(_connect()) as conn:
        return conn.execute(
            """
            SELECT log_date,
                   SUM(CASE WHEN status = 'done'   THEN 1 ELSE 0 END) AS done,
                   SUM(CASE WHEN status = 'missed' THEN 1 ELSE 0 END) AS missed,
                   COUNT(*) AS total
              FROM task_logs
             WHERE user_id = ? AND log_date BETWEEN ? AND ?
             GROUP BY log_date
             ORDER BY log_date
            """,
            (user_id, date_from, date_to),
        ).fetchall()
