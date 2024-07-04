from flask import Flask, render_template, request, redirect, url_for, flash
from database import Database
from database_file import Db
import json
from aws import AWS
import regex as re
app = Flask(__name__)
app.secret_key = 'your_secret_key'

with open("data.json", 'r') as json_file:
    users = json.load(json_file)
db=Database(users['user'],users['password'])
aws=AWS()
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in db.select_users() and db.get_password(email) == password:
            return render_template('search.html')
        else:
            flash('Invalid username or password', 'danger')
            return redirect('/login')
    return render_template('login.html')
EMAIL_REGEX = re.compile(r'^[a-zA-Z][a-zA-Z0-9._%+-]*@[a-zA-Z]{1,10}\.[a-zA-Z0-9]{2,3}$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,30}$')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['name']
        number = request.form['mobile']
        email = request.form['email']
        password = request.form['password']

        # Validate email with the refined regex
        if not EMAIL_REGEX.match(email):
            flash('Invalid email address', 'danger')
            return redirect(url_for('signup'))
        if not PASSWORD_REGEX.match(password):
            flash('Password must be 6-30 characters long, include at least one uppercase letter, one lowercase letter, one number, and one special character.', 'danger')
            return redirect(url_for('signup'))
        # Check if email already exists
        if email in db.select_users():
            flash('Username already exists', 'danger')
        else:
            db.insert_table(username, number, email, password)
            flash('User created successfully!', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    elif request.method == 'POST':
        search_query = request.form['query']
        
        if not search_query:
            return render_template('search.html', error='No query provided.')

        # Example database connection and operations
        try:
            database = Db("saikumar-007", "Saikumar20@")
            if database.initialized:
                database.create_table()  # Example method to create table
                database.insert_table()  # Example method to insert data
                search_results = database.search(search_query)  # Example method to search

                # Example AWS function to format results
                formatted_results = aws.return_content(search_results)
                print(formatted_results)

                return render_template('search_results.html', results=formatted_results)
            else:
                return render_template('search.html', error='Database not initialized.')

        except Exception as e:
            print(f"Error: {str(e)}")
            return render_template('search.html', error='An error occurred while processing your request.')


@app.route('/home')
def home():
    query = request.args.get('query', '')
    # Here you can implement the logic to perform the search
    return render_template('home.html', query=query)

if __name__ == '__main__':
    app.run(debug=True)

