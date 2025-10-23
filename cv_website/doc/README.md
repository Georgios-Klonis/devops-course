Resume website (Flask) — Georgios Klonis

Overview
--------
This is a minimal Flask application that serves a responsive HTML/CSS resume for Georgios Klonis at http://localhost:5000.

Files added
- `app.py` — Flask application
- `templates/index.html` — Resume HTML template
- `static/style.css` — Site styles
- `requirements.txt` — Python dependencies

Run locally (macOS, zsh)
------------------------
1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open http://127.0.0.1:5000 in your browser.

Notes
- The project will serve `resume.pdf` if present at the repository root. It's already included in this workspace.
 - The project will serve `resume.pdf` from the `resources/` directory. It's already included in this workspace.
- Change `app.run(..., debug=True)` to `False` when not developing.

Run without virtualenv (quick)
------------------------------
If you don't want to use a virtual environment, install dependencies system-wide (or with --user) and run the app directly:

```bash
# install dependencies system-wide (you may need sudo)
pip3 install -r requirements.txt

# then run
python3 app.py
```

Or install to your user account without sudo:

```bash
pip3 install --user -r requirements.txt
python3 app.py
```
