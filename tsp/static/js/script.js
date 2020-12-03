$(document).ready(function() {
    $('h1').click(function() {
        $(this).hide();
        console.log(search('whatever I want'));
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

			//Here's how to access it.
			$.each(response['results'], function(index, result){
				console.log(result['url']);
				console.log(result['description']);
			});
        }
    });
}