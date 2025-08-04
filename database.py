"""
Database models for the credit scoring API.
"""
import sqlite3
import logging
from pathlib import Path

DB_PATH = Path(__file__).with_name("credit.db")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_connection(db_file: str) -> sqlite3.Connection:
    """Create a connection to the SQLite database specified by db_file."""
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row        # query rows behave like dicts
        logging.debug(f"Connected to database: {db_file}")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        raise

# Create tables if they do not exist
def create_tables(conn: sqlite3.Connection):
    """Create tables in the SQLite database."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applicants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                income REAL NOT NULL,
                age INTEGER NOT NULL,
                existing_loans INTEGER NOT NULL
            )
        """)
        conn.commit()
        logging.info("Tables created successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error creating tables: {e}")
        raise

# Insert a new applicant into the database
def insert_applicant(conn: sqlite3.Connection, name: str, income: float, age: int, existing_loans: int) -> int:
    """Insert a new applicant into the database and return the applicant ID."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO applicants (name, income, age, existing_loans)
            VALUES (?, ?, ?, ?)
        """, (name, income, age, existing_loans))
        conn.commit()
        applicant_id = cursor.lastrowid
        logging.info(f"Inserted applicant with ID: {applicant_id}")
        return applicant_id
    except sqlite3.Error as e:
        logging.error(f"Error inserting applicant: {e}")
        raise

# Retrieve an applicant by ID
def get_applicant(conn: sqlite3.Connection, applicant_id: int) -> sqlite3.Row:
    """Retrieve an applicant by ID."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applicants WHERE id = ?", (applicant_id,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        logging.error(f"Error retrieving applicant: {e}")
        raise

