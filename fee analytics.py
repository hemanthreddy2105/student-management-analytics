from database import get_connection

conn = None
cursor = None

try:
    conn = get_connection()
    cursor = conn.cursor()

    # Total Students
    cursor.execute("SELECT COUNT(*) FROM students;")
    total_students = cursor.fetchone()[0]

    # Fee Analytics
    cursor.execute("""
        SELECT
            fee_status,
            COUNT(*) AS total
        FROM students
        GROUP BY fee_status
        ORDER BY fee_status;
    """)

    results = cursor.fetchall()

    print("\n========== FEE ANALYTICS ==========\n")

    for row in results:

        percentage = (row[1] / total_students) * 100

        print(f"Fee Status : {row[0]}")
        print(f"Students   : {row[1]}")
        print(f"Percentage : {percentage:.2f}%")
        print("-" * 35)

except Exception as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
