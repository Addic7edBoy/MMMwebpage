

window.onload = function () {
    let sourceVal = String;
    let targetVal = String;


    $('.form-check-input').on('click', function () {
        console.log($(this).val());
        if ($(this).attr('id').indexOf('src') == 0) {
            console.log('source radio')
            sourceVal = $(this).val()
            switch (sourceVal) {
                case 'vk':
                    $('#sourceLogin').removeAttr('disabled')
                    $('#sourceHelp').text('2 factor auth must be off')
                    $('#sourcePassword').removeAttr('disabled')
                    $('#check-source').removeAttr('disabled')
                    break;

                case 'sp':
                    $('#sourceLogin').removeAttr('disabled')
                    $('#sourceHelp').text('sp needs to verify permissions, press "check"')
                    $('#check-source').removeAttr('disabled')
                    $('#sourcePassword').attr('disabled', 'disabled')
                    break;

                case 'ym':
                    $('#sourceLogin').removeAttr('disabled')
                    $('#sourceHelp').text('')
                    $('#sourcePassword').removeAttr('disabled')
                    $('#check-source').removeAttr('disabled')
                    break;
            }
        } else {
            console.log('target radio')
            targetVal = $(this).val()
            switch (targetVal) {
                case 'sp':
                    $('#trgtLogin').removeAttr('disabled')
                    $('#trgtHelp').text('sp needs to verify permissions, press "check"')
                    $('#check-trgt').removeAttr('disabled')
                    $('#trgtPassword').attr('disabled', 'disabled')
                    break;

                case 'ym':
                    $('#trgtLogin').removeAttr('disabled')
                    $('#trgtHelp').text('')
                    $('#trgtPassword').removeAttr('disabled')
                    $('#check-trgt').removeAttr('disabled')
                    break;
            }
        }
    })

    $('#confirm').on('click', function () {
        $(this).attr('disabled', 'disabled')
        $('.usage-menu').attr('style', 'border-bottom-left-radius: 0rem;')
        $('#progress').collapse('show');
        var playlist_ids = getCheckedPlaylists();
        $.post('/run', {
            s: sourceVal,
            t: targetVal,
            s_login: $('#sourceLogin').val().toLowerCase(),
            s_pass: $('#sourcePassword').val().toLowerCase(),
            t_login: $('#trgtLogin').val().toLowerCase(),
            t_pass: $('#trgtPassword').val().toLowerCase(),
            all: $('#checkAll').prop('checked'),
            artists: $('#checkArtists').prop('checked'),
            albums: $('#checkAlbums').prop('checked'),
            playlists: playlist_ids
        })
    })


    $('#check-source').on('click', function () {
        console.log(sourceVal);
        $('#spinner').show();
        $('#btn-text').html('Loading...')
        switch (sourceVal) {
            case 'vk':
                $.post('/vk-login', {
                    login: $('#sourceLogin').val().toLowerCase(),
                    pass: $('#sourcePassword').val().toLowerCase(),
                    get_playlists: true
                }).done(function (response) {
                    if (response['success'] == 1) {
                        console.log('vk login successful')
                        console.log(response)
                        $('#spinner').hide();
                        $('#btn-text').html('Success')
                        $('#check-source').addClass('btn-success')
                        renderPlaylistDropdown(response['playlist_list'])
                        trgtStep(sourceVal);
                    } else { console.log('ERROR') }
                }).fail(function () {
                    console.log('REQUEST FAILED')
                    $('#spinner').hide();
                    $('#btn-text').html('Retry')
                    $('#check-source').addClass('btn-danger')
                })
                break;

            case 'ym':
                $.post('/ym-login', {
                    login: $('#sourceLogin').val().toLowerCase(),
                    pass: $('#sourcePassword').val().toLowerCase(),
                    get_playlists: true
                }).done(function (response) {
                    if (response['success'] == 1) {
                        console.log('ym login successful');
                        console.log(response);
                        $('#spinner').hide();
                        $('#btn-text').html('Success')
                        $('#check-source').addClass('btn-success')
                        renderPlaylistDropdown(response['playlist_list'])
                        trgtStep(sourceVal);
                    } else { console.log('ERROR') }
                }).fail(function () {
                    console.log('REQUEST FAILED')
                    $('#spinner').hide();
                    $('#btn-text').html('Retry')
                    $('#check-source').addClass('btn-danger')
                })
                break;

            case 'sp':
                $.post('/sp-token', {
                    login: $('#sourceLogin').val().toLowerCase(),
                    get_playlists: true
                }).done(function (response) {
                    if (response['token'] == 1) {
                        console.log('yes token')
                        $('#check-source span').hide();
                        $('#btn-text').html('Success')
                        $('#check-source').addClass('btn-success')
                        renderPlaylistDropdown(response['playlist_list'])
                        trgtStep(sourceVal)
                    }
                    else {
                        console.log('no token')
                        $('#sp-login-btn').attr('href', response['auth_url'])
                        $('#sp-login-btn').show()
                    }
                    console.log(response)
                }).fail(function () {
                    console.log('ERROR')
                    $('#spinner').hide();
                    $('#btn-text').html('Retry')
                    $('#check-source').addClass('btn-danger')
                })
                break;

            default:
                console.log('unexpected value "sourceVal"', sourceVal)
                break;
        }
    })



    $('#check-trgt').on('click', function () {
        $('#spinner2').show();
        $('#btn2-text').html('Loading...')
        switch (targetVal) {

            case 'ym':
                $.post('/ym-login', {
                    login: $('#trgtLogin').val().toLowerCase(),
                    pass: $('#trgtPassword').val().toLowerCase(),
                }).done(function (response) {
                    if (response['success'] == 1) {
                        console.log('ym login successful');
                        console.log(response);
                        $('#spinner2').hide();
                        $('#btn2-text').html('Success')
                        $('#check-trgt').addClass('btn-success')
                        contentStep(sourceVal);
                    } else { console.log('ERROR') }
                }).fail(function () {
                    console.log('REQUEST FAILED')
                    $('#spinner2').hide();
                    $('#btn2-text').html('Retry')
                    $('#check-trgt').addClass('btn-danger')
                })
                break;

            case 'sp':
                $.post('/sp-token', {
                    login: $('#trgtLogin').val().toLowerCase(),
                    get_playlists: false
                }).done(function (response) {
                    if (response['token'] == 1) {
                        console.log('yes token')
                        $('#spinner2').hide();
                        $('#btn2-text').html('Success')
                        $('#check-trgt').addClass('btn-success')
                        contentStep(sourceVal);
                    }
                    else {
                        console.log('no token')
                        $('#sp-login-btn2').attr('href', response['auth_url'])
                        $('#sp-login-btn2').show()
                    }
                }).fail(function () {
                    console.log('ERROR')
                    $('#spinner2').hide();
                    $('#btn2-text').html('Retry')
                    $('#check-trgt').addClass('btn-danger')
                })
                break;

            default:
                console.log('unexpected value "sourceVal"', targetVal)
                break;
        }
    })
}

