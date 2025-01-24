from flask import Flask, render_template, request, redirect, url_for, flash
from user_database import UseeDatabase
from vector_database import VectorDatabase
import json
from aws import AWS
import regex as re
from log_file import logger
app = Flask(__name__)
app.secret_key = 'your_secret_key'

with open("data.json", 'r') as json_file:
    users = json.load(json_file)
db=UseeDatabase(users['user'],users['password'])
aws=AWS()
EMAIL_REGEX = re.compile(r'^[a-zA-Z][a-zA-Z0-9._%+-]*@[a-zA-Z]{1,10}\.[a-zA-Z0-9]{2,3}$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,30}$')

@app.route('/')
def index():
    logger.info("Home page retrieved successfully")
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        logger.info("Login Page retrieved successfully")
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in db.select_users() and db.get_password(email) == password:
            logger.info("User Login Successful")
            return render_template('search.html')
        else:
            logger.warning("Invalid username or password")
            flash('Invalid username or password', 'danger')
            return redirect('/login')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        logger.info("Signup page retrieved successfully")
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['name']
        number = request.form['mobile']
        email = request.form['email']
        password = request.form['password']

        # Validate email with the refined regex
        if not EMAIL_REGEX.match(email):
            logger.warning("Invalid email address entered by user")
            flash('Invalid email address', 'danger')
            return redirect(url_for('signup'))
        if not PASSWORD_REGEX.match(password):
            logger.warning("Invalid password entered by user")
            flash('Password must be 6-30 characters long, include at least one uppercase letter, one lowercase letter, one number, and one special character.', 'danger')
            return redirect(url_for('signup'))
        # Check if email already exists
        if email in db.select_users():
            logger.warning("Username already exists")
            flash('Username already exists', 'danger')
        else:
            logger.info("New user added to the database")
            db.insert_table(username, number, email, password)
            flash('User created successfully!', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        logger.info("Search page retrieved successfully")
        return render_template('search.html')
    elif request.method == 'POST':
        search_query = request.form['query']
        
        if not search_query:
            logger.warning("No query provided by user")
            return render_template('search.html', error='No query provided.')

        # Example database connection and operations
        try:
            database = VectorDatabase("saikumar-007", "Saikumar20@")
            if database.initialized:
                logger.info("Database initialized successfully")
                database.create_table()  # Example method to create table
                database.insert_table()  # Example method to insert data
                search_results = database.search(search_query)  # Example method to search

                # Example AWS function to format results
                formatted_results = aws.return_content(search_results)

                return render_template('search_results.html', results=formatted_results)
            else:
                logger.warning("Database not initialized")
                return render_template('search.html', error='Database not initialized.')

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return render_template('search.html', error='An error occurred while processing your request.')


@app.route('/home')
def home():
    logger.info("Home page retrieved successfully")
    query = request.args.get('query', '')
    # Here you can implement the logic to perform the search
    return render_template('home.html', query=query)

if __name__ == '__main__':
    app.run(debug=True)

