/*      https://tutorialzine.com/2017/08/converting-from-speech-to-text-with-javascript     */
var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
if (isChrome.toString() !== 'true') {
	$(document).ready(function () {
		const mq = window.matchMedia( "(min-width: 800px)" );
		console.log(mq.matches);
		console.log("is chrome: " + isChrome.toString());
		$('.search-button-container').find('.voice-button-container').remove();
		if(mq.matches){	//not chrome and responsive --no buttons
			$('.search-button-container').css('grid-template-columns', '2fr 1fr');
			$('.search-button-container').css('grid-template-rows', 'unset');
		}
		else {			//not chrome not responsive --no buttons
			$('.search-button-container').css('grid-template-rows', '1fr 1fr');
			$('.search-button-container').css('grid-template-columns', 'unset');

		}
	});
} else {
	$(document).ready(function () {
		const mq = window.matchMedia("(min-width: 800px)");
		console.log(mq.matches);
		if(mq.matches){	//chrome and responsive --yes buttons
			$('.search-button-container').css('grid-template-columns', '1fr 1fr 1fr');
			$('.search-button-container').css('grid-template-rows', 'unset');
		}
		else {			//chrome not responsive --yes buttons
			$('.search-button-container').css('grid-template-rows', '1fr 1fr 1fr');
			$('.search-button-container').css('grid-template-columns', 'unset');

		}
		$('#home-mic-up').on('click', function (e) {
			$('#home-mic-up').find('img').css('border', '2px solid lime');
			recognition.start();
		});
		$('#home-mic-down').on('click', function (e) {
			$('#home-mic-up').find('img').css('border', '2px solid transparent');
			recognition.stop();
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
		$('#homeInput').val(transcript);
	}
}