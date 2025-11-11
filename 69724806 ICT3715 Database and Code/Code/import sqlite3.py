try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    print("MySQL Connector not found. Please install it using:")
    print("pip install mysql-connector-python")
    exit(1)

try:
    # connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # change this to your MySQL username
        password="Bat2-3man",        # change if you have a MySQL password
    )
    cursor = conn.cursor()

    # Create your database (if not already created)
    cursor.execute("CREATE DATABASE IF NOT EXISTS amandla_locker_system")
    cursor.execute("USE amandla_locker_system")

    # Read and execute your SQL file
    with open(r"C:\Users\nisha\Desktop\ICT3715 Database and Code\Database\amandla_locker_system.sql", "r") as f:
        sql_script = f.read()

    for statement in sql_script.split(";"):
        if statement.strip():
            try:
                cursor.execute(statement)
            except Error as e:
                print(f"⚠️ Skipped statement due to error: {e}")

    conn.commit()

except Error as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("✅ Database connection closed.")

print("✅ Database imported successfully into MySQL!")