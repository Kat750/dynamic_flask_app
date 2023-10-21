from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE_NAME = "app_database.db"

def get_db_connection():
    return sqlite3.connect(DATABASE_NAME)

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        """)
        conn.commit()

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')

    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            message = "Successfully registered!"
        except sqlite3.IntegrityError:
            message = "Email already exists!"

    return render_template('main.html', message=message)

@app.route('/users')
def show_users():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, email FROM users")
        users = cursor.fetchall()

    return render_template('users.html', users=users)

init_db()

if __name__ == "__main__":
    app.run(debug=True)

