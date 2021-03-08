$(document).ready(function () {
	/*		load toggle from storage				*/
	defaultToggle();
	/*			toggle theme on click				*/
	/*
	$('.btn-toggle').on('click', function () {
		var currentTheme = localStorage.getItem("theme");
		if (currentTheme == 'light') {
			setdark();
			localStorage.setItem("theme", "dark");
		} else {
			setlight();
			localStorage.setItem("theme", "light");
		}
	});
	*/
	//$('.query').attr('isTrine', 'false');
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
		search($('.query').val(), $('.query').attr('isTrine'));
	});
});
/*			search on enter key			*/
$(document).keypress(function (event) {
	var keycode = (event.keyCode ? event.keyCode : event.which);
	if (keycode == '13') {
		search($('.query').val(), $('.query').attr('isTrine'));
	}
});

function search(query, isTrine) {
	if (query == '') {
		window.location = "/";
	} else if (isTrine == 'false') {
		window.location = "/results/?query=" + encodeURIComponent(query);
	} else if (isTrine == 'true') {
		window.location = "/trine-results/?query=" + encodeURIComponent(query);
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


