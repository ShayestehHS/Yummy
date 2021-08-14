// __________Map__________

// Right value in google map
let lat = 50.337628;
// Left value in google map
let lng = 35.699795;
// Token : use for mapbox
mapboxgl.accessToken = $('#mapbox_token').val();
let map;

function ShowMap() {
    map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/satellite-streets-v10',
        center: [lat, lng],
        zoom: 15,
        bearing: 180
    });
}

// Show restaurant icon in map
function ShowIcon() {
    const el = document.createElement('div');
    const srcImg = $('#center_logo').attr("src");
    el.style.backgroundImage = "url(" + srcImg + ")";
    el.style.width = '25px';
    el.style.height = '25px';
    el.style.borderRadius = '50%';
    new mapboxgl.Marker(el).setLngLat([lat, lng]).addTo(map);
}

// Click functionality of 'View on Map'
$("#view_on_map").click(function () {
    lat =$('#lat').val();
    lng = $('#long').val();
    $('#mapBox_logo').remove();
    ShowMap();
    ShowIcon();
});