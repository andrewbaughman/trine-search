$(document).ready(function () {
	/*		load theme from cache, default dark		*/
	defaultTheme();
	/*			toggle theme on click				*/
	$('.btn-toggle').on('click', function () {
		console.log('click');
		var currentTheme = localStorage.getItem("theme");
		if (currentTheme == 'light') {
			setdark();
			localStorage.setItem("theme", "dark");
		} else {
			setlight();
			localStorage.setItem("theme", "light");
		}
	});
	/*			search on click				*/
	$('#search_button').click(function () {
		search($('.query').val());
	});
});
/*			search on enter key			*/
$(document).keypress(function (event) {
	var keycode = (event.keyCode ? event.keyCode : event.which);
	if (keycode == '13') {
		search($('.query').val());
	}
});

function search(query) {
	if (query == '') {
		window.location = "/";
	} else {
		window.location = "/results/?query=" + encodeURIComponent(query);
	}
}

function defaultTheme() {
	var currentTheme = localStorage.getItem("theme");
	if (currentTheme == "light") { //change this parameter to set default
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
	root.style.setProperty('--main-bg-color', '#404040');
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
