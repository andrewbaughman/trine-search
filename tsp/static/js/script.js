$(document).ready(function() {
    $('#search_button').click(function() {
		if ($('.query').val() == '') {
			window.location = "/";
		} else {
			window.location = "/results/"+ $('.query').val() +"/";
		}
    });
});

$(document).keypress(function(event) {
	var keycode = (event.keyCode ? event.keyCode : event.which);
	if (keycode == '13') {
		search($('.query').val());
	}
});


function search(query) {
	if (query == '') {
		window.location = "/";
	} else {
		window.location = "/results/"+ query +"/";
	}
}


//No longer used, but left here as an example.
function search(query){
    $.ajax({
        type: 'GET',
        data: {
            'query': query,
        },
        url: '/search/',
        success: function(response) {
			//This is what the response actually looks like.
			console.log(response);
			$(document).find('.results').html("");
			$.each(response['results'], function(index, result){
				$(document).find('.results').html($(document).find('.results').html()
				+"<div class='result'>"
				+	"<tr>"
				+		"<url><td>"+ result['url'] +"</td></url>"
				+		"<td><a href= "+ result['url'] +"><title-result></br>"+ result['title'] +"</td></title-result></a>"
				+		"<td></br><info><td>"+ result['description'] +"</td></info>"
				+"</div>");
			});
        }
    });
}
