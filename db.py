# db.py
import sqlite3
import os
from typing import List, Tuple

DB_PATH = os.path.join(os.path.dirname(__file__), "tags.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS file_tags (
        file_path TEXT PRIMARY KEY,
        tags TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_tags(file_path: str, tags: List[str]):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    tags_str = ",".join(tags)
    c.execute("INSERT OR REPLACE INTO file_tags (file_path, tags) VALUES (?, ?)", (file_path, tags_str))
    conn.commit()
    conn.close()

def get_tags(file_path: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT tags FROM file_tags WHERE file_path = ?", (file_path,))
    row = c.fetchone()
    conn.close()
    return row[0].split(",") if row else []

def search_by_tag(tag: str) -> List[Tuple[str, str]]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    like = f"%{tag}%"
    c.execute("SELECT file_path, tags FROM file_tags WHERE tags LIKE ?", (like,))
    rows = c.fetchall()
    conn.close()
    return rows
