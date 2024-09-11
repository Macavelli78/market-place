from flask import Flask, request, render_template
from flask import Flask, render_template, request, redirect, url_for

import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

#Setting a secret key



# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change to your MySQL server address
            database='marketplace',  # Your database name
            user='root',  # Your MySQL username
            password='Draughtsman78'  # Your MySQL password
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Render the login and sign-up forms
@app.route('/')
def index():
    return render_template('index.html')

# Handle user login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Connect to the database and validate user credentials
    connection = create_connection()
    if connection is None:
        return "Error connecting to the database"

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM user_login WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return redirect(url_for('welcome'))
    else:
        return "Login failed. Incorrect username or password."

# Handle user sign-up and add the new user to the database
@app.route('/signup', methods=['POST'])
def signup():
    new_username = request.form['new_username']
    new_password = request.form['new_password']

    # Connect to the database
    connection = create_connection()
    if connection is None:
        return "Error connecting to the database"

    cursor = connection.cursor()

    # Check if the username already exists
    check_query = "SELECT * FROM user_login WHERE username = %s"
    cursor.execute(check_query, (new_username,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        connection.close()
        return "Username already exists. Please choose a different username."

    # Insert new user into the database
    insert_query = "INSERT INTO user_login (username, password) VALUES (%s, %s)"
    cursor.execute(insert_query, (new_username, new_password))
    connection.commit()

    cursor.close()
    connection.close()

    return f"User {new_username} registered successfully!"

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')
    
if __name__ == '__main__':
    app.run(debug=True)
