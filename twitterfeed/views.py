from . import app

from flask import render_template, redirect, url_for
from flask import request

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/teaminfo')
def teaminfoindex():
	return render_template('teaminfoindex.html')

@app.route('/teaminfo/<int:teamnumber>')
def teaminfo(teamnumber):
	return render_template('teaminfo.html', teamnumber = teamnumber, regionals = ["a",'b'])

@app.route('/teaminfo_dispatcher', methods=['GET'])
def teaminfo_dispatcher():
	return redirect(url_for('teaminfo',teamnumber = request.args['teamnumber']))
