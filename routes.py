from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# connecting to the database
def get_db_connection():
    conn = sqlite3.connect('DF_DATABASE.db')
    conn.row_factory = sqlite3.Row
    return conn

# it retrieves the categories from the 'Categories' table
@app.context_processor
def inject_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM Categories').fetchall()
    conn.close()
    return {'nav_categories': categories}

# this function opens a connection to the database, executes a query to get all categories from the 'Categories' table, and then closes the connection.
@app.route('/')
def index():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM Categories').fetchall()
    conn.close()
    return render_template('index.html', categories=categories)

# this function takes a category ID from the URL, retrieves the category details and associated devil fruits from the database, and then closes the connection.
@app.route('/category/<int:category_id>')
def category(category_id):
    conn = get_db_connection()
    category = conn.execute('SELECT * FROM Categories WHERE category_id = ?', (category_id,)).fetchone()
    fruits = conn.execute('SELECT * FROM DevilFruits WHERE category_id = ?', (category_id,)).fetchall()
    conn.close()
    return render_template('category.html', category=category, fruits=fruits)

# this function takes a fruit ID from the URL, retrieves the details of the devil fruit and its associated abilities from the database, and then closes the connection.
@app.route('/fruit/<int:fruit_id>')
def fruit(fruit_id):
    conn = get_db_connection()
    fruit = conn.execute('SELECT * FROM DevilFruits WHERE fruit_id = ?', (fruit_id,)).fetchone()
    abilities = conn.execute('SELECT * FROM DevilFruits_Abilities WHERE fruit_id = ?', (fruit_id,)).fetchall()
    conn.close()
    return render_template('fruit.html', fruit=fruit, abilities=abilities)

# this function retrieves all user records from the 'Users' table in the database and closes the database connection
@app.route('/users')
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM Users').fetchall()
    conn.close()
    return render_template('users.html', users=users)

#
if __name__ == '__main__':
    app.run(debug=True)