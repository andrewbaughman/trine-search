$(document).ready(function() {
    $('h1').click(function() {
        $(this).hide();
        console.log(testAjax());
    });
});

function testAjax(){
    $.ajax({
        type: 'GET',
        url: '/testAjax/',
        success: function(response) {
            console.log(response);
        }
    });
}