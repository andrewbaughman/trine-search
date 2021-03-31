$(document).ready(function () {
	/*		load toggle from storage				*/
	defaultToggle();	 
	$('.trine-toggle').on('change', function () {
		//var current = $('#homeInpput').attr('placeholder');
		if ($(".trine-toggle").find('input').is(':checked')) {
			$('.query').attr('placeholder', 'Search Trine resources...');
			$('.query').attr('isTrine', 'True');
			localStorage.setItem("isTrine", "True");
		} else {
			$('.query').attr('placeholder', 'Search All resources...');
			$('.query').attr('isTrine', 'false');
			localStorage.setItem("isTrine", "false");
		}
	});
	/*			search on click				*/
	$('#search_button').click(function () {
		search($('.query').val(), $('.query').attr('isTrine'), '1');
	});

	$('#image_button').click(function () {
		images($('.query').val(), '1');
	});
});
/*			search on enter key			*/
$(document).keypress(function (event) {
	var keycode = (event.keyCode ? event.keyCode : event.which);
	if (keycode == '13') {
		if (window.location.toString().includes("/images/?query")) {
			images($('.query').val(), '1');
		}
		else {
			search($('.query').val(), $('.query').attr('isTrine'), '1');
		}

	}
});

function search(query, isTrine, page) {
	if (query == '') {
		window.location = "/";
	} else {
		window.location = "/results/?query=" + encodeURIComponent(query) + "&page=" + page + "&isTrine=" + isTrine;
	}
}

function images(query, page) {
	if (query == '') {
		window.location = "/images/?query=trine&page=1"
	}
	else{
		window.location = "/images/?query=" + encodeURIComponent(query) + "&page=" + page;
	}
}

function defaultToggle() {
	var currentToggle = localStorage.getItem("isTrine");
	if (currentToggle == "True") {
		$(".trine-toggle").find('input').attr('checked', 'checked');
		$('.query').attr('placeholder', 'Search Trine resources...');
		$('.query').attr('isTrine', 'True');
	} else {
		$(".trine-toggle").find('input').removeAttr('checked', 'checked');
		$('.query').attr('placeholder', 'Search All resources...');
		$('.query').attr('isTrine', 'False');
		localStorage.setItem("isTrine", "False");
	}
}
