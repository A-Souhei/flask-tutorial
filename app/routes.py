from app import app
import os


@app.route('/')
@app.route('/index')
def index():
    return f"From {os.getenv('FLASK_APP')} : Hello, World!"
