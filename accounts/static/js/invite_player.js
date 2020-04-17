function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Check if this cookie string begin with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
             }
         }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

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

function ChangeTeam(e) {
    var id_num = e.target.id.split('-')[e.target.id.split('-').length - 1];
    $('#modal-teams-' + id_num).modal('show');
    $('#accept-team-' + id_num).on('click', function(){
        let source_team = $('#current-team-' + id_num).data('target');
        let target_team = $('#choose-team-' + id_num).find(':selected').data('target');
        let csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();
        var data = {source_team, target_team, csrfmiddlewaretoken};

        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            url: '/ajax/change_team/',
            type: 'POST',
            data: data,
            success: function(response) {
                $('#modal-teams-' + id_num).modal('hide');
                location.reload();
            },
            error: function(response) {
                alert('Something went wrong, try again later');
            }
        })
    })
    $('#decline-team-' + id_num).on('click', function(){
        $('#modal-teams-' + id_num).modal('hide');
    })
}

function AnswerBid(e) {
    let bid = $('#' + e.target.id).data('target');
    if (e.target.name.includes('accept')) {
       var answer = 'accept';
    }
    else if (e.target.name.includes('decline')) {
        var answer = 'decline';
    }
    var data = {bid, answer};
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        url: '/ajax/change_team/',
        type: 'POST',
        data: data,
        success: function(response) {
            location.reload();
        },
        error: function(response) {
            alert('Something went wrong, try again later');
        }
    })
}

$(document).ready(function(){
    $('#invite-btn-pg').on('click', Invitation);

    for (i = 0; i < $('.current-team').length; i++) {
        $('.current-team')[i].addEventListener('click', ChangeTeam);
    }

    for (i = 0; i < document.getElementsByName('accept-bid-btn').length; i++) {
        document.getElementsByName('accept-bid-btn')[i].addEventListener('click', AnswerBid);
    }
    for (i = 0; i < document.getElementsByName('decline-bid-btn').length; i++) {
        document.getElementsByName('decline-bid-btn')[i].addEventListener('click', AnswerBid);
    }
})