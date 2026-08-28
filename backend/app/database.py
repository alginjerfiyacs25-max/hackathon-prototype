from copy import deepcopy
import json
import sqlite3
from pathlib import Path
from .seed_data import VILLAGES, SHELTERS, ROADS
from .models import Village, Shelter, Road

villages = deepcopy(VILLAGES)
shelters = deepcopy(SHELTERS)
roads = deepcopy(ROADS)
DB_PATH = Path(__file__).resolve().parent.parent / 'aquasentinel.db'

def init_db() -> None:
    """Persist the simulated seed snapshot in SQLite for the prototype."""
    with sqlite3.connect(DB_PATH) as connection:
        connection.executescript('''
            CREATE TABLE IF NOT EXISTS villages (id TEXT PRIMARY KEY, name TEXT NOT NULL, payload TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS shelters (id TEXT PRIMARY KEY, name TEXT NOT NULL, payload TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS roads (id TEXT PRIMARY KEY, start_node TEXT NOT NULL, end_node TEXT NOT NULL, payload TEXT NOT NULL);
        ''')
        for table, records, key in [('villages', VILLAGES, 'id'), ('shelters', SHELTERS, 'id'), ('roads', ROADS, 'id')]:
            for record in records:
                payload = json.dumps(record.model_dump())
                columns = 'id, name, payload' if table != 'roads' else 'id, start_node, end_node, payload'
                values = (record.id, getattr(record, 'name', None), payload) if table != 'roads' else (record.id, record.start_node, record.end_node, payload)
                placeholders = '?, ?, ?' if table != 'roads' else '?, ?, ?, ?'
                connection.execute(f'INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})', values)

init_db()

def reset_data():
    global villages, shelters, roads
    villages, shelters, roads = deepcopy(VILLAGES), deepcopy(SHELTERS), deepcopy(ROADS)
