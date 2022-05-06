function sign_up() {
    let email = $('#email').val();
    let pw = $('#pw').val();

    $.ajax({
        type: "POST",
        url: "/sign_up",
        data: {
            'email_give': email,
            'pw_give': pw,
        },
        success: function (response) {
            alert("회원가입을 축하드립니다!")
            window.location.replace("/login")
        }
    });
}

function sign_in() {
    let email = $('#email').val();
    let pw = $('#pw').val();

    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            'email_give': email,
            'pw_give': pw,
        },
        success: function (response) {
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token']);
                window.location.replace("/")
            }
        }
    });
}