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
    if ($('#login-uri-id').data('target') == 'staff') {
        let home = $('#home-'+num).find('option:selected').data('target');
        let visitors = $('#visitors-'+num).find('option:selected').data('target');
        let home_goals = $('#home-goals-'+num).val();
        let visitors_goals = $('#visitors-goals-'+num).val();
        let slot = $('#game-'+num).find('option:selected').data('target').split('-')[$('#game-'+num).find('option:selected').data('target').split('-').length-1];
        let csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();
        let group = $('#row-'+num).data('target');
        var data = {home, visitors, home_goals, visitors_goals, slot, csrfmiddlewaretoken, num, group};
    }
    else if ($('#login-uri-id').data('target') == 'user') {
        let home_goals = $('#home-goals-'+num).val();
        let visitors_goals = $('#visitors-goals-'+num).val();
        let slot = $('#game-'+num).find('option:selected').data('target').split('-')[$('#game-'+num).find('option:selected').data('target').split('-').length-1];
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
        url: '/ajax/gamesettings/',
        type: 'POST',
        data: data,
        success: function(response) {
            console.log(response);
            $(e.target).parent().parent().addClass('acception');
            $(e.target).attr('disabled', true);
            $('#game-'+num).attr('disabled', true);
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
    }
})