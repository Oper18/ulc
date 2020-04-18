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

function AnswerBid(e) {
    let bid = e.target.id.split('-')[e.target.id.split('-').length - 1];
    let answer = '';
    if (e.target.name.includes('accept')) {
        answer = 'accept';
    }
    else if (e.target.name.includes('decline')) {
        answer = 'decline';
    }
    let csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();
    var data = {csrfmiddlewaretoken, answer, bid};
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        url: '/ajax/answer_bid/',
        type: 'POST',
        data: data,
        success: function(response) {
            $('#accept-team-bid-' + bid).attr('disabled', true);
            $('#decline-team-bid-' + bid).attr('disabled', true);
        }
    });
}

$(document).ready(function(){
    for (i = 0; i < $('[name=accept-bid-btn]').length; i++) {
        $('[name=accept-bid-btn]')[i].addEventListener('click', AnswerBid);
    }
    for (i = 0; i < $('[name=decline-bid-btn]').length; i++) {
        $('[name=decline-bid-btn]')[i].addEventListener('click', AnswerBid);
    }
})