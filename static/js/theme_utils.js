/*			These are theme defaults			*/
var default_main_bg_color = '#36393f';
var default_main_button_color = '#36393f';
var default_toggle_button_color = '#1a1a1a';
var default_toggle_button_text_color = '#ffffff';
var default_second_bg_color = '#36393f';
var default_highlight_color = '#737373';
var default_search_bar = '#1a1a1a';
var default_main_text = '#ffffff';
var default_info_text = '#b4b6b9';
var default_url_text = '#ffffff';
var default_title_text = '#ffffff';
var default_title_text_hover = '#add8e6';
var default_title_text_visit = '#ffb9fe';
var default_padding_color = '#404f60';

$(document).ready(function () {
	/*			 Theme				*/
	get_theme_or_defaults()
	/*			 widgets			*/
	$("#color-picker-widget").dialog({
		modal: true,
		position: { my: "center", at: "center", of: 'body' }, 
		autoOpen: false,
	});
	$(".btn-toggle").click(function () {
		$("#color-picker-widget").dialog("open");
	});
	/*			 icons				*/
	$("#reset-button").click(function () {
		reset_colors();
	});
	$("#light-button").click(function () {
		setlight();
	});
	$("#dark-button").click(function () {
		setdark();
	});
	$("#save-button").click(function () {
		update_colors();
		$("#color-picker-widget").dialog("close");
	});
	$('.scroll-top').on('click', function () {
		scrollTopAnimated();
	});
});


/*			These are theme presets			*/
function setlight() {
	var main_bg_color = '#add8e6';
	var toggle_button_color = '#99ccff';
	var toggle_button_text_color = '#000000';
	var second_bg_color = '#ffffff';
	var highlight_color = '#99ccff';
	var search_bar = '#ffffff';
	var main_text = '#000000';
	var info_text = '#4d5156';
	var url_text = '#202124';
	var title_text = '#000000';
	var title_text_hover = '#0000ff';
	var title_text_visit = '#800080';
	var padding_color = '#f1f5ff';
	$('#main-background-color-input').val(trim_lowercase_text(main_bg_color));
	$('#toggle-button-color-input').val(trim_lowercase_text(toggle_button_color));
	$('#toggle-button-text-color-input').val(trim_lowercase_text(toggle_button_text_color));
	$('#second-background-color-input').val(trim_lowercase_text(second_bg_color));
	$('#highlight-color-input').val(trim_lowercase_text(highlight_color));
	$('#search-bar-color-input').val(trim_lowercase_text(search_bar));
	$('#main-text-color-input').val(trim_lowercase_text(main_text));
	$('#info-text-color-input').val(trim_lowercase_text(info_text));
	$('#url-text-color-input').val(trim_lowercase_text(url_text));
	$('#title-text-color-input').val(trim_lowercase_text(title_text));
	$('#title-text-hover-color-input').val(trim_lowercase_text(title_text_hover));
	$('#title-text-visited-color-input').val(trim_lowercase_text(title_text_visit));
	$('#padding-color-input').val(trim_lowercase_text(padding_color));
}

function setdark() {
	var main_bg_color = default_main_bg_color;
	var main_button_color = default_main_button_color;
	var toggle_button_color = default_toggle_button_color;
	var toggle_button_text_color = default_toggle_button_text_color;
	var second_bg_color = default_second_bg_color;
	var highlight_color = default_highlight_color;
	var search_bar = default_search_bar;
	var main_text = default_main_text;
	var info_text = default_info_text;
	var url_text = default_url_text;
	var title_text = default_title_text;
	var title_text_hover = default_title_text_hover;
	var title_text_visit = default_title_text_visit;
	var padding_color = default_padding_color;
	$('#main-background-color-input').val(trim_lowercase_text(main_bg_color));
	$('#toggle-button-color-input').val(trim_lowercase_text(toggle_button_color));
	$('#toggle-button-text-color-input').val(trim_lowercase_text(toggle_button_text_color));
	$('#second-background-color-input').val(trim_lowercase_text(second_bg_color));
	$('#highlight-color-input').val(trim_lowercase_text(highlight_color));
	$('#search-bar-color-input').val(trim_lowercase_text(search_bar));
	$('#main-text-color-input').val(trim_lowercase_text(main_text));
	$('#info-text-color-input').val(trim_lowercase_text(info_text));
	$('#url-text-color-input').val(trim_lowercase_text(url_text));
	$('#title-text-color-input').val(trim_lowercase_text(title_text));
	$('#title-text-hover-color-input').val(trim_lowercase_text(title_text_hover));
	$('#title-text-visited-color-input').val(trim_lowercase_text(title_text_visit));
	$('#padding-color-input').val(trim_lowercase_text(padding_color));
}

