import os

import psycopg


def get_connection():
    """Return a PostgreSQL connection.

    The password is read from the DB_PASSWORD environment variable so it is
    never stored in the code. DB_HOST, DB_NAME, DB_USER and DB_PORT are
    optional and default to a local PostgreSQL setup.
    """
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "student_management"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.environ["DB_PASSWORD"],
        port=int(os.getenv("DB_PORT", "5432")),
    )
