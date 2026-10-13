from database import get_connection

conn = None
cursor = None

try:
    student_id = int(input("Enter Student ID : "))
    new_marks = float(input("Enter New Marks (0-100) : "))

    while new_marks < 0 or new_marks > 100:
        print("Marks must be between 0 and 100.")
        new_marks = float(input("Enter New Marks (0-100) : "))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE students SET marks = %s WHERE student_id = %s",
        (new_marks, student_id)
    )

    if cursor.rowcount == 0:
        print("Student not found.")
    else:
        conn.commit()
        print("Marks Updated Successfully")

except ValueError:
    print("Error: please enter valid numbers.")

except Exception as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
