from . import app

from flask import render_template;

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/teaminfo')
def teaminfo():
	return render_template('teaminfo.html')