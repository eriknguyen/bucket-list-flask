$(function() {
    /*add jQuery POST request with ajax for Sign Up button*/
    $('#btnSignUp').click(function () {
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});