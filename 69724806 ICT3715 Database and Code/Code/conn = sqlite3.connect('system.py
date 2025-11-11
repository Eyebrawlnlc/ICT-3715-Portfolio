import sqlite3


conn = sqlite3.connect('system.db')
with open("amandla_locker_system_sqlite.sql", "r", encoding="utf-8") as f:
    conn.executescript(f.read())