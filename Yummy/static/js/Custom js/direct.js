$('.directAJAX').on('click', function () {
    var id = $(this).parent().attr('id');
    var destination = id.split('*')[0];
    var searched_type = id.split('*')[1];
    var searched_value = id.split('*')[2];

    if (destination === 'grid'){
        destination = 'http://127.0.0.1:8000/grid_list/';
    }else if (destination === 'list'){
        destination = 'http://127.0.0.1:8000/list_page/'
    }

    if (searched_type === 'tag'){
        destination += 'tag/'+searched_value+'/';
    }
    destination += '1/';

    alert(destination)
    $.ajax({
        type: 'POST',
        async: false,
        url: destination,
        data: {'searched_value':searched_value},
        success: function (data) {
            alert('success');
            $("#Restaurants").html(data);
        },
        error: function (data){
            alert('ERROR\nSorry, we have a problem');
            location.reload();
        }
    })
})