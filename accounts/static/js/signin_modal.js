$(document).ready(function(){
    if ($('#signin-logo')) {
        $('#signin-logo').on('click', function(){
            if ($(this).data('user') == 'anonymous') {
                $('#signin-form').modal('show');
            }
            else {
                window.location.replace(location.origin + '/account/' + $(this).data('user'));
            }
        })
    }
    if ($('#signin-logo-mob')) {
        $('#signin-logo-mob').on('click', function(){
            if ($(this).data('user') == 'anonymous') {
                $('#signin-form').modal('show');
            }
            else {
                window.location.replace(location.origin + '/account/' + $(this).data('user'));
            }
        })
    }
})