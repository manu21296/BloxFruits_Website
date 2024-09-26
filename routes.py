from flask import Flask, render_template, url_for, request, abort
import sqlite3

app = Flask(__name__)

# Connecting to the database
def get_db_connection():
    conn = sqlite3.connect('DF_DATABASE.db')  # Replace with your actual local path if different
    conn.row_factory = sqlite3.Row
    return conn

# It retrieves the categories from the 'Categories' table, excluding unwanted ones from the navigation bar
@app.context_processor
def inject_categories():
    conn = get_db_connection()
    excluded_categories = ('Paramecia', 'Logia', 'Zoan')
    categories = conn.execute('SELECT * FROM Categories WHERE name NOT IN (?, ?, ?)', excluded_categories).fetchall()
    conn.close()
    return {'nav_categories': categories}

# Index route
@app.route('/')
def index():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM Categories').fetchall()
    fruits = conn.execute('SELECT * FROM DevilFruits').fetchall()  # Fetch all fruits if needed
    conn.close()
    return render_template('index.html', categories=categories, fruits=fruits, active_page='home')

# Route for all categories
@app.route('/categories')
def categories():
    conn = get_db_connection()
    all_categories = conn.execute('SELECT * FROM Categories').fetchall()
    conn.close()
    return render_template('categories.html', categories=all_categories, active_page='categories')

# Route for individual category
@app.route('/category/<int:category_id>')
def category(category_id):
    conn = get_db_connection()
    category = conn.execute('SELECT * FROM Categories WHERE category_id = ?', (category_id,)).fetchone()
    fruits = conn.execute('SELECT * FROM DevilFruits WHERE category_id = ?', (category_id,)).fetchall()
    if category is None:
        abort(404)  # This will trigger your 404 error page
    conn.close()
    return render_template('category.html', category=category, fruits=fruits, active_page='category_' + str(category_id))

# Route for individual fruit
@app.route('/fruit/<int:fruit_id>')
def fruit(fruit_id):
    conn = get_db_connection()
    fruit = conn.execute('SELECT * FROM DevilFruits WHERE fruit_id = ?', (fruit_id,)).fetchone()
    abilities = conn.execute('SELECT * FROM DevilFruits_Abilities WHERE fruit_id = ?', (fruit_id,)).fetchall()
    conn.close()
    return render_template('fruit.html', fruit=fruit, abilities=abilities)

# Route for users
@app.route('/users')
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM Users').fetchall()
    conn.close()
    return render_template('users.html', users=users, active_page='users')

# Route for individual user
@app.route('/user/<int:user_id>')
def user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    if not user:
        abort(404)  # Triggers the 404 error page
    return render_template('user.html', user=user)

# Route for about page
@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

# Search route
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if len(query) > 10:
        return render_template('404.html'), 404
    conn = get_db_connection()
    results = conn.execute('SELECT * FROM DevilFruits WHERE name LIKE ?', ('%' + query + '%',)).fetchall()
    conn.close()
    return render_template('search_results.html', query=query, results=results)

# 404 error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Main function
if __name__ == '__main__':
    app.run(debug=True)
