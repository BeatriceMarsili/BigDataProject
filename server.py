from flask import Flask, render_template
from museums import *
import json

app = Flask(__name__)

#with open('museums.json') as file:
#  data_mus = json.load(file)
data_mus = elaborate()
data_mus = json.dumps(data_mus)

@app.route('/')
def map():
	docks = {"docks":[{"name":"dock1", "latitude":"46.011977","longitude":"11.135038"}, {"name":"dockbello", "latitude":"46.022289","longitude":"11.114299"}]}
	return render_template('map.html', museums=data_mus, docks=docks)

