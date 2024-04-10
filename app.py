from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'process.env.JWT_SECRET'

client = MongoClient('')  
db = client['flask-auth']  
users_collection = db['users']  
attendance_collection = db['attendance']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        if users_collection.find_one({'username': username}):
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            users_collection.insert_one({'username': username, 'password': hashed_password})
            flash('Signup successful. You can now login.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            flash('Login successful.', 'success')
            return redirect(url_for('welcome', username=username))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('log.html')

@app.route('/dashboard/<username>')
def welcome(username):
    user = users_collection.find_one({'username': username})
    if user:
        return render_template('dashboard.html', username=username)
    else:
        flash('User not found.', 'danger')
        return redirect(url_for('index'))
    

@app.route('/save_attendance', methods=['POST'])
def save_attendance():
    if request.method == 'POST':
        try:
            username = request.form['username']
            total_lectures = int(request.form['total_lectures'])
            attended_lectures = int(request.form['attended_lectures'])
            
            attendance_collection.insert_one({'username': username, 'total_lectures': total_lectures, 'attended_lectures': attended_lectures})

            flash('Attendance saved successfully.', 'success')
            return redirect(url_for('welcome', username=username))
        except Exception as e:
            flash(f'Error occurred while saving attendance: {str(e)}', 'danger')
            return redirect(url_for('index'))
    else:
        flash('Invalid request method.', 'danger')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
