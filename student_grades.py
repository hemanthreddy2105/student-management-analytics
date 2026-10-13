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
        marks,
        get_grade(marks)

        FROM students

        ORDER BY student_id;

    """)

    students = cursor.fetchall()

    print("\n========== STUDENT GRADES ==========\n")

    for student in students:

        print("Student ID :", student[0])
        print("Name       :", student[1])
        print("Marks      :", student[2])
        print("Grade      :", student[3])
        print("-" * 40)

except Exception as e:

    print("Error :", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
