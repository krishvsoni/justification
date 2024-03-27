from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'process.env.JWT_SECRET'

client = MongoClient('mongodb+srv://krishsoni:2203031050659@paytm.aujjoys.mongodb.net/')  
db = client['user_db']  
users_collection = db['users']  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if users_collection.find_one({'username': username}):
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            users_collection.insert_one({'username': username, 'password': password})
            flash('Signup successful. You can now login.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            flash('Login successful.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('log.html')

if __name__ == '__main__':
    app.run(debug=True)
