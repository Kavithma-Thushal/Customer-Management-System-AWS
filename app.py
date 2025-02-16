from flask import Flask, request, redirect, url_for
import boto3
import os
from customer_save import save_customer_to_db  # Import the function to save to DB

app = Flask(__name__)

# Provide AWS Credentials
os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAQ4NSBRLG6INV3V7A'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
s3 = boto3.resource('s3')

# Define the S3 bucket name
BUCKET_NAME = "ijse-s3-bucket"

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        name = request.form['name']
        address = request.form['address']
        salary = request.form['salary']

        if file:
            # Generate new filename based on the customer's name
            new_filename = f"{name.lower()}-profile-photo{os.path.splitext(file.filename)[1]}"
            file_path = os.path.join(UPLOAD_FOLDER, new_filename)

            # Save the file locally with the new name
            file.save(file_path)

            # Use the new filename as the S3 key
            s3_key = new_filename

            # Upload the file to S3
            with open(file_path, 'rb') as f:
                s3.Bucket(BUCKET_NAME).put_object(Key=s3_key, Body=f)
            os.remove(file_path)  # Remove the local file after uploading

            # Save customer details to DB with the new filename
            save_customer_to_db(name, address, salary, s3_key)

            # Redirect with a success flag
            return redirect(url_for('upload_file', success=1))

    success_alert = request.args.get('success', '')

    return f'''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Customer Management</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <script>
            window.onload = function() {{
                var success = "{success_alert}";
                if (success === "1") {{
                    alert("Customer Saved Successfully...!");
                    window.location.href = "/";
                }}
            }};
        </script>
    </head>
    
    <body>
        <div class="d-flex justify-content-center align-items-center vh-100">
            <div class="container">
                <div class="row justify-content-center mt-5">
                    <div class="col-6 text-center shadow-lg p-5 rounded">
                        <h1 class="mb-5">Customer Management</h1>
                        <form method="POST" enctype="multipart/form-data">
                            <div class="mb-3">
                                <input type="text" name="name" class="form-control" placeholder="Name" required>
                            </div>
                            <div class="mb-3">
                                <input type="text" name="address" class="form-control" placeholder="Address" required>
                            </div>
                            <div class="mb-3">
                                <input type="number" name="salary" class="form-control" placeholder="Salary" required>
                            </div>
                            <div class="mb-3">
                                <input type="file" name="file" class="form-control" required>
                            </div>
                            <div class="mb-3 text-center">
                                <button type="submit" class="btn btn-primary px-4 mt-3">Save</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)
