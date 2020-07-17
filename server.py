from flask import Flask, request, render_template
from museums import *
from docks import *
from closest_station import *
from privates import *
import json

app = Flask(__name__)

@app.route('/')
def serveMap():
	return render_template('newmap.html', token=mapbox_token)

@app.route('/api/museums')
def serveMuseums():
	#data1 = request.args.get('somedata1')

	data_mus = elaborate()
	data_mus = json.dumps(data_mus)

	return data_mus

@app.route('/api/docks')
def serveDocks():
	#data1 = request.args.get('somedata1')

	data_docks = join_info_mask()
	data_docks = json.dumps(data_docks)

	return data_docks

@app.route('/path')
def pathfinder():
	count = request.args.get('count')

	print(count)
	return "0"