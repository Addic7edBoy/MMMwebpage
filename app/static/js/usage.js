

window.onload = function () {
    let input_source = document.getElementById("input-source");
    let input_target = document.getElementById("input-target");
    let alltracks_chk = document.getElementById("alltracks_chk");
    let playlists_chk = document.getElementById("playlists_chk");
    let albums_chk = document.getElementById("albums_chk");
    let artists_chk = document.getElementById("artists_chk");

    console.log(input_source);

    $('#input-source').on('click', function () {
        // alert($(this).val());
        console.log($(this).val());
        selected_src = $(this).val();
        switch(selected_src){
            case 'VK':
                alltracks_chk.disabled = true;
                artists_chk.disabled = true;
                albums_chk.disabled = true;
                $('#note1').hide();
                $('#sourcePassword').show();
                break;
            case 'SP':
                // document.getElementById('source-text').innerHTML = 'In order to use Spotify, you need to grand permissions to this app';
                $('#note1').show();
                $('#sourcePassword').hide();
                break;

            default:
                alltracks_chk.disabled = false;
                artists_chk.disabled = false;
                albums_chk.disabled = false;
                $('#note1').hide();
                $('#sourcePassword').show();
                break;
            }

        document.getElementById('source-text').innerHTML = 'Credentials for ' + selected_src
    });
    $('#input-target').on('click', function () {
        // alert($(this).val());
        console.log($(this).val());
        selected_trgt = $(this).val();
        if (selected_trgt == 'SP'){
            $('#note1').show();
            $('#targetPassword').hide();
        } else {
            $('#targetPassword').show();
        }
        document.getElementById('target-text').innerHTML = 'Credentials for ' + selected_trgt;
    });


    $('#submit-button').on('click', function () {
        // $(".modal").fadeOut(500)
        $('#confirm_info').hide();
        $('#progressbar').show();
        var conf = $('#conf').text()
        $.post('/run', {
            s: $('#s').text().toLowerCase(), t: $('#t').text().toLowerCase(), s_user: $('#s_l').text(),
            s_pass: $('#s_p').text(), t: $('#t').text(), t_user: $('#t_l').text(), t_pass: $('#t_p').text(), conf: conf
        }).done(function (response) {
            $('#status-text').text(`Done. Run exit status: ${response}`);
            $('#status-img').hide()
            // $('#img').src = {{ url_for("static", filename="img / success.jpg")}}
            // $('#status-img').html('<img src="{{ url_for("static", filename="img/success.jpg")}}" height="173" width="300" alt="success">')
            $('#back-button').show()
            console.log(response)
        }).fail(function () {
            console.log('ERROR')
            $('#status-img').hide()
            $('#status-text').text('ERROR')
            $('#back-button').show()
        })
    })
}
