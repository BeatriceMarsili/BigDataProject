from flask import Flask, request, render_template
from museums import *
from docks import *
from pathfinder import *
from privates import *
import json

app = Flask(__name__)

@app.route('/')
def serveMap():
	return render_template('newmap.html', token=mapbox_token)

@app.route('/api/museums')
def serveMuseums():
	#data1 = request.args.get('somedata1')

	data_mus = museums_info()
	data_mus = json.dumps(data_mus)

	return data_mus

@app.route('/api/docks')
def serveDocks():
	#data1 = request.args.get('somedata1')

	data_docks = join_station_info_masked()
	data_docks = json.dumps(data_docks)

	return data_docks

@app.route('/path')
def pathfinder():

	count = int(request.args.get('count'))
	lat = float(request.args.get('lat'))
	lon = float(request.args.get('lon'))

	print("pathfinding from..." + str(lat) + ", " + str(lon))

	return user_path(lat,lon,count)