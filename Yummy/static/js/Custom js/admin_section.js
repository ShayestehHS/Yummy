new CBPFWTabs(document.getElementById('tabs'));
$('.wysihtml5').wysihtml5({});

/////////////
var modal = $("#DeleteConf_Modal");
$('.minimize').on('click', function () {
    $(this).toggleClass('arrow_carrot-2dwnn_alt arrow_carrot-2up_alt'); // toggle icon
    $(this).attr('title', (_, attr) => attr === 'Maximize' ? 'Minimize' : 'Maximize'); // toggle tooltip
});
$('.delete').on('click', function () {
    var selected_item_name = $(this).parents().eq(2).find('.item_name').html();
    var selected_item_id = $(this).parent().parent().find('.item_id').val();
    modal.find('#modal_item_name').html(selected_item_name);
    modal.data('item-id', selected_item_id);
});
$('.save').on('click', function () {
    const editedItem_id = $(this).parent().parent().find('.item_id').val();
    const editedItem = $('#item_' + editedItem_id);
    const editedItem_name = editedItem.find('.MenuForm_name').val();
    const editedItem_category = editedItem.find('.MenuForm_category').find(":selected").text();
    const editedItem_price = editedItem.find('.MenuForm_price').val();
    const editedItem_description = editedItem.find('.MenuForm_description').val();

    const Url = $('#UrlAJAX_updateItem').val();
    $.ajax({
        url: Url,
        type: 'POST',
        data: {
            'id': editedItem_id,
            'name': editedItem_name,
            'category': editedItem_category,
            'price': editedItem_price,
            'description': editedItem_description,
        },
        success: () => ShowMessageAjax('success', 'Your item is updated 😉'),
        error: function () {
            alert('ERROR\nSorry, we have a problem');
            location.reload();
        }
    })
});


$('#modal_delete_btn').on('click', function () {
    var Url = $("#UrlAJAX_deleteItem").val();
    var item_id = modal.data('item-url_ajax')
    $.ajax({
        url: Url,
        type: 'POST',
        dataType: 'json',
        data: {
            item_ID: item_id,
        },
        success: function (data) {
            if (data.result === 'success') {
                const removedItem = $("#item_" + item_id);
                // Refresh number of each item
                RefreshList(removedItem.find('h4').data('number'));
                // Remove item form list
                removedItem.fadeOut("normal", () => $(this).remove());
                ShowMessageAjax('success', 'Your item is deleted from menu 😉');
            }
        },
        error: function (data) {
            alert('ERROR\nSorry, we have a problem');
            location.reload();
        },
    })
    const removedItem = $("#item_" + item_id);
    // Refresh number of each item
    RefreshList(removedItem.find('h4').data('number'));
    // Remove item form list
    removedItem.fadeOut("normal", () => removedItem.remove());
});

$("#Add_item").on('click', function () {
    const Url = $("#UrlAJAX_addItem").val();
    const form = $("#MenuForm");
    $.ajax({
        url: Url,
        type: "GET",
        data: {'form': form.serialize()},
        async: false,
        success: function (data) {
            $('#all_items').html(data);
        }
    })
});

$("#MenuForm").on('submit', function (e) {
    e.preventDefault();
    const form = $(this);
    $.ajax({
        url: form.attr('action'),
        type: form.attr('method'),
        dataType: false,
        processData: false,
        contentType: false,
        data: new FormData($("#MenuForm")[0]),
        success: function (data) {
            $('#MenuForm')[0].reset();
            $('#all_items').html(data);
            ShowMessageAjax('success', 'Your item is saved 😉');
        },
        error: function () {
            alert('ERROR\nSorry, we have a problem');
            location.reload();
        }
    })
})

function RefreshList(removedItem_data_number) {
    const nextItems_h4 = $('.item').find('h4').filter(function () {
        return $(this).data("number") > removedItem_data_number;
    });

    let old_dataNumber, itemName;
    nextItems_h4.each(function (index) {
        old_dataNumber = $(this).data('number');
        itemName = $(this).html().split(')')[1];
        $(this).data('number', old_dataNumber - 1);
        $(this).html($(this).data('number') + ') ' + itemName);
    });
}