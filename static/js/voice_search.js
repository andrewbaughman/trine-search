/*      https://tutorialzine.com/2017/08/converting-from-speech-to-text-with-javascript     */
/*      https://stackoverflow.com/a/4565120	for isChrome check							    */
/*      https://stackoverflow.com/a/31511072 for mq.matches check							*/

var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
if (isChrome.toString() !== 'true') {
	$(document).ready(function () {
		const mq = window.matchMedia( "(min-width: 800px)" );
		//console.log("is chrome: " + isChrome.toString());
		$('.search-button-container').find('.voice-button-container').remove();
		// if(mq.matches){	//not chrome not responsive --no buttons
		// 	$('.search-button-container').css('grid-template-columns', '2fr 1fr');
		// 	$('.search-button-container').css('grid-template-rows', 'unset');
		// }
		// else {			//not chrome and responsive --no buttons
		// 	$('.search-button-container').css('grid-template-rows', '1fr 1fr');
		// 	$('.search-button-container').css('grid-template-columns', 'unset');

		// }
	});
} else {
	$(document).ready(function () {
		const mq = window.matchMedia("(min-width: 800px)");
		// if(mq.matches){	//chrome not responsive --yes buttons
		// 	$('.search-button-container').css('grid-template-rows', 'unset');
		// }
		// else {			//chrome and responsive --yes buttons
		// 	$('.search-button-container').css('grid-template-columns', 'unset');

		// }
		$('#home-mic-up').on('click', function (e) {
			image = document.getElementById('voiceimage');
			if (image.src.includes('mic.svg')){
				image.src = image.src.replace('mic.svg', 'mic-up.svg');
				recognition.start();
			} else if (image.src.includes('mic-up.svg')){
				image.src = image.src.replace('mic-up.svg', 'mic.svg');
				recognition.stop();
			}
     		
		});
	});


	var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
	var recognition = new SpeechRecognition();


	recognition.onstart = function () {
		console.log('Speech start');
	}
	recognition.onspeechend = function () {
		console.log('Speech end');
	}

	recognition.onerror = function (event) {
		if (event.error == 'no-speech') {
			alert('No speech was detected. Try again, make sure microphone permissions are set.');
		};
	}
	recognition.onresult = function (event) {
		var current = event.resultIndex;
		var transcript = event.results[current][0].transcript;
		if ($('#homeInput')) {
			$('#homeInput').val(transcript);
		voiceSearch();
		}
		if ($('#resultsInput')) {
			$('#resultsInput').val(transcript);
		voiceSearch();
		}
	}
	
	function voiceSearch() {
		query = $('.query').val()
		isTrine = $('.query').attr('isTrine')
		if (query == '') {
			window.location = "/";
		} else {
			window.location = "/results/?query=" + encodeURIComponent(query) + "&isTrine=" + isTrine + "&page=1";
		}
	}
}