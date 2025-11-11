import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",        # your MySQL username
    password="Bat2-3man"          # your MySQL password, if any
)
cursor = conn.cursor()

# Create database (if not already created)
cursor.execute("CREATE DATABASE IF NOT EXISTS amandla_locker_system")
cursor.execute("USE amandla_locker_system")

# Read the SQL file
with open(r"C:\Users\nisha\Desktop\New folder (2)\amandla_locker_system.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

# Execute each statement separately
for statement in sql_script.split(";"):
    statement = statement.strip()
    if statement:
        try:
            cursor.execute(statement)
        except mysql.connector.Error as e:
            print(f"⚠️ Skipped statement: {e}")

conn.commit()
conn.close()
print("✅ Database imported successfully into MySQL!")