function get_theme_or_defaults() {
	//retrieve elements from storage
	var main_bg_color = localStorage.getItem("--main-bg-color");
	var toggle_button_color = localStorage.getItem("--toggle-button-color");
	var toggle_button_text_color = localStorage.getItem("--toggle-button-text-color");
	var second_bg_color = localStorage.getItem("--second-bg-color");
	var highlight_color = localStorage.getItem("--highlight-color");
	var search_bar = localStorage.getItem("--search-bar");
	var main_text = localStorage.getItem("--main-text");
	var info_text = localStorage.getItem("--info-text");
	var url_text = localStorage.getItem("--url-text");
	var title_text = localStorage.getItem("--title-text");
	var title_text_hover = localStorage.getItem("--title-text-hover");
	var title_text_visit = localStorage.getItem("--title-text-visit");
	var padding_color = localStorage.getItem("--padding-color");
	//if retrieved value is nothing, set to default, else apply retrieved 
	if ((main_bg_color == '') || (main_bg_color == null)) {
		main_bg_color = default_main_bg_color;
	}
	if ((toggle_button_color == '') || (toggle_button_color == null)) {
		toggle_button_color = default_toggle_button_color;
	}
	if ((toggle_button_text_color == '') || (toggle_button_text_color == null)) {
		toggle_button_text_color = default_toggle_button_text_color;
	}
	if ((second_bg_color == '') || (second_bg_color == null)) {
		second_bg_color = default_second_bg_color;
	}
	if ((highlight_color == '') || (highlight_color == null)) {
		highlight_color = default_highlight_color;
	}
	if ((search_bar == '') || (search_bar == null)) {
		search_bar = default_search_bar;
	}
	if ((main_text == '') || (main_text == null)) {
		main_text = default_main_text;
	}
	if ((info_text == '') || (info_text == null)) {
		info_text = default_info_text;
	}
	if ((url_text == '') || (url_text == null)) {
		url_text = default_url_text;
	}
	if ((title_text == '') || (title_text == null)) {
		title_text = default_title_text;
	}
	if ((title_text_hover == '') || (title_text_hover == null)) {
		title_text_hover = default_title_text_hover;
	}
	if ((title_text_visit == '') || (title_text_visit == null)) {
		title_text_visit = default_title_text_visit;
	}
	if ((padding_color == '') || (padding_color == null)) {
		padding_color = default_padding_color;
	}

	//apply colors to site
	var root = document.documentElement;
	root.style.setProperty("--main-bg-color", main_bg_color);
	root.style.setProperty("--toggle-button-color", toggle_button_color);
	root.style.setProperty("--toggle-button-text-color", toggle_button_text_color);
	root.style.setProperty("--second-bg-color", second_bg_color);
	root.style.setProperty("--highlight-color", highlight_color);
	root.style.setProperty("--search-bar", search_bar);
	root.style.setProperty("--main-text", main_text);
	root.style.setProperty("--info-text", info_text);
	root.style.setProperty("--url-text", url_text);
	root.style.setProperty("--title-text", title_text);
	root.style.setProperty("--title-text-hover", title_text_hover);
	root.style.setProperty("--title-text-visit", title_text_visit);
	root.style.setProperty("--padding-color", padding_color);

	//set defaults to switcher
	$('#main-background-color-input').val(trim_lowercase_text(main_bg_color));
	$('#toggle-button-color-input').val(trim_lowercase_text(toggle_button_color));
	$('#toggle-button-text-color-input').val(trim_lowercase_text(toggle_button_text_color));
	$('#second-background-color-input').val(trim_lowercase_text(second_bg_color));
	$('#highlight-color-input').val(trim_lowercase_text(highlight_color));
	$('#search-bar-color-input').val(trim_lowercase_text(search_bar));
	$('#main-text-color-input').val(trim_lowercase_text(main_text));
	$('#info-text-color-input').val(trim_lowercase_text(info_text));
	$('#url-text-color-input').val(trim_lowercase_text(url_text));
	$('#title-text-color-input').val(trim_lowercase_text(title_text));
	$('#title-text-hover-color-input').val(trim_lowercase_text(title_text_hover));
	$('#title-text-visited-color-input').val(trim_lowercase_text(title_text_visit));
	$('#padding-color-input').val(trim_lowercase_text(padding_color));
}

