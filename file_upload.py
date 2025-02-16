import boto3
import os
from customer_save import save_customer

# Provide AWS Credentials
os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAQ4NSBRLG6INV3V7A'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
s3 = boto3.client('s3')

# Define the S3 bucket name
BUCKET_NAME = "ijse-s3-bucket"


def upload_file(file, name, address, salary):
    try:
        # Generate new filename based on the customer's name
        new_filename = f"{name.lower()}-profile-photo{os.path.splitext(file.filename)[1]}"

        # Upload file to S3
        s3.upload_fileobj(file, BUCKET_NAME, new_filename)

        # Save customer to the database
        save_customer(name, address, salary, new_filename)

        return "success"
    except Exception as e:
        print(f"Error: {e}")
        return "Failed to save the customer...!"
