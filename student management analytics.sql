-- Run this line first, then connect to student_management and run the rest.
CREATE DATABASE student_management;

CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100),
    hod VARCHAR(100)
);

CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(100),
    age INT,
    gender VARCHAR(10) CHECK (gender IN ('Male','Female','Other')),
    phone VARCHAR(15),
    email VARCHAR(100),
    department_id INT,
    city VARCHAR(50),
    marks NUMERIC(5,2) DEFAULT 0 CHECK (marks BETWEEN 0 AND 100),
    attendance NUMERIC(5,2) DEFAULT 0 CHECK (attendance BETWEEN 0 AND 100),
    fee_status VARCHAR(20) DEFAULT 'Pending' CHECK (fee_status IN ('Paid','Pending')),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE faculty (
    faculty_id SERIAL PRIMARY KEY,
    faculty_name VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100),
    credits INT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id INT,
    course_id INT,
    attendance_date DATE,
    status VARCHAR(20) CHECK (status IN ('Present','Absent')),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE marks (
    mark_id SERIAL PRIMARY KEY,
    student_id INT,
    course_id INT,
    exam_type VARCHAR(50),
    marks INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE fees (
    payment_id SERIAL PRIMARY KEY,
    student_id INT,
    total_fee DECIMAL(10,2),
    paid_fee DECIMAL(10,2),
    balance DECIMAL(10,2),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

--- Views

CREATE VIEW student_report AS

SELECT

s.student_id,
s.student_name,
s.age,
s.gender,
s.phone,
s.email,
d.department_name,
s.city,
s.marks,
s.attendance,
s.fee_status

FROM students s

JOIN departments d

ON s.department_id=d.department_id;

-- Functions

CREATE OR REPLACE FUNCTION get_grade(student_marks NUMERIC)

RETURNS VARCHAR

LANGUAGE plpgsql

AS $$

BEGIN

    IF student_marks >= 90 THEN
        RETURN 'A+';

    ELSIF student_marks >= 80 THEN
        RETURN 'A';

    ELSIF student_marks >= 70 THEN
        RETURN 'B';

    ELSIF student_marks >= 60 THEN
        RETURN 'C';

    ELSIF student_marks >= 50 THEN
        RETURN 'D';

    ELSE
        RETURN 'F';

    END IF;

END;

$$;

---- triggers for audit log

CREATE TABLE deleted_students (

    student_id INT,

    student_name VARCHAR(100),

    age INT,

    gender VARCHAR(10),

    phone VARCHAR(15),

    email VARCHAR(100),

    department_id INT,

    city VARCHAR(100),

    marks NUMERIC(5,2),

    attendance NUMERIC(5,2),

    fee_status VARCHAR(20),

    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

---- function for triggers

CREATE OR REPLACE FUNCTION save_deleted_student()

RETURNS TRIGGER

LANGUAGE plpgsql

AS $$

BEGIN

    INSERT INTO deleted_students(

        student_id,
        student_name,
        age,
        gender,
        phone,
        email,
        department_id,
        city,
        marks,
        attendance,
        fee_status

    )

    VALUES(

        OLD.student_id,
        OLD.student_name,
        OLD.age,
        OLD.gender,
        OLD.phone,
        OLD.email,
        OLD.department_id,
        OLD.city,
        OLD.marks,
        OLD.attendance,
        OLD.fee_status

    );

    RETURN OLD;

END;

$$;

----- triggers


CREATE TRIGGER backup_deleted_student

BEFORE DELETE

ON students

FOR EACH ROW

EXECUTE FUNCTION save_deleted_student();


CREATE INDEX idx_student_name
ON students(student_name);

CREATE INDEX idx_email
ON students(email);

CREATE INDEX idx_phone
ON students(phone);

CREATE INDEX idx_department
ON students(department_id);

SELECT
    s.student_id,
    s.student_name,
    s.age,
    s.gender,
    d.department_name,
    s.city,
    s.marks,
    s.attendance,
    s.fee_status
FROM students s
JOIN departments d
ON s.department_id = d.department_id
ORDER BY s.student_id;