function update_colors() {
	//get from widget
	var main_bg_color = $('#main-background-color-input').val();
	var toggle_button_color = $('#toggle-button-color-input').val();
	var toggle_button_text_color = $('#toggle-button-text-color-input').val();
	var second_bg_color = $('#second-background-color-input').val();
	var highlight_color = $('#highlight-color-input').val();
	var search_bar = $('#search-bar-color-input').val();
	var main_text = $('#main-text-color-input').val();
	var info_text = $('#info-text-color-input').val();
	var url_text = $('#url-text-color-input').val();
	var title_text = $('#title-text-color-input').val();
	var title_text_hover = $('#title-text-hover-color-input').val();
	var title_text_visit = $('#title-text-visited-color-input').val();
	var padding_color = $('#padding-color-input').val();
	localStorage.setItem("--main-bg-color", main_bg_color);
	localStorage.setItem("--toggle-button-color", toggle_button_color);
	localStorage.setItem("--toggle-button-text-color", toggle_button_text_color);
	localStorage.setItem("--second-bg-color", second_bg_color);
	localStorage.setItem("--highlight-color", highlight_color);
	localStorage.setItem("--search-bar", search_bar);
	localStorage.setItem("--main-text", main_text);
	localStorage.setItem("--info-text", info_text);
	localStorage.setItem("--url-text", url_text);
	localStorage.setItem("--title-text", title_text);
	localStorage.setItem("--title-text-hover", title_text_hover);
	localStorage.setItem("--title-text-visit", title_text_visit);
	localStorage.setItem("--padding-color", padding_color);
	//apply to site
	get_theme_or_defaults();
}

function reset_colors() {
	//set storage to default values, apply to page
	localStorage.removeItem('--main-bg-color');
	localStorage.removeItem('--toggle-button-color');
	localStorage.removeItem('--toggle-button-text-color');
	localStorage.removeItem('--second-bg-color');
	localStorage.removeItem('--highlight-color');
	localStorage.removeItem('--search-bar');
	localStorage.removeItem('--main-text');
	localStorage.removeItem('--info-text');
	localStorage.removeItem('--url-text');
	localStorage.removeItem('--title-text');
	localStorage.removeItem('--title-text-hover');
	localStorage.removeItem('--title-text-visit');
	localStorage.removeItem('--padding-color');
	get_theme_or_defaults();
}

function scrollTopAnimated() {
	$("html, body").animate({
		scrollTop: "0"
	}, 10);
}

function trim_lowercase_text(sample) {
	//for setting value of color input, it has to be trimmed and lowercase
	sample = sample.toString();
	sample = sample.trim();
	sample = sample.toLowerCase();
	return sample;
}