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

function AcceptChanges(e) {
    $(e.target).parent().parent().removeClass('acception');
    $(e.target).parent().parent().removeClass('decline');
    var num = e.target.id.split('-')[e.target.id.split('-').length-1]
    if ($('#signin-logo').data('target') == 'staff') {
        let home = $('#home-'+num).find('option:selected').data('target');
        let visitors = $('#visitors-'+num).find('option:selected').data('target');
        let home_goals = $('#home-goals-'+num).val();
        let visitors_goals = $('#visitors-goals-'+num).val();
        let slot = $('#game-'+num).find('option:selected').data('target').split('-')[$('#game-'+num).find('option:selected').data('target').split('-').length-1];
        let csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();
        let group = $('#row-'+num).data('target');
        var data = {home, visitors, home_goals, visitors_goals, slot, csrfmiddlewaretoken, num, group};
    }
    else if ($('#signin-logo').data('target') == 'user') {
        let home_goals = $('#home-goals-'+num).val();
        let visitors_goals = $('#visitors-goals-'+num).val();
        if ( $('#game-'+num).find('option:selected').data('target') ){
            var slot = $('#game-'+num).find('option:selected').data('target').split('-')[$('#game-'+num).find('option:selected').data('target').split('-').length-1];
        }
        else {
            var slot = null;
        }
        let group = $('#row-'+num).data('target');
        let csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();
        var data = {home_goals, visitors_goals, slot, csrfmiddlewaretoken, num, group};
    }
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        url: '/ajax/request/accept/',
        type: 'POST',
        data: data,
        success: function(response) {
            console.log(response);
            $(e.target).parent().parent().addClass('acception');
            $(e.target).attr('disabled', true);
            $('#decline-'+num).removeAttr('disabled');
            $('#game-'+num).attr('disabled', true);
            $('#home-goals-'+num).attr('disabled', true);
            $('#visitors-goals-'+num).attr('disabled', true);
        },
        error: function(response) {
            console.log(response);
            $(e.target).parent().parent().addClass('decline');
        }
    });
}

function DeclineChanges(e) {
    $(e.target).parent().parent().removeClass('acception');
    $(e.target).parent().parent().removeClass('decline');
    var num = e.target.id.split('-')[e.target.id.split('-').length-1]
    if ($('#signin-logo').data('target') == 'staff') {
        let home = $('#home-'+num).find('option:selected').data('target');
        let visitors = $('#visitors-'+num).find('option:selected').data('target');
        let csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();
        var data = {home, visitors, csrfmiddlewaretoken, num};
    }
    else if ($('#signin-logo').data('target') == 'user') {
        let csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();
        var data = {csrfmiddlewaretoken, num};
    }
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        url: '/ajax/request/decline/',
        type: 'POST',
        data: data,
        success: function(response) {
            console.log(response);
            $(e.target).parent().parent().addClass('acception');
            $(e.target).attr('disabled', true);
            $('#accept-'+num).removeAttr('disabled');
            $('#game-'+num).removeAttr('disabled');
            $('#home-goals-'+num).removeAttr('disabled');
            $('#visitors-goals-'+num).removeAttr('disabled');
        },
        error: function(response) {
            console.log(response);
            $(e.target).parent().parent().addClass('decline');
        }
    });
}

$(document).ready(function(){
    var accepts = document.getElementsByName('accept-changed-btn');
    var declines = document.getElementsByName('decline-changed-btn');
    for(i = 0; i < accepts.length; i++) {
        accepts[i].onclick = AcceptChanges;
    };
    for(i = 0; i < declines.length; i++) {
        declines[i].onclick = DeclineChanges;
    };
})