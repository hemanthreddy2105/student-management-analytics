from database import get_connection

conn = None
cursor = None

try:

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM student_report

    ORDER BY student_id;

    """)

    students = cursor.fetchall()

    print("\n========== STUDENT REPORT ==========\n")

    for student in students:

        print("Student ID :",student[0])
        print("Name :",student[1])
        print("Age :",student[2])
        print("Gender :",student[3])
        print("Phone :",student[4])
        print("Email :",student[5])
        print("Department :",student[6])
        print("City :",student[7])
        print("Marks :",student[8])
        print("Attendance :",student[9])
        print("Fee Status :",student[10])

        print("-"*45)

except Exception as e:

    print(e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
