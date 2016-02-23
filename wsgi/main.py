from flask import Flask, jsonify, render_template, make_response, send_from_directory
import os
import config
import data

app = Flask(__name__)

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

@app.route('/data.json', methods=['GET'])
def json_data():
	return jsonify(members=[m['name'] for m in config.members], summary=data.copa())

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
	return send_from_directory(root, path)

@app.route('/', methods=['GET'])
def redirect_to_index():
	return send_from_directory(root, 'index.html')

if __name__ == '__main__':
	#app.debug = True
	app.config['PROPAGATE_EXCEPTIONS'] = True
	app.run(host='0.0.0.0')
