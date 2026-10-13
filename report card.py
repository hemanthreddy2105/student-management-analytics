from database import get_connection

conn = None
cursor = None

try:
    student_id = int(input("Enter Student ID: "))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.student_id,
            s.student_name,
            s.age,
            s.gender,
            d.department_name,
            s.city,
            s.marks,
            s.attendance,
            s.fee_status
        FROM students s
        JOIN departments d
        ON s.department_id = d.department_id
        WHERE s.student_id = %s;
    """, (student_id,))

    student = cursor.fetchone()

    if student:

        marks = float(student[6]) if student[6] is not None else 0.0

        if marks >= 90:
            grade = "A+"
        elif marks >= 80:
            grade = "A"
        elif marks >= 70:
            grade = "B"
        elif marks >= 60:
            grade = "C"
        elif marks >= 50:
            grade = "D"
        else:
            grade = "F"

        print("\n========== REPORT CARD ==========\n")

        print(f"Student ID     : {student[0]}")
        print(f"Name           : {student[1]}")
        print(f"Age            : {student[2]}")
        print(f"Gender         : {student[3]}")
        print(f"Department     : {student[4]}")
        print(f"City           : {student[5]}")
        print(f"Marks          : {student[6]}")
        print(f"Attendance     : {student[7]}%")
        print(f"Fee Status     : {student[8]}")
        print(f"Grade          : {grade}")

    else:
        print("Student not found.")

except ValueError:
    print("Error: Student ID must be a number.")

except Exception as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
