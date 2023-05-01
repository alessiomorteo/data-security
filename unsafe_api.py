from flask import Flask, request
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

# define endpoint for getting user by ID (unsafe version)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_unsafe(user_id):
    # create cursor object to execute queries
    cursor = db.cursor()

    # construct SQL query string using user input directly (unsafe!)
    sql = "SELECT * FROM users WHERE id = %s" % user_id

    # execute query to retrieve user by ID
    cursor.execute(sql)

    # retrieve result set and return user data as JSON
    result = cursor.fetchone()
    if result is None:
        return {'error': 'User not found'}
    else:
        user = {'id': result[0], 'name': result[1], 'email': result[2]}
        return user

if __name__ == '__main__':
    app.run(debug=True)
