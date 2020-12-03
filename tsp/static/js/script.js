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
            console.log(response);
        }
    });
}