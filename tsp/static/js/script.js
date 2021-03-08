$(document).ready(function () {
	/*		load theme from cache, default dark		*/
	defaultTheme();
	/*		load toggle from storage				*/
	defaultToggle();
	/*			toggle theme on click				*/
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
	var toggleSetting = localStorage.getItem("toggle"); //for later
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

function defaultTheme() {
	var currentToggle = localStorage.getItem("theme");
	if (currentToggle == "light") { //change this parameter to set default
		setlight(); //
	} else {
		setdark();
	}
}

/*			These are theme elements			*/

function setlight() {
	var root = document.documentElement;
	root.style.setProperty('--main-bg-color', 'lightblue');
	root.style.setProperty('--toggle-button-color', 'white');
	root.style.setProperty('--toggle-button-text-color', 'black');
	root.style.setProperty('--second-bg-color', 'white');
	root.style.setProperty('--highlight-color', '#9cf');
	root.style.setProperty('--search-bar', 'white')
	root.style.setProperty('--main-text', 'black')
	root.style.setProperty('--info-text', '#4d5156')
	root.style.setProperty('--url-text', '#202124')
	root.style.setProperty('--title-text', 'black')
	root.style.setProperty('--title-text-hover', 'blue')
	root.style.setProperty('--title-text-visit', 'purple')
	root.style.setProperty('--padding-color', '#f1f5ff')
}

function setdark() {
	var root = document.documentElement;
	root.style.setProperty('--main-bg-color', '#36393f');
	root.style.setProperty('--toggle-button-color', '#1a1a1a');
	root.style.setProperty('--toggle-button-text-color', 'white');
	root.style.setProperty('--second-bg-color', '#36393f');
	root.style.setProperty('--highlight-color', '#737373');
	root.style.setProperty('--search-bar', '#1a1a1a')
	root.style.setProperty('--main-text', 'white')
	root.style.setProperty('--info-text', '#b4b6b9')
	root.style.setProperty('--url-text', 'white')
	root.style.setProperty('--title-text', 'white')
	root.style.setProperty('--title-text-hover', 'lightblue')
	root.style.setProperty('--title-text-visit', '#ffb9fe')
	root.style.setProperty('--padding-color', '#2a3547')

}
