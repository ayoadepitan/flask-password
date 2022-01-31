from flask import render_template
from password import app

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')
