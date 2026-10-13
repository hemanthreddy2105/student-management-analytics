from database import get_connection

name = input("Enter Student Name: ").strip()

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
            s.marks
        FROM students s
        JOIN departments d
        ON s.department_id = d.department_id
        WHERE s.student_name ILIKE %s
        ORDER BY s.student_name;
    """, (f"%{name}%",))

    students = cursor.fetchall()

    if students:

        print("\n========== SEARCH RESULTS ==========\n")

        for student in students:

            print("Student ID :", student[0])
            print("Name       :", student[1])
            print("Department :", student[2])
            print("Marks      :", student[3])
            print("-" * 35)

    else:
        print("No student found.")

except Exception as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
