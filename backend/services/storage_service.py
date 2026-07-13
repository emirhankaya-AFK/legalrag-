import sqlite3
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from ..config.settings import settings

class StorageService:
    def __init__(self):
        self.db_path = settings.DB_PATH
        # Ensure directories exist
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Enable Foreign Keys
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            # Documents Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                upload_date TEXT NOT NULL
            );
            """)

            # Clauses Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS clauses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                clause_type TEXT NOT NULL,
                content TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                page_num INTEGER,
                FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE
            );
            """)

            # Analyses Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                risk_score INTEGER NOT NULL,
                summary TEXT,
                risk_explanation TEXT, -- JSON string
                analysis_date TEXT NOT NULL,
                FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE
            );
            """)
            conn.commit()

    # --- Document Operations ---
    def save_file(self, file_content: bytes, filename: str) -> Path:
        target_path = settings.UPLOAD_DIR / filename
        # Resolve conflicts by appending timestamp if file exists
        if target_path.exists():
            stem = Path(filename).stem
            suffix = Path(filename).suffix
            filename = f"{stem}_{int(datetime.utcnow().timestamp())}{suffix}"
            target_path = settings.UPLOAD_DIR / filename

        with open(target_path, "wb") as f:
            f.write(file_content)
        return target_path

    def add_document(self, filename: str, file_path: str, file_size: int) -> Dict[str, Any]:
        upload_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO documents (filename, file_path, file_size, upload_date) VALUES (?, ?, ?, ?);",
                (filename, str(file_path), file_size, upload_date)
            )
            doc_id = cursor.lastrowid
            conn.commit()
            return {"id": doc_id, "filename": filename, "file_path": str(file_path), "file_size": file_size, "upload_date": upload_date}

    def get_document(self, doc_id: int) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documents WHERE id = ?;", (doc_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_documents(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documents ORDER BY upload_date DESC;")
            return [dict(row) for row in cursor.fetchall()]

    def delete_document(self, doc_id: int) -> bool:
        doc = self.get_document(doc_id)
        if not doc:
            return False
        
        # Delete file
        file_path = Path(doc["file_path"])
        if file_path.exists():
            file_path.unlink()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM documents WHERE id = ?;", (doc_id,))
            conn.commit()
            return True

    # --- Clause Operations ---
    def add_clause(self, document_id: int, clause_type: str, content: str, risk_level: str, page_num: Optional[int] = None) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO clauses (document_id, clause_type, content, risk_level, page_num) VALUES (?, ?, ?, ?, ?);",
                (document_id, clause_type, content, risk_level, page_num)
            )
            clause_id = cursor.lastrowid
            conn.commit()
            return clause_id

    def get_clauses(self, document_id: int) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clauses WHERE document_id = ?;", (document_id,))
            return [dict(row) for row in cursor.fetchall()]

    # --- Analysis Operations ---
    def add_analysis(self, document_id: int, risk_score: int, summary: str, risk_explanation: str) -> int:
        analysis_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Check if analysis already exists for this document, delete it
            cursor.execute("DELETE FROM analyses WHERE document_id = ?;", (document_id,))
            
            cursor.execute(
                "INSERT INTO analyses (document_id, risk_score, summary, risk_explanation, analysis_date) VALUES (?, ?, ?, ?, ?);",
                (document_id, risk_score, summary, risk_explanation, analysis_date)
            )
            analysis_id = cursor.lastrowid
            conn.commit()
            return analysis_id

    def get_analysis(self, document_id: int) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM analyses WHERE document_id = ?;", (document_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

storage_service = StorageService()
