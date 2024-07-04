import mysql.connector
import json
from request import Request
import numpy as np
from aws import AWS
import time
class Db:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connection = None
        self.cursor = None
        self.initialized=False
        self.request=Request()
        self.aws=AWS()
        self.database_initialize()

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
        self.cursor.execute("CREATE TABLE IF NOT EXISTS bucket_vector (file_name TEXT,vector text)")
        self.connection.commit()
    
    def insert_table(self):
        self.cursor.execute('SELECT file_name FROM bucket_vector')
        rows = self.cursor.fetchall()
        # Convert dict_keys to a set
        x_set = set(self.aws.file_keys)

        # Convert list of tuples to a set
        # This step extracts 'America.pdf' from the tuple inside the list
        y_set = set([item for sublist in rows for item in sublist])

        # Perform the set subtraction
        result = x_set - y_set
        not_added=list(result)
        for text in not_added: 
            file_content=self.aws.return_content(text)
            vector=self.request.request_insert(file_content)
            vector_json=json.dumps(vector)
            query='INSERT INTO bucket_vector (file_name,vector) values (%s,%s)'
            time.sleep(30)
            self.cursor.execute(query,(text,vector_json))
            self.connection.commit()
    
    def search(self,text):
        print(text)
        if self.cursor is None:
            print("Database connection is not established.")
            return

        vector = self.request.request_search(text)  # Assuming this returns the vector as a Python object
        
        self.cursor.execute('SELECT file_name, vector FROM bucket_vector')
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
        top_results = results[:2]
        print(top_results[0])
        top_results = [row[0] for row in top_results]
        print(top_results[0])
        return top_results[0]

    def cursor_close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


def main():
    database = Db("saikumar-007","Saikumar20@")
    if database.initialized:
        database.create_table()
        database.insert_table()
    else:
        print("Invalid credentials. Please try again.")

            
main()
