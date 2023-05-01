from flask import Flask, request, jsonify
import mysql.connector
import os

# read MySQL database credentials from environment variables
mysql_host = os.environ.get('MYSQL_HOST')
mysql_user = os.environ.get('MYSQL_USER')
mysql_password = os.environ.get('MYSQL_PASSWORD')
mysql_database = os.environ.get('MYSQL_DATABASE')

app = Flask(__name__)

# create connection to the MySQL database
db = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
)


# Customers routes

@app.route("/customers", methods=["GET"])
def get_customers():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers")
    result = cursor.fetchall()
    customers = []
    for row in result:
        customer = {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3],
            "address": row[4]
        }
        customers.append(customer)
    return jsonify(customers)

@app.route("/customers/<int:id>", methods=["GET"])
def get_customer(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = %s", (id,))
    result = cursor.fetchone()
    if result is None:
        return jsonify({"message": "Customer not found"}), 404
    customer = {
        "id": result[0],
        "name": result[1],
        "email": result[2],
        "phone": result[3],
        "address": result[4]
    }
    return jsonify(customer)

@app.route("/customers", methods=["POST"])
def create_customer():
    name = request.json["name"]
    email = request.json["email"]
    phone = request.json["phone"]
    address = request.json["address"]
    cursor = db.cursor()
    sql = "INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s)"
    values = (name, email, phone, address)
    cursor.execute(sql, values)
    db.commit()
    return jsonify({"message": "Customer created successfully"}), 201

@app.route("/customers/<int:id>", methods=["PUT"])
def update_customer(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = %s", (id,))
    result = cursor.fetchone()
    if result is None:
        return jsonify({"message": "Customer not found"}), 404
    name = request.json["name"]
    email = request.json["email"]
    phone = request.json["phone"]
    address = request.json["address"]
    sql = "UPDATE customers SET name = %s, email = %s, phone = %s, address = %s WHERE id = %s"
    values = (name, email, phone, address, id)
    cursor.execute(sql, values)
    db.commit()
    return jsonify({"message": "Customer updated successfully"})

@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = %s", (id,))
    result = cursor.fetchone()
    if result is None:
        return jsonify({"message": "Customer not found"}), 404
    sql = "DELETE FROM customers WHERE id = %s"
    values = (id,)
    cursor.execute(sql, values)
    db.commit()
    return jsonify({"message": "Customer deleted successfully"})

# Orders routes

@app.route("/orders", methods=["GET"])
def get_orders():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM orders")
    result = cursor.fetchall()
    orders = []
    for row in result:
        order = {
           
