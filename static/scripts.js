$(document).ready(() =>{
	var socket = io();
	socket.on('connect', () => {
		// socket.emit('my event', {data: 'I\'m connected!'});
		console.log('Socket connected');
	});


	socket.on('update', (data) => {
		// socket.emit('my event', {data: 'I\'m connected!'});
		console.log('Socket recieved: ' + data);
	});


});