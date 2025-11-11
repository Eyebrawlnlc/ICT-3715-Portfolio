import sqlite3

conn = sqlite3.connect("amandla_locker_system.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

with open("sqlite_dump.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()
cursor.executescript(sql_script)

conn.commit()
conn.close()
