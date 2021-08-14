var spinner = $('#subsSpinner');
spinner.hide();
var btnSubmit = $("#submitID");

btnSubmit.click(function (event) {
    event.preventDefault();
    let subsEmail = $('#user_email'); // subscriber Email
    if (subsEmail.val()) {
        $.ajax({
            type: 'POST',
            url: $('#subscribe_form').data('url_ajax'),
            data: {'email': subsEmail.val()},
            dataType: 'json',
            beforeSend: () => spinner.show(),
            success: function (data) {
                if (data.success) {
                    ShowMessageAjax('success', data.success, 1000);
                } else if (data.error) {
                    ShowMessageAjax('error', data.error, 1000);
                }
            },
            error: function () {
                alert('ERROR\nSorry, we have a problem');
                location.reload();
            },
            complete: () => spinner.hide()
        })
    } else {
        // else => subsEmail is null
        alert('Email field is empty');
    }
})