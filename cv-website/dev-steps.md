# Dev steps — build and host resume site

This file lists concise, repeatable developer steps to produce and host your resume website locally using Flask, and to convert a LinkedIn/ PDF resume into text using chat or local tools.

- [ ] Get resume PDF from LinkedIn
- [ ] Convert PDF to text (chat or local tool)
- [ ] Prompt/code in VS Code to create a Flask app that serves HTML/CSS

1) Get resume from my LinkedIn
- Sign in to LinkedIn and open your profile (`linkedin.com/in/georgios-klonis`).
- Use the "More" → "Save to PDF" (or browser Print → Save as PDF) to download your profile/resume as a PDF.
- Save the file to the project root as `resume.pdf` (path: `/Users/georgiosklonis/cv/resume.pdf`).


2) Use chat to convert PDF to text
- Use this chat (recommended for clean sectioned output):
    - Upload the `resume.pdf` to the chat and ask: "Please extract the text from this PDF and return a plain text version preserving headings (Contact, Experience, Education, Skills, etc.). Use double newlines between sections."
    - Example prompt to paste to the chat if upload isn't available:
        "I have a resume PDF. Convert it to plain text retaining headings and bullet points. Output only the text, no commentary."

3) Prompt in VS Code to create the app using Flask and static HTML/CSS
- Goal: produce a minimal, responsive site and a small Flask server that serves it on `http://127.0.0.1:5000`.

- Prompt: "I want to create using css and html the webiste for my resume. Then i need a server to host it (localhost, flask). I attach my resume,. Make the files needed and make good ui"

- After the assistant generates files, verify these items exist in the project root:
    - `app.py`
    - `templates/index.html`
    - `static/style.css`
    - `requirements.txt`
    - `resume.pdf` (optional but recommended)