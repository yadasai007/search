import mysql.connector
import json
from request import Request
import numpy as np
class Database:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connection = None
        self.cursor = None
        self.initialized=False
        self.request=Request()
        self.database_initialize()
        self.create_table()

    def database_initialize(self):
        with open("data.json", 'r') as json_file:
            users = json.load(json_file)
        user_credentials = users
        if user_credentials["password"]==self.password:
            try:
                self.connection = mysql.connector.connect(**user_credentials)
                self.cursor = self.connection.cursor()
                print("Connection to MySQL database successful")
                self.initialized=True
            except mysql.connector.Error as e:
                print(f"Error connecting to MySQL database: {e}")
                raise  # Raise the exception to notify the caller
        else:
            print("Incorrect password")

    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT,number TEXT,email TEXT, password TEXT)")
        self.connection.commit()
        pass
    def delete_table(self):
        self.cursor.execute("drop table vectors_1")
        self.connection.commit()
    def insert_table(self,name,email,mobile,password):
        query='INSERT INTO users (name,number,email,password) values (%s,%s,%s,%s)'
        self.cursor.execute(query,(name,email,mobile,password))
        self.connection.commit()

    def get_password(self, email):
        query = "SELECT password FROM users WHERE email=%s"
        self.cursor.execute(query, (email,))
        users = self.cursor.fetchall()
        users = [row[0] for row in users]
        return users[0]


    def select_users(self):
        query = "SELECT email FROM users"
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        users = [row[0] for row in users]
        return users


    def search(self):
        if self.cursor is None:
            print("Database connection is not established.")
            return

        text = input("Enter search text: ")
        vector = self.request.request_search(text)  # Assuming this returns the vector as a Python object
        
        self.cursor.execute('SELECT text, vector FROM vectors1')
        rows = self.cursor.fetchall()

        # Prepare a list to hold dot product results
        results = []

        for row in rows:
            content, stored_vector_json = row
            stored_vector = np.array(json.loads(stored_vector_json))
            
            # Calculate the dot product
            score = np.dot(vector, stored_vector)
            
            # Append the content and score to the results list
            results.append((content, score))

        # Sort the results based on the score in descending order
        results.sort(key=lambda x: x[1], reverse=True)

        # Select the top 3 results
        top_results = results[:3]

        for content, score in top_results:
            print(f"Content: {content}, Score: {round(score,2)}")


    def cursor_close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
db=Database("saikumar-007","Saikumar20@")
