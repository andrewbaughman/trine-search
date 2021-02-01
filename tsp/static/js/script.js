$(document).ready(function() {
    $('#search_button').click(function() {
		search($('.query').val());
    });
});

$(document).keypress(function(event) {
	var keycode = (event.keyCode ? event.keyCode : event.which);
	if (keycode == '13') {
		search($('.query').val());
	}
});


function search(query) {
	if (query == '') {
		window.location = "/";
	} else {
		window.location = "/results/"+ query +"/";
	}
}
