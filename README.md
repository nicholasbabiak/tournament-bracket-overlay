# tournament-bracket-overlay
Web based live stream overlay for a tournament


# Install
1. Create config.py in the root of the application  with
```
class Config():
	def __init__(self):
		self.app_url = "<<SERVER IP ADDRESS>>"
		self.secret_key = "<<SECRET STRING>>"
```
2. Run `pip install flask`
3. Run `pip install flask-socketio`
4. To start the application run `python run.py`
5. Navigate to app on `http://<<SERVER ADDRESS IP>>:5005`

# Usage
This is a small application that can host a 4 person double elimination bracket. The server only use
a single global history object in the python file so all clients that connect will get the same game. This makes the
application only useful for single client to server use. This is helpful for a small tournament but very specialized.

To control the bracket, you send web request to the server. I designed it so that it can be paired with
[Bitfocus Companion](https://bitfocus.io/companion/) so that with only 8 buttons:
 * set-seed
   * Times 4
 * Reset
   * Think Clear
 * Back
   * Think `CTR + Z`
 * Home Win
 * Away Win

A whole bracket can be run allowing a small live stream tournament to have an easy bracket overlay.

The other usage that this application was designed was to add the client URL to an [OBS ](https://obsproject.com) browser
source. Allowing the bracket to be used as an overlay. If you set the Width to `1920` and with Height to `1080` the scaling
will be captured correctly.

> Note: To prevent editing of the source when you add the browser source adding the following CSS will set the background
color to be transparent so different background/video can show through. `#app-base {background-color: transparent;}`

# Control
These commands can be run from anything that can send an HTTP request such as
[Bitfocus Companion](https://bitfocus.io/companion/) or [Insomnia](https://insomnia.rest/) or even as a
[curl](https://curl.se/) command as shown below.
```
URL BASE = http://<<SERVER IP ADDRESS>:5005
```
## Set Seed:
```
curl --request POST \
  --url <<URL BASE>>/api/set-seed \
  --header 'Content-Type: application/json' \
  --data '{"name": "<<NAME>>"}'
```
## Reset
```
curl --request POST \
  --url <<URL BASE>>/api/reset
```
## Back
```
curl --request POST \
  --url <<URL BASE>>/api/back
```
## Home/Away Win
```
curl --request POST \
  --url <<URL BASE>>/api/win/<<home/away>>
```

# Philosophy
* This is not a responsive web application.
* This will only work with on client (or multiple clients with the same output) for one server
* This application only can do a [double elimination bracket](https://en.wikipedia.org/wiki/Double-elimination_tournament)
for 4 team/people
* The styling is bright, so it contrasted better with a dark backdrop
* In this application and the control "Home" is the team on the top leg of the game while "Away" is the team on the bottom
leg.
* In the HTML file the first game in designated with `g-1` but in the python and JavaScript the first game is at the 0 index
since lists were used.