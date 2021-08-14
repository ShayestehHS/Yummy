// Used in
// list_page.html grid_list.html

// Sorter functionality
$('#sort_rating').on('change', function () {
    const mode = this.value;
    const key = $("#searched_key").val();
    const tag = $("#searched_tag").val();
    $.ajax({
        url: $(this).data('url_ajax') + "?mode=" + mode,
        type: 'GET',
        data: {
            'senderPath': window.location.href,
            'key': key,
            'tag': tag,
        },
        async: false,
        success: function (data) {
            $('#Restaurants').html(data);
            $('.page-link').on('click', next_sortPage);
        },
        error: function () {
            alert('ERROR\nSorry, we have a problem');
            location.reload();
        }
    })
})

// toggle 'all' and 'tags' check box
$(".tag_name").change(function () {
    var all_checkbox = $("#all_checkbox");
    var all_checkbox_bool = all_checkbox.is(":checked");

    if ($(this).attr('id') === "all_checkbox") {
        $(".tag_name").not(all_checkbox).each(function () {
            this.checked = all_checkbox_bool;
        })

    } else { // else => clicked checkbox is not all_checkbox
        all_checkbox_bool = $('#tag_list').find('input[name="tag"]:checked').length === $(".tag_name").length - 1;
        all_checkbox.prop('checked', all_checkbox_bool)
    }
});

// This function get the data-tag value of selected tag
function GetSelectedTag() {
    var type = [];
    $('#tag_list :checkbox').not($('[data-number~="0"]')[0]).each(function () {
        if ($(this).is(':checked')) {
            type.push($(this).data("tag"));
        }
    })
    return type
}


$('#submitForm').on('click', function (e) {
    e.preventDefault();
    const Url = $('#FilterForm').data('url_ajax');
    alert(Url)
    $.ajax({
        type: 'GET',
        url: Url,
        async: false,
        data: {
            'type': GetSelectedTag(),
            'rating': $('.filter_type').find('input[name="rating"]:checked').val(),
            'isDelivery': $('#isDelivery').prop('checked'),
            'isTakeAway': $('#isTakeAway').prop('checked'),
            'popularity': $('.PopularOption').find('input[name="popularity"]').prop('checked') === true ? "true" : "false",
            'senderPath': window.location.href,
        },
        success: function (data) {
            $("#Restaurants").html(data);
            $('.page-link').on('click', next_sortPage);
        },
        error: function (data) {
            alert('ERROR\nSorry, we have a problem');
            location.reload();
        },
    });
});

$('.page-link').on('click', next_sortPage);

function next_sortPage(e) {
    const href = $(this).attr('href');
    if (href.indexOf('/sort_restaurants/') >= 0 ||
        href.indexOf('/Filter/') >= 0) {
        e.preventDefault();
        $.ajax({
            url: href,
            type: 'GET',
            success: function (data) {
                $("#Restaurants").html(data);
            },
            error: function () {
                alert('ERROR\nSorry, we have a problem');
                location.reload();
            }
        })
    }
}