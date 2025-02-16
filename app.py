import boto3
import os
from flask import Flask, request, redirect, url_for
from customer_save import save_customer

app = Flask(__name__)

# Provide AWS Credentials
os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAQ4NSBRLG6INV3V7A'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
s3 = boto3.client('s3')

# Define the S3 bucket name
BUCKET_NAME = "ijse-s3-bucket"


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        file = request.files['file']
        name = request.form['name']
        address = request.form['address']
        salary = request.form['salary']

        if file:
            # Generate new filename based on the customer's name
            new_filename = f"{name.lower()}-profile-photo{os.path.splitext(file.filename)[1]}"

            try:
                # Upload file
                s3.upload_fileobj(file, BUCKET_NAME, new_filename)

                # Save customer to the database
                save_customer(name, address, salary, new_filename)

                # Redirect with a success flag
                return redirect(url_for('main', success=1))
            except Exception as e:
                print(f"Error: {e}")
                return "<h3>There was an error...!</h3>"

    success_alert = request.args.get('success', '')

    return f'''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Customer Management</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
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
        
        <script>
            window.onload = function() {{
                var success = "{success_alert}";
                if (success === "1") {{
                    alert("Customer Saved Successfully...!");
                }}
            }}; 
        </script>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
