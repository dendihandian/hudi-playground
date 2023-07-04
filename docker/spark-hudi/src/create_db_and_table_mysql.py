"""
docker-compose exec spark-hudi-master python src/create_db_and_table_mysql.py
"""

import pymysql
from faker import Faker
from datetime import datetime
from faker.providers import date_time
from faker.providers import lorem

# Connect to MySQL server
conn = pymysql.connect(
    host="mysql",
    user="root",
    password="example"
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Check if a database exists
database_name = "test_db"
cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")

# Fetch the result
result = cursor.fetchone()

# Check if the result is None (i.e., database exists)
if result is None:
    # Create a database
    cursor.execute(f"CREATE DATABASE {database_name}")

# Switch to the created database
cursor.execute(f"USE {database_name}")

# Create a table
table_name = "test_table"
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP NULL
)
"""
cursor.execute(create_table_query)

# Commit the changes to the database
conn.commit()

# Create fake data generator
fake = Faker()
fake.add_provider(date_time)
fake.add_provider(lorem)


# Generate and insert fake data into the table
num_records = 100  # Number of records to generate

for _ in range(num_records):

    title = fake.sentence(nb_words=4, variable_nb_words=True)
    created_at = fake.date_time_between(start_date="-1y", end_date="-30d")
    updated_at = fake.date_time_between(start_date="-30d", end_date="now")
    
    insert_query = f"INSERT INTO {table_name} (title, created_at, updated_at) VALUES ('{title}', '{created_at}', '{updated_at}')"
    cursor.execute(insert_query)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
