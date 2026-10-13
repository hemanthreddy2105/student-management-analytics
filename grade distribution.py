from database import get_connection

conn = None
cursor = None

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            CASE
                WHEN marks >= 90 THEN 'A+'
                WHEN marks >= 80 THEN 'A'
                WHEN marks >= 70 THEN 'B'
                WHEN marks >= 60 THEN 'C'
                WHEN marks >= 50 THEN 'D'
                ELSE 'F'
            END AS grade,
            COUNT(*) AS total_students
        FROM students
        GROUP BY grade
        ORDER BY MIN(marks) DESC;
    """)

    grades = cursor.fetchall()

    print("\n========== GRADE DISTRIBUTION ==========\n")

    for grade in grades:
        grade_name = grade[0]
        student_count = grade[1]

        print("Grade :", grade_name)
        print("Students :", student_count)
        print("----------------------")

except Exception as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
