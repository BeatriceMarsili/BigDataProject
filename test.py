from flask import Flask, send_file, render_template

app = Flask(__name__)


@app.route('/images/<string:color>')
def marker(color):
	return send_file("./images/marker"+color+".png",mimetype='image/gif')

@app.route('/')
def map():
	data = {"museums":[{"name":"muse", "lat":"46.004093","lon":"11.118709"}, {"name":"stocazzo", "lat":"46.004193","lon":"11.128709"}, {"name":"terzo", "lat":"46.001492","lon":"11.131723"}],
	"docks":[{"name":"dock1", "lat":"46.011977","lon":"11.135038"}, {"name":"dockbello", "lat":"46.022289","lon":"11.114299"}]}
	return render_template('map.html', data=data)

