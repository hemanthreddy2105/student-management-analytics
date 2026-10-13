from database import get_connection

conn = None
cursor = None

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_students,
            ROUND(AVG(marks),2) AS average_marks,
            MAX(marks) AS highest_marks,
            MIN(marks) AS lowest_marks,
            ROUND(AVG(attendance),2) AS average_attendance,
            COUNT(CASE WHEN fee_status='Paid' THEN 1 END) AS paid_students,
            COUNT(CASE WHEN fee_status='Pending' THEN 1 END) AS pending_students
        FROM students;
    """)

    stats = cursor.fetchone()

    print("\n========== CLASS STATISTICS ==========\n")

    print(f"Total Students : {stats[0]}")
    print(f"Average Marks  : {stats[1]}")
    print(f"Highest Marks  : {stats[2]}")
    print(f"Lowest Marks   : {stats[3]}")
    print(f"Average Attendance : {stats[4]}")
    print(f"Paid Students    : {stats[5]}")
    print(f"Pending Students : {stats[6]}")

except Exception as e:
    print("Error :", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
