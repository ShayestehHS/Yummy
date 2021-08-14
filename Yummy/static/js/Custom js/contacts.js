$("#contactsForm").on('submit', function (e) {
    e.preventDefault();
    const Url = $(this).find('#UrlAJAX_sendEmail').val()
    alert(Url)
    $.ajax({
        url: Url,
        type: 'POST',
        data: $(this).serialize(),
        success: function () {
            ShowMessageAjax('success',
                "We received your emailThanks for your email",
                3000);
        },
        error: function () {
            alert('ERROR\nSorry, we have a problem');
            location.reload();
        }
    })
})