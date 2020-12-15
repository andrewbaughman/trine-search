$(document).ready(function() {
    $('#search_button').click(function() {
		search($('#resultsInput').val());
    });
});

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