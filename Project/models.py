from django.db import connection

# Create your models here.
def create_table():
    with connection.cursor() as cursor:
        cursor.execute("""
                CREATE TABLE if not exists my_integer_data (
                id SERIAL PRIMARY KEY,
                value1 INT,
                value2 INT,
                value3 INT
                );
        """)
def insert_data():
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO my_integer_data (value1, value2, value3)
            VALUES
            (10, 20, 30),
            (15, 25, 35),
            (8, 18, 28),
            (12, 22, 32),
            (5, 15, 25),
            (30, 40, 50),
            (7, 17, 27),
            (22, 32, 42),
            (14, 24, 34),
            (18, 28, 38);
        """)

def retreive_data():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM my_integer_data;
        """)
        data = cursor.fetchall()
    return data
