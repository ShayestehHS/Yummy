jQuery('#sidebar').theiaStickySidebar({
    additionalMarginTop: 80
});

// Calculate Total
function CalculateItems() {
    let sumItemPrice = 0;
    let price = 0;

    $('.order_total_price').each(function () {
        price = parseFloat($(this).html().substring(1));
        sumItemPrice += (!Number.isNaN(price)) ? price : 0;
    })
    return sumItemPrice;
}

// Calculate prices
function RefreshTable(d_charge = 0) {
    d_charge = (typeof d_charge !== 'function') ? d_charge : 0;
    const sumTotal = CalculateItems() + d_charge;
    $('#total').html('$' + sumTotal);

    const emptyMessage = $('#empty_message'); // 'Your order list is empty'
    if ($('.remove_item').length - 1 === 0) { // Minus 1: because of tr_template
        // Show the message
        emptyMessage.show('slow');
        $('#btn_checkOut').hide('slow');
        $('#order_now').hide('slow');
    } else {
        emptyMessage.hide('slow');
        $('#btn_checkOut').show('slow');
        $('#order_now').show('slow');
    }
}


$(document).ready(function () {
    const d_charge = ($("#td_DCharge").is(":hidden")) ? 0 : parseFloat($("#delivery_charge").val());
    RefreshTable(d_charge);
    // In step_1.html:
    // Set value for fields if (order_detail) is exists
    const scheduleDay_value = $("#selected_dDay").val(); // Check order_detail is exists
    const step1 = $('#Step1_form'); // Check page that is order_1
    if (step1.length && scheduleDay_value != null) {
        const scheduleDay_select = step1.find("#delivery_schedule_day");
        scheduleDay_select.val(scheduleDay_value).change();

        const DeliveryTime_value = $("#selected_dTime").val();
        const DeliveryTime_select = $("#delivery_schedule_time");
        DeliveryTime_select.val(DeliveryTime_value).change();

        const DeliveryMethod_value = $("#selected_dMethod").val();
        const DeliveryMethod_select = $("#delivery_method");
        DeliveryMethod_select.val(DeliveryMethod_value).change();
    }

});
const Url_ajax = $('#url_removeItem').data('url_ajax');

// Removing item
$('#order_table').on('click', '.remove_item', function () {
    const item_full_id = $(this).parent().parent().attr('id');
    const item_id = item_full_id.split('_')[1];
    $.ajax({
        type: 'POST',
        url: Url_ajax,
        data: {
            item_mode: '-',
            item_id: item_id,
        },
        dataType: 'json',
        success: function (data) {
            const quantity = data.quantity;
            const item_tr = $('#' + item_full_id);
            if (quantity === 0) {
                item_tr.fadeOut(300, function () { // remove item from list
                    $(this).remove();
                });
            } else {
                item_tr.find('.order_quantity').html(quantity + "x");
                item_tr.find('.order_total_price').html('$' + data.total_price)
            }
            window.setTimeout(RefreshTable, .5 * 1000);
        }
    });
});

//Add new item
$('.add_to_cart').on('click', function () {
    const item_full_id = $(this).parents().eq(2).attr('id');
    const item_name = item_full_id.split('_')[0];
    const item_id = item_full_id.split('_')[1];
    $.ajax({
        type: 'POST',
        url: Url_ajax,
        data: {
            item_mode: '+',
            item_id: item_id,
        },
        dataType: 'json',
        success: function (data) {
            if (!data.errorMsg) {
                const quantity = data.quantity;
                let trItem = $("#order_" + item_id);
                if (quantity === 1) {
                    trItem = $('#order_parent').clone();
                    trItem.attr('id', 'order_' + item_id);
                    trItem.find('.order_name').html(item_name);
                    trItem.find('.order_total_price').html('$' + data.total_price);
                    $('#order_table').find('tbody').last().append(trItem);
                    trItem.show('slow');
                    trItem.removeAttr('hidden');
                }
                trItem.find('.order_quantity').html(quantity + "x");
                trItem.find('.order_total_price').html('$' + data.total_price)
                RefreshTable();
            } else {
                // User had a Cart in database
                ShowMessageAjax("error", data.errorMsg)
            }
        },
        error: function (data) {
            alert('ERROR\nSorry, we have a problem');
            location.reload();
        }
    })
})


// Select option in step_1.html
$('#delivery_method').change(function () {
    const d_charge = $('.d_charge');
    if ($(this).val() === "Delivery") {
        const delivery_charge = $("#delivery_charge").val();
        RefreshTable(parseFloat(delivery_charge));
        d_charge.find("#d_charge").html("$" + delivery_charge);
        d_charge.show('slow');
        // Here I should add 'delivery charge' to cart
    } else {
        RefreshTable(0);
        d_charge.hide('slow');
    }
})



