from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def get_db_connection():
    """Connect to the SQLite database"""
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Home page - redirect to registration"""
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Student registration page"""
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        date_of_birth = request.form['date_of_birth']
        address = request.form['address']
        
        # Basic validation
        if not all([first_name, last_name, email]):
            flash('First name, last name, and email are required!', 'error')
            return render_template('register.html')
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Insert student into database
            cursor.execute('''
                INSERT INTO students (first_name, last_name, email, phone, date_of_birth, address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, phone, date_of_birth, address))
            
            conn.commit()
            conn.close()
            
            flash('Student registered successfully!', 'success')
            return redirect(url_for('view_students'))
            
        except sqlite3.IntegrityError:
            flash('Email already exists!', 'error')
            return render_template('register.html')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/students')
def view_students():
    """View all registered students"""
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students ORDER BY registration_date DESC').fetchall()
    conn.close()
    
    return render_template('students.html', students=students)

@app.route('/students/<int:student_id>')
def view_student(student_id):
    """View individual student details"""
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    conn.close()
    
    if student is None:
        flash('Student not found!', 'error')
        return redirect(url_for('view_students'))
    
    return render_template('student_detail.html', student=student)

@app.route('/students/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    """Delete a student"""
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()
    
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('view_students'))

@app.route('/api/students', methods=['GET', 'POST'])
def api_students():
    """API endpoint to get all students in JSON format or create a new student"""
    if request.method == 'GET':
        conn = get_db_connection()
        students = conn.execute('SELECT * FROM students ORDER BY registration_date DESC').fetchall()
        conn.close()

        # Convert to list of dictionaries
        students_list = []
        for student in students:
            students_list.append(dict(student))

        return jsonify(students_list)

    elif request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        date_of_birth = data.get('date_of_birth')
        address = data.get('address')

        # Basic validation
        if not all([first_name, last_name, email]):
             return jsonify({'error': 'First name, last name, and email are required'}), 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO students (first_name, last_name, email, phone, date_of_birth, address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, phone, date_of_birth, address))

            student_id = cursor.lastrowid
            conn.commit()

            # Fetch the created student
            student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
            conn.close()

            return jsonify(dict(student)), 201

        except sqlite3.IntegrityError:
            return jsonify({'error': 'Email already exists'}), 409
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>')
def api_get_student(student_id):
    """API endpoint to get a single student in JSON format"""
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    conn.close()
    
    if student is None:
        return jsonify({'error': 'Student not found'}), 404
    
    return jsonify(dict(student))

if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists('students.db'):
        init_db()
    
    app.run(debug=True, host='0.0.0.0', port=5000)