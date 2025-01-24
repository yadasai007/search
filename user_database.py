import mysql.connector
import json
from request import Request
import numpy as np
from log_file import logger
class UseeDatabase:
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
                logger.info("Connection to MySQL database successful")
                self.initialized=True
            except mysql.connector.Error as e:
                logger.error(f"Error connecting to MySQL database: {e}")
                raise  # Raise the exception to notify the caller
        else:
            logger.warning("Incorrect password")

    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT,number TEXT,email TEXT, password TEXT)")
        self.connection.commit()
        pass

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

    def cursor_close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
db=UseeDatabase("saikumar-007","Saikumar20@")
