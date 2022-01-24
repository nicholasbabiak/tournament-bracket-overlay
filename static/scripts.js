$(document).ready(() =>{
	var socket = io();
	// Connect Socket
	socket.on('connect', () => {
		console.log('Socket connected');
	});

	socket.on('update', (response) => {
		console.log('Socket recieved: ' + response);
		let data = JSON.parse(response);

		// Save seed names
		for (let index = 0; index < data['seed_names'].length; index++) {
			$('.seed' + index + ":first").html(data['seed_names'][index]);
		}

		let bracket = data['bracket']
		let names = data['seed_names']
		let found_current = false;
		// If game state received
		if (names.length == 4 && bracket != []) {
			// Loop through games
			for (let index = 0; index < bracket.length; index++) {
				let game = index + 1;

				// Looking for current game to add highlight
				if ((
						bracket[index]['win'] == null &&
						!found_current &&
						index != 6
					) || (
						// Adds logic for game 7
						//	(Only play game 7 if winner of game 3 loses game 6)
						index == 6 &&
						bracket[index]['win'] == null &&
						!found_current &&
						bracket[index]['away'] != null
					)) {
					$('#g-' + game).removeClass("d-none");
					found_current = true;
				}
				else {
					$('#g-' + game).addClass("d-none");
				}

				// Show name on bracket
				$(`#g-${game}-h`).html(
					names[bracket[index]['home']] == undefined ? "" : names[bracket[index]['home']]
					);
				$(`#g-${game}-a`).html(
					names[bracket[index]['away']] == undefined ? "" : names[bracket[index]['away']]
					);
			}
		}
		// Cleans bracket on reset
		else {
			// Shows "Seed x?""
			for (let index = 0; index < 4; index++) {
				if (index >= data['seed_names'].length || data['seed_names'].length == 0 ){
					$('.seed' + index +':first').html("Seed " + (index + 1) + "?");
				}
			}

			// Removes all highlights
			$('.highlight').each((i, v) => {
				$(v).addClass("d-none");
			});

			// Clears all name tags
			for (let game = 3; game < 9; game++) {
				$(`#g-${game}-h`).html("");
				$(`#g-${game}-a`).html("");
			}
		}
	});


});