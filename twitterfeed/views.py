from . import app

from flask import render_template

@app.route('/')
def boo():
	return render_template('index.html');