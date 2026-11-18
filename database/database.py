import hashlib
import hmac
import secrets
import sqlite3
from pathlib import Path
from datetime import datetime

from config import DATABASE_DIR, DATABASE_FILE


class DatabaseManager:
    def __init__(self, database_path: Path = DATABASE_FILE):
        self._database_path = database_path
        self._connection = None

    @property
    def path(self):
        return self._database_path

    @property
    def connection(self):
        if self._connection is None:
            self.connect()
        return self._connection

    def connect(self):
        DATABASE_DIR.mkdir(parents=True, exist_ok=True)

        if self._connection is None:
            self._connection = sqlite3.connect(
                str(self._database_path)
            )

            self._connection.row_factory = sqlite3.Row

            self._connection.execute(
                "PRAGMA foreign_keys = ON"
            )

            self._create_tables()

        return self._connection

    def initialize(self):
        self.connect()

    # =============================================================
    # Tables
    # =============================================================

    def _create_tables(self):
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS ecg_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                file_name TEXT NOT NULL,
                sample_rate REAL NOT NULL,
                duration REAL NOT NULL,
                beat_count INTEGER NOT NULL,
                heart_rate REAL,
                average_rr REAL,
                pr_ms REAL,
                qrs_ms REAL,
                qt_ms REAL,
                qtc_ms REAL,
                status TEXT NOT NULL,
                findings TEXT,
                created_at TEXT NOT NULL,

                FOREIGN KEY(patient_id)
                    REFERENCES patients(id)
            );

            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )

        self.connection.commit()

    # =============================================================
    # Authentication
    # =============================================================

    def _hash_password(
        self,
        password,
        salt=None,
    ):
        if salt is None:
            salt = secrets.token_bytes(32)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            200_000,
        )

        return (
            password_hash.hex(),
            salt.hex(),
        )

    def register_user(
        self,
        username,
        password,
    ):
        username = username.strip()

        if not username:
            return False, "Username cannot be empty."

        if not password:
            return False, "Password cannot be empty."

        if len(username) < 3:
            return (
                False,
                "Username must contain at least 3 characters.",
            )

        if len(password) < 6:
            return (
                False,
                "Password must contain at least 6 characters.",
            )

        exists = self.connection.execute(
            """
            SELECT id
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

        if exists:
            return (
                False,
                "This username is already registered.",
            )

        password_hash, salt = (
            self._hash_password(password)
        )

        self.connection.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                salt,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                username,
                password_hash,
                salt,
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            ),
        )

        self.connection.commit()

        return True, "Account created successfully."

    def authenticate_user(
        self,
        username,
        password,
    ):
        username = username.strip()

        if not username or not password:
            return None

        user = self.connection.execute(
            """
            SELECT
                id,
                username,
                password_hash,
                salt,
                created_at
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

        if user is None:
            return None

        try:
            salt = bytes.fromhex(
                user["salt"]
            )

            password_hash, _ = (
                self._hash_password(
                    password,
                    salt,
                )
            )

            if hmac.compare_digest(
                password_hash,
                user["password_hash"],
            ):
                return user

        except (
            ValueError,
            TypeError,
        ):
            return None

        return None

    def user_count(self):
        row = self.connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM users
            """
        ).fetchone()

        return row["count"]

    # =============================================================
    # Patients
    # =============================================================

    def add_patient(
        self,
        name,
        age,
        gender,
    ):
        name = str(name).strip()
        gender = str(gender).strip()

        if not name:
            raise ValueError(
                "Patient name is required."
            )

        try:
            age = int(age)

        except (
            TypeError,
            ValueError,
        ):
            raise ValueError(
                "Age must be a number."
            )

        if age < 0 or age > 130:
            raise ValueError(
                "Please enter a valid age."
            )

        if not gender:
            raise ValueError(
                "Gender is required."
            )

        # Generate patient ID internally.
        patient_code = (
            f"PAT-{secrets.token_hex(4).upper()}"
        )

        cursor = self.connection.execute(
            """
            INSERT INTO patients (
                patient_id,
                name,
                age,
                gender,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                patient_code,
                name,
                age,
                gender,
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            ),
        )

        self.connection.commit()

        return self.get_patient(
            cursor.lastrowid
        )

    def get_patients(self):
        return self.connection.execute(
            """
            SELECT
                id,
                patient_id,
                name,
                age,
                gender,
                created_at
            FROM patients
            ORDER BY id DESC
            """
        ).fetchall()

    def get_patient(
        self,
        patient_db_id,
    ):
        return self.connection.execute(
            """
            SELECT
                id,
                patient_id,
                name,
                age,
                gender,
                created_at
            FROM patients
            WHERE id = ?
            """,
            (patient_db_id,),
        ).fetchone()

    def get_patient_by_code(
        self,
        patient_code,
    ):
        return self.connection.execute(
            """
            SELECT
                id,
                patient_id,
                name,
                age,
                gender,
                created_at
            FROM patients
            WHERE patient_id = ?
            """,
            (patient_code,),
        ).fetchone()

    # =============================================================
    # ECG Analysis
    # =============================================================

    def save_result(
        self,
        result,
        patient_name="Unknown",
        patient_code="",
    ):
        patient_db_id = None

        if patient_code:
            row = self.connection.execute(
                """
                SELECT id
                FROM patients
                WHERE patient_id = ?
                """,
                (patient_code,),
            ).fetchone()

            if row:
                patient_db_id = row["id"]

        # Compatibility with manually entered patient data.
        if (
            patient_db_id is None
            and patient_code
        ):
            row = self.connection.execute(
                """
                SELECT id
                FROM patients
                WHERE name = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (patient_name,),
            ).fetchone()

            if row:
                patient_db_id = row["id"]

        self.connection.execute(
            """
            INSERT INTO ecg_records (
                patient_id,
                file_name,
                sample_rate,
                duration,
                beat_count,
                heart_rate,
                average_rr,
                pr_ms,
                qrs_ms,
                qt_ms,
                qtc_ms,
                status,
                findings,
                created_at
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?
            )
            """,
            (
                patient_db_id,
                result["file_name"],
                result["sample_rate"],
                result["duration"],
                result["beat_count"],
                result.get("heart_rate"),
                result.get("average_rr"),
                result.get("pr_ms"),
                result.get("qrs_ms"),
                result.get("qt_ms"),
                result.get("qtc_ms"),
                result.get(
                    "status",
                    "UNKNOWN",
                ),
                "\n".join(
                    result.get(
                        "findings",
                        [],
                    )
                ),
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            ),
        )

        self.connection.commit()

        return self.connection.execute(
            "SELECT last_insert_rowid()"
        ).fetchone()[0]

    # =============================================================
    # History
    # =============================================================

    def get_history(self):
        return self.connection.execute(
            """
            SELECT
                r.id,
                COALESCE(
                    p.name,
                    'Unknown'
                ) AS patient,
                COALESCE(
                    p.age,
                    ''
                ) AS age,
                COALESCE(
                    p.gender,
                    ''
                ) AS gender,
                r.created_at,
                r.heart_rate,
                r.file_name,
                r.status

            FROM ecg_records r

            LEFT JOIN patients p
                ON p.id = r.patient_id

            ORDER BY r.id DESC
            """
        ).fetchall()

    # =============================================================
    # Reports
    # =============================================================

    def get_report_history(self):
        return self.connection.execute(
            """
            SELECT
                r.id,

                COALESCE(
                    p.name,
                    'Unknown'
                ) AS patient,

                COALESCE(
                    p.patient_id,
                    ''
                ) AS patient_id,

                COALESCE(
                    p.age,
                    ''
                ) AS age,

                COALESCE(
                    p.gender,
                    ''
                ) AS gender,

                r.file_name,
                r.sample_rate,
                r.duration,
                r.beat_count,
                r.heart_rate,
                r.average_rr,
                r.pr_ms,
                r.qrs_ms,
                r.qt_ms,
                r.qtc_ms,
                r.status,
                r.findings,
                r.created_at

            FROM ecg_records r

            LEFT JOIN patients p
                ON p.id = r.patient_id

            ORDER BY r.id DESC
            """
        ).fetchall()

    def get_report(
        self,
        report_id,
    ):
        return self.connection.execute(
            """
            SELECT
                r.id,

                COALESCE(
                    p.name,
                    'Unknown'
                ) AS patient,

                COALESCE(
                    p.patient_id,
                    ''
                ) AS patient_id,

                COALESCE(
                    p.age,
                    ''
                ) AS age,

                COALESCE(
                    p.gender,
                    ''
                ) AS gender,

                r.file_name,
                r.sample_rate,
                r.duration,
                r.beat_count,
                r.heart_rate,
                r.average_rr,
                r.pr_ms,
                r.qrs_ms,
                r.qt_ms,
                r.qtc_ms,
                r.status,
                r.findings,
                r.created_at

            FROM ecg_records r

            LEFT JOIN patients p
                ON p.id = r.patient_id

            WHERE r.id = ?
            """,
            (report_id,),
        ).fetchone()

    # =============================================================
    # Close
    # =============================================================

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None


database_manager = DatabaseManager()