function renderPlaylistDropdown(playlist_list) {
    for (const [key, value] of Object.entries(playlist_list)) {
        console.log(key, value);
        $("#playlist-dropdown").append("<li><label><input type='checkbox' id='" + value + "'>" + key + "</label></li>")
    }
}

function trgtStep(sourceVal) {
    $('#step2Heading').removeClass('text-muted')
    if (sourceVal == 'sp') {
        $('#trgtRadio2').removeAttr('disabled')
        $('#trgtRadio3').attr('disabled', 'disabled')
    } else if (sourceVal == 'ym') {
        $('#trgtRadio3').removeAttr('disabled')
        $('#trgtRadio2').attr('disabled', 'disabled')
     } else { console.log('unexpected value "sourceval"', sourceVal) }
}

function contentStep(sourceVal){
    if (sourceVal != 'vk')
        $('#checkAll').removeAttr('disabled')
        $('#checkAlbums').removeAttr('disabled')
        $('#checkArtists').removeAttr('disabled')
    $('#dropdownMenu1').removeAttr('disabled')
    $('#confirm').removeAttr('disabled')
    $('#step3Heading').removeClass('text-muted')
}

function getCheckedPlaylists() {
    var selected = []
    $('#playlist-dropdown input:checked').each(function(){
        selected.push($(this).attr('id'))
    })
    return selected
}
