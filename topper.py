from database import get_connection

conn = None
cursor = None

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.student_id,
            s.student_name,
            d.department_name,
            s.marks,
            s.attendance,
            s.fee_status
        FROM students s
        JOIN departments d
        ON s.department_id = d.department_id
        ORDER BY s.marks DESC
        LIMIT 1;
    """)

    topper = cursor.fetchone()

    if topper:

        print("\n========== CLASS TOPPER ==========\n")

        print("Student ID   :", topper[0])
        print("Name         :", topper[1])
        print("Department   :", topper[2])
        print("Marks        :", topper[3])
        print("Attendance   :", topper[4])
        print("Fee Status   :", topper[5])

    else:
        print("No student records found.")

except Exception as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
