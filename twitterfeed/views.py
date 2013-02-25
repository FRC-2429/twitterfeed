from . import app

from flask import render_template, redirect, url_for
from flask import request

from . import fms

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/teaminfo')
def teaminfoindex():
	return render_template('teaminfoindex.html')

@app.route('/teaminfo/<int:teamnumber>')
def teaminfo(teamnumber):

	with fms.FMS() as fmsSystem:
		fmsSystem.checkForUpdates()
		regionalInfo =  fmsSystem.getEventsForTeam(teamnumber)
		years = {event['year'] for event in regionalInfo}
		events = {event['event'] for event in regionalInfo}
		
		finalStorage = {name:{year:False for year in years} for name in events}
		for event in regionalInfo:
			finalStorage[event['event']][event['year']] = True


		return render_template('teaminfo.html', teamnumber = teamnumber, regionals = finalStorage, years=years, regionalKeys = finalStorage.keys() )

@app.route('/teaminfo_dispatcher', methods=['GET'])
def teaminfo_dispatcher():
	return redirect(url_for('teaminfo',teamnumber = request.args['teamnumber']))
