from database import get_connection

conn = None
cursor = None

try:
    conn = get_connection()
    cursor = conn.cursor()

    # Read-only check, so running it repeatedly never adds duplicate rows.
    cursor.execute("SELECT COUNT(*) FROM departments;")
    count = cursor.fetchone()[0]

    print("Database Connection Successful!")
    print(f"Departments in database : {count}")

except Exception as e:
    print("Connection Failed:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
