import json
import requests
from log_file import logger
class Request:
    def __init__(self) -> None:
        self.token=None
        self.url=None
        self.token_initialization()
        self.header= {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    def token_initialization(self):
        with open("api.json", 'r') as json_file:
            api = json.load(json_file)
        self.token=api['token']
        self.url=api['url']
    
    def request_insert(self,vector_text):
        body = {
        "model": "text-embedding-ada-002",
        "input": vector_text
        }
        response = requests.post(self.url, json=body, headers=self.header)

        if response.status_code == 200:
            # Request was successful
            data = response.json()  # Assuming response is JSON data
            logger.info("Success") 
        else:
            logger.error('Error:', response.status_code)

        vector=data['data'][0]['embedding']
        return vector
    
    def request_search(self,vector_text):
        body = {
        "model": "text-embedding-ada-002",
        "input": vector_text
        }
        response = requests.post(self.url, json=body, headers=self.header)
        if response.status_code == 200:
            # Request was successful
            data = response.json()  # Assuming response is JSON data
            logger.info("Success") 
        else:
            logger.error('Error:', response.status_code)
        vector=data['data'][0]['embedding']
        return vector