from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/resume.pdf')
def resume_pdf():
    # serve the attached PDF if present in the project root
    return send_from_directory(os.path.dirname(__file__), 'resume.pdf')


if __name__ == '__main__':
    # debug True for local development; change in production
    app.run(host='127.0.0.1', port=5000, debug=True)
