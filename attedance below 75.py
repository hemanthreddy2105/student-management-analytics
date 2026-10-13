from database import get_connection

conn = None
cursor = None

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            student_id,
            student_name,
            attendance
        FROM students
        WHERE attendance < 75
        ORDER BY attendance;
    """)

    students = cursor.fetchall()

    print("\n===== STUDENTS BELOW 75% ATTENDANCE =====\n")

    if students:

        for student in students:

            print(f"Student ID : {student[0]}")
            print(f"Name       : {student[1]}")
            print(f"Attendance : {student[2]}%")
            print("-" * 40)

        print(f"\nTotal Students Below 75% : {len(students)}")

    else:
        print("No students found below 75% attendance.")

except Exception as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
