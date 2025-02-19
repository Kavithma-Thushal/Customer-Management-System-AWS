import boto3
import os
from customer_save import save_customer

# Provide AWS Credentials
os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAQ4NSBRLGTTGJ2G7J'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
s3 = boto3.client('s3')

# Define the S3 bucket name
BUCKET_NAME = "ijse-s3-bucket"


def upload_file(name, address, salary, file):
    try:
        # Generate new filename based on the customer's name
        profile_photo = f"{name.lower()}-profile-photo{os.path.splitext(file.filename)[1]}"

        # Upload file to S3
        s3.upload_fileobj(file, BUCKET_NAME, profile_photo)

        # Save customer to the database
        save_customer(name, address, salary, profile_photo)

        return "success"
    except Exception as e:
        print(f"Error: {e}")
        return "Failed to save the customer!"
