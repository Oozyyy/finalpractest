import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "scores.db")


def get_connection(db_path=None):
    path = db_path if db_path is not None else DB_PATH
    return sqlite3.connect(path)


def init_db(db_path=None):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            attempts INTEGER NOT NULL,
            min_number INTEGER NOT NULL,
            max_number INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_score(player_name, attempts, min_number=1, max_number=100, db_path=None):
    if not player_name or not str(player_name).strip():
        raise ValueError("Имя игрока не может быть пустым")
    if not isinstance(attempts, int) or isinstance(attempts, bool) or attempts <= 0:
        raise ValueError("Количество попыток должно быть положительным целым числом")
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scores (player_name, attempts, min_number, max_number) VALUES (?, ?, ?, ?)",
        (str(player_name).strip(), attempts, min_number, max_number),
    )
    conn.commit()
    conn.close()


def get_top_scores(limit=10, db_path=None):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT player_name, attempts, min_number, max_number, created_at "
        "FROM scores ORDER BY attempts ASC LIMIT ?",
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_all_scores(db_path=None):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT player_name, attempts, min_number, max_number, created_at "
        "FROM scores ORDER BY attempts ASC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def clear_scores(db_path=None):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scores")
    conn.commit()
    conn.close()


def get_player_best(player_name, db_path=None):
    if not player_name or not str(player_name).strip():
        raise ValueError("Имя игрока не может быть пустым")
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT player_name, attempts, min_number, max_number, created_at "
        "FROM scores WHERE player_name = ? ORDER BY attempts ASC LIMIT 1",
        (str(player_name).strip(),),
    )
    row = cursor.fetchone()
    conn.close()
    return row
