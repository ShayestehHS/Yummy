$("#contactsForm").on('submit', function (e) {
    e.preventDefault();
    const Url = $(this).find('#UrlAJAX_sendEmail').val()
    alert(Url)
    $.ajax({
        url: Url,
        type: 'POST',
        data: $(this).serialize(),
        success: function (data) {
            if (data.success) {
                ShowMessageAjax('success', data.success, 3000);
            }
        },
        error: function () {
            alert('ERROR\nSorry, we have a problem');
            location.reload();
        }
    })
})