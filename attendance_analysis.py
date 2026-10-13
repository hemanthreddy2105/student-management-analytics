from database import get_connection

conn = None
cursor = None

try:
    conn = get_connection()
    cursor = conn.cursor()

    # Attendance Statistics
    cursor.execute("""
        SELECT
            ROUND(AVG(attendance),2),
            MAX(attendance),
            MIN(attendance)
        FROM students;
    """)

    stats = cursor.fetchone()

    print("\n========== ATTENDANCE ANALYSIS ==========\n")

    print(f"Average Attendance : {stats[0]}%")
    print(f"Highest Attendance : {stats[1]}%")
    print(f"Lowest Attendance  : {stats[2]}%")  

except Exception as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
