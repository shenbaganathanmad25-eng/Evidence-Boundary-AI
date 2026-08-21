import sqlite3
import os
import logging
from config import settings

logger = logging.getLogger("evidence_boundary.database")

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "evidence_boundary.db")

def get_db_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create claims audit log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verification_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_claim TEXT NOT NULL,
            verdict TEXT NOT NULL,
            fragility_score REAL NOT NULL,
            is_demo INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    logger.info(f"SQLite database initialized at: {DB_PATH}")

def log_verification(raw_claim: str, verdict: str, fragility_score: float, is_demo: bool):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO verification_logs (raw_claim, verdict, fragility_score, is_demo) VALUES (?, ?, ?, ?)",
            (raw_claim, verdict, fragility_score, 1 if is_demo else 0)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to log verification to SQLite: {e}")
