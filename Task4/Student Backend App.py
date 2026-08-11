from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, make_response
import sqlite3
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = '123hello'

auth = HTTPBasicAuth()

users = {
    "hah": "123"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            CGPA FLOAT NOT NULL,
            Address TEXT
        )
    ''')
    conn.close()

@app.route('/')
@auth.login_required
def home():
    return get_students()

@app.route('/logout')
def logout():
    response = make_response('Logged out')
    response.status_code = 401
    return response

@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM students WHERE id = ?", (id,))
        conn.commit()
        flash('Student deleted successfully!')
    except sqlite3.Error as e:
        flash(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()
    return redirect(url_for('get_students'))

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        cgpa = request.form['CGPA']
        address = request.form['Address']

        if not first_name or not last_name or not cgpa:
            flash('First Name, Last Name, and CGPA are required fields!')
        else:
            try:
                conn = sqlite3.connect('database.db')
                cur = conn.cursor()
                cur.execute("INSERT INTO students (FirstName, LastName, CGPA, Address) VALUES (?, ?, ?, ?)",
                            (first_name, last_name, cgpa, address))
                conn.commit()
                conn.close()
                flash('Student added successfully!')
                return redirect(url_for('home'))
            except sqlite3.Error as e:
                flash(f"An error occurred: {e}")
                conn.rollback()
                conn.close()

    return render_template('create.html')

@app.route('/update/<int:id>/', methods=('GET', 'POST'))
def update(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    
    # Fetch the existing student data
    cur.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cur.fetchone()
    
    if request.method == 'POST':
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        cgpa = request.form['CGPA']
        address = request.form['Address']

        if not first_name or not last_name or not cgpa:
            flash('First Name, Last Name, and CGPA are required fields!')
        else:
            try:
                # Update the student's information
                cur.execute('''
                    UPDATE students
                    SET FirstName = ?, LastName = ?, CGPA = ?, Address = ?
                    WHERE id = ?
                ''', (first_name, last_name, cgpa, address, id))
                conn.commit()
                flash('Student updated successfully!')
                return redirect(url_for('home'))
            except sqlite3.Error as e:
                flash(f"An error occurred: {e}")
                conn.rollback()
            finally:
                conn.close()

    conn.close()
    return render_template('update.html', student=student)

@app.route('/students', methods=['GET'])
def get_students():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    return render_template('students.html', students=rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
