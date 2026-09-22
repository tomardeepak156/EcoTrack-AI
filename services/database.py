import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "ecotrack.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS footprint_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            transport REAL DEFAULT 0,
            electricity REAL DEFAULT 0,
            food REAL DEFAULT 0,
            flight REAL DEFAULT 0,
            shopping REAL DEFAULT 0,
            waste REAL DEFAULT 0,
            total REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_type TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            co2 REAL NOT NULL,
            logged_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_activity(activity_type, quantity, unit, co2):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO activities
        (activity_type, quantity, unit, co2, logged_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        activity_type,
        quantity,
        unit,
        co2,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def get_activities(activity_type=None, start_date=None, end_date=None):
    connection = get_connection()

    query = """
        SELECT id, activity_type, quantity, unit, co2, logged_at
        FROM activities
        WHERE 1=1
    """
    params = []

    if activity_type and activity_type != "All":
        query += " AND activity_type = ?"
        params.append(activity_type)

    if start_date:
        query += " AND date(logged_at) >= date(?)"
        params.append(str(start_date))

    if end_date:
        query += " AND date(logged_at) <= date(?)"
        params.append(str(end_date))

    query += " ORDER BY logged_at DESC"

    cursor = connection.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()

    connection.close()
    return rows


def get_weekly_co2(week_start=None):
    if week_start is None:
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())

    week_end = week_start + timedelta(days=6)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(co2), 0)
        FROM activities
        WHERE date(logged_at) BETWEEN date(?) AND date(?)
    """, (str(week_start), str(week_end)))

    total = cursor.fetchone()[0]
    connection.close()

    return float(total), week_start, week_end


def set_weekly_target(target):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO settings(key, value)
        VALUES('weekly_target', ?)
        ON CONFLICT(key)
        DO UPDATE SET value = excluded.value
    """, (str(target),))

    connection.commit()
    connection.close()


def get_weekly_target(default=50.0):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT value
        FROM settings
        WHERE key = 'weekly_target'
    """)

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return default

    try:
        return float(row[0])
    except (TypeError, ValueError):
        return default


def save_footprint(
    transport,
    electricity,
    food,
    flight,
    shopping,
    waste,
    total
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO footprint_history
        (
            date,
            transport,
            electricity,
            food,
            flight,
            shopping,
            waste,
            total
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        transport,
        electricity,
        food,
        flight,
        shopping,
        waste,
        total
    ))

    connection.commit()
    connection.close()


def get_history():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            date,
            transport,
            electricity,
            food,
            flight,
            shopping,
            waste,
            total
        FROM footprint_history
        ORDER BY date DESC
    """)

    rows = cursor.fetchall()
    connection.close()
    return rows
