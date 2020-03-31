function Invitation(e) {
    console.log(e.target);
    $.ajax({
        url: '/ajax/invite/',
        type: 'GET',
        success: function(response) {
            console.log(response);
            let mes = 'Your invitation url: <a class="nav-link" href="$">$</a>';
            mes = mes.replace('$', window.location.origin + '/registration/?key=' + response['key']);
            mes = mes.replace('$', window.location.origin + '/registration/?key=' + response['key']);
            $('#invite-mes-label').html(mes);
            $('#invite-mes-label').css('color', '#00ff00');
            $('#invite-mes-label').css('display', 'block');
        },
        error: function(response) {
            console.log(response);
            $('#invite-mes-label').text('Something went wrong, please try later');
            $('#invite-mes-label').css('display', 'block');
        }
    });
}

$(document).ready(function(){
    $('#invite-btn-pg').on('click', Invitation);
})