document.querySelector('.img__btn').addEventListener('click', function () {
    document.querySelector('.cont').classList.toggle('s--signup');
});

function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

// Check that passwords are match or not
var password = $('#PassWord');
var conPassword = $('#ConPassWord');
conPassword.on('input', function () {
    if (password.val() !== conPassword.val()) {
        password.css('box-shadow', '0px 14px 12px -5px #FF3D0F');
        conPassword.css('box-shadow', '0px 14px 12px -5px #FF3D0F');
    } else {
        password.css('box-shadow', '0px 14px 12px -5px #44FF36');
        conPassword.css('box-shadow', '0px 14px 12px -5px #44FF36');
    }
})


$(document).ready(function () {
    $('footer').remove();

    // AJAX for fields
    var emailField = $('#Email');
    emailField.on('input', function () {
        if ($(this).val() !== "") {
            if (validateEmail($(this).val())) {
                $.ajax({
                    type: 'POST',
                    url: $('#signUp_form').attr('action'),
                    data: {'email': emailField.val()},
                    dataType: 'json',
                    success: function (data) {
                        if (data.email === "True") {
                            emailField.css('box-shadow', '0px 14px 12px -5px #44FF36');
                        } else if (data.email === "False") {
                            emailField.css('box-shadow', '0px 14px 12px -5px #FF3D0F');
                        }
                    }
                })
            } else {
                // validateEmail : returned false
                emailField.css("box-shadow", "none");
            }
        } else {
            // emailField.value is null
            emailField.css("box-shadow", "none");
        }
    })
})