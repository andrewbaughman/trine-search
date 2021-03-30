$(document).ready(function () {
	/*		load toggle from storage				*/
	defaultToggle();	 
	$('.trine-toggle').on('change', function () {
		//var current = $('#homeInpput').attr('placeholder');
		if ($(".trine-toggle").find('input').is(':checked')) {
			$('.query').attr('placeholder', 'Search Trine resources...');
			$('.query').attr('isTrine', 'true');
			localStorage.setItem("isTrine", "true");
		} else {
			$('.query').attr('placeholder', 'Search All resources...');
			$('.query').attr('isTrine', 'false');
			localStorage.setItem("isTrine", "false");
		}
	});
	/*			search on click				*/
	$('#search_button').click(function () {
		page = "1"
		search($('.query').val(), $('.query').attr('isTrine'), page);
	});
});
/*			search on enter key			*/
$(document).keypress(function (event) {
	var keycode = (event.keyCode ? event.keyCode : event.which);
	if (keycode == '13') {
		page = "1"
		search($('.query').val(), $('.query').attr('isTrine'), page);
	}
});

function search(query, isTrine, page) {
	if (query == '') {
		window.location = "/";
	} else if (isTrine == 'false') {
		window.location = "/results/?query=" + encodeURIComponent(query) + "&page=" + page;
	} else if (isTrine == 'true') {
		window.location = "/trine-results/?query=" + encodeURIComponent(query) + "&page=" + page;
	}
}

function defaultToggle() {
	var currentToggle = localStorage.getItem("isTrine");
	if (currentToggle == "true") {
		$(".trine-toggle").find('input').attr('checked', 'checked');
		$('.query').attr('placeholder', 'Search Trine resources...');
		$('.query').attr('isTrine', 'true');
	} else {
		$(".trine-toggle").find('input').removeAttr('checked', 'checked');
		$('.query').attr('placeholder', 'Search All resources...');
		$('.query').attr('isTrine', 'false');
		localStorage.setItem("isTrine", "false");
	}
}
