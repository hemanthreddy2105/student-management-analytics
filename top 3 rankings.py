from database import get_connection

conn = None
cursor = None

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            RANK() OVER (ORDER BY s.marks DESC) AS rank,
            s.student_id,
            s.student_name,
            d.department_name,
            s.marks
        FROM students s
        JOIN departments d
        ON s.department_id = d.department_id
        ORDER BY s.marks DESC, s.student_id
        LIMIT 3;
    """)

    students = cursor.fetchall()

    if students:

        print("\n========== TOP 3 STUDENTS ==========\n")

        for student in students:

            print(f"Rank        : {student[0]}")
            print(f"Student ID  : {student[1]}")
            print(f"Name        : {student[2]}")
            print(f"Department  : {student[3]}")
            print(f"Marks       : {student[4]}")
            print("-" * 40)

    else:
        print("No student records found.")

except Exception as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
