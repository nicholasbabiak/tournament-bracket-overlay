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

# Helper function that only looks at active history and gets name count
def get_name_count():
	starting_point = max(loc for loc, val in enumerate(history) if val == "reset")
	working_history = history[starting_point:]
	count = 0
	for obj in working_history:
		if 'set-seed' in obj:
			count += 1

	return count

# Sends current state to the client
def send_update():
	seed_names = []
	bracket = []

	# Gets current history
	starting_point = max(loc for loc, val in enumerate(history) if val == "reset")

	working_history = history[starting_point:]
	print(working_history)

	# Records names
	for obj in working_history:
		if 'set-seed' in obj:
			seed_names.append(obj['set-seed'])

	# Creates empty game object
	if len(seed_names) == 4:
		bracket = [
			{
				"home": 0,
				"away": 3,
				"win": None
			},
			{
				"home": 1,
				"away": 2,
				"win": None
			},
			{
				"home": None,
				"away": None,
				"win": None
			},
			{
				"home": None,
				"away": None,
				"win": None
			},
			{
				"home": None,
				"away": None,
				"win": None
			},
			{
				"home": None,
				"away": None,
				"win": None
			},
			{
				"home": None,
				"away": None,
				"win": None
			},
			{
				"home": None,
				"away": None,
				"win": None
			}
		]

		# Helper dictionary to map progression through bracket
		win_home_path = dict([(0, 2), (2, 5), (5, 6), (6, 7)])
		win_away_path = dict([(1, 2), (3, 4), (4, 5)])
		lose_home_path = dict([(0, 3), (2, 4)])
		lose_away_path = dict([(1, 3), (5, 6)])

		# Loops through games to populate bracket
		for obj in working_history:
			# Sets winner in current match
			if 'set-win' in obj:
				# Loops through bracket to find the next unplayed game
				for index in range(len(bracket)):
					if not bracket[index]['win']:
						# Sets the winner
						bracket[index]['win'] = obj['set-win']

						# If the winner has another game finds out which "home" or "away" game they need to be added to
						if index in win_home_path:
							bracket[win_home_path[index]]['home'] = bracket[index][obj['set-win']]
						elif index in win_away_path:
							bracket[win_away_path[index]]['away'] = bracket[index][obj['set-win']]

						# Handles game 7 exception where if on the 6 game the winner of the 3 game has lost once there
						# 	is another game other wise they win the tournament
						if index == 5 and obj['set-win'] == 'home':
							break

						# If the lower has another game finds out where it is and add them to it
						lose = 'home' if obj['set-win'] == 'away' else 'away'
						if index in lose_home_path:
							bracket[lose_home_path[index]]['home'] = bracket[index][lose]
						elif index in lose_away_path:
							bracket[lose_away_path[index]]['away'] = bracket[index][lose]

						break

	# Sends game state to client
	socketio.emit("update", json.dumps({
		'seed_names': seed_names,
		'bracket': bracket
	}))

# When a client connects send them the current state (Helpful for disconnects)
@socketio.on('connect')
def test_connect(auth):
	send_update()

# Resets the current game to the start (None distructive since the back can reverse)
@app.route("/api/reset", methods=['POST'])
def reset():
	history.append("reset")
	send_update()

	data = {"status": "success"}
	return data, 200

# Reverse the last action in the game. Includes (win/set-seed/ reset)
@app.route("/api/back", methods=['POST'])
def back():
	history.pop()
	send_update()

	data = {"status": "success"}
	return data, 200

# Sets a name to the next avalable seed
@app.route("/api/set-seed", methods=['POST'])
def set_seed():
	data = request.get_json()

	if get_name_count() == 4:
		data = {"status": "error", "Message": "All names already set"}
		return data, 500

	history.append({"set-seed": data['name']})
	send_update()

	data = {"status": "success"}
	return data, 200

# Sets the winner for the current game
@app.route("/api/win/<string:team>", methods=['POST'])
def win(team):
	if not team.lower() in ["home", "away"]:
		data = {"status": "error", "Message": "Invalid input use <Home/Away>"}
		return data, 500

	if get_name_count() < 4:
		data = {"status": "error", "Message": "All names not set yet"}
		return data, 500

	history.append({"set-win": team})
	send_update()

	data = {"status": "success"}
	return data, 200


if __name__ == '__main__':
	socketio.run(app, host=conf.app_url, port=5005, debug=True)