$(document).ready(function(){
    $('#signin-logo').on('click', function(){
        if ($(this).data('user') == 'anonymous') {
            $('#signin-form').modal('show');
        }
        else {
            window.location.replace(location.origin + '/account/' + $(this).data('user'));
        }
    })
})