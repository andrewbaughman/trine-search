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

	$('#image_button').click(function () {
		page = "1"
		images($('.query').val(), page);
	});
});
/*			search on enter key			*/
$(document).keypress(function (event) {
	var keycode = (event.keyCode ? event.keyCode : event.which);
	if (keycode == '13') {
		page = "1"
		if (window.location.toString().includes("/images/?query")) {
			images($('.query').val(), page);
		}
		else {
			search($('.query').val(), $('.query').attr('isTrine'), page);
		}

	}
});

function search(query, isTrine, page) {
	if (query == '') {
		window.location = "/";
	} else if (isTrine == 'false') {
		window.location = "/results/?query=" + encodeURIComponent(query) + "&page=" + page + "&isTrine=False";
	} else if (isTrine == 'true') {
		window.location = "/results/?query=" + encodeURIComponent(query) + "&page=" + page + "&isTrine=True";
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
