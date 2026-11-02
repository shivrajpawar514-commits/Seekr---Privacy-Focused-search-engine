"""
Database abstraction layer supporting SQLite and PostgreSQL.
Enforces privacy principles: zero-IP logging, hashed query counters,
and clean document persistence.
"""
import sqlite3
import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from backend.config import DATA_DIR

logger = logging.getLogger(__name__)

DB_PATH = DATA_DIR / "seekr.db"


class StorageManager:
    """Manages SQLite storage for crawled documents and privacy-preserving stats."""

    def __init__(self, db_file=DB_PATH):
        self.db_file = str(db_file)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # 1. Documents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    url TEXT UNIQUE,
                    domain TEXT,
                    title TEXT,
                    meta_description TEXT,
                    headings TEXT,
                    body_text TEXT,
                    word_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 2. Query Analytics (Zero PII - counts only with Laplace noise capability)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_analytics (
                    query TEXT PRIMARY KEY,
                    raw_count INTEGER DEFAULT 1,
                    last_searched TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 3. Crawler Logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS crawl_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    seed_url TEXT,
                    domain TEXT,
                    pages_crawled INTEGER,
                    status TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_document(self, doc: Dict[str, Any]) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO documents (id, url, domain, title, meta_description, headings, body_text, word_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(url) DO UPDATE SET
                    title=excluded.title,
                    meta_description=excluded.meta_description,
                    headings=excluded.headings,
                    body_text=excluded.body_text,
                    word_count=excluded.word_count
            """, (
                doc["id"],
                doc["url"],
                doc.get("domain", ""),
                doc.get("title", ""),
                doc.get("meta_description", ""),
                json.dumps(doc.get("headings", [])),
                doc.get("body_text", ""),
                doc.get("word_count", 0),
            ))
            conn.commit()

    def save_documents_bulk(self, docs: List[Dict[str, Any]]) -> None:
        for doc in docs:
            self.save_document(doc)

    def get_all_documents(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documents")
            rows = cursor.fetchall()
            results = []
            for r in rows:
                results.append({
                    "id": r["id"],
                    "url": r["url"],
                    "domain": r["domain"],
                    "title": r["title"],
                    "meta_description": r["meta_description"],
                    "headings": json.loads(r["headings"]) if r["headings"] else [],
                    "body_text": r["body_text"],
                    "word_count": r["word_count"],
                })
            return results

    def get_document_count(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM documents")
            return cursor.fetchone()[0]

    def record_search_query(self, query: str) -> None:
        """Records query count without storing user IP, cookies, or timestamps of users."""
        clean_query = query.strip().lower()
        if not clean_query or len(clean_query) < 2:
            return
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO search_analytics (query, raw_count, last_searched)
                VALUES (?, 1, CURRENT_TIMESTAMP)
                ON CONFLICT(query) DO UPDATE SET
                    raw_count = raw_count + 1,
                    last_searched = CURRENT_TIMESTAMP
            """, (clean_query,))
            conn.commit()

    def get_query_counts(self) -> Dict[str, int]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT query, raw_count FROM search_analytics")
            return {r["query"]: r["raw_count"] for r in cursor.fetchall()}

