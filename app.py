from flask import Flask, request
import boto3
import os

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

        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            s3_key = file.filename
            with open(file_path, 'rb') as f:
                s3.Bucket(BUCKET_NAME).put_object(Key=s3_key, Body=f)
            os.remove(file_path)

            return "<h3'>Image uploaded successfully...!</h3>"

        return "<h3>No file uploaded...!</h3>"

    return '''
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
                        <h1 class="mb-4">Customer Management</h1>
                        <form method="POST" enctype="multipart/form-data">
                            <div class="mb-3 d-flex align-items-center">
                                <input type="file" name="file" class="form-control me-2" required>
                                <button type="submit" class="btn btn-primary">Upload</button>
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
