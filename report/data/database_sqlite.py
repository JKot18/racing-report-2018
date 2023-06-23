import sqlite3
import os
from report.src.core.main import build_report
from typing import NoReturn
from pathlib import Path

default_folder = Path(__file__).resolve().parent.parent.parent / 'report' / 'data'
report = build_report(default_folder, 'asc')[0]


def create_time() -> NoReturn:
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS time (key TEXT, time_start INTEGER, time_end INTEGER, time_diff INTEGER, "
            "valid TEXT);")
        db.commit()
        query = "SELECT * FROM time WHERE key = ?"
        for key, info in report.items():
            time_start = info['time_start']
            time_end = info['time_end']
            time_diff = info['time_diff'].total_seconds() * 1000
            valid = info['valid']
            cursor.execute(query, (key,))
            key_exists = cursor.fetchone()
            if key_exists:
                pass
            else:
                insert_query = "INSERT INTO time (key, time_start, time_end, time_diff, valid) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(insert_query, (key, time_start, time_end, time_diff, valid))
                db.commit()


def create_racers() -> NoReturn:
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS racers (key TEXT, name TEXT, team TEXT);")
        db.commit()
        query = "SELECT * FROM racers WHERE key = ?"
        for key, info in report.items():
            name = info['name']
            team = info['team']
            cursor.execute(query, (key,))
            key_exists = cursor.fetchone()
            if key_exists:
                pass
            else:
                insert_query = "INSERT INTO racers (key, name, team) VALUES (?, ?, ?)"
                cursor.execute(insert_query, (key, name, team))
                db.commit()


def get_report(order: str = 'asc') -> list[tuple]:
    database_path = os.path.join(default_folder, 'database.db')
    with sqlite3.connect(database_path) as db:
        cursor = db.cursor()
        query = """
        SELECT time.key, time.time_diff, racers.name, racers.team 
        from time 
        JOIN racers ON time.key = racers.key
        WHERE valid = 'Time entry is valid'
        ORDER BY time.time_diff {};
        """.format('DESC' if order == 'desc' else 'ASC')
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_list() -> list[tuple]:
    database_path = os.path.join(default_folder, 'database.db')
    with sqlite3.connect(database_path) as db:
        cursor = db.cursor()
        query = """
        SELECT time.key, racers.name
        from time 
        JOIN racers ON time.key = racers.key;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_racer(key: str) -> list[tuple]:
    database_path = os.path.join(default_folder, 'database.db')
    with sqlite3.connect(database_path) as db:
        cursor = db.cursor()
        query = """
        SELECT time.key, racers.name, racers.team, time.time_start, time.time_end, time.time_diff, time.valid 
        from time 
        JOIN racers ON time.key = racers.key
        WHERE time.key = ?;
        """
        cursor.execute(query, (key,))
        result = cursor.fetchall()
        return result
