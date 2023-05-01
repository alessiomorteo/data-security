from faker import Faker
import random
import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="yourdatabase"
)

# Create a Faker instance
fake = Faker()

# Generate 50 random customers
for i in range(50):
    # Generate fake customer data
    name = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    address = fake.address()

    # Insert customer data into the database
    cursor = db.cursor()
    sql = "INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s)"
    values = (name, email, phone, address)
    cursor.execute(sql, values)
    db.commit()

# Generate 100 random orders
for i in range(100):
    # Choose a random customer ID
    cursor = db.cursor()
    cursor.execute("SELECT id FROM customers")
    customer_id = random.choice(cursor.fetchall())[0]

    # Generate fake order data
    order_date = fake.date_between(start_date='-1y', end_date='today')
    total = round(random.uniform(10, 1000), 2)

    # Insert order data into the database
    cursor = db.cursor()
    sql = "INSERT INTO orders (customer_id, order_date, total) VALUES (%s, %s, %s)"
    values = (customer_id, order_date, total)
    cursor.execute(sql, values)
    db.commit()

# Generate 50 random products
for i in range(50):
    # Generate fake product data
    name = fake.word()
    description = fake.text()
    price = round(random.uniform(1, 100), 2)

    # Insert product data into the database
    cursor = db.cursor()
    sql = "INSERT INTO products (name, description, price) VALUES (%s, %s, %s)"
    values = (name, description, price)
    cursor.execute(sql, values)
    db.commit()

# Close the database connection
db.close()
