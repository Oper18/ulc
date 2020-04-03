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

function sendAJAX(data, uri, e) {
    console.log(e)
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        url: uri,
        type: 'POST',
        data: data,
        success: function(response){
            console.log(response);
            if (e.id == 'signup-btn-pg-form') {
                sendAJAX(data, '/ajax/login/', $('#signin-btn')[0]);
            }
            else {
                window.location.replace(window.location.origin + response['redirect'])
            }
        },
        error: function(response){
            if (e.id == 'signin-btn') {
                $('#danger-mes').css('display', 'block');
            }
            else if (e.id == 'signin-btn-pg') {
                $('#danger-mes-pg').css('display', 'block');
            }
            else if (e.id == 'signup-btn-pg-form') {
                $('#error-mes-label').css('display', 'block');
            }
            console.log(response);
        }
    });
}

function Login(e) {
    if (e.target.id == 'signin-btn') {
        var u = $('#username-input').val();
        var p = $('#password-input').val();
        var csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();
    }
    else if (e.target.id == 'signin-btn-pg') {
        var u = $('#username-input-pg').val();
        var p = $('#password-input-pg').val();
        var csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();
    }
    var data = {'username': u, 'password': p, 'csrfmiddlewaretoken': csrfmiddlewaretoken, 'uri': window.location.href};

    sendAJAX(data, '/ajax/login/', e.target);
}

function Signup(e) {
    if ($('#username-input-pg').hasClass('success-border') && $('#password-input-pg').hasClass('success-border') &&
        $('#email-input-pg').hasClass('success-border') && $('#firstname-input-pg').hasClass('success-border') &&
        $('#lastname-input-pg').hasClass('success-border')) {

        let username = $('#username-input-pg').val();
        let password = $('#password-input-pg').val();
        let email = $('#email-input-pg').val();
        let first_name = $('#firstname-input-pg').val();
        let last_name = $('#lastname-input-pg').val();
        let csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();

        var data = {username, password, email, first_name, last_name, csrfmiddlewaretoken, 'uri': window.location.href};

        sendAJAX(data, '/ajax/registration/', e.target);
    }
}

function validateName(name) {
    if (/^([A-Z]*[a-z]*[а-я]*[А-Я]*)+([\.-\s]?([A-Z]*[a-z]*[а-я]*[А-Я]*)*)*([A-Z]*[a-z]*[а-я]*[А-Я]*)*$/.test(name))
    {
        return (true)
    }
        return (false)
}

function validateEmail(mail) {
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w+)+$/.test(mail))
    {
        return (true)
    }
        return (false)
}

function validateUserName(name) {
    if (/^[A-Za-z0-9@\.\+-_]+$/.test(name))
    {
        return (true)
    }
        return (false)
}

function testUserName(e) {
    let username = $('#username-input-pg').val();
    let csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();
    var data = {username, csrfmiddlewaretoken};
    if (username.length > 0 && validateUserName(username)) {
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            url: '/ajax/testusername/',
            type: 'POST',
            data: data,
            success: function(response) {
                console.log(response);
                $('#username-input-pg').removeClass('alert-border');
                $('#username-input-pg').addClass('success-border');
            },
            error: function(response) {
                console.log(response);
                $('#username-input-pg').removeClass('success-border');
                $('#username-input-pg').addClass('alert-border');
            }
        });
    }
}

var debouncedUserName = _.debounce(testUserName, 500)

function testName(e) {
    var name = $('#firstname-input-pg').val()
    if (validateName(name) && name.length > 0) {
        $('#firstname-input-pg').removeClass('alert-border');
        $('#firstname-input-pg').addClass('success-border');
    }
    else {
        $('#firstname-input-pg').removeClass('success-border');
        $('#firstname-input-pg').addClass('alert-border');
    }
}

var debouncedName = _.debounce(testName, 500)

function testSurname(e) {
    var name = $('#lastname-input-pg').val()
    if (validateName(name) && name.length > 0) {
        $('#lastname-input-pg').removeClass('alert-border');
        $('#lastname-input-pg').addClass('success-border');
    }
    else {
        $('#lastname-input-pg').removeClass('success-border');
        $('#lastname-input-pg').addClass('alert-border');
    }
}

var debouncedSurname = _.debounce(testSurname, 500)

function testEmail(e) {
    var email = $('#email-input-pg').val()
    if (validateEmail(email) && email.length > 0) {
        $('#email-input-pg').removeClass('alert-border');
        $('#email-input-pg').addClass('success-border');
    }
    else {
        $('#email-input-pg').removeClass('success-border');
        $('#email-input-pg').addClass('alert-border');
    }
}

var debouncedEmail = _.debounce(testEmail, 500)

function testPassword(e) {
    var password = $('#password-input-pg').val()
    if (password.length > 0) {
        $('#password-input-pg').removeClass('alert-border');
        $('#password-input-pg').addClass('success-border');
    }
    else {
        $('#password-input-pg').removeClass('success-border');
        $('#password-input-pg').addClass('alert-border');
    }
}

var debouncedPassword = _.debounce(testPassword, 500)

$(document).ready(function(){
    $('#signin-logo').on('click', function(){
        if ($(this).data('user') == 'anonymous') {
            $('#signin-form').modal('show');
        }
        else {
            window.location.replace(location.origin + '/account/' + $(this).data('user'));
        }
    });

    $('#username-input-pg')[0].addEventListener('input', debouncedUserName);
    $('#password-input-pg')[0].addEventListener('input', debouncedPassword);
    $('#email-input-pg')[0].addEventListener('input', debouncedEmail);
    $('#firstname-input-pg')[0].addEventListener('input', debouncedName);
    $('#lastname-input-pg')[0].addEventListener('input', debouncedSurname);

    $('#signin-btn').on('click', Login);
    $('#signin-btn-pg').on('click', Login);
    $('#signup-btn-pg-form').on('click', Signup);
    $('#logout-btn-pg').on('click', function(e){
        $.ajax({
            url: '/ajax/logout/',
            type: 'GET',
            success: function(response) {
                window.location.replace(window.location.origin + response['redirect']);
            },
            error: function(response) {
                console.log(response);
                $('#invite-mes-label').text('Some went wrong, try later');
                $('#invite-mes-label').css('display', 'block');
            }
        })
    })
})