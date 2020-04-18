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

function SendBid(e) {
    let activity = 'save';
    if (e.target.name.includes('send')) {
        activity = 'send';
    }
    let bid = $('#' + e.target.id).data('bid');
    let championat = $('#' + e.target.id).data('championat');
    let team = $('#' + e.target.id).data('team');

    var players = [];
    for (i = 1; i < $('#bid-table-' + team)[0].rows.length; i++) {
        let player_id = $($('#bid-table-' + team)[0].rows[i]).data('player');
        if (!$('#checkbox-' + team + '-' + player_id)[0].hasAttribute('checked') && $('#checkbox-' + team + '-' + player_id)[0].checked ||
            $('#checkbox-' + team + '-' + player_id)[0].hasAttribute('checked') && !$('#checkbox-' + team + '-' + player_id)[0].checked) {
            players.push([player_id, $('#pos-' + team + '-' + player_id).val(), $('#number-' + team + '-' + player_id).val()]);
        }
    }

    let csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();
    var data = {csrfmiddlewaretoken, bid, championat, team, players, activity};
    console.log(data);
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        url: '/ajax/save_bid/',
        type: 'POST',
        data: data,
        success: function(response) {
            $('#save-bid-changes-' + championat + '-' + team).attr('disabled', true);
            $('#send-bid-' + championat + '-' + team).attr('disabled', true);
            $('#success-bid-' + championat + '-' + team).css('display', 'inline-block');
        },
        error: function(response) {
            $('#success-bid-' + championat + '-' + team).css('display', 'inline-block');
        }
    });
}

function AddAccess(e) {
    let id_num = e.target.id.split('-')[1] + '-' + e.target.id.split('-')[2];
    var number = false;
    var position = false;

    if ($('#number-' + id_num).is('input') && $('#number-' + id_num).val().length > 0) {
        number = true;
    }
    else if ($('#number-' + id_num).is('span')) {
        number = true;
    }

    if ($('#pos-' + id_num).is('input') && $('#pos-' + id_num).val().length > 0) {
        position = true;
    }
    else if ($('#pos-' + id_num).is('span')) {
        position = true;
    }

    if (position && number) {
        $('#checkbox-' + id_num).removeAttr('disabled');
    }
}

$(document).ready(function(){
    for (i = 0; i < $('[name=player-number').length; i++) {
        $('[name=player-number]')[i].addEventListener('input', AddAccess);
    }
    for (i = 0; i < $('[name=player-pos').length; i++) {
        $('[name=player-pos]')[i].addEventListener('input', AddAccess);
    }

    for (i = 0; i < $('[name=send-bid-btn]').length; i++) {
        $('[name=send-bid-btn]')[i].addEventListener('click', SendBid);
    }
    for (i = 0; i < $('[name=save-bid-btn]').length; i++) {
        $('[name=save-bid-btn]')[i].addEventListener('click', SendBid);
    }
})