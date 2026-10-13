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
            s.phone,
            s.email,
            d.department_name,
            s.city
        FROM students s
        JOIN departments d
        ON s.department_id = d.department_id
        WHERE s.student_id = %s
    """, (student_id,))

    student = cursor.fetchone()

    if student:

        print("\nStudent Found\n")

        print("ID         :", student[0])
        print("Name       :", student[1])
        print("Age        :", student[2])
        print("Gender     :", student[3])
        print("Phone      :", student[4])
        print("Email      :", student[5])
        print("Department :", student[6])
        print("City       :", student[7])

    else:
        print("Student Not Found")

except ValueError:
    print("Error: Student ID must be a number.")

except Exception as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
