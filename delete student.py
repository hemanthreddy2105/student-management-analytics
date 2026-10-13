from database import get_connection

conn = None
cursor = None

try:
    student_id = int(input("Enter Student ID : "))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE student_id = %s",
        (student_id,)
    )

    if cursor.rowcount == 0:
        print("Student not found.")
    else:
        conn.commit()
        print("Student Deleted Successfully")

except ValueError:
    print("Error: Student ID must be a number.")

except Exception as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
