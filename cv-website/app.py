from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/resume.pdf')
def resume_pdf():
    # serve the attached PDF if present in the project root
    # serve the attached PDF from the `resources` directory
    resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
    return send_from_directory(resources_dir, 'resume.pdf')


@app.route('/resources/<path:filename>')
def resources_file(filename):
    """Serve files from the resources directory (e.g., /resources/resume.pdf)."""
    resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
    return send_from_directory(resources_dir, filename)


if __name__ == '__main__':
    # debug True for local development; change in production
    app.run(host='127.0.0.1', port=5000, debug=True)
