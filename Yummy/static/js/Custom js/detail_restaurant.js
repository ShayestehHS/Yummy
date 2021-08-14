$(document).ready(function ($) {
    $('#Img_carousel').sliderPro({
        width: 960,
        height: 500,
        fade: true,
        arrows: true,
        buttons: false,
        fullScreen: false,
        smallSize: 500,
        startSlide: 0,
        mediumSize: 1000,
        largeSize: 3000,
        thumbnailArrows: true,
        autoplay: false
    });
});

// Review Form
const form = $('#reviForm');
form.submit(function (e) {
    e.preventDefault();
    const Url = $(this).data('url_ajax');
    alert(Url)
    $.ajax({
        type: 'POST',
        url: Url,
        data: form.serialize(),
        dataType: 'json',
        success: function (data) {
            if (!data.error) {
                ShowMessageAjax('success', "Your review is save.");
                location.reload();
            } else {
                ShowMessageAjax('error', data.error)
            }
        },
        error: function (data) {
            alert('ERROR\nSorry, we have a problem');
            location.reload();
        },
    });
})

$(document).ready(function () {
    $(".icon-input-btn").each(function () {
        var btnFont = $(this).find(".btn").css("font-size");
        var btnColor = $(this).find(".btn").css("color");
        $(this).find(".fa").css({'font-size': btnFont, 'color': btnColor});
    });
})
