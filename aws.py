import numpy as np
import requests
import boto3
import PyPDF2
import io
import json
class AWS:
    def __init__(self):
        with open("aws.json", 'r') as json_file:
                    credentials = json.load(json_file)
        s3=boto3.resource(service_name='s3',
                        region_name="us-east-1",
                        aws_access_key_id=credentials["aws_access_key_id"],
                        aws_secret_access_key=credentials["aws_secret_access_key"]
                        )
        self.file_keys=[]
        self.files_content={}
        self.bucket_name = 'storage-sample-bucket'
        self.file_key = 'America.pdf'
        self.bucket=s3.Bucket(self.bucket_name)
        for obj in self.bucket.objects.all():
            self.file_keys.append(obj.key)
        self.aws_retrieval()
        
    def aws_retrieval(self):
        for file_key in self.file_keys:
            pdf_data = io.BytesIO()
            self.bucket.download_fileobj(file_key, pdf_data)
            pdf_data.seek(0)

            # Read PDF data using PyPDF2
            pdf_reader = PyPDF2.PdfReader(pdf_data)

            # Get number of pages
            num_pages = len(pdf_reader.pages)

            # Extract text from each page
            file_content=""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                file_content=file_content+text
            self.files_content[file_key]=file_content
    def prints(self):
        print(self.files_content.keys())
    
    def return_content(self,file_name):
        if file_name in self.files_content.keys():
            return self.files_content[file_name]
        