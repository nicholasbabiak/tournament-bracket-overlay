import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send

from config import Config
conf = Config()

history = ["reset"]

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = conf.secret_key
socketio = SocketIO(app)


@app.route("/")
def overlay():
	return render_template('overlay.html')

def send_update():
	socketio.emit("update", json.dumps(history[-1]))

@app.route("/api/reset", methods=['POST'])
def reset():
	history.append("reset")
	send_update()

	data = {"status": "success"}
	return data, 200

@app.route("/api/back", methods=['POST'])
def back():
	history.pop()
	send_update()

	data = {"status": "success"}
	return data, 200

@app.route("/api/set-seed", methods=['POST'])
def set_seed():
	data = request.get_json()

	history.append({"set-seed": data['name']})
	send_update()

	data = {"status": "success"}
	return data, 200

@app.route("/api/win/<string:team>", methods=['POST'])
def win(team):
	if not team.lower() in ["home", "away"]:
		data = {"status": "error"}
		return data, 500

	history.append({"set-win": team})
	send_update()

	data = {"status": "success"}
	return data, 200


if __name__ == '__main__':
	# app.run(host=conf.app_url, port=5005, debug=True, threaded=True)
	socketio.run(app, host=conf.app_url, port=5005, debug=True)