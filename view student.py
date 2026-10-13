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
            age,
            gender,
            phone,
            email,
            department_name,
            city
        FROM students 
        JOIN departments 
        ON students.department_id = departments.department_id
        ORDER BY students.student_id
                   LIMIT 10;
    """)

    students = cursor.fetchall()

    print("\n================ STUDENT LIST ================\n")

    for student in students:

        print(f"ID          : {student[0]}")
        print(f"Name        : {student[1]}")
        print(f"Age         : {student[2]}")
        print(f"Gender      : {student[3]}")
        print(f"Phone       : {student[4]}")
        print(f"Email       : {student[5]}")
        print(f"Department  : {student[6]}")
        print(f"City        : {student[7]}")
        print("-"*45)

except Exception as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
