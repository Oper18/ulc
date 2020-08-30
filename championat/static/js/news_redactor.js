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

function getNews() {
    $.ajax({
        url: '/ajax/get_news/',
        type: 'GET',
        success: setNews,
        error: function(response) {
            console.log(response);
        }
    });
}

function newsList(props) {
    return <li class="list-group-item">props.head</li>;
}

function setNews(response) {
    const heads = [];
    for (let i = 0; i < response['news'].length; i++) {
        if (response['correct']) {
            const item = (
                <li class="list-group-item">
                    <div class="columns">
                        <a href="#" class="news_link" id={"link_" + response['news'][i]['id']}>
                        <div class="media">
                          <img src={response['news'][i]['head_img']} class="mr-3" height="64px" />
                          <div class="media-body">
                            <h5 class="mt-0" id={"head_" + response['news'][i]['id']}>{response['news'][i]['head']}</h5>
                            <div class="preread" id={"preread_" + response['news'][i]['id']}>{response['news'][i]['preread']}</div>
                            <div class="new-body" id={"body_" + response['news'][i]['id']}>{window.HTMLReactParser(response['news'][i]['news_body'])}</div>
                          </div>
                        </div>
                        </a>
                        <div class="correct_btn">
                            <button type="button" class="btn btn-light correct_modal" id={"correct_" + response['news'][i]['id']}>&#9998;</button>
                        </div>
                    </div>
                </li>
            );
            heads.push(item);
        }
        else {
            const item = (
                <li class="list-group-item">
                    <div class="columns">
                        <a href="#" class="news_link" id={"link_" + response['news'][i]['id']}>
                        <div class="media">
                          <img src={response['news'][i]['head_img']} class="mr-3" height="64px" />
                          <div class="media-body">
                            <h5 class="mt-0" id={"head_" + response['news'][i]['id']}>{response['news'][i]['head']}</h5>
                            <div class="preread" id={"preread_" + response['news'][i]['id']}>{response['news'][i]['preread']}</div>
                            <div class="new-body" id={"body_" + response['news'][i]['id']}>{window.HTMLReactParser(response['news'][i]['news_body'])}</div>
                          </div>
                        </div>
                        </a>
                    </div>
                </li>
            );
            heads.push(item);
        }
    }
    const list = heads.map((h) => <ul class="list-group" id="news-list_id">{h}</ul>);
    ReactDOM.render(list, document.getElementById('root'));
    $('.media').click(openNew);
    $('.correct_modal').click(openModal);
}

function openNew(e) {
    var pk = e.target.id.split('_')[e.target.id.split('_').length - 1];
    $('.preread').css('display', 'block');
    $('.new-body').css('display', 'none');
    $('#preread_' + pk).css('display', 'none');
    $('#body_' + pk).css('display', 'block');
}

function openModal(e) {
    $('#correct_new_head').removeClass('danger-input');
    $('#model_new_title').text('Новость');
    $('#correct_new_head').val('');
    $('#correct_new_preread').text('');
    tinyMCE.activeEditor.setContent('');
    if (e.target.id.split('_').length > 1) {
        $('#model_new_title').text('Новость ' + e.target.id.split('_')[e.target.id.split('_').length - 1]);
        $('#correct_new_head').val($('#head_' + e.target.id.split('_')[e.target.id.split('_').length - 1]).text());
        $('#correct_new_preread').text($('#preread_' + e.target.id.split('_')[e.target.id.split('_').length - 1]).text());
        tinyMCE.activeEditor.setContent($('#body_' + e.target.id.split('_')[e.target.id.split('_').length - 1]).html());
    }
    $('#news_modal').modal('show');
}

function changeNew(e) {
    if ($('#correct_new_head').val() && $('#correct_new_head').val() != '') {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', $('[name=csrfmiddlewaretoken').val());
        data.append('head_img', $('#correct_new_file')[0].files[0]);
        data.append('head', $('#correct_new_head').val());
        data.append('preread', $('#correct_new_preread').val());
        data.append('news_body', tinyMCE.activeEditor.getContent());
        if ($('#model_new_title').text().split(' ').length > 1) {
            data.append('id', $('#model_new_title').text().split(' ')[$('#model_new_title').text().split(' ').length - 1]);
        }
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            url: '/ajax/update_news/',
            type: 'POST',
            data: data,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log(response);
                $('#news_modal').modal('hide');
                getNews();
            },
            error: function(response) {
                console.log(response);
            }
        });
    }
    else {
        $('#correct_new_head').addClass('danger-input');
    }
}

$(document).ready(function(){
    getNews();
    tinymce.init({
        selector: '#correct_new_body',
        plugins: 'a11ychecker advcode casechange formatpainter linkchecker autolink lists checklist media mediaembed pageembed permanentpen powerpaste table advtable tinycomments tinymcespellchecker image link',
        toolbar: 'bullist numlist code image link',
        toolbar_mode: 'floating',
        tinycomments_mode: 'embedded',
        tinycomments_author: 'Author name',
    });
    $('#update_new').click(changeNew);
    $('#close_update').click(function(){
        $('#news_modal').modal('hide');
    });
    $('#correct_new_head').on('input', function() {
        $('#correct_new_head').removeClass('danger-input');
    });
    $('#add-new-btn-id').click(openModal);
})