

window.onload = function() {
    let modal = document.getElementById("myModal");
    let content = document.getElementById('modalContent');
    let login_btns = document.getElementsByClassName('login-btn');
    let auth_btn = document.getElementById('auth');
    console.log(login_btns)
    console.log(modal)

    $(".alert").delay(4000).slideUp(200, function () {
        $(this).alert('close');
    });

    for (var i = 0; i < login_btns.length; i++) {
        login_btns[i].addEventListener("click", function () {
            console.log('clicked')
            $(".modal").fadeIn(500)
        });
        }
        window.addEventListener("click", function(event){
            if (event.target == modal){
                $(".modal").fadeOut(500)
            }
        });
    }
