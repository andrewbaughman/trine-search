/*      https://tutorialzine.com/2017/08/converting-from-speech-to-text-with-javascript     */
$(document).ready(function () {
	$('#home-mic-up').on('click', function(e) {
		$('#home-mic-up').find('img').css('border','2px solid lime');
		recognition.start();
	  });
	$('#home-mic-down').on('click', function(e) {
		$('#home-mic-up').find('img').css('border','2px solid transparent');
		recognition.stop();
	  });

});
try {
	var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
	var recognition = new SpeechRecognition();
}
catch(e) {
	console.error(e);
	$('#home-mic-up').hide();
	$('#home-mic-down').hide();
}
recognition.onstart = function() { 
	console.log('Speech start');
}
recognition.onspeechend = function() {
	console.log('Speech end');
}
  
recognition.onerror = function(event) {
    if(event.error == 'no-speech') {
        alert('No speech was detected. Try again, make sure microphone permissions are set.');  
    };
}
recognition.onresult = function(event) {
    var current = event.resultIndex;
    var transcript = event.results[current][0].transcript;
    $('#homeInput').val(transcript);
}