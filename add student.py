from database import get_connection

conn = None
cursor = None

try:
    # Connect to database
    conn = get_connection()
    cursor = conn.cursor()

    # Display available departments
    cursor.execute("""
        SELECT department_id, department_name
        FROM departments
        ORDER BY department_id;
    """)

    departments = cursor.fetchall()

    print("\n========== AVAILABLE DEPARTMENTS ==========\n")

    for dept in departments:
        print(f"{dept[0]}. {dept[1]}")

    print()

    # Take input
    name = input("Enter Student Name: ").strip()

    while not name:
        print("Name cannot be empty.")
        name = input("Enter Student Name: ").strip()

    age = int(input("Enter Age: "))
    while age < 18 or age > 30:
        print("Age must be between 18 and 30.")
        age = int(input("Enter Age: "))

    gender = input("Enter Gender (Male/Female/Other): ").strip().title()

    while gender not in ["Male", "Female", "Other"]:
        print("Invalid Gender!")
        gender = input("Enter Gender (Male/Female/Other): ").strip().title()

    phone = input("Enter Phone Number: ").strip()

    while len(phone) != 10 or not phone.isdigit():
        print("Phone number must contain exactly 10 digits.")
        phone = input("Enter Phone Number: ").strip()

    email = input("Enter Email: ").strip().lower()

    while "@" not in email or "." not in email.split("@")[-1]:
        print("Please enter a valid email address.")
        email = input("Enter Email: ").strip().lower()

    department_id = int(input("Enter Department ID: "))

    city = input("Enter City: ").strip()

    # Check department exists
    cursor.execute(
        "SELECT * FROM departments WHERE department_id=%s",
        (department_id,)
    )

    department = cursor.fetchone()

    if department is None:
        print("Department ID not found!")

    else:

        cursor.execute("""
            INSERT INTO students
            (student_name, age, gender, phone, email, department_id, city)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            RETURNING student_id
        """,
        (
            name,
            age,
            gender,
            phone,
            email,
            department_id,
            city
        ))

        new_id = cursor.fetchone()[0]

        conn.commit()

        print("\nStudent Added Successfully!")
        print("Generated Student ID :", new_id)

except ValueError:
    print("\nError : please enter a valid number.")

except Exception as e:
    print("\nError :", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
