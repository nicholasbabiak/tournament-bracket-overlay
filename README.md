# tournament-bracket-overlay
Web based live stream overlay for a tournament


# Install
1. Create config.py in the root of the apption with
```
class Config():
	def __init__(self):
		self.app_url = "<<SERVER IP ADDRESS>>"
		self.secret_key = "<<SECRET STRING>>"
```
2. Run `pip install flask`
3. Run `pip install flask-socketio`
4. To start the application run `python run.py`