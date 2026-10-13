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
            s.attendance
        FROM students s
        JOIN departments d
        ON s.department_id = d.department_id
        WHERE s.marks >= 75
        AND s.attendance >= 75
        ORDER BY s.marks DESC;
     """)
 
    students = cursor.fetchall()

    if students:

        print("\n========== SCHOLARSHIP ELIGIBLE STUDENTS ==========\n")

        for student in students:
            print(f"ID         : {student[0]}")
            print(f"Name       : {student[1]}")
            print(f"Department : {student[2]}")
            print(f"Marks      : {student[3]}")
            print(f"Attendance : {student[4]}%")
            print("-" * 45)

    else:
        print("No students are eligible for scholarship.")

except Exception as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
