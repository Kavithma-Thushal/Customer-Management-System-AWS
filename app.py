from flask import Flask, request, redirect, url_for, render_template
from image_upload import upload_file

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        salary = request.form['salary']
        file = request.files['file']

        if file:
            result = upload_file(name, address, salary, file)

            if result == "success":
                return redirect(url_for('main', success=1))
            else:
                return "<h3>Failed to save the customer!</h3>"

    success_alert = request.args.get('success', '')
    return render_template('index.html', success_alert=success_alert)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
