"""
PulseMind - Database Connection Manager
==========================================

Phase 1 scope: establish a working SQLite connection and initialization
routine only. No tables, models, or CRUD operations are created here --
that belongs to later phases (see PRD Module 3, 8, 9). Keeping the
connection layer in place now means future phases can start writing
schema/migrations without touching application wiring.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from config import DATABASE_DIR, DATABASE_FILE


class DatabaseManager:
    """Owns the single SQLite connection used by the application.

    This is intentionally minimal in Phase 1: it guarantees the database
    file and its parent directory exist, opens a connection with sane
    pragmas, and exposes it for future service layers to consume.
    """

    def __init__(self, database_path: Path = DATABASE_FILE) -> None:
        self._database_path = database_path
        self._connection: Optional[sqlite3.Connection] = None

    @property
    def path(self) -> Path:
        return self._database_path

    @property
    def connection(self) -> sqlite3.Connection:
        if self._connection is None:
            raise RuntimeError(
                "Database connection has not been initialized. "
                "Call DatabaseManager.connect() first."
            )
        return self._connection

    def connect(self) -> sqlite3.Connection:
        """Open (or reuse) the SQLite connection and apply base pragmas."""
        DATABASE_DIR.mkdir(parents=True, exist_ok=True)

        if self._connection is not None:
            return self._connection

        connection = sqlite3.connect(str(self._database_path))
        connection.row_factory = sqlite3.Row

        # Sensible defaults for a desktop, single-user SQLite database.
        connection.execute("PRAGMA foreign_keys = ON;")
        connection.execute("PRAGMA journal_mode = WAL;")

        self._connection = connection
        return connection

    def initialize(self) -> None:
        """Ensure the database file exists and is reachable.

        Phase 1 deliberately creates no tables. Schema creation for
        Users, Patients, and Reports (see PRD section 11) is reserved
        for Phase 2 onward.
        """
        self.connect()

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None


# Module-level singleton so any part of the app can share one connection
# without threading a reference through every constructor.
database_manager = DatabaseManager